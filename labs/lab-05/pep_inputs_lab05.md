# PepsiCo, Inc. (PEP) — Lab 05 Transferred Evidence Ledger

**Student Analyst:** Oladapo Olaniyan  
**Teammate:** kogbuef@purdue.edu  
**Course:** FIN 43900 — AI Finance Applications, Purdue University  
**Filing Reference:** SEC Form 10-K for Fiscal Year Ended December 28, 2024  

---

## 1. Transferred DCF Inputs Table

| Input Name | Value | Unit | Primary SEC Source & Locator | Classification |
|---|---|---|---|---|
| **Starting FCFF** | $9,688.59M | USD Millions | SEC Form 10-K, Cash Flows (p. 63) & Income Statement (p. 61). GAAP OCF ($12,680M) + Tax-Adjusted Interest ($771M) − CapEx ($5,318M) + Reversal of one-off impairment/restructuring charges ($1,811M). | Normalized Core Reported Fact |
| **Growth Years 1–5** | 3.0%, 3.5%, 4.0%, 3.5%, 3.0% | Decimal | Item 7 MD&A Division Review (pp. 43–47) & Q4 Earnings Guidance. Reflects FLNA volume recovery. | Labeled Forecast Assumption |
| **WACC** | 7.00% | Decimal | Note 8 Debt (p. 98) & Note 5 Income Taxes (p. 84). CAPM Cost of Equity 7.30%, After-Tax Cost of Debt 3.87%, 80/20 Capital Structure. | Calculated Financial Estimate |
| **Terminal Growth ($g$)** | 2.50% | Decimal | BEA / FRED Long-run US real GDP + inflation target. Bounded $g < \text{WACC}$. | Economic Boundary Parameter |
| **Non-Operating Cash** | $8,505.0M | USD Millions | Consolidated Balance Sheet (p. 65), Cash & Cash Equivalents. | Reported Fact |
| **Total Debt** | $44,306.0M | USD Millions | Consolidated Balance Sheet (p. 65), Short-Term Debt ($7,842M) + Long-Term Debt ($36,464M). | Reported Fact |
| **Diluted Shares** | 1,378.0M | Million Shares | Note 10 Net Income Per Share (p. 106), Diluted common share count. | Reported Fact |

---

## 2. Unresolved Assumption Note

* **Unresolved Item:** `wacc_cost_of_debt`  
* **Details:** While cost of equity is anchored at 7.30% ($R_f=4.30\%, \beta=0.60, \text{ERP}=5.00\%$) and effective tax rate is 19.4%, weighted average pre-tax cost of debt across PepsiCo's multi-tranche fixed/floating debt structure ($44.3B) requires full debt schedule extraction from Note 8 before Thursday's Session 6 sensitivity grid.
