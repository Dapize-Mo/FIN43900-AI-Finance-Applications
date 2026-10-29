# Preview retry comparison — Oladapo Olaniyan

October 29, 2026. Frozen exploratory Q4 sample: 32 events; 30 have previews exceeding 8,000 characters. Identical Gemini 3.5 Flash-Lite prompt and facts compared 8,000 vs 16,000 character preview limits. Archived outcomes were not included in prompts.

Original delta R squared: 0.044375. Extended preview: 0.000000. Difference: -0.044375; paired 90% bootstrap interval [-0.21415378112302882, 0.07109522340493112]. Coverage after recovery 32/32; preregistered improvement gate failed. The original model's OLS coefficient on this small sample was negative, so its R squared should not be interpreted as evidence of useful direction. Q4 events were previously explored; results are not independent confirmation and possible model training contamination remains.

Successful-call elapsed time (median / maximum): original 18.9s / 2421.6s; extended 17.4s / 29.2s. Elapsed values include any hidden SDK retry but are not end-to-end webhook timing. Three earlier failed outer requests are retained in the copied log; incomplete events were resumed with one bounded SDK retry. Successful cached calls used the previous no-SDK-retry configuration; reliability comparison is therefore not controlled. No paid billing or live deployment changes were made.

Retain the 8,000-character limit. Reassess future improvements with a new independent sample and real signed round-trip deadline checks if a candidate merits it. Artifacts: validation-plan.json, validate_retry.py, validation-results.json, inferences.jsonl, 2026Q4.jsonl.gz. Source: official Q4 archive and frozen organizer scorer; input and sample provenance are in the prior preview-test-2026-10-29 folder.
