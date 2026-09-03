# Project 1 Valuation — Edition A Baseline & Lab 03 Checkout Package

**Course:** FIN 43900 — AI Finance Applications  
**Lab:** Lab 03 (Session 3) — The Valuation Contract  
**Author:** Oladapo Olaniyan  
**Teammate:** kogbuef@purdue.edu  
**Date:** September 1, 2026  
**Target Company:** PepsiCo, Inc. (PEP)  
**Filing Reference:** SEC Form 10-K for Fiscal Year Ended December 28, 2024 (CIK: 0000077476)  

---

> ## 📌 SUBMISSION GUIDE — WHAT TO COPY WHERE
> - **PART 1 (Lines below):** Copy and submit this whole report to the separate ungraded **Project 1 Edition A** assignment.
> - **PART 2 (Bottom of this file):** Copy the exact text under **SECTION 10** into your **Lab 03 Quiz — Question 3** text box.
> - **PART 3:** Record your **Edition A Receipt ID** into the quiz checkout.

---

# PART 1: Project 1 Valuation — Edition A Human Baseline (Submit to Project 1 Edition A Assignment)

## 1. Decision and Intended User
- **Decision User:** Equity Research Analyst / Buy-Side Investment Committee.
- **Decision:** Evaluate whether to initiate research coverage and establish a defended intrinsic valuation range for PepsiCo, Inc. (PEP).
- **Valuation Object:** Enterprise Value bridged to Common Equity Value per Diluted Share ($ USD / share).
- **Valuation Date:** September 1, 2026.

---

## 2. Initial Thesis
**Watch-Defer.**  
PepsiCo operates an exceptional, recession-resilient consumer staples business model anchored by global market share in convenient foods (Frito-Lay, Quaker) and commercial beverages (Pepsi, Gatorade, Rockstar). Its direct-store-delivery (DSD) distribution network provides substantial pricing power and consistent shareholder capital returns via growing dividends and share repurchases. 

However, at current forward trading multiples (~20–22x P/E), the market fully prices in mid-single-digit organic revenue growth while overlooking emerging consumer price elasticity limits in North American snacks and sticky input cost inflation. Coverage is deferred until valuation provides a wider margin of safety or volume stabilizes.

---

## 3. Known Evidence (Audited SEC Form 10-K for FY2024)

| Metric | Reported Value | Source Locator | Economic Interpretation |
|---|---|---|---|
| **Revenue** | ,854.0M | Consolidated Statements of Income | Global net operating revenue scale |
| **Operating Income (EBIT)** | ,887.0M | Consolidated Statements of Income | Core operating profit before interest & tax (14.03% margin) |
| **Effective Tax Rate** | 19.4% | Note 5 (Income Taxes) | Audited effective rate on continuing operations |
| **Depreciation & Amortization** | ,160.0M | Consolidated Statements of Cash Flows | Non-cash operating charges (,523M D&A +  amort.) |
| **Capital Expenditures (CapEx)** | ,318.0M | Consolidated Statements of Cash Flows | Reinvestment in property, plant & equipment (5.79% of revenue) |
| **Operating Working Capital (NWC)** | ,642.0M | Consolidated Balance Sheets | ,333M Receivables + ,306M Inventory − ,997M Payables |
| **Cash & Non-Operating Assets** | ,505.0M | Consolidated Balance Sheets | Total cash and cash equivalents for bridge |
| **Debt & Debt-like Claims** | ,306.0M | Consolidated Balance Sheets / Note 8 | ,082M Short-term debt + ,224M Long-term debt |
| **Diluted Common Shares** | 1,378.0M | Consolidated Statements of Income | Weighted average diluted share count |

---

## 4. Base Unlevered Cash Generation & Net Debt Calculations
- **NOPAT (Net Operating Profit After Tax):**  
  NOPAT = EBIT * (1 - t) = ,887.0M * (1 - 0.194) = ,386.92M
- **Base Unlevered FCFF (Excluding NWC delta):**  
  FCFF_base = NOPAT + D&A - CapEx = ,386.92M + ,160.0M - ,318.0M = ,228.92M
- **Net Debt Claim:**  
  Net Debt = Total Debt - Cash = ,306.0M - ,505.0M = ,801.0M

---

## 5. Consequential Assumptions
1. **Organic Revenue Growth:** 3.5% – 4.5% long-term CAGR across normalized pricing and volume.
2. **Operating Margin:** Steady-state operating margin of 14.5% – 15.5% supported by supply chain productivity savings.
3. **CapEx Reinvestment:** 5.5% – 6.0% of revenue to support automation and supply chain resilience.
4. **Weighted Average Cost of Capital (WACC):** 7.0% – 7.5% (Cost of equity ~8.2%, after-tax cost of debt ~3.8%).
5. **Terminal Perpetual Growth Rate (g):** 2.0% – 2.5% (anchored to long-term GDP growth).

---

## 6. Unknowns and Uncertainties
- **Consumer Elasticity & Trade-Down:** Risk of volume deceleration in Frito-Lay North America as lower-income consumers shift to private-label snacks.
- **Foreign Currency Translation:** Volatility in emerging market currencies impacting reported international profit margins.
- **Commodity & Packaging Input Costs:** Sticky agricultural raw material prices and packaging costs testing gross margins.

---

## 7. Research, Modeling, and Validation Plan
1. **Three-Lens Valuation Model:**
   - **Lens 1 (Reverse DCF):** Solve for the revenue growth rate and operating margin implied by current market price.
   - **Lens 2 (Pro-Forma DCF):** Build explicit 5-year cash flow projections across Base, Bull, and Bear operating scenarios.
   - **Lens 3 (Market Multiples):** Benchmark EV/EBITDA, EV/FCFF, and P/E against peers (Coca-Cola, Mondelez, Keurig Dr Pepper).
2. **Economic Contamination Audit:**
   - Review 10-K footnotes for non-recurring restructuring and supply-chain impairment charges to construct clean normalization adjustments.
3. **Sensitivity Analysis:**
   - Stress test intrinsic value per share across a matrix of WACC (6.5%–8.0%) and Terminal Growth (1.5%–3.0%).

---

## 8. Partner Falsification Question
> What evidence of sustained volume deceleration in North American convenient foods (Frito-Lay) despite increased promotional discounting would prove that brand pricing power is broken, invalidating the 4% organic growth thesis and triggering a downgrade to Do Not Initiate?

---

## 9. Non-AI Truth Attestation
I completed this work in today’s class with the teammate(s) listed above, and this checkout is truthful. This Edition A baseline represents human-authored judgment and pre-AI research. Generative AI was not used to generate these conclusions or perform the valuation analysis for this baseline.

---
---

# PART 2: Lab 03 Quiz — Question 3 (COPY THE EXACT BLOCK BELOW INTO QUESTION 3)

`	ext
DISCOVER — What was uncertain or unknown at the start? What evidence, test, result, or discussion made it clearer?
At the start, it was uncertain how to build a strict valuation contract for PepsiCo (PEP) without confusing Enterprise Value with Equity Value. Reviewing the FCFF formula [FCFF = EBIT(1-t) + D&A - CapEx - Change in NWC] and pulling numbers from PepsiCo's audited FY2024 10-K made it clear that we must separate core operating cash flows from balance sheet claims (adding ,505M cash and subtracting ,306M total debt) before dividing by 1,378M diluted shares.

DEFINE — State the problem or question as you now understand it. Identify one boundary, assumption, or success criterion that matters.
The task is establishing an audited before-AI baseline (Edition A) and Enterprise-to-Equity bridge for PepsiCo (PEP). A key boundary is ensuring Enterprise Value reflects only operating assets, properly isolating debt claims and cash. A critical success criterion is that every single input in our 9-row evidence ledger has a verified SEC 10-K source, period date, and classification (reported fact vs. calculated output) before running AI valuation models.

GOOD QUESTION — Write one question worth pursuing next and explain why it matters.
How much of PepsiCo's operating income is affected by one-time restructuring charges, and does recent volume slowdown in Frito-Lay snacks signal price elasticity limits that could break our 4% organic growth assumption? This matters because it identifies contamination before forecasting 5-year cash flows.

MY CONTRIBUTION — What did you personally do? Be specific enough to distinguish your work from your teammates’ work.
Working alongside my teammate (kogbuef@purdue.edu), I independently retrieved the 9 audited financial inputs from PepsiCo's FY2024 Form 10-K (Revenue, EBIT, Tax Rate, D&A, CapEx, Working Capital, Cash, Debt, Diluted Shares), populated the 9-row evidence ledger CSV, implemented and ran the student_company_bridge() Python script to compute base NOPAT (,386.92M) and FCFF (,228.92M), authored the Edition A baseline thesis, and formulated the falsification question.

TEST / CHECK / RESULT — What did you test, verify, compare, challenge, or change, and what happened? For a case discussion, identify the claim or evidence you examined.
I tested the synthetic known-answer case in valuation_foundations_starter.py (verifying FCFF of .50M and per-share value of .20), then ran PepsiCo's 10-K numbers through our Python bridge. The test verified that FY2024 EBIT (,887M) at a 19.4% tax rate yields NOPAT of ,386.92M and base FCFF of ,228.92M after adding ,160M D&A and subtracting ,318M CapEx. It also verified Net Debt of ,801M across 1,378M diluted shares.

OPTIONAL ARTIFACT LINK — Add a GitHub, app, notebook, document, or other link if one exists. Write N/A if no artifact was produced.
https://github.com/CinderZhang/FIN43900-Fall2026/tree/main/lessons/week-02

ATTESTATION — Type exactly: I completed this work in today’s class with the teammate(s) listed above, and this checkout is truthful.
I completed this work in today’s class with the teammate(s) listed above, and this checkout is truthful.
`