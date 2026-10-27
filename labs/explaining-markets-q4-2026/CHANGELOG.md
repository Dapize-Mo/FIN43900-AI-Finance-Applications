# Explaining Markets change history

**Oladapo Olaniyan — FIN-43900**

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
