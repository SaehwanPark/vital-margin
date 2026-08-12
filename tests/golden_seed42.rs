use vital_margin::cli::build_history_for_strategy;
use vital_margin::model::*;

#[test]
fn default_seed_reproduces_canonical_demo_trajectory() {
  let ruleset = default_ruleset();
  let history =
    build_history_for_strategy(StrategyPath::AccessStabilization, DEFAULT_SEED, &ruleset).unwrap();

  assert_eq!(history.transitions.len(), 5);
  assert_eq!(
    history.transitions[0].resolved_inputs,
    ResolvedInputs {
      measurement_noise: 4,
      delayed_access_report: 67,
      labor_sick_call_delta: -3,
      policy_signal: 4,
      coalition_leverage_signal: 2,
      access_measurement_revision: 0,
      competitor_market_signal: 0,
    }
  );
  assert_eq!(
    history.transitions[1].resolved_inputs,
    ResolvedInputs {
      measurement_noise: -5,
      delayed_access_report: 70,
      labor_sick_call_delta: -2,
      policy_signal: 3,
      coalition_leverage_signal: 4,
      access_measurement_revision: -1,
      competitor_market_signal: 0,
    }
  );
  assert_eq!(
    history.transitions[0].actor_decision.decision,
    ActorDecision::Insurer(InsurerDecision::Reject)
  );
  assert_eq!(
    history.transitions[1].actor_decision.decision,
    ActorDecision::StatePolicy(StatePolicyDecision::GrantFlexibility)
  );
  assert_eq!(
    history.transitions[2].resolved_inputs,
    ResolvedInputs {
      measurement_noise: -5,
      delayed_access_report: 69,
      labor_sick_call_delta: -5,
      policy_signal: 1,
      coalition_leverage_signal: 2,
      access_measurement_revision: 2,
      competitor_market_signal: 0,
    }
  );
  assert_eq!(
    history.transitions[2].actor_decision.decision,
    ActorDecision::Labor(LaborDecision::Cooperative)
  );
  assert_eq!(
    history.transitions[3].resolved_inputs,
    ResolvedInputs {
      measurement_noise: -2,
      delayed_access_report: 71,
      labor_sick_call_delta: -5,
      policy_signal: 5,
      coalition_leverage_signal: 3,
      access_measurement_revision: -1,
      competitor_market_signal: 0,
    }
  );
  assert_eq!(
    history.transitions[3].actor_decision.decision,
    ActorDecision::Coalition(CoalitionDecision::FullPartnership)
  );
  assert_eq!(history.transitions[3].state_hash, "bce02dff9b4b4ac6");
  assert_eq!(
    history.transitions[4].resolved_inputs,
    ResolvedInputs {
      measurement_noise: -5,
      delayed_access_report: 78,
      labor_sick_call_delta: -4,
      policy_signal: 2,
      coalition_leverage_signal: 2,
      access_measurement_revision: 3,
      competitor_market_signal: 6,
    }
  );
  assert_eq!(
    history.transitions[4].actor_decision.decision,
    ActorDecision::Competitor(CompetitorDecision::PartialRetreat)
  );
  assert_eq!(
    history.transitions.last().unwrap().state_hash,
    "6fb1ebbea564274f"
  );
}
