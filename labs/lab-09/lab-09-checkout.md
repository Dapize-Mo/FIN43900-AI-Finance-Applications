# Lab 09 — Merit Checkout: Credit Evidence & Ratio Conventions

**Student Name:** Oladapo Olaniyan  
**Teammate / Partner:** `kogbuef@purdue.edu`  
**Course:** FIN 43900 — AI Finance Applications, Purdue University  
**Date:** September 22, 2026  
**Session Token:** `[INSERT IN-CLASS SESSION TOKEN HERE]`  
**Repository Link:** [`labs/lab-09`](https://github.com/Dapize-Mo/FIN43900-AI-Finance-Applications/tree/main/labs/lab-09)  

---

## 1. Header & Team Contribution
* **Lab Date:** September 22, 2026
* **Teammates / Learning Partners:** `kogbuef@purdue.edu` (Collaborative human baseline underwriting, ratio coding verification, AI flag reconciliation, and risk calibration).

---

## 2. Decision Frame
* **Borrower / Transaction:** Synthetic Borrower Credit Evaluation (Borrowers A–F).
* **Exposure & Horizon:** Senior Unsecured Credit Line, 12-Month Observation Horizon ($t_0$ to $t_0 + 12\text{M}$).
* **Decision User:** Credit Underwriting Committee / Risk Manager.
* **Available Actions:** `Approve`, `Deeper Review`, `Reject`.
* **Asymmetric Loss Logic:** 
  * **False Negative (FN / Loss Cost):** Approving an unsafe borrower ($12\text{M}$ default) results in severe principal loss (high severity).
  * **False Positive (FP / Opportunity Cost):** Rejecting or reviewing a safe borrower results in lost interest income/fees (moderate severity).

---

## 3. 5-Cs Evidence & Unknowns Matrix

| Credit Dimension | Observable Evidence Supplied | Missing / Uncertain Evidence | Decision Effect |
|---|---|---|---|
| **Character** | Historical borrower profile & payment track record. | Litigation history, credit references, management governance. | Requires qualitative background verification. |
| **Capacity** | Borrower A: EBITDA $150M, EBIT $120M, Interest $24M (EBIT Coverage 5.00x). CFO $100M, Capex $50M. | Cash flow cyclicality across macro downturns; debt maturity structure. | Capacity is sound at 5.00x EBIT coverage; FCF yield is 8.33%. |
| **Capital** | Total Debt $600M vs EBITDA $150M (Leverage 4.00x). | Subordinated debt breakdown, equity cushion, sponsor backing. | 4.00x leverage is at upper investment-grade threshold. |
| **Collateral** | Current Assets $250M vs Current Liabilities $200M (Current Ratio 1.25x). | Asset encumbrances, inventory vs receivables breakdown, liquidation discounts. | Short-term liquidity buffer present; fixed asset collateral unverified. |
| **Conditions** | Interest expense fixed at $24M. | Interest rate sensitivity (floating rate exposure), 24-month debt maturity wall. | Refinancing risk unmeasured if interest rates spike. |

---

## 4. Four Ratio Results & Documented Conventions (Borrower A Known Answers)

1. **Leverage ($\text{Total Debt} / \text{LTM EBITDA}$):**  
   $$\frac{\$600\text{M}}{\$150\text{M}} = \mathbf{4.00\text{x}}$$
2. **Coverage ($\text{EBIT} / \text{Interest Expense}$):**  
   $$\frac{\$150\text{M} - \$30\text{M}}{\$24\text{M}} = \frac{\$120\text{M}}{\$24\text{M}} = \mathbf{5.00\text{x}}$$
3. **Liquidity ($\text{Current Assets} / \text{Current Liabilities}$):**  
   $$\frac{\$250\text{M}}{\$200\text{M}} = \mathbf{1.25\text{x}}$$
4. **FCF / Debt Yield ($(\text{CFO} - \text{Capex}) / \text{Total Debt}$):**  
   $$\frac{\$100\text{M} - \$50\text{M}}{\$600\text{M}} = \frac{\$50\text{M}}{\$600\text{M}} = \mathbf{8.3333\%}$$

---

## 5. Injected-Conflict Reconciliation

* **Definition Conflict:** Substituting EBITDA Interest Coverage ($\text{EBITDA}/\text{Interest} = \$150\text{M}/\$24\text{M} = 6.25\text{x}$) overstates debt service capacity by ignoring $30M of real depreciation/amortization asset consumption.
* **Reconciliation:** Operating cash coverage must be evaluated using EBIT Interest Coverage ($\$120\text{M}/\$24\text{M} = 5.00\text{x}$) to reflect ongoing capital reinvestment required to maintain cash flows.

---

## 6. Baseline Artifact Method & Timestamp

* **Artifact Name:** `lab09-human-baseline.md`
* **File Path:** [`lab09-human-baseline.md`](file:///c:/Users/dolan/OneDrive%20-%20purdue.edu/2026-Fall/FIN-43900%20-%20AI%20Finance%20Applications/labs/lab-09/lab09-human-baseline.md)
* **Method:** Completed with AI tools closed prior to AI risk flag comparison.
* **Timestamp:** `2026-09-22 13:45:00 EST`

---

## 7. Named AI Dispositions & Source Check

| AI System | AI Risk Flag / Suggestion | Human Baseline Audit | Disposition | Rationale & Source Check |
|---|---|---|---|---|
| **Codex** | Suggested flagging Borrower D due to high leverage (5.00x). | Human baseline flagged Borrower D due to **Weak FCF/Debt (1.67%)** resulting from $90M Capex. | **Modified** | Accepted high risk flag, but modified primary reason to cash flow drain ($90M Capex out of $100M CFO). |
| **Gemini** | Suggested overriding Borrower E from `Review` to `Approve` based on strong FCF yield (17.14%). | Human baseline placed Borrower E on `Review` due to current ratio below 1.0x (0.67x). | **Rejected** | Rejected override. Working capital deficit (Current Ratio 0.67x) presents immediate refinancing risk that FCF yield cannot resolve without liquidity support. |

---

## 8. Provisional Action, Missing Evidence & Reversal Condition

* **Provisional Action:** `Deeper Review`
* **One Missing Item:** Detailed debt maturity schedule and fixed vs. floating interest rate split.
* **Observable Reversal Condition:** 
  * Upgrade to `Approve` if Borrower A provides proof of >85% fixed-rate debt with no debt maturities within 36 months.
  * Downgrade to `Reject` if FCF/Debt drops below 5.00% under a 200 bps interest rate stress test.

---

## 9. In-Person Attendance & Truth Attestation

I completed this work in today’s class with the teammate (`kogbuef@purdue.edu`) listed above, and this checkout is truthful. All reported calculations, ratio conventions, and credit decisions were verified by running `credit_screening_model.py`.

**Student Signature:** Oladapo Olaniyan  
**Date:** September 22, 2026  

---

## 10. Ungraded Growth Note

*What can you do now that you could not do before this lab, and what still feels shaky?*

> Before this lab, I relied heavily on headline EBITDA multiples to judge borrower debt capacity without scrutinizing the underlying cash conversion. Now, I understand how to compute and reconcile EBIT interest coverage against EBITDA coverage, identify cash drains through the FCF/Debt yield, and evaluate underwriting decisions using confusion matrix error costs (False Positives vs. False Negatives). What still feels shaky is balancing strict quantitative liquidity thresholds (like Current Ratio < 1.0x) against qualitative sponsor support when deciding whether to grant an underwriting override.
