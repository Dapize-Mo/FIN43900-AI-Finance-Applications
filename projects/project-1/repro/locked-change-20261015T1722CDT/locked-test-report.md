# Locked changed-input test — terminal ROIC

**Analyst:** Oladapo Olaniyan  
**Course:** FIN-43900 — AI Finance Applications  
**Precommit:** October 15, 2026, 5:22 p.m. CDT  
**Instruction basis:** Oladapo reported that the professor clarified in class on October 15 that the “no AI” wording was a typo and encouraged more AI use. This test prediction was AI-assisted and that clarification is recorded in the validation ledger.

## Frozen design

- **Material input:** global terminal incremental ROIC.
- **Change:** 15.0% to 12.0%.
- **Expected:** lower ROIC increases terminal reinvestment for the same terminal growth, reducing terminal FCFF, terminal value, and value per share. The expected working decision label was watch/defer with narrower valuation support.
- **Frozen baseline:** `frozen-baseline/`; source and input SHA-256 values are in `frozen-baseline/snapshot-hashes.csv`.
- **Baseline comparison output:** copied from `outputs/final-working-run/` before the test.
- **Test run:** `experiment-run/outputs/after-change/`.

The run uses a copy of the frozen model and data. Semantic comparison confirms the only changed model assumption is `terminal_roic`; the copied model, checks, and all other data files retain their frozen hashes. The original working model and `outputs/final-working-run/` were not changed.

## Result

| Base-case measure | Baseline (15% ROIC) | Changed (12% ROIC) | Change |
|---|---:|---:|---:|
| Terminal reinvestment ($M) | 2,270.1 | 2,837.6 | +567.5 |
| Terminal FCFF ($M) | 11,350.3 | 10,782.8 | -567.5 |
| Present value of terminal value ($M) | 160,985.3 | 152,936.1 | -8,049.3 |
| Enterprise value ($M) | 200,935.6 | 192,886.3 | -8,049.3 |
| Value per diluted share | $117.29 | $111.41 | -$5.88 (-5.02%) |
| Terminal value / EV | 80.12% | 79.29% | -0.83 percentage points |
| Draft action label | Watch/defer | Watch/defer | No change |

The direction prediction matched. The action label did not flip because the model writes a fixed `watch/defer pending analyst review and source/convention closure` string; it has no numeric action threshold. The unchanged label is therefore not evidence that ROIC does not matter. Both base values remain below the unchanged $125.65 October 5 reference price.

Other scenario values per diluted share also declined: low $76.12 to $73.84; high $170.22 to $159.87; Value Reset Failure $51.63 to $50.51.

## Run and check record

- The copied model exited **0** and produced a distinct output directory.
- Its ordinary check suite reported **42 PASS, 0 FAIL, 5 OPEN, 2 QUALIFIED**. The open/qualified items are unresolved evidence or judgment checks. The suite contains a static “human locked record blank/not run” OPEN message because the unchanged check code predates this separate test; the dedicated precommit and this report document the completed test. Do not treat that static row as the locked-test result.
- The changed run input hashes are in `experiment-run/run-input-hashes.csv`; the generated run records its own source/data hashes in `experiment-run/outputs/after-change/input-hashes.json`.
- No external source, current market input, recommendation assumption, or original output was updated by this test.

## Limitations

This is a one-variable model response test, not validation that 12% is the correct terminal ROIC or a complete investment recommendation. The action label is not threshold-driven. Source closure, current bridge, peer judgments, and student acceptance of the full valuation remain open.
