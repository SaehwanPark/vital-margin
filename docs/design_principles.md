# Vital Margin
## Design Principles

**Status:** Canonical design guidance  
**Audience:** Project owner and contributors  
**Purpose:** Provide durable principles for evaluating product, simulation, technical, and educational decisions

**Current application:** The playable prototype now applies these principles
across stabilization, competitive regional-market, and regional-affiliation
campaigns, with a CLI/reference interface, MCP adapter, and host-backed loopback
GUI task workspace sharing the same deterministic core and action surface. New
runtime or platform work remains evidence-gated; automated validation does not
establish calibration, policy validity, human learning, lived accessibility, or
classroom effectiveness.

---

## 1. Model Strategic Systems, Not Isolated Decisions

The game should represent health policy and health-system management as the result of interacting institutions rather than a sequence of independent choices.

Player actions should propagate through:

- markets;
- regulation;
- labor;
- financing;
- clinical operations;
- public opinion;
- organizational trust;
- and political response.

The value of the simulation lies in second- and third-order effects. A decision should rarely affect only one metric or stakeholder.

---

## 2. Preserve Meaningful Tradeoffs

The game should not allow the player to optimize every objective at once.

Core tensions may include:

- margin versus access;
- growth versus resilience;
- efficiency versus redundancy;
- control versus professional autonomy;
- short-term stabilization versus long-term legitimacy;
- competition versus regional coordination;
- and organizational interest versus social welfare.

Tradeoffs should be real, persistent, and understandable. Difficulty should come from conflicting objectives and constraints, not arbitrary punishment.

---

## 3. Separate Actor Rationality from Social Welfare

Every actor should pursue its own objectives within its authority, information, and constraints.

A hospital, insurer, regulator, union, employer, elected official, and patient population should not share one hidden objective function. Their preferences may overlap in some contexts and conflict in others.

The game must distinguish:

- what is rational for an individual actor;
- what is beneficial for the player's organization;
- and what improves overall social welfare.

This separation is essential for representing coordination failure, cost shifting, market power, public goods, and policy conflict.

---

## 4. Make Cooperation and Competition Contextual

Actors should not be permanently categorized as cooperative or competitive.

The same organizations may:

- compete for commercially insured patients;
- cooperate on emergency preparedness;
- form coalitions around Medicaid policy;
- bargain aggressively over reimbursement;
- and coordinate on workforce development.

Cooperation should emerge when the value of joint action exceeds coordination costs, defection risks, and available alternatives. Competition should arise from conflicting objectives, scarce resources, or incompatible strategies.

---

## 5. Use Game Theory as a Decision Framework, Not an Ornament

Strategic interaction should be modeled explicitly where it improves behavior and understanding.

Appropriate game forms may include:

- bargaining;
- repeated games;
- coalition formation;
- coordination games;
- entry and capacity competition;
- sequential policy games;
- and Bayesian games with private information.

The project should not require exact equilibrium solutions for every interaction. Bounded rationality, approximate best response, satisficing, level-k reasoning, and structured heuristics may be more realistic and computationally practical.

Game-theoretic models should remain local, inspectable, and tied to specific interactions.

---

## 6. Keep the Core Engine Deterministic

The core engine should be a deterministic state-transition system.

Given:

- an immutable prior state;
- explicit player and non-player actions;
- explicit resolved external inputs;
- and a versioned ruleset;

the resulting events, effects, and next state must be reproducible.

Conceptually:

```text
prior state + actions + resolved inputs + ruleset
  -> events + attributed effects + next state
```

No hidden randomness, system time, network state, mutable singleton, or implicit external dependency should affect core transitions.

---

## 7. Place Stochasticity at Explicit Boundaries

The simulated world may be uncertain and variable even though the engine is deterministic.

Stochasticity may enter through explicitly generated:

- macroeconomic shocks;
- epidemiologic events;
- patient behavior;
- political events;
- measurement noise;
- reporting delays;
- and boundedly rational choice realizations.

Randomness should be seeded, versioned, and isolated by subsystem or stable identifiers. Random draws should become explicit inputs before the core transition is evaluated.

A seed alone is not sufficient if small code changes can shift every later realization.

---

## 8. Distinguish True State, Belief, and Observation

The game should maintain a strict distinction among:

- the true state of the simulated world;
- each actor's beliefs about that world;
- and the observations or reports available to that actor.

Different actors should see different information. Measurements may be:

- delayed;
- incomplete;
- noisy;
- biased;
- revised;
- or strategically disclosed.

Players should make decisions using the information available at the time, not omniscient state.

This principle supports information asymmetry, signaling, uncertainty, and fair evaluation of decision quality.

---

## 9. Treat History as Immutable

Snapshots and committed transitions should be static.

Later corrections should create new information rather than rewrite what an actor previously observed. The history of the simulation should preserve:

- prior true state;
- observed information;
- actions;
- strategic decisions;
- exogenous inputs;
- events;
- effects;
- and resulting state hashes.

Immutable history enables:

- replay;
- auditing;
- counterfactual analysis;
- debugging;
- educational debriefing;
- and reproducibility.

---

## 10. Make Causality Inspectable

The simulation should explain why outcomes occurred.

Major effects should retain provenance, allowing the game to attribute changes to:

- policy;
- contracts;
- labor pressure;
- capital decisions;
- market response;
- implementation quality;
- macroeconomic conditions;
- and delayed feedback.

A player should be able to distinguish:

- direct from indirect effects;
- immediate from delayed effects;
- intended from unintended effects;
- and structural consequences from random realizations.

Opaque complexity is not realism.

---

## 11. Prefer Credible Abstraction Over Exhaustive Detail

The first goal is not to reproduce every reimbursement rule, clinical workflow, or legal provision.

Realism should come from:

- correct institutional relationships;
- plausible incentives;
- credible constraints;
- understandable causal mechanisms;
- and realistic strategic response.

A small model with coherent behavior is more valuable than a large model with uninterpretable outputs.

Every added detail should justify itself through gameplay, education, or model validity.

---

## 12. Make Assumptions Visible and Contestable

Health policy includes empirical uncertainty and normative disagreement.

The game should not present assumptions as undisputed facts. Important assumptions should be:

- documented;
- versioned;
- configurable where practical;
- associated with evidence or expert judgment;
- and tested through sensitivity analysis.

The project should support alternative parameterizations or behavioral models when credible disagreement exists.

The model should clearly distinguish:

- empirical claims;
- theoretical assumptions;
- design abstractions;
- balancing choices;
- and normative scoring decisions.

---

## 13. Separate Mechanics, Institutions, Scenarios, and Evaluation

The architecture should distinguish:

- **mechanics:** general processes such as bargaining, demand response, measurement, and coalition formation;
- **institutions:** hospitals, insurers, Medicaid, regulators, employers, and labor organizations;
- **scenarios:** initial conditions, actor configurations, policies, events, and learning objectives;
- **evaluation:** organizational performance, actor utility, social welfare, and educational assessment.

This separation supports extensibility and prevents the US implementation from becoming inseparable from the engine.

---

## 14. Keep the Engine Typed and the Content Data-Driven

Rust should be used to encode:

- domain invariants;
- valid state transitions;
- actor and policy types;
- commands, events, and effects;
- validation;
- replay;
- and deterministic resolution.

Scenario content and empirical parameters should remain external where practical.

Configuration should compose known mechanisms rather than permit arbitrary executable logic. The project should avoid accidentally creating an unrestricted rules language before the core game is mature.

---

## 15. Make Invalid States Difficult to Represent

The type system should express important distinctions directly.

Examples include:

- proposed versus enacted policy;
- legal authority versus political influence;
- true metrics versus reported metrics;
- valid commands versus resolved outcomes;
- money versus rates versus probabilities;
- and technical failure versus unfavorable strategic result.

A rejected contract, failed coalition, or strike is a legitimate game outcome. An action issued by an actor without authority is a validation failure.

The code should preserve that distinction.

---

## 16. Favor Pure Transitions and Explicit Effects

Core logic should be organized around:

```text
command
  -> validation
  -> strategic resolution
  -> domain events
  -> attributed effects
  -> next state
```

Systems should inspect state and emit explicit effects rather than mutating a shared world opportunistically.

A central resolver should handle:

- ordering;
- simultaneity;
- conflicts;
- invariants;
- and final commitment.

This reduces hidden coupling and makes outcomes easier to test and explain.

---

## 17. Design Non-Player Decisions for Interpretability

Non-player actors should produce not only actions, but also rationales.

A strategic decision record should identify:

- feasible actions considered;
- expected benefits and costs;
- beliefs about other actors;
- outside options;
- risk and time preferences;
- and the selected decision procedure.

The rationale need not expose every internal numeric detail to the player, but it should be available for debugging, analysis, and instruction.

Non-player actors should be coherent without being omniscient or perfectly optimal.

---

## 18. Distinguish Decision Quality from Outcome Quality

A good decision may lead to a poor realized outcome. A bad decision may succeed by chance.

The game should support evaluation based on:

- information available at decision time;
- quality of reasoning;
- robustness across plausible realizations;
- consistency with strategy;
- and adaptation to new evidence.

This principle is central to educational use. The game should not teach hindsight bias.

---

## 19. Treat Distributional Effects as First-Class Outcomes

Aggregate improvement can conceal concentrated harm.

The simulation should track, where relevant, outcomes across:

- income;
- geography;
- insurance status;
- age;
- health risk;
- race and ethnicity;
- urban and rural populations;
- providers;
- employers;
- taxpayers;
- and future versus current populations.

Distributional analysis should not be an optional report added after the core model. It should influence policy, stakeholder behavior, legitimacy, and evaluation.

---

## 20. Design for Debriefing, Not Only Play

The game should support structured reflection.

A completed run should make it possible to ask:

- What did the player know?
- What did other actors believe?
- Why did each actor act?
- Which mechanisms drove the outcome?
- Which effects were delayed?
- What alternatives were available?
- How sensitive was the result to assumptions?
- Was the decision reasonable even if the outcome was unfavorable?

The debrief is part of the product, not supplementary documentation.

---

## 21. Preserve Multiple Defensible Strategies

The game should avoid a single hidden optimal path.

Scenarios should permit different coherent strategies, such as:

- financial stabilization;
- safety-net preservation;
- regional growth;
- value-based transformation;
- workforce investment;
- or political coalition building.

Strategies should create different risks, stakeholder relationships, and long-term consequences.

Balance should not mean making every action equally effective. It should mean that multiple approaches can be rational under different objectives and beliefs.

Difficulty settings should preserve this principle. Harder tiers may give
rivals better resource access, faster information, or more aggressive risk
posture, but they should not rely on hidden omniscience or arbitrary punishment.
The hardest tier should be severe but winnable through more than one coherent
strategy.

---

## 22. Build Vertical Slices Before General Frameworks

The project should validate its distinctive ideas through a narrow playable slice before expanding.

A useful slice should include:

- one player health system;
- a few external actors;
- one strategic negotiation;
- one policy process;
- true versus observed state;
- stochastic inputs;
- delayed effects;
- deterministic replay;
- and causal explanation.

Generalization should follow demonstrated need.

The project should resist building a universal simulation framework before proving that the game is understandable, engaging, and educational.

---

## 23. Research Before Calibration, Validation Before Authority

Mechanisms should be grounded in literature, prior simulations, expert input, or clearly labeled abstraction.

Calibration should preserve uncertainty rather than manufacture precision. Validation should include:

- technical correctness;
- institutional plausibility;
- strategic coherence;
- sensitivity analysis;
- gameplay quality;
- and educational effectiveness.

The game must not be presented as a policy forecasting tool unless substantially stronger validation is completed.

---

## 24. Optimize for Contributor Comprehension

The architecture, model, and documentation should be understandable to contributors from different backgrounds.

Design decisions should favor:

- explicit concepts;
- stable terminology;
- narrow interfaces;
- versioned assumptions;
- local reasoning;
- and strong examples.

Sophistication should come from interacting simple mechanisms, not from unnecessary abstraction or clever code.

---

## 25. Preserve Extensibility Without Premature Generalization

The first version is US-focused, but the conceptual model should avoid assumptions that make broader health-policy modeling impossible.

International expansion may reuse general mechanisms while redefining:

- financing;
- ownership;
- purchasing;
- authority;
- benefit design;
- labor relations;
- capital allocation;
- and patient choice.

Other health systems should not be modeled as US healthcare with different parameter values.

Extensibility should be achieved through separation of concerns, not speculative abstraction.

---

## 26. Keep the CLI as a Reference Interface and Build the GUI as a Shared Boundary

The terminal interface should emphasize:

- clear state summaries;
- concise policy and stakeholder briefings;
- explicit decisions;
- reproducible commands;
- causal reports;
- and complete logs.

The CLI remains a reproducible reference interface for systems, explanation, and
educational usability. GUI development is the active presentation focus, but it
must consume the same host-authoritative action surface rather than introduce a
second rules or persistence model.

Future interfaces should consume the same underlying engine rather than redefine the simulation.

The loopback GUI remains an interface layer: rendering, input, assets, layout,
and packaging stay outside the deterministic core; the same actor observations,
commands, replay history, checkpoints, and debrief logic stay inside the product
boundary. Chromium evergreen desktop is the default end-user target; the Codex
in-app browser is a development inspection surface, while Firefox, WebKit/Safari,
mobile, and legacy browsers remain deferred and non-certified.

Regional merger or acquisition mechanics should be held to the same standards
as other strategic interactions. They must separate organizational advantage,
actor utility, social welfare, community effects, and educational evaluation
instead of treating consolidation as automatically good or bad.

---

## 27. Adopt Explicit Design Tensions

Some principles will conflict and require judgment.

Examples include:

- realism versus playability;
- rigor versus iteration speed;
- transparency versus information overload;
- stable mechanics versus empirical revision;
- deterministic replay versus behavioral variation;
- and extensibility versus simplicity.

These tensions should be documented rather than resolved implicitly.

When choosing between them, the project should generally prefer:

1. conceptual clarity;
2. reproducibility;
3. educational usefulness;
4. strategic depth;
5. credible abstraction;
6. implementation elegance.

---

## 28. Guiding Test for New Features

Before adding a feature, ask:

1. Which player or educational problem does it solve?
2. Which mechanism or institution does it represent?
3. Does it create a meaningful decision or explain an important consequence?
4. Can it be tested and replayed deterministically?
5. Can its assumptions and causal effects be inspected?
6. Does it fit the current scope?
7. Could the same value be achieved with a simpler abstraction?

A feature that fails these questions should usually be deferred.

---

## 29. Guiding Principle

> Build a transparent strategic system in which institutions act on incomplete information, policies alter incentives and constraints, and outcomes emerge through understandable causal mechanisms.

The project should prioritize a small number of deeply coherent interactions over broad but shallow coverage. Its success will depend not on simulating everything, but on making complex health-policy dynamics playable, inspectable, and debatable.

## 30. Progressive task presentation

The GUI should present one player task at a time and reveal additional detail
through explicit, reversible navigation or disclosure. Progressive presentation
may reduce default density, but it must never remove actor-visible source,
uncertainty, missingness, cost, legality, history, written equivalents, or
host-owned consequences. Navigation and acknowledgement state are ephemeral
presentation state; commands, deterministic transitions, replay, checkpoints,
and debrief semantics remain host-authoritative. Icons and visual tokens may
supplement repeated labels only when a persistent legend, accessible name, and
text explanation remain available.
