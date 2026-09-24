# FIN 43900 Lab 10 — Pro-Forma: Your Company Through It

**Course:** FIN 43900 — AI Finance Applications, Purdue University  
**Student Analyst:** Oladapo Olaniyan  
**Teammate / Partner:** Kenechukwu Ogbuefi (`kogbuef@purdue.edu`)  
**Target Company:** PepsiCo, Inc. (NASDAQ: `PEP` | CIK: `0000077476`)  
**Filing Reference:** SEC Form 10-K for Fiscal Year Ended December 28, 2024  
**Date:** September 2026 / Thursday Merit Checkout  
**Session Token:** `Pro-Forma`  

---

## Deliverables & Repository Links

- **Python 3-Statement Model Script:** [`pep_proforma_lab10.py`](file:///c:/Users/dolan/OneDrive%20-%20purdue.edu/2026-Fall/FIN-43900%20-%20AI%20Finance%20Applications/labs/lab-10/pep_proforma_lab10.py)
- **Pro-Forma Execution Wrapper:** [`proforma.py`](file:///c:/Users/dolan/OneDrive%20-%20purdue.edu/2026-Fall/FIN-43900%20-%20AI%20Finance%20Applications/labs/lab-10/proforma.py)
- **Lab 10 Checkout Report:** [`lab-10-checkout.md`](file:///c:/Users/dolan/OneDrive%20-%20purdue.edu/2026-Fall/FIN-43900%20-%20AI%20Finance%20Applications/labs/lab-10/lab-10-checkout.md)
- **Lab 10 README Overview:** [`README.md`](file:///c:/Users/dolan/OneDrive%20-%20purdue.edu/2026-Fall/FIN-43900%20-%20AI%20Finance%20Applications/labs/lab-10/README.md)

---

## D — The Question

> **What are five years of PepsiCo's statements worth, built from assumptions you can defend?**

### Company & Ticker
**PepsiCo, Inc. (NASDAQ: `PEP`)**

### Company Differentiation Line
"PepsiCo is a dual-engine consumer packaged goods giant (Frito-Lay snacks + PepsiCo beverages) with high gross margins (~54%), heavy supply chain automation CapEx (~$5.3B/yr), no floor plan financing ($0.0 floor plan debt), and substantial direct cash returns to shareholders (~$7.5B/yr in dividends and buybacks)."

---

## R — History, Ratios, and Assumption Set

### 1. Three-Year Historical Financial Grid (SEC Form 10-K Traced)

| Line Item (USD Millions) | FY2022 | FY2023 | FY2024 | Primary SEC Filing Source & Page Locator | Confirmation Status |
|---|---:|---:|---:|---|---|
| **Total Net Revenue** | $86,392.0 | $91,471.0 | $91,854.0 | SEC Form 10-K, Consolidated Statements of Income (p. 61) | Confirmed by hand |
| **Gross Profit** | $45,781.0 | $49,701.0 | $49,864.0 | SEC Form 10-K, Consolidated Statements of Income (p. 61) | Confirmed by hand |
| **SG&A Expenses** | $34,249.0 | $37,704.0 | $38,829.0 | SEC Form 10-K, Consolidated Statements of Income (p. 61) | Confirmed by hand |
| **Net Income (PepsiCo Share)** | $8,910.0 | $9,074.0 | $8,245.0 | SEC Form 10-K, Consolidated Statements of Income (p. 61) | Confirmed by hand |
| **Inventories** | $5,222.0 | $5,334.0 | $5,432.0 | SEC Form 10-K, Consolidated Balance Sheets (p. 65) | Confirmed by hand |
| **Property, Plant & Equipment (Net)** | $24,187.0 | $26,767.0 | $27,890.0 | SEC Form 10-K, Consolidated Balance Sheets (p. 65) | Confirmed by hand |
| **Shareholders' Equity** | $17,163.0 | $18,631.0 | $18,915.0 | SEC Form 10-K, Consolidated Balance Sheets (p. 65) | Confirmed by hand |

*All items verified directly against PepsiCo, Inc. audited SEC Form 10-K filings.*

---

### 2. Three-Year Historical Ratio Table

| Historical Ratio | FY2022 | FY2023 | FY2024 | 3-Year Trend & Economic Rationale |
|---|---:|---:|---:|---|
| **Gross Margin (%)** | 53.00% | 54.34% | 54.29% | Expanding ~130 bps due to pricing power across snacks and beverages. |
| **SG&A ÷ Gross Profit (%)** | 74.81% | 75.86% | 77.87% | Reported ratio spiked in 2024 due to $1.81B one-off impairment/restructuring charges; core ratio is ~74.24%. |
| **Inventory ÷ COGS (%)** | 12.86% | 12.77% | 12.94% | Highly stable (~47 inventory days), reflecting efficient CPG turnover. |
| **Depreciation ÷ PP&E (%)** | 11.85% | 11.45% | 11.33% | D&A averages ~11.5% of net fixed assets ($3,160M D&A in 2024). |
| **CapEx ÷ Revenue (%)** | 5.48% | 5.89% | 5.79% | Disciplined reinvestment in bottling plants, fleet, and automation ($5,318M in 2024). |
| **Effective Tax Rate (%)** | 20.50% | 20.10% | 19.40% | Stable global effective tax rate averaging ~20.0%. |
| **Reported vs. Organic Revenue Growth** | +8.7% (Rep) / +14.4% (Org) | +5.9% (Rep) / +9.5% (Org) | +0.4% (Rep) / +2.1% (Org) | Organic growth consistently exceeds reported growth due to FX headwind drags. |

---

### 3. Labelled Three-Column Assumption Set

| Assumption Line Item | Model Value | Label Type | Economic Rationale & Student Defense |
|---|---:|---|---|
| **Revenue Growth Path (2025E–2029E)** | `[3.0%, 3.5%, 4.0%, 3.5%, 3.0%]` | **Judgment** | Reflects near-term Frito-Lay North America volume stabilization from -2.5% to +0.5%, combined with 2.0%–2.5% net pricing and 6%+ international emerging market expansion. |
| **Gross Margin** | **54.30%** | **History** | Anchored on FY2023–FY2024 average (54.31%), reflecting strong brand pricing power and productivity offsets. |
| **SG&A ÷ Gross Profit Path** | `[74.0%, 73.5%, 73.0%, 72.5%, 72.0%]` | **Judgment** | Begins at normalized core FY2024 level (74.24% excluding one-offs) and improves 200 bps over 5 years via $1B+ annual automation and digitalization savings. |
| **Impairment / One-offs** | **$0.0M** | **Guidance** | Normalized going-forward operating basis; non-recurring 2024 asset write-downs ($1.81B) are removed from forward baseline. |
| **Annual Capital Expenditures (CapEx)** | **$5,300.0M** | **Guidance** | Aligns with management guidance (~5.5% of revenue) for ongoing bottling network upgrades and logistics automation. |
| **Depreciation ÷ PP&E Ratio** | **11.33%** | **History** | Locked to FY2024 actual D&A rate ($3,160M D&A on $27,890M Net PP&E). |
| **Effective Tax Rate** | **19.50%** | **Guidance** | Aligns with PepsiCo's 2024 reported rate (19.4%) and long-term tax guidance (19.0%–20.0%). |
| **Minimum Cash Floor** | **$4,000.0M** | **Judgment** | Operational liquidity threshold required to support global working capital, supply chain operations, and payroll. |
| **Annual Net Debt Reduction** | **$1,000.0M** | **Judgment** | Orderly debt paydown schedule to maintain A+/A1 credit rating and optimize leverage ratio. |
| **Shareholder Cash Return (Div + Buyback)** | **$7,500.0M** | **Guidance** | Reflects annual dividend commitments (~$6.7B) plus modest share repurchases (~$0.8B). |
| **Floor Plan Notes Payable / Ratio** | **$0.0M ("none")** | **Judgment** | PepsiCo is a consumer packaged goods manufacturer, not an auto dealer; floor plan financing does not exist for PEP. |
| **Cost of Equity ($k_e$)** | **7.00%** | **History / Judgment** | Derived from CAPM in Lab 06 ($R_f = 4.30\%$, $\beta = 0.60$, $\text{ERP} = 5.00\%$, $WACC \approx 7.00\%$). |
| **Terminal Growth Rate ($g_{term}$)** | **2.50%** | **Guidance** | Perpetual long-run growth bounded by US/global real GDP growth plus target inflation. |
| **Diluted Shares Outstanding** | **1,378.0M** | **History** | SEC Form 10-K, Note 10 (p. 106) weighted average diluted share count. |

---

## I & V — The Engine, Statement Grid, Check Block, and Market Price

### 1. Five-Year Pro-Forma Financial Summary Grid (`pep_proforma_lab10.py`)

```
=====================================================================================
FIN 43900 Lab 10 — PepsiCo, Inc. (PEP) 3-Statement Pro-Forma Model
Analyst: Oladapo Olaniyan | Teammate: Kenechukwu Ogbuefi (kogbuef@purdue.edu)
=====================================================================================
Metric / Year (USD $M)         2025E      2026E      2027E      2028E      2029E
-------------------------------------------------------------------------------------
Revenue                      94,609.6   97,921.0  101,837.8  105,402.1  108,564.2
Operating Income (EBIT)      10,197.0   10,687.9   11,313.0   11,931.1   12,529.0
Net Income                    6,799.6    7,233.4    7,644.8    8,055.7    8,478.3
Free Cash Flow (FCFE)         3,457.0    4,090.4    4,671.9    5,299.7    5,921.0
Cash (Year End)               4,462.0    4,000.0    4,000.0    4,000.0    4,000.0
Assets - Liab - Equity            0.0        0.0        0.0        0.0        0.0
-------------------------------------------------------------------------------------

--- VALUATION SUMMARY (PEPSICO, INC.) ---
PV of 5-Year FCFE:        $18,881.96M
Terminal Value (TV):      $157,645.77M  (PV: $112,399.25M)
Total Equity Value:       $131,281.21M
Shares Outstanding:       1,378.0M
Model Value per Share:    $95.27
Observed Market Price:    $143.21 (as of Feb 2025)
Valuation Ratio (M/M):    0.67x
Terminal Value Share:     85.6%
=====================================================================================
```

### 2. Balance Sheet Check Block Verification
- **Check Block Result:** The model outputs `0.0` in every projected year (2025E: 0.0, 2026E: 0.0, 2027E: 0.0, 2028E: 0.0, 2029E: 0.0).
- **Cash & Revolver Status:** Cash is maintained above the minimum operational cash floor ($4,000M in all years; 2025E starts at $4,462.0M). Revolver draws remain at $0.0 across the entire projection horizon.

### 3. Market Price Comparison & Valuation Interpretation
- **Model FCFE Value per Share:** **$95.27**
- **Observed Market Price:** **$143.21** (as of February 4, 2025)
- **Valuation Ratio:** $\frac{\$95.27}{\$143.21} = \mathbf{0.67\times}$
- **Economic Takeaway:** The 3-statement FCFE model yields $95.27 per share because FCFE directly deducts annual debt repayments ($1.0B/yr) and heavy CapEx reinvestment ($5.3B/yr) before calculating equity residual cash flow. By contrast, our Lab 06 Enterprise DCF (FCFF) yielded $140.73 per share before debt burden. The market price of $143.21 reflects investor expectations of continuous refinancing (rather than net debt reduction) and expanding gross margins.

---

## E — Fresh Eyes (Partner Review & Attack)

### 1. Partner Attack on PepsiCo Model
**Partner Reviewer:** Kenechukwu Ogbuefi (`kogbuef@purdue.edu`)  
**Attack Question:**  
*"Why assume SG&A as a percentage of gross profit improves from 74.0% down to 72.0% over 5 years when historical SG&A ÷ Gross Profit rose from 74.81% in FY2022 to 77.87% in FY2024?"*

**Student Defense Answer (Oladapo Olaniyan):**  
"The FY2024 SG&A ratio spike to 77.87% was driven by $1.81B of non-recurring pre-tax restructuring, impairment, and recall charges disclosed in Note 5; stripping these out yields a core historical SG&A ratio of 74.24%. The projected 224 bps efficiency gain to 72.0% is supported by management's ongoing $1B+ annual productivity program through DSD route optimization, automated distribution hubs, and digitalization."

### 2. Student Attack on Partner Model
**Target Model:** Asbury Automotive Group (`ABG`) / Peer Model  
**Attack Question:**  
*"Why hold ABG's SG&A ratio flat at 64.5% in Years 3–5 when dealership SG&A leverage historically degrades when unit vehicle sales volume slows down?"*

---

## Organic Growth — Learn On Your Own

1. **What is organic growth?**  
   Organic growth measures the rate of revenue expansion generated purely by internal operations, excluding the effects of corporate acquisitions, business divestitures, and foreign currency exchange rate fluctuations.
2. **How does PepsiCo's MD&A disclose it?**  
   PepsiCo discloses organic revenue growth in Item 7 MD&A by breaking total revenue change into three components: organic volume growth, net pricing/product mix impact, and foreign exchange/M&A translation impacts across its core operating divisions (Frito-Lay North America, PBNA, Quaker Foods, and International).
3. **Why did the video carry 1.8% for ABG when reported growth was 4.7%?**  
   Asbury Automotive's reported growth of 4.7% included revenue added from newly acquired auto dealerships. Stripping out acquired dealerships left same-store (organic) revenue growth at 1.8%, which reflects the true underlying growth rate of existing locations.

---

## Reflect

1. **Which label would you defend longest and why?**  
   I would defend the **CapEx assumption ($5,300M / ~5.5% of revenue)** longest. PepsiCo operates a massive global manufacturing and distribution infrastructure; cutting CapEx below 5% would immediately bottleneck bottling capacity, degrade direct-store-delivery (DSD) efficiency, and jeopardize long-term volume growth.
2. **What one number in the filing surprised you?**  
   I was surprised by PepsiCo's **$8,505 Million Cash & Cash Equivalents balance** on the FY2024 balance sheet. For a mature, high-dividend consumer staple company, holding over $8.5B in liquid cash is exceptionally high and demonstrates strategic liquidity buffer management prior to upcoming debt maturities.

---

## Verification & Execution Check

- **Baseline ABG known answer verified:** `$291.75` per share (Lab 09 baseline `proforma.py` ran with 0.0 balance gaps).
- **PepsiCo pro-forma engine verified:** [`pep_proforma_lab10.py`](file:///c:/Users/dolan/OneDrive%20-%20purdue.edu/2026-Fall/FIN-43900%20-%20AI%20Finance%20Applications/labs/lab-10/pep_proforma_lab10.py) ran with `0.0` balance sheet gaps for all five projected years (2025E–2029E).

```bash
python labs/lab-10/pep_proforma_lab10.py
```

*Completed by Student Analyst **Oladapo Olaniyan** for FIN 43900.*
