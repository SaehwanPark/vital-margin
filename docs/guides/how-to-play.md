# How To Play

This guide covers both the recommended live GUI tutorial and the CLI
alternative. Install from [Installation and first launch](installation.md),
then use the [GUI guide](gui-how-to-play.md) for settings, checkpoints,
alternate ports, and recovery.

## What this game is

You lead a fictional nonprofit US health system. Decisions balance finance,
workforce, policy, community trust, and rivals. The host reports only
actor-visible information; seeded uncertainty and the same choices produce the
same run.

The three campaigns are alternatives rather than sequential chapters. Progress
and checkpoints do not transfer between them:

| Campaign | What you do | Interface and audience |
| --- | --- | --- |
| **Stabilization tutorial** (`stabilization-v1`) | Five abstract executive decisions; no calendar duration or difficulty. | Recommended first GUI run; CLI also has beginner guided choices (`b`). |
| **Competitive regional market** (`competitive-regional-v1`) | A separate 24-month campaign with simultaneous AI-rival actions, monthly AP planning, and lagged public information. | Difficulty tiers apply; this is local AI pressure, not network multiplayer. |
| **Regional affiliation** (`regional-affiliation-v1`) | A separate six-stage nonprofit-partner scenario covering assessment, posture, commitments, review, and early integration or independence. | No AI rivals or difficulty; it is not legal, valuation, antitrust, or transaction advice. |

## Recommended GUI first run: stabilization tutorial

1. From the repository root, start the live GUI host:

   ```bash
   cargo run --bin vital-margin-gui
   ```

2. Keep that terminal running and open the printed URL, normally
   `http://127.0.0.1:7878`.
3. Select **Stabilization tutorial** (`stabilization-v1`) and seed `42`.
   Difficulty is not used by this campaign.
4. Choose **Start selected session**. Read the visible brief, choose one
   host-provided action, review the committed stage, and continue until the
   terminal Review debrief after five decisions.

Do not open `gui/index.html` directly when you want to play: direct/static mode
contains demonstration data and no live game host.

## CLI alternative

1. Run the reference CLI:

   ```bash
   cargo run
   ```

2. Choose Enter or `1` for `stabilization-v1`, then `b` for beginner guided
   choices and seed `42` (press Enter at each default prompt).
3. To explore other campaigns, choose `2`/`c` for competitive or `3`/`a` for
   regional affiliation. Competitive difficulty is Easy (1 rival, 4 AP/month),
   Normal (2, 3 AP), Hard (3, 3 AP), or Expert (4, 2 AP).
4. Use `?`/`help` for context and `q`, `quit`, or `exit` to leave.

## Game structure from your perspective

## Stabilization (`stabilization-v1`)

For each of 5 turns, you:

1. Read your observation and briefing.
2. (Interactive mode) review uncertainty preview.
3. Enter turn-specific numeric command fields.
4. Submit and watch NPC response plus turn summary.
5. Continue to next turn.

At run end, you get replay verification and a debrief.

## Competitive campaign (`competitive-regional-v1`)
 
 For each month in the 24-month campaign, you:
 
 1. Read the executive report.
 2. Enter one command batch (Stata-like verbs).
 3. Submit; AI rivals submit simultaneously.
 4. Review resolution summary.
 5. Repeat next month with updated conditions.
 
 Note: the 24-month campaign features full autosave/resume, scenario loading, and replay export.

## Regional affiliation (`regional-affiliation-v1`)

Across six stages, you assess a fictional nonprofit partner, choose an
independence/defer/pursue posture, set community/workforce/continuity
commitments when applicable, submit or await review, and choose an integration
approach. The campaign keeps partner observations, assumptions, commitments,
resolved review inputs, history, replay verification, and debrief output
explicit.

This is a bounded educational scenario, not legal, antitrust, valuation, or
transaction advice.

## Key terminology

- `True state`: full modeled world state inside the engine.
- `Observation`: what you (or another actor) are allowed to see.
- `Resolved inputs`: seeded uncertainty values computed before transition.
- `AP (action points)`: your monthly command-capacity budget (competitive).
- `Political capital`: resource used by selected strategic commands.
- `Simultaneous resolution`: all player monthly batches are resolved together.
- `Replay`: deterministic re-check from genesis over committed history.
- `Debrief`: end-of-run explanation of why outcomes happened.
- `Decision quality`: whether your choice was reasonable with available info.
- `Outcome quality`: what happened after all responses and uncertainty.

For the full contributor/domain glossary, see `docs/reference/glossary.md`.

## Commands

## Stabilization input style

Stabilization interactive prompts ask for integer fields per turn (for example,
capital spend, access commitment, schedule relief). The prompt always shows:

- exact field names,
- valid ranges,
- and a default command line you can accept.

Use Enter to accept defaults where the prompt allows.

## Competitive command cheat sheet

Use `verb arg=value` syntax. You can chain commands with semicolons.

Examples:

```text
invest domain=beds amount=25
recruit role=nurse headcount=5
monitor target=northlake depth=2
negotiate payer=carrier_a rate_posture=neutral
commit pledge_type=access level=3
project kind=ehr_epic budget=60
hold
```

Batch example:

```text
monitor target=summit depth=1; invest domain=outpatient amount=15
```

Global/meta helpers in competitive prompt:

- `help` or `?`: list command usage.
- `Enter` on empty input: submit fallback batch.
- `q`/`quit`/`exit`: quit the session.

## Gameplay walkthrough (example interaction)

Scenario: you are in competitive Month 2 on Normal difficulty.

Executive report highlights:

- Rival Northlake announced bed expansion last month.
- Your cash runway shows `watch`.
- Nursing vacancy remains elevated.
- Consultant options suggest either fast bed investment or workforce-first.

Your decision:

```text
monitor target=northlake depth=1; recruit role=nurse headcount=4
```

Why this can be strong:

- `monitor` improves next-month intel before a larger capital move.
- `recruit` addresses workforce pressure without immediate large cash burn.
- You keep AP and cash flexibility if rivals escalate unexpectedly.

Possible next-month follow-up:

```text
invest domain=beds amount=20
```

if intel confirms market-share risk and your runway improves.

Lesson: you are not trying to "solve" one month. You are managing tempo under
uncertainty while preserving options.

## If the game feels too difficult

Use this triage playbook.

1. Protect capacity to respond:
   - avoid spending all AP on one theme every month;
   - keep at least one flexible action open when possible.
2. Respect cash runway signals:
   - if runway is `watch` or `strained`, prioritize lower-burn actions;
   - delay large `project` or high `invest` commitments unless essential.
3. Buy information before big commitments:
   - use `monitor` when rival intent is unclear.
4. Use `hold` strategically:
   - a deliberate pass can be correct when information is weak and downside is high.
5. Prefer reversible actions early:
   - small recruit/invest steps often outperform one large irreversible bet.
6. Focus on decision quality, not perfection:
   - strong process beats chasing one "best" move that may not exist.

## Practical beginner patterns

- Conservative month: `monitor` + light `recruit`.
- Balanced month: medium `invest` + one legitimacy move (`commit`).
- Information-first month: `monitor`, then adjust next month with better intel.

## Strategy notes from playtesting

- Commercial rate asks work best when you have visible leverage. Reported access,
  capacity, quality, and market context matter; a high rate posture by itself can
  create relationship risk without improving your outside option.
- Public access pledges can reduce scrutiny and build legitimacy, especially
  when access pressure is visible. Repeating access pledges is not the same as
  adding durable capacity, staffing, monitoring rivals, or improving payer
  posture; use commitments with operational follow-through.
- Recruitment is not instant capacity. Hiring spends cash immediately, resolves
  after role-specific delays, and can strain workforce trust while the added
  capacity is still pending.

## FAQ and troubleshooting

Q: I entered a command and got an error. Did I lose the month?  
A: No. Validation errors do not advance the month; fix command syntax/limits and
retry.

Q: Why did a "good" decision still lead to a bad result?  
A: Rival actions, delayed effects, and seeded uncertainty can produce adverse
outcomes. Debrief helps separate decision quality from outcome quality.

Q: Is competitive a full campaign already?  
A: Yes. The competitive campaign loop runs for 24 months, with AI rivals, monthly events, and scenario loading.

Q: I want a less overwhelming first run.  
A: Start with `stabilization-v1` and beginner mode (`b`), then move to
competitive once the loop feels familiar.

## Learn more

- Core loop: `docs/design/core-loop-spec.md`
- Competitive gameplay spec: `docs/design/gameplay-competitive-sketch.md`
- Command grammar draft: `docs/design/cli-command-grammar-draft.md`
- Action catalog: `docs/design/action-catalog-draft.md`
- Executive report schema: `docs/design/executive-report-format.md`
- Glossary: `docs/reference/glossary.md`
