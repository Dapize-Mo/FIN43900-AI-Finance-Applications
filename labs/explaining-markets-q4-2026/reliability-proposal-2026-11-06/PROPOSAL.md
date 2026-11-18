# Deadline-aware retry proposal — Oladapo Olaniyan, FIN-43900
Status: TESTED LOCALLY, NOT APPLIED, NOT DEPLOYED. Nothing in agent/ was changed (git status clean; `git apply --check` passes).

## Problem (from Modal logs, Oct 16-Nov 5)
32 delivered events got no prediction: 503 high-demand errors and request timeouts. The webhook was already ACKed, so there was no redelivery.
503s failed 5-60 s after receipt, with about 4 minutes of the 5-minute budget unused. Timeouts never reached the 3.1 fallback.
Nov 5 alone logged 33 fallback attempts and 4 losses.

## Change (predict.py only; prompt, model, temperature, inputs and the success path are unchanged)
- Transient = HTTP 429/500/502/503/504, timeout or connection errors. Non-transient errors (401, 400, refusals) still fail at once.
- On a transient error: alternate 3.5 Flash-Lite and 3.1 Flash-Lite with backoff of 0, 5, 10, 20, 30 s.
  Each attempt has timeout min(45 s, time left) and no hidden SDK retries.
- The budget comes from the event's prediction_deadline, keeping 25 s for submission. No request starts with under 10 s left.
- Still no neutral/constant fallback. A missing forecast is mean-imputed by the scorer, so a 0.5 placeholder would add nothing.

## Evidence
- Baseline agent suite in an isolated copy: 41 passed. After the change: 48 passed (7 new tests in test_deadline_retry.py:
  timeout->fallback, repeated 503 recovery, 429, outage stops before deadline, no call without time, non-transient not retried,
  and predict() passing the event deadline).
- Real OpenAI SDK 3.46: with_options(timeout, max_retries) works, and the exception names match.
- NOT tested: live provider behavior during an outage, a hosted signed round trip, or end-to-end timing on Modal.
- Expected effect: fewer lost forecasts. It cannot be quantified from the logs, and the score effect is likely small (about 2% coverage). No rank claim.
- More forecasts may come from 3.1 Flash-Lite, whose forecast quality has not been evaluated historically.

## Before any deploy (requires your explicit approval)
1. Apply: `git apply ../reliability-proposal-2026-11-06/predict-deadline-retry.patch`, and copy test_deadline_retry.py into agent/tests/.
2. Run the full suite; deploy with EM_STRATEGY=original; check health and the 401 on an unsigned request; run the portal signed test.
3. Update the model card's fallback sentence (it currently says the fallback runs only after a primary 503) and record the deployment in CHANGELOG.
