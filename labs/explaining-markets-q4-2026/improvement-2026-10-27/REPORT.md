# Rank recovery audit and fresh validation

**Oladapo Olaniyan — FIN-43900 — October 27, 2026**

## Outcome

No demonstrated rank recovery or proven forecasting upgrade was established. The live method remains the user-authorized October 23 equal-weight blend. A diagnostic-only update was explicitly approved and deployed October 27, preserving the predictions, credentials, spending settings and prior source. Do not interpret the lack of a strategy switch as evidence that the blend is superior.

## Why the drop does not measure the blend

The latest contest snapshot, through October 26 at 23:45 UTC, placed the submission 65/354, delta R² 0.036 and 270/279 coverage. The private all-quarter R² of 0.098 over 286 scored predictions is a different metric.

All 286 scored rows displayed event dates through October 23. There were 80 pending forecasts: 19 dated October 26 and 61 dated October 27. The official archive confirms the 34 October 23 events ended by 18:00 UTC, while the blend deployment was verified by 23:37:35 UTC that evening. The pre-deployment portal showed its last delivery at 23:00:54 UTC. These observations support attributing the currently scored cohort to the older strategy, rather than claiming that the blend caused the rank decline. Event times alone are not a complete per-prediction deployment audit; original delivery timestamps and this recorded portal context support the timing conclusion.

The older October 22 cohort had 105 scored forecasts with rounded-display MAE approximately 0.277, compared with 0.186 for 40 October 20 forecasts. This is a descriptive error diagnostic, not the contest ranking metric or a causal decomposition of rank. Quarterly target percentile labels and participant scores change as the scored sample grows.

## Infrastructure audit

Before the new synthetic check, rolling 24-hour health showed 73 successful deliveries and 73 predictions, with zero delivery failures, late, duplicate or invalid submissions. A five-day ERROR-filtered Modal log search returned no matching error lines; this is not proof that all historical events succeeded. The common-board shortfall of nine is not equivalent to nine pipeline failures: the portal separately displays seven Excluded and five Missing Data rows, whose detailed reasons were unavailable in the visible table. No past predictions were revised or resubmitted.

## Fresh historical comparison

The user explicitly approved sending official facts, previews and available option statistics for 96 additional archived events to Gemini. Outcomes, archived reference predictions, account details and competition credentials were excluded from prompt bodies. Authentication used the existing Gemini key only at its intended provider endpoint.

The fixed 96-event Q3 sample excludes every event in the original evaluation. Both prompts and the 50/50 weight were frozen, with no selection or tuning on this sample. Both methods used Gemini 3.5 Flash-Lite at temperature zero. Quarter-wide labels used the pinned organizer scorer already preserved in the October 23 research folder. Five hundred paired bootstrap resamples used a fixed seed. All 192 unique component responses succeeded after bounded, paced retries. Temporary error categories: {'RateLimitError': 3, 'InternalServerError': 1, 'APITimeoutError': 1}.

| Method | Fresh 96-event incremental R² |
|---|---:|
| Original prompt, temperature zero | 0.154475 |
| Equal-weight blend | 0.127457 |

Blend minus original: **-0.027018**. Paired-bootstrap 90% interval: **[-0.061491, 0.000898]**.

The blend failed the positive deployment-evidence gate. The result favors the original prompt on this sample, but the interval narrowly includes zero. The pre-result policy recommended rollback only for loss at least 0.01 and an interval wholly below zero. That rollback criterion was not met. Keep the existing authorized experiment until genuinely prospective evidence arrives; do not repeatedly tune or retest weights against this now-examined sample. The earlier favorable historical sample and this unfavorable one show instability, not proof of a reliable improvement.

Historical training contamination cannot be excluded. Archived bundles may differ from original delivery-time materials. The original live baseline left temperature at the provider default, whereas this controlled comparison uses zero; it is not an exact replay. Historical absolute scores do not predict a leaderboard position. Event bootstrap intervals also may understate uncertainty from correlated company/date observations. No guaranteed rank gain is claimed.

## Diagnostic deployment and verification

The new [FORECAST_AUDIT] record contains ticker, event type, original forecast, outlook forecast, resulting blend and strategy label. It excludes credentials and document contents. Existing Modal log timestamps identify when a record was emitted. Normal prediction logic and model-call volume are unchanged from the October 23 blend. TEST events still bypass model inference.

The original failing diagnostic test showed the audit record was absent; after implementation the complete agent suite passed **37 tests**, with one upstream Starlette/AnyIO deprecation warning. The user explicitly approved the production diagnostic deployment after automatic approval review initially rejected it for lacking exact deployment authorization. Modal deployment then succeeded. Live health passed, unsigned requests returned 401, and the portal confirmed the full signed round trip at **1:49:28 PM America/Indianapolis on October 27**. The model card remains materially accurate because the forecasting method did not change.

## Next decision

Use future component logs matched to newly released official outcomes to compare the original prompt and blend prospectively. The 80 pending forecasts are the next evidence, not guaranteed improvement. No recurring monitor was scheduled. No extra model providers, paid plans or increased spending limits were enabled.

## Files created or modified

Research folder: C:/Users/dolan/Code/school/Fall-2026/FIN-43900/workspace/labs/explaining-markets-q4-2026/improvement-2026-10-27

- REPORT.md: this report.
- audit.json: dated leaderboard, health, event-timing audit and source metadata.
- EARNINGS_RELEASE_2026Q4.jsonl.gz: current official archive, through October 23.
- validate_fresh.py: frozen independent-sample comparison.
- fresh-plan.json: immutable sample, prompts hash and gate.
- decision-policy.md: decision policy recorded before inspecting results.
- results/inferences.jsonl: cached responses and sanitized error categories.
- results/fresh-metrics.json: final complete corrected scores and bootstrap interval.
- predict.py.before-audit: exact rollback copy of the October 23 prediction code.
- deployment-check.json: diagnostic-deployment source hash and endpoint checks.

Agent folder: C:/Users/dolan/Code/school/Fall-2026/FIN-43900/workspace/labs/explaining-markets-q4-2026/agent

- predict.py: component-level diagnostic logging; no forecast-method change.
- tests/test_forecast_audit.py: diagnostic record and credential/document-exclusion check.

Ordinary Python/pytest caches may also have been produced within the local Code workspace. Source archives, baseline strategy, original research results and spending configuration were preserved.

## Sources

Accessed October 27, 2026; archive hash and source metadata are in audit.json.

- https://portal.explainingmarkets.ai/leaderboard?period=2026Q4-CONTEST
- https://portal.explainingmarkets.ai/submissions/s_fb8c124cad37?tab=predictions
- https://portal.explainingmarkets.ai/submissions/s_fb8c124cad37?tab=health
- https://api.explainingmarkets.ai/v1/archive
- https://explainingmarkets.ai/contest-rules
- https://portal.explainingmarkets.ai/docs
- https://raw.githubusercontent.com/explaining-markets/examples/501bd31/src/examples/scoring.py
