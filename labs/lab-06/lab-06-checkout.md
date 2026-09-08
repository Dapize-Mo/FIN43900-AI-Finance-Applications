# Lab 06 Checkout Package — Sensitivity, Reverse DCF, and Conditional Recommendation

**Course:** FIN 43900 — AI Finance Applications, Purdue University  
**Session:** Session 6 (Week 3, Thursday / Lab 06 Merit Checkout)  
**Author / Student Name:** Oladapo Olaniyan  
**Teammate:** kogbuef@purdue.edu  
**Date:** September 8, 2026  
**Target Security:** PepsiCo, Inc. (`PEP` | CIK: `0000077476`)  
**Filing Reference:** SEC Form 10-K for Fiscal Year Ended December 28, 2024 (Accession No. `0000077476-25-000007`)  
**Target Market Price (Reverse DCF):** **$143.21** per share as of February 4, 2025 (Nasdaq close on FY2024 earnings release date)  

---

## 📌 GITHUB ARTIFACT LINKS (Required for Submission)

- **Root DCF Engine (`dcf.py`):**  
  `https://github.com/Dapize-Mo/FIN43900-AI-Finance-Applications/blob/main/dcf.py`
- **Lab 06 Sourced Inputs & Price Markdown (`pep_inputs.md`):**  
  `https://github.com/Dapize-Mo/FIN43900-AI-Finance-Applications/blob/main/labs/lab-06/pep_inputs.md`
- **Lab 06 DCF Script (`pep_dcf_model_lab06.py`):**  
  `https://github.com/Dapize-Mo/FIN43900-AI-Finance-Applications/blob/main/labs/lab-06/pep_dcf_model_lab06.py`
- **Lab 06 Directory README:**  
  `https://github.com/Dapize-Mo/FIN43900-AI-Finance-Applications/tree/main/labs/lab-06`

---

## 📌 BRIGHTSPACE LAB 06 CHECKOUT (Field-by-Field Answers & Merit Anchors)

### 1. Session Token
`[ENTER TOKEN ANNOUNCED ON CLASSROOM BOARD]`

### 2. Lab Date
`09/08/2026`

### 3. Partner & Teammates
`kogbuef@purdue.edu`

### 4. My Personal Contribution
`Working with my partner (kogbuef@purdue.edu), I wrote and validated dcf.py to execute both the official training case and PepsiCo (PEP). On the training case, I confirmed that dcf.py reproduced all 12 known answers ($27.50/sh, 72.4% TV share), matched the 3x3 sensitivity grid cell for cell ($21.06 to $39.02), and solved the $30.00 target price reverse DCF shift at +1.78 percentage points. For PepsiCo, I transferred our sourced FY2024 10-K inputs ($9,688.59M normalized core FCFF base, $35,801M net debt, 1,378M diluted shares), ran our Base Case ($140.73/sh), confirmed it sits at 0.98x of market price ($143.21 on Feb 4, 2025), built the WACC/g sensitivity grid with Base in the center, solved the reverse DCF shift (+0.33 points), and defended our conditional Watch-Defer recommendation.`

---

### Criterion 1: Grid and Direction (Merit Anchor 5/5)
*Base case in the centre; direction holds; the range read off the corners.*

**PepsiCo Sensitivity Grid — Value per Diluted Share ($):**

| WACC \ Terminal Growth ($g$) | 2.0% | 2.5% (Base Case) | 3.0% |
|---|---:|---:|---:|
| **6.0%** | $165.01 | $188.52 | $219.87 |
| **7.0% (Base Case)** | $126.65 | **$140.73** | $158.34 |
| **8.0%** | $101.07 | $110.33 | $121.43 |

- **Center Cell Check:** Base Case sits in the exact middle at **$140.73** (WACC = 7.0%, $g$ = 2.5%).
- **Directional Check (Monotonicity):** Value strictly falls going down (higher WACC: $188.52 $\rightarrow$ $140.73 $\rightarrow$ $110.33) and strictly rises going right (higher $g$: $126.65 $\rightarrow$ $140.73 $\rightarrow$ $158.34).
- **Defensible Range Read Off the Corners:**  
  - **Down-Left Corner (Bear / Stress Case):** WACC = 8.0%, $g$ = 2.0% $\rightarrow$ **$101.07** per diluted share (-28.2% vs. base).  
  - **Up-Right Corner (Bull / Upside Case):** WACC = 6.0%, $g$ = 3.0% $\rightarrow$ **$219.87** per diluted share (+56.2% vs. base).  
  - **Full Supported Range:** **$101.07 – $219.87** per share.

---

### Criterion 2: Reverse DCF (Merit Anchor 5/5)
*Solved variable and held-fixed list stated; training shift reproduced before the company run.*

**1. Training Case Reproduction First:**
- Target share price: **$30.00**
- Inputs held fixed: WACC = 10.0%, $g$ = 3.0%, Cash = $50.0M, Debt = $300.0M, Diluted Shares = 50.0M, Starting FCFF = $100.0M, Base Growth Path = `[8%, 6%, 5%, 4%, 3%]`.
- **Solved Uniform Growth Shift:** **+1.78 percentage points** (+0.0178), exactly reproducing the training benchmark.
- Implied Growth Path: `[9.78%, 7.78%, 6.78%, 5.78%, 4.78%]`.

**2. PepsiCo Target Company Run:**
- Target share price: **$143.21** (Nasdaq close on February 4, 2025 earnings release date).
- Inputs held fixed: WACC = 7.00%, Terminal Growth $g$ = 2.50%, Non-Operating Cash = $8,505.0M, Total Debt = $44,306.0M, Diluted Shares = 1,378.0M, Starting FCFF = $9,688.59M.
- **Solved Variable (Uniform Growth Shift):** **+0.33 percentage points** (+0.0033).
- Implied 5-Year Compounding Path: `[3.33%, 3.83%, 4.33%, 3.83%, 3.33%]`.
- **Economic Meaning:** At $143.21, the market is pricing in roughly 0.33 points of extra cash flow growth across each of the next five years compared to our base forecast. This is one set of assumptions consistent with the price, not proof of mispricing. It implies the market expects modest stabilization from 2024's -2.0% volume contraction.

---

### Criterion 3: Inputs and Sources (Merit Anchor 5/5)
*Every row has a locator and an as-of date; unresolved, placeholder, and estimate labelled.*

| Input | Value & Unit | As-of Date | Primary SEC Filing Locator | Status & Sourcing Rationale |
|---|---|---|---|---|
| **Starting FCFF** | $9,688.59M (Core) / $8,133.00M (GAAP) | FY2024 (ended 2024-12-28) | SEC Form 10-K: Cash Flow Statement (p. 63), Income Statement (p. 61), Note 5 (p. 84), Item 7 p. 49 | **Sourced Fact with Audited Normalization:** GAAP Cash Flow = Operating Cash ($12,680M) + After-tax Net Interest ($957M × (1 − 0.194) = $771M) − CapEx ($5,318M) = $8,133M. Core FCFF reverses $1,811M one-off charges ($714M impairments, $698M restructuring, $184M recall, $218M indirect tax) to yield $9,688.59M. |
| **Growth Years 1–5** | 3.0%, 3.5%, 4.0%, 3.5%, 3.0% | FY2025–FY2029 | SEC Form 10-K, Item 7 MD&A pp. 43–47, Q4 2024 Earnings Call Transcript (CEO Remarks, p. 3) | **Labelled Forecast:** Reflects gradual recovery in Frito-Lay North America (FLNA) volume from -2.5% to +0.5%–1.0%, disciplined net pricing (+2.0% to +2.5%), and continued emerging market expansion. |
| **WACC** | 7.00% | FY2024 / Q1 2025 | SEC Form 10-K Note 8 (Debt, p. 98) & Note 5 (Taxes, p. 84); FRED 10-Yr Treasury; S&P beta | **Labelled Estimate:** Cost of equity = 4.30% $R_f$ + 0.60 $\beta$ × 5.0% ERP = 7.30%. After-tax cost of debt = 4.80% × (1 − 0.194) = 3.87%. Capital structure 80% equity / 20% debt yields ~6.8%–7.0%. |
| **Terminal Growth ($g$)** | 2.50% | Perpetual Horizon | BEA / FRED Series `A191RL1Q225SBEA` (US Long-Run GDP) | **Labelled Boundary Parameter:** Anchored to long-run nominal US/global GDP growth (~2.0%–2.5%). Strictly satisfies $g < \text{WACC}$. |
| **Cash, Debt, Shares** | Cash: $8,505.0M; Debt: $44,306.0M; Shares: 1,378.0M | FY2024 (ended 2024-12-28) | SEC Form 10-K: Balance Sheet (p. 65), Income Statement (p. 61), Note 10 (p. 106) | **Sourced Reported Facts:** Cash and cash equivalents ($8,505M); Short-term borrowings ($7,842M) + Long-term debt ($36,464M) = $44,306M (Net Debt claim = $35,801M); Diluted weighted-average common shares = 1,378.0M shares. |
| **Today's Market Price** | $143.21 per share | February 4, 2025, 4:00 PM EST | Nasdaq Official Close (Q4/FY2024 Earnings Release Day) | **Sourced Market Fact:** Target benchmark for Reverse DCF. |

---

### Criterion 4: Reasonableness (Merit Anchor 5/5)
*Value beside price, band stated, distrusted input named with a reason.*

- **Model Fair Value per Share:** **$140.73**
- **Observed Market Price:** **$143.21** (February 4, 2025)
- **Valuation Band Assessment:** The valuation ratio is **0.98×** ($\$140.73 / \$143.21$). This sits comfortably inside the ordinary **0.5× to 2.0× reasonableness band** ($71.60 to $286.42), demonstrating that our independently audited model and the market are pricing PepsiCo within 2% of each other.
- **Distrusted Input Named with Reason:** **North American Convenient Foods Organic Volume Growth (FLNA).** FLNA organic volume declined **-2.5%** in FY2024 *(10-K Item 7, p. 45)* as consumers pushed back against three years of cumulative 20%+ price increases. If consumers continue to trade down to private-label snacks or eat fewer packaged convenience foods, PepsiCo will be unable to deliver even 3% top-line compounding without price cuts that erode gross margins. This is the single load-bearing assumption that could force our valuation down to the Bear case ($101.07).

---

### Criterion 5: The Conditional Call (Merit Anchor 5/5)
*A real call, a condition that flips it, something to monitor.*

> **"For an investment committee with no current position, my recommendation is WATCH-DEFER. Initiate coverage with a Buy only if the market price pulls back below $125.00 (creating an adequate 12%+ margin of safety), or if SEC filings confirm two consecutive quarters of positive organic volume growth in Frito-Lay North America without promotional gross-margin erosion. Monitor: Frito-Lay North America organic unit volume in next quarter's Form 10-Q."**

---

### 6. Growth Note (Ungraded, Yours Alone)
`Before this lab, I understood how to calculate DCF present values on paper, but I did not realize that value is almost entirely hostage to the terminal spread (WACC - g), which accounts for over 80% of PepsiCo's enterprise value. I can now run a reverse DCF bisection search to translate a stock price into an exact required growth shift (+0.33 points) and audit 10-K segment tables directly, but determining whether debt should be treated at book value or market value in volatile rate environments still feels like something I want to practice more.`

### 7. In-Person Attendance Declaration & Truth Attestation
`I completed this work in today’s class with the teammate(s) listed above, and this checkout is truthful.`
