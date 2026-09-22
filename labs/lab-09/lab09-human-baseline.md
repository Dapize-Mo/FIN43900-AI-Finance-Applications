# Lab 09 — Human Credit Baseline Switch Sheet

**Timestamp:** 2026-09-22 13:45:00 EST  
**Student Analyst:** Oladapo Olaniyan  
**Teammate / Partner:** `kogbuef@purdue.edu`  
**Course:** FIN 43900 — AI Finance Applications, Purdue University  

---

## 1. Decision Frame & 5-Cs Evidence Mapping

**Provisional Decision:** `Deeper Review` (Review required due to FCF/Debt margin and working capital sensitivity in standard baseline).

| Credit Dimension | Observable Evidence Supplied | Missing / Uncertain Evidence | Underwriting Decision Effect |
|---|---|---|---|
| **Character** | Payment history implied by baseline historical record; management governance structure. | Clean litigation check, debt covenant compliance history, bank credit reference. | Requires qualitative management check before final approval. |
| **Capacity** | Borrower A EBITDA = $150M, EBIT = $120M, Interest = $24M (Coverage = 5.00x). CFO = $100M, Capex = $50M. | Free cash flow volatility across macro stress cycles; debt maturity schedule. | Capacity is sound at 5.00x EBIT coverage, but FCF/Debt is moderate at 8.33%. |
| **Capital** | Total Debt = $600M against $150M EBITDA (Leverage = 4.00x). | Subordinated debt breakdown, equity cushion, sponsor backing. | 4.00x leverage is at the upper threshold for investment-grade credit. |
| **Collateral** | Current Assets = $250M vs Current Liabilities = $200M (Current Ratio = 1.25x). | Asset encumbrances, inventory vs. receivables breakdown, liquidation discount. | Liquidity provides short-term buffer, but non-cash collateral unverified. |
| **Conditions** | Operating environment and interest expense fixed at $24M. | Interest rate sensitivity (floating vs fixed debt), debt maturity wall in next 24M. | Refinancing risk unmeasured if market rates spike. |

---

## 2. Known-Answer Record (Borrower A Baseline Ratios)

| Ratio Name | Convention / Formula | Numerator / Denominator | Result | Reconciliation / Definition Warning |
|---|---|---|---:|---|
| **Leverage** | Gross Debt / LTM EBITDA | $600M / $150M | **4.00x** | Standard gross leverage. Leases/net debt omitted. |
| **Coverage** | EBIT / Interest Expense | ($150M - $30M) / $24M = $120M / $24M | **5.00x** | **Injected Conflict:** Using EBITDA/Interest yields **6.25x**; EBIT coverage (5.00x) is the true cash interest cushion. |
| **Liquidity** | Current Assets / Current Liabilities | $250M / $200M | **1.25x** | Current ratio. Quality of receivables/inventory uninspected. |
| **FCF / Debt** | (CFO - Capex) / Total Debt | ($100M - $50M) / $600M = $50M / $600M | **8.3333%** | Net free cash flow yield relative to principal debt. |

---

## 3. Injected Definition Conflict & Reconciliation

* **Conflict Identified:** Standard credit screens often substitute EBITDA Interest Coverage ($\text{EBITDA}/\text{Interest} = \$150\text{M}/\$24\text{M} = 6.25\text{x}$) for true operating cash coverage.
* **Reconciliation:** Depreciation and Amortization ($30M) represent real asset consumption necessary to maintain operating capacity. Using EBIT Interest Coverage ($\$120\text{M}/\$24\text{M} = 5.00\text{x}$) provides the accurate, un-distorted operating income available to service debt.

---

## 4. Underwriting Action & Reversal Conditions

* **Provisional Action:** `Deeper Review`
* **One Missing Item:** Detailed debt amortization schedule and floating vs. fixed rate breakdown.
* **Observable Reversal Condition:** If Borrower A demonstrates >85% fixed-rate debt with no maturities in the next 36 months, upgrade decision to `Approve`. If FCF/Debt drops below 5.00% under a 200 bps rate spike stress, downgrade to `Reject`.
