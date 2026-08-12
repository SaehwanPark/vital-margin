use std::fs;
use vital_margin::model::{Difficulty, default_competitive_ruleset, default_ruleset};
use vital_margin::scenario::{
  load_scenario_file, validate_competitive_scenario, validate_regional_affiliation_scenario,
  validate_stabilization_scenario,
};

#[test]
fn test_load_non_existent_file() {
  let res = load_scenario_file("this_file_does_not_exist_at_all.toml");
  assert!(res.is_err());
}

#[test]
fn test_load_malformed_toml() {
  let temp_path = "temp_malformed_test.toml";
  fs::write(temp_path, "not_valid_toml = [").unwrap();
  let res = load_scenario_file(temp_path);
  let _ = fs::remove_file(temp_path);
  assert!(res.is_err());
}

#[test]
fn test_load_valid_scenario() {
  let temp_path = "temp_valid_test.toml";
  let content = fs::read_to_string("scenarios/stabilization-v1.toml").expect("read bundled file");
  fs::write(temp_path, content).unwrap();
  let res = load_scenario_file(temp_path);
  let _ = fs::remove_file(temp_path);
  assert!(res.is_ok());

  let scenario = res.unwrap();
  assert_eq!(scenario.campaign_id, "stabilization-v1");
  let ruleset = default_ruleset();
  assert!(validate_stabilization_scenario(&scenario, &ruleset).is_ok());
}

#[test]
fn test_load_valid_competitive_scenario() {
  let scenario =
    load_scenario_file("scenarios/competitive-v1-template.toml").expect("load template");
  assert_eq!(scenario.campaign_id, "competitive-regional-v1");
  let ruleset = default_competitive_ruleset();
  assert!(validate_competitive_scenario(&scenario, &ruleset).is_ok());

  let initial_state = scenario.initial_competitive_world_state(Difficulty::Normal, &ruleset);
  assert!(initial_state.is_ok());
  let world = initial_state.unwrap();
  assert_eq!(world.systems.len(), 3);
  assert_eq!(world.market.regional_demand_index, 102);
}

#[test]
fn test_validate_competitive_scenario_errors() {
  let mut scenario =
    load_scenario_file("scenarios/competitive-v1-template.toml").expect("load template");
  let ruleset = default_competitive_ruleset();

  // Test ruleset mismatch
  scenario.ruleset_id = "bad-ruleset".to_string();
  assert!(validate_competitive_scenario(&scenario, &ruleset).is_err());
  scenario.ruleset_id = ruleset.version.to_string();

  // Test wrong campaign_id
  scenario.campaign_id = "stabilization-v1".to_string();
  assert!(validate_competitive_scenario(&scenario, &ruleset).is_err());
  scenario.campaign_id = "competitive-regional-v1".to_string();

  // Test zero human controller
  if let Some(systems) = &mut scenario.systems {
    systems[0].controller = "Ai".to_string();
    systems[0].ai_style = Some("growth".to_string());
  }
  assert!(validate_competitive_scenario(&scenario, &ruleset).is_err());
}

#[test]
fn test_load_exemplary_competitive_scenario() {
  let scenario =
    load_scenario_file("scenarios/competitive-exemplary-v1.toml").expect("load exemplary scenario");
  assert_eq!(scenario.campaign_id, "competitive-regional-v1");
  assert_eq!(scenario.scenario_id, "exemplary-competitive-v1");
  let ruleset = default_competitive_ruleset();
  assert!(validate_competitive_scenario(&scenario, &ruleset).is_ok());

  let initial_state = scenario.initial_competitive_world_state(Difficulty::Normal, &ruleset);
  assert!(initial_state.is_ok());
  let world = initial_state.unwrap();
  assert_eq!(world.systems.len(), 3);
  assert_eq!(world.systems[0].name, "Riverside Community Health");
  assert_eq!(world.systems[0].resources.cash, 500);
}

#[test]
fn test_load_valid_regional_affiliation_scenario() {
  let scenario =
    load_scenario_file("scenarios/regional-affiliation-v1.toml").expect("load affiliation");
  assert_eq!(scenario.campaign_id, "regional-affiliation-v1");
  validate_regional_affiliation_scenario(
    &scenario,
    &vital_margin::model::default_affiliation_ruleset(),
  )
  .expect("validate affiliation");
}
