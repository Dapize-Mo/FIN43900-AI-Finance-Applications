# Deployment checkout — October 6, 2026

**Student / author: Oladapo Olaniyan — FIN-43900**

## Verified outcome

- Submission: **Oladapo Olaniyan — FIN439**, `s_fb8c124cad37`.
- Local Modal client authenticated to workspace `d-olaniyan06`; login configuration saved to `C:/Users/dolan/.modal.toml` by Modal's standard authorization flow.
- Agent deployed: https://modal.com/apps/d-olaniyan06/main/deployed/explaining-markets-starter.
- HTTPS endpoint: https://d-olaniyan06--explaining-markets.modal.run/.
- Portal endpoint saved and submission displayed **Live / Receiving events**.
- Portal synthetic test confirmed **Full round trip verified** at 1:53:47 p.m. Indiana time: signed event delivery, endpoint HTTP 200, and test prediction submitted.
- Separate hosted synthetic Gemini inference returned a valid percentile of **0.5**, using Gemini 3.5 Flash-Lite. This tests the actual cloud dependency environment and secrets, rather than only the TEST webhook's neutral response path.
- Accurate model card published: https://portal.explainingmarkets.ai/models/s_fb8c124cad37.

## Validation and limits

Previously: 32 offline tests passed, competition API credential verified with HTTP 200, and local synthetic Gemini inference succeeded. Final source compilation and diff whitespace checks passed before deployment.

The first deployment attempt hit Windows console encoding; UTF-8 output resolved it. The separate smoke-check script initially failed remote imports; serialized-function mode resolved the issue. The deployed production handler was not modified by these smoke-check fixes.

User approved deployment and storage of the Gemini API key, competition API key, and signing secret in Modal. No key values are included in this document. No payment method was added. The last confirmed Modal workspace usage limit was $1. This may be insufficient for the full quarter; continued operation is not guaranteed beyond the credit allowance or API quotas.

These tests establish connectivity, not forecasting performance or prize eligibility. No scored competition prediction was intentionally submitted. Historical holdout evaluation and live scoring results remain future work.

## Files created this deployment session

- `agent/cloud_check.py`: reproducible synthetic hosted-model check; sends no competition predictions.
- `model-card.md`: final published model-card source, preserving the earlier draft.
- `deployment-checkout.md`: this verification record.

Hosted secrets and the new Modal login configuration were also created through the approved deployment and authorization flows. The competition portal webhook and public model card were updated. Earlier status reports are superseded by this checkout for deployment and connection state.
