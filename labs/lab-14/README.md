# Lab 14 — Portfolio Baselines

**Course:** FIN 43900 — AI Finance Applications, Fall 2026  
**Student / Author:** Oladapo Olaniyan (`oolaniy@purdue.edu`)  
**Case:** Meridian Foundation Reserve ($100 Million Reserve)  
**Date:** October 20, 2026  
**Category:** Tuesday Authenticated Completion (25 Points)

---

## Controlling Instructions & Source Hierarchy

- **Course Instruction:** [Week 9 — Lab 14 Portfolio Baselines](https://github.com/CinderZhang/FIN43900-Fall2026/blob/main/lessons/week-09/lab-14-portfolio-baselines.md)
- **Student Handout:** [Student Handout — Portfolio Construction and Stability](https://github.com/CinderZhang/FIN43900-Fall2026/blob/main/lessons/week-09/student-handout.md)
- **Calculation Recovery Protocol:** [Week 9 Portfolio Calculation Recovery](https://github.com/CinderZhang/FIN43900-Fall2026/blob/main/lessons/week-09/portfolio-calculation-recovery.md)
- **Mandate Context:** Meridian Foundation Common CIO Case (Week 8)

---

## Required Deliverables & Files

1. **Portfolio Baselines Engine:** [`portfolio_baselines.py`](portfolio_baselines.py)  
   Python script calculating input validation, annualized covariance matrix via $\Sigma = \text{diag}(\sigma) C \text{diag}(\sigma)$, equal-weight baseline, inverse-volatility baseline, provisional mechanics candidate allocation, and rigorous matrix/mandate audits.
2. **Teaching Input Datasets:**
   - [`asset_statistics.csv`](asset_statistics.csv): Annualized expected returns and volatilities across four core asset classes (`GovBond`, `CorpBond`, `USEquity`, `IntlEquity`).
   - [`correlation.csv`](correlation.csv): Symmetric correlation matrix with unit diagonals.
3. **Full Lab Checkout Deliverable:** [`checkout.md`](checkout.md)  
   Comprehensive, audited checkout document covering decision boundary, manual cell reconciliations, baseline vs. candidate comparisons, AI disclosures, fiduciary deferral, and personal growth note.
4. **Brightspace Submission Block:** [`../../brightspace/lab-14_submission.txt`](../../brightspace/lab-14_submission.txt)  
   Pre-formatted copy-paste plain text block formatted specifically for the Brightspace checkout quiz.

---

## Status

**Complete & Fully Verified.**
- Arithmetic covariance matrix reconciled against four independent manual calculations (diagonal and off-diagonal).
- Baseline metrics computed:
  - **Equal Weight:** Return = 6.50%, Volatility = 9.80%
  - **Inverse Volatility:** Return = 5.61%, Volatility = 6.80%
  - **Provisional Mechanics Probe (60/40):** Return = 6.90%, Volatility = 11.15%
- Fiduciary disposition explicitly documented as `DEFERRED_NO_ADOPTABLE_CANDIDATE` due to unresolved CIO utility function and qualitative 10% loss statement S9.
