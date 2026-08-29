# Glossary

[Documentation Home](../index.md) | [Installation Guide](../guides/installation.md) | [GUI Guide](../guides/gui-how-to-play.md) | [CLI Guide](../guides/how-to-play.md) | [Strategy Guide](../guides/strategy-and-mechanics.md)

**Status:** Maintained terminology reference  
**Audience:** Players, contributors, domain reviewers, and playtest designers  

This glossary defines core terminology for **Vital Margin**, aligned with
[`system-boundary.md`](../design/system-boundary.md) and
[`design_principles.md`](../design_principles.md).

---

## ⚙️ Simulation Core

| Term | Definition |
| --- | --- |
| **True state** | The full modeled world state stored within the deterministic transition engine. |
| **Observation** | Actor-specific reported measures and metrics visible to a specific player at decision time. Excludes hidden rival choices and unresolved future stochastic inputs. |
| **Resolved inputs** | Seeded stochastic values computed before a transition executes. |
| **Transition** | One deterministic step: `prior state + player commands + resolved inputs + ruleset → next state`. |
| **History** | Genesis state plus an append-only sequence of committed transitions. |
| **State hash** | Stable 64-bit FNV-1a fingerprint calculated over canonical state for replay and verification checks. |
| **Replay** | Complete re-execution of committed transitions from genesis to mathematically verify state hashes and run reproducibility. |
| **Replay artifact** | Versioned text export containing seed, campaign ruleset, and committed history. |

---

## 🏛️ Executive Resources & Economics

| Term | Definition |
| --- | --- |
| **Action Points (AP)** | The monthly management-attention budget that limits how many strategic commands an executive can submit in a single month (e.g., 3 AP/month on Normal). |
| **Cash Runway** | Estimated months of liquidity remaining before reserves are exhausted (`comfortable`, `watch`, `strained`, `critical`). |
| **Political Capital (PC)** | Influence and advocacy resource consumed when conducting rate negotiations or making binding public pledges. |
| **Operating Margin** | Net operating revenue minus operating expenses divided by revenue; reflects day-to-day healthcare delivery profitability. |
| **Workforce Trust** | Staff morale and retention index (0% to 100%). High trust boosts clinical retention; low trust accelerates nurse vacancy and turnover. |
| **Capital Project** | Multi-month infrastructure or IT initiative (e.g., `asc_unit`, `cardiac_tower`, `ehr_epic`) with monthly cash draws (max 2 active projects). |

---

## 🎮 Actors & Commands

| Term | Definition |
| --- | --- |
| **Player command** | Validated executive action submitted to the simulation host (e.g., `invest`, `recruit`, `monitor`, `negotiate`, `commit`, `project`, `hold`). |
| **Simultaneous resolution** | Execution mode where human player commands and all autonomous AI rival plans are resolved concurrently in the same monthly step. |
| **AI player** | In-game autonomous health system peer (e.g., Summit Health, Northlake Regional) competing for regional market share under the exact same command catalog. |
| **AI-agent playtester** | External testing client running via Model Context Protocol (MCP) or loopback GUI to generate automated validation evidence; distinct from an in-game AI rival. |
| **NPC actor** | External institutions (commercial payers, Medicaid/Medicare regulators, labor unions, community coalitions) that react to market conditions. |
| **Attributed effect** | Explicitly labeled delta linking an action or external event to a specific metric change in the post-turn resolution ledger. |
| **Actor card** | Specification defining an institutional actor's authority, incentives, and decision procedure. |

---

## 🎓 Educational & Debriefing Concepts

| Term | Definition |
| --- | --- |
| **Debrief** | End-of-run causal explanation generated from committed history and visible observations. |
| **Decision quality** | Retrospective evaluation of whether an executive choice was sound, timely, and defensible *given only the information visible at decision time*. |
| **Outcome quality** | The realized end-state metrics after accounting for unpredictable rival actions and stochastic shocks. |
| **Pledge Follow-Through Gap** | Discrepancy that occurs when a player makes high public access or workforce pledges without backing them up with operational capacity and capital investments. |

---

## 📦 Campaigns & Scenarios

| Term | Definition |
| --- | --- |
| **Campaign** | Standalone playable game mode: `stabilization-v1` (5-turn tutorial), `competitive-regional-v1` (24-month competition), or `regional-affiliation-v1` (6-stage partnership scenario). |
| **Scenario** | Packaged initial world state, actor configuration, and learning objectives. |
| **Vertical slice** | Bounded end-to-end playable slice proving game design, simulation determinism, and user experience. |
| **Abstraction** | Intentional design simplification used to illustrate a health-policy mechanism without claiming empirical predictive calibration. |

---

## 🔗 Related Documents

- [`system-boundary.md`](../design/system-boundary.md)
- [`actor-cards.md`](../design/actor-cards.md)
- [`competitive-scenario-brief.md`](../design/competitive-scenario-brief.md)
- [`gameplay-competitive-sketch.md`](../design/gameplay-competitive-sketch.md)
- [`versioning-policy.md`](versioning-policy.md)
