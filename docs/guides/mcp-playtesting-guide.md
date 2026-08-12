# MCP Playtesting Guide

This guide describes how to run automated gameplay evidence of the Health Policy
Strategy Game using the Model Context Protocol (MCP) interface, the loopback GUI
host, and the provided Python tooling. It is the operational runbook for the
active [`AI-Agent Playtest Protocol`](../validation/playtesting.md).

## Current operating rule (v0.14.3)

Use agents or scripted policies by default across `stabilization-v1`,
`competitive-regional-v1`, and `regional-affiliation-v1`. The MCP stdio server
owns session truth, validation, action ordering, transitions, history/replay,
and debriefs in process memory. The loopback GUI host additionally provides
durable checkpoint archives, discovery, and restoration when configured; GUI and
MCP clients consume the same actor-visible projections. Chromium evergreen desktop is the default GUI target,
with the Codex in-app browser used for development inspection. Firefox,
WebKit/Safari, mobile, and legacy browsers are deferred and non-certified.

Human sessions are optional external feedback. They can inform a separately
authorized research or product decision, but they do not gate technical
progression. Automated evidence does not prove human learning, lived
accessibility, legal clearance, calibration, balance, or policy validity.

The versioned run notes below preserve historical evidence and command examples;
they do not create current roadmap gates. Prefer the current routes, schemas,
and campaign coverage documented in `ARCHITECTURE.md`.

## Architecture Overview

The playtesting harness decouples the simulation logic from the player client:
1. **MCP/GUI host:** The Rust executables expose bounded stdio and loopback HTTP
   tools using JSON-RPC/JSON DTOs. Both use `GameSessionStore` and host-owned
   session state; durable checkpoint discovery/restoration is a configured
   loopback GUI-host capability, not a default MCP-stdio capability.
2. **Python Client Wrapper:** Located in `scripts/play_game.py`. It starts the MCP server as a subprocess, performs the initialize handshake, and exposes high-level Python wrappers for:
   - Starting a campaign session (`start_session`)
   - Submitting commands and advancing turns (`submit_turn`)
   - Receiving the latest transition and debrief from the session result
     (`end_session`); use the MCP `get_history` tool directly when a full
     history read is required.

## Running Automated Playtests

We have automated four scripted profiles (Fiscal Caution, Capacity Growth,
Balanced Strategy, and Naive First-Time) across the stabilization and
competitive campaign previews. Regional-affiliation coverage uses the
host-backed MCP/GUI campaign-coverage path. Competitive scripts submit commands
across the 24-month campaign and include newer service-line, public-payer, staffing,
monitoring, and commitment actions. Treat these runs as simulated-player
evidence; they do not measure actual human learning or classroom effectiveness.

To execute the automated playtests and print a comparison table of their ending metrics:

```bash
python3 scripts/run_automated_playtests.py
```

To persist a compact JSON artifact for strategy-space diagnostics:

```bash
python3 scripts/run_automated_playtests.py --json-output _workspace/experiments/v0.9.6-playtest-policy-coverage/results.json
python3 scripts/diagnose_runs.py _workspace/experiments/v0.9.6-playtest-policy-coverage/results.json --output _workspace/experiments/v0.9.6-playtest-policy-coverage/diagnostics.md
```

To run the targeted project-command coverage diagnostic:

```bash
python3 scripts/run_automated_playtests.py --target project-coverage --json-output _workspace/experiments/v0.9.7-project-command-coverage/results.json
python3 scripts/diagnose_runs.py _workspace/experiments/v0.9.7-project-command-coverage/results.json --output _workspace/experiments/v0.9.7-project-command-coverage/diagnostics.md
```

To run the targeted difficulty-tier competitive sweep:

```bash
python3 scripts/run_automated_playtests.py --target difficulty-sweep --json-output _workspace/experiments/v0.9.8-difficulty-sweep/results.json
python3 scripts/diagnose_runs.py _workspace/experiments/v0.9.8-difficulty-sweep/results.json --output _workspace/experiments/v0.9.8-difficulty-sweep/diagnostics.md
```

To run the targeted difficulty-adaptive competitive sweep:

```bash
python3 scripts/run_automated_playtests.py --target difficulty-adaptive --json-output _workspace/experiments/v0.9.9-difficulty-adaptive/results.json
python3 scripts/diagnose_runs.py _workspace/experiments/v0.9.9-difficulty-adaptive/results.json --output _workspace/experiments/v0.9.9-difficulty-adaptive/diagnostics.md
```

To run the v0.11.1 operating-loop AI validation matrix and audit its
player-owned monthly operating evidence:

```bash
python3 _workspace/experiments/v0.11.1-operating-loop-ai-validation/run_sessions.py
python3 _workspace/experiments/v0.11.1-operating-loop-ai-validation/run_audit.py
python3 -m unittest tests/test_operating_loop_ai_validation.py
```

To audit operating-loss and bottleneck explainability from the existing
v0.11.1 artifact without launching new sessions:

```bash
python3 _workspace/experiments/v0.11.2-operating-loss-explainability/run_audit.py
python3 -m unittest tests/test_operating_loss_explainability.py
```

This read-only audit separates decision-time context, transition attribution,
month-level debrief outcome linkage, and global debrief attribution. It is
descriptive traceability evidence, not causal, balance, or human-learning
evidence.

Competitive end-session debriefs now also include one `Operating result:` line
per committed player month. The line is derived from committed player state and
reports visible game-unit demand, treated volume, unmet demand, revenue, cost,
and margin; it is a post-run outcome link, not a calibrated financial or clinical
measure.

To validate the post-v0.11.3 operating-result linkage matrix:

```bash
python3 _workspace/experiments/v0.11.4-operating-outcome-debrief-validation/run_sessions.py
python3 _workspace/experiments/v0.11.4-operating-outcome-debrief-validation/run_audit.py
python3 -m unittest tests/test_operating_outcome_debrief_validation.py
```

The v0.11.4 artifact covers 60 runs and 1,440 committed months, with one
player-owned result line per month and 469/469 categorized signal-month
outcome links. It remains descriptive traceability evidence, not causal,
balance, winnability, calibration, human-learning, or policy-validity evidence.

To audit operating-outcome use without launching new sessions:

```bash
python3 _workspace/experiments/v0.11.5-operating-outcome-use-audit/run_audit.py
python3 -m unittest tests/test_operating_outcome_use_audit.py
```

The v0.11.5 read-only audit checks prior-month observation timing, exact
player-owned debrief outcomes, signal-to-next-command continuity, terminal
signals, and rival-result boundaries. It reports 441 non-terminal response
opportunities and 28 expected terminal signals in the frozen v0.11.4 capture.
Response distributions remain descriptive simulated-policy evidence and do not
establish causality, comprehension, learning, balance, or runtime-promotion
need.

This matrix runs five deterministic policy lanes across seeds `42`, `43`, `44`
and Easy/Normal/Hard/Expert. It is descriptive gameplay-validation evidence;
it does not establish causal marginal effects, dominance, balance, calibration,
human learning, or policy validity.

### Expected Output
The script builds `vital-margin-mcp`, launches the local stdio binary, runs both
campaigns for all four profiles across seeds `42`, `43`, and `44`, and
prints per-seed comparison tables plus compact metric ranges. Stabilization
metrics are parsed from the committed debrief. Competitive end-session debriefs
expose final player tradeoff metrics from committed history; treat those as
scripted-agent evidence, not human learning or empirical calibration evidence.
The optional JSON artifact records final observations, transition summaries,
debrief lines, validation failures, and metrics for lightweight diagnostics; it
is not a full replay artifact.
As of `v0.10.23`, competitive debriefs can include an access follow-through
note for low-cash access-heavy runs when public pledges outnumber durable
operational follow-through. Treat that note as explanatory product wording, not
as a balance change, validation failure, or human-learning result.
As of `v0.10.24`, bounded trigger/control MCP runs validate that the note
appears through end-session debriefs when expected and stays absent in nearby
controls. Keep follow-up work evidence-led; this validation does not justify
runtime tuning, pledge cooldowns, command-cost changes, or difficulty changes.
As of `v0.10.28`, the strategy-space synthesis compares finance-first,
access-heavy, workforce-protective, and growth-oriented signals across existing
competitive evidence. Treat those strategy labels as interpretive development
summaries, not hidden game classes, validated learner archetypes, or balance
proof.
As of `v0.10.29`, the debrief comparison surface turns the strategy-space
synthesis into a compact instructor/reviewer aid for comparing decision quality,
outcome quality, cash runway, durable follow-through, rival pressure, and
debrief traceability across repeated competitive runs. Treat it as discussion
design, not as human-learning validation, empirical calibration, or runtime
tuning evidence.
As of `v0.10.30`, the workforce-protective evidence review narrows one
comparison axis from the debrief surface. Treat workforce-protective play as an
interpretive review posture across staffing follow-through, workforce trust,
pacing, monitoring, and commitment discipline, not as a hidden strategy class,
validated learner archetype, standalone balance proof, or reason to tune
workforce formulas.
As of `v0.10.33`, the growth/capacity-oriented evidence review narrows a
parallel comparison axis from the debrief surface. Treat growth/capacity play
as an interpretive review posture across projects, investments, staffed
capacity, cash runway, access, and rival pressure, not as a hidden strategy
class, validated learner archetype, standalone balance proof, or reason to
tune project costs or capacity effects.
As of `v0.10.34`, the instructor debrief facilitation note sequences recent
comparison, workforce-protective, and growth/capacity evidence into classroom
or reviewer prompts. Treat it as a discussion aid, not as measured human
learning, a validated assessment instrument, or a reason to tune runtime
mechanics.
As of `v0.10.39`, competitive MCP observations include four deterministic,
non-binding consultant options derived from the actor-visible observation, and
competitive debriefs retain the options shown for comparison with submitted
actions. Treat this as an explanation and traceability improvement, not as
advice quality evidence, a learning claim, or an advisor-market implementation.
As of `v0.10.40`, competitive transition summaries also include the consultant
options already retained in history. The consultant-advice traceability matrix
uses that additive audit field to verify rendered options match committed history
and remain available in debriefs across existing profiles, seeds, and
Normal/Hard difficulty. Its command-family counts are descriptive only; they do
not measure advice uptake, quality, learning, or causal outcomes.

```bash
python3 _workspace/experiments/v0.10.40-consultant-advice-evidence/run_sessions.py
python3 -m json.tool _workspace/experiments/v0.10.40-consultant-advice-evidence/results.json
```

As of `v0.10.41`, the consultant-advice usage matrix pairs two existing control
policies with deterministic advice-aware wrappers. The wrappers use only visible
consultant options, observation cues, and resource hints; they record selection,
fallback, safe-hold, and command-alignment signals. The controls must retain the
v0.10.40 state hashes. Treat all signals as simulated-policy evidence, not advice
quality, causal impact, human learning, or balance evidence.

```bash
python3 _workspace/experiments/v0.10.41-consultant-advice-usage/run_sessions.py
python3 -m json.tool _workspace/experiments/v0.10.41-consultant-advice-usage/results.json
```

As of `v0.10.42`, the consultant-advice synthesis closes the generic-baseline
evidence chain. The v0.10.40 and v0.10.41 artifacts establish observation,
history, debrief, reproducibility, visible-cue, and fallback behavior across
existing profiles, seeds, and Normal/Hard difficulty. Keep the advisor market
deferred unless a later artifact identifies a concrete limitation that the
generic baseline cannot address. These artifacts do not establish advice
quality, causal impact, human learning, calibration, or balance evidence.

```bash
python3 -m json.tool _workspace/experiments/v0.10.40-consultant-advice-evidence/results.json
python3 -m json.tool _workspace/experiments/v0.10.41-consultant-advice-usage/results.json
```

As of `v0.10.43`, the rival-information follow-through capture compares three
deterministic policies across seeds 42–44 and Hard/Expert difficulty:
monitor-reactive, monitor-ignoring, and unmonitored. It records whether a
monitor signal in one actor-visible observation is followed by a next-turn
simulated-policy response. Treat the records as signal-to-command traceability,
not causal monitor value, human-learning, balance, or difficulty evidence.

```bash
python3 _workspace/experiments/v0.10.43-rival-info-follow-through/run_sessions.py
python3 -m json.tool _workspace/experiments/v0.10.43-rival-info-follow-through/results.json
```

The monitor-ignoring and unmonitored controls should retain matching hashes;
reactive endpoint differences are expected because the response policy submits
different commands. Keep runtime monitor and difficulty mechanics deferred
unless later evidence identifies a concrete explanation or gameplay gap.

As of `v0.10.54`, the project-limit recovery capture starts two valid projects,
submits a third project, and preserves the rejection, same-turn observation,
safe retry, history, hashes, and debrief across Hard seeds `42`, `43`, and `44`.
The response exposes `too_many_concurrent_projects` and a plain limit message
without structured `resource_limit` or `hint` fields. Treat that as recovery-
surface evidence, not proof of human comprehension or a reason to change the
MCP schema or runtime behavior.

```bash
python3 _workspace/experiments/v0.10.54-project-limit-recovery/run_sessions.py
python3 -m json.tool _workspace/experiments/v0.10.54-project-limit-recovery/results.json
```

As of `v0.10.55`, the ASC project observation capture reruns the v0.10.54
project-limit schedule after correcting the missing `AscCapacity` observation
branch. It verifies that accepted `ClinicNetwork` and `AscUnit` projects are
both visible before and after a rejected third-project command, while all
transition hashes remain identical to the v0.10.54 source artifact.

```bash
python3 _workspace/experiments/v0.10.55-asc-project-observation/run_sessions.py
python3 -m json.tool _workspace/experiments/v0.10.55-asc-project-observation/results.json
```

As of `v0.10.56`, the project-recovery-use capture adds a response-conditioned
simulated policy to the same schedule. The recovery branch reads only the plain
validation error and unchanged actor-visible observation, does not consume
`code`, `hint`, or `resource_limit` fields, and preserves v0.10.55 hashes.
Treat this as response-surface traceability evidence, not human comprehension
or a reason to change the MCP schema.

```bash
python3 _workspace/experiments/v0.10.56-project-recovery-use/run_sessions.py
python3 -m json.tool _workspace/experiments/v0.10.56-project-recovery-use/results.json
```

As of `v0.10.57`, the read-only debrief-use audit checks event-specific
continuity across the rival-pressure, strategy, resource-retry, and
project-recovery artifacts. It verifies visibility, response, follow-through,
outcome, explanation coverage, and v0.10.54–v0.10.56 project hash continuity
without launching new sessions. Treat supported coverage as traceability
evidence, not proof of debrief clarity, learning, or classroom effectiveness.

```bash
python3 _workspace/experiments/v0.10.57-debrief-use-audit/run_audit.py
python3 -m json.tool _workspace/experiments/v0.10.57-debrief-use-audit/results.json
```

As of `v0.10.58`, the read-only debrief-coherence audit joins decision-time
observations, submitted commands, accepted transitions, delayed or partial
context, outcomes, and retrospective decision-quality framing across the same
six source artifacts. It preserves the v0.10.51 pre-submit observation contract
for expected resource probes and keeps runtime promotion deferred.

```bash
python3 _workspace/experiments/v0.10.58-debrief-coherence-audit/run_audit.py
python3 -m json.tool _workspace/experiments/v0.10.58-debrief-coherence-audit/results.json
```

As of `v0.10.35`, the difficulty pressure dimension gate selects rival
information and monitoring pressure visibility as the next bounded difficulty
surface to design or test if difficulty remains the active priority. Treat it
as a routing gate, not as Expert winnability evidence, runtime tuning,
scoring evidence, or a reason to give rivals hidden omniscience.
As of `v0.10.36`, the rival information pressure design note defines
information delay, monitor value, and public disclosure as the reviewable
difficulty surfaces for future testing. Treat those tier descriptions as design
hypotheses, not implemented rules, empirical calibration, Expert winnability
proof, or a reason to change AP budgets, command costs, scoring, or balance.
As of `v0.10.37`, paired Hard/Expert live MCP captures compare monitored and
unmonitored rival-information policies at seed `42`. Treat the result as
observation-surface evidence for monitor value and debrief traceability, not as
human-learning validation, empirical calibration, Expert winnability proof, or
runtime tuning evidence.
The `project-coverage` target is intentionally narrower than the default
baseline and is meant to exercise capital-project command paths, not to model a
recommended strategy or justify balance changes.
The `difficulty-sweep` target runs the four baseline competitive profiles at
`easy` and `hard` across seeds `42`, `43`, and `44`. It satisfies the agent
playtest protocol's difficulty-variation requirement without changing the default
Normal-only baseline batch.
The `difficulty-adaptive` target uses the same Easy/Hard matrix but wraps
baseline profiles with rival-aware command adjustments on Hard difficulty only
(Easy passes through static month tables). Reduced aggressive invests, added
monitors/holds, and workforce-commit preference when trust is low apply on Hard.
Use it when testing whether difficulty tiers change scripted player tradeoff
metrics; compare results against the static `difficulty-sweep` batch rather than
treating either batch as balance evidence.

## Creating a Custom Strategy Policy

You can define a custom programmatic policy to test new behaviors. A policy is a Python function that takes:
- `obs`: List of strings representing the current actor-visible observations.
- `legal`: List of strings containing hints or descriptions of legal command formats.
- `turn`: The current 1-indexed turn or month.

And returns a string command batch.

### Example Policy Function

```python
def my_custom_policy(obs, legal, turn):
  # Stabilization Turn 1 input: staffed_beds capital_spend requested_rate
  if turn == 1:
    return "6 12 110"
  
  # Competitive commands
  if turn == 2:
    return "recruit role=nurse headcount=3; monitor target=northlake depth=1"
    
  return "hold"
```

To run this policy:

```python
from play_game import play_session

result = play_session("competitive-regional-v1", seed=42, policy_fn=my_custom_policy)
print(result["debrief"])
```

## Interactive Play via MCP Client

You can also use the python script to play interactively in the terminal by omitting the `policy_fn`:

```python
python3 scripts/play_game.py stabilization-v1
```

This will print the observation and prompt you to input the commands manually, sending them directly to the underlying MCP server.

## Free-Form Agent Evidence Runs

Use this procedure when collecting a bounded free-form agent artifact rather
than adding another scripted policy. The operator or agent should choose
commands only from player-facing docs, current MCP observations, and the
`legal_commands` hints returned by the server.

1. Use seed `42` unless the findings question requires seed variation.
2. Run all current campaigns: `stabilization-v1`,
   `competitive-regional-v1`, and `regional-affiliation-v1` with normal
   difficulty where supported.
3. Record the agent profile or persona, observations shown, legal command hints,
   submitted command text, validation errors and retries, transition hashes,
   final debrief, and the agent's causal explanation after reading the history
   and debrief.
4. Label the result as free-form agent evidence. Do not present it as human
   learning evidence, empirical calibration, balance validation, or policy
   forecasting.

The run may use `scripts/play_game.py` interactively or a small operator-owned
MCP client wrapper. Do not commit a new LLM runner unless repeated findings show
that the existing client cannot capture the needed evidence.

## Free-Form Hard Competitive Runs

Use this procedure when collecting observation-driven free-form evidence on the
full 24-month competitive campaign at Hard difficulty. This extends the general
free-form procedure above. This slice omits stabilization and Normal difficulty;
it is competitive Hard only.

1. Build the MCP server: `cargo build --bin vital-margin-mcp`.
2. Start `competitive-regional-v1` with `difficulty=hard` and seed `42` unless
   the findings question requires seed variation.
3. Use deterministic observation-heuristic policies or manual command entry
   (not LLM play unless separately documented). Choose commands only from
   player-facing docs, current MCP observations, and `legal_commands` hints.
   Record persona prompts, per-month observation cues, submitted commands,
   validation failures, transition hashes, and final debrief metrics.
4. Run at least two distinct free-form profiles. Recommended personas from prior
   evidence: Free-Form Fiscal Steward, Free-Form Access Expansion Advocate, and
   Free-Form First-Time Executive.
5. Compare outcomes against the v0.9.9 `--target difficulty-adaptive` Hard
   scripted baselines for the same seed rather than treating either artifact as
   balance evidence.
6. Label results as free-form simulated-agent evidence. Do not present them as
   human learning, empirical calibration, or policy forecasting.

Operator capture for free-form Hard competitive runs:

```bash
python3 _workspace/experiments/v0.10.0-free-form-hard/run_sessions.py
```

The operator script writes `_workspace/experiments/v0.10.0-free-form-hard/results.json`.
Findings are synthesized in versioned
`docs/history/playtests/v*/playtest-findings-v*.md` artifacts.

To extend the same three free-form Hard competitive profiles across seeds `42`,
`43`, and `44`:

```bash
python3 _workspace/experiments/v0.10.1-free-form-hard-seed-variation/run_sessions.py
```

The seed-variation script writes
`_workspace/experiments/v0.10.1-free-form-hard-seed-variation/results.json`.
Use it to test completion and profile endpoint stability across seeds, not to
justify balance or runtime changes.

To compare the v0.10.1 free-form Hard policies against bounded access-pledge
cooldown and reported-access-threshold variants:

```bash
python3 _workspace/experiments/v0.10.2-access-loop-diagnostic/run_sessions.py
```

The access-loop diagnostic script writes
`_workspace/experiments/v0.10.2-access-loop-diagnostic/results.json`. Use it to
test whether repetitive access commitments are reducible through operator-policy
or guidance changes. Do not treat it as evidence for runtime balance changes or
automatic command cooldowns.

To validate whether the v0.10.3 access-commitment guidance can reduce repeated
access pledges in a bounded operator policy:

```bash
python3 _workspace/experiments/v0.10.4-post-guidance-validation/run_sessions.py
```

The post-guidance validation script writes
`_workspace/experiments/v0.10.4-post-guidance-validation/results.json`. Use it to
compare unchanged baseline free-form Hard policies against a guidance-aware
variant that redirects repeated or high-access pledges to existing legal
fallback actions. Do not treat it as evidence for runtime balance changes,
automatic command cooldowns, or pledge-effect tuning.

The cross-artifact synthesis in `docs/history/playtests/v0.10/playtest-findings-v0.10.5.md` summarizes
the `v0.10.0` through `v0.10.4` free-form Hard evidence without adding new runs.
Use it as the current routing note for access-pledge follow-up: repeated
baseline matrices are controls, not independent player evidence, and runtime
cooldowns or pledge-effect tuning still require a separate evidence gate.

The v0.10.7 sub-agent access-pledge slice replays three generated Hard
competitive command plans through MCP:

```bash
python3 _workspace/experiments/v0.10.7-llm-access-pledge-evidence/run_sessions.py
```

Use `docs/history/playtests/v0.10/playtest-findings-v0.10.7.md` as bounded simulated-agent evidence
only. It does not justify runtime access cooldowns, pledge-effect tuning, or a
general LLM runner.

To capture observation-by-observation Hard competitive evidence through the
existing MCP wrapper:

```bash
python3 _workspace/experiments/v0.10.9-live-mcp-capture/run_sessions.py
```

The script writes
`_workspace/experiments/v0.10.9-live-mcp-capture/results.json` with actor-visible
observations, legal command hints, submitted commands, validation outcomes,
transition hashes, final observations, and final debriefs. Use
`docs/history/playtests/v0.10/playtest-findings-v0.10.9.md` as workflow evidence for live capture, not as
human-learning, calibration, balance, or runtime-tuning evidence.

To generate a compact diagnostic report from that live-capture artifact:

```bash
python3 scripts/diagnose_runs.py _workspace/experiments/v0.10.9-live-mcp-capture/results.json --output _workspace/experiments/v0.10.10-live-capture-diagnostics/diagnostics.md
```

The report summarizes profile outcomes, action frequencies, validation failures,
access pledges, and final hashes. Use it as simulated-agent strategy-space
diagnostics only; it is not evidence for runtime tuning or balance changes.

To extend live capture across the current deterministic persona policies,
seeds `42`, `43`, and `44`, and Normal/Hard competitive difficulty tiers:

```bash
python3 _workspace/experiments/v0.10.11-live-capture-matrix/run_sessions.py
python3 scripts/diagnose_runs.py _workspace/experiments/v0.10.11-live-capture-matrix/results.json --output _workspace/experiments/v0.10.11-live-capture-matrix/diagnostics.md
```

Use `docs/history/playtests/v0.10/playtest-findings-v0.10.11.md` as workflow evidence that the live MCP
capture path supports small seed/difficulty matrices. Do not treat the repeated
deterministic policies as independent player samples or evidence for runtime
tuning.

To run a live-capture matrix using the existing automated pressure policies and
the Hard difficulty-adaptive wrapper:

```bash
python3 _workspace/experiments/v0.10.12-live-difficulty-pressure/run_sessions.py
python3 scripts/diagnose_runs.py _workspace/experiments/v0.10.12-live-difficulty-pressure/results.json --output _workspace/experiments/v0.10.12-live-difficulty-pressure/diagnostics.md
```

Use `docs/history/playtests/v0.10/playtest-findings-v0.10.12.md` as simulated-agent pressure evidence
for Normal/Hard comparison. Do not treat it as balance proof, empirical
calibration, human-learning evidence, or justification for runtime tuning by
itself.

To compare static and adaptive policies side by side in one live-capture
artifact:

```bash
python3 _workspace/experiments/v0.10.13-live-static-adaptive-capture/run_sessions.py
python3 scripts/diagnose_runs.py _workspace/experiments/v0.10.13-live-static-adaptive-capture/results.json --output _workspace/experiments/v0.10.13-live-static-adaptive-capture/diagnostics.md
```

Use `docs/history/playtests/v0.10/playtest-findings-v0.10.13.md` as simulated-agent evidence for the
policy-wrapper comparison. Do not treat it as balance proof, empirical
calibration, human-learning evidence, or justification for runtime tuning by
itself.

To run independent observation-conditioned reviewer policies through the same
live-capture path:

```bash
python3 _workspace/experiments/v0.10.14-independent-reviewer-agent-capture/run_sessions.py
python3 scripts/diagnose_runs.py _workspace/experiments/v0.10.14-independent-reviewer-agent-capture/results.json --output _workspace/experiments/v0.10.14-independent-reviewer-agent-capture/diagnostics.md
```

Use `docs/history/playtests/v0.10/playtest-findings-v0.10.14.md` as simulated-agent reviewer evidence.
Do not treat it as balance proof, empirical calibration, human-learning
evidence, or justification for runtime tuning by itself.

To replay the accepted live month-by-month LLM/sub-agent difficulty-gate command
streams:

```bash
python3 _workspace/experiments/v0.10.15-live-llm-difficulty-gate/run_sessions.py
python3 scripts/diagnose_runs.py _workspace/experiments/v0.10.15-live-llm-difficulty-gate/results.json --output _workspace/experiments/v0.10.15-live-llm-difficulty-gate/diagnostics.md
```

Use `docs/history/playtests/v0.10/playtest-findings-v0.10.15.md` as simulated-agent live-decision
evidence. It can inform follow-up guidance, debrief, and validation questions;
do not treat it as balance proof, empirical calibration, human-learning
evidence, or justification for runtime tuning by itself.

As of `v0.10.17`, live-capture diagnostics also report optional
`live_validation_retries` metadata when an artifact includes it. Use the
`Live Retry Signals` table to distinguish final replay validation failures from
cash-overrun or other rejected live decision attempts before the accepted
command stream.

As of `v0.10.18`, competitive MCP validation errors may include additive
structured fields alongside the existing `error` string. Resource-limit failures
such as cash overrun, AP overrun, and political-capital overrun include a stable
`code`, a `resource_limit` object, and a short `hint`. Use these fields in live
capture wrappers to classify retry causes without parsing human-readable error
text. Do not treat the presence of structured retry metadata as balance,
calibration, or runtime-tuning evidence by itself.

As of `v0.10.19`, the shared Python MCP wrapper preserves those additive fields
inside captured `validation_failures` and `live_validation_retries` records
while keeping the plain `error` string for compatibility. Diagnostics prefer
structured cash-retry metadata when present and fall back to legacy string-only
artifacts when older evidence files do not include `code` or `resource_limit`.

As of `v0.10.20`, the current retry-visibility gate is closed for live-capture
classification: the MCP server emits structured resource-limit fields, the
Python wrapper preserves them, and diagnostics prefer them while retaining
legacy fallback. Treat this as tooling confidence only. Runtime tuning, command
cost changes, pledge cooldowns, or difficulty changes still require a separate
evidence slice naming a concrete mechanic problem beyond retry classification.

As of `v0.10.21`, the live-capture evidence synthesis routes the next bounded
question toward access-heavy player understanding: can debrief and guidance
clearly distinguish public access pledges from durable operational follow-through
under cash pressure? Use existing live-capture artifacts and diagnostics first.
Do not expand retry metadata again or tune runtime mechanics unless a later
evidence slice identifies a concrete mechanic problem.

As of `v0.10.22`, the access-heavy comprehension review uses the existing
`v0.10.15` live-capture artifact and diagnostic report to compare the Live
Access Operator's Normal and Hard runs. Treat the next bounded follow-up as
explanatory competitive debrief wording for access-heavy runs, not runtime
tuning, command-cost changes, access-pledge cooldowns, or difficulty changes.

As of `v0.10.24`, `_workspace/experiments/v0.10.24-access-debrief-validation/`
contains bounded MCP trigger/control evidence for the access follow-through
debrief note. Use it as debrief-surface validation only, not as human-learning
or balance evidence.

As of `v0.10.25`, `docs/history/playtests/v0.10/playtest-findings-v0.10.25.md` synthesizes the
`v0.10.21` through `v0.10.24` access-heavy evidence chain. Treat that synthesis
as a routing checkpoint: access follow-through is now covered as debrief
explanation, and future runtime changes still require a separate artifact that
identifies a concrete mechanics problem.

As of `v0.10.26`, `docs/history/playtests/v0.10/playtest-findings-v0.10.26.md` compares recent
competitive evidence for teachability, debrief coherence, and repeated-play
interest. Treat that synthesis as a broader Phase 7 routing checkpoint:
follow-up work should prefer instructor-facing comparison prompts or broader
strategy-space synthesis before reopening runtime tuning.

As of `v0.10.27`, `docs/history/playtests/v0.10/playtest-findings-v0.10.27.md` turns the competitive
teachability synthesis into instructor-facing comparison prompts. Use it for
discussion of decision quality versus outcome quality across existing evidence,
not as human-learning validation, empirical calibration, or runtime tuning
evidence.

As of `v0.10.29`, `docs/history/playtests/v0.10/playtest-findings-v0.10.29.md` adds a compact
debrief comparison surface for repeated competitive runs. Use it to structure
instructor or reviewer discussion across strategy postures and final debriefs.
Do not treat it as a score, hidden strategy taxonomy, classroom-effectiveness
measure, balance proof, or justification for runtime changes.

As of `v0.10.30`, `docs/history/playtests/v0.10/playtest-findings-v0.10.30.md` reviews
workforce-protective play as an interpretive comparison axis across staffing,
trust, pacing, monitoring, and commitment discipline. Use it for discussion and
future evidence routing, not as a standalone strategy class, validated learner
archetype, balance proof, or reason to tune workforce mechanics.

As of `v0.10.33`, `docs/history/playtests/v0.10/playtest-findings-v0.10.33.md` reviews
growth/capacity-oriented play as an interpretive comparison axis across
projects, investments, staffed capacity, cash runway, access, and rival
pressure. Use it for discussion and future evidence routing, not as a
standalone strategy class, validated learner archetype, balance proof, or
reason to tune project costs, capacity effects, staffing allocation, or
difficulty.

As of `v0.10.34`, `docs/history/playtests/v0.10/playtest-findings-v0.10.34.md` provides an instructor
debrief facilitation sequence across decision context, outcome context,
follow-through, workforce posture, growth posture, rival response, and debrief
clarity. Use it to guide repeated-run discussion, not to claim measured
learning or promote runtime tuning.

As of `v0.10.44`, `docs/history/playtests/v0.10/playtest-findings-v0.10.44.md` connects the generic
consultant-advice and rival-monitor evidence chains into one information-to-
action comparison surface. Use it to compare visible information, subsequent
commands, operational follow-through, realized tradeoffs, and debrief
traceability across runs. Treat response records as inspectability evidence,
not as proof of advice quality, monitor value, human learning, causal impact,
balance, or calibration. Keep runtime and advisor-market work deferred unless
a later artifact identifies a concrete gap that current observations, history,
diagnostics, and debriefs cannot explain.

As of `v0.10.45`, the instructor debrief-use audit checks the existing
v0.10.37, v0.10.40, v0.10.41, and v0.10.43 artifacts for coverage of the five
information-to-action review steps. It is a read-only trace-field audit across
70 complete runs, not human or classroom evidence. A supported field indicates
inspectability only; it does not establish clarity, learning, advice quality,
monitor value, causal impact, balance, or calibration.

```bash
python3 _workspace/experiments/v0.10.45-instructor-debrief-use-audit/run_audit.py
python3 -m json.tool _workspace/experiments/v0.10.45-instructor-debrief-use-audit/results.json
```

As of `v0.10.46`, the Expert clearability evidence matrix runs the existing
Fiscal Caution, Capacity Growth, Balanced Strategy, and Naive First-Time
profiles across seeds `42`, `43`, and `44` at Expert difficulty. It records
actor-visible traces, commands, validation failures, histories, hashes, and
debriefs for a bounded completion check. Full 24-month completion is a
clearability proxy for these policies and seeds, not general Expert winnability,
balance, human-learning, causal, or policy-validity evidence.

```bash
python3 _workspace/experiments/v0.10.46-expert-clearability-evidence/run_sessions.py
python3 -m json.tool _workspace/experiments/v0.10.46-expert-clearability-evidence/results.json
```

As of `v0.11.9`, the post-difficulty-expansion Expert validation matrix runs
Access First, Commercial Focus, Workforce Resilience, Capital Modernization, and
Coalition/Legitimacy policies across seeds `42`, `43`, and `44` at Expert
difficulty. It verifies bounded clearability after the v0.11.7 risk-posture and
v0.11.8 rival resource-scaling changes. Treat it as simulated-policy evidence,
not general Expert winnability, balance, human-learning, causal, calibration, or
policy-validity evidence.

```bash
python3 _workspace/experiments/v0.11.9-expert-difficulty-validation/run_sessions.py
python3 -m json.tool _workspace/experiments/v0.11.9-expert-difficulty-validation/results.json
```

As of `v0.11.11`, the post-change all-tier validation matrix reruns the five
existing policy profiles across seeds `42`, `43`, and `44` at Easy, Normal,
Hard, and Expert difficulty on current code. It records 60 complete 24-month
runs, operating accounting, strategy trajectories, endpoint tradeoffs,
bottlenecks, threshold candidates, actor-visible traces, hashes, and debriefs.
This is bounded simulated-policy evidence, not general winnability, balance,
causal strategy, human-learning, calibration, or policy-validity evidence.

```bash
python3 _workspace/experiments/v0.11.11-phase7-post-change-all-tier-validation/run_sessions.py
python3 _workspace/experiments/v0.11.11-phase7-post-change-all-tier-validation/run_audit.py
python3 -m json.tool _workspace/experiments/v0.11.11-phase7-post-change-all-tier-validation/results.json
```

As of `v0.11.12`, the current-code teachability capture reruns three existing
observation-driven profiles across seeds `42`, `43`, and `44` at Hard
difficulty. It records actor-visible observations, legal commands, submitted
commands, retries, histories, hashes, and debriefs, then reports action cadence
and traceability as descriptive proxies. It does not change runtime behavior
or establish human comprehension, learning, balance, or winnability.

```bash
python3 _workspace/experiments/v0.11.12-phase7-current-code-teachability-capture/run_sessions.py
python3 _workspace/experiments/v0.11.12-phase7-current-code-teachability-capture/run_audit.py
python3 -m unittest tests/test_phase7_current_code_teachability_capture.py
```

As of `v0.10.47`, the command-to-effect explainability audit checks the same
12 Expert traces for action-specific transition evidence and monthly `Player:`
debrief records. It is a read-only traceability check: the complete result does
not establish that commands caused endpoint metrics or that the debrief is
clear to human learners.

```bash
python3 _workspace/experiments/v0.10.47-command-effect-explainability/run_audit.py
python3 -m json.tool _workspace/experiments/v0.10.47-command-effect-explainability/results.json
```

As of `v0.10.48`, the strategy-diversity audit summarizes command-family
trajectories and descriptive final tradeoffs across the same 12 Expert traces.
It is read-only evidence: distinct trajectories do not establish causal value,
dominance, optimality, balance, or human learning.

```bash
python3 _workspace/experiments/v0.10.48-strategy-diversity-evidence/run_audit.py
python3 -m json.tool _workspace/experiments/v0.10.48-strategy-diversity-evidence/results.json
```

As of `v0.10.49`, the teachability-gate synthesis checks continuity across the
v0.10.45–v0.10.48 evidence chain. It confirms source coverage and the shared
Expert profile/seed matrix without creating a generalized evidence schema or
promoting runtime work.

```bash
python3 _workspace/experiments/v0.10.49-teachability-gate-synthesis/run_audit.py
python3 -m json.tool _workspace/experiments/v0.10.49-teachability-gate-synthesis/results.json
```

As of `v0.10.50`, the observation-driven capture runs Fiscal Steward, Access
Expansion Advocate, and First-Time Executive policies across Hard seeds 42, 43,
and 44. Policies read only actor-visible observations, legal command hints, and
turn number. The wrapper preserves rejected commands, safe retries, transition
hashes, histories, and debriefs. Treat the nine runs as deterministic
simulated-policy evidence, not human-learning, balance, winnability, or policy
validity evidence.

```bash
python3 _workspace/experiments/v0.10.50-teachability-observation-capture/run_sessions.py
python3 scripts/diagnose_runs.py \
  _workspace/experiments/v0.10.50-teachability-observation-capture/results.json \
  --output _workspace/experiments/v0.10.50-teachability-observation-capture/diagnostics.md
python3 -m json.tool _workspace/experiments/v0.10.50-teachability-observation-capture/results.json
```

As of `v0.10.51`, the adversarial resource-probe capture submits fixed
observation-driven probes for cash, monthly action points, and concurrent
projects at Hard difficulty across seeds 42, 43, and 44. Expected validation
failures are separated from unexpected failures; each rejected probe is
followed by a safe `hold` retry, and the wrapper confirms that the rejected
submission did not advance the session. Treat this as deterministic resource
guard and traceability evidence, not exploit, balance, winnability, human
learning, or policy-validity evidence.

```bash
python3 _workspace/experiments/v0.10.51-adversarial-resource-probe/run_sessions.py
python3 -m json.tool _workspace/experiments/v0.10.51-adversarial-resource-probe/results.json
```

As of `v0.10.52`, the decision-load audit reads the existing v0.10.50
observation-driven traces and reports action concentration, active months,
holds, multi-action months, and maximum actions per month. Treat these as
descriptive pacing and action-overload proxies, not cognitive-load, human
comprehension, strategy-quality, balance, or runtime-tuning evidence.

```bash
python3 _workspace/experiments/v0.10.52-decision-load-evidence/run_audit.py
python3 -m json.tool _workspace/experiments/v0.10.52-decision-load-evidence/results.json
```

As of `v0.10.53`, the Phase 7 evidence synthesis checks source identity and
declared coverage across the v0.10.50 observation capture, v0.10.51 resource
probe, and v0.10.52 pacing audit. It verifies the v0.10.51 First-Time Executive
control hashes and the shared nine-member profile/seed matrix without creating a
generalized evidence schema or launching new sessions. Treat continuity as
descriptive evidence only; runtime promotion remains deferred.

```bash
python3 _workspace/experiments/v0.10.53-evidence-synthesis/run_audit.py
python3 -m json.tool _workspace/experiments/v0.10.53-evidence-synthesis/results.json
```
