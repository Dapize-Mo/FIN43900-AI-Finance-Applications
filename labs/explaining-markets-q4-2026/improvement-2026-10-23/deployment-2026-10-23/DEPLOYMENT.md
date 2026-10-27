# Blend deployment — Oladapo Olaniyan

October 23, 2026. The user explicitly requested deployment after being informed that the historical uncertainty interval included a loss. This is a user-authorized experimental deployment, not a claim that the validation gate passed.

## Behavior

Two independent Gemini 3.5 Flash-Lite calls at temperature zero run concurrently: the existing prompt and the frozen outlook prompt. The normal prediction is their equal-weight average. If one call fails validation or encounters a provider failure, use the surviving valid forecast; if both fail, report failure rather than silently submit neutral. No credential/billing/budget settings changed. Normal model requests per event increase from one to two, so free-tier quota use can increase. TEST events continue to bypass the model and submit neutral diagnostics.

## Verified

- Agent test suite: 36 passed; one upstream Starlette/AnyIO deprecation warning.
- Hosted synthetic cases: positive 0.925, neutral 0.500, negative 0.010; each under two seconds in this check.
- Modal deploy completed for the existing `explaining-markets-starter` app.
- Live endpoint returned `strategy: blend-2026-10-23` and health OK.
- Unsigned webhook returned HTTP 401.
- Existing public model card updated for the blend and historical uncertainty; portal confirmed Published.
- Signed portal round-trip: portal confirmed "Full round trip verified at 7:37:35 PM" on October 23, 2026.

Endpoint: https://d-olaniyan06--explaining-markets.modal.run/
Deployment: https://modal.com/apps/d-olaniyan06/main/deployed/explaining-markets-starter
Submission: https://portal.explainingmarkets.ai/submissions/s_fb8c124cad37

## Rollback

Preserved `predict.py.before-blend` and `modal_app.py.before-blend` are exact pre-deployment source copies. To roll back, restore those two files into the sibling agent folder and redeploy its modal_app.py with the course Python interpreter. No reset of the persistent deduplication store is needed. Test-file backups are also preserved. No prior competition predictions were modified.

## Changed files

Agent directory: C:/Users/dolan/Code/school/Fall-2026/FIN-43900/workspace/labs/explaining-markets-q4-2026/agent

- predict.py: concurrent blending, fallback, temperature matching validation.
- outlook_strategy.py: frozen outlook prompt/schema, deployment description only adjusted.
- modal_app.py: bundle outlook module and expose version in health response.
- tests/test_blend.py: new blending, concurrency and fallback tests.
- tests/test_gemini.py: preserve existing checks at original component boundary.
- tests/test_modal_app.py: replace removed SDK get_raw_f interface with supported local execution; check async behavior directly.

This report folder contains the four original source/test backups, hosted-check.json, endpoint-check.json and DEPLOYMENT.md. The parent research REPORT.md also records this later user-authorized decision. No secrets are included in these records.
