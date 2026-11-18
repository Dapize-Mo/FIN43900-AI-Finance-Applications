# Explaining Markets change history

**Oladapo Olaniyan — FIN-43900**

## November 12, 2026 — error-mining research (nothing deployed)

- Research only (rulebook-2026-11-09/): tested recalibration and ridge/feature adjustments on live forecasts, Nov 3-6 (n=1,042). Best variant, forecast + preview tone, gained +0.017 delta R^2 (90% CI [+0.010, +0.025]), but about a dozen variants were tried on the same four days, so the gain is flattered.
- Clean check on unseen events, Nov 9-11 (n=267): raw 0.1915, frozen adjustment 0.1963, difference +0.0048, 90% CI [-0.022, +0.032]. Not confirmed; no deployment recommended. Live agent unchanged.
- Gemini free-tier limits (read Nov 9): no stronger model is usable at competition volume (LIMITS.md).
- The official Q4 archive (2026Q4.jsonl.gz, 13 MB) stays local and is not committed; fetch_q4.py re-downloads it.

## November 6, 2026 — deadline-aware retry deployment

- Diagnosis: Modal logs (Oct 16–Nov 5) showed 33 failed predictions after acknowledged webhooks (24 Gemini 503, 4 timeouts, 5 Oct 28 blend double-failures). 32 had no submitted forecast. 27 of those fall on Oct 16–29, close to the 26-event leaderboard shortfall. See no-llm-candidate-2026-11-05/DIAGNOSIS_2026-11-05.md.
- Change (agent/predict.py, uncommitted): temporary provider errors (429/5xx, timeout, connection) alternate Gemini 3.5/3.1 Flash-Lite with backoff until 25 s before the event deadline. Prompt, inputs, temperature and the success path are unchanged. No neutral placeholder. Patch and tests: reliability-proposal-2026-11-06/.
- Verification: 48 agent tests passed (7 new). Explicit user approval; the user ran the Modal deploy. Health reports original-2026-10-28, unsigned POST returns 401, portal signed round trip verified 12:29:55 AM ET Nov 6. Public model card updated and republished. Spending, credentials and past predictions unchanged. No commit or push.
- Research: no-LLM feature/ridge candidate rejected on frozen walk-forward tests (no-llm-candidate-2026-11-05/REPORT.md).

## October 27, 2026 — audit and diagnostic deployment

Agent repository commit: `12ec49b` — Add experimental Gemini blend and forecast diagnostics. The independently versioned agent lives in `agent/`; its code is deliberately excluded from this course repository.

- Added sanitized per-component forecast logs without event documents or credentials; predictions and spending settings unchanged. Explicit deployment approval obtained; endpoint and portal signed test verified.
- Agent suite: 37 passed; one upstream Starlette/AnyIO deprecation warning.
- Verified contest snapshot through October 26: 65/354, incremental R² 0.036, 270/279 coverage. Latest scored event cohort predates the blend; 80 newer forecasts were pending.
- Fresh, previously unused 96-event comparison: original prompt 0.154475 incremental R², blend 0.127457. Blend difference -0.027018, paired-bootstrap 90% interval [-0.061491, 0.000898]. Neither the positive evidence gate nor the predefined negative rollback criterion passed. Forecast method retained; no live improvement claimed.
- Research and reports: [October 27 report](improvement-2026-10-27/REPORT.md), frozen plan, scorer-based metrics and audit provenance. All 192 component responses completed after bounded retries.

## October 23, 2026 — experimental blend deployment

- Earlier 32-development/64-holdout comparison selected the equal-weight blend. Holdout original prompt 0.145358 incremental R²; blend 0.165916. Gain 0.020559, 90% interval [-0.015809, 0.061457]; positive deployment gate failed.
- After uncertainty was disclosed, the user explicitly authorized the experimental blend. Concurrent original/outlook Gemini 3.5 Flash-Lite calls at temperature zero, single-component fallback, bounded retries, existing webhook security and deduplication preserved.
- Hosted synthetic checks and full signed round trip passed; public model card updated; spending limits preserved. No prior predictions changed.
- [Research report](improvement-2026-10-23/REPORT.md) and [deployment record](improvement-2026-10-23/deployment-2026-10-23/DEPLOYMENT.md).

## Version-control boundaries

This course commit includes research source, immutable event plans, aggregate metrics, provenance, MIT-licensed organizer scoring source, and reports. Downloaded raw archives, inference response caches, local rollback copies, environment files, credentials and Python caches remain local and excluded. Reproducing provider calls requires the official archives and private credentials; no credential is committed. The root .gitignore change was committed separately as bbc5382 while this work was in progress; it is not included in this research commit. No push is authorized or performed.
