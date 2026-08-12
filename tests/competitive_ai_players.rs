use vital_margin::competitive::{
  compute_ai_batch, genesis_competitive_world_with_ruleset, month1_batches_with_ai,
};
use vital_margin::model::{Difficulty, default_competitive_ruleset};

#[test]
fn ai_batches_are_deterministic_for_same_seed_and_genesis() {
  let ruleset = default_competitive_ruleset();
  let world = genesis_competitive_world_with_ruleset(Difficulty::Expert, &ruleset);

  let first = month1_batches_with_ai(&world, &ruleset, 42).expect("first");
  let second = month1_batches_with_ai(&world, &ruleset, 42).expect("second");

  assert_eq!(first, second);
}

#[test]
fn ai_batches_include_rationale_for_each_rival() {
  let ruleset = default_competitive_ruleset();
  let world = genesis_competitive_world_with_ruleset(Difficulty::Hard, &ruleset);

  let batches = month1_batches_with_ai(&world, &ruleset, 42).expect("batches");
  let rival_batches = batches.iter().filter(|batch| batch.system_id != 0);
  for batch in rival_batches {
    assert!(
      batch.rationale.is_some(),
      "missing rationale for rival system {}",
      batch.system_id
    );
  }
}

#[test]
fn ai_batch_has_non_empty_rationale() {
  let ruleset = default_competitive_ruleset();
  let world = genesis_competitive_world_with_ruleset(Difficulty::Normal, &ruleset);
  let ai_batch = compute_ai_batch(1, &world, &ruleset, 42).expect("ai batch");
  let rationale = ai_batch.rationale.expect("rationale");
  assert!(!rationale.trim().is_empty());
}
