# Working validation and AI-use record

**Recording-support page refreshed October 17, 2026 for Oladapo Olaniyan.** The earlier version shown in the recording is preserved in `recorded-page-snapshots/03-validation-and-ai-use.md`. This refresh does not change the video.

Current full source: [validation-and-ai-use-v3.md](../../docs/validation-and-ai-use-v3.md).

Analyst: Oladapo Olaniyan. Interaction/access dates 2026-10-06 and 2026-10-15. Working source; no final frozen submission or student attestation. One locked changed-input test is complete as recorded below.

**October 17 recording update:** Three actual recordings and audio-compared transcript drafts now exist. [Recording clarifications](../../docs/recording-clarifications-20261017.md) reconcile the old validation page shown in Video 1 with this current executed record, document the reported TA resolution, and distinguish Video 3's narration from sampled visual evidence. [The audio check](../../docs/audio-check/recording-check-report.md) records local machine transcription, frame samples, revised approximate topic times, and remaining wording uncertainty. Earlier PDF versions require content-equivalent refresh before final freeze.

## Evidence boundary

Market date2026-10-05 close. Annual accounts FY2025 ended2025-12-27; interim bridge2026-06-13 and point shares2026-07-02. USD millions/shares millions; USD per share. Annual comparative statements are consolidated GAAP. Normalization, forecasts and book/fair-value proxies are distinguished in the source register and assumption challenges. No post-quarter cash/debt/share rollforward is claimed. Direct SEC downloads returned403; browsed SEC text was used and failed retrieval logs retained. Captured market/course/Treasury snapshots have hashes. No credentials required for model run.

## Executed ordinary checks

`outputs/final-working-run/checks.csv`: 42 PASS, zero FAIL, five OPEN, two QUALIFIED. PASS means the described executable calculation ran, not that every financial assumption is verified. Historical IS/BS/cash articulation; restricted-cash distinction; 20 forecast rows; FCFF financing reconciliation; independent Decimal EV-to-equity bridges; WACC/g directional and invalid-boundary checks; zero-value case; remaining-year stub timing; 12 published synthetic known answers; terminal reinvestment arithmetic; numerical reverse DCF residual; causal downside; deliberate copied-ledger cash corruption detection. These are AI-assisted ordinary checks. The separately recorded October 15 changed-input test appears below; it is not asserted by this older static check output.

Independent source/definition checks: normalized EBIT11,498+1,993=13,491; capex4,415 ties CF and Note1; cash/restricted difference45; CFO minus capex7,672 ties algebra after tax/nonoperating/CFO adjustments. Cash-flow operating-WC increase1,212 vs broad BS change410 remains802 unresolved, not silently equated. Peer arithmetic uses common price date and annual GAAP denominators but fair value/leases/claim/share-age closure remains QUALIFIED. Independent source check means separate primary evidence, not a second AI vote.

Highest-risk failure: mechanically balanced statements could conceal cash funding errors/double-counted FCFF. Synthetic corruption of copied closing cash by100 USDm produced a detected articulation discrepancy; source inputs and delivered forecast not changed. Forecast FCFF reconciles from CFO after after-tax financing/nonoperating effects; D&A embedded in EBIT expenses is added once to cash flow. This checks technical propagation, not economic forecasts.

Known failures preserved: original course `.venv/Scripts/python.exe` could not launch (“file cannot be accessed”); bundled Python used successfully. Sandbox DNS blocked initial downloads; later generic user-agent retrieval succeeded for market/course/Treasury, SEC403 remained. Browser body capture initially timed out; fresh tab yielded full live instructions. Initial model terminal growth policy was replaced by explicit reinvestment; initial results remain in `outputs/initial-run/`. See cold-run evidence JSON for actual fresh-environment outcome; do not infer it from this narrative.

## Material AI uses and dispositions

Tool: Codex desktop coding assistant, exposed system identity GPT-6; finer model/build/version not available, not invented. Browser automation, web search/read, local Python calculation and ReportLab artifact generation were used in the2026-10-06 interaction. The browser/web tools retrieved sources; finance reasoning/code/drafts were AI-assisted.

| Material use | Output / location | Independent check | Working disposition | Student judgment |
|---|---|---|---|---|
| Lab audit and instructions | continuation-audit.md | Live Brightspace, original lab files and current course architecture | Retain traceable findings; unavailableA stays unavailable | blank |
| SEC extraction/base normalization | filing-inputs.json, source-register-v2.csv | Source line arithmetic; impairment and capex notes | Arithmetic accepted by executed checks; normalization economics qualified | blank |
| Five-year forecast and FCFF/WACC code | model.py/checks.py | 12-metric known answer, statement and cash/bridge checks | Technically runs; assumptions not approved | blank |
| Terminal reinvestment correction | terminalNOPAT*g/ROIC; initial vs verified outputs | Identity and monotonicity checks | Replace mechanical growth in current model; ROIC qualified | blank |
| Scenarios, beta/ERP/spread and peer policy | assumptions.json, peer-policy.md | Sources distinguish guidance from assumptions; qualified peer calculations | Proposed, not observed facts or human ownership | blank |
| Committee memo/research/video outline | docs/*working* and video-preparation.md | Outputs/date consistency; PDF size/layout review | Draft only; personal sections blank | blank |
| AI capital-spending mismatch implication | CF vs segment Note1 | Both primary lines4,415 | Corrected/rejected mismatch implication | blank |

No fabricated no-AI attestation, personal experience, partner review, completed recording/transcript or staff guidance. This table records AI assistance rather than claiming Oladapo Olaniyan endorsed it. Final Validation-and-AI-Use.pdf must be content-equivalent to repository record at freeze.

## Locked Changed-Input Record — completed October 15, 2026

Oladapo Olaniyan directly confirmed that the professor described the posted “AI-off” instruction as a typo during class and said AI use could count. This record is therefore AI-assisted. The original Brightspace wording is retained in course-source records; no written revision is claimed here.

| Required field | Recorded evidence |
|---|---|
| Prediction frozen before run | Lower terminal ROIC would require more reinvestment for the same growth, lowering terminal FCFF, terminal value, and value per share. Draft watch/defer expected to remain unchanged. |
| Exact material input | Terminal incremental ROIC |
| Old → new value and units | 15.0% → 12.0% annual terminal incremental ROIC |
| Timestamp and frozen baseline | 2026-10-15 5:22 p.m. CDT; `repro/locked-change-20261015T1722CDT/frozen-baseline/` |
| Separate execution evidence | `repro/locked-change-20261015T1722CDT/experiment-run/outputs/after-change/`; copied run exited 0 |
| Before → after outputs | Reinvestment $2,270.1M → $2,837.6M; terminal FCFF $11,350.3M → $10,782.8M; EV $200,935.6M → $192,886.3M; value/share $117.29 → $111.41 |
| Actual direction and decision effect | Prediction matched. Value/share fell $5.88 (5.02%); fixed draft action remained watch/defer. |
| Reconciliation | No calculation failure. The action label is fixed rather than threshold-driven; the dedicated test report explains why it did not change. |

Full record: `validation-and-ai-use-working.md` and `repro/locked-change-20261015T1722CDT/locked-test-report.md`.

Edition A recovery, actual fresh-eyes challenge, student final recommendation, peer/bridge/stub/ROIC acceptance, recordings/transcripts, hosted/access-checked repository/videos and final package freeze remain incomplete. No submission/contact/push/deployment occurred.


## Final continuation run and draft correction

Analyst: Oladapo Olaniyan. Final working model produced42 PASS,0 FAIL,5 OPEN,2 QUALIFIED. Fresh no-pip environment run `repro/cold-20261006T053603935700Z/cold-run-evidence.json` exited0 with no stderr and exact SHA256 matches for results.json, statements, sensitivity, checks and peer multiples. This is executed reproducibility evidence; it does not validate the economic assumptions. It predates and is separate from the completed October 15 changed-input test.

Final primary recheck corrected the capital-spending locator from Note15 to Note1 p68 and distinguishes segment4,192 plus corporate223 from total4,415. Independent note inputs now feed an executable equality check against the CF line. Earlier working PDFs remain superseded; corrected-v2 PDFs and source-register-v3 are current. Packet UTF-8 loading failure and Poppler wrapper path failure were retained; direct bundled Poppler executable rendered the drafts. A localhost/browser preview attempt failed to attach and sandbox socket access was blocked; no successful browser interaction is claimed. Static HTML contains visible inputs/outputs, and PDF layout/text evidence is separately recorded.
