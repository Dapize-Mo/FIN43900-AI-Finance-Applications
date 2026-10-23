# Validation and AI Use — Working Record

**Author:** Oladapo Olaniyan  
**Project version:** Initial Edition B work started October 6, 2026  
**Current repository state:** No project-specific commit has been made for this working package.  
**Source boundary:** As of October 6, 2026 for this initial audit; refresh to the final declared valuation date before freezing results.  
**Status:** Planning/source identification only; no Project 1 valuation is validated.

## Data and convention ledger

See `source-register.csv`. No pending source extraction or market datum is an approved valuation input. Add exact values, definitions, units, transformations/exclusions, and independent checks only after direct verification.

## Validation register

| Claim/output | Failure mode | Test and expected result/direction | Actual result | Disposition | Evidence location |
|---|---|---|---|---|---|
| Model responds to published synthetic known-answer case | formula, timing, or bridge error | Reconcile every published training output within its tolerance | Not run for Project 1 package | Open | Add result and output path after execution |
| Load-bearing source definition | GAAP/non-GAAP, unit, fiscal-period, or share-count mismatch | Independently reconcile to filing or authoritative definition | Not run | Open | `source-register.csv` and evidence ledger |
| Pro-forma statements articulate | Cash flow and balance sheet do not connect or balance | Balance sheet gap zero within stated tolerance; cash-flow ending cash ties to balance-sheet cash; base year reconciles | Not run | Open | Model checks/output |
| DCF boundary and direction | terminal growth >= WACC or valuation moves in wrong direction | Invalid terminal relation must fail; higher WACC lowers value; higher terminal growth raises value | Not run | Open | Model checks/output |
| Enterprise-to-equity bridge | debt/cash/share definition inconsistency | Independently recompute bridge and per-share basis | Not run | Open | Bridge check/output |
| Peer policy and multiple consistency | cherry-picked peer, mismatched metric/period/claims | Apply predeclared policy and reconcile EV and equity multiples | Not run | Open | Peer policy and peer data ledger |
| Highest-risk/downside test | shock not propagated through linked forecast or does not connect to action | Trace named shock through statements, cash flow/value, and conditional action | Not run | Open | Scenario record/output |
| Clean-environment run | hidden local dependency or missing input prevents reproduction | Fresh environment reaches same visible output; preserve first failure and resolution | Not run | Open | Cold-run log |
| AI output check | unsupported AI claim or model-generated conclusion accepted without evidence | Preserve one material output and independently test it; record disposition | Not run | Open | Named AI-use register |

## Locked Changed-Input Record — prediction frozen before the test

**Instruction clarification reported by Oladapo Olaniyan:** In class on October 15, 2026, the professor said the “no AI” instruction was a typo and encouraged students to use more AI. This precommit is therefore AI-assisted. The earlier AI-off language in the working notes is superseded for this exercise based on that student-reported clarification; it is retained in prior records as historical context.

### Precommit — AI-assisted prediction frozen before run

| Precommit timestamp | Repository commit/snapshot | Material input | Old → new value and units | Expected output direction | Expected decision effect |
|---|---|---|---|---|---|
| 2026-10-15 5:22 p.m. CDT | `repro/locked-change-20261015T1722CDT/frozen-baseline/` | Terminal ROIC | 15.0% → 12.0% annual terminal incremental ROIC | Lower terminal FCFF, terminal value, and base value per diluted share; lower ROIC requires more reinvestment to support the same terminal growth | Narrow the valuation support; draft watch/defer expected to remain unchanged because base value is already below the observed price and evidence gaps remain |

### Preserved execution result — complete only after the frozen precommit

| Before/after output | Actual decision effect | Prediction reconciliation | Failure diagnosis or reason action did not change | Evidence path |
|---|---|---|---|---|
|  |  |  |  |  |

## Named AI-use register

| Tool/model/version exposed | Date | Material task | Output considered | Independent check | Disposition | Decision effect |
|---|---|---|---|---|---|---|
| Codex AI assistant (GPT-6; this session) | 2026-10-06 | Read course requirements, inspect existing artifacts, plan Edition B/source gates | Requirement summary and preliminary gap audit in `README.md` and `artifact-audit.md` | Compared against the live Brightspace assignment/homepage, checkpoint receipt, and local course files; all valuation claims remain pending | Use as planning aid; source and model claims remain unaccepted until independently verified | None yet; recommendation pending |
| Codex AI assistant (GPT-6) | 2026-10-15 | Develop and freeze changed-input prediction; select one material assumption change and expected effects | AI-assisted precommit: terminal ROIC 15.0% to 12.0% | Reviewed the model formula: terminal reinvestment = terminal NOPAT × g / ROIC; lower ROIC raises reinvestment and lowers terminal FCFF/value | Use as an AI-assisted test prediction following Oladapo Olaniyan's report that the professor clarified the “no AI” instruction was a typo in class on October 15 | Lower terminal value/base value; expected draft action remains watch/defer |

## Limitations, monitoring, and escalation

- Current FY2024 material is not enough to make a current valuation. Rebuild the base using the FY2025 filing and latest interim period.
- The latest current market price, beta/WACC inputs, and comparable-company data are not yet verified.
- A first successful Edition A receipt was verified; this record does not independently prove the pre-checkpoint tool history.
- The Brightspace-linked Edition A attachment was retrieved read-only and compared with the local PDF. They are byte-identical (SHA-256 `F745E7EA27A1445830573029A77D28967A1E4F5E53A9BA9A794079373F35464F`); both contain a one-page Edge “File not found” message. The receipt confirms submission event only. Edition A content/recovery remains an issue for instructor/TA guidance; neither copy was modified.
- Keep the original Edition A file unchanged and record any correction separately.
- The locked changed-input test is blocked until the analyst writes and freezes the human prediction above. The prediction must not be AI-assisted; execution must occur with AI closed.
