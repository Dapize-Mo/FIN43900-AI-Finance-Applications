# Explaining Markets — Q4 2026 preparation

**Student / author: Oladapo Olaniyan**  
**Course: FIN-43900 — AI Finance Applications**  
**Prepared / sources accessed: October 6, 2026**

## Authority and current status

Professor announcement supplied by Oladapo: sign up for the competition; prize winners receive an A. The screenshot does not specify further course deliverables or a grading rubric.

User request: work on https://explainingmarkets.ai/.

This document records verified public requirements and a recommended approach. Account registration, eligibility, credentials, hosting, and live predictions are **not verified or completed**. No prior competition package was found in this course workspace. The browser failed to attach during portal inspection.

## Official competition requirements

- Registration deadline: October 11, 2026, 11:59 p.m. Central; October 12, 12:59 a.m. in West Lafayette.
- Scoring: October 12–December 15, 2026.
- Entry: account, completed profile, submission, and platform connection.
- Prize eligibility: qualifying U.S. legal residency, age 18 or older and local age of majority, other exclusions, and an accurate model card. Eligibility remains for the student and organizers to establish.
- One account per person; at most five submissions; at most ten members per submission.
- Predictions must be numeric percentiles in [0,1]. Only the first valid timely prediction counts.
- Respect each event's knowledge_cutoff. Later information is prohibited except event information supplied through official competition APIs.
- Keep records sufficient to support compliance; update the model card after material method changes.

Source: [Official rules, updated September 29](https://explainingmarkets.ai/contest-rules).

## What the model predicts

A percentile describes how an event's next-day market-adjusted return ranks against other events in the scoring period. For example, 0.80 means a relatively strong reaction, not an 80% chance of a positive return.

The frozen scorer fits realized return percentiles using both our prediction and earnings-surprise percentiles. Ranking uses the increase in R-squared over the surprise-only model, with missing predictions filled by the submission's mean valid prediction. Thus the goal is explanatory information beyond the earnings surprise. Constant predictions add zero explanatory value. Historical LLM results may benefit from memorized outcomes, so they cannot establish live performance.

Source: [Frozen scoring implementation, commit 501bd31](https://github.com/explaining-markets/examples/blob/501bd31/src/examples/scoring.py).

## Recommended first approach — proposed, not implemented

Use the official starter's existing event handling and one language model to interpret official earnings facts, preview, and available option statistics. Extract guidance relative to expectations, margins, demand, cash-flow quality, and unusual items; produce a supported percentile. Initially exclude external live searches to simplify cutoff compliance. Evaluate against the starter and a neutral diagnostic baseline before adding complexity.

Alternatives: a statistical model offers lower inference costs but needs feature development; a multi-model ensemble adds cost and should follow evidence of improvement. Model provider, spending limit, hosting, and solo/team choice remain unresolved.

## Setup and validation sequence

1. Confirm whether an account already exists; finish signup and profile through the participant portal.
2. Decide solo/team membership before the registration deadline.
3. Inspect and adapt the official starter in a separate working subfolder, retaining upstream license and attribution.
4. Configure credentials privately; never paste keys into chat or commit them.
5. Run the starter's offline prediction-shape and signature checks. Inspect Q4 material parsing, including absent previews and object-valued option statistics.
6. Evaluate on chronological historical holdouts using the frozen scorer; document historical contamination limits.
7. Publish an accurate model card, connect hosting, and verify a synthetic event round trip before scored events begin.
8. Record event IDs, cutoff/deadline timestamps, model versions, inputs, predictions, and delivery outcomes without storing secrets.

The starter uses a signed webhook, acknowledges promptly, then predicts in the background. Its documented timing is 20 seconds to acknowledge and five minutes afterward to submit; also obey the event's explicit deadline. With no model key, its neutral fallback is useful only for connection testing.

Sources: [Official Modal starter](https://github.com/explaining-markets/starter-modal), [Official example notebooks](https://github.com/explaining-markets/examples).

## Completion check

Completed: course workspace inspection, announcement interpretation, public rules and scoring review, and this setup brief.

Pending: registration, eligibility confirmation, model selection and budget, implementation, validation, model card, and live connection. No predictions or external forms were submitted.
