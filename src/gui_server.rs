use std::net::SocketAddr;
use std::sync::{Arc, Mutex};

use axum::body::Body;
use axum::extract::{Path, Query, State};
use axum::http::{StatusCode, Uri, header};
use axum::response::{IntoResponse, Response};
use axum::routing::{get, post};
use axum::{Json, Router};
use serde::Deserialize;

use crate::mcp::{
  EndSessionRequest, GameSessionStore, GetActionCatalogRequest, GetCampaignCoverageRequest,
  GetHistoryRequest, GetObservationRequest, GetPresentationRequest, GetRegionalWorldRequest,
  GetReplayRequest, GetResolutionRequest, HistoryEnvelope, LoadSessionRequest, McpErrorMessage,
  SaveSessionRequest, StartSessionRequest, SubmitTurnRequest, ValidateTurnRequest,
};

const DEFAULT_BIND: &str = "127.0.0.1:7878";
const HOST_ADAPTER_MARKER: &str = "<!-- HS_MGT_GAME_HOST_ADAPTER -->";
const GUI_HISTORY_CAMPAIGN: &str = "competitive-regional-v1";
const GUI_CAMPAIGN_COVERAGE_CAMPAIGNS: [&str; 3] = [
  "competitive-regional-v1",
  "stabilization-v1",
  "regional-affiliation-v1",
];

#[derive(Clone, Default)]
struct GuiState {
  store: Arc<Mutex<GameSessionStore>>,
}

impl GuiState {
  fn with_competitive_persistence(path: std::path::PathBuf) -> Self {
    Self {
      store: Arc::new(Mutex::new(GameSessionStore::with_competitive_persistence(
        path,
      ))),
    }
  }
}

#[derive(Debug, Deserialize)]
#[serde(deny_unknown_fields)]
struct GuiStartSessionRequest {
  campaign: String,
  seed: Option<u64>,
  difficulty: Option<String>,
}

#[derive(Debug, Deserialize)]
struct CommandBody {
  command_text: String,
}

#[derive(Debug, Default, Deserialize)]
struct ResolutionQuery {
  turn: Option<u32>,
}

#[derive(Debug, Default, Deserialize)]
struct CheckpointArtifactQuery {
  storage: Option<String>,
}

pub fn parse_bind_args(args: impl IntoIterator<Item = String>) -> Result<SocketAddr, String> {
  let mut args = args.into_iter();
  let _program = args.next();
  let mut bind = DEFAULT_BIND.to_string();
  while let Some(argument) = args.next() {
    match argument.as_str() {
      "--bind" => {
        bind = args
          .next()
          .ok_or_else(|| "--bind requires a loopback IP address and port".to_string())?;
      }
      "--help" | "-h" => {
        return Err(format!("usage: vital-margin-gui [--bind {DEFAULT_BIND}]"));
      }
      _ => return Err(format!("unknown argument: {argument}")),
    }
  }
  let address = bind
    .parse::<SocketAddr>()
    .map_err(|error| format!("invalid bind address '{bind}': {error}"))?;
  ensure_loopback(address)?;
  Ok(address)
}

fn ensure_loopback(address: SocketAddr) -> Result<(), String> {
  if address.ip().is_loopback() {
    Ok(())
  } else {
    Err(format!(
      "GUI host must bind to a loopback address, not {}",
      address.ip()
    ))
  }
}

pub async fn run_gui_server(address: SocketAddr) -> Result<(), Box<dyn std::error::Error>> {
  ensure_loopback(address).map_err(std::io::Error::other)?;
  let listener = tokio::net::TcpListener::bind(address).await?;
  let local = listener.local_addr()?;
  println!("Vital Margin GUI: http://{local}");
  let save_path = crate::cli::gui_competitive_session_save_path();
  println!(
    "Keep this terminal running. Explicit GUI checkpoints use the host archive rooted at {}.",
    save_path.display()
  );
  axum::serve(listener, gui_router_with_persistence(save_path))
    .with_graceful_shutdown(shutdown_signal())
    .await?;
  Ok(())
}

async fn shutdown_signal() {
  let _ = tokio::signal::ctrl_c().await;
}

#[cfg(test)]
fn gui_router() -> Router {
  gui_router_with_state(GuiState::default())
}

fn gui_router_with_persistence(path: std::path::PathBuf) -> Router {
  gui_router_with_state(GuiState::with_competitive_persistence(path))
}

fn gui_router_with_state(state: GuiState) -> Router {
  Router::new()
    .route("/api/v1/checkpoints", get(list_checkpoints))
    .route(
      "/api/v1/sessions/{session_id}/save-artifact",
      get(download_checkpoint_artifact),
    )
    .route("/api/v1/sessions", post(start_session))
    .route("/api/v1/sessions/{session_id}", get(get_session))
    .route(
      "/api/v1/sessions/{session_id}/presentation",
      get(get_presentation),
    )
    .route(
      "/api/v1/sessions/{session_id}/campaign-coverage",
      get(get_campaign_coverage),
    )
    .route(
      "/api/v1/sessions/{session_id}/action-catalog",
      get(get_action_catalog),
    )
    .route(
      "/api/v1/sessions/{session_id}/validation",
      post(validate_turn),
    )
    .route("/api/v1/sessions/{session_id}/turns", post(submit_turn))
    .route(
      "/api/v1/sessions/{session_id}/resolution",
      get(get_resolution),
    )
    .route(
      "/api/v1/sessions/{session_id}/regional-world",
      get(get_regional_world),
    )
    .route("/api/v1/sessions/{session_id}/history", get(get_history))
    .route("/api/v1/sessions/{session_id}/replay", get(get_replay))
    .route("/api/v1/sessions/{session_id}/save", post(save_session))
    .route("/api/v1/sessions/{session_id}/load", post(load_session))
    .route("/api/v1/sessions/{session_id}/end", post(end_session))
    .fallback(get(static_asset))
    .with_state(state)
}

async fn list_checkpoints(State(state): State<GuiState>) -> Response {
  with_store(&state, |store| store.get_checkpoint_discovery())
}

async fn download_checkpoint_artifact(
  State(state): State<GuiState>,
  Path(session_id): Path<String>,
  Query(query): Query<CheckpointArtifactQuery>,
) -> Response {
  let artifact = match state.store.lock() {
    Ok(store) => store.read_checkpoint_artifact(&session_id, query.storage.as_deref()),
    Err(_) => {
      return store_lock_error_response();
    }
  };
  match artifact {
    Ok(bytes) => Response::builder()
      .status(StatusCode::OK)
      .header(header::CONTENT_TYPE, "application/octet-stream")
      .header(
        header::CONTENT_DISPOSITION,
        format!("attachment; filename=\"hs-mgt-checkpoint-{session_id}.save\""),
      )
      .body(Body::from(bytes))
      .expect("valid checkpoint artifact response headers")
      .into_response(),
    Err(error) => checkpoint_artifact_error_response(error),
  }
}

async fn start_session(
  State(state): State<GuiState>,
  Json(request): Json<GuiStartSessionRequest>,
) -> Response {
  if request.campaign != GUI_HISTORY_CAMPAIGN
    && !GUI_CAMPAIGN_COVERAGE_CAMPAIGNS.contains(&request.campaign.as_str())
  {
    return (
      StatusCode::BAD_REQUEST,
      Json(McpErrorMessage {
        error: "live GUI supports competitive-regional-v1, stabilization-v1, and regional-affiliation-v1 only".to_string(),
        code: Some("unsupported_gui_campaign".to_string()),
        resource_limit: None,
        hint: Some("Choose a supported launcher campaign or use cargo run for a custom scenario.".to_string()),
      }),
    )
      .into_response();
  }
  with_store(&state, |store| {
    store.start_session(StartSessionRequest {
      campaign: request.campaign,
      seed: request.seed,
      difficulty: request.difficulty,
      scenario_path: None,
    })
  })
}

async fn get_session(State(state): State<GuiState>, Path(session_id): Path<String>) -> Response {
  with_store(&state, |store| {
    store.get_observation(GetObservationRequest { session_id })
  })
}

async fn get_presentation(
  State(state): State<GuiState>,
  Path(session_id): Path<String>,
) -> Response {
  with_store(&state, |store| {
    store.get_presentation(GetPresentationRequest { session_id })
  })
}

async fn get_campaign_coverage(
  State(state): State<GuiState>,
  Path(session_id): Path<String>,
) -> Response {
  with_store(&state, |store| {
    store.get_campaign_coverage(GetCampaignCoverageRequest { session_id })
  })
}

async fn get_action_catalog(
  State(state): State<GuiState>,
  Path(session_id): Path<String>,
) -> Response {
  with_store(&state, |store| {
    store.get_action_catalog(GetActionCatalogRequest { session_id })
  })
}

async fn validate_turn(
  State(state): State<GuiState>,
  Path(session_id): Path<String>,
  Json(body): Json<CommandBody>,
) -> Response {
  with_store(&state, |store| {
    store.validate_turn(ValidateTurnRequest {
      session_id,
      command_text: body.command_text,
    })
  })
}

async fn submit_turn(
  State(state): State<GuiState>,
  Path(session_id): Path<String>,
  Json(body): Json<CommandBody>,
) -> Response {
  with_store(&state, |store| {
    store.submit_turn(SubmitTurnRequest {
      session_id,
      command_text: body.command_text,
    })
  })
}

async fn get_resolution(
  State(state): State<GuiState>,
  Path(session_id): Path<String>,
  Query(query): Query<ResolutionQuery>,
) -> Response {
  with_store(&state, |store| {
    store.get_resolution(GetResolutionRequest {
      session_id,
      turn: query.turn,
    })
  })
}

async fn get_regional_world(
  State(state): State<GuiState>,
  Path(session_id): Path<String>,
) -> Response {
  with_store(&state, |store| {
    store.get_regional_world(GetRegionalWorldRequest { session_id })
  })
}

fn get_competitive_history(
  store: &mut GameSessionStore,
  session_id: String,
) -> Result<HistoryEnvelope, McpErrorMessage> {
  let history = store.get_history(GetHistoryRequest { session_id })?;
  if history.campaign != GUI_HISTORY_CAMPAIGN {
    return Err(McpErrorMessage {
      error: "live GUI history currently supports competitive-regional-v1 only".to_string(),
      code: Some("unsupported_gui_campaign_history".to_string()),
      resource_limit: None,
      hint: Some("Use the campaign-specific host history interface.".to_string()),
    });
  }
  Ok(history)
}

async fn get_history(State(state): State<GuiState>, Path(session_id): Path<String>) -> Response {
  with_store(&state, |store| get_competitive_history(store, session_id))
}

async fn get_replay(State(state): State<GuiState>, Path(session_id): Path<String>) -> Response {
  with_store(&state, |store| {
    store.get_replay(GetReplayRequest { session_id })
  })
}

async fn save_session(State(state): State<GuiState>, Path(session_id): Path<String>) -> Response {
  with_store(&state, |store| {
    store.save_session(SaveSessionRequest { session_id })
  })
}

async fn load_session(State(state): State<GuiState>, Path(session_id): Path<String>) -> Response {
  with_store(&state, |store| {
    store.load_session(LoadSessionRequest { session_id })
  })
}

async fn end_session(State(state): State<GuiState>, Path(session_id): Path<String>) -> Response {
  with_store(&state, |store| {
    store.end_session(EndSessionRequest { session_id })
  })
}

fn with_store<T>(
  state: &GuiState,
  run: impl FnOnce(&mut GameSessionStore) -> Result<T, McpErrorMessage>,
) -> Response
where
  T: serde::Serialize,
{
  match state.store.lock() {
    Ok(mut store) => match run(&mut store) {
      Ok(value) => Json(value).into_response(),
      Err(error) => error_response(error),
    },
    Err(_) => store_lock_error_response(),
  }
}

fn error_response(error: McpErrorMessage) -> Response {
  let status = if error.error.starts_with("unknown session") {
    StatusCode::NOT_FOUND
  } else {
    StatusCode::BAD_REQUEST
  };
  (status, Json(error)).into_response()
}

fn checkpoint_artifact_error_response(error: McpErrorMessage) -> Response {
  let status = if error.code.as_deref() == Some("checkpoint_missing") {
    StatusCode::NOT_FOUND
  } else {
    StatusCode::BAD_REQUEST
  };
  (status, Json(error)).into_response()
}

fn store_lock_error_response() -> Response {
  (
    StatusCode::INTERNAL_SERVER_ERROR,
    Json(McpErrorMessage {
      error: "GUI session store lock failed".to_string(),
      code: Some("session_store_unavailable".to_string()),
      resource_limit: None,
      hint: None,
    }),
  )
    .into_response()
}

async fn static_asset(uri: Uri) -> Response {
  let path = uri.path();
  let (content_type, content) = match path {
    "/" | "/index.html" => (
      "text/html; charset=utf-8",
      include_str!("../gui/index.html").replace(
        HOST_ADAPTER_MARKER,
        r#"<script type="module" src="./host-adapter.mjs"></script>"#,
      ),
    ),
    "/app.mjs" => (
      "text/javascript; charset=utf-8",
      include_str!("../gui/app.mjs").to_string(),
    ),
    "/ambience-contract.mjs" => (
      "text/javascript; charset=utf-8",
      include_str!("../gui/ambience-contract.mjs").to_string(),
    ),
    "/asset-availability.mjs" => (
      "text/javascript; charset=utf-8",
      include_str!("../gui/asset-availability.mjs").to_string(),
    ),
    "/asset-credits-renderer.mjs" => (
      "text/javascript; charset=utf-8",
      include_str!("../gui/asset-credits-renderer.mjs").to_string(),
    ),
    "/asset-credits.mjs" => (
      "text/javascript; charset=utf-8",
      include_str!("../gui/asset-credits.mjs").to_string(),
    ),
    "/audio-cue-contract.mjs" => (
      "text/javascript; charset=utf-8",
      include_str!("../gui/audio-cue-contract.mjs").to_string(),
    ),
    "/audio-priority-contract.mjs" => (
      "text/javascript; charset=utf-8",
      include_str!("../gui/audio-priority-contract.mjs").to_string(),
    ),
    "/audio.mjs" => (
      "text/javascript; charset=utf-8",
      include_str!("../gui/audio.mjs").to_string(),
    ),
    "/consequence-links.mjs" => (
      "text/javascript; charset=utf-8",
      include_str!("../gui/consequence-links.mjs").to_string(),
    ),
    "/facility-components.mjs" => (
      "text/javascript; charset=utf-8",
      include_str!("../gui/facility-components.mjs").to_string(),
    ),
    "/first-month.mjs" => (
      "text/javascript; charset=utf-8",
      include_str!("../gui/first-month.mjs").to_string(),
    ),
    "/workspace.mjs" => (
      "text/javascript; charset=utf-8",
      include_str!("../gui/workspace.mjs").to_string(),
    ),
    "/metric-visualizations.mjs" => (
      "text/javascript; charset=utf-8",
      include_str!("../gui/metric-visualizations.mjs").to_string(),
    ),
    "/music-stem-contract.mjs" => (
      "text/javascript; charset=utf-8",
      include_str!("../gui/music-stem-contract.mjs").to_string(),
    ),
    "/operational-overlays.mjs" => (
      "text/javascript; charset=utf-8",
      include_str!("../gui/operational-overlays.mjs").to_string(),
    ),
    "/host-adapter.mjs" => (
      "text/javascript; charset=utf-8",
      include_str!("../gui/host-adapter.mjs").to_string(),
    ),
    "/playtest.mjs" => (
      "text/javascript; charset=utf-8",
      include_str!("../gui/playtest.mjs").to_string(),
    ),
    "/regional-board.mjs" => (
      "text/javascript; charset=utf-8",
      include_str!("../gui/regional-board.mjs").to_string(),
    ),
    "/resolution-sequence.mjs" => (
      "text/javascript; charset=utf-8",
      include_str!("../gui/resolution-sequence.mjs").to_string(),
    ),
    "/scene.mjs" => (
      "text/javascript; charset=utf-8",
      include_str!("../gui/scene.mjs").to_string(),
    ),
    "/visual.mjs" => (
      "text/javascript; charset=utf-8",
      include_str!("../gui/visual.mjs").to_string(),
    ),
    "/audio-catalog.json" => (
      "application/json",
      include_str!("../gui/audio-catalog.json").to_string(),
    ),
    "/visual-catalog.json" => (
      "application/json",
      include_str!("../gui/visual-catalog.json").to_string(),
    ),
    _ => return StatusCode::NOT_FOUND.into_response(),
  };
  ([(header::CONTENT_TYPE, content_type)], content).into_response()
}

#[cfg(test)]
mod tests {
  use super::*;
  use crate::mcp::gui_session_checkpoint_path;
  use tokio::io::{AsyncReadExt, AsyncWriteExt};

  #[test]
  fn bind_arguments_default_to_loopback_and_reject_remote_addresses() {
    assert_eq!(
      parse_bind_args(["gui".to_string()]).expect("default bind"),
      "127.0.0.1:7878".parse::<SocketAddr>().unwrap()
    );
    let error = parse_bind_args([
      "gui".to_string(),
      "--bind".to_string(),
      "0.0.0.0:7878".to_string(),
    ])
    .expect_err("remote bind must fail");
    assert!(error.contains("loopback"));
  }

  #[test]
  fn ipv4_and_ipv6_loopback_are_allowed() {
    assert!(ensure_loopback("127.0.0.1:0".parse().unwrap()).is_ok());
    assert!(ensure_loopback("[::1]:0".parse().unwrap()).is_ok());
    assert!(
      ensure_loopback(SocketAddr::new(
        std::net::IpAddr::from([192, 0, 2, 1]),
        7878
      ))
      .is_err()
    );
  }

  #[test]
  fn gui_history_rejects_noncompetitive_campaigns() {
    let mut store = GameSessionStore::default();
    let session = store
      .start_session(StartSessionRequest {
        campaign: "stabilization-v1".to_string(),
        seed: Some(42),
        difficulty: None,
        scenario_path: None,
      })
      .expect("stabilization session");
    let error = get_competitive_history(&mut store, session.session_id)
      .expect_err("GUI history must reject stabilization");
    assert_eq!(
      error.code.as_deref(),
      Some("unsupported_gui_campaign_history")
    );
  }

  async fn test_server() -> (SocketAddr, tokio::task::JoinHandle<()>) {
    let listener = tokio::net::TcpListener::bind("127.0.0.1:0").await.unwrap();
    let address = listener.local_addr().unwrap();
    let task = tokio::spawn(async move {
      axum::serve(listener, gui_router()).await.unwrap();
    });
    (address, task)
  }

  async fn test_server_with_persistence(
    path: std::path::PathBuf,
  ) -> (SocketAddr, tokio::task::JoinHandle<()>) {
    let listener = tokio::net::TcpListener::bind("127.0.0.1:0").await.unwrap();
    let address = listener.local_addr().unwrap();
    let task = tokio::spawn(async move {
      axum::serve(listener, gui_router_with_persistence(path))
        .await
        .unwrap();
    });
    (address, task)
  }

  async fn request(
    address: SocketAddr,
    method: &str,
    path: &str,
    body: Option<&str>,
  ) -> (u16, String) {
    let (status, _headers, body) = request_with_headers(address, method, path, body).await;
    (status, body)
  }

  async fn request_with_headers(
    address: SocketAddr,
    method: &str,
    path: &str,
    body: Option<&str>,
  ) -> (u16, String, String) {
    let body = body.unwrap_or("");
    let mut stream = tokio::net::TcpStream::connect(address).await.unwrap();
    let request = format!(
      "{method} {path} HTTP/1.1\r\nHost: {address}\r\nContent-Type: application/json\r\nContent-Length: {}\r\nConnection: close\r\n\r\n{body}",
      body.len()
    );
    stream.write_all(request.as_bytes()).await.unwrap();
    let mut response = Vec::new();
    stream.read_to_end(&mut response).await.unwrap();
    let response = String::from_utf8(response).unwrap();
    let (head, body) = response.split_once("\r\n\r\n").unwrap();
    let status = head
      .split_whitespace()
      .nth(1)
      .unwrap()
      .parse::<u16>()
      .unwrap();
    (status, head.to_string(), body.to_string())
  }

  #[tokio::test]
  async fn live_gui_embeds_complete_offline_module_graph() {
    let (address, server) = test_server().await;
    let resources = [
      ("/host-adapter.mjs", include_str!("../gui/host-adapter.mjs")),
      (
        "/ambience-contract.mjs",
        include_str!("../gui/ambience-contract.mjs"),
      ),
      ("/app.mjs", include_str!("../gui/app.mjs")),
      (
        "/asset-availability.mjs",
        include_str!("../gui/asset-availability.mjs"),
      ),
      (
        "/asset-credits-renderer.mjs",
        include_str!("../gui/asset-credits-renderer.mjs"),
      ),
      (
        "/asset-credits.mjs",
        include_str!("../gui/asset-credits.mjs"),
      ),
      (
        "/audio-cue-contract.mjs",
        include_str!("../gui/audio-cue-contract.mjs"),
      ),
      (
        "/audio-priority-contract.mjs",
        include_str!("../gui/audio-priority-contract.mjs"),
      ),
      ("/audio.mjs", include_str!("../gui/audio.mjs")),
      (
        "/consequence-links.mjs",
        include_str!("../gui/consequence-links.mjs"),
      ),
      (
        "/facility-components.mjs",
        include_str!("../gui/facility-components.mjs"),
      ),
      ("/first-month.mjs", include_str!("../gui/first-month.mjs")),
      ("/workspace.mjs", include_str!("../gui/workspace.mjs")),
      (
        "/metric-visualizations.mjs",
        include_str!("../gui/metric-visualizations.mjs"),
      ),
      (
        "/music-stem-contract.mjs",
        include_str!("../gui/music-stem-contract.mjs"),
      ),
      (
        "/operational-overlays.mjs",
        include_str!("../gui/operational-overlays.mjs"),
      ),
      ("/playtest.mjs", include_str!("../gui/playtest.mjs")),
      (
        "/regional-board.mjs",
        include_str!("../gui/regional-board.mjs"),
      ),
      (
        "/resolution-sequence.mjs",
        include_str!("../gui/resolution-sequence.mjs"),
      ),
      ("/scene.mjs", include_str!("../gui/scene.mjs")),
      ("/visual.mjs", include_str!("../gui/visual.mjs")),
      (
        "/audio-catalog.json",
        include_str!("../gui/audio-catalog.json"),
      ),
      (
        "/visual-catalog.json",
        include_str!("../gui/visual-catalog.json"),
      ),
    ];
    for (path, expected) in resources {
      let (status, body) = request(address, "GET", path, None).await;
      assert_eq!(status, 200, "{path}: {body}");
      assert_eq!(body, expected, "{path} did not return its embedded source");
    }
    for path in ["/", "/index.html"] {
      let (status, body) = request(address, "GET", path, None).await;
      assert_eq!(status, 200, "{path}: {body}");
      assert!(
        body.contains("host-adapter.mjs"),
        "{path} omitted host adapter"
      );
    }
    server.abort();
  }

  #[tokio::test]
  async fn live_transport_completes_one_competitive_month() {
    let (address, server) = test_server().await;

    let (status, html) = request(address, "GET", "/", None).await;
    assert_eq!(status, 200);
    assert!(html.contains("host-adapter.mjs"));

    let start_body = r#"{"campaign":"competitive-regional-v1","seed":42,"difficulty":"normal"}"#;
    let (status, body) = request(address, "POST", "/api/v1/sessions", Some(start_body)).await;
    assert_eq!(status, 200, "{body}");
    let started: serde_json::Value = serde_json::from_str(&body).unwrap();
    let session_id = started["session_id"].as_str().unwrap();

    let history_path = format!("/api/v1/sessions/{session_id}/history");
    let (status, body) = request(address, "GET", &history_path, None).await;
    assert_eq!(status, 200, "{body}");
    let history: serde_json::Value = serde_json::from_str(&body).unwrap();
    assert_eq!(history["schema_version"], "competitive-history-v1");
    assert_eq!(history["transition_count"], 0);
    assert!(history["transitions"].as_array().unwrap().is_empty());

    for suffix in ["presentation", "regional-world", "action-catalog"] {
      let path = format!("/api/v1/sessions/{session_id}/{suffix}");
      let (status, body) = request(address, "GET", &path, None).await;
      assert_eq!(status, 200, "{suffix}: {body}");
    }

    let replay_path = format!("/api/v1/sessions/{session_id}/replay");
    let (status, body) = request(address, "GET", &replay_path, None).await;
    assert_eq!(status, 200, "{body}");
    let replay: serde_json::Value = serde_json::from_str(&body).unwrap();
    assert_eq!(replay["schema_version"], "competitive-replay-v1");
    assert_eq!(replay["transition_count"], 0);
    assert!(replay["latest_state_hash"].is_null());

    let validation_path = format!("/api/v1/sessions/{session_id}/validation");
    let (status, body) = request(
      address,
      "POST",
      &validation_path,
      Some(r#"{"command_text":"hold"}"#),
    )
    .await;
    assert_eq!(status, 200, "{body}");
    let validation: serde_json::Value = serde_json::from_str(&body).unwrap();
    assert_eq!(validation["valid"], true);

    let turns_path = format!("/api/v1/sessions/{session_id}/turns");
    let (status, body) = request(
      address,
      "POST",
      &turns_path,
      Some(r#"{"command_text":"hold"}"#),
    )
    .await;
    assert_eq!(status, 200, "{body}");

    let resolution_path = format!("/api/v1/sessions/{session_id}/resolution");
    let (status, body) = request(address, "GET", &resolution_path, None).await;
    assert_eq!(status, 200, "{body}");
    let resolution: serde_json::Value = serde_json::from_str(&body).unwrap();
    assert_eq!(resolution["schema_version"], "competitive-resolution-v1");

    let (status, body) = request(address, "GET", &history_path, None).await;
    assert_eq!(status, 200, "{body}");
    let history: serde_json::Value = serde_json::from_str(&body).unwrap();
    assert_eq!(history["schema_version"], "competitive-history-v1");
    assert_eq!(history["transition_count"], 1);
    assert_eq!(history["transitions"].as_array().unwrap().len(), 1);
    assert_eq!(
      history["transitions"][0]["state_hash"],
      resolution["replay"]["state_hash"]
    );
    let (status, body) = request(address, "GET", &replay_path, None).await;
    assert_eq!(status, 200, "{body}");
    let replay: serde_json::Value = serde_json::from_str(&body).unwrap();
    assert_eq!(replay["schema_version"], "competitive-replay-v1");
    assert_eq!(replay["transition_count"], 1);
    assert_eq!(
      replay["latest_state_hash"],
      history["transitions"][0]["state_hash"]
    );

    let load_path = format!("/api/v1/sessions/{session_id}/load");
    let (status, body) = request(address, "POST", &load_path, None).await;
    assert_eq!(status, 400, "{body}");
    let error: serde_json::Value = serde_json::from_str(&body).unwrap();
    assert_eq!(error["code"], "checkpoint_missing");

    let save_path = format!("/api/v1/sessions/{session_id}/save");
    let (status, body) = request(address, "POST", &save_path, None).await;
    assert_eq!(status, 200, "{body}");
    let saved: serde_json::Value = serde_json::from_str(&body).unwrap();
    assert_eq!(saved["schema_version"], "competitive-save-v1");
    assert_eq!(saved["operation"], "saved");
    assert_eq!(saved["transition_count"], 1);

    let (status, body) = request(
      address,
      "POST",
      &turns_path,
      Some(r#"{"command_text":"hold"}"#),
    )
    .await;
    assert_eq!(status, 200, "{body}");
    let (status, body) = request(address, "POST", &load_path, None).await;
    assert_eq!(status, 200, "{body}");
    let loaded: serde_json::Value = serde_json::from_str(&body).unwrap();
    assert_eq!(loaded["schema_version"], "competitive-save-v1");
    assert_eq!(loaded["operation"], "loaded");
    assert_eq!(loaded["transition_count"], 1);
    assert_eq!(loaded["latest_state_hash"], saved["latest_state_hash"]);

    let end_path = format!("/api/v1/sessions/{session_id}/end");
    let (status, body) = request(address, "POST", &end_path, None).await;
    assert_eq!(status, 200, "{body}");
    let ended: serde_json::Value = serde_json::from_str(&body).unwrap();
    assert_eq!(ended["schema_version"], "competitive-end-session-v1");
    assert_eq!(ended["replay"]["transition_count"], 1);
    assert_eq!(ended["history"].as_array().unwrap().len(), 1);
    assert!(!ended["debrief"].as_array().unwrap().is_empty());

    let (status, body) = request(
      address,
      "GET",
      &format!("/api/v1/sessions/{session_id}/presentation"),
      None,
    )
    .await;
    assert_eq!(status, 404, "{body}");

    server.abort();
  }

  #[tokio::test]
  async fn live_transport_discovers_valid_checkpoint_metadata_without_save_contents() {
    let path = std::env::temp_dir().join(format!(
      "hs-mgt-game-gui-discovery-transport-{}.save",
      std::process::id()
    ));
    let (address, server) = test_server_with_persistence(path.clone()).await;
    let (status, body) = request(
      address,
      "POST",
      "/api/v1/sessions",
      Some(r#"{"campaign":"competitive-regional-v1","seed":42,"difficulty":"normal"}"#),
    )
    .await;
    assert_eq!(status, 200, "{body}");
    let session_id = serde_json::from_str::<serde_json::Value>(&body).unwrap()["session_id"]
      .as_str()
      .unwrap()
      .to_string();
    let (status, body) = request(
      address,
      "POST",
      &format!("/api/v1/sessions/{session_id}/save"),
      None,
    )
    .await;
    assert_eq!(status, 200, "{body}");

    let (status, body) = request(address, "GET", "/api/v1/checkpoints", None).await;
    assert_eq!(status, 200, "{body}");
    let discovery: serde_json::Value = serde_json::from_str(&body).unwrap();
    assert_eq!(discovery["schema_version"], "gui-checkpoint-discovery-v1");
    assert_eq!(discovery["invalid_entry_count"], 0);
    let checkpoint = &discovery["checkpoints"].as_array().unwrap()[0];
    assert_eq!(checkpoint["session_id"], session_id);
    assert_eq!(checkpoint["campaign"], "competitive-regional-v1");
    assert_eq!(checkpoint["storage"], "archive");
    assert_eq!(checkpoint["transition_count"], 0);
    assert!(checkpoint.get("save").is_none());
    let (status, body) = request(
      address,
      "POST",
      &format!("/api/v1/sessions/{session_id}/end"),
      None,
    )
    .await;
    assert_eq!(status, 200, "{body}");
    assert!(!path.exists());
    server.abort();
  }

  #[tokio::test]
  async fn live_transport_downloads_only_a_host_validated_checkpoint_artifact() {
    let path = std::env::temp_dir().join(format!(
      "hs-mgt-game-gui-artifact-transport-{}.save",
      std::process::id()
    ));
    let (address, server) = test_server_with_persistence(path.clone()).await;
    let (status, body) = request(
      address,
      "POST",
      "/api/v1/sessions",
      Some(r#"{"campaign":"competitive-regional-v1","seed":42,"difficulty":"normal"}"#),
    )
    .await;
    assert_eq!(status, 200, "{body}");
    let session_id = serde_json::from_str::<serde_json::Value>(&body).unwrap()["session_id"]
      .as_str()
      .unwrap()
      .to_string();
    let (status, body) = request(
      address,
      "POST",
      &format!("/api/v1/sessions/{session_id}/save"),
      None,
    )
    .await;
    assert_eq!(status, 200, "{body}");

    let (status, headers, artifact) = request_with_headers(
      address,
      "GET",
      &format!("/api/v1/sessions/{session_id}/save-artifact?storage=archive"),
      None,
    )
    .await;
    assert_eq!(status, 200, "{artifact}");
    assert!(headers.contains("content-type: application/octet-stream"));
    assert!(headers.contains(&format!(
      "content-disposition: attachment; filename=\"hs-mgt-checkpoint-{session_id}.save\""
    )));
    assert!(artifact.contains("gui-competitive-save-v1"));
    assert!(artifact.contains(&format!("\"session_id\": \"{session_id}\"")));

    let (status, body) = request(
      address,
      "GET",
      &format!("/api/v1/sessions/{session_id}/save-artifact?storage=legacy"),
      None,
    )
    .await;
    assert_eq!(status, 404, "{body}");
    assert!(body.contains("checkpoint_missing"));

    let (status, body) = request(
      address,
      "GET",
      &format!("/api/v1/sessions/{session_id}/save-artifact?storage=other"),
      None,
    )
    .await;
    assert_eq!(status, 400, "{body}");
    assert!(body.contains("invalid_checkpoint_artifact_storage"));

    let (status, body) = request(
      address,
      "POST",
      &format!("/api/v1/sessions/{session_id}/end"),
      None,
    )
    .await;
    assert_eq!(status, 200, "{body}");
    assert!(!path.exists());
    server.abort();
  }

  #[tokio::test]
  async fn live_transport_recovers_durable_checkpoint_after_host_restart() {
    let path = std::env::temp_dir().join(format!(
      "hs-mgt-game-gui-transport-{}.save",
      std::process::id()
    ));
    let (address, server) = test_server_with_persistence(path.clone()).await;
    let (status, body) = request(
      address,
      "POST",
      "/api/v1/sessions",
      Some(r#"{"campaign":"competitive-regional-v1","seed":42,"difficulty":"normal"}"#),
    )
    .await;
    assert_eq!(status, 200, "{body}");
    let session_id = serde_json::from_str::<serde_json::Value>(&body).unwrap()["session_id"]
      .as_str()
      .unwrap()
      .to_string();
    let turns_path = format!("/api/v1/sessions/{session_id}/turns");
    let (status, body) = request(
      address,
      "POST",
      &turns_path,
      Some(r#"{"command_text":"hold"}"#),
    )
    .await;
    assert_eq!(status, 200, "{body}");
    let save_path = format!("/api/v1/sessions/{session_id}/save");
    let (status, body) = request(address, "POST", &save_path, None).await;
    assert_eq!(status, 200, "{body}");
    let saved: serde_json::Value = serde_json::from_str(&body).unwrap();
    assert_eq!(saved["transition_count"], 1);
    let checkpoint_path = gui_session_checkpoint_path(&path, &session_id).unwrap();
    assert!(checkpoint_path.is_file());
    server.abort();

    let (address, restarted_server) = test_server_with_persistence(path.clone()).await;
    let load_path = format!("/api/v1/sessions/{session_id}/load");
    let (status, body) = request(address, "POST", &load_path, None).await;
    assert_eq!(status, 200, "{body}");
    let loaded: serde_json::Value = serde_json::from_str(&body).unwrap();
    assert_eq!(loaded["operation"], "loaded");
    assert_eq!(loaded["transition_count"], 1);
    assert_eq!(loaded["latest_state_hash"], saved["latest_state_hash"]);

    let (status, body) = request(
      address,
      "GET",
      &format!("/api/v1/sessions/{session_id}/presentation"),
      None,
    )
    .await;
    assert_eq!(status, 200, "{body}");
    let (status, body) = request(
      address,
      "GET",
      &format!("/api/v1/sessions/{session_id}/replay"),
      None,
    )
    .await;
    assert_eq!(status, 200, "{body}");
    let replay: serde_json::Value = serde_json::from_str(&body).unwrap();
    assert_eq!(replay["transition_count"], 1);

    let (status, body) = request(
      address,
      "POST",
      &format!("/api/v1/sessions/{session_id}/end"),
      None,
    )
    .await;
    assert_eq!(status, 200, "{body}");
    assert!(!path.exists());
    restarted_server.abort();
  }

  #[tokio::test]
  async fn live_transport_recovers_durable_stabilization_checkpoint_after_host_restart() {
    let path = std::env::temp_dir().join(format!(
      "hs-mgt-game-gui-stabilization-transport-{}.save",
      std::process::id()
    ));
    let (address, server) = test_server_with_persistence(path.clone()).await;
    let (status, body) = request(
      address,
      "POST",
      "/api/v1/sessions",
      Some(r#"{"campaign":"stabilization-v1","seed":42,"difficulty":null}"#),
    )
    .await;
    assert_eq!(status, 200, "{body}");
    let session_id = serde_json::from_str::<serde_json::Value>(&body).unwrap()["session_id"]
      .as_str()
      .unwrap()
      .to_string();
    let (status, body) = request(
      address,
      "POST",
      &format!("/api/v1/sessions/{session_id}/turns"),
      Some(r#"{"command_text":"8 18 112"}"#),
    )
    .await;
    assert_eq!(status, 200, "{body}");
    let (status, body) = request(
      address,
      "POST",
      &format!("/api/v1/sessions/{session_id}/save"),
      None,
    )
    .await;
    assert_eq!(status, 200, "{body}");
    let saved: serde_json::Value = serde_json::from_str(&body).unwrap();
    assert_eq!(saved["transition_count"], 1);
    let checkpoint_path = gui_session_checkpoint_path(&path, &session_id).unwrap();
    assert!(checkpoint_path.is_file());
    server.abort();

    let (address, restarted_server) = test_server_with_persistence(path.clone()).await;
    let (status, body) = request(
      address,
      "POST",
      &format!("/api/v1/sessions/{session_id}/load"),
      None,
    )
    .await;
    assert_eq!(status, 200, "{body}");
    let loaded: serde_json::Value = serde_json::from_str(&body).unwrap();
    assert_eq!(loaded["operation"], "loaded");
    assert_eq!(loaded["transition_count"], 1);
    assert_eq!(loaded["latest_state_hash"], saved["latest_state_hash"]);

    let (status, body) = request(
      address,
      "GET",
      &format!("/api/v1/sessions/{session_id}/campaign-coverage"),
      None,
    )
    .await;
    assert_eq!(status, 200, "{body}");
    let coverage: serde_json::Value = serde_json::from_str(&body).unwrap();
    assert_eq!(coverage["session"]["campaign"], "stabilization-v1");
    assert_eq!(coverage["stage"]["id"], "turn-2");

    let (status, body) = request(
      address,
      "POST",
      &format!("/api/v1/sessions/{session_id}/end"),
      None,
    )
    .await;
    assert_eq!(status, 200, "{body}");
    assert!(!path.exists());
    restarted_server.abort();
  }

  #[tokio::test]
  async fn live_transport_recovers_durable_affiliation_checkpoint_after_host_restart() {
    let path = std::env::temp_dir().join(format!(
      "hs-mgt-game-gui-affiliation-transport-{}.save",
      std::process::id()
    ));
    let (address, server) = test_server_with_persistence(path.clone()).await;
    let (status, body) = request(
      address,
      "POST",
      "/api/v1/sessions",
      Some(r#"{"campaign":"regional-affiliation-v1","seed":42,"difficulty":null}"#),
    )
    .await;
    assert_eq!(status, 200, "{body}");
    let session_id = serde_json::from_str::<serde_json::Value>(&body).unwrap()["session_id"]
      .as_str()
      .unwrap()
      .to_string();
    let (status, body) = request(
      address,
      "POST",
      &format!("/api/v1/sessions/{session_id}/turns"),
      Some(r#"{"command_text":"assess"}"#),
    )
    .await;
    assert_eq!(status, 200, "{body}");
    let (status, body) = request(
      address,
      "POST",
      &format!("/api/v1/sessions/{session_id}/save"),
      None,
    )
    .await;
    assert_eq!(status, 200, "{body}");
    let saved: serde_json::Value = serde_json::from_str(&body).unwrap();
    assert_eq!(saved["transition_count"], 1);
    let checkpoint_path = gui_session_checkpoint_path(&path, &session_id).unwrap();
    assert!(checkpoint_path.is_file());
    server.abort();

    let (address, restarted_server) = test_server_with_persistence(path.clone()).await;
    let (status, body) = request(
      address,
      "POST",
      &format!("/api/v1/sessions/{session_id}/load"),
      None,
    )
    .await;
    assert_eq!(status, 200, "{body}");
    let loaded: serde_json::Value = serde_json::from_str(&body).unwrap();
    assert_eq!(loaded["operation"], "loaded");
    assert_eq!(loaded["transition_count"], 1);
    assert_eq!(loaded["latest_state_hash"], saved["latest_state_hash"]);

    let (status, body) = request(
      address,
      "GET",
      &format!("/api/v1/sessions/{session_id}/campaign-coverage"),
      None,
    )
    .await;
    assert_eq!(status, 200, "{body}");
    let coverage: serde_json::Value = serde_json::from_str(&body).unwrap();
    assert_eq!(coverage["session"]["campaign"], "regional-affiliation-v1");
    assert_eq!(coverage["stage"]["id"], "chooseposture");

    let (status, body) = request(
      address,
      "POST",
      &format!("/api/v1/sessions/{session_id}/end"),
      None,
    )
    .await;
    assert_eq!(status, 200, "{body}");
    assert!(!path.exists());
    restarted_server.abort();
  }

  #[tokio::test]
  async fn live_transport_returns_structured_unknown_session_error() {
    let (address, server) = test_server().await;
    let (status, body) = request(
      address,
      "GET",
      "/api/v1/sessions/missing/presentation",
      None,
    )
    .await;
    assert_eq!(status, 404);
    let error: serde_json::Value = serde_json::from_str(&body).unwrap();
    assert!(error["error"].as_str().unwrap().contains("unknown session"));
    let (status, body) = request(address, "GET", "/api/v1/sessions/missing/replay", None).await;
    assert_eq!(status, 404);
    let error: serde_json::Value = serde_json::from_str(&body).unwrap();
    assert!(error["error"].as_str().unwrap().contains("unknown session"));
    let (status, body) = request(
      address,
      "GET",
      "/api/v1/sessions/missing/campaign-coverage",
      None,
    )
    .await;
    assert_eq!(status, 404);
    let error: serde_json::Value = serde_json::from_str(&body).unwrap();
    assert!(error["error"].as_str().unwrap().contains("unknown session"));
    let (status, body) = request(address, "GET", "/api/v1/sessions/missing", None).await;
    assert_eq!(status, 404);
    let error: serde_json::Value = serde_json::from_str(&body).unwrap();
    assert!(error["error"].as_str().unwrap().contains("unknown session"));
    let (status, body) = request(address, "POST", "/api/v1/sessions/missing/save", None).await;
    assert_eq!(status, 404);
    let error: serde_json::Value = serde_json::from_str(&body).unwrap();
    assert!(error["error"].as_str().unwrap().contains("unknown session"));
    let (status, body) = request(address, "GET", "/api/v1/sessions/missing/history", None).await;
    assert_eq!(status, 404);
    let error: serde_json::Value = serde_json::from_str(&body).unwrap();
    assert!(error["error"].as_str().unwrap().contains("unknown session"));
    server.abort();
  }

  async fn assert_full_campaign_coverage_transport(
    address: SocketAddr,
    campaign: &str,
    commands: &[&str],
  ) {
    let start_body = format!(r#"{{"campaign":"{campaign}","seed":42,"difficulty":null}}"#);
    let (status, body) = request(address, "POST", "/api/v1/sessions", Some(&start_body)).await;
    assert_eq!(status, 200, "{campaign} start: {body}");
    let session: serde_json::Value = serde_json::from_str(&body).unwrap();
    let session_id = session["session_id"].as_str().unwrap().to_string();

    let coverage_path =
      |session_id: &str| format!("/api/v1/sessions/{session_id}/campaign-coverage");
    let (status, body) = request(address, "GET", &coverage_path(&session_id), None).await;
    assert_eq!(status, 200, "{campaign} genesis coverage: {body}");
    let coverage: serde_json::Value = serde_json::from_str(&body).unwrap();
    assert_eq!(coverage["schema_version"], "campaign-coverage-v1");
    assert_eq!(coverage["session"]["campaign"], campaign);
    assert!(!coverage["session"]["done"].as_bool().unwrap());
    assert_eq!(coverage["replay"]["transition_count"], 0);
    assert!(coverage["audio"].is_object());

    for (index, command) in commands.iter().enumerate() {
      let turn_body = format!(r#"{{"command_text":"{command}"}}"#);
      let (status, body) = request(
        address,
        "POST",
        &format!("/api/v1/sessions/{session_id}/turns"),
        Some(&turn_body),
      )
      .await;
      assert_eq!(status, 200, "{campaign} transition {}: {body}", index + 1);

      let (status, body) = request(address, "GET", &coverage_path(&session_id), None).await;
      assert_eq!(status, 200, "{campaign} coverage {}: {body}", index + 1);
      let coverage: serde_json::Value = serde_json::from_str(&body).unwrap();
      assert_eq!(coverage["schema_version"], "campaign-coverage-v1");
      assert_eq!(coverage["session"]["campaign"], campaign);
      assert_eq!(coverage["replay"]["transition_count"], index + 1);
      assert_eq!(coverage["history"].as_array().unwrap().len(), index + 1);
      assert!(coverage["audio"].is_object());
      if index + 1 == commands.len() {
        assert!(coverage["session"]["done"].as_bool().unwrap());
        assert!(!coverage["debrief"].as_array().unwrap().is_empty());
        assert_eq!(coverage["audio"]["music_state_id"], "debrief");
      } else {
        assert!(!coverage["session"]["done"].as_bool().unwrap());
      }
    }
  }

  #[tokio::test]
  async fn live_transport_supports_campaign_coverage_campaigns() {
    let (address, server) = test_server().await;
    for campaign in [
      "competitive-regional-v1",
      "stabilization-v1",
      "regional-affiliation-v1",
    ] {
      let body = format!(r#"{{"campaign":"{campaign}","seed":42,"difficulty":null}}"#);
      let (status, body) = request(address, "POST", "/api/v1/sessions", Some(&body)).await;
      assert_eq!(status, 200, "{campaign}: {body}");
      let session: serde_json::Value = serde_json::from_str(&body).unwrap();
      assert_eq!(session["campaign"], campaign);
      let session_id = session["session_id"].as_str().unwrap();
      let (status, body) = request(
        address,
        "GET",
        &format!("/api/v1/sessions/{session_id}/campaign-coverage"),
        None,
      )
      .await;
      assert_eq!(status, 200, "{campaign}: {body}");
      let coverage: serde_json::Value = serde_json::from_str(&body).unwrap();
      assert_eq!(coverage["schema_version"], "campaign-coverage-v1");
      assert_eq!(coverage["session"]["campaign"], campaign);
      let command = if campaign == "competitive-regional-v1" {
        "hold"
      } else if campaign == "stabilization-v1" {
        "8 18 112"
      } else {
        "assess"
      };
      let body = format!(r#"{{"command_text":"{command}"}}"#);
      let (status, body) = request(
        address,
        "POST",
        &format!("/api/v1/sessions/{session_id}/turns"),
        Some(&body),
      )
      .await;
      assert_eq!(status, 200, "{campaign} valid decision: {body}");
      let (status, body) = request(
        address,
        "POST",
        &format!("/api/v1/sessions/{session_id}/turns"),
        Some(r#"{"command_text":"not-a-valid-command"}"#),
      )
      .await;
      assert_eq!(status, 400, "{campaign} invalid decision: {body}");
      let (status, body) = request(
        address,
        "GET",
        &format!("/api/v1/sessions/{session_id}/campaign-coverage"),
        None,
      )
      .await;
      assert_eq!(status, 200, "{campaign} post-submit coverage: {body}");
      let coverage: serde_json::Value = serde_json::from_str(&body).unwrap();
      assert_eq!(coverage["replay"]["transition_count"], 1);
    }
    let body = r#"{"campaign":"unsupported-v1","seed":42,"difficulty":null}"#;
    let (status, body) = request(address, "POST", "/api/v1/sessions", Some(body)).await;
    assert_eq!(status, 400);
    let error: serde_json::Value = serde_json::from_str(&body).unwrap();
    assert_eq!(error["code"], "unsupported_gui_campaign");
    server.abort();
  }

  #[tokio::test]
  async fn live_transport_covers_full_campaign_coverage_reads() {
    let (address, server) = test_server().await;
    let competitive_commands = vec![""; 24];
    let stabilization_commands = vec![""; crate::model::INTERACTIVE_TURN_COUNT as usize];
    let affiliation_commands = [
      "assess",
      "posture choice=independent",
      "hold",
      "hold",
      "hold",
      "hold",
    ];

    assert_full_campaign_coverage_transport(
      address,
      "competitive-regional-v1",
      &competitive_commands,
    )
    .await;
    assert_full_campaign_coverage_transport(address, "stabilization-v1", &stabilization_commands)
      .await;
    assert_full_campaign_coverage_transport(
      address,
      "regional-affiliation-v1",
      &affiliation_commands,
    )
    .await;
    server.abort();
  }

  #[test]
  fn live_start_request_rejects_scenario_paths() {
    let request = r#"{"campaign":"competitive-regional-v1","seed":42,"difficulty":"normal","scenario_path":"/tmp/private.toml"}"#;
    assert!(serde_json::from_str::<GuiStartSessionRequest>(request).is_err());
  }
}
