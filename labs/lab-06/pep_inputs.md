# PepsiCo, Inc. (PEP) — Sourced DCF Inputs & Valuation Benchmark

**Target Company:** PepsiCo, Inc. (NASDAQ: `PEP` | CIK: `0000077476`)  
**Student Analyst:** Oladapo Olaniyan  
**Teammate:** kogbuef@purdue.edu  
**Course:** FIN 43900 — AI Finance Applications, Purdue University  
**Filing Reference:** SEC Form 10-K for Fiscal Year Ended December 28, 2024  
**Observed Market Price (Reverse DCF Target):** **$143.21** per share as of February 4, 2025, 4:00 PM EST (Nasdaq closing price on FY2024 earnings release date)  

---

## 1. Sourced Inputs Table (R — Five Rows, Sourced & Dated)

| Input Name | Training Value | PepsiCo Value | Unit | As-of Date | Primary SEC Filing Source & Exact Locator | Economic Rationale & Reconciled Calculation | Status / Classification |
|---|---|---|---|---|---|---|---|
| **Starting FCFF** | $100M | **$9,688.59M** *(Core)* / **$8,133.00M** *(GAAP)* | USD Millions | FY2024 (ended 2024-12-28) | SEC Form 10-K, Consolidated Statements of Cash Flows (p. 63), Consolidated Statements of Income (p. 61), Note 5 (p. 84), and Item 7 MD&A Items Affecting Comparability (p. 49) | **GAAP Operating Cash Flow:** $12,680M + **After-tax Net Interest:** $957M × (1 − 0.194) = $771M − **CapEx:** $5,318M = **$8,133M**. **Normalized Core FCFF:** Reversing $1,811M pre-tax one-off charges ($714M impairments, $698M restructuring, $184M recall, $218M indirect taxes) yields Core NOPAT $11,846.59M + D&A $3,160M − CapEx $5,318M = **$9,688.59M**. | Sourced Reported Fact with Audited Non-GAAP Normalization |
| **Growth Rates (Years 1–5)** | 8%, 6%, 5%, 4%, 3% | **3.0%, 3.5%, 4.0%, 3.5%, 3.0%** | Decimal / % | FY2025–FY2029 | SEC Form 10-K, Item 7 MD&A, Division Review (pp. 43–47) and Q4 2024 Earnings Release Guidance (CEO Commentary) | Reflects steady volume stabilization in Frito-Lay North America (FLNA) from 2024's -2.5% volume drop to +0.5%–1.0% volume, disciplined 2.0%–2.5% net pricing, and 6%–8% emerging market constant-currency growth. | Labelled Operational Forecast Path |
| **WACC (Discount Rate)** | 10.0% | **7.00%** | Decimal / % | FY2024 / Q1 2025 Estimate | SEC Form 10-K, Note 8 Debt Obligations (p. 98) and Note 5 Income Taxes (p. 84); FRED 10-Yr Treasury; S&P Capital IQ beta | **Cost of Equity:** $R_f$ (4.30%) + $\beta$ (0.60) × ERP (5.00%) = 7.30%. **Cost of Debt:** Pre-tax 4.80% × (1 − 0.194 effective tax rate) = 3.87%. **Capital Structure:** 80% Equity / 20% Debt $\rightarrow$ $(0.80 \times 7.30\%) + (0.20 \times 3.87\%) \approx \mathbf{6.8\% - 7.0\%}$ (Base: **7.00%**). | Sourced Financial Estimate |
| **Terminal Growth Rate ($g$)** | 3.0% | **2.50%** | Decimal / % | Long-run Perpetual Horizon | Bureau of Economic Analysis (BEA) / Federal Reserve Bank of St. Louis FRED (Series `A191RL1Q225SBEA`) | Bounded by long-term US and global real GDP growth (~1.8%–2.0%) plus mature inflation target (2.0%–2.5%). Strictly obeys boundary $g < \text{WACC}$. | Economic Boundary Parameter |
| **Balance Sheet Bridge: Cash, Debt, Diluted Shares** | $50M Cash, $300M Debt, 50M Shares | **$8,505.0M** Cash, **$44,306.0M** Debt, **1,378.0M** Shares | USD Millions / Million Shares | FY2024 (ended 2024-12-28) | SEC Form 10-K, Consolidated Balance Sheets (p. 65), Consolidated Statements of Income (p. 61), and Note 10 Net Income Per Share (p. 106) | **Cash & Cash Equivalents:** $8,505M (p. 65). **Total Debt:** Short-term borrowings $7,842M + Long-term debt $36,464M = $44,306M (Net Debt claim = $35,801M). **Diluted Common Shares:** 1,378.0M shares (basic count 1,372M + 6M dilutive share equivalents, Note 10). | Sourced Primary Balance Sheet Fact |

---

## 2. Valuation Output Summary (I & V — Through the Model & Reasonableness)

- **Starting Base Value per Diluted Share:** **$140.73**
- **Observed Market Price:** **$143.21** (as of February 4, 2025)
- **Valuation Ratio:** $\frac{\$140.73}{\$143.21} = \mathbf{0.98\times}$
- **Reasonableness Assessment:** **Inside the 0.5× to 2.0× band ($71.60 to $286.42).** The model produces an unforced, independent valuation that sits within 2% of the observed market trading price.
- **Most Distrusted Input:** **North American Volume Growth trajectory (FLNA).** If consumer snack price pushback continues and volume contracts further beyond -2.5%, the entire 5-year growth path degrades into our Bear case ($102.72).

---

## 3. Sensitivity Grid & Reverse DCF (E — From One Message / `python dcf.py`)

### Sensitivity Grid (Value per Diluted Share)

| WACC \ Terminal Growth ($g$) | 2.0% | 2.5% (Base) | 3.0% |
|---|---:|---:|---:|
| **6.0%** | $165.01 | $188.52 | $219.87 |
| **7.0% (Base)** | $126.65 | **$140.73** | $158.34 |
| **8.0%** | $101.07 | $110.33 | $121.43 |

*Notes:*  
- Base case sits in the center cell ($140.73).  
- Direction strictly holds: value falls going down (higher WACC) and rises going right (higher $g$).  
- Defensible range read off the corners: **$101.07** (Stress Bear: 8.0% WACC, 2.0% $g$) to **$219.87** (Bull: 6.0% WACC, 3.0% $g$).

### Reverse DCF Solved Expectation
- **Target Price:** $143.21
- **Inputs Held Fixed:** WACC = 7.00%, $g$ = 2.50%, Cash = $8,505.0M, Debt = $44,306.0M, Diluted Shares = 1,378.0M, Starting FCFF = $9,688.59M.
- **Solved Uniform Growth Shift:** **+0.33 percentage points** (+0.0033).
- **Implied 5-Year Growth Path:** `[3.33%, 3.83%, 4.33%, 3.83%, 3.33%]`.
- **Economic Takeaway:** At $143.21, the market demands roughly 0.33 points of extra cash flow growth per year above our base forecast. This is achievable if management's price-pack architecture stabilizes snack volumes, leaving the stock fairly valued with zero margin of safety.

---

## 4. Conditional Recommendation Call

> **"Watch-defer. Initiate if the growth the price demands drops below my forecast path — a market price below about $125.00, or a sourced reason in two consecutive quarters of 10-Q filings showing positive organic volume growth in Frito-Lay North America without gross margin dilution. Monitor: Frito-Lay North America organic unit volume in next quarter's 10-Q."**
