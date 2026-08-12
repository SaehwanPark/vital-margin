use std::fs;
use std::path::PathBuf;

use crate::artifact::{
  describe_session_save_error, deserialize_competitive_session_save,
  serialize_competitive_session_save, serialize_session_save, verify_session_save,
};
use crate::model::{
  CompetitiveRuleset, CompetitiveSessionSave, Ruleset, SessionSave, SessionSaveError,
};

pub fn config_dir() -> PathBuf {
  if let Ok(xdg) = std::env::var("XDG_CONFIG_HOME") {
    PathBuf::from(xdg).join("vital-margin")
  } else if let Ok(home) = std::env::var("HOME") {
    PathBuf::from(home).join(".config").join("vital-margin")
  } else {
    PathBuf::from(".config").join("vital-margin")
  }
}

pub fn session_save_path() -> PathBuf {
  config_dir().join("session.save")
}

pub fn competitive_session_save_path() -> PathBuf {
  config_dir().join("competitive_session.save")
}

pub fn gui_competitive_session_save_path() -> PathBuf {
  config_dir().join("gui_competitive_session.save")
}

pub fn settings_path() -> PathBuf {
  config_dir().join("settings")
}

pub fn session_save_exists() -> bool {
  session_save_path().is_file()
}

pub fn competitive_session_save_exists() -> bool {
  competitive_session_save_path().is_file()
}

pub fn load_session_save(ruleset: &Ruleset) -> Result<SessionSave, SessionSaveError> {
  let path = session_save_path();
  let text = fs::read_to_string(&path).map_err(|error| {
    SessionSaveError::IoError(format!(
      "unable to read session save at {}: {error}",
      path.display()
    ))
  })?;
  verify_session_save(&text, ruleset)
}

pub fn write_session_save(save: &SessionSave) -> Result<(), SessionSaveError> {
  let dir = config_dir();
  fs::create_dir_all(&dir).map_err(|error| {
    SessionSaveError::IoError(format!(
      "unable to create config directory {}: {error}",
      dir.display()
    ))
  })?;

  let path = session_save_path();
  fs::write(&path, serialize_session_save(save)).map_err(|error| {
    SessionSaveError::IoError(format!(
      "unable to write session save to {}: {error}",
      path.display()
    ))
  })
}

pub fn delete_session_save() -> Result<(), SessionSaveError> {
  let path = session_save_path();
  if !path.is_file() {
    return Ok(());
  }

  fs::remove_file(&path).map_err(|error| {
    SessionSaveError::IoError(format!(
      "unable to delete session save at {}: {error}",
      path.display()
    ))
  })
}

pub fn load_competitive_session_save(
  ruleset: &CompetitiveRuleset,
) -> Result<CompetitiveSessionSave, SessionSaveError> {
  let path = competitive_session_save_path();
  let text = fs::read_to_string(&path).map_err(|error| {
    SessionSaveError::IoError(format!(
      "unable to read competitive session save at {}: {error}",
      path.display()
    ))
  })?;
  deserialize_competitive_session_save(&text, ruleset)
}

pub fn write_competitive_session_save(
  save: &CompetitiveSessionSave,
) -> Result<(), SessionSaveError> {
  let dir = config_dir();
  fs::create_dir_all(&dir).map_err(|error| {
    SessionSaveError::IoError(format!(
      "unable to create config directory {}: {error}",
      dir.display()
    ))
  })?;

  let path = competitive_session_save_path();
  fs::write(&path, serialize_competitive_session_save(save)).map_err(|error| {
    SessionSaveError::IoError(format!(
      "unable to write competitive session save to {}: {error}",
      path.display()
    ))
  })
}

pub fn delete_competitive_session_save() -> Result<(), SessionSaveError> {
  let path = competitive_session_save_path();
  if !path.is_file() {
    return Ok(());
  }

  fs::remove_file(&path).map_err(|error| {
    SessionSaveError::IoError(format!(
      "unable to delete competitive session save at {}: {error}",
      path.display()
    ))
  })
}

pub fn describe_persistence_error(error: &SessionSaveError) -> String {
  describe_session_save_error(error)
}

pub fn first_run_complete() -> bool {
  let path = settings_path();
  fs::read_to_string(path)
    .map(|text| {
      text
        .lines()
        .any(|line| line.trim() == "first_run_complete=true")
    })
    .unwrap_or(false)
}

pub fn mark_first_run_complete() -> Result<(), SessionSaveError> {
  let dir = config_dir();
  fs::create_dir_all(&dir).map_err(|error| {
    SessionSaveError::IoError(format!(
      "unable to create config directory {}: {error}",
      dir.display()
    ))
  })?;

  let path = settings_path();
  fs::write(&path, "first_run_complete=true\n").map_err(|error| {
    SessionSaveError::IoError(format!(
      "unable to write settings to {}: {error}",
      path.display()
    ))
  })
}

#[cfg(test)]
mod tests {
  use super::*;
  use crate::model::{ExperienceMode, History, SessionSave, genesis_state};
  use std::sync::Mutex;

  static PERSISTENCE_TEST_LOCK: Mutex<()> = Mutex::new(());

  #[test]
  fn delete_session_save_is_idempotent_when_missing() {
    let _lock = PERSISTENCE_TEST_LOCK.lock().unwrap();
    let _ = delete_session_save();
  }

  #[test]
  fn session_save_round_trip_fields() {
    use crate::artifact::deserialize_session_save;

    let save = SessionSave {
      ruleset_version: "demo-ruleset-0.1.0".to_string(),
      seed: 42,
      experience_mode: ExperienceMode::Standard,
      history: History {
        genesis: genesis_state(),
        transitions: Vec::new(),
      },
      next_turn: 1,
    };

    let text = serialize_session_save(&save);
    let restored = deserialize_session_save(&text).unwrap();
    assert_eq!(restored.seed, 42);
    assert_eq!(restored.next_turn, 1);
    assert_eq!(restored.experience_mode, ExperienceMode::Standard);
  }

  #[test]
  fn competitive_session_save_round_trip_fields() {
    use crate::artifact::{
      deserialize_competitive_session_save, serialize_competitive_session_save,
    };
    use crate::competitive::{build_month1_resolution_history, genesis_competitive_world};
    use crate::model::{
      CompetitiveHistory, CompetitiveSessionSave, Difficulty, default_competitive_ruleset,
    };

    let ruleset = default_competitive_ruleset();
    let genesis = genesis_competitive_world(Difficulty::Normal);

    let save = CompetitiveSessionSave {
      ruleset_version: ruleset.version.to_string(),
      seed: 42,
      difficulty: Difficulty::Normal,
      history: CompetitiveHistory {
        genesis,
        transitions: build_month1_resolution_history(Difficulty::Normal, 42)
          .expect("history")
          .transitions,
      },
      next_month: 1,
    };

    let text = serialize_competitive_session_save(&save);
    let restored = deserialize_competitive_session_save(&text, &ruleset).unwrap();
    assert_eq!(restored.seed, 42);
    assert_eq!(restored.next_month, 1);
    assert_eq!(restored.difficulty, Difficulty::Normal);
    assert_eq!(restored.history.transitions[0].consultant_options.len(), 4);

    let mut legacy_json: serde_json::Value = serde_json::from_str(&text).expect("json");
    legacy_json["history"]["transitions"][0]
      .as_object_mut()
      .expect("transition object")
      .remove("consultant_options");
    let legacy_text = serde_json::to_string_pretty(&legacy_json).expect("legacy json");
    let legacy = deserialize_competitive_session_save(&legacy_text, &ruleset).unwrap();
    assert!(legacy.history.transitions[0].consultant_options.is_empty());
  }

  #[test]
  fn delete_competitive_session_save_is_idempotent_when_missing() {
    let _lock = PERSISTENCE_TEST_LOCK.lock().unwrap();
    let _ = delete_competitive_session_save();
  }

  #[test]
  fn competitive_persistence_write_load_delete_round_trip() {
    let _lock = PERSISTENCE_TEST_LOCK.lock().unwrap();
    use crate::competitive::genesis_competitive_world;
    use crate::model::{
      CompetitiveHistory, CompetitiveSessionSave, Difficulty, default_competitive_ruleset,
    };

    let ruleset = default_competitive_ruleset();
    let genesis = genesis_competitive_world(Difficulty::Normal);

    let save = CompetitiveSessionSave {
      ruleset_version: ruleset.version.to_string(),
      seed: 12345,
      difficulty: Difficulty::Normal,
      history: CompetitiveHistory {
        genesis,
        transitions: Vec::new(),
      },
      next_month: 2,
    };

    // Ensure clean state
    let _ = delete_competitive_session_save();
    assert!(!competitive_session_save_exists());

    // Write save
    write_competitive_session_save(&save).unwrap();
    assert!(competitive_session_save_exists());

    // Load save
    let loaded = load_competitive_session_save(&ruleset).unwrap();
    assert_eq!(loaded.seed, 12345);
    assert_eq!(loaded.next_month, 2);
    assert_eq!(loaded.difficulty, Difficulty::Normal);

    // Delete save
    delete_competitive_session_save().unwrap();
    assert!(!competitive_session_save_exists());
  }
}
