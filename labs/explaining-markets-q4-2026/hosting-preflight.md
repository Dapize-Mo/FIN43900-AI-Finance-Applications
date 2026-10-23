# Hosting preflight — October 6, 2026

**Author: Oladapo Olaniyan — FIN-43900**

The local Gemini, competition API-key, and signing-secret fields are populated. Their values were not included in this report. Restored `GEMINI_MODEL=gemini-3.5-flash-lite` in `agent/.env` after its setting reverted to the unsupported older model.

Read-only production competition credential check: `GET https://api.explainingmarkets.ai/v1/events` returned HTTP 403 with `INVALID_API_KEY`. A populated field does not establish working authentication. The portal's one-time credential dialog remains open, enabling the student to copy the correct lines into `.env` before dismissing it.

No Modal local authentication configuration was found. Opened https://modal.com/login?next=/apps for the student to sign in or create an account. No deployment or secret upload was performed.

Hosting source review, accessed October 6, 2026:

- [Modal pricing](https://modal.com/pricing): Starter has $30 monthly compute credits and usage-based charges beyond covered usage.
- [Modal budgets](https://modal.com/docs/guide/budgets): workspace budgets cap usage before credits; spend limits cap net charges. A zero out-of-pocket spend limit should be verified before deploying this zero-budget project.

Pending: correct API credential, authenticate hosting, verify zero-spend controls, authorize secret upload to the hosting destination, deploy, set webhook, test the round trip, and publish an accurate model card.
