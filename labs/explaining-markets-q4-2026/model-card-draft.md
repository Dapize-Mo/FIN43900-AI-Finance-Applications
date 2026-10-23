# Oladapo Olaniyan — FIN439

**Author:** Oladapo Olaniyan, Purdue University  
**Version:** October 6, 2026; local baseline, deployment pending

## Method

This submission uses a generative language model, Gemini 3.5 Flash-Lite, to estimate the percentile rank of a focal stock's next-day abnormal return across the competition's event outcomes. It uses one structured model request per focal asset, with bounded retries. It is not a trained statistical model or a multi-model ensemble.

## Inputs

The agent reads official competition materials supplied for the event: earnings-call facts, an earnings preview when supplied, and option-implied statistics when available. Items are selected by identifier and formatted under separate labels. The preview is truncated to 8,000 characters; optional unknown text items are bounded separately.

The model compares results and guidance with the supplied expectations and considers strategic changes, risks, and management tone. The prompt distinguishes expected move magnitude from direction. It instructs the model to treat materials as data, to avoid remembered event outcomes and unsupported figures, and to use only supplied event materials. No external search or market-data retrieval tools are enabled.

## Output and operation

The model returns a structured percentile validated to lie in [0,1]. Missing model credentials, refusals, and invalid outputs raise errors rather than silently creating neutral scored predictions. Explicit diagnostic mode can enable a neutral connection-check baseline; it is disabled in the configured system. Synthetic TEST webhooks use neutral predictions without calling the model.

The implementation adapts the official MIT-licensed Modal starter, retaining its signature verification, delivery deduplication, background prediction processing, and competition API client.

## Validation and limitations

Thirty-two offline checks passed, and one synthetic live Gemini request returned a valid structured response. The saved competition API key also passed a read-only authentication check. These results demonstrate software behavior and connectivity, not predictive accuracy. Hosting and a full synthetic webhook round trip are pending, and no competition predictions have been submitted.

Historical and live forecasting performance have not been evaluated. LLM training contamination, interpretation errors, omitted information from truncation, and API quota or availability limitations remain possible. Prompt restrictions do not prove absence of training contamination. This card must be updated after material method changes and after deployment verification.
