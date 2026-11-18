# No-generative-AI candidate and diagnosis status — Oladapo Olaniyan
FIN-43900, November 5, 2026. Research only: nothing deployed, committed, pushed, or changed live.

## Candidate
Deterministic features from the official bundle only (facts lexicon/guidance/vs-expectation counts, parsed revenue growth;
preview-parsed price position, market cap, beta, YTD, consensus growth; option IV/move/skew) -> ridge or shallow GBM.
No LLM, no paid API. Walk-forward: each test week is predicted by a model fit only on events realized (+2 days) before that
week's first knowledge cutoff; training target is the within-training-window rank of car1. Scoring: pinned official scorer
(delta R^2, imputed family), quarter-wide labels. Dev = Q3 before Aug 16 (grid of 12; chose facts-only ridge alpha 3000,
dev 0.033; options+preview ~0.001). Frozen in plan.json (code hashes) before any test period was scored.

## Frozen test results (delta R^2)
| Test | n | Candidate | Organizer Gemini 2.5 Flash-Lite reference (same rows) | Cand - ref (90% CI, event / day-clustered) |
|---|---|---|---|---|
| A: Q3 Aug 17-Sep 30 | 262 | 0.0110 | 0.0658 | -0.055 [-0.096,-0.020] / [-0.095,-0.019] |
| B: Q4 Oct 1-27 | 413 | 0.0064 | 0.0203 | -0.014 [-0.037,+0.002] / [-0.052,-0.000] |
Overlap with cached live-style original (Gemini 3.5 Flash-Lite, T=0): A n=47: 0.009 vs 0.101; B n=32: 0.002 vs 0.044 (intervals include 0; too small to conclude).
Coverage 100% of scoreable events; cost $0; inference ms.
Exploratory post-freeze variants (not selections): all features 0.011 / 0.007; options+preview ridge300 0.009 / 0.0004.
Bootstrap intervals for a single delta R^2 are biased away from zero (delta R^2 is non-negative in sample); use the paired differences.

## Limits
Reference is the organizer's 2.5 model, not the live 3.5 agent; live Q4 predictions and post-Oct-28 outcomes were not available.
Q4 labels rank only events through Oct 27, not the contest scoring period. Walk-forward weeks reuse test data only after realization.

## Diagnosis status
Portal (Health, Predictions) required sign-in in both browsers; not accessed. Modal logs not accessed. See chat for the exact items needed.

Files: em_features.py, common.py, run_dev.py, run_test.py, plan.json, test-results.json, REPORT.md.
