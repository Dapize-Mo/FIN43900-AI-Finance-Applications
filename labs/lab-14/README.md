# Lab 14 — Portfolio Baselines

**Course:** FIN 43900 — AI Finance Applications, Fall 2026  
**Student / Author:** Oladapo Olaniyan (`oolaniy@purdue.edu`)  
**Case:** Meridian Foundation Reserve ($100 Million Reserve)  
**Date:** October 20, 2026  
**Category:** Tuesday Authenticated Completion (25 Points)

---

## Controlling Instructions & Source Hierarchy

- **Course Instruction:** [Week 9 — Lab 14 Portfolio Baselines](https://github.com/CinderZhang/FIN43900-Fall2026/blob/main/lessons/week-09/lab-14-portfolio-baselines.md) (Rebuilt October 13, 2026)
- **Session Slides:** [Session 14 Slides](https://github.com/CinderZhang/FIN43900-Fall2026/blob/main/lessons/week-09/slides-session-14.md)
- **Student Handout:** [Student Handout — Portfolio Construction and Stability](https://github.com/CinderZhang/FIN43900-Fall2026/blob/main/lessons/week-09/student-handout.md)
- **Mandate Context:** Meridian Foundation Common CIO Case (Week 8)

---

## Deliverables & Files

1. **Standard-Library Risk Engine:** [`portfolio.py`](portfolio.py)  
   Python script built using Python's standard library only. Implements editable inputs, covariance matrix construction ($\Sigma_{ij} = \rho_{ij} \sigma_i \sigma_j$), strict input contract validation (refuses out-of-bound correlations $[-1, 1]$ or asymmetric matrices), and computes return, volatility, reserve-eligible weight, and objective testing across three core portfolios:
   - **Benchmark:** 40% IG bond fund, 60% global equity index fund
   - **Equal weight:** 25% in each of the four sleeves
   - **Inverse volatility:** weights proportional to $1/\sigma_i$ scaled to 100%
2. **Updated Mandate Checker (with Candidate E):** [`../lab-13/mandate.py`](../lab-13/mandate.py)  
   Evaluates Candidate E (the Benchmark: 40% IG, 60% Equity), revealing that the client's own benchmark fails the mandatory $3.0\%$ liquidity reserve rule at $0.0\%$.
3. **Historical Price Dataset for Thursday App:** [`prices.csv`](prices.csv)  
   Five years of monthly adjusted close prices (Nov 2021 – Oct 2026) for the student's Project 2 universe:
   - `BIL`: SPDR Bloomberg 1-3 Month T-Bill ETF (Cash / Reserve)
   - `IEF`: iShares 7-10 Year Treasury Bond ETF (Government Bonds)
   - `LQD`: iShares iBoxx $ Investment Grade Corporate Bond ETF (Fixed Income)
   - `VT`: Vanguard Total World Stock ETF (Global Equities)
4. **Full Lab Checkout Deliverable:** [`checkout.md`](checkout.md)  
   Comprehensive, audited checkout document covering manual first-principles derivations, known-answer reconciliations, sensitivity probes, reflections, and personal growth note.
5. **Brightspace Submission Block:** [`../../brightspace/lab-14_submission.txt`](../../brightspace/lab-14_submission.txt)  
   Clean, pre-formatted plain-text block formatted specifically for the Brightspace checkout quiz.

---

## Known-Answer Verification Summary

| Portfolio | Weights: bills / 10-year / IG / equity | Expected Return | Volatility | Reserve-Eligible | Meets 6.5% Objective? |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Benchmark** | $0.0 \ / \ 0.0 \ / \ 40.0 \ / \ 60.0$ | **6.80%** | **10.46%** | **0.0%** | **yes** |
| **Equal weight** | $25.0 \ / \ 25.0 \ / \ 25.0 \ / \ 25.0$ | **5.20%** | **5.21%** | **50.0%** | **no** |
| **Inverse volatility** | $84.3 \ / \ 6.0 \ / \ 7.0 \ / \ 2.6$ | **3.77%** | **1.05%** | **90.3%** | **no** |

- **Sensitivity Probe:** Setting IG–Equity correlation to $0.50$ increases Benchmark volatility to exactly **11.00%**.
- **Input Refusal:** Setting correlation to $1.3$ or violating symmetry raises an immediate `ValueError`.
- **Mandate Collision:** Candidate E fails the reserve rule at $0.0\%$ (requires $3.0\%$ minimum).
