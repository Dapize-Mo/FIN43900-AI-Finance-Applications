# Lab 15 — Portfolio Stability Decision

**Course:** FIN 43900 — AI Finance Applications, Fall 2026  
**Student / Author:** Oladapo Olaniyan (`oolaniy@purdue.edu`)  
**Teammate / Learning Partner:** J. Maffei (`maffeij@purdue.edu` | Target Company: Oracle Corp. — `ORCL`)  
**Institution:** Mitchell E. Daniels, Jr. School of Business, Purdue University  
**Case:** Meridian Foundation Reserve ($100 Million Reserve) & Student Universe  
**Date:** October 22, 2026  
**Session Token:** `webapp`  
**Category:** Thursday Merit Checkout (25 Points)

---

## 📌 Controlling Instructions & Source Hierarchy

- **Course Instruction:** [Week 9 — Lab 15 Portfolio Stability Decision](https://github.com/CinderZhang/FIN43900-Fall2026/blob/main/lessons/week-09/lab-15-portfolio-stability.md)
- **Session Slides:** [Session 15 Slides](https://github.com/CinderZhang/FIN43900-Fall2026/blob/main/lessons/week-09/slides-session-15.md)
- **Student Handout:** [Student Handout — Portfolio Construction and Stability](https://github.com/CinderZhang/FIN43900-Fall2026/blob/main/lessons/week-09/student-handout.md)
- **Engine Foundation:** [`../lab-14/portfolio.py`](../lab-14/portfolio.py)

---

## 🚀 Deliverables & Files

1. **Portfolio Engine & Optimization Search:** [`portfolio.py`](portfolio.py)  
   Python script built using Python's standard library only. Preserves all Tuesday baseline calculations and console output while adding:
   - `search_lowest_risk_mix()`: 5-point long-only grid search returning the minimum-volatility portfolio satisfying the target return hurdle ($\ge 6.5\%$) and minimum reserve constraint ($\ge 3.0\%$).
   - `estimate_from_prices()`: Standard-library parser calculating annualized mean return ($\text{mean} \times 12$), annualized volatility ($\text{std} \times \sqrt{12}$), and correlation matrix from monthly prices across full history or trailing 36-month window.
2. **Streamlit Interactive Application:** [`app.py`](app.py)  
   Interactive web application that imports the calculation engine directly without copying math. Features a configurable sidebar (target return, reserve minimum, file uploader for `prices.csv`, live `yfinance` market query connector, 36-month toggle), editable expected return boxes, reserve-eligibility checkboxes, side-by-side baseline vs. stressed mix display, and stability diagnosis showing the largest weight change in points.
3. **Historical Monthly Price Dataset:** [`prices.csv`](prices.csv)  
   Five years of monthly adjusted close prices (Nov 2021 – Oct 2026) across four liquid sleeve ETFs (`BIL`, `IEF`, `LQD`, `VT`) downloaded from Yahoo Finance on October 20, 2026.
4. **Complete Lab Checkout Document:** [`checkout.md`](checkout.md)  
   Audited report documenting known-answer verifications, engine link proofs, student universe estimations (60 months vs. 36 months), partner stress attack, the investment decision call, estimation risk deep-dive, and personal reflections.
5. **Brightspace Submission Block:** [`../../brightspace/lab-15_submission.txt`](../../brightspace/lab-15_submission.txt)  
   Clean, pre-formatted plain-text block formatted specifically for the Brightspace checkout quiz.

---

## 🎯 Verification & Stability Results Summary

### 1. Training Set Verification (Meridian Foundation)

| Configuration / Run | Weights (Bills / 10-year / IG / Equity) | Return | Volatility | Reserve-Eligible | Largest Shift |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Meridian As Loaded** | `0 / 20 / 25 / 55` | **6.51%** | **9.44%** | **20.0%** | Baseline |
| **Equity Return $8.0\% \to 7.0\%$** | `0 / 10 / 10 / 80` | **6.53%** | **12.94%** | **10.0%** | **25 points** |
| **Engine Link Probe ($\rho_{\text{IG,Eq}} = 0.50$)** | `0 / 40 / 0 / 60` | **6.52%** | **9.73%** | **40.0%** | Engine Verified |

### 2. Student Universe Analysis (`BIL`, `IEF`, `LQD`, `VT`)

| Horizon | Weights (BIL / IEF / LQD / VT) | Return (Estimate) | Volatility (Estimate) | Reserve-Eligible | Status |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **All Months (60 mo)** | `60 / 0 / 0 / 40` | **6.87%** | **6.01%** | **60.0%** | Meets Mandate |
| **Last 36 Months** | `85 / 0 / 0 / 15` | **6.84%** | **1.76%** | **85.0%** | Meets Mandate |
| **Horizon Shift** | **Largest Weight Change:** | — | — | — | **25 points** |

---

## 💻 Running the Streamlit App

Run the application from the workspace terminal using the course Python environment:

```powershell
streamlit run app.py
```

*(Or via direct venv path):*

```powershell
& "C:\Users\dolan\Code\school\Fall-2026\FIN-43900\workspace\.venv\Scripts\python.exe" -m streamlit run app.py
```