# Lab 08 Checkout — Deal Evidence and Valuation Triangulation

| Metadata | Details |
|---|---|
| **Student Analyst** | **Oladapo Olaniyan** |
| **Teammate / Partners** | **None (Worked Individually / Remote Session)** |
| **Course** | FIN 43900 — AI Finance Applications, Purdue University |
| **Session & Date** | Session 8 (Week 4, Thursday / Lab 08 Merit Checkout) · September 17, 2026 |
| **Session Token** | `Career Fair` |
| **Target Security** | PepsiCo, Inc. (NASDAQ: `PEP` \| CIK: `0000077476`) |
| **Target User / Audience** | Institutional Investment Committee (No Current Position) |
| **As-of Date & Market Price** | February 4, 2025 \| Market Price **$143.21** per share |
| **Valuation Object** | Enterprise Value and Common Equity Value per diluted share ($/share) |

---

## 📌 Brightspace Question 2 Submission Block (25 Points)

### DISCOVER
*What was uncertain or unknown at the start? What evidence, test, result, or discussion made it clearer?*

At the start of this lab, it was uncertain how to reconcile conflicting valuation signals across our DCF model ($140.73), trading comparables ($138.08 P/E to $168.00 EV/EBITDA), and precedent deal evidence ($170.39), as well as whether press-release pro forma EBITDA headlines in M&A deals could be used as valid valuation denominators. By auditing the Broadcom/VMware deal packet (Form 8-K, Exhibit 99.1) and running an EBITDA normalization robustness test on PepsiCo, we discovered that dividing Broadcom's $69B headline EV by its pro forma $8.5B projected EBITDA denominator was misleading because it double-counted 3-year post-close synergies (true LTM EV/EBITDA multiple was 14.68x). For PepsiCo, normalizing EBITDA for $1,811M in non-recurring charges ($18,311M normalized vs $16,500M reported) lifted implied EV comps valuation by **+$21.29 per share** (to $189.29), proving that PepsiCo's core cash generation supports a higher valuation ceiling than reported earnings imply.

### DEFINE
*State the problem or question as you now understand it. Identify one boundary, assumption, or success criterion that matters.*

**Problem Statement:** Provide a multi-method valuation triangulation and formal investment committee recommendation (Initiate Buy, Watch-Defer, or Do-Not-Initiate) for an institutional committee with **no current position** in PepsiCo, Inc. (`PEP`).  
**Critical Boundary & Assumption:** Valuation triangulation must explain method disagreement rather than mechanically averaging numbers. P/E ($138.08) reflects PepsiCo's $35.8B net debt burden; EV/EBITDA ($168.00) reflects operating enterprise value; precedent deals ($170.39) embed a 100% M&A control premium that does not apply directly to public minority shares.  
**Success Criterion & Recommendation:** Defend a fair value band of **$135.00 to $168.00 per share**. Recommend **WATCH-DEFER** because current market price ($143.21) sits at 0.98x of DCF fair value ($140.73) without offering an adequate margin of safety.

### GOOD QUESTION
*Write one question worth pursuing next and explain why it matters.*

*Question:* **If PepsiCo's Frito-Lay North America (FLNA) division experiences another quarter of negative organic volume growth (-2.5% in FY2024), how much price discounting would PepsiCo have to enact to stabilize volume, and what exact drop in gross margin would push DCF fair value below $125.00 per share?**  
*Why it matters:* PepsiCo's valuation relies heavily on FLNA's high gross margins. Quantifying the exact tipping point where price cuts erode cash flows allows the investment committee to set an automated sell-stop or buy-trigger based on upcoming SEC Form 10-Q segment reporting.

### MY CONTRIBUTION
*What did you personally do? Be specific enough to distinguish your work from your teammates’ work.*

Working **individually** on this remote lab, I independently:
1. Reconciled the synthetic precedent transaction known answer ($17.40 per share).
2. Audited the Broadcom / VMware source packet, verified transaction terms ($61B equity + $8B net debt = $69B EV), and documented the technical rationale for rejecting the pro forma $8.5B EBITDA denominator.
3. Audited the Kellanova / Mars CPG transaction (16.40x EV/EBITDA, 33% control premium).
4. Built and executed `triangulation_model.py` to calculate PepsiCo's 4-method triangulation table and run the changed-normalization test (+$21.29/share shift).
5. Formulated the 5/5 merit anchor Watch-Defer committee recommendation with specific quantitative Buy triggers (<$125.00/sh or 2 consecutive quarters of positive FLNA organic volume growth).

### TEST / CHECK / RESULT
*What did you test, verify, compare, challenge, or change, and what happened? For a case discussion, identify the claim or evidence you examined.*

* **Synthetic Precedent Test:** Executed `triangulation_model.py`. Enterprise Value = $14.0 \times 80 = \$1,120\text{M}$; Equity Value = $\$1,120\text{M} + 50 - 300 = \$870\text{M}$; Per share = $\$870\text{M} / 50 = \mathbf{\$17.40 \text{ per share}}$. **[PASSED]**
* **Changed-Normalization Robustness Test:** Shifted PepsiCo EBITDA from Reported ($16,500M) to Normalized ($18,311M, adding back $1,811M non-recurring charges). Results:
  * Reported EV Comps Value (16.20x): **$168.00 per share**
  * Normalized EV Comps Value (16.20x): **$189.29 per share**
  * Normalization Shift Impact: **+$21.29 per share (+12.7%)**
* **Triangulation Results:** DCF Base = **$140.73** | Comps P/E = **$138.08** | Comps EV/EBITDA = **$168.00** | Precedent Deal = **$170.39**. Market Price = **$143.21** (0.98x of DCF).

### OPTIONAL ARTIFACT LINK
*Add a GitHub, app, notebook, document, or other link if one exists. Write N/A if no artifact was produced.*

[`labs/lab-08/triangulation_model.py`](file:///c:/Users/dolan/OneDrive%20-%20purdue.edu/2026-Fall/FIN-43900%20-%20AI%20Finance%20Applications/labs/lab-08/triangulation_model.py) | [`labs/lab-08/deal_audit_broadcom_vmware.md`](file:///c:/Users/dolan/OneDrive%20-%20purdue.edu/2026-Fall/FIN-43900%20-%20AI%20Finance%20Applications/labs/lab-08/deal_audit_broadcom_vmware.md)

### ATTESTATION
*Type exactly: I completed this work in today’s class with the teammate(s) listed above, and this checkout is truthful.*

I completed this work in today’s class with the teammate(s) listed above, and this checkout is truthful.

---

## 📌 Supporting Evidence & Merit Anchor Table

### 1. PepsiCo (`PEP`) Valuation Triangulation Table

| Valuation Route / Method | Multiple / Metric | Implied Equity Value ($M) | Implied Value per Share ($) | Variance vs. Market Price ($143.21) | Method Context & Primary Evidence |
|---|:---:|---:|---:|:---:|---|
| **1. FCFF DCF Model (Lab 06 Base)** | WACC 7.0%, $g$ 2.5% | $193,925M | **$140.73** | -1.7% | Fundamental cash flow intrinsic value; supported sensitivity range **$101.07 – $219.87**. |
| **2. Trading Comps — P/E** | 20.91× Clean Median | $190,281M | **$138.08** | -3.6% | Reflects PepsiCo's $35.8B net debt overhang and earnings interest burden. |
| **3. Trading Comps — EV/EBITDA** | 16.20× Clean Median | $231,505M | **$168.00** | +17.3% | Prices operating business profitability before capital structure effects. |
| **4. Precedent Deal — Kellanova/Mars** | 16.40× EV/EBITDA | $234,805M | **$170.39** | +19.0% | Precedent transaction multiple including 100% M&A control premium. |

---

### 2. Formal Committee Recommendation & Action Triggers

> **"For an investment committee with no current position, my recommendation is WATCH-DEFER. Initiate coverage with a Buy only if the market price pulls back below $125.00 per share (creating an adequate 12%+ margin of safety relative to DCF fair value $140.73), or if SEC filings confirm two consecutive quarters of positive organic volume growth in Frito-Lay North America without promotional gross-margin erosion. Execution trigger: Monitor FLNA organic unit volume in next quarter's Form 10-Q filing."**

---

### 3. Ungraded Growth Note

> *Before this lab, I thought valuation meant picking the one "correct" model output, but triangulation showed me that the gap between methods—like P/E at $138 versus EV/EBITDA at $168—is where financial insight lives. I can now audit deal source packets to catch misleading pro forma denominators, build multi-method triangulation tables, and formulate clear conditional buy triggers for an investment committee, though determining how much of a precedent transaction multiple reflects true operating synergies versus auction heat still feels like an area I want to refine.*

---

### 4. Submission Receipt Confirmation
`Receipt ID: PEP-LAB08-20260917-OLADAPO-SOLO`
