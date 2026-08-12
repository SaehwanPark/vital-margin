use std::sync::{Arc, Mutex};

use rmcp::{
  ErrorData, ServerHandler, ServiceExt,
  handler::server::{router::tool::ToolRouter, wrapper::Parameters},
  model::{CallToolResult, Content, Implementation, ServerCapabilities, ServerInfo},
  tool, tool_handler, tool_router,
};

use super::session::{
  EndSessionEnvelope, EndSessionRequest, GameSessionStore, GetActionCatalogRequest,
  GetCampaignCoverageRequest, GetHistoryRequest, GetObservationRequest, GetPresentationRequest,
  GetRegionalWorldRequest, GetReplayRequest, GetResolutionRequest, HistoryEnvelope,
  LoadSessionRequest, McpErrorMessage, ReplayEnvelope, SaveEnvelope, SaveSessionRequest,
  SessionEnvelope, StartSessionRequest, SubmitTurnRequest, ValidateTurnRequest,
};

#[derive(Clone)]
pub struct McpGameServer {
  store: Arc<Mutex<GameSessionStore>>,
  #[allow(dead_code)]
  tool_router: ToolRouter<Self>,
}

impl Default for McpGameServer {
  fn default() -> Self {
    Self::new()
  }
}

impl McpGameServer {
  pub fn new() -> Self {
    Self {
      store: Arc::new(Mutex::new(GameSessionStore::default())),
      tool_router: Self::tool_router(),
    }
  }
}

#[tool_router]
impl McpGameServer {
  #[tool(
    name = "start_session",
    description = "Start a bounded game session for stabilization-v1, competitive-regional-v1, or regional-affiliation-v1."
  )]
  async fn start_session(
    &self,
    Parameters(request): Parameters<StartSessionRequest>,
  ) -> CallToolResult {
    self.with_store(|store| store.start_session(request))
  }

  #[tool(
    name = "get_observation",
    description = "Read the current actor-visible observation and legal command format for a session."
  )]
  async fn get_observation(
    &self,
    Parameters(request): Parameters<GetObservationRequest>,
  ) -> CallToolResult {
    self.with_store(|store| store.get_observation(request))
  }

  #[tool(
    name = "get_action_catalog",
    description = "Return the host-owned competitive action catalog and parameter metadata without advancing the session."
  )]
  async fn get_action_catalog(
    &self,
    Parameters(request): Parameters<GetActionCatalogRequest>,
  ) -> CallToolResult {
    self.with_store(|store| store.get_action_catalog(request))
  }

  #[tool(
    name = "get_resolution",
    description = "Return a committed competitive-month resolution for the latest or selected turn without advancing the session."
  )]
  async fn get_resolution(
    &self,
    Parameters(request): Parameters<GetResolutionRequest>,
  ) -> CallToolResult {
    self.with_store(|store| store.get_resolution(request))
  }

  #[tool(
    name = "get_regional_world",
    description = "Return the actor-visible schematic regional world for the current competitive session without advancing it."
  )]
  async fn get_regional_world(
    &self,
    Parameters(request): Parameters<GetRegionalWorldRequest>,
  ) -> CallToolResult {
    self.with_store(|store| store.get_regional_world(request))
  }

  #[tool(
    name = "get_campaign_coverage",
    description = "Return actor-visible stage, decision, actor, process, history, and debrief coverage for stabilization or affiliation without advancing the session."
  )]
  async fn get_campaign_coverage(
    &self,
    Parameters(request): Parameters<GetCampaignCoverageRequest>,
  ) -> CallToolResult {
    self.with_store(|store| store.get_campaign_coverage(request))
  }

  #[tool(
    name = "validate_turn",
    description = "Validate a canonical competitive command batch without advancing the session or resolving outcomes."
  )]
  async fn validate_turn(
    &self,
    Parameters(request): Parameters<ValidateTurnRequest>,
  ) -> CallToolResult {
    self.with_store(|store| store.validate_turn(request))
  }

  #[tool(
    name = "submit_turn",
    description = "Submit one player command batch and advance the current session by one turn or month."
  )]
  async fn submit_turn(
    &self,
    Parameters(request): Parameters<SubmitTurnRequest>,
  ) -> CallToolResult {
    self.with_store(|store| store.submit_turn(request))
  }

  #[tool(
    name = "get_history",
    description = "Return append-only transition summaries and state hashes for a session."
  )]
  async fn get_history(
    &self,
    Parameters(request): Parameters<GetHistoryRequest>,
  ) -> CallToolResult {
    self.with_store(|store| store.get_history(request))
  }

  #[tool(
    name = "get_replay",
    description = "Verify and return host-owned replay metadata and immutable transition summaries for a session without advancing session state."
  )]
  async fn get_replay(&self, Parameters(request): Parameters<GetReplayRequest>) -> CallToolResult {
    self.with_store(|store| store.get_replay(request))
  }

  #[tool(
    name = "save_session",
    description = "Save an explicit host checkpoint for a live session without serializing state in the client; the loopback GUI may persist competitive, stabilization, or regional-affiliation checkpoints in its host-owned file."
  )]
  async fn save_session(
    &self,
    Parameters(request): Parameters<SaveSessionRequest>,
  ) -> CallToolResult {
    self.with_store(|store| store.save_session(request))
  }

  #[tool(
    name = "load_session",
    description = "Restore an in-memory host checkpoint or a matching durable loopback competitive, stabilization, or regional-affiliation checkpoint and return aligned save metadata without client-side state restoration."
  )]
  async fn load_session(
    &self,
    Parameters(request): Parameters<LoadSessionRequest>,
  ) -> CallToolResult {
    self.with_store(|store| store.load_session(request))
  }

  #[tool(
    name = "get_presentation",
    description = "Return a typed actor-visible read-only presentation projection without advancing the session or enabling commands."
  )]
  async fn get_presentation(
    &self,
    Parameters(request): Parameters<GetPresentationRequest>,
  ) -> CallToolResult {
    self.with_store(|store| store.get_presentation(request))
  }

  #[tool(
    name = "end_session",
    description = "End a session and return its final debrief summary."
  )]
  async fn end_session(
    &self,
    Parameters(request): Parameters<EndSessionRequest>,
  ) -> CallToolResult {
    self.with_store(|store| store.end_session(request))
  }
}

impl McpGameServer {
  fn with_store<T>(
    &self,
    run: impl FnOnce(&mut GameSessionStore) -> Result<T, McpErrorMessage>,
  ) -> CallToolResult
  where
    T: serde::Serialize,
  {
    match self.store.lock() {
      Ok(mut store) => match run(&mut store) {
        Ok(value) => CallToolResult::structured(serde_json::to_value(value).expect("MCP result")),
        Err(error) => {
          CallToolResult::structured_error(serde_json::to_value(error).expect("MCP error result"))
        }
      },
      Err(_) => CallToolResult::error(vec![Content::text("MCP session store lock failed")]),
    }
  }
}

#[tool_handler]
impl ServerHandler for McpGameServer {
  fn get_info(&self) -> ServerInfo {
    ServerInfo::new(ServerCapabilities::builder().enable_tools().build())
      .with_server_info({
        let mut implementation =
          Implementation::new("vital-margin-mcp", env!("CARGO_PKG_VERSION"));
        implementation.title = Some("Vital Margin MCP".to_string());
        implementation.description =
          Some("Local MCP interface for autonomous play of bounded campaign sessions.".to_string());
        implementation
      })
      .with_instructions(
        "Use start_session, get_observation, get_presentation, get_action_catalog, get_campaign_coverage, validate_turn, submit_turn, get_resolution, get_regional_world, get_history, get_replay, save_session, load_session, and end_session to play bounded deterministic campaign sessions. get_presentation, get_action_catalog, get_campaign_coverage, validate_turn, get_resolution, get_regional_world, get_history, and get_replay are non-mutating actor-visible reads; save_session and load_session are explicit host checkpoint operations.",
      )
  }
}

pub async fn run_stdio_server() -> Result<(), Box<dyn std::error::Error>> {
  let service = McpGameServer::new().serve(rmcp::transport::stdio()).await?;
  service.waiting().await?;
  Ok(())
}

#[allow(dead_code)]
fn _assert_result_shapes(
  _: SessionEnvelope,
  _: HistoryEnvelope,
  _: ReplayEnvelope,
  _: SaveEnvelope,
  _: EndSessionEnvelope,
  _: ErrorData,
) {
}
