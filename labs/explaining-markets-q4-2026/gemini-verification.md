# Gemini verification — October 6, 2026

**Student / author: Oladapo Olaniyan — FIN-43900**

Verified privately that `agent/.env` contains a Gemini API key. No key value was displayed. AI Studio shows the newly created competition project on Free tier. Competition API and signing-secret fields remain blank.

Live connection results:

- `gemini-2.5-flash`: Google returned HTTP 404, explicitly stating this model is no longer available to new users.
- `gemini-3.8-flash`: Google returned HTTP 503 for temporary high demand.
- `gemini-3.5-flash-lite`: successfully returned a structured percentile of **0.5** for a synthetic company with in-line revenue and unchanged guidance. This demonstrates connectivity and structured-output handling, not predictive accuracy.

Saved `gemini-3.5-flash-lite` as the configured model in `agent/.env`, `agent/.env.example`, `agent/predict.py`, and `agent/tests/test_gemini.py`. No credentials were changed. This record supersedes the older setup document's default-model statement and claim that no live Gemini inference had been tested.

Validation after the model update: **32 tests passed**, one upstream test-client deprecation warning; `git diff --check` passed.

Current status: Gemini is connected locally. The competition entry is not receiving events; hosting, competition credentials, synthetic webhook verification, and public model card remain pending. No competition predictions have been submitted.

Sources accessed October 6, 2026: [Gemini pricing](https://ai.google.dev/gemini-api/docs/pricing), Google API model-list and inference responses, signed-in Google AI Studio, and the competition portal. Free-tier quota sufficiency and live event throughput remain unverified.
