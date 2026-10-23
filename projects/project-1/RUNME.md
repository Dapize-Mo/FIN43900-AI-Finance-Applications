# PEP working model - Oladapo Olaniyan

FIN-43900 Project1. This supplemental run guide leaves the original README intact. Start here for the current continuation. AI-assisted working package; no final student recommendation or submission readiness claimed.

Decision: a buy-side committee with no PEP position is considering initiate/watch-defer/do-not-initiate. Working review horizon12-24months; modeled fiscal2026-2030. USD/common PEP, NASDAQ; no preferred/security valuation. Price date2026-10-05; bridge/share dates separately disclosed. Provisional AI action watch/defer pending student review and source closure.

## Reproduce offline

Python3.11+; standard library only, no pip dependencies, credentials or network. From this project directory:

```powershell
python src/model.py
```

Each run creates a NEW dated directory under outputs and refuses to overwrite an existing output directory. Optional explicit new destination: `python src/model.py --output outputs/my-new-run`. Nonzero exit if finance checks FAIL. OPEN/QUALIFIED records deliberately remain visible and do not mean submission is complete. If your shell Python is unavailable, use an installed working Python executable; the inherited course .venv was inaccessible in this session. The Codex bundled Python completed the recorded run.

Open `outputs/final-working-run/visible-output.html` directly for the current executed view; the accompanying Markdown/CSV/JSON expose statements, sensitivity, peer values, normalization and all checks without rerunning. Local HTML links resolve relative to the same directory. This is a static local product; no deployment needed. New output remains separate from preserved initial-run.

Optional independent cold-run replication: `python src/cold_run.py`. It copies only model.py, checks.py and data into a new project-local repro folder; creates a fresh no-pip environment; runs the isolated copy; compares deterministic financial CSV/JSON hashes with final-working-run; saves full stdout/stderr, exit codes/runtime and equality checks. No network or altered forecast input is involved. This is ordinary reproducibility, not the locked test.

## Map and financial logic

- `data/filing-inputs.json`: FY23-25 income/CF, FY24-25 BS, Q2bridge/shares, dated price/rate, source metadata.
- `data/assumptions.json`: explicitly AI-proposed forecast/WACC/terminal/payout assumptions.
- `data/peer-inputs.csv`: separate qualified KO/MDLZ lenses; dates/locators/status.
- `data/dcf_case.csv`, `dcf_expected_output.csv`: unchanged professor known-answer training fixtures.
- `src/model.py`: normalize -> forecast -> FCFF -> WACC/DCF -> bridge -> scenarios/sensitivity/reverse/comps -> outputs.
- `src/checks.py`: numerical finance tests, primary reconciliation, unresolved evidence.
- `docs/`: audit, assumption challenges, working memo, research evolution, validation/AI use, video preparation; student-owned evidence blanks.
- `sources/`: downloaded public evidence and retrieval failures; SEC values browsed but original SEC HTML downloads blocked403.
- `source-register-v3.csv` and `data/management-outlook-ledger.csv`: current line-level facts/definitions/as-of/locators versus assumptions and management guidance.
- `project1-manifest-working-v2.csv`:12 rows with unfinished hosting/recordings/frozen evidence explicitly pending.

Operating expenses include D&A; cash flow adds it back once. FCFF=EBIT*(1-tax)+D&A-capex-change operatingWC. Cash/debt/shareholder financing stays outside FCFF. Statements roll PP&E, intangibles, cash and equity; debt draw funds explicit cash floor rather than plugging cash silently. WACC uses basicpoint marketcap and bookdebtproxy. Valuation uses point shares+incremental dilutionproxy. Terminal netreinvestment=terminalNOPAT*g/ROIC; g<WACC and g<ROIC. Remaining fiscal2026 FCFF is prorated82/365, a disclosed seasonality approximation. DCF bridge adds cash/STI/bookaffiliateproxy and subtracts debt/NCI; other claims/fair value remain qualified.

Major limitations: unavailableEditionA report; actualpartnerreview absent; unapproved economics/beta/ERP/spread/ROIC; no quarterly/current-date bridge rollforward; full WC/acquisition/FX/lease/claim reconciliation missing; two qualified peers with bookinvestment and historicalearnings distortion; no actual videos/transcripts/hostedrepo/access/freeze. One AI-assisted locked changed-input test is complete under Oladapo Olaniyan's direct confirmation of the professor's in-class clarification; the posted Brightspace AI-off wording remains preserved in course-source records. Arithmetic PASS is not factual/judgment endorsement. Read `validation-and-ai-use-working.md`, `docs/validation-and-ai-use-v3.md`, and `docs/completion-report.md` before using results. Corrected working PDFs have `working-v2.pdf` suffixes; earlier drafts are preserved and superseded.

No original submitted file overwritten; no contact, push, publication or Brightspace submission. Final filenames/access identity must be verified before final packaging.
