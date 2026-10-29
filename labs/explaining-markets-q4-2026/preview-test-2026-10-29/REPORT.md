# Preview truncation investigation — Oladapo Olaniyan

October 29, 2026. In the October 28 Q4 archive, 390 of 395 previews exceeded the current 8,000-character cap; median length 11,021 characters. The discarded text contained the word risk in 259 previews and only after the cutoff in 103; valuation occurred only after the cutoff in 150. These keyword counts do not establish that the text is material or improves predictions.

The exploratory Q4 plan selected 32 events; 30 had previews longer than 8,000 characters. The test compared 8,000 and 16,000 character limits with identical model and prompt. It was stopped after 32 completed attempts and 3 failures affecting 3 distinct events. Successful matched pairs: 13; three failures already made the fixed 95% coverage gate unattainable without retries. Median successful response time: 19.4s original, 17.9s extended. The incomplete, non-randomly stopped sample is not a reliable accuracy comparison; no score or improvement is claimed.

Research artifacts: validation-plan.json, validate_preview.py, inferences.jsonl and 2026Q4.jsonl.gz. Calls used official event inputs and free-tier Gemini; no outcomes or credentials were supplied in prompts. The live agent, predictions, and billing were not changed. A new fixed validation with a provider reliability strategy and sufficient coverage is needed before deploying a preview change. The Q4 sample is exploratory and not untouched confirmation data.

Source: official competition Q4 archive, fetched October 28 via https://api.explainingmarkets.ai/v1/archive; competition scorer and code in ../improvement-2026-10-23. Accessed October 29, 2026.
