# Lab 06 Checkout Package — Sensitivity, Reverse DCF, and Conditional Recommendation

**Course:** FIN 43900 — AI Finance Applications, Purdue University  
**Session:** Session 6 (Week 3, Thursday / Lab 06 Merit Checkout, 0–25)  
**Author / Student Name:** Oladapo Olaniyan  
**Teammate:** kogbuef@purdue.edu  
**Date:** September 8, 2026  
**Target Security:** PepsiCo, Inc. (`PEP` | CIK: `0000077476`)  
**Filing Reference:** SEC Form 10-K for Fiscal Year Ended December 28, 2024 (Accession No. `0000077476-25-000007`)  

---

## 📌 BRIGHTSPACE LAB 06 CHECKOUT SUBMISSION (Field-by-Field Answers)

### 1. Session Token
`[ENTER TOKEN ANNOUNCED ON CLASSROOM BOARD]`

### 2. Lab Date
`09/08/2026`

### 3. Partner & Teammates
`kogbuef@purdue.edu`

### 4. My Personal Contribution
`Working alongside my partner (kogbuef@purdue.edu), I implemented and verified the four required STUDENT_WORK functions (project_fcff, value_dcf, sensitivity_table, and reverse_dcf_for_growth) in Python. I first confirmed our engine against the synthetic training case (dcf_case.csv / dcf_expected_output.csv), matching all 12 checkpoints within tolerance (including $27.50/sh value and 72.4% TV share). I then transferred PepsiCo's audited Week 2/Lab 04 evidence ($9,688.59M normalized core FCFF base, $35,801M net debt, 1,378.0M diluted shares) into causal Low, Base, and High scenarios. I generated the 5x4 WACC/terminal-growth sensitivity grid, mathematically verified monotonic consistency, calculated base (81.0%) and stress (76.8%) terminal value concentrations, executed a binary search reverse DCF solving for PepsiCo's market-implied growth rate (3.73%), audited bull and bear claims from Google Gemini and ChatGPT/Codex against SEC Form 10-K Item 7 disclosures, and established our defended Watch-Defer conditional recommendation and volume reversal trigger.`

### 5. Decision Call and Valuation Convention
```text
Decision Call: watch-defer: wait for more information before making decision

Valuation Convention:
- Target Security: PepsiCo, Inc. (NASDAQ: PEP | CIK: 0000077476)
- Currency & Unit: Annual FCFF in USD millions; diluted common shares in millions; per-share value in USD.
- Explicit Period: 5 explicit forecast years (FY2025–FY2029); cash flows arrive at year-end.
- Discounting: Weighted Average Cost of Capital (WACC) discounts unlevered FCFF.
- Terminal Value: Gordon Growth model evaluated at the end of Year 5: TV_5 = FCFF_5 * (1 + g) / (WACC - g), with hard boundary g < WACC strictly enforced.
- Enterprise-to-Equity Bridge: Equity Value = Enterprise Value + Non-Operating Cash ($8,505.0M) - Total Debt Claims ($44,306.0M) = EV - Net Debt ($35,801.0M).
- Diluted Share Count: Divided by 1,378.0M diluted common shares (reconciled to 10-K Income Statement).
```

### 6. Low / Base / High Scenarios and Causal Operating Drivers
```text
Causal Story & Scenario Definitions:

1. Base Case — Per-Share Value: $140.73 | EV: $229,731.6M | TV Share: 81.0%
   - Story: Modest volume stabilization (+0.5% to +1.0%) combined with disciplined net pricing (+2.0% to +2.5%). Frito-Lay North America (FLNA) stabilizes after the 2024 price-resistance shock.
   - Operating Assumptions: Starting FCFF = $9,688.59M. FCFF growth path = [3.0%, 3.5%, 4.0%, 3.5%, 3.0%] over Years 1–5. Core operating margin sustained at ~16.0%. CapEx stable at 5.5% of sales.
   - Valuation Drivers: WACC = 7.00% (cost of equity ~7.5%, after-tax cost of debt ~3.8%), Terminal Growth g = 2.50% (aligned with long-run nominal US/global GDP growth).

2. Low (Bear) Case — Per-Share Value: $102.72 | EV: $177,342.9M | TV Share: 76.8%
   - Story: The consumer price elasticity wall in North America persists. Private-label snack brands capture shelf space, forcing PepsiCo to implement margin-diluting promotional discounts. International emerging market FX devaluations accelerate.
   - What Moves Together & Why:
     * FCFF growth slows to [1.5%, 2.0%, 2.0%, 1.5%, 1.5%] due to volume stagnation and lost pricing power.
     * Core operating margin compresses ~100 bps to ~15.0% as promotional spending increases while supply chain automation CapEx remains non-discretionary (elevating reinvestment intensity).
     * WACC rises 50 bps to 7.50% reflecting higher operating volatility and consumer staples cyclicality.
     * Terminal growth fades to 2.00% (reflecting mature staple drag below global GDP).

3. High (Bull) Case — Per-Share Value: $170.48 | EV: $270,725.6M | TV Share: 83.0%
   - Story: Price-pack architecture innovation succeeds in restoring FLNA volume growth (+2.0%), while international divisions (AMESA, Europe, APAC) maintain high-single-digit organic growth. Factory automation under the 2019 Multi-Year Productivity Plan yields record cost savings.
   - What Moves Together & Why:
     * FCFF growth accelerates to [5.0%, 5.0%, 4.5%, 4.0%, 3.5%].
     * Core operating margin expands ~80 bps to 16.8% via automation and supply chain scale.
     * CapEx intensity normalizes toward 5.0% of revenue as initial automation rollouts conclude.
     * WACC declines 50 bps to 6.50% due to steady cash flow predictability and debt paydown.
     * Terminal growth remains bounded at 2.50%.
```

### 7. WACC / Terminal Growth Grid Excerpt and Monotonicity Result
```text
PepsiCo Per-Share Valuation Sensitivity Grid ($ per diluted share):

Terminal Growth (g) \ WACC     6.00%      6.50%      7.00% (Base)   7.50%      8.00%
--------------------------------------------------------------------------------------
1.50%                         $146.73    $129.34    $115.12       $103.27     $93.24
2.00%                         $165.01    $143.70    $126.65       $112.69    $101.07
2.50% (Base)                  $188.52    $161.64    $140.73       $124.01    $110.33
3.00%                         $219.87    $184.71    $158.34       $137.84    $121.43

Monotonicity Verification: PASSED
- Horizontal Test (WACC): In every row, as WACC increases from 6.00% to 8.00%, per-share value strictly decreases (e.g., at g=2.5%, $188.52 -> $161.64 -> $140.73 -> $124.01 -> $110.33).
- Vertical Test (Terminal Growth): In every column, as g increases from 1.50% to 3.00%, per-share value strictly increases (e.g., at WACC=7.0%, $115.12 -> $126.65 -> $140.73 -> $158.34).
- Boundary Condition: All cells strictly satisfy g < WACC; any hypothetical cell with g >= WACC is mathematically blanked to prevent division-by-zero or negative denominator distortion.
```

### 8. Terminal-Value Shares and Interpretation
```text
Terminal-Value Concentration:
- Base Case TV Share: 81.0% of Enterprise Value (PV of TV = $186,134.1M / EV = $229,731.6M)
- Stress (Low) Case TV Share: 76.8% of Enterprise Value (PV of TV = $136,252.7M / EV = $177,342.9M)

Financial Interpretation:
A terminal value concentration between 76% and 81% is standard for a mature, cash-generative consumer staples giant like PepsiCo. Because more than three-quarters of enterprise value lives beyond the 5-year explicit forecast horizon, the model's output is fundamentally hostage to the terminal spread (WACC - g = 0.070 - 0.025 = 0.045). A mere 50 bp increase in WACC (7.0% -> 7.5%) erodes per-share value by $16.72 (-11.9%), whereas shifting Year 1 FCFF growth by 100 bp alters equity value by less than $0.70/share. Therefore, our investment defense must focus on interest rate regime duration, credit spread stability, and long-run consumer pricing power rather than short-term quarterly noise.
```

### 9. Reverse-DCF Solved Assumption & Economic Interpretation
```text
Market Data & Benchmark:
- Target Market Price: $143.21 per diluted share
- As-of Date & Source: February 4, 2025 (Nasdaq closing price on FY2024 earnings release date)
- Reconciled Market EV: $233,144.4M (Equity Value $197,343.4M + Net Debt $35,801.0M)

Solved Implied Assumption (Reverse DCF via Binary Search):
- Fixed Parameters: WACC = 7.00%, Terminal Growth g = 2.50%, Net Debt = $35,801.0M, Diluted Shares = 1,378.0M, Starting FCFF = $9,688.59M.
- Solved Implied 5-Year Constant FCFF Growth Rate: 3.73% per annum.

Economic Interpretation:
At PepsiCo's observed price of $143.21, the market is pricing in exactly 3.73% annualized FCFF growth over the next five years. Economically, this expectation is plausible but demanding: PepsiCo achieved 2.0% organic revenue growth in FY2024 amidst a -2.0% volume contraction. To deliver 3.73% cash flow compounding, management must halt snack volume attrition in Frito-Lay North America (-2.5% in 2024) and successfully realize guided productivity savings. The market is effectively pricing PepsiCo at fair value under a mild operational turnaround, offering virtually zero margin of safety against further consumer price pushback.
```

### 10. AI Bull / Bear Claim Checks with Primary Sources & Dispositions
```text
1. System 1 (Google Gemini) — Bear Challenge Check:
   - AI Claim: "Gemini claimed that PepsiCo's Frito-Lay North America division experienced a severe operating profit collapse of over 15% in FY2024 due to consumer boycotts and snack category volume losses."
   - Primary Source & Locator: SEC Form 10-K for FY2024, Item 7 (MD&A), Results of Operations — Division Review: FLNA, p. 45 and Table of Items Affecting Comparability, p. 49.
   - Primary Evidence: FLNA net revenue declined 1% and reported operating profit decreased 7% (from $6,777M to $6,316M), while Core constant currency operating profit declined 5%. Unit volume fell 2.5%, offset by +2.0% net pricing. The filing cites consumer price sensitivity and strategic investments, with no mention of boycotts.
   - Disposition: CORRECT. We keep the underlying economic driver (volume resistance of -2.5% in FLNA capping top-line growth and compressing margin), but correct the magnitude from "over 15% collapse" to a 7% reported / 5% core decline and remove the unsubstantiated boycott claim.

2. System 2 (ChatGPT / Codex) — Bull Challenge Check:
   - AI Claim: "ChatGPT claimed that PepsiCo's international convenience foods business delivered double-digit volume growth across emerging markets, which will fully neutralize North American domestic softness."
   - Primary Source & Locator: SEC Form 10-K for FY2024, Item 7 (MD&A), Division Review — LatAm (p. 46), Europe (p. 46), AMESA (p. 46), APAC (p. 47).
   - Primary Evidence: While specific countries saw double-digit volume expansion (e.g., India convenient foods double-digit, Thailand double-digit), consolidated division convenient foods volume grew only +2% in AMESA, +2% in Europe, +4% in APAC, and actually DECLINED -2% in Latin America (driven by double-digit declines in Peru and Argentina). Furthermore, severe foreign exchange translation headwinds reduced AMESA operating profit by 8% and LatAm net revenue by 3%.
   - Disposition: QUALIFY. We accept that emerging markets offer essential geographic diversification and high organic revenue growth (+10% in AMESA), but qualify the claim because aggregate international volume grew only 2–4% (with LatAm contracting) and currency devaluations substantially erode dollar-denominated cash flows.
```

### 11. Defended Range, Conditional Recommendation, and Reversal Trigger
```text
Decision Statement:
"My supported valuation range is $102.72 – $170.48 per diluted share (Base Case: $140.73) versus an observed market price of $143.21 as of February 4, 2025 (Nasdaq closing price / FY2024 SEC earnings release). The conclusion is most sensitive to the WACC discount rate (a 50 bp shift changes per-share value by ~$16.70) and North American convenient foods volume stabilization. For a committee with no current position, I recommend WATCH-DEFER. I would move to Initiate-Buy only if a market pullback brings the price below $125.00 (providing a 12%+ margin of safety) OR if Frito-Lay North America achieves two consecutive quarters of positive organic volume growth without gross margin-diluting promotions; revisit immediately if quarterly 10-Q reports show convenient foods volume contractions steepening beyond -3.0%, which would trigger our Low/Bear case ($102.72). Terminal value represents 81.0% of enterprise value, so long-term interest rate and terminal growth assumptions remain material model limitations."
```

### 12. Artifact Link
`https://github.com/Dapize-Mo/FIN43900-AI-Finance-Applications/tree/main/labs/lab-06`  
*(Local file: labs/lab-06/pep_dcf_model_lab06.py and labs/lab-06/lab-06-checkout.md)*

### 13. Growth Note (Ungraded, Yours Alone)
`On Tuesday I understood how to calculate DCF cash flows and present values mechanically, but today's lab taught me what actually moves the number: value is fundamentally hostage to the terminal spread (WACC - g), which accounts for over 80% of enterprise value. I can now run a reverse DCF to translate a stock price into an implied growth rate (3.73%) and audit AI claims directly against 10-K division tables, but estimating the exact debt-equity capital structure weighting under volatile rate environments still feels like something I want to practice more.`

### 14. In-Person Attendance Declaration & Truth Attestation
`I completed this work in today’s class with the teammate(s) listed above, and this checkout is truthful.`

---

*This checkout package was prepared for FIN 43900 (AI Finance Applications, Purdue University) by Oladapo Olaniyan. All models, calculations, sensitivity tables, and source checks were independently executed and verified in Python.*
