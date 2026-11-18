# Portal diagnosis and cohort check — Oladapo Olaniyan
Read-only; portal pages accessed Nov 5, 2026 ~10:30 PM America/Indianapolis (scored data as of 6:45 PM). Nothing submitted, edited or deployed.
Source: https://portal.explainingmarkets.ai/submissions/s_fb8c124cad37 (?tab=health, ?tab=predictions)

## Health (rolling 24h)
Webhook 2XX 403; 4XX 0; 5XX 0; timeouts 1; consecutive failures 0. Inbound predictions 399; duplicates 0, late 0, early 0, invalid 0.
403 deliveries vs 399 predictions: the 4-row gap is not explained by the page (TEST events, retried deliveries, or failed predictions all possible).

## Predictions tab (Q4 2026): 1,808 rows
Scored 1,302 | Awaiting outcome 472 | Missing Data 27 | Excluded 7.
- 26 of 27 Missing Data rows are dated Oct 14 or later (the 27th, ODC on Oct 9, predates the Oct 12 scoring start). All 27 have a submitted prediction and a realized CAR1; SURPRISE is blank. This matches the 26-event shortfall numerically, and points to a missing earnings-surprise value, not delivery failure. The portal does not state the rule.
- 7 Excluded rows (Oct 13: WFC, GS, FBK, JPM, JNJ, DPZ, ACI): prediction submitted, no outcome shown; reason not displayed.
- 10 events in the Oct 28 archive have NO row in the predictions table: Oct 16 MTB, LADR; Oct 22 DGX, TTMI, URI, MEDP, TRST, LUV, FAF, R. Cause unknown (never delivered, failed in Modal, or not shown). Not visible in Health (24h only). Need Modal logs for Oct 15-16 and Oct 21-22.

## Cohorts (approximate: portal 2-decimal actuals; surprise percentile ranked among own scored rows)
All Oct 13-Nov 4: n=1286, dR2 0.0676 (matches the published 0.0669-0.0672 snapshot).
| Cohort (event date) | n | dR2 | 90% CI |
| Pre-blend Oct 13-23 | 270 | 0.036 | [0.008, 0.079] |
| Blend Oct 26-28 | 296 | 0.033 | [0.007, 0.078] |
| Transition Oct 29 (deployment boundary) | 256 | 0.114 | [0.054, 0.182] |
| Original-only, clean Oct 30-Nov 4 | 464 | 0.081 | [0.044, 0.130] |
Original-only minus pre-Oct-29: +0.047 (event bootstrap 90% [0.000, 0.098]; day-clustered [-0.009, 0.098]). Not established. Daily dR2 ranges 0.009-0.194.
Caveats: different events and market days, no randomization, single-sample dR2 intervals lean positive, Oct 29 delivery times straddle the deploy, and the 3.1 fallback timing is unrecorded.

## CORRECTION — Nov 6, 2026 (Modal logs read; supersedes the "26 Missing Data" inference above)
Modal app explaining-markets-starter logs (Oct 15-Nov 6), read-only. Search "ERROR" returned 33 "[ERROR] prediction failed" lines, Oct 16-Nov 5:
24 Gemini 503 "high demand", 4 "Request timed out", 5 "Both Gemini blend components failed" (Oct 28, blend era). No other ERROR types.
32 of the 33 events have NO row in the portal Predictions tab (HAS recovered; it has a scored Oct 20 row).
- Oct 16: MTB, LADR (503). Oct 22: URI, DGX, TTMI, LUV, FAF (503); TRST, MEDP, R (timeout).
- Oct 28 (blend): UE, EAT, RDWR, CSTM, AAT. Oct 29 (original-only, before fallback): FTRE, FTAI, CLMB, LKQ, ENTG, PBI, PLXS, HSY, MO, FTI, HWM, EHC (503).
- After the fallback went live (card dated Oct 29): SMRT (Nov 4, 503), CELH, CRAI, WES (Nov 5, 503), SHOO (Nov 5, timeout).
Every failure was AFTER a 200 OK webhook ACK, so the platform did not redeliver. These are model/API failures, not delivery failures.
27 lost events fall on Oct 16-Oct 29, close to the leaderboard's 26-event shortfall. The pinned scorer's common sample requires a surprise value,
so the Missing Data rows (blank surprise) are most likely OUTSIDE the common sample and NOT the shortfall. Exact membership is not shown by the portal.
Fallback usage: "[WARN] primary model unavailable; trying gemini-3.1-flash-lite" 39 times (Nov 3: 3, Nov 4: 3, Nov 5: 33). It rescues most 503s, but not all, and timeouts never trigger it.
The log view may cap results; counts are as displayed.
