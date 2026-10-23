# Recording clarifications and evidence index

Oladapo Olaniyan | FIN-43900 Project 1 | October 17, 2026

## Recommendation recorded by the analyst

In Videos 1 and 3, Oladapo Olaniyan states a watch/defer recommendation for PepsiCo. Video 3's committee ask begins at approximately 4:04: defer entry, monitor revenue growth, operating margin, cash conversion, debt, and payouts, and reconsider after a reviewed current-date bridge and verified improvement in margins and cash flow or a defensible margin of safety. Structural margin erosion, weaker cash conversion, or insufficient downside funding would argue against initiation.

This records the position expressed in the recordings. It does not imply blanket acceptance of every working forecast, source convention, proposed numerical entry threshold, or personal attestation in earlier AI-assisted drafts. The recordings do not establish acceptance of the separately proposed $93.84 entry threshold.

## Video 1: dated research and validation screens

The recording shows earlier working pages. Their statements that staff guidance is unresolved, student judgment is blank, or particular checks have not been run describe those earlier pages rather than the current evidence package.

The two recording-support pages were subsequently refreshed in place at `../videos/video-1/02-research-evolution.md` and `../videos/video-1/03-validation-and-ai-use.md`. Exact copies of their earlier recorded versions are preserved in `../videos/video-1/recorded-page-snapshots/`. Refreshing a page after recording does not change the video frames.

Oladapo reported that the TA verbally resolved the Edition A issue and said the copy is acceptable as long as the information is the same. This is documented in [the reported TA guidance](staff-guidance-user-reported-v3-20261017.md). October 17 is the date this clarification was recorded locally; the conversation in class occurred earlier, on an unspecified date. No written TA message is claimed.

The original receipt-linked PDF remains preserved unchanged at `../recovery/edition-a-20261006/Edition-A-approved-redownload.pdf`. The recovery record identifies receipt **22599005**, submitted **September 1, 2026 at 2:30 PM**, and the original attachment's SHA256:

`f745e7ea27a1445830573029a77d28967a1e4f5e53a9ba9a794079373f35464f`

The submitted PDF contains an error page; the receipt establishes submission, not recoverable report content. The separate preexisting Markdown draft remains supporting evidence. The reported TA resolution governs the working-package treatment; an old screen saying "unresolved" is not the current status.

Current validation evidence is `../outputs/final-working-run/checks.csv`: **42 PASS, 0 FAIL, 5 OPEN, 2 QUALIFIED**. Open/qualified findings remain disclosed. The separate terminal-ROIC prediction and run are documented in `../repro/locked-change-20261015T1722CDT/locked-test-report.md`. The static old check message about an unexecuted locked record predates that separate run.

In Video 1, the spoken capex explanation is supported by the saved reconciliation: **$4.192 billion segment + $0.223 billion corporate = $4.415 billion consolidated**. The ROIC test changed **15% to 12%**, lowering base value from **$117.29 to $111.41**, a **$5.88 / 5.02%** decline using the unrounded model outputs. Standard ROIC terminology is *return on invested capital*; the spoken expansion is retained in the transcript, with its correction separately labeled.

## Video 2: technical evidence

The sampled recording frames show model code, the validation CSV, and cold-run JSON. Audio topic markers are approximately **0:59 assumptions; 1:31 results; 2:04 terminal value; 2:26 validation; 3:12 clean run**. Cold-run evidence at `../repro/cold-20261006T053603935700Z/cold-run-evidence.json` reports exit 0 and matching principal output hashes. Paths beginning `labs/project-1` in that historical log reflect the former project location; use `../RUNME.md` for current reproduction instructions.

## Video 3: spoken coverage and visible evidence

The recording presents the live output page and speaks to the following topics. Times are approximate topic navigation markers from the local audio comparison:

| Time | Spoken topic | Evidence treatment |
|---|---|---|
| 0:03 | Watch/defer, recorded price, base value | Opening narration; local output provides the figures |
| 0:35 | Low/base/high scenarios | Summary table is part of the displayed output |
| 1:05 | Five-year FCFF, WACC, growth, bridge | Spoken explanation; forecast summary in output |
| 2:13 | Value Reset Failure | Spoken operating/downside explanation; scenario summary in output |
| 2:50 | Sensitivity and reverse DCF | Spoken explanation; detailed grid and reverse calculation supplied in repository |
| 3:23 | Qualified KO/MDLZ peers; no mechanical averaging | Spoken explanation; detailed peer evidence supplied in repository |
| 4:04 | Committee ask, monitoring, reversal conditions | Spoken conclusion |

At sampled times **2:30, 3:10, and 3:45**, the screen displays scenario and forecast summary tables. Those samples do not establish that the detailed sensitivity grid or peer section was expanded onscreen. The manifest therefore indexes sensitivity/reverse DCF/peers as **spoken explanations**, rather than claiming a visual demonstration of those detailed calculations.

Supporting repository evidence: `../outputs/final-working-run/visible-output.html`, `../outputs/final-working-run/sensitivity.csv`, `../outputs/final-working-run/peer-multiples.csv`, and `../outputs/final-working-run/results.json`. These explain the numerical claims without relying on an unsupported description of the recording. They supplement the recording; they do not establish that every visual requirement was demonstrated.

## Transcript and submission status

The three recordings measure **2:16.405**, **4:08.768**, and **4:41.240**, within the respective **3:00 / 5:00 / 5:00** limits. Originals are unchanged in the user's Zoom folders.

The current transcript copies are in `audio-check/transcript-video-1-audio-compared.txt` through `transcript-video-3-audio-compared.txt`. They preserve supplied speech wording, use approximate audio-aligned topic times, and separate editorial notes. Full local automated recognition and sampled frame review are documented in [the recording check](audio-check/recording-check-report.md). A few uncertain spoken words/self-corrections remain flagged; these copies are not yet asserted as final corrected word-for-word transcripts.

Use `../project1-manifest-working-v5.csv` as the current working manifest. Hosted repository/video URLs, logged-out access checks, final transcript wording, and refreshed content-equivalent submission PDFs remain to be completed before freezing the submission. This clarification is an explanatory addendum; it does not replace the required Research-Evolution or Validation-and-AI-Use deliverables.
