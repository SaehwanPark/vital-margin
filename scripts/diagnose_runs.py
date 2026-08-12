#!/usr/bin/env python3
import argparse
import json
import os
import re
import sys
from collections import Counter, defaultdict

def parse_command_verb(cmd):
  if isinstance(cmd, str):
    return cmd
  if isinstance(cmd, dict):
    return list(cmd.keys())[0]
  return "Unknown"

def parse_summary_command_verbs(command_text):
  verbs = []
  for verb in ["Monitor", "Recruit", "Invest", "Negotiate", "Commit", "Project", "Hold"]:
    verbs.extend([verb] * command_text.count(verb))
  return verbs

def parse_summary_project_kinds(command_text):
  kinds = []
  for token in command_text.replace(";", " ").split():
    if token.startswith("kind="):
      kinds.append(token.split("=", 1)[1].strip())
  kinds.extend(re.findall(r"kind:\s*([A-Za-z]+)", command_text))
  return kinds

def parse_raw_command_verbs(command_text):
  verbs = []
  for command in command_text.split(";"):
    token = command.strip().split(maxsplit=1)
    if not token:
      continue
    verb = token[0].lower()
    known = {
      "monitor": "Monitor",
      "recruit": "Recruit",
      "invest": "Invest",
      "negotiate": "Negotiate",
      "commit": "Commit",
      "project": "Project",
      "hold": "Hold"
    }
    if verb in known:
      verbs.append(known[verb])
  return verbs

def parse_final_tradeoff(debrief):
  metrics = {}
  text = "\n".join(debrief)
  tradeoff = re.search(
    r"cash moved from -?\d+ to (?P<Cash>-?\d+), access from -?\d+ to "
    r"(?P<Access>-?\d+), quality from -?\d+ to (?P<Quality>-?\d+), "
    r"workforce trust from -?\d+ to (?P<WorkforceTrust>-?\d+), "
    r"community trust from -?\d+ to (?P<CommunityTrust>-?\d+), and "
    r"market share from -?\d+ to (?P<MarketShare>-?\d+)",
    text
  )
  if tradeoff:
    metrics.update({key: int(value) for key, value in tradeoff.groupdict().items()})

  resources = re.search(
    r"political capital (?P<PC>-?\d+), active projects "
    r"(?P<ActiveProjects>-?\d+), active project monthly draws "
    r"(?P<ActiveProjectDraws>-?\d+), staffed beds (?P<Beds>-?\d+)",
    text
  )
  if resources:
    metrics.update({key: int(value) for key, value in resources.groupdict().items()})
  return metrics

def is_cash_retry(retry):
  if not isinstance(retry, dict):
    return False
  resource_limit = retry.get("resource_limit")
  if isinstance(resource_limit, dict) and resource_limit.get("resource") == "cash":
    return True
  if retry.get("code") == "insufficient_cash":
    return True
  error = str(retry.get("error", "")).lower()
  return "cash required" in error and "exceeds available" in error

def format_retry_detail(retry):
  if not isinstance(retry, dict):
    return str(retry)
  turn = retry.get("turn")
  turn_label = f"turn {turn}" if turn is not None else "unknown turn"
  command = retry.get("command")
  error = retry.get("error", "unknown error")
  if command:
    return f"{turn_label}: {error} [{command}]"
  return f"{turn_label}: {error}"

def summarize_retry_details(retries, limit=2):
  if not retries:
    return "None"
  details = [format_retry_detail(retry) for retry in retries[:limit]]
  remaining = len(retries) - len(details)
  if remaining > 0:
    details.append(f"+{remaining} more")
  return "<br>".join(details)

def classify_strategy(hold_count, verb_counts):
  total_commands = hold_count + sum(verb_counts.values())
  if total_commands == 0:
    return "Passive"
  
  if hold_count / total_commands >= 0.70:
    return "Conservative / Passive"
    
  non_hold_total = sum(verb_counts.values())
  if non_hold_total == 0:
    return "Conservative / Passive"
    
  # Check heuristics
  capacity_verbs = verb_counts.get("Invest", 0) + verb_counts.get("Project", 0)
  if capacity_verbs / non_hold_total >= 0.40:
    return "Capacity-Builder"
    
  if verb_counts.get("Negotiate", 0) / non_hold_total >= 0.40:
    return "Revenue-Optimizer"
    
  if verb_counts.get("Commit", 0) / non_hold_total >= 0.40:
    return "Public-Committed"
    
  if verb_counts.get("Monitor", 0) / non_hold_total >= 0.40:
    return "Intel-Gatherer"
    
  if verb_counts.get("Recruit", 0) / non_hold_total >= 0.40:
    return "Workforce-Focused"
    
  return "Balanced Strategy"

def analyze_single_run(file_path):
  try:
    with open(file_path, 'r') as f:
      data = json.load(f)
  except Exception as e:
    print(f"Error reading {file_path}: {e}", file=sys.stderr)
    return None

  # Basic check
  if "genesis" not in data or "transitions" not in data:
    print(f"Skipping {file_path}: does not match CompetitiveHistory structure.", file=sys.stderr)
    return None

  genesis = data["genesis"]
  transitions = data["transitions"]
  
  difficulty = genesis.get("difficulty", "Normal")
  rival_count = len(genesis.get("systems", [])) - 1
  total_turns = len(transitions)
  
  # Map system_id -> name
  system_names = {sys["system_id"]: sys["name"] for sys in genesis.get("systems", [])}
  
  # Initialize stats per system
  system_stats = {}
  for sys_id, name in system_names.items():
    system_stats[sys_id] = {
      "name": name,
      "holds": 0,
      "verbs": Counter(),
      "burnout_events": 0,
      "resource_trajectories": defaultdict(list)
    }

  # Walk transitions
  for transition in transitions:
    aggregated = transition.get("aggregated", {})
    next_state = transition.get("next", {})
    
    # Process commands in this month's batches
    batches = aggregated.get("batches", [])
    for batch in batches:
      sys_id = batch.get("system_id")
      if sys_id not in system_stats:
        continue
      
      commands = batch.get("commands", [])
      for cmd in commands:
        verb = parse_command_verb(cmd)
        if verb == "Hold":
          system_stats[sys_id]["holds"] += 1
        else:
          system_stats[sys_id]["verbs"][verb] += 1
          
    # Track resources from the resulting state
    next_systems = next_state.get("systems", [])
    for sys_state in next_systems:
      sys_id = sys_state.get("system_id")
      if sys_id not in system_stats:
        continue
      
      res = sys_state.get("resources", {})
      stats = system_stats[sys_id]
      stats["resource_trajectories"]["cash"].append(res.get("cash", 0))
      stats["resource_trajectories"]["political_capital"].append(res.get("political_capital", 0))
      stats["resource_trajectories"]["staffed_beds"].append(sys_state.get("staffed_beds", 0))
      stats["resource_trajectories"]["nurses"].append(sys_state.get("nurses", 0))
      stats["resource_trajectories"]["physicians"].append(sys_state.get("physicians", 0))
      stats["resource_trajectories"]["admins"].append(sys_state.get("admins", 0))
      stats["resource_trajectories"]["access_index"].append(sys_state.get("access_index", 0))
      stats["resource_trajectories"]["quality_index"].append(sys_state.get("quality_index", 0))
      stats["resource_trajectories"]["workforce_trust"].append(sys_state.get("workforce_trust", 0))
      stats["resource_trajectories"]["community_trust"].append(sys_state.get("community_trust", 0))
      stats["resource_trajectories"]["market_share_index"].append(sys_state.get("market_share_index", 0))

    # Look for events/burnout
    events = transition.get("events", [])
    for ev in events:
      ev_str = str(ev).lower()
      for sys_id, name in system_names.items():
        if name.lower() in ev_str and ("burnout" in ev_str or "understaffing" in ev_str):
          system_stats[sys_id]["burnout_events"] += 1

  # Package run info
  return {
    "filename": os.path.basename(file_path),
    "difficulty": difficulty,
    "rival_count": rival_count,
    "total_turns": total_turns,
    "system_stats": system_stats
  }

def empty_playtest_stats():
  return {
    "sessions": 0,
    "holds": 0,
    "verbs": Counter(),
    "validation_failures": 0,
    "cash": [],
    "access": [],
    "beds": [],
    "workforce_trust": [],
    "community_trust": [],
    "political_capital": [],
    "hashes": [],
    "active_projects": [],
    "active_project_draws": [],
    "project_kinds": Counter()
  }

def accumulate_playtest_result(stats, result):
  stats["sessions"] += 1
  stats["validation_failures"] += len(result.get("validation_failures", []))
  for transition in result.get("transitions", []):
    for verb in parse_summary_command_verbs(transition.get("command", "")):
      if verb == "Hold":
        stats["holds"] += 1
      else:
        stats["verbs"][verb] += 1
    for kind in parse_summary_project_kinds(transition.get("command", "")):
      stats["project_kinds"][kind] += 1
  metrics = result.get("metrics", {})
  for key, target in [
    ("Cash", "cash"),
    ("Access", "access"),
    ("Beds", "beds"),
    ("WorkforceTrust", "workforce_trust"),
    ("CommunityTrust", "community_trust"),
    ("PC", "political_capital"),
    ("ActiveProjects", "active_projects"),
    ("ActiveProjectDraws", "active_project_draws")
  ]:
    value = metrics.get(key)
    if value is not None and value != "N/A":
      stats[target].append(int(value))
  if metrics.get("Hash") and metrics["Hash"] != "N/A":
    stats["hashes"].append(metrics["Hash"])

def analyze_playtest_batch(file_path, data):
  competitive = data.get("campaigns", {}).get("competitive-regional-v1", [])
  stabilization = data.get("campaigns", {}).get("stabilization-v1", [])
  if not competitive and not stabilization:
    print(f"Skipping {file_path}: playtest batch has no campaign results.", file=sys.stderr)
    return None

  profile_stats = {}
  difficulty_stats = {}
  profile_difficulty_stats = {}
  for result in competitive:
    strategy = result.get("strategy", "Unknown")
    difficulty = (result.get("difficulty") or "normal").lower()
    profile_key = strategy
    difficulty_key = difficulty
    profile_difficulty_key = f"{strategy} / {difficulty}"

    for key, bucket in [
      (profile_key, profile_stats),
      (difficulty_key, difficulty_stats),
      (profile_difficulty_key, profile_difficulty_stats)
    ]:
      stats = bucket.setdefault(key, empty_playtest_stats())
      accumulate_playtest_result(stats, result)

  return {
    "filename": os.path.basename(file_path),
    "code_version": data.get("code_version", "unknown"),
    "target": data.get("target", "unknown"),
    "seeds": data.get("seeds", []),
    "difficulties": data.get("difficulties", []),
    "stabilization_sessions": len(stabilization),
    "competitive_sessions": len(competitive),
    "profile_stats": profile_stats,
    "difficulty_stats": difficulty_stats,
    "profile_difficulty_stats": profile_difficulty_stats
  }

def analyze_live_capture_batch(file_path, data):
  runs = data.get("runs", [])
  if not runs:
    print(f"Skipping {file_path}: live-capture artifact has no runs.", file=sys.stderr)
    return None

  run_stats = []
  for run in runs:
    verbs = Counter()
    holds = 0
    project_kinds = Counter()
    for command in run.get("commands", []):
      for verb in parse_raw_command_verbs(command):
        if verb == "Hold":
          holds += 1
        else:
          verbs[verb] += 1
      for kind in parse_summary_project_kinds(command):
        project_kinds[kind] += 1

    metrics = parse_final_tradeoff(run.get("debrief", []))
    live_retries = run.get("live_validation_retries") or []
    cash_retries = [retry for retry in live_retries if is_cash_retry(retry)]
    run_stats.append({
      "profile_name": run.get("profile_name", run.get("profile_id", "Unknown")),
      "profile_id": run.get("profile_id", "unknown"),
      "policy_variant": run.get("policy_variant", "unknown"),
      "difficulty": run.get("difficulty", "unknown"),
      "completion_status": run.get("completion_status", "unknown"),
      "run_error": run.get("run_error", ""),
      "transition_count": run.get("transition_count", len(run.get("state_hashes", []))),
      "validation_failures": len(run.get("validation_failures", [])),
      "live_retry_count": len(live_retries),
      "cash_retry_count": len(cash_retries),
      "non_cash_retry_count": len(live_retries) - len(cash_retries),
      "retry_details": summarize_retry_details(live_retries),
      "monitor_intel_line_count": run.get("monitor_intel_line_count", 0),
      "public_rival_line_count": run.get("public_rival_line_count", 0),
      "private_activity_gap_line_count": run.get("private_activity_gap_line_count", 0),
      "no_public_signal_line_count": run.get("no_public_signal_line_count", 0),
      "rival_information_examples": run.get("rival_information_examples", {}),
      "access_pledges": run.get("access_pledge_count", 0),
      "final_hash": run.get("final_hash", "N/A"),
      "holds": holds,
      "verbs": verbs,
      "project_kinds": project_kinds,
      "metrics": metrics,
      "strategy": classify_strategy(holds, verbs)
    })

  return {
    "filename": os.path.basename(file_path),
    "batch_id": data.get("batch_id", "unknown"),
    "code_version": data.get("code_version", "unknown"),
    "campaign": data.get("campaign", "unknown"),
    "difficulty": data.get("difficulty", "unknown"),
    "seed": data.get("seed", "unknown"),
    "evidence_type": data.get("evidence_type", "unknown"),
    "run_stats": run_stats
  }

def format_metric_range(values):
  if not values:
    return "N/A"
  if min(values) == max(values):
    return str(values[0])
  return f"{min(values)}-{max(values)}"

def print_playtest_outcome_table(title, stats_by_key):
  print(f"### {title}")
  print("| Group | Sessions | Cash | Access | Beds | Workforce Trust | Community Trust | PC | Validation Failures | Representative Hashes |")
  print("| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |")
  for group, stats in stats_by_key.items():
    hashes = ", ".join(stats["hashes"][:3]) if stats["hashes"] else "N/A"
    print(
      f"| {group} | {stats['sessions']} | "
      f"{format_metric_range(stats['cash'])} | "
      f"{format_metric_range(stats['access'])} | "
      f"{format_metric_range(stats['beds'])} | "
      f"{format_metric_range(stats['workforce_trust'])} | "
      f"{format_metric_range(stats['community_trust'])} | "
      f"{format_metric_range(stats['political_capital'])} | "
      f"{stats['validation_failures']} | {hashes} |"
    )
  print()

def print_run_markdown(run_data):
  print(f"## Diagnostic Report for `{run_data['filename']}`")
  print(f"- **Difficulty:** {run_data['difficulty']}")
  print(f"- **Rivals:** {run_data['rival_count']}")
  print(f"- **Turns Simulated:** {run_data['total_turns']} months\n")
  
  # Final State Table
  print("### Final Health System Metrics")
  print("| Health System | Cash | Staffed Beds | Nurses | Physicians | Admins | Access | Quality | Workforce Trust | Community Trust | Market Share |")
  print("| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |")
  for sys_id, stats in run_data["system_stats"].items():
    traj = stats["resource_trajectories"]
    last_cash = traj["cash"][-1] if traj["cash"] else "N/A"
    last_beds = traj["staffed_beds"][-1] if traj["staffed_beds"] else "N/A"
    last_nurses = traj["nurses"][-1] if traj["nurses"] else "N/A"
    last_physicians = traj["physicians"][-1] if traj["physicians"] else "N/A"
    last_admins = traj["admins"][-1] if traj["admins"] else "N/A"
    last_access = traj["access_index"][-1] if traj["access_index"] else "N/A"
    last_quality = traj["quality_index"][-1] if traj["quality_index"] else "N/A"
    last_wf_trust = traj["workforce_trust"][-1] if traj["workforce_trust"] else "N/A"
    last_ct_trust = traj["community_trust"][-1] if traj["community_trust"] else "N/A"
    last_share = traj["market_share_index"][-1] if traj["market_share_index"] else "N/A"
    
    print(f"| {stats['name']} | {last_cash} | {last_beds} | {last_nurses} | {last_physicians} | {last_admins} | {last_access} | {last_quality} | {last_wf_trust} | {last_ct_trust} | {last_share}% |")
  print()

  # Command Choice and Strategy Table
  print("### Strategic Profile Summary")
  print("| Health System | Holds | Action Commands | Top Non-Hold Verb | Strategic Classification | Burnout/Penalty Events |")
  print("| --- | ---: | ---: | --- | --- | ---: |")
  for sys_id, stats in run_data["system_stats"].items():
    holds = stats["holds"]
    non_holds = sum(stats["verbs"].values())
    top_verb = stats["verbs"].most_common(1)
    top_verb_str = f"{top_verb[0][0]} ({top_verb[0][1]})" if top_verb else "None"
    strategy = classify_strategy(holds, stats["verbs"])
    print(f"| {stats['name']} | {holds} | {non_holds} | {top_verb_str} | {strategy} | {stats['burnout_events']} |")
  print()

def print_aggregated_markdown(runs):
  print("## Aggregated Diagnostics across Multiple Runs")
  print(f"- **Total Sessions Analyzed:** {len(runs)}")
  
  difficulties = Counter([r["difficulty"] for r in runs])
  diff_str = ", ".join([f"{k} ({v})" for k, v in difficulties.items()])
  print(f"- **Difficulty Distribution:** {diff_str}\n")

  # Compute ranges for Player System (ID 0)
  player_final_cash = []
  player_final_access = []
  player_final_wf_trust = []
  player_final_ct_trust = []
  player_strategies = Counter()
  
  for run in runs:
    player_stats = run["system_stats"].get(0)
    if not player_stats:
      continue
    traj = player_stats["resource_trajectories"]
    if traj["cash"]:
      player_final_cash.append(traj["cash"][-1])
    if traj["access_index"]:
      player_final_access.append(traj["access_index"][-1])
    if traj["workforce_trust"]:
      player_final_wf_trust.append(traj["workforce_trust"][-1])
    if traj["community_trust"]:
      player_final_ct_trust.append(traj["community_trust"][-1])
      
    strategy = classify_strategy(player_stats["holds"], player_stats["verbs"])
    player_strategies[strategy] += 1

  if player_final_cash:
    print("### Player Health System Outcome Ranges")
    print("| Metric | Minimum | Maximum | Average |")
    print("| --- | ---: | ---: | ---: |")
    print(f"| Cash | {min(player_final_cash)} | {max(player_final_cash)} | {sum(player_final_cash)/len(player_final_cash):.1f} |")
    print(f"| Access | {min(player_final_access)} | {max(player_final_access)} | {sum(player_final_access)/len(player_final_access):.1f} |")
    print(f"| Workforce Trust | {min(player_final_wf_trust)} | {max(player_final_wf_trust)} | {sum(player_final_wf_trust)/len(player_final_wf_trust):.1f} |")
    print(f"| Community Trust | {min(player_final_ct_trust)} | {max(player_final_ct_trust)} | {sum(player_final_ct_trust)/len(player_final_ct_trust):.1f} |")
    print()

    print("### Player Strategy Profile Distribution")
    print("| Strategy Profile | Occurrence Count | Percentage |")
    print("| --- | ---: | ---: |")
    for strat, count in player_strategies.items():
      pct = (count / len(runs)) * 100
      print(f"| {strat} | {count} | {pct:.1f}% |")
    print()

def print_adaptive_difficulty_comparison(batch):
  if batch.get("target") != "difficulty-adaptive":
    return

  difficulty_stats = batch.get("difficulty_stats", {})
  easy = difficulty_stats.get("easy")
  hard = difficulty_stats.get("hard")
  if not easy or not hard:
    return

  print("### Difficulty-Adaptive Action Comparison")
  print("| Difficulty | Holds | Action Commands | Monitor | Invest | Recruit | Commit |")
  print("| --- | ---: | ---: | ---: | ---: | ---: | ---: |")
  for label, stats in [("easy", easy), ("hard", hard)]:
    print(
      f"| {label} | {stats['holds']} | {sum(stats['verbs'].values())} | "
      f"{stats['verbs'].get('Monitor', 0)} | {stats['verbs'].get('Invest', 0)} | "
      f"{stats['verbs'].get('Recruit', 0)} | {stats['verbs'].get('Commit', 0)} |"
    )
  print()
  print(
    "- Adaptive hard policies should show more holds and monitors than easy when "
    "rival pressure triggers the adaptation layer."
  )
  print(
    "- Compare player tradeoff metrics in the difficulty tables above against "
    "the static `difficulty-sweep` batch to see whether adaptation differentiates "
    "Easy/Hard endpoints for the same seed/profile."
  )
  print()

def print_playtest_batch_markdown(batch):
  print(f"## Playtest Batch Diagnostics for `{batch['filename']}`")
  print(f"- **Code version:** {batch['code_version']}")
  print(f"- **Target:** {batch.get('target', 'unknown')}")
  print(f"- **Seeds:** {', '.join(str(seed) for seed in batch['seeds'])}")
  if batch.get("difficulties"):
    print(f"- **Competitive difficulties:** {', '.join(batch['difficulties'])}")
  print(f"- **Stabilization sessions:** {batch['stabilization_sessions']}")
  print(f"- **Competitive sessions:** {batch['competitive_sessions']}\n")

  print_playtest_outcome_table("Competitive Profile Outcomes", batch["profile_stats"])

  if batch.get("difficulty_stats"):
    print_playtest_outcome_table(
      "Competitive Outcomes by Difficulty",
      batch["difficulty_stats"]
    )

  if batch.get("profile_difficulty_stats") and len(batch["profile_difficulty_stats"]) > len(batch["profile_stats"]):
    print_playtest_outcome_table(
      "Competitive Profile Outcomes by Difficulty",
      batch["profile_difficulty_stats"]
    )

  print_adaptive_difficulty_comparison(batch)

  print("### Competitive Action Frequency Signals")
  print("| Profile | Holds | Action Commands | Project Commands | Top Non-Hold Verb | Strategy Classification |")
  print("| --- | ---: | ---: | ---: | --- | --- |")
  for profile, stats in batch["profile_stats"].items():
    non_holds = sum(stats["verbs"].values())
    project_commands = stats["verbs"].get("Project", 0)
    top_verb = stats["verbs"].most_common(1)
    top_verb_str = f"{top_verb[0][0]} ({top_verb[0][1]})" if top_verb else "None"
    strategy = classify_strategy(stats["holds"], stats["verbs"])
    print(f"| {profile} | {stats['holds']} | {non_holds} | {project_commands} | {top_verb_str} | {strategy} |")
  print()

  print("### Competitive Project Coverage")
  print("| Profile | Project Kinds | Final Active Projects | Final Monthly Draws |")
  print("| --- | --- | ---: | ---: |")
  for profile, stats in batch["profile_stats"].items():
    project_kinds = ", ".join(
      f"{kind} ({count})" for kind, count in stats["project_kinds"].most_common()
    ) or "None"
    print(
      f"| {profile} | {project_kinds} | "
      f"{format_metric_range(stats['active_projects'])} | "
      f"{format_metric_range(stats['active_project_draws'])} |"
    )
  print()

  print("### Evidence Limits")
  print("- Batch diagnostics use MCP transition summaries, final observations, and debriefs; they are not full replay artifacts.")
  print("- These diagnostics support gameplay and explanation review, not human-learning, empirical calibration, or policy-validity claims.")
  print("- Treat formula tuning or runtime expansion as a separate follow-up requiring stronger evidence.\n")

def print_live_capture_batch_markdown(batch):
  print(f"## Live-Capture Diagnostics for `{batch['filename']}`")
  print(f"- **Batch id:** {batch['batch_id']}")
  print(f"- **Code version:** {batch['code_version']}")
  print(f"- **Campaign:** {batch['campaign']}")
  print(f"- **Difficulty:** {batch['difficulty']}")
  print(f"- **Seed:** {batch['seed']}")
  print(f"- **Evidence type:** {batch['evidence_type']}\n")

  print("### Profile Outcomes")
  print("| Profile | Status | Months | Cash | Access | Quality | Workforce Trust | Community Trust | Market Share | PC | Beds | Validation Failures | Access Pledges | Final Hash |")
  print("| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |")
  for stats in batch["run_stats"]:
    metrics = stats["metrics"]
    status = stats["completion_status"]
    if stats["run_error"]:
      status = f"{status}: {stats['run_error']}".replace("|", "\\|")
    print(
      f"| {stats['profile_name']} | {status} | {stats['transition_count']} | "
      f"{metrics.get('Cash', 'N/A')} | {metrics.get('Access', 'N/A')} | "
      f"{metrics.get('Quality', 'N/A')} | {metrics.get('WorkforceTrust', 'N/A')} | "
      f"{metrics.get('CommunityTrust', 'N/A')} | {metrics.get('MarketShare', 'N/A')} | "
      f"{metrics.get('PC', 'N/A')} | {metrics.get('Beds', 'N/A')} | "
      f"{stats['validation_failures']} | {stats['access_pledges']} | "
      f"{stats['final_hash']} |"
    )
  print()

  print("### Action Frequency Signals")
  print("| Profile | Holds | Action Commands | Monitor | Recruit | Invest | Negotiate | Commit | Project | Top Non-Hold Verb | Strategy Classification |")
  print("| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- |")
  for stats in batch["run_stats"]:
    verbs = stats["verbs"]
    non_holds = sum(verbs.values())
    top_verb = verbs.most_common(1)
    top_verb_str = f"{top_verb[0][0]} ({top_verb[0][1]})" if top_verb else "None"
    print(
      f"| {stats['profile_name']} | {stats['holds']} | {non_holds} | "
      f"{verbs.get('Monitor', 0)} | {verbs.get('Recruit', 0)} | "
      f"{verbs.get('Invest', 0)} | {verbs.get('Negotiate', 0)} | "
      f"{verbs.get('Commit', 0)} | {verbs.get('Project', 0)} | "
      f"{top_verb_str} | {stats['strategy']} |"
    )
  print()

  print("### Live Retry Signals")
  print("| Profile | Difficulty | Final Validation Failures | Live Retries | Cash-Overrun Retries | Other Retries | Representative Retry Details |")
  print("| --- | --- | ---: | ---: | ---: | ---: | --- |")
  for stats in batch["run_stats"]:
    print(
      f"| {stats['profile_name']} | {stats['difficulty']} | "
      f"{stats['validation_failures']} | {stats['live_retry_count']} | "
      f"{stats['cash_retry_count']} | {stats['non_cash_retry_count']} | "
      f"{stats['retry_details']} |"
    )
  print()

  if any(
    stats["monitor_intel_line_count"]
    or stats["public_rival_line_count"]
    or stats["private_activity_gap_line_count"]
    or stats["no_public_signal_line_count"]
    for stats in batch["run_stats"]
  ):
    print("### Rival Information Signals")
    print("| Profile | Difficulty | Variant | Monitor Intel Lines | Public Rival Lines | Private Activity Gaps | No Public Signal Lines | Example Signal |")
    print("| --- | --- | --- | ---: | ---: | ---: | ---: | --- |")
    for stats in batch["run_stats"]:
      examples = stats["rival_information_examples"]
      example = "None"
      for key in ["monitor_intel", "public_rival", "private_activity_gap", "no_public_signal"]:
        values = examples.get(key, [])
        if values:
          example = values[0].replace("|", "\\|")
          break
      print(
        f"| {stats['profile_name']} | {stats['difficulty']} | "
        f"{stats['policy_variant']} | {stats['monitor_intel_line_count']} | "
        f"{stats['public_rival_line_count']} | "
        f"{stats['private_activity_gap_line_count']} | "
        f"{stats['no_public_signal_line_count']} | {example} |"
      )
    print()

  print("### Evidence Limits")
  print("- Live-capture diagnostics use actor-visible observations, submitted commands, transition summaries, and debrief text from the captured MCP wrapper artifact.")
  print("- Live retry signals come from optional wrapper metadata and describe rejected or retried decision attempts before the accepted command stream; they are separate from final replay validation failures.")
  print("- These diagnostics support gameplay, command-surface, and explanation review; they are not human-learning, empirical-calibration, policy-validity, or balance evidence.")
  print("- Do not use a single seed, difficulty, or scripted persona batch to justify runtime tuning.\n")

def main():
  parser = argparse.ArgumentParser(description="Strategy-Space Diagnostics for Vital Margin")
  parser.add_argument("inputs", nargs="+", help="Paths to replay JSON files or directories containing replay files")
  parser.add_argument("--output", help="Output file path (saves as markdown; defaults to printing to stdout)")
  
  args = parser.parse_args()
  
  # Resolve inputs (handling directories)
  files = []
  for path in args.inputs:
    if os.path.isdir(path):
      for entry in os.listdir(path):
        if entry.endswith(".json"):
          files.append(os.path.join(path, entry))
    else:
      files.append(path)
      
  if not files:
    print("Error: No JSON replay files found.", file=sys.stderr)
    sys.exit(1)
    
  # Analyze
  runs = []
  batches = []
  live_batches = []
  for file in files:
    try:
      with open(file, "r", encoding="utf-8") as f:
        data = json.load(f)
    except Exception as e:
      print(f"Error reading {file}: {e}", file=sys.stderr)
      continue

    if data.get("artifact_type") == "automated_playtest_batch":
      res = analyze_playtest_batch(file, data)
      if res:
        batches.append(res)
    elif data.get("runs") is not None and data.get("evidence_type") is not None:
      res = analyze_live_capture_batch(file, data)
      if res:
        live_batches.append(res)
    else:
      res = analyze_single_run(file)
      if res:
        runs.append(res)
      
  if not runs and not batches and not live_batches:
    print("Error: No runs could be successfully parsed.", file=sys.stderr)
    sys.exit(1)
    
  # Redirect output if requested
  original_stdout = sys.stdout
  if args.output:
    try:
      sys.stdout = open(args.output, "w")
    except Exception as e:
      print(f"Error opening output file {args.output}: {e}", file=sys.stderr)
      sys.exit(1)
      
  # Print reports
  print("# Strategy-Space Diagnostic Report")
  print("This diagnostic summary maps strategic actions, outcome distributions, and strategy-cluster classifications.\n")
  
  for batch in batches:
    print_playtest_batch_markdown(batch)
    print("---")

  for batch in live_batches:
    print_live_capture_batch_markdown(batch)
    print("---")

  for run in runs:
    print_run_markdown(run)
    print("---")
    
  if len(runs) > 1:
    print_aggregated_markdown(runs)
    
  # Clean up stdout redirect
  if args.output:
    sys.stdout.close()
    sys.stdout = original_stdout
    print(f"Diagnostic report written successfully to {args.output}")

if __name__ == "__main__":
  main()
