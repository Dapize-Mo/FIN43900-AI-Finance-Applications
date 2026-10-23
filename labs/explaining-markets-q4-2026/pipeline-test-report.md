# Hosted pipeline test — October 6, 2026

**Author: Oladapo Olaniyan — FIN-43900**

**Outcome: all checks passed.**

The test ran the production `predict(event)` function in Modal with the same image and credentials as the deployed agent. Only the materials download was replaced with controlled synthetic facts, preview, and option statistics; Gemini inference was real. No synthetic forecast was posted to the competition prediction API.

| Synthetic case | Predicted percentile | Model execution time |
|---|---:|---:|
| Positive revenue/EPS surprise, raised guidance, stronger orders | 0.88 | 1.120 seconds |
| Results in line with consensus and unchanged guidance | 0.50 | 0.639 seconds |
| Negative revenue/EPS surprise, cut guidance, cancelled orders | 0.02 | 0.644 seconds |

Each case produced one correctly identified asset and a numeric percentile in [0,1]. Predictions followed the expected positive > neutral > negative order. All model calls finished well inside the configured 270-second check allowance; these times exclude initial container startup and full event delivery overhead.

Additional live checks against https://d-olaniyan06--explaining-markets.modal.run/:

- Health GET: HTTP 200.
- Unsigned synthetic webhook POST: HTTP 401, correctly rejected before prediction processing.

Previous verification remains relevant: 32 offline tests passed, and the competition portal verified signed delivery, acknowledgement, and return test prediction. This test did not resend a scored event or modify the production strategy, deployment, or model card.

## Limits

This is a three-case synthetic behavioral and connectivity test, not an accuracy benchmark. It does not establish calibration, real-event rank correlation, competition score, deadline reliability under load, or prize eligibility. Historical holdout evaluation and real-event scoring remain unevaluated. Hosting remains subject to the $1 workspace limit and Gemini project quotas.

## Created files

- `C:/Users/dolan/OneDrive - purdue.edu/2026-Fall/FIN-43900 - AI Finance Applications/labs/explaining-markets-q4-2026/agent/pipeline_check.py`: reproducible hosted checks.
- `C:/Users/dolan/OneDrive - purdue.edu/2026-Fall/FIN-43900 - AI Finance Applications/labs/explaining-markets-q4-2026/pipeline-test-results.json`: measured results.
- `C:/Users/dolan/OneDrive - purdue.edu/2026-Fall/FIN-43900 - AI Finance Applications/labs/explaining-markets-q4-2026/pipeline-test-report.md`: this report.

Hosted run: https://modal.com/apps/d-olaniyan06/main/ap-SqmXtlYnDFRFBREVgcvMFn.
