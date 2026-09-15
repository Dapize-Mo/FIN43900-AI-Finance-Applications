# Lab 08 Checkout — Deal Evidence and Valuation Triangulation

| Metadata | Details |
|---|---|
| **Student Analyst** | **Oladapo Olaniyan** |
| **Teammates** | **None (Worked Individually / Remote Session)** |
| **Course** | FIN 43900 — AI Finance Applications, Purdue University |
| **Lab Date & Token** | September 17, 2026 \| Session Token: `Career Fair` |
| **Target Security** | PepsiCo, Inc. (NASDAQ: `PEP` \| CIK: `0000077476`) |

---

## 📌 Brightspace Question 2 Copy-Paste Box (25 Points)

DISCOVER
Uncertain how to reconcile DCF ($140.73) vs. Comps ($138.08–$168.00) vs. Precedent Deals ($170.39) for PepsiCo (PEP), and whether pro forma M&A headline denominators are valid. Auditing the Broadcom/VMware packet proved headline pro forma $8.5B EBITDA double-counted 3-year post-close synergies (true LTM EV/EBITDA was 14.68x). Normalizing PepsiCo's EBITDA for $1,811M non-recurring charges ($18.311B vs $16.5B) shifted implied EV comps value by +$21.29/sh (to $189.29).

DEFINE
Valuation triangulation and committee action for PepsiCo, Inc. (PEP) for a committee with no current position. Key boundary: Public trading multiples ($138.08–$168.00) reflect minority shares, whereas precedent deals ($170.39) embed a 100% control premium. Recommendation: WATCH-DEFER at current market price ($143.21) with a Buy trigger below $125.00 or 2 quarters of positive FLNA volume growth.

GOOD QUESTION
What magnitude of price cuts would PepsiCo need to reverse negative FLNA organic unit volume growth (-2.5%), and at what gross margin erosion threshold does DCF fair value drop below $125.00?

MY CONTRIBUTION
Worked individually on this remote lab. Reconciled synthetic precedent known answer ($17.40), audited Broadcom/VMware and Kellanova/Mars deal source packets, built and executed `triangulation_model.py`, ran the EBITDA normalization test, and formulated the committee Watch-Defer recommendation.

TEST / CHECK / RESULT
1. Synthetic Precedent Test: Reconciled 14.0x EV/EBITDA training case -> $17.40/sh -> PASSED.
2. Normalization Test: Reported EBITDA ($16.5B) = $168.00/sh vs Normalized EBITDA ($18.311B) = $189.29/sh (+$21.29/sh shift).
3. Triangulation Summary: DCF Base = $140.73 | Comps P/E = $138.08 | Comps EV/EBITDA = $168.00 | Precedent Deal = $170.39. Market Price = $143.21 (0.98x of DCF).

OPTIONAL ARTIFACT LINK
https://github.com/Dapize-Mo/FIN43900-AI-Finance-Applications/tree/main/labs/lab-08

ATTESTATION
I completed this work in today’s class with the teammate(s) listed above, and this checkout is truthful.

---

## 📌 Detailed Repository Evidence & Triangulation Data

### PepsiCo (`PEP`) Valuation Triangulation Table

| Valuation Route / Method | Multiple / Metric | Implied Equity Value ($M) | Implied Value per Share ($) | Variance vs. Market Price ($143.21) | Method Context & Primary Evidence |
|---|:---:|---:|---:|:---:|---|
| **1. FCFF DCF Model (Lab 06 Base)** | WACC 7.0%, $g$ 2.5% | $193,925M | **$140.73** | -1.7% | Fundamental cash flow intrinsic value; supported sensitivity range **$101.07 – $219.87**. |
| **2. Trading Comps — P/E** | 20.91× Clean Median | $190,281M | **$138.08** | -3.6% | Reflects PepsiCo's $35.8B net debt overhang and earnings interest burden. |
| **3. Trading Comps — EV/EBITDA** | 16.20× Clean Median | $231,505M | **$168.00** | +17.3% | Prices operating business profitability before capital structure effects. |
| **4. Precedent Deal — Kellanova/Mars** | 16.40× EV/EBITDA | $234,805M | **$170.39** | +19.0% | Precedent transaction multiple including 100% M&A control premium. |
