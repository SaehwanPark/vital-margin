# Vital Margin
## Initial Game Development Proposal

**Status:** Canonical project proposal  
**Audience:** Project owner and contributors  
**Initial platform:** Command-line interface with a local loopback GUI
**Initial domain:** United States health policy and health-system strategy  
**Primary implementation language:** Rust

## Current Implementation Checkpoint

As of 2026-08-02 (v0.14.12), the proposal has progressed beyond its initial concept and
vertical-slice stages into a playable, evidence-gated prototype. The repository
contains three deterministic campaign paths:

- a five-turn stabilization campaign;
- a 24-month competitive regional-market campaign; and
- an opt-in six-stage regional-affiliation campaign.

The implementation includes a CLI reference interface, a local stdio MCP adapter
for bounded agent playtesting, replay and state-hash verification, scenario
loading, durable checkpoint discovery/restoration, educational debriefs, and a
loopback Axum GUI host over the shared action surface. The GUI presents all three
campaigns through the Setup/Brief/Decide/Resolve/Review workspace while leaving
the Rust session store and action ordering authoritative. The shared task rail
uses the host terminal signal to label final history/debrief review, and visible
consequence links retain host timing/hash context and show signed committed-effect
deltas and visible institutional responses with registered status-token
emphasis. Current numerical
mechanisms remain documented game abstractions rather than calibrated forecasts,
and AI-agent playtests remain gameplay and explanation evidence rather than
evidence of human learning.

The original proposal below remains the durable product thesis. Current scope,
completed slices, and promotion gates are tracked in [`SPEC.md`](../SPEC.md),
[`docs/roadmap.md`](roadmap.md), and [`ARCHITECTURE.md`](../ARCHITECTURE.md).

---

## 1. Project Summary

This project is a turn-based strategy and simulation game in which the player leads a health system as a newly appointed chief executive. The player must navigate financial pressure, clinical obligations, workforce constraints, market competition, government policy, and stakeholder politics through a CLI/reference or loopback GUI workspace.

The first version will focus on the United States. Its deeper purpose, however, is broader: to model health policy as an evolving system produced by strategic interaction among institutions operating under economic, political, legal, and social constraints.

The game is intended to be:

- an engaging strategy experience;
- an educational resource for graduate healthcare management and policy programs;
- a transparent computational model of institutional behavior;
- and, eventually, a reusable platform for comparative health-policy scenarios.

The initial target setting is a fictional regional US health market centered on a nonprofit health system. The player will make executive decisions while non-player actors—including insurers, government agencies, competitors, labor groups, employers, clinicians, and political coalitions—respond strategically.

---

## 2. Background and Motivation

Health systems are not conventional firms. Their leaders operate in markets shaped by third-party payment, administered prices, professional norms, public obligations, regulation, asymmetric information, fragmented authority, and competing definitions of value.

Many educational approaches divide this environment into separate topics:

- healthcare finance;
- operations;
- public policy;
- market strategy;
- organizational behavior;
- health economics;
- political institutions;
- and population health.

In practice, these domains are inseparable. A financially rational action may reduce access. A quality initiative may worsen short-term capacity. A reimbursement reform may trigger consolidation, service closure, labor pressure, or political opposition. A technically sound policy may fail during adoption or implementation. Individually rational actors may collectively produce poor social outcomes.

A simulation game can make these interactions visible in ways that lectures, static cases, and spreadsheets often cannot. It can require players to act with incomplete information, manage delayed consequences, negotiate with other institutions, and distinguish a sound decision from a fortunate outcome.

The project is inspired by business and policy simulations such as *Capitalism*, *SimHealth*, *HealthBound*, *Democracy*, economic strategy games, negotiation exercises, and agent-based social simulations. Existing work demonstrates demand for this kind of experience, but also reveals recurring limitations:

- policies are often treated as direct levers rather than politically produced and strategically mediated interventions;
- non-player actors are commonly scripted, reactive, or opaque;
- model assumptions and normative scoring are difficult to inspect;
- stochastic behavior is often entangled with core state transitions;
- and educational explanations are weaker than the underlying simulation requires.

This project aims to address those limitations through explicit domain modeling, deterministic transition logic, actor-specific information, transparent assumptions, and strategic non-player decision-making.

---

## 3. Project Thesis

The core thesis is:

> Health-policy outcomes are not produced by policy alone. They emerge from strategic responses by institutions operating within markets, political systems, professional cultures, and social structures.

The game should therefore model not only policies and operational decisions, but also:

- who has authority to act;
- what each actor wants;
- what each actor knows or believes;
- which actions are feasible;
- how actors bargain, compete, coordinate, or form coalitions;
- how implementation changes intended policy;
- and how outcomes feed back into markets, organizations, public opinion, and future policy.

---

## 4. Product Vision

The desired experience is a serious, replayable strategy simulation rather than a detailed administrative spreadsheet.

The player should feel responsible for a complex institution but never fully in control of the environment. The game should create meaningful tradeoffs among:

- financial sustainability;
- quality and patient safety;
- access and equity;
- workforce stability;
- organizational growth;
- regulatory standing;
- political legitimacy;
- community trust;
- and mission.

There should be no universal optimal strategy. Different scenarios may support different defensible goals, including turnaround, growth, safety-net preservation, value-based transformation, rural access, or academic mission.

The educational value should come from the interaction of systems, not from presenting textbook concepts as trivia. Economic and political mechanisms should become visible through play and be made explicit during analysis and debriefing.

---

## 5. Initial Scope

The first version will model one fictional US state and one regional healthcare market.

The player will lead a medium-sized nonprofit health system with multiple hospitals and ambulatory operations. The surrounding environment may include:

- Medicare;
- a state Medicaid program;
- several commercial insurers;
- competing health systems;
- independent physician groups;
- major employers;
- healthcare labor organizations;
- state and federal regulators;
- elected officials;
- advocacy and industry groups;
- and heterogeneous patient populations.

Initial policy and strategic domains should remain limited to a manageable set, likely including:

1. insurance coverage and payer mix;
2. provider payment and market power;
3. workforce regulation and labor relations;
4. access, quality, and safety-net obligations;
5. capital allocation and service-line strategy;
6. selected state and federal policy changes.

The first playable campaign should be short enough for classroom use and structured enough to support comparison across teams.

---

## 6. Intellectual Foundations

The simulation will draw from several disciplines.

### Microeconomics

Relevant mechanisms include:

- market power;
- price and quantity responses;
- adverse selection;
- moral hazard;
- principal-agent problems;
- information asymmetry;
- externalities;
- public goods;
- cross-subsidization;
- risk adjustment;
- transaction costs;
- and labor-market constraints.

### Game Theory

Non-player behavior should arise from explicit strategic interactions where practical, including:

- bargaining;
- repeated games;
- sequential games;
- coordination problems;
- coalition formation;
- credible commitments;
- signaling;
- entry and capacity competition;
- and Bayesian games with private information.

The project will not require exact equilibrium computation in every interaction. Bounded rationality, approximate best response, satisficing, level-k reasoning, and structured heuristics may be more realistic and tractable.

### Political Science and Public Administration

Policy should be modeled as a lifecycle involving:

- agenda formation;
- coalition building;
- legislative or administrative action;
- rulemaking;
- implementation;
- enforcement;
- judicial review;
- strategic adaptation;
- and political feedback.

Federalism, institutional authority, bureaucratic capacity, elections, lobbying, and path dependence should matter.

### Social and Behavioral Science

Actors should not be treated as perfectly rational abstractions. Relevant considerations include:

- trust;
- professional identity;
- organizational culture;
- status quo bias;
- loss aversion;
- social norms;
- institutional legitimacy;
- bounded attention;
- diffusion of innovation;
- and social inequality.

### Macroeconomics

Macroeconomic conditions should shape the environment through specific channels such as employment, insurance coverage, state revenue, labor costs, inflation, interest rates, and capital availability.

---

## 7. Core Design Principles

### 7.1 Deterministic Core Engine

The simulation engine should be a deterministic state-transition system.

Given:

- an immutable prior state;
- explicit player and non-player actions;
- explicit external inputs;
- and a versioned ruleset;

the next state and resulting events must be reproducible.

Conceptually:

```text
(previous state, actions, resolved inputs, ruleset)
  -> next state, events, attributed effects
```

No hidden random-number generation, wall-clock dependency, filesystem state, or global mutable state should influence core transitions.

### 7.2 Stochastic Inputs and Observations

Stochasticity may enter through:

- exogenous events;
- behavioral realizations;
- measurement noise;
- missingness;
- reporting delays;
- uncertain estimates;
- and actor decision procedures that use externally resolved stochastic inputs.

Randomness should be seeded, explicit, and separated by subsystem or stable identifiers so that unrelated model changes do not unnecessarily alter all future outcomes.

### 7.3 True State Versus Observed State

The simulation must distinguish between:

- the true state of the modeled world;
- the information available to each actor;
- and public or reported measurements.

Different actors may observe different, delayed, biased, or incomplete representations of the same underlying state.

This distinction is central to the educational design. Players should be judged partly on whether decisions were reasonable given the information available at the time, rather than only on realized outcomes.

### 7.4 Immutable Snapshots and Append-Only History

Snapshots should be static representations of state at a defined point in time.

Corrections or revised estimates should appear in later observations rather than rewriting what an actor previously knew. Simulation history should be append-only and support replay, auditing, counterfactual analysis, and causal explanation.

### 7.5 Strategic Non-Player Actors

Non-player actors should not rely solely on fixed scripts or random actions.

Each actor should have explicit:

- objectives;
- constraints;
- authority;
- resources;
- information;
- beliefs;
- outside options;
- risk tolerance;
- time horizon;
- relationships;
- and decision procedure.

Strategic interactions should be represented as localized game instances, such as payer-provider bargaining, labor negotiation, coalition formation, market entry, shared investment, or policy opposition.

Actors should not be permanently labeled cooperative or competitive. Cooperation should be issue-specific and emerge when coalition value exceeds coordination costs, defection risk, and available alternatives.

### 7.6 Separation of Actor Utility and Social Welfare

Each actor should optimize its own objectives. Those objectives must remain distinct from the educational or social-welfare evaluation of the overall system.

This allows the game to represent:

- coordination failures;
- cost shifting;
- underinvestment in public goods;
- excessive consolidation;
- political capture;
- and individually rational but socially harmful outcomes.

### 7.7 Transparent Mechanisms and Assumptions

The game should make it possible to inspect:

- model assumptions;
- actor objectives;
- information available at decision time;
- strategic procedures used;
- activated causal mechanisms;
- outcome attribution;
- and sensitivity to alternative assumptions.

False precision and ideological opacity are major risks in health-policy simulation. The project should treat transparency as a core feature, not post hoc documentation.

### 7.8 Data-Driven Scenarios, Typed Mechanics

The engine should implement a limited set of well-defined mechanisms. Scenarios, policies, actor configurations, and empirical parameters should be externalized where practical.

Configuration should compose known mechanisms rather than evolve into an unrestricted programming language.

---

## 8. Technical Direction

Rust is the preferred implementation language.

The rationale is not primarily performance. Rust is attractive because the project will benefit from:

- algebraic data types;
- exhaustive pattern matching;
- typed state transitions;
- explicit error handling;
- strong domain invariants;
- deterministic behavior;
- serialization support;
- and reliable testing.

The domain should distinguish legitimate unfavorable outcomes from invalid operations. For example, a failed negotiation is a modeled outcome, while an action taken without legal authority is a validation failure.

A likely high-level architecture is:

```text
domain model
  -> simulation engine
  -> scenario and policy configuration
  -> analysis and attribution
  -> CLI presentation
```

The central transition function should be close to a pure function. Input/output, persistence, scenario loading, random input generation, and terminal rendering should remain outside the core engine.

The project should use explicit commands, events, and effects:

```text
command
  -> validation
  -> strategic resolution
  -> domain events
  -> attributed effects
  -> next state
```

This structure supports replay, classroom analysis, save files, deterministic testing, and explanation of outcomes.

The command-line interface is an intentional first platform. It minimizes presentation overhead, supports structured reports and reproducible sessions, and allows the project to focus on mechanics and educational clarity.

---

## 9. Educational Direction

The game is intended to support graduate-level healthcare education, including possible use in Wharton healthcare programs.

Important educational capabilities include:

- fixed or seeded scenarios;
- comparable conditions across student teams;
- complete decision logs;
- actor and policy rationales;
- end-of-game causal analysis;
- counterfactual reruns;
- distinction between decision quality and outcome quality;
- and instructor-controlled assumptions or shocks.

The game should support debriefing at two levels:

1. **Player-facing:** decisions, forecasts, observed outcomes, stakeholder reactions, and tradeoffs.
2. **Analytic/instructor-facing:** true state, causal mechanisms, actor utilities, model assumptions, alternative scenarios, and distributional consequences.

Longer-term, role-based team play may assign participants responsibilities such as CEO, CFO, chief medical officer, nursing leader, strategy lead, or government affairs lead.

---

## 10. Initial Development Strategy

The project should begin with a narrow vertical slice rather than a general-purpose framework.

A first playable slice may include:

- one health system;
- one competitor;
- one commercial insurer;
- Medicare and Medicaid;
- a small number of patient cohorts;
- one policy proposal;
- one payer negotiation;
- one workforce pressure;
- a limited set of executive actions;
- several quarterly turns in the first stabilization slice;
- deterministic replay;
- actor-specific observations;
- and an end-of-run explanation.

The stabilization vertical slice at v0.1.27 implements five abstract executive
decision points. A **parallel competitive campaign** (`competitive-regional-v1`)
is now specified separately with **monthly turns**, **1 human + K AI health-system
players**, simultaneous monthly actions, an action economy, executive-report
briefings, and a Stata-like CLI. See
[`docs/design/gameplay-competitive-sketch.md`](design/gameplay-competitive-sketch.md) and
[`docs/design/competitive-scenario-brief.md`](design/competitive-scenario-brief.md).

The purpose of the vertical slice is to validate:

- whether the core loop is engaging;
- whether strategic actors produce understandable behavior;
- whether the true/observed state distinction is useful;
- whether the causal model is explainable;
- and whether Rust supports acceptable iteration speed.

Only after this slice should the project expand its actor set, policy domains, strategic models, or scenario authoring capabilities.

---

## 11. Non-Goals for the First Version

The first version should not attempt to:

- model the entire US healthcare system;
- reproduce every reimbursement rule or clinical detail;
- support multiple countries;
- solve global equilibria among all actors;
- provide empirically authoritative policy forecasts;
- simulate individual patients in full detail;
    - replace the current shared-action GUI boundary with a second simulation or
      browser-owned state model;
- or create a general-purpose policy programming language.

The goal is a credible, transparent, and extensible strategy simulation—not comprehensive replication of reality.

---

## 12. Key Risks

### Scope Expansion

Health policy is effectively unbounded. The project must maintain a strict initial boundary and prioritize interactions that are both educational and playable.

### False Precision

Detailed numerical outputs may appear more validated than they are. Parameters, assumptions, confidence, and sensitivity should be visible.

### Normative Bias

Scoring systems and causal assumptions embed values. Actor objectives, social-welfare criteria, and model assumptions must remain distinguishable and inspectable.

### Over-Engineering

There is a risk of building an abstract simulation framework before confirming the game loop. Concrete vertical slices should precede generalized architecture.

### Strategic Complexity

Game-theoretic NPC behavior can become the entire project. Initial implementations should focus on a few high-value interactions and use bounded, interpretable methods.

### Educational Opacity

A complex model is not educational unless players can understand why outcomes occurred. Causal attribution and debriefing are required features.

### Iteration Speed

Rust's rigor may slow early model changes. Strong module boundaries, data-driven scenarios, and external analysis exports should preserve flexibility.

---

## 13. Measures of Success

An initial version should be considered successful if it can demonstrate that:

- players face meaningful and non-obvious tradeoffs;
- non-player institutions respond coherently to incentives and beliefs;
- identical inputs and actions reproduce identical transitions;
- the same true state can yield actor-specific observations;
- outcomes can be traced to explicit mechanisms;
- different strategies remain defensible;
- the simulation prompts substantive discussion of economics, politics, and organizational behavior;
- and contributors can extend scenarios without rewriting the engine.

---

## 14. Longer-Term Direction

After validating the US regional-market model, the project may expand toward:

- additional US states and institutional environments;
- federal policy scenarios;
- rural and academic health-system variants;
- value-based payment and insurance-market scenarios;
- multiplayer or role-based classroom use (distinct from K AI competitor systems
  in the competitive campaign; see [`core-loop-spec.md`](design/core-loop-spec.md));
- richer instructor tooling;
- comparative model assumptions;
- and non-US health systems.

International expansion should not treat other countries as simple parameter changes. The architecture should support different allocations of authority, financing, ownership, labor relations, and patient choice, while reusing general mechanisms where appropriate.

---

## 15. Guiding Principle

The project should remain grounded in the following principle:

> Build a small, transparent, strategically rich model whose behavior can be understood, replayed, and debated before building a large model whose apparent realism cannot be inspected.

This document establishes the initial direction. Detailed specifications for the domain model, actor framework, policy lifecycle, game-theoretic interactions, observation system, scenario schema, educational design, and CLI will be developed separately.
