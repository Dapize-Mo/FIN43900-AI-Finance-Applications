# Lab 06 Checkout — Sensitivity, Reverse DCF & Conditional Recommendation

| Metadata | Details |
|---|---|
| **Student Analyst** | **Oladapo Olaniyan** |
| **Teammate** | `kogbuef@purdue.edu` |
| **Course** | FIN 43900 — AI Finance Applications, Purdue University |
| **Session & Date** | Session 6 (Week 3, Thursday / Lab 06 Merit Checkout) |
| **Target Security** | PepsiCo, Inc. (`PEP` \| CIK: `0000077476`) |
| **Filing Reference** | SEC Form 10-K for Fiscal Year Ended December 28, 2024 |
| **Target Market Price** | **$143.21** per share (February 4, 2025 Nasdaq closing price) |

---

## 📌 Artifact Links

* **Root DCF Engine (`dcf.py`):**  
  [`dcf.py`](file:///C:/Users/dolan/OneDrive%20-%20purdue.edu/College/2026-Fall/FIN-43900%20-%20AI%20Finance%20Applications/dcf.py)
* **Lab 06 Sourced Inputs (`pep_inputs.md`):**  
  [`labs/lab-06/pep_inputs.md`](file:///C:/Users/dolan/OneDrive%20-%20purdue.edu/College/2026-Fall/FIN-43900%20-%20AI%20Finance%20Applications/labs/lab-06/pep_inputs.md)
* **Lab 06 DCF Script (`pep_dcf_model_lab06.py`):**  
  [`labs/lab-06/pep_dcf_model_lab06.py`](file:///C:/Users/dolan/OneDrive%20-%20purdue.edu/College/2026-Fall/FIN-43900%20-%20AI%20Finance%20Applications/labs/lab-06/pep_dcf_model_lab06.py)
* **Lab 06 Directory README:**  
  [`labs/lab-06/README.md`](file:///C:/Users/dolan/OneDrive%20-%20purdue.edu/College/2026-Fall/FIN-43900%20-%20AI%20Finance%20Applications/labs/lab-06/README.md)

---

## 📌 Brightspace Checkout Fields

### 1. Lab Date & Session Token
* **Lab Date:** September 10, 2026
* **Session Token:** `Reverse DCF`

### 2. Partner & Teammates
`kogbuef@purdue.edu`

### 3. Personal Contribution
Working alongside my partner (`kogbuef@purdue.edu`), I wrote and validated `dcf.py` to execute both the official training case and PepsiCo (`PEP`). On the training case, I confirmed that `dcf.py` reproduced all 12 known answers ($27.50/sh, 72.4% TV share), matched the 3x3 sensitivity grid cell for cell ($21.06 to $39.02), and solved the $30.00 target price reverse DCF shift at +1.78 percentage points. For PepsiCo, I transferred our sourced FY2024 10-K inputs ($9,688.59M normalized core FCFF base, $35,801M net debt, 1,378M diluted shares), ran our Base Case ($140.73/sh), confirmed it sits at 0.98x of market price ($143.21 on Feb 4, 2025), built the WACC/g sensitivity grid with Base in the center, solved the reverse DCF shift (+0.33 points), and defended our conditional Watch-Defer recommendation.

---

### Criterion 1: Sensitivity Grid & Direction (Merit Anchor 5/5)

#### PepsiCo Sensitivity Grid — Value per Diluted Share ($)

| WACC \ Terminal Growth ($g$) | 2.0% | 2.5% (Base Case) | 3.0% |
|---|---:|---:|---:|
| **6.0%** | $165.01 | $188.52 | $219.87 |
| **7.0% (Base Case)** | $126.65 | **$140.73** | $158.34 |
| **8.0%** | $101.07 | $110.33 | $121.43 |

* **Center Cell Check:** Base Case sits in the exact middle at **$140.73** (WACC = 7.0%, $g$ = 2.5%).
* **Directional Check (Monotonicity):** Value strictly falls going down (higher WACC) and strictly rises going right (higher $g$).
* **Defensible Range Read Off the Corners:**  
  * **Down-Left Corner (Bear / Stress Case):** WACC = 8.0%, $g$ = 2.0% $\rightarrow$ **$101.07** per share.  
  * **Up-Right Corner (Bull / Upside Case):** WACC = 6.0%, $g$ = 3.0% $\rightarrow$ **$219.87** per share.  
  * **Full Supported Range:** **$101.07 – $219.87** per share.

---

### Criterion 2: Reverse DCF (Merit Anchor 5/5)

> [!NOTE]
> **1. Training Case Reproduction First:**  
> * Target share price: **$30.00**  
> * Inputs held fixed: WACC = 10.0%, $g$ = 3.0%, Cash = $50.0M, Debt = $300.0M, Diluted Shares = 50.0M, Starting FCFF = $100.0M.  
> * **Solved Uniform Growth Shift:** **+1.78 percentage points** (+0.0178).

> [!IMPORTANT]
> **2. PepsiCo Target Company Run:**  
> * Target share price: **$143.21**  
> * Inputs held fixed: WACC = 7.00%, $g$ = 2.50%, Cash = $8,505.0M, Debt = $44,306.0M, Diluted Shares = 1,378.0M, Starting FCFF = $9,688.59M.  
> * **Solved Variable (Uniform Growth Shift):** **+0.33 percentage points** (+0.0033).  
> * Implied 5-Year Compounding Path: `[3.33%, 3.83%, 4.33%, 3.83%, 3.33%]`.  
> * **Economic Meaning:** At $143.21, the market is pricing in roughly 0.33 points of extra cash flow growth across each of the next five years compared to our base forecast.

---

### Criterion 3: Inputs & Sources (Merit Anchor 5/5)

| Input | Value & Unit | As-of Date | Primary SEC Filing Locator | Status & Sourcing Rationale |
|---|---|---|---|---|
| **Starting FCFF** | $9,688.59M (Core) / $8,133.00M (GAAP) | FY2024 (2024-12-28) | SEC Form 10-K Cash Flows (p. 63) & Income Stmt (p. 61) | **Sourced Fact with Normalization:** OCF $12,680M + Interest $771M − CapEx $5,318M + Charges $1,811M = $9,688.59M. |
| **Growth Years 1–5** | 3.0%, 3.5%, 4.0%, 3.5%, 3.0% | FY2025–FY2029 | Item 7 MD&A pp. 43–47 | **Labelled Forecast:** FLNA volume recovery + net pricing. |
| **WACC** | 7.00% | FY2024 / Q1 2025 | Note 8 Debt (p. 98) & Note 5 Taxes (p. 84) | **Labelled Estimate:** Cost of equity 7.30%, cost of debt 3.87%, 80/20 capital structure. |
| **Terminal Growth ($g$)** | 2.50% | Perpetual | BEA / FRED Series `A191RL1Q225SBEA` | **Labelled Boundary Parameter:** Bounded by real GDP + inflation. |
| **Cash, Debt, Shares** | Cash: $8,505M; Debt: $44,306M; Shares: 1,378M | FY2024 (2024-12-28) | Balance Sheet (p. 65), Note 10 (p. 106) | **Sourced Facts:** Cash $8,505M, Debt $44,306M, Diluted Shares 1,378M. |
| **Today's Market Price** | $143.21 per share | Feb 4, 2025 | Nasdaq Close | **Sourced Market Fact:** Target benchmark for Reverse DCF. |

---

### Criterion 4: Reasonableness (Merit Anchor 5/5)

* **Model Fair Value per Share:** **$140.73**
* **Observed Market Price:** **$143.21** (February 4, 2025)
* **Valuation Band Assessment:** Valuation ratio is **0.98×** ($\$140.73 / \$143.21$), sitting comfortably inside the ordinary **0.5× to 2.0× reasonableness band** ($71.60 to $286.42).
* **Distrusted Input Named with Reason:** **North American Convenient Foods Organic Volume Growth (FLNA).** FLNA organic volume declined **-2.5%** in FY2024 *(10-K Item 7, p. 45)*. If consumers continue trading down, PepsiCo will be unable to deliver 3% top-line compounding without price cuts that erode gross margins, pushing value down to the Bear case ($101.07).

---

### Criterion 5: The Conditional Call (Merit Anchor 5/5)

> **"For an investment committee with no current position, my recommendation is WATCH-DEFER. Initiate coverage with a Buy only if the market price pulls back below $125.00 (creating an adequate 12%+ margin of safety), or if SEC filings confirm two consecutive quarters of positive organic volume growth in Frito-Lay North America without promotional gross-margin erosion. Monitor: Frito-Lay North America organic unit volume in next quarter's Form 10-Q."**

---

### 6. Growth Note (Ungraded & Personal Record)

`Before this lab, I understood how to calculate DCF present values on paper, but I did not realize that value is almost entirely hostage to the terminal spread (WACC - g), which accounts for over 80% of PepsiCo's enterprise value. I can now run a reverse DCF bisection search to translate a stock price into an exact required growth shift (+0.33 points) and audit 10-K segment tables directly, but determining whether debt should be treated at book value or market value in volatile rate environments still feels like something I want to practice more.`

---

### 7. Attendance & Verification Declarations
`I completed this work in today’s class with the teammate(s) listed above, and this checkout is truthful.`
