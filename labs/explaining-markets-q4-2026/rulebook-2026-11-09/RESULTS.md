# Error mining on live forecasts — Oladapo Olaniyan, FIN-43900 (Nov 9, 2026)
Research only. Nothing deployed or changed live.

Data: official Q4 archive refreshed Nov 9 (2,104 events through Nov 6; source.json) joined by ticker to 1,642 live forecasts read from the
portal Predictions tab (Oct 28-Nov 6; checksum n=1642, sum=92674). 1,599 rows have forecast, outcome and surprise. Official scorer labels.

Live agent, Oct 28-Nov 6: delta R^2 0.088 (organizer Gemini 2.5 Flash-Lite reference on the same rows: 0.061).
Forecast vs outcome is roughly linear; the top bucket is flatter (forecasts 0.75-0.83 realized 0.57 on average).

Tested on Nov 3-6 (n=1,042), each day predicted with coefficients fit only on earlier, already-realized events:
| Variant | delta R^2 | vs raw 0.0923 | 90% CI of difference |
| Isotonic recalibration | 0.0844 | -0.008 | [-0.017, +0.001] |
| Ridge hybrid, all features (alpha 100 / 1000) | 0.087 / 0.068 | -0.006 / -0.025 | includes 0 / below 0 |
| Ridge hybrid, small set (alpha 100) | 0.096 | +0.004 | [-0.013, +0.020] |
| Forecast + preview tone (p_net) | 0.1093 | +0.017 | [+0.010, +0.025], positive on all 4 days |
| Forecast + YTD return + preview tone | 0.1089 | +0.017 | [+0.002, +0.031] |
| Forecast + YTD return only | 0.0964 | +0.004 | [-0.009, +0.018] |
Preview tone = (positive words - cautious words) per 1,000 characters of the pre-release research note. Its coefficient is negative:
an upbeat preview goes with a weaker reaction than the agent forecasts (expectations already priced in).

Cautions: about a dozen variants were tried on the same four test days, so the best one is flattered. Day-level variation is large.
Features were first ranked using all rows, then re-ranked on Oct 28-Nov 2 only (preview tone and YTD were top in both).
frozen-adjustment.json fixes one formula (fit on all 1,599 rows) for an untouched check on events from Nov 9 onward.
Files: load.py, preds_a/b/c.txt, 2026Q4.jsonl.gz, source.json, frozen-adjustment.json, LIMITS.md, fetch_q4.py.

## Clean check — Nov 12, 2026 (frozen formula, unseen events)
Archive refreshed Nov 12 (2,397 events through Nov 11). Forecasts for Nov 9-11 read from the portal (checksum n=298, sum=15418).
286 archive events on Nov 9-11, all 286 with a live forecast; 267 with outcome and surprise.
Raw forecast delta R^2 0.1915 (90% CI [0.128, 0.264]); frozen adjustment 0.1963; difference +0.0048, 90% CI [-0.022, +0.032].
By day (raw -> adjusted): Nov 9 0.241 -> 0.230; Nov 10 0.133 -> 0.144; Nov 11 0.406 -> 0.411 (n=25).
Verdict: not confirmed. The gain seen on Nov 3-6 (+0.017) did not reproduce at a detectable size. No deployment recommended.
Labels are quarter-wide ranks from the Nov 12 archive; portal scoring for these dates was still pending.
