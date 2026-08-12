import argparse
import json
import sys
import os
import re
import subprocess

# Add scripts directory to path to allow import
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from play_game import play_session

SEEDS = [42, 43, 44]
TARGET_BASELINE = "baseline"
TARGET_PROJECT_COVERAGE = "project-coverage"
TARGET_DIFFICULTY_SWEEP = "difficulty-sweep"
TARGET_DIFFICULTY_ADAPTIVE = "difficulty-adaptive"
DIFFICULTY_SWEEP_LEVELS = ["easy", "hard"]
ACTION_VERBS = ("recruit", "invest", "negotiate", "commit", "project", "monitor")
WORKFORCE_TRUST_HARD_THRESHOLD = 50

def code_version():
  try:
    with open("Cargo.toml", "r", encoding="utf-8") as f:
      text = f.read()
  except OSError:
    return "unknown"
  match = re.search(r'^version\s*=\s*"([^"]+)"', text, re.MULTILINE)
  return match.group(1) if match else "unknown"

def is_stabilization_legal(legal):
  return len(legal) == 1

def riverside_observation_block(obs):
  block = ""
  in_riverside = False
  for line in "\n".join(obs).split("\n"):
    if "RIVERSIDE COMMUNITY HEALTH" in line.upper():
      in_riverside = True
    elif in_riverside and ("NORTHLAKE" in line.upper() or "SUMMIT" in line.upper() or "VALLEY" in line.upper()):
      in_riverside = False
    if in_riverside:
      block += line + "\n"
  return block

def parse_obs_workforce_trust(obs):
  riverside_block = riverside_observation_block(obs)
  wf_m = re.search(r"Workforce trust:\s*(\d+)", riverside_block)
  if not wf_m:
    wf_m = re.search(r"Workforce:\s*(\d+)", riverside_block)
  return int(wf_m.group(1)) if wf_m else None

def count_action_verbs(cmd):
  count = 0
  for part in cmd.split(";"):
    part = part.strip().lower()
    for verb in ACTION_VERBS:
      if part == verb or part.startswith(f"{verb} "):
        count += 1
        break
  return count

def reduce_large_invest(cmd):
  def replace_beds(match):
    amount = int(match.group(1))
    if amount > 10:
      return f"invest domain=beds amount={min(8, amount)}"
    return match.group(0)

  cmd = re.sub(
    r"invest domain=beds amount=(\d+)",
    replace_beds,
    cmd,
    flags=re.IGNORECASE
  )

  def replace_other(match):
    domain = match.group(1).lower()
    if domain == "beds":
      return match.group(0)
    amount = int(match.group(2))
    if amount >= 8:
      return f"invest domain={match.group(1)} amount={max(4, amount - 2)}"
    return match.group(0)

  return re.sub(
    r"invest domain=(\w+) amount=(\d+)",
    replace_other,
    cmd,
    flags=re.IGNORECASE
  )

def prefer_workforce_commit_over_growth(cmd, workforce_trust):
  if workforce_trust is None or workforce_trust >= WORKFORCE_TRUST_HARD_THRESHOLD:
    return cmd
  if "commit pledge_type=workforce" in cmd.lower():
    return cmd
  parts = [part.strip() for part in cmd.split(";") if part.strip()]
  replaced = False
  updated = []
  for part in parts:
    if not replaced and part.lower().startswith("invest"):
      updated.append("commit pledge_type=workforce level=1")
      replaced = True
    else:
      updated.append(part)
  return "; ".join(updated) if updated else cmd

def adapt_command(cmd, difficulty, obs, turn):
  if difficulty != "hard":
    return cmd

  adapted = reduce_large_invest(cmd)
  adapted = prefer_workforce_commit_over_growth(
    adapted,
    parse_obs_workforce_trust(obs)
  )

  obs_text = "\n".join(obs).upper()
  rivals_visible = any(
    rival in obs_text for rival in ("NORTHLAKE", "SUMMIT", "VALLEY")
  )
  if rivals_visible and "monitor" not in adapted.lower() and turn % 3 == 0:
    adapted = f"monitor target=northlake depth=1; {adapted}"

  if count_action_verbs(adapted) >= 2 and not any(
    part.strip().lower() == "hold" for part in adapted.split(";")
  ):
    adapted = f"{adapted}; hold"

  return adapted

def with_difficulty(base_policy, difficulty):
  def policy(obs, legal, turn):
    if is_stabilization_legal(legal):
      return base_policy(obs, legal, turn)
    base_cmd = base_policy(obs, legal, turn)
    return adapt_command(base_cmd, difficulty, obs, turn)

  return policy

def policy_for_competitive(base_policy, difficulty, target):
  if target == TARGET_DIFFICULTY_ADAPTIVE:
    return with_difficulty(base_policy, difficulty)
  return base_policy

def policy_fiscal(obs, legal, turn):
  if is_stabilization_legal(legal):
    commands = ["4 10 104", "4 5", "8 5", "6 5", "8 5"]
    return commands[turn - 1]
  else:  # competitive
    commands = [
      "monitor target=northlake depth=1; hold",
      "recruit role=nurse headcount=2; hold",
      "commit pledge_type=access level=1; hold",
      "negotiate payer=medicaid rate_posture=neutral; hold",
      "invest domain=emergency amount=8; hold",
      "monitor target=summit depth=1; hold",
      "recruit role=admin headcount=1; hold",
      "commit pledge_type=workforce level=1; hold",
      "invest domain=infusion amount=6; hold",
      "hold",
      "negotiate payer=medicare rate_posture=neutral; hold",
      "monitor target=northlake depth=1; hold",
      "commit pledge_type=quality level=1; hold",
      "invest domain=psychiatric amount=5; hold",
      "invest domain=asc amount=6; hold",
      "monitor target=northlake depth=1; hold",
      "monitor target=summit depth=1; hold",
      "hold",
      "commit pledge_type=access level=1; hold",
      "hold",
      "monitor target=northlake depth=1; hold",
      "hold",
      "commit pledge_type=workforce level=1; hold",
      "hold"
    ]
    if turn <= len(commands):
      return commands[turn - 1]
    return "hold"

def policy_growth(obs, legal, turn):
  if is_stabilization_legal(legal):
    commands = ["12 25 115", "15 9", "15 9", "15 9", "15 9"]
    return commands[turn - 1]
  else:  # competitive
    commands = [
      "invest domain=beds amount=15",
      "recruit role=nurse headcount=2",
      "negotiate payer=carrier_a rate_posture=aggressive",
      "invest domain=emergency amount=6; hold",
      "monitor target=northlake depth=1; hold",
      "invest domain=icu amount=6; hold",
      "invest domain=cardiology amount=6; hold",
      "monitor target=northlake depth=1; hold",
      "commit pledge_type=quality level=2; hold",
      "negotiate payer=carrier_b rate_posture=neutral; hold",
      "invest domain=oncology amount=8; hold",
      "monitor target=northlake depth=1; hold",
      "commit pledge_type=quality level=1; hold",
      "monitor target=summit depth=1; hold",
      "commit pledge_type=access level=2; hold",
      "monitor target=northlake depth=1; hold",
      "negotiate payer=carrier_a rate_posture=neutral; hold",
      "commit pledge_type=workforce level=1; hold",
      "monitor target=summit depth=1; hold",
      "commit pledge_type=quality level=1; hold",
      "monitor target=northlake depth=1; hold",
      "commit pledge_type=workforce level=1; hold",
      "hold",
      "monitor target=summit depth=1; hold"
    ]
    if turn <= len(commands):
      return commands[turn - 1]
    return "hold"

def policy_balanced(obs, legal, turn):
  if is_stabilization_legal(legal):
    commands = ["8 18 112", "10 7", "14 8", "12 8", "14 8"]
    return commands[turn - 1]
  else:  # competitive
    commands = [
      "monitor target=northlake depth=1; recruit role=nurse headcount=4",
      "invest domain=beds amount=15; commit pledge_type=access level=2",
      "negotiate payer=carrier_a rate_posture=neutral; hold",
      "invest domain=outpatient amount=8; hold",
      "monitor target=northlake depth=1; hold",
      "monitor target=summit depth=1; hold",
      "commit pledge_type=workforce level=2; hold",
      "recruit role=admin headcount=1; hold",
      "monitor target=summit depth=1; hold",
      "invest domain=obstetrics amount=5; hold",
      "commit pledge_type=workforce level=1; hold",
      "monitor target=northlake depth=1; hold",
      "invest domain=cardiology amount=6; hold",
      "commit pledge_type=quality level=1; hold",
      "negotiate payer=carrier_b rate_posture=conservative; hold",
      "monitor target=northlake depth=1; hold",
      "commit pledge_type=quality level=1; hold",
      "monitor target=summit depth=1; hold",
      "monitor target=northlake depth=1; hold",
      "monitor target=summit depth=1; hold",
      "commit pledge_type=access level=1; hold",
      "negotiate payer=carrier_a rate_posture=neutral; hold",
      "hold",
      "monitor target=northlake depth=1; hold"
    ]
    if turn <= len(commands):
      return commands[turn - 1]
    return "hold"

def policy_naive_first_time(obs, legal, turn):
  if is_stabilization_legal(legal):
    commands = ["6 10 108", "5 4", "5 4", "5 4", "5 4"]
    return commands[turn - 1]
  else:  # competitive
    commands = [
      "monitor target=northlake depth=1; hold",
      "hold",
      "commit pledge_type=access level=1; hold",
      "recruit role=nurse headcount=1; hold",
      "hold",
      "invest domain=emergency amount=5; hold",
      "monitor target=summit depth=1; hold",
      "hold",
      "commit pledge_type=workforce level=1; hold",
      "negotiate payer=medicaid rate_posture=neutral; hold",
      "hold",
      "invest domain=outpatient amount=5; hold",
      "monitor target=northlake depth=1; hold",
      "hold",
      "recruit role=admin headcount=1; hold",
      "commit pledge_type=quality level=1; hold",
      "hold",
      "negotiate payer=medicare rate_posture=neutral; hold",
      "monitor target=summit depth=1; hold",
      "hold",
      "invest domain=asc amount=5; hold",
      "hold",
      "commit pledge_type=access level=1; hold",
      "hold"
    ]
    if turn <= len(commands):
      return commands[turn - 1]
    return "hold"

def policy_project_coverage(obs, legal, turn):
  if is_stabilization_legal(legal):
    return "6 10 108" if turn == 1 else "5 4"

  commands = [
    "project kind=emergency_pavilion budget=6",
    "project kind=clinic_network budget=9",
    "monitor target=northlake depth=1; hold",
    "commit pledge_type=workforce level=1; hold",
    "monitor target=summit depth=1; hold",
    "negotiate payer=medicaid rate_posture=neutral; hold",
    "monitor target=northlake depth=1; hold",
    "project kind=asc_unit budget=6",
    "commit pledge_type=access level=1; hold",
    "hold",
    "monitor target=summit depth=1; hold",
    "monitor target=summit depth=1; hold",
    "project kind=neurology_unit budget=6",
    "hold",
    "monitor target=northlake depth=1; hold",
    "monitor target=northlake depth=1; hold",
    "monitor target=summit depth=1; hold",
    "hold",
    "commit pledge_type=quality level=1; hold",
    "monitor target=summit depth=1; hold",
    "monitor target=northlake depth=1; hold",
    "hold",
    "commit pledge_type=workforce level=1; hold",
    "project kind=infusion_center budget=6"
  ]
  if turn <= len(commands):
    return commands[turn - 1]
  return "hold"

def parse_stabilization_metrics(obs, debrief=None):
  metrics = {"Cash": "N/A", "Access": "N/A", "Beds": "N/A", "WorkforceTrust": "N/A", "CommunityTrust": "N/A", "Policy": "N/A"}
  # Helper to parse lists of observations
  text = "\n".join(obs)
  debrief_text = "\n".join(debrief or [])
  
  cash_m = re.search(r"Cash:\s*(\d+)", text)
  if cash_m:
    metrics["Cash"] = cash_m.group(1)
    
  access_m = re.search(r"Reported access index:\s*(\d+)", text)
  if access_m:
    metrics["Access"] = access_m.group(1)

  beds_m = re.search(r"Staffed beds:\s*(\d+)", text)
  if beds_m:
    metrics["Beds"] = beds_m.group(1)
    
  wf_m = re.search(r"Workforce trust:\s*(\d+)", text)
  if wf_m:
    metrics["WorkforceTrust"] = wf_m.group(1)

  ct_m = re.search(r"Community trust:\s*(\d+)", text)
  if ct_m:
    metrics["CommunityTrust"] = ct_m.group(1)
    
  pol_m = re.search(r"Policy pressure:\s*(\d+)", text)
  if pol_m:
    metrics["Policy"] = pol_m.group(1)

  tradeoff_m = re.search(
    r"cash moved from \d+ to (\d+), access from \d+ to (\d+), workforce trust from \d+ to (\d+), community trust from \d+ to (\d+), policy pressure from \d+ to (\d+)",
    debrief_text
  )
  if tradeoff_m:
    metrics["Cash"] = tradeoff_m.group(1)
    metrics["Access"] = tradeoff_m.group(2)
    metrics["WorkforceTrust"] = tradeoff_m.group(3)
    metrics["CommunityTrust"] = tradeoff_m.group(4)
    metrics["Policy"] = tradeoff_m.group(5)

  return metrics

def parse_competitive_metrics(obs, history=None, debrief=None):
  metrics = {"Cash": "N/A", "Access": "N/A", "Beds": "N/A", "WorkforceTrust": "N/A", "CommunityTrust": "N/A", "PC": "N/A", "Hash": "N/A", "ActiveProjects": "N/A", "ActiveProjectDraws": "N/A"}
  text = "\n".join(obs)
  debrief_text = "\n".join(debrief or [])

  # Check Riverside Community Health metrics block
  riverside_block = ""
  lines = text.split("\n")
  in_riverside = False
  for line in lines:
    if "RIVERSIDE COMMUNITY HEALTH" in line.upper():
      in_riverside = True
    elif in_riverside and len(line.strip()) == 0:
      # Blank line after block ends
      pass
    elif in_riverside and ("NORTHLAKE" in line.upper() or "SUMMIT" in line.upper() or "VALLEY" in line.upper()):
      in_riverside = False
    
    if in_riverside:
      riverside_block += line + "\n"

  cash_m = re.search(r"Cash runway:\s*\$?(-?\d+)", riverside_block)
  if not cash_m:
    cash_m = re.search(r"Cash:\s*\$?(-?\d+)", riverside_block)
  if cash_m:
    metrics["Cash"] = cash_m.group(1)

  access_m = re.search(r"Reported access:\s*(\d+)", riverside_block)
  if access_m:
    metrics["Access"] = access_m.group(1)

  beds_m = re.search(r"Staffed beds:\s*(\d+)", riverside_block)
  if beds_m:
    metrics["Beds"] = beds_m.group(1)

  wf_m = re.search(r"Workforce trust:\s*(\d+)", riverside_block)
  if not wf_m:
    wf_m = re.search(r"Workforce:\s*(\d+)", riverside_block)
  if wf_m:
    metrics["WorkforceTrust"] = wf_m.group(1)

  ct_m = re.search(r"Community trust:\s*(\d+)", riverside_block)
  if not ct_m:
    ct_m = re.search(r"Community:\s*(\d+)", riverside_block)
  if ct_m:
    metrics["CommunityTrust"] = ct_m.group(1)

  pc_m = re.search(r"Political capital:\s*(\d+)", riverside_block)
  if pc_m:
    metrics["PC"] = pc_m.group(1)

  if history:
    metrics["Hash"] = history[-1]["state_hash"]

  tradeoff_m = re.search(
    r"cash moved from -?\d+ to (-?\d+), access from \d+ to (\d+), quality from \d+ to \d+, workforce trust from \d+ to (\d+), community trust from \d+ to (\d+), and market share from \d+ to \d+",
    debrief_text
  )
  if tradeoff_m:
    metrics["Cash"] = tradeoff_m.group(1)
    metrics["Access"] = tradeoff_m.group(2)
    metrics["WorkforceTrust"] = tradeoff_m.group(3)
    metrics["CommunityTrust"] = tradeoff_m.group(4)

  resource_m = re.search(
    r"Final player resources: political capital (\d+), active projects \d+, active project monthly draws -?\d+, staffed beds (\d+)",
    debrief_text
  )
  if resource_m:
    metrics["PC"] = resource_m.group(1)
    metrics["Beds"] = resource_m.group(2)

  project_m = re.search(
    r"Final player resources: political capital \d+, active projects (\d+), active project monthly draws (-?\d+), staffed beds \d+",
    debrief_text
  )
  if project_m:
    metrics["ActiveProjects"] = project_m.group(1)
    metrics["ActiveProjectDraws"] = project_m.group(2)

  return metrics

def numeric_values(results, key):
  values = []
  for result in results:
    value = result["metrics"].get(key, "N/A")
    if value != "N/A":
      values.append(int(value))
  return values

def format_range(results, key):
  values = numeric_values(results, key)
  if not values:
    return "N/A"
  if min(values) == max(values):
    return str(values[0])
  return f"{min(values)}-{max(values)}"

def print_range_summary(title, results, keys):
  print("====================================================")
  print(title)
  print("====================================================")
  print(f"Sessions: {len(results)}")
  for key in keys:
    print(f"{key}: {format_range(results, key)}")
  print()

def competitive_difficulties_for_target(target):
  if target in (TARGET_DIFFICULTY_SWEEP, TARGET_DIFFICULTY_ADAPTIVE):
    return DIFFICULTY_SWEEP_LEVELS
  return ["normal"]

def write_json_artifact(path, stab_results, comp_results, target):
  artifact = {
    "artifact_type": "automated_playtest_batch",
    "code_version": code_version(),
    "target": target,
    "seeds": SEEDS,
    "strategies": sorted({result["strategy"] for result in stab_results + comp_results}),
    "campaigns": {
      "stabilization-v1": stab_results,
      "competitive-regional-v1": comp_results
    }
  }
  difficulties = competitive_difficulties_for_target(target)
  if len(difficulties) > 1:
    artifact["difficulties"] = difficulties
  os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
  with open(path, "w", encoding="utf-8") as f:
    json.dump(artifact, f, indent=2)
    f.write("\n")

def strategies_for_target(target):
  if target == TARGET_PROJECT_COVERAGE:
    return {
      "Project Coverage": policy_project_coverage
    }
  return {
    "Fiscal Caution": policy_fiscal,
    "Capacity Growth": policy_growth,
    "Balanced Strategy": policy_balanced,
    "Naive First-Time": policy_naive_first_time
  }

def run_tests(json_output=None, target=TARGET_BASELINE):
  subprocess.run(
    ["cargo", "build", "--quiet", "--bin", "vital-margin-mcp"],
    check=True
  )

  strategies = strategies_for_target(target)

  print("====================================================")
  print("STARTING AUTOMATED GAMEPLAY PLAYTEST RUNS")
  print("====================================================\n")
  print(f"Target: {target}\n")

  # 1. Run Stabilization Campaigns
  stab_results = []
  for seed in SEEDS:
    for name, policy in strategies.items():
      print(f"Running stabilization campaign for '{name}' with seed {seed}...")
      res = play_session("stabilization-v1", seed=seed, policy_fn=policy)
      if res:
        metrics = parse_stabilization_metrics(res["final_observation"], res["debrief"])
        stab_results.append({
          "seed": seed,
          "strategy": name,
          "campaign": res["campaign"],
          "metrics": metrics,
          "transition_count": len(res["history"]),
          "transitions": res["history"],
          "final_observation": res["final_observation"],
          "debrief": res["debrief"],
          "validation_failures": res["validation_failures"]
        })
        print(f"  -> Done. Final Cash: {metrics['Cash']}, Reported Access: {metrics['Access']}\n")
      else:
        print(f"  -> Failed to execute run for '{name}' with seed {seed}\n")

  # 2. Run Competitive Campaigns
  comp_results = []
  competitive_difficulties = competitive_difficulties_for_target(target)
  for seed in SEEDS:
    for difficulty in competitive_difficulties:
      for name, policy in strategies.items():
        print(
          f"Running competitive regional campaign for '{name}' with seed {seed} "
          f"at difficulty {difficulty}..."
        )
        competitive_policy = policy_for_competitive(policy, difficulty, target)
        res = play_session(
          "competitive-regional-v1",
          seed=seed,
          difficulty=difficulty,
          policy_fn=competitive_policy
        )
        if res:
          metrics = parse_competitive_metrics(res["final_observation"], res["history"], res["debrief"])
          comp_results.append({
            "seed": seed,
            "strategy": name,
            "campaign": res["campaign"],
            "difficulty": res["difficulty"],
            "metrics": metrics,
            "transition_count": len(res["history"]),
            "transitions": res["history"],
            "final_observation": res["final_observation"],
            "debrief": res["debrief"],
            "validation_failures": res["validation_failures"]
          })
          print(f"  -> Done. Final Hash: {metrics['Hash']}\n")
        else:
          print(
            f"  -> Failed to execute run for '{name}' with seed {seed} "
            f"at difficulty {difficulty}\n"
          )

  expected_stab_sessions = len(SEEDS) * len(strategies)
  expected_comp_sessions = expected_stab_sessions * len(competitive_difficulties)
  if len(stab_results) != expected_stab_sessions or len(comp_results) != expected_comp_sessions:
    raise RuntimeError(
      "Automated playtest batch incomplete: "
      f"stabilization {len(stab_results)}/{expected_stab_sessions}, "
      f"competitive {len(comp_results)}/{expected_comp_sessions}"
    )

  # Print Comparison Tables
  print("====================================================")
  print("STABILIZATION CAMPAIGN COMPARISON SUMMARY")
  print("====================================================")
  print(f"{'Seed':<6} | {'Strategy':<20} | {'Cash':<6} | {'Access':<8} | {'Beds':<6} | {'Workforce':<9} | {'Community':<9}")
  print("-" * 84)
  for result in stab_results:
    m = result["metrics"]
    print(f"{result['seed']:<6} | {result['strategy']:<20} | {m['Cash']:<6} | {m['Access']:<8} | {m['Beds']:<6} | {m['WorkforceTrust']:<9} | {m['CommunityTrust']:<9}")
  print()

  print("====================================================")
  print("COMPETITIVE CAMPAIGN COMPARISON SUMMARY")
  print("====================================================")
  comp_header = (
    f"{'Seed':<6} | {'Strategy':<20} | {'Difficulty':<8} | {'Final Hash':<16} | "
    f"{'Cash':<6} | {'Access':<8} | {'Beds':<6} | {'Workforce':<9} | {'Community':<9} | {'PC':<4}"
  )
  print(comp_header)
  print("-" * (len(comp_header) + 2))
  for result in comp_results:
    m = result["metrics"]
    difficulty = result.get("difficulty") or "normal"
    print(
      f"{result['seed']:<6} | {result['strategy']:<20} | {difficulty:<8} | {m['Hash']:<16} | "
      f"{m['Cash']:<6} | {m['Access']:<8} | {m['Beds']:<6} | {m['WorkforceTrust']:<9} | "
      f"{m['CommunityTrust']:<9} | {m['PC']:<4}"
    )
  print()

  print_range_summary(
    "STABILIZATION SEED-VARIATION RANGES",
    stab_results,
    ["Cash", "Access", "WorkforceTrust", "CommunityTrust", "Policy"]
  )
  print_range_summary(
    "COMPETITIVE SEED-VARIATION RANGES",
    comp_results,
    ["Cash", "Access", "Beds", "WorkforceTrust", "CommunityTrust", "PC"]
  )

  if json_output:
    write_json_artifact(json_output, stab_results, comp_results, target)
    print(f"Automated playtest batch JSON written to {json_output}")

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description="Run automated MCP gameplay playtests")
  parser.add_argument(
    "--target",
    choices=[
      TARGET_BASELINE,
      TARGET_PROJECT_COVERAGE,
      TARGET_DIFFICULTY_SWEEP,
      TARGET_DIFFICULTY_ADAPTIVE
    ],
    default=TARGET_BASELINE,
    help=(
      "Playtest target to run; baseline preserves the default four-profile batch, "
      "project-coverage exercises capital-project commands, difficulty-sweep "
      "runs static baseline profiles at easy and hard competitive difficulty, "
      "and difficulty-adaptive applies rival-aware policy adjustments on hard "
      "(easy remains a static baseline control)"
    )
  )
  parser.add_argument(
    "--json-output",
    help="Optional path for a JSON batch artifact containing observations, transitions, debriefs, and metrics"
  )
  args = parser.parse_args()
  run_tests(json_output=args.json_output, target=args.target)
