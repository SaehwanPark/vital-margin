use std::path::PathBuf;
use vital_margin::cli::{describe_cli_error, eprint_error, run};
use vital_margin::model::SessionOutcome;

fn main() {
  let mut args = std::env::args().skip(1);
  let mut scenario_path = None;

  while let Some(arg) = args.next() {
    match arg.as_str() {
      "-h" | "--help" => {
        println!("Vital Margin CLI");
        println!("Usage: vital-margin [OPTIONS]");
        println!();
        println!("Options:");
        println!("  -s, --scenario <PATH>  Path to a custom TOML scenario file to load");
        println!("  -h, --help             Print help information");
        return;
      }
      "-s" | "--scenario" => {
        if let Some(path_str) = args.next() {
          scenario_path = Some(PathBuf::from(path_str));
        } else {
          eprintln!("Error: --scenario requires a path argument.");
          std::process::exit(1);
        }
      }
      other => {
        eprintln!("Error: Unknown argument '{}'. Use --help for usage.", other);
        std::process::exit(1);
      }
    }
  }

  match run(scenario_path) {
    Ok(SessionOutcome::Completed)
    | Ok(SessionOutcome::CompetitivePreview)
    | Ok(SessionOutcome::QuitSaved)
    | Ok(SessionOutcome::QuitNoSave) => {}
    Err(error) => {
      eprint_error(&format!(
        "Unable to run demo: {}",
        describe_cli_error(&error)
      ));
      std::process::exit(1);
    }
  }
}
