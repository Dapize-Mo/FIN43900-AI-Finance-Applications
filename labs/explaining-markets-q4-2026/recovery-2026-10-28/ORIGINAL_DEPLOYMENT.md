# Original-only deployment — Oladapo Olaniyan

October 28, 2026. The user explicitly selected "Deploy original-only mode" after reviewing the historical uncertainty. Deployed to the existing explaining-markets-starter Modal app, endpoint https://d-olaniyan06--explaining-markets.modal.run/.

The current mode uses the original Gemini 3.5 Flash-Lite prompt at temperature zero: one normal provider request per focal asset, with the existing bounded retries. It preserves official material formatting, signature verification, deduplication, deadline flow and sanitized forecast audit output. Model credentials, spending controls and past predictions were not changed. Halving normal requests is not a guarantee of rank improvement.

The deployment default in agent/modal_app.py is now original. The EM_STRATEGY environment setting can explicitly select original or blend; unsupported values fail. Local standalone predict.py without a deployment setting retains its safe blend default, while the Modal image explicitly sets the deployed mode. No private environment file was modified.

## Verification

- All 39 agent tests passed; one upstream Starlette/AnyIO deprecation warning.
- Hosted original-only synthetic pipeline cases returned positive 0.95, neutral 0.50, negative 0.05; each under one second in this check. These test outputs are not evidence of financial accuracy.
- Portal verified the signed round trip at 7:28:13 PM America/Indianapolis.
- The public model card was updated and the portal confirmed Published.
- After persisting the approved default and redeploying, live health reported original-2026-10-28; unsigned requests returned 401.

Evidence: hosted-original-check.json and original-deployment.json. The prior mode wiring check used stubs and zero provider calls; this later synthetic check used three actual provider calls without submitting scored forecasts.

## Rollback

Set EM_STRATEGY=blend when deploying the existing agent/modal_app.py to return to the blend. Preserve the current original-only source and record any new deployment. Exact pre-selector source backups remain in this recovery folder. The public model card must be updated if the live method changes again.

## Files and remote changes

Earlier preparation modified agent/predict.py, agent/modal_app.py and added agent/tests/test_strategy_mode.py. This deployment changed agent/modal_app.py's default from blend to original. New local records: hosted-original-check.json, original-deployment.json, ORIGINAL_DEPLOYMENT.md; RECOVERY_PLAN.md has a dated deployment addendum. Research files and the rejected text model are listed in RECOVERY_PLAN.md. The existing public model card was modified remotely. No push or recurring automation was created.
