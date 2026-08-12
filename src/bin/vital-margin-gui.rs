use vital_margin::gui_server::{parse_bind_args, run_gui_server};

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
  let address = parse_bind_args(std::env::args()).map_err(std::io::Error::other)?;
  run_gui_server(address).await
}
