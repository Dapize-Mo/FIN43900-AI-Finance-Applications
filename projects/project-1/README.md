# FIN 43900 Project 1 — Corporate Finance Application

**Student Analyst:** Oladapo Olaniyan  
**Target:** PepsiCo, Inc. (NASDAQ: PEP; CIK 0000077476)  
**Decision user:** Buy-side investment committee; fund currently has no position  
**Brightspace due:** October 19, 2026, 11:59 PM (verified October 6, 2026)  
**Status:** Three recordings completed and locally checked; written package and external access are being finalized. Oladapo's recorded recommendation is watch/defer. Economic qualifications remain disclosed.

## Current recording and packaging record

The prepared local deliverables are now in [submission/](submission/). Start with [START-HERE.txt](submission/START-HERE.txt), the three refreshed PDFs, corrected topic transcripts, and [submission manifest](submission/submission-manifest.csv). The clean repository payload and ZIP are included there. All seven PDF pages were visually inspected; a run of the packaged model exited 0 and matched all five principal output hashes. YouTube publication status is tracked in [youtube-upload-status.json](submission/youtube-upload-status.json); only states verified in Studio are recorded. The clean repository package is published publicly on codex/project-1-submission; the submission manifest pins its frozen commit. Anonymous video player access passed for all three links; Brightspace submission succeeded October 18, 2026 at 12:11 AM, receipt 23393007.

Start with [recording clarifications](docs/recording-clarifications-20261017.md) and [working manifest v5](project1-manifest-working-v5.csv). They reconcile Video 1's dated working screens with the reported TA resolution and completed checks, distinguish Video 3's spoken coverage from sampled screen evidence, and point to the three audio-compared transcript drafts. The current submission folder contains hosted video links, audio-compared transcripts and refreshed content-equivalent PDFs. Anonymous video player access passed for all three links. Earlier manifests and presentation PDFs are retained versions, not the current recording status.

## Purpose

Build a locally runnable, evidence-traceable valuation system that supports a conditional committee decision to initiate, watch/defer, or not initiate PEP. The final result must be a defensible valuation range with dated evidence, assumptions, risks, and reversal/monitoring triggers. This working directory supplements earlier labs; it does not replace or edit the frozen Edition A submission.

## Official requirements

Brightspace's **Project 1 — Corporate Finance Application** assignment page is authoritative. It requires:

- A five-year, company-specific, linked income statement, balance sheet, and cash-flow forecast, with the forecast driving an FCFF DCF.
- A normalized filing-based base year; assumptions labeled by value, basis, challenge, and evidence that would change them.
- A complete EV-to-common-equity-to-diluted-share bridge; causal low/base/high cases; WACC/g sensitivity; terminal-value share; and a reverse DCF or market-implied expectation.
- A peer-selection policy established before selecting peers; consistent EV and equity multiples; an explanation when methods disagree; and a named downside case that can change the recommendation.
- Known-answer, independent-source/definition, changed-input, articulation, DCF boundary/monotonicity, bridge, peer-policy, highest-risk, AI-output, and clean-environment checks.
- A final package: unchanged Edition A plus Edition B and comparison; accessible runnable repository with visible executed output; memo (maximum two pages) or deck (maximum eight main slides); frozen validation/AI-use record; Video 1 (maximum 3 minutes), Video 2 (maximum 5 minutes), Video 3 (maximum 5 minutes, with Project 1's live product demonstration as its main delivery), corrected transcripts, and a complete manifest.

The full package and time limits are in `FIN43900-Fall2026-main/projects/major-project-student-checklist.md` and `FIN43900-Fall2026-main/PROJECT-SUBMISSION-ARCHITECTURE.md`. Brightspace remains authoritative if those course-repository copies differ.

## Frozen baseline and data boundary

Brightspace Submission History shows the separate Edition A checkpoint's first submission: ID **22599005**, `Project_1_Edition_A_Baseline_PEP.pdf`, submitted **September 1, 2026 at 2:30 PM**. Keep that PDF unchanged. A dated correction or Edition B belongs beside it in the final Research-Evolution package.

**Edition A clarification recorded October 17:** Oladapo reports the TA verbally resolved the copy issue and said it is acceptable if the information is the same. See [reported TA guidance](docs/staff-guidance-user-reported-v3-20261017.md). The receipt-linked PDF remains byte-identical to the original (SHA-256 `F745E7EA27A1445830573029A77D28967A1E4F5E53A9BA9A794079373F35464F`) and contains a Microsoft Edge error page. The receipt verifies submission; the separate preexisting draft is supporting evidence. Originals remain preserved. The issue is no longer awaiting staff guidance in this working package.

Current research starts from PepsiCo's FY2025 Form 10-K and the latest 10-Q filed by this workspace's October 6, 2026 review date (Q2 2026, filed July 9, 2026). The old project files use FY2024 inputs and must be rolled forward and reconciled. Every market datum must carry an as-of date and provider definition. See `source-register.csv`; entries marked pending are not approved model inputs.

## Work plan

1. Reconcile FY2025 audited statements and the latest interim filing to a source ledger; identify one-time items and accounting-basis changes before normalizing.
2. Audit and retain useful prior code only after reconciling its definitions; replace FCFE or stale-price paths where Project 1 requires forecast-driven FCFF.
3. Set a dated price/security/share-count convention and peer policy; source comparable financials and market data consistently.
4. Build linked five-year statements and explicit assumption lineage, then connect them to scenario DCF, bridge, sensitivity, reverse DCF, peer multiples, and a named downside stress.
5. The locked changed-input record is complete: it changes terminal ROIC from 15.0% to 12.0%, with a prediction frozen before the separate run. It was AI-assisted under Oladapo Olaniyan's direct confirmation that the professor clarified the posted “AI-off” wording in class. See `validation-and-ai-use-working.md` and `repro/locked-change-20261015T1722CDT/locked-test-report.md`. The original Brightspace wording remains preserved in the course-source records.
6. Run required checks, prepare visible output and validation/AI-use record, then draft Edition B, the memo/deck, video/transcript plan, and final manifest.

## Files in this folder

- `artifact-audit.md` — existing work and reuse decisions.
- `source-register.csv` — filing/market-source queue, cutoffs, and review state.
- `research-evolution-working.md` — baseline pointer and Edition B comparison workspace.
- `docs/validation-and-ai-use-v3.md` — current validation/disclosure source, including the separate completed terminal-ROIC test; PDF refresh remains pending.
- `docs/recording-clarifications-20261017.md` — dated-screen clarification and accurate spoken/visual recording index.
- `docs/audio-check/` — recording check, measured file identities, timestamp comparison, and three audio-compared transcript drafts.
- `project1-manifest-working-v5.csv` — current local recordings and remaining submission/access steps.

No results, future assumptions, source values, or final recommendation should be treated as validated until the evidence ledger and checks support them.
