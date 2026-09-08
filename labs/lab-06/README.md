# Lab 06 — Sensitivity, Reverse DCF, and Conditional Recommendation

**Target Company:** PepsiCo, Inc. (NASDAQ: `PEP` | CIK: `0000077476`)  
**Student Analyst:** Oladapo Olaniyan  
**Teammate:** kogbuef@purdue.edu  
**Course:** FIN 43900 — AI Finance Applications, Purdue University  
**Date:** September 8, 2026  

---

## Overview

This directory houses the complete quantitative model, sensitivity analysis, reverse DCF, and Brightspace checkout package for **Lab 06**. 

The mission of Lab 06 is to stress-test the DCF valuation built in Week 3, understand the dominant sensitivity drivers of enterprise value, translate observed market prices into implied operating expectations, and defend a conditional investment recommendation before an investment committee.

---

## Directory Contents

| File | Description |
|---|---|
| [`pep_dcf_model_lab06.py`](pep_dcf_model_lab06.py) | Full Python DCF engine implementing `project_fcff`, `value_dcf`, `sensitivity_table`, `reverse_dcf_for_growth`, training-case validation, PepsiCo scenarios, and monotonicity tests. |
| [`pep_sensitivity_grid.csv`](pep_sensitivity_grid.csv) | Exported 5x4 sensitivity grid of per-share values across WACC (6.0%–8.0%) and Terminal Growth (1.5%–3.0%). |
| [`lab-06-checkout.md`](lab-06-checkout.md) | Official, copy-paste ready Brightspace submission package with field-by-field answers, causal scenario tables, and growth note. |

---

## Executive Summary of Valuation Results

### 1. Synthetic Training Validation (Known-Answer Check)
- **Engine Verification:** Evaluated against `dcf_case.csv` and `dcf_expected_output.csv`.
- **Result:** All 12 synthetic checkpoints passed within strict numerical tolerances ($27.50/share per-diluted-share equity value, $1,624.87M enterprise value, 72.40% terminal value share).

### 2. PepsiCo Scenario Matrix (Causal Drivers)
- **Base Starting FCFF:** $9,688.59M (Normalized Core FY2024 unlevered free cash flow from SEC Form 10-K).
- **Net Debt Claim:** $35,801.0M (Total Debt $44,306.0M less Cash & Equivalents $8,505.0M).
- **Diluted Common Shares:** 1,378.0M shares.

| Scenario | 5-Year FCFF Growth Path | WACC | Terminal Growth (g) | Enterprise Value ($M) | Equity Value ($M) | Value / Diluted Share | TV Share of EV |
|---|---|---|---|---|---|---|---|
| **Low (Bear) Case** | [1.5%, 2.0%, 2.0%, 1.5%, 1.5%] | 7.50% | 2.00% | $177,342.9M | $141,541.9M | **$102.72** | 76.8% |
| **Base Case** | [3.0%, 3.5%, 4.0%, 3.5%, 3.0%] | 7.00% | 2.50% | $229,731.6M | $193,930.6M | **$140.73** | 81.0% |
| **High (Bull) Case**| [5.0%, 5.0%, 4.5%, 4.0%, 3.5%] | 6.50% | 2.50% | $270,725.6M | $234,924.6M | **$170.48** | 83.0% |

### 3. WACC / Terminal Growth Grid Excerpt ($ per Diluted Share)

| Terminal Growth (g) \ WACC | 6.00% | 6.50% | 7.00% (Base) | 7.50% | 8.00% |
|---|---|---|---|---|---|
| **1.50%** | $146.73 | $129.34 | $115.12 | $103.27 | $93.24 |
| **2.00%** | $165.01 | $143.70 | $126.65 | $112.69 | $101.07 |
| **2.50% (Base)** | $188.52 | $161.64 | **$140.73** | $124.01 | $110.33 |
| **3.00%** | $219.87 | $184.71 | $158.34 | $137.84 | $121.43 |

*Monotonicity Test: Verified. Value strictly decreases with increasing WACC and strictly increases with increasing g across all rows and columns.*

### 4. Reverse DCF (Market-Implied Expectation)
- **Observed Market Price:** **$143.21** (Nasdaq close on February 4, 2025 earnings release date).
- **Solved Implied 5-Year FCFF Compounding Rate:** **3.73% per year**.
- **Economic Takeaway:** The market is currently pricing PepsiCo at fair value under an operational recovery scenario (moving from 2024's +2.0% organic top-line pace to 3.73% annual cash flow expansion). There is minimal safety margin for North American volume slips.

### 5. Conditional Committee Recommendation
- **Stance:** **WATCH-DEFER**
- **Action Trigger:** Upgrade to Initiate-Buy only if PEP pulls back below **$125.00** (a 12%+ discount to Base Case fair value) OR if Frito-Lay North America prints two consecutive quarters of positive organic volume growth without margin compression.
- **Reversal Trigger:** Revisit downward immediately if North American convenient foods volume contraction worsens past -3.0%.

---

## Instructions to Run the Model

To execute the model and regenerate all validation metrics, sensitivity grids, and reverse DCF solutions:

```bash
python labs/lab-06/pep_dcf_model_lab06.py
```
