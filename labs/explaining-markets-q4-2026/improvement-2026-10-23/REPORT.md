# Historical improvement comparison

**Oladapo Olaniyan — FIN-43900 — October 23, 2026**

## Decision

Keep the live strategy unchanged. The revised prompt and equal-weight blend are research candidates only. The blend improved the 64-event holdout point estimate, but failed the preregistered uncertainty gate. No deployment, public model-card change, retrospective prediction revision, billing change, or account change was made.

## Results

The figures below are historical sample incremental R² controlling for earnings-surprise percentile, calculated with the organizer's pinned scorer. They are not live leaderboard scores or projected ranks.

| Method | Development: 32 events | Holdout: 64 events |
|---|---:|---:|
| current | 0.004411 | 0.145358 |
| outlook | 0.000975 | 0.162071 |
| blend | 0.002509 | 0.165916 |

The development rule selected the blend among the two alternatives. Neither alternative beat the current prompt on development. The selected blend's holdout gain was **0.020559**. Its paired event-bootstrap 90% interval was **[-0.015809, 0.061457]**. This includes a loss. All **192 of 192** event-method responses succeeded after bounded retries.

The fixed deployment gate required a gain of at least 0.01, a bootstrap 90% lower bound above zero, and at least 95% inference coverage. **Gate failed.** A favorable point estimate alone does not justify replacing the live agent.

## What was tested

The current prompt emphasizes quantitative earnings surprises first. The candidate emphasizes unexpected forward guidance, recurring demand, margin quality, cash conversion and conflicting evidence. A blend averages the two forecasts. Both methods used Gemini 3.5 Flash-Lite at temperature zero; the deployed agent currently leaves temperature at the provider default, so this is a controlled prompt comparison rather than an exact replay of live behavior.

A fixed random seed selected 32 earlier Q3 events for development and 64 later Q3 events for holdout. Prompts, schema, event selection, selection rule and deployment gate were frozen before model requests. Only official disclosure facts, previews and available option statistics entered prompts. Outcomes, earnings-surprise labels, archived reference forecasts and competition credentials were excluded. The Gemini key was used only for authentication.

`scoring-correction.md` records a pre-decision correction: quarter-wide outcome and surprise percentile labels are fixed before sample selection and remain fixed during bootstrap resampling. The earlier running evaluator used within-sample ranks; its output was superseded by the corrected final `results/metrics.json`. All three temporarily failed requests were retried successfully before the corrected result was calculated.

## Live audit

The dated October 22 contest snapshot was 35/353, with incremental R² 0.089; tenth place was 0.115. These are dated observations, not a refreshed rank claim. Among 114 scored contest forecasts, 88 were above 0.5, with an average forecast of 0.596 versus average realized percentile 0.497. Frequent repeated values suggest limited differentiation, but a uniform affine shift or rescaling cannot improve the OLS incremental R² metric.

The October 23 health check showed 55 successful deliveries and 55 predictions over the preceding 24 hours, with no reported delivery errors or late, duplicate, or invalid predictions. This supports prioritizing signal quality over infrastructure changes. Existing Gemini free-tier use and Modal budget settings were preserved.

## Validation and limits

Four local checks passed: model-input label exclusion, reproducible disjoint chronological samples, affine-score invariance, and bootstrap mapping to fixed quarterly labels. Requests were paced after free-tier rate limiting; successful responses were cached.

The sample is small and the bootstrap interval is wide. Historical LLM training contamination cannot be ruled out. The official archive may differ from the exact original webhook bundle or later revisions; this is not a point-in-time production replay. This sample's absolute R² is not directly comparable with the current contest's score, and scores do not translate into a guaranteed rank. October errors informed the hypothesis, so Q4 was not treated as untouched validation. The holdout has now been examined and must not be repeatedly reused to tune another candidate.

## Next research step

Retain this candidate for a prospective shadow comparison or a new, untouched historical sample with a separately frozen plan. No recurring shadow model calls or extra data transfers have been scheduled or enabled. Require new independent evidence before a live switch. Keep monitoring normal delivery coverage; existing forecasts cannot be improved retroactively.

## Sources

Accessed October 23, 2026:

- Official competition rules: https://explainingmarkets.ai/contest-rules
- Authenticated archive manifest: https://api.explainingmarkets.ai/v1/archive (signed download links deliberately not retained in this report).
- Frozen organizer scorer: https://raw.githubusercontent.com/explaining-markets/examples/501bd31/src/examples/scoring.py
- Scorer license: https://raw.githubusercontent.com/explaining-markets/examples/501bd31/LICENSE
- User prediction audit: https://portal.explainingmarkets.ai/submissions/s_fb8c124cad37?tab=predictions
- Dated contest leaderboard: https://portal.explainingmarkets.ai/leaderboard?period=2026Q4-CONTEST
- Authenticated delivery health: https://api.explainingmarkets.ai/v1/health

See `sources/source-register.json` for archive/scorer hashes and access metadata. The scorer's MIT license is retained beside the source.

## Files created or modified in this research session

All paths below are relative to this report's folder:

- `candidate.py`: research-only prompt and structured response schema.
- `evaluate.py`: inference collection, caching, scoring, selection and bootstrap gate; corrected full-quarter targets and pacing.
- `test_research.py`: four validity checks.
- `evaluation-plan.json`: frozen candidate hash, event identifiers and decision rules.
- `scoring-correction.md`: scoring correction record.
- `sources/EARNINGS_RELEASE_2026Q3.jsonl.gz` and `sources/EARNINGS_RELEASE_2026Q4.jsonl.gz`: preserved official archives.
- `sources/scoring_frozen.py`, `sources/LICENSE-examples.txt`, `sources/source-register.json`: pinned official scoring source, license and provenance.
- `results/inferences.jsonl`: cached model responses and sanitized error metadata.
- `results/metrics.json`: final corrected comparison.
- `results/live-audit.json`: dated live prediction and health observations.
- `results/archive-baseline-audit.json`: organizer reference-model analysis; not our live forecasts.
- `REPORT.md`: this report.

Python/pytest may also have produced ordinary local cache files in this Code workspace. Production files under the sibling `agent` folder were not modified.


## Subsequent user-authorized deployment — October 23, 2026

After receiving the failed-gate result, the user explicitly asked to deploy the tested approach. The equal-weight blend was deployed to the existing Modal app. This later instruction overrides the earlier keep-live-unchanged decision; the uncertainty and failed historical gate remain unchanged. See `deployment-2026-10-23/DEPLOYMENT.md` for live verification, rollback copies, request-volume implications and the complete changed-file list.
