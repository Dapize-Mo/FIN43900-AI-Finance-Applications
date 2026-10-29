# Recovery proposal — Oladapo Olaniyan

FIN-43900, October 28, 2026. Target: work toward contest rank 30; no rank guarantee or demonstrated recovery.

## Current evidence

The latest verified board was rank 76/357, delta R² 0.027, 281/290 predictions, through October 27 at 23:45 UTC. Rank 30 had delta R² 0.046 on the same board. This moving threshold is not a forecast of the required final score.

A two-day Modal component-log query returned 153 records: 148 complete pairs and five component failures handled by the surviving-forecast fallback. These counts do not establish predictive accuracy. Modal's visible billing page showed $0.12 used of a $1 limit, $0 in charges, $0.88 credits remaining. No budget, billing, model key or credential settings changed.

## New local candidate tested and rejected

A hashed unigram/bigram TF-IDF ridge model used only official Q3 disclosure text. The first 1,137 chronological eligible events were training data, next 341 development data, and 637 later events formed a holdout excluding all 192 events used in prior model comparisons. The 0.1/1/10 ridge grid was selected on development only. Vocabulary features were hashed deterministically; inverse document frequencies were fitted only on training data. Alpha 10 was selected. The candidate and plan were frozen before evaluation.

Candidate holdout incremental R²: 0.006874. Archived organizer Gemini 2.5 Flash-Lite reference on the same sample: 0.132819. The reference differs from our live Gemini 3.5 strategy. The text candidate is rejected and is not deployment-ready. Its synthetic mathematical sanity check passed, but that does not validate financial performance. No additional provider calls or package installs were made for this experiment. Model arrays remain a research artifact only.

## Concrete proposed recovery mode

Use only the original Gemini prompt at temperature zero, with the existing input formatting, timeout, retries, validated output, signature handling, deduplication, deadline flow, and sanitized audit record. It makes one normal model request per focal asset rather than two. No silent neutral fallback is introduced. TEST events still bypass the provider.

The prior independent 96-event sample favored original-only: 0.154475 versus blend 0.127457 incremental R². Difference for blend minus original: -0.027018, 90% interval [-0.061491, 0.000898]. This remains uncertain and does not satisfy the previously strict statistical rollback criterion. The recommendation is a simpler recovery attempt supported by a favorable fresh point estimate and fewer model calls, not a claim that a statistical gate passed or that the blend caused all rank declines. The older 64-event sample favored the blend, reinforcing uncertainty.

## Prepared, tested, not yet deployed

- EM_STRATEGY defaults to blend. Original-only requires explicit selection at deployment. Unknown values fail clearly before provider calls.
- Full agent suite: 39 passed; one upstream Starlette/AnyIO deprecation warning.
- Hosted ephemeral configuration check: original mode selected, exactly one original-component call, no outlook call, zero actual model-provider calls. Stubs were used to test wiring; this is not a new hosted financial model-accuracy test.
- Live method remains the blend pending explicit production approval. A deployment approval question was presented after these concrete checks.

If approved, deploy the existing Modal app with EM_STRATEGY=original, verify live health reports original-2026-10-28, verify unsigned rejection and signed round trip, and update the public model card. Do not revise past predictions. Original code copies are preserved for rollback; selecting EM_STRATEGY=blend and redeploying returns to the existing blend.

## Files created or modified

Agent base: C:/Users/dolan/Code/school/Fall-2026/FIN-43900/workspace/labs/explaining-markets-q4-2026/agent

- predict.py: explicit selector; default remains blend; original-only audit output.
- modal_app.py: validated deployment-time strategy setting in image environment and health version.
- tests/test_strategy_mode.py: original-only call count and unknown-mode rejection checks.

Research base: C:/Users/dolan/Code/school/Fall-2026/FIN-43900/workspace/labs/explaining-markets-q4-2026/recovery-2026-10-28

- text_model.py and evaluate_text.py: local text candidate and frozen chronological evaluation.
- text-plan.json and text-results.json: immutable plan and evaluation results.
- text-model-research.npz: rejected local model arrays, not deployed.
- predict.py.before-recovery-mode and modal_app.py.before-recovery-mode: exact source backups.
- mode_check.py and mode-check.json: hosted configuration-only verification.
- RECOVERY_PLAN.md: this record.

No new historical forecasts were sent to Gemini, no production forecast method was switched, no spending settings were changed, and no push or new monitor was scheduled during preparation.

## Sources

Accessed October 28, 2026:

- https://portal.explainingmarkets.ai/leaderboard?period=2026Q4-CONTEST
- https://portal.explainingmarkets.ai/submissions/s_fb8c124cad37
- https://modal.com/settings/d-olaniyan06/usage?tab=budgets
- https://explainingmarkets.ai/contest-rules
- Preserved official Q3 archive and pinned scorer in ../improvement-2026-10-23/sources/; their hashes and license remain in source-register.json and LICENSE-examples.txt.
- Prior original-versus-blend result in ../improvement-2026-10-27/results/fresh-metrics.json.


## Approved deployment completed October 28, 2026

The user explicitly approved original-only mode after reviewing this proposal. The mode is now deployed and is the Modal app's persisted deployment default. This supersedes the earlier pending/default-blend preparation status above. Live health, security rejection, hosted synthetic cases and the signed portal round trip passed; the public model card is Published. See ORIGINAL_DEPLOYMENT.md and original-deployment.json. No immediate rank recovery is claimed.
