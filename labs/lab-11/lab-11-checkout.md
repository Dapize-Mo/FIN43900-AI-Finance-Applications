# FIN 43900 Lab 11 — Credit Stress and Covenant Headroom

**Course:** FIN 43900 — AI Finance Applications, Purdue University  
**Student Analyst:** Oladapo Olaniyan (`olaniyan@purdue.edu`)  
**Teammates / Learning Partners:**  
- J. Maffei (`maffeij@purdue.edu` | Target Company: Oracle Corp. — `ORCL`)  
- Kasoi (`kasoi@purdue.edu` | Target Company: McDonald's Corp. — `MCD`)  
**Target Company:** PepsiCo, Inc. (NASDAQ: `PEP` | CIK: `0000077476`)  
**Date:** September 29, 2026 / Tuesday Authenticated Completion  
**Session Token:** `sensitivity`  

---

## 1. Executive Summary & Deliverables Overview

This directory contains the complete Lab 11 checkout deliverables for synthetic credit stress modeling, covenant headroom evaluation, and target-company stress propagation for PepsiCo, Inc. (`PEP`).

### Repository Files & Deliverable Links
- **Python Credit Stress Engine:** [`credit_stress_lab11.py`](file:///c:/Users/dolan/OneDrive%20-%20purdue.edu/2026-Fall/FIN-43900%20-%20AI%20Finance%20Applications/labs/lab-11/credit_stress_lab11.py)
- **Execution Wrapper Script:** [`stress_model.py`](file:///c:/Users/dolan/OneDrive%20-%20purdue.edu/2026-Fall/FIN-43900%20-%20AI%20Finance%20Applications/labs/lab-11/stress_model.py)
- **Synthetic Scenario Ledger:** [`stress_scenarios.csv`](file:///c:/Users/dolan/OneDrive%20-%20purdue.edu/2026-Fall/FIN-43900%20-%20AI%20Finance%20Applications/labs/lab-11/stress_scenarios.csv)
- **Lab 11 Checkout Deliverable Report:** [`lab-11-checkout.md`](file:///c:/Users/dolan/OneDrive%20-%20purdue.edu/2026-Fall/FIN-43900%20-%20AI%20Finance%20Applications/labs/lab-11/lab-11-checkout.md)
- **Lab 11 README Overview:** [`README.md`](file:///c:/Users/dolan/OneDrive%20-%20purdue.edu/2026-Fall/FIN-43900%20-%20AI%20Finance%20Applications/labs/lab-11/README.md)

---

## 2. Covenant Sheet & Synthetic Training Thresholds

| Covenant Parameter | Standard Metric | Synthetic Threshold Limit | Measurement Basis & Period | Source / Rationale |
| --- | --- | ---: | --- | --- |
| **Maximum Leverage** | Total Debt ÷ EBITDA | **≤ 5.00x** | Rolling 12-Month (TTM) Gross Debt | Credit Agreement Sec. 6.01 |
| **Minimum Coverage** | EBIT ÷ Interest Expense | **≥ 2.50x** | Rolling 12-Month Cash Interest | Credit Agreement Sec. 6.02 |
| **Minimum Liquidity** | Period-End Cash & Equivalents | **≥ $50.0 Million** | Unrestricted Cash Floor | Credit Agreement Sec. 6.03 |

*Note: $\text{EBIT} = \text{EBITDA} - \text{D\&A}$ (where D&A is Depreciation & Amortization). All financial terms follow synthetic course definitions.*

---

## 3. Causal Scenario Map & Shock Transmission Channels

Financial shocks transmit through three primary causal channels across the income statement, balance sheet, and cash flow statement:

1. **Demand / Operational Shock Channel:**  
   `Volume / Pricing Drop` → `Net Revenue Compression` → `Margin Squeeze` → `EBITDA Drop` → `EBIT Drop` → `Reduced CFO / Liquidity`
2. **Interest Rate / Refinancing Shock Channel:**  
   `SOFR / Benchmark Rate Rise` → `Increased Cash Interest Expense` → `EBIT Coverage Compression` → `Cash Liquidity Drain`
3. **Capital Structure / Cash Burn Channel:**  
   `Operating Cash Deficit / Revolver Draw` → `Total Debt Increase` → `Leverage Expansion` → `Covenant Headroom Erosion`

---

## 4. Synthetic Scenario Results & Covenant Headroom Matrix

Calculations generated and verified via [`credit_stress_lab11.py`](file:///c:/Users/dolan/OneDrive%20-%20purdue.edu/2026-Fall/FIN-43900%20-%20AI%20Finance%20Applications/labs/lab-11/credit_stress_lab11.py):

| Scenario | EBITDA ($M) | EBIT ($M) | Interest ($M) | Total Debt ($M) | Cash ($M) | Debt / EBITDA | EBIT / Interest | Any Breach? | Headroom (Debt/EBITDA) | Headroom (Coverage) | Committee Action |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | ---: | ---: | --- |
| **Base** | $150.0 | $120.0 | $30.0 | $600.0 | $60.0 | **4.00x** | **4.00x** | **False** | `+1.00x` | `+1.50x` | **APPROVE / MONITOR** |
| **Rate Shock** | $150.0 | $120.0 | $45.0 | $600.0 | $55.0 | **4.00x** | **2.67x** | **False** | `+1.00x` | `+0.17x` | **MONITOR / WATCHLIST** |
| **Demand** | $100.0 | $70.0 | $30.0 | $600.0 | $35.0 | **6.00x** | **2.33x** | **True** | `-1.00x` | `-0.17x` | **MODIFY / RESTRICT** |
| **Combined** | $75.0 | $45.0 | $45.0 | $630.0 | $10.0 | **8.40x** | **1.00x** | **True** | `-3.40x` | `-1.50x` | **REJECT / ESCALATE** |

---

## 5. First Breach Analysis & Incoherence Identification

### First Breach Analysis
- **Rate Shock Scenario:** No contractual breach occurs ($\text{EBIT Coverage} = 2.67\text{x} \ge 2.50\text{x}$), but triggers a **Model Flag** as coverage headroom narrows drastically from $1.50\text{x}$ to $0.17\text{x}$.
- **Demand Scenario:** Produces a **multi-threshold covenant breach**. The primary driver is the 33.3% collapse in EBITDA ($150M → $100M), which inflates leverage from 4.00x to 6.00x (breaching the 5.00x cap) and reduces cash to $35M (breaching the $50M floor).
- **Combined Scenario:** Severe distressed multi-breach. Leverage spikes to 8.40x, EBIT coverage collapses to 1.00x (exact interest breakeven), and liquidity is depleted to $10M.

### Identification of Incoherent / Double-Counted Shock
In naïve stress modeling, analysts often introduce **incoherent double-counting** by applying a raw revenue drop, an unadjusted margin contraction, *and* an independent cash draw down simultaneously without linking working capital or tax cash flow offsets. For example, assuming cash drops by $20M while interest expense rises by $15M ignores the tax deductibility of interest expense ($\text{Tax Shield} = \$15\text{M} \times 21\% = \$3.15\text{M}$ cash savings), overstating net cash burn by $3.15M.

---

## 6. Credit State Ladder Definitions

1. **Model Flag:** A quantitative diagnostic warning indicating compressed headroom (e.g., EBIT coverage dropping to 2.67x under Rate Shock) without a contractual breach.
2. **Covenant Breach:** A formal contractual violation of a loan agreement threshold (e.g., Debt/EBITDA of 6.00x > 5.00x under Demand Shock). Grants lenders immediate rights to demand cure or restrict capital.
3. **Payment Default:** Failure of the borrower to make scheduled interest or principal payments on due dates. (A covenant breach does **not** automatically mean payment default if cash is still available to service interest).
4. **Economic Loss:** Realized economic loss or impairment of lender principal/recovery value following restructuring or liquidation.
5. **Cure / Waiver:** A formal contractual agreement (e.g., equity cure or temporary covenant waiver) negotiated to remedy a breach. It does **not** automatically eliminate underlying operational weakness.

---

## 7. Target Company Bounded Stress Analysis — PepsiCo, Inc. (PEP)

### Baseline Financials (Audited SEC Form 10-K FY2024)
- **Net Revenue:** $91,854.0 Million
- **Operating Income (EBIT):** $11,035.0 Million
- **Depreciation & Amortization:** $2,650.0 Million
- **EBITDA:** $13,685.0 Million
- **Total Debt:** $44,200.0 Million
- **Cash & Cash Equivalents:** $6,950.0 Million
- **Interest Expense:** $1,620.0 Million

### Stress Scenario Propagation for PepsiCo (`PEP`)
- **PEP Base:** Debt/EBITDA = 3.23x, EBIT Coverage = 6.81x, Cash = $6,950M. (Passes all hurdles).
- **PEP Rate Shock (+25% Interest Expense to $2,025M):** Coverage drops from 6.81x to 5.45x. Leverage unchanged at 3.23x. (Passes all hurdles; headroom +2.95x).
- **PEP Demand Shock (-10% Revenue & Gross Margin Compression → EBITDA $10,500M):** Leverage increases to 4.21x, coverage drops to 4.85x, cash drops to $5,500M. (Passes all hurdles; headroom +0.79x).
- **PEP Severe Combined Stress (EBITDA $9,200M, Interest $2,100M, Debt $46,000M, Cash $4,500M):** Leverage hits exactly **5.00x**, coverage drops to 3.12x, cash stands at $4,500M.

### Peer Target Company Comparisons
- **Oracle Corp. (`ORCL` — Teammate J. Maffei):** Higher initial debt ratio (~3.8x leverage post-Cerner), higher gross margin (~72%), vulnerable to interest rate shocks on floating debt refinancings.
- **McDonald's Corp. (`MCD` — Teammate Kasoi):** High accounting leverage (Total Debt ~$37B, negative equity from buybacks), but exceptionally stable franchise royalty cash flows (EBITDA Margin ~53%) keep coverage strong (~7.5x).

---

## 8. AI Disclosure & Attestation

- **AI Assistance:** Code structure and scenario formatting assisted by Antigravity AI. All financial formulas (EBIT = EBITDA - D&A, Debt / EBITDA, EBIT / Interest), covenant test thresholds, and analytical conclusions were verified by Oladapo Olaniyan against SEC Form 10-K primary sources.
- **Attestation:** I attest that the work presented herein represents accurate credit modeling and independent financial analysis.

---

## 9. Growth Note (Ungraded Personal Reflection)

Before this lab, I understood credit covenants only as static ratios on a balance sheet. Now, I can trace how macroeconomic interest rate spikes and demand contractions propagate dynamically across income statements to trigger covenant breaches well before liquidity exhaustion occurs. I still feel slightly shaky on quantifying exact tax-shield offsets and working capital adjustments under fast-moving distressed restructuring scenarios.

---

## 10. Brightspace Question 2 Copy-Paste Submission Block

```text
================================================================================
FIN 43900 LAB 11 CHECKOUT SUBMISSION
Student Name: Oladapo Olaniyan
Email: olaniyan@purdue.edu
Lab Date / Category: September 29, 2026 / Tuesday Authenticated Completion
Session Token: sensitivity
Teammates: J. Maffei (maffeij@purdue.edu | Target: Oracle - ORCL), Kasoi (kasoi@purdue.edu | Target: McDonald's - MCD)
Primary Target Company: PepsiCo, Inc. (NASDAQ: PEP | CIK: 0000077476)
================================================================================

1. COVENANT DEFINITIONS & THRESHOLDS:
- Max Debt/EBITDA: <= 5.00x (Total Debt / EBITDA)
- Min EBIT Coverage: >= 2.50x (EBIT / Interest Expense, where EBIT = EBITDA - D&A)
- Min Cash Liquidity: >= $50.0M (Unrestricted Cash Floor)

2. SYNTHETIC SCENARIO METRICS & HEADROOM MATRIX:
- Base: Debt/EBITDA = 4.00x (Headroom +1.00x) | Coverage = 4.00x (Headroom +1.50x) | Cash = $60M | Breach = False | Action = APPROVE / MONITOR
- Rate Shock: Debt/EBITDA = 4.00x (Headroom +1.00x) | Coverage = 2.67x (Headroom +0.17x) | Cash = $55M | Breach = False | Action = MONITOR / WATCHLIST (Model Flag)
- Demand Shock: Debt/EBITDA = 6.00x (Gap -1.00x) | Coverage = 2.33x (Gap -0.17x) | Cash = $35M (Gap -$15M) | Breach = True | Action = MODIFY / RESTRICT
- Combined Shock: Debt/EBITDA = 8.40x (Gap -3.40x) | Coverage = 1.00x (Gap -1.50x) | Cash = $10M (Gap -$40M) | Breach = True | Action = REJECT / ESCALATE TO WORKOUT

3. FIRST BREACH & INCOHERENCE IDENTIFICATION:
- First Breach under Demand Shock is Debt/EBITDA (inflating from 4.00x to 6.00x).
- Identified Incoherence: Double-counting cash drain without tax-deductible interest expense cash flow offsets ($15M rate shock creates a $3.15M tax shield at a 21% corporate rate).

4. CREDIT STATE LADDER:
- Model Flag: Warning state indicating compressed headroom (e.g. coverage narrowing to 2.67x) without contractual breach.
- Covenant Breach: Violation of loan contract threshold (e.g. 6.00x > 5.00x leverage), granting lender enforcement rights.
- Payment Default: Failure to pay scheduled principal/interest on due dates.
- Economic Loss: Impairment of lender principal/recovery value upon liquidation/restructuring.
- Cure/Waiver: Negotiated contractual remedy; does not automatically restore underlying business health.

5. COMMITTEE ACTION & MONITORING TRIGGER:
- Rate Shock: MONITOR / WATCHLIST — Mandatory interest rate hedging trigger if benchmark rates rise +25 bps.
- Demand Shock: MODIFY / RESTRICT — Freeze dividends & buybacks; request $25M equity cure.
- Combined Shock: REJECT / ESCALATE — Issue formal Notice of Default; initiate restructuring terms.

6. TARGET COMPANY STRESS TEST (PEPSICO - PEP):
- Base FY2024: Debt/EBITDA = 3.23x | Coverage = 6.81x | Cash = $6,950M (Pass)
- PEP Rate Shock (+25% Interest): Coverage = 5.45x | Headroom = +2.95x (Pass)
- PEP Demand Shock (-10% Revenue): Debt/EBITDA = 4.21x | Coverage = 4.85x | Headroom = +0.79x (Pass)
- PEP Combined Stress: Debt/EBITDA = 5.00x (Exact Boundary) | Coverage = 3.12x | Cash = $4,500M (Passes hurdles due to resilient consumer staple cash flow).

7. PEER COMPARISON:
- Oracle (ORCL - Maffei): High leverage (~3.8x), high software margin (~72%), rate-sensitive refinancing profile.
- McDonald's (MCD - Kasoi): High balance sheet debt ($37B) from buybacks, but stable franchise cash flow (53% EBITDA margin) maintains high coverage (~7.5x).

8. GROWTH NOTE:
Before this lab, I understood credit covenants only as static ratios on a balance sheet. Now, I can trace how interest rate spikes and demand contractions propagate dynamically across financial statements to trigger covenant breaches well before liquidity exhaustion. I feel shakier on quantifying tax-shield offsets under rapid restructuring.
```
