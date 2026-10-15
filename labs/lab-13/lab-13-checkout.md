# FIN 43900 Lab 13 — Portfolio Mandate Defense

**Course:** FIN 43900 — AI Finance Applications, Purdue University  
**Student Analyst:** **Oladapo Olaniyan** (`oolaniy@purdue.edu`)  
**Institution:** Mitchell E. Daniels, Jr. School of Business, Purdue University  
**Case:** Meridian Foundation Reserve (Fictional Course Common Case)  
**As-Of Date:** October 15, 2026  
**Session Token:** `CFA Investment`  
**Brightspace Item:** Lab 13 — Portfolio Mandate Defense (Thursday Merit Checkout, 25 Points)  

---

## 📌 1. Executive Summary & Deliverable Links

This checkout delivers the complete mandate defense and rule verification package for the **$100 million Meridian Foundation Reserve**. Before selecting or executing any mathematical portfolio optimizer, this analysis formalizes the CIO's qualitative requests into a rigorous decision contract, tests candidate portfolios against all checkable mandate constraints via a standard-library Python engine ([`mandate.py`](mandate.py)), compares two competing AI operational interpretations, and escalates foundational ambiguities requiring committee governance.

### Repository Links & Artifacts
- **Mandate Defense Worksheet:** [`lab-13-mandate-defense-worksheet.md`](lab-13-mandate-defense-worksheet.md)
- **Standard-Library Rule Checker:** [`mandate.py`](mandate.py)
- **Lab 13 Directory README:** [`README.md`](README.md)
- **GitHub Direct Worksheet Link:** [lab-13-mandate-defense-worksheet.md on GitHub](https://github.com/Dapize-Mo/FIN43900-AI-Finance-Applications/blob/main/labs/lab-13/lab-13-mandate-defense-worksheet.md)
- **GitHub Direct Script Link:** [mandate.py on GitHub](https://github.com/Dapize-Mo/FIN43900-AI-Finance-Applications/blob/main/labs/lab-13/mandate.py)

---

## 2. Decision Contract & Boundary Definitions

| Dimension | Specification | Source / Governing Fact | Fiduciary Rationale |
|---|---|---|---|
| **Intended User** | Investment Committee & CIO of Meridian Foundation | Common CIO Case § Decision Request | Governs fiduciary policy for the endowment reserve |
| **Immediate Action** | Authorize analytical mandate and pilot sizing (not live trade execution) | Common CIO Case § Decision Request | Pre-commits constraints before running quantitative optimizers |
| **Portfolio Horizon** | Seven (7) years with quarterly review & annual rebalancing | Fact S1 | Aligns with foundation capital commitment cycle |
| **Investable Universe** | Cash, U.S. Treasuries, Diversified Equity/Bond/Real Estate Funds, Approved Single Equities/Bonds | Live Case Holdings Table | Excludes unapproved asset classes, illiquid vehicles, or raw commodities |
| **As-Of Boundary** | October 15, 2026 | Case As-Of Fact | Strict information boundary; excludes post-date market data |
| **Stated Objective** | CPI + 4.0% annualized net of fees over rolling 5-year periods | Fact S2 | Measurable purchasing-power preservation objective |
| **Policy Benchmark** | 60% broad global equities / 40% U.S. investment-grade bonds | Fact S4 | Strategic asset allocation anchor and risk reference |
| **Naive Baseline** | Static 60/40 benchmark with cash reserve carved out | Fact S4 | Default counterfactual to justify any active tracking risk |

---

## 3. Human-First Statement Classification (S1–S10)

Classified independently without AI per course instructions:

| ID | CIO Statement | Classification | Governing Rationale |
|---|---|---|---|
| **S1** | Horizon seven years; annual rebalancing. | **Hard constraint** | Imposes non-negotiable structural rules dictating a fixed seven-year horizon and mandatory annual rebalancing schedule. |
| **S2** | Objective: CPI + 4% a year, net of costs, over rolling five-year periods. | **Objective** | Specifies the target quantitative outcome that portfolio design seeks to attain over rolling five-year measurement windows. |
| **S3** | Pays out $0.75 million every quarter; twelve months of payouts held in cash or daily-liquid government securities. | **Hard constraint** | Sets an absolute cash distribution requirement ($3.0M / 3.0% floor) that must be held in daily-liquid sovereign paper or cash. |
| **S4** | Benchmark: 60% global equities, 40% U.S. investment-grade bonds. | **Preference** | Establishes the strategic asset allocation guideline and performance hurdle, guiding portfolio balance while allowing active tracking tradeoffs. |
| **S5** | Long-only: no borrowing, short sales, or derivatives. | **Hard constraint** | Explicit contractual boundary strictly prohibiting leverage, short exposure, and derivative contracts. |
| **S6** | No single issuer above 8%. | **Hard constraint** | Enforces a strict diversification floor capping aggregate exposure to any single corporate issuer at 8%. |
| **S7** | Annual turnover at most 25% without committee approval. | **Preference** | Operates as a desirable trading friction ceiling that allows exceptions whenever explicit committee authorization is granted. |
| **S8** | At least 90% redeemable within five business days. | **Hard constraint** | Quantitative liquidity floor requiring 90% of assets to convert to cash within 5 business days under normal market conditions. |
| **S9** | “The reserve cannot have a calendar-year loss greater than 10%.” No measure, no breach rule. | **Unverifiable promise** | Expresses an unachievable absolute guarantee in public long-only markets without shorting/derivatives, lacking confidence level, risk metric, or breach protocol. |
| **S10** | No sector, ESG, tax, or home-bias preference; nobody has said what the pilot should optimize. | **Missing** | Identifies a fundamental gap: the CIO has not specified the core utility function or optimization objective for the pilot portfolio. |

---

## 4. Standard-Library Rule Engine & Validation Matrix

The mechanical rule checker [`mandate.py`](mandate.py) was built using Python standard library only (`collections.defaultdict`, `copy.deepcopy`, `sys`). It evaluates the reserve minimum ($4 \times \$0.75\text{M} / \$100\text{M} = 3.0\%$), 5-day liquidity ($\ge 90\%$), single-issuer concentration cap ($\le 8\%$, exempting cash, Treasuries, and diversified funds), allocation sum ($100.0\%$), and long-only minimum ($\ge 0\%$).

### Candidate Reconciliation & Probe Matrix

| Check / Metric | Rule Hurdle | Candidate A | Candidate B | Candidate C | Candidate D | Candidate A Probe |
|---|---|---:|---:|---:|---:|---:|
| **Allocation Sum** | Exactly 100.0% | 100.0% (pass) | 100.0% (pass) | 100.0% (pass) | 100.0% (pass) | 100.0% (pass) |
| **Lowest Holding Weight** | $\ge 0.0\%$ (Long-Only) | 0.0% (pass) | 0.0% (pass) | 0.0% (pass) | 0.0% (pass) | **-2.0% (FAIL)** |
| **Reserve Floor** | $\ge 3.0\%$ ($4 \times \$0.75\text{M}$) | 14.0% (pass) | **1.0% (FAIL)** | **2.0% (FAIL)** | 4.0% (pass) | 10.0% (pass) |
| **5-Day Liquidity** | $\ge 90.0\%$ | 100.0% (pass) | **85.0% (FAIL)** | 100.0% (pass) | 100.0% (pass) | 100.0% (pass) |
| **Single Issuer Cap** | $\le 8.0\%$ (Non-Exempt) | 0.0% (pass) | **9.0% (FAIL)** | 8.0% (pass) | 0.0% (pass) | 0.0% (pass) |
| **Calendar-Year Loss** | Unverifiable Guarantee | *requires CIO clarification* | *requires CIO clarification* | *requires CIO clarification* | *requires CIO clarification* | *requires CIO clarification* |
| **Overall Verdict** | All Coded Rules | **Passes every rule** | **Fails 3 rules** | **Fails 1 rule** | **Passes every rule** | **Fails 1 rule** |

*Verification Note:* Candidate A negative-weight probe verifies that setting Cash to -2.0% and Global Equity to 64.0% triggers an immediate `FAIL` on long-only while keeping other checkable rules intact.

---

## 5. Candidate D Challenge & Skeptical Colleague Review

### Candidate D Profile
- **Allocation:** 4% Cash, 96% Global Equity Index Fund, 0% Fixed Income.
- **Checker Result:** Passes 100% of coded checks (Allocation = 100%, Min Weight = 0%, Reserve = 4% $\ge$ 3%, Liquidity = 100% $\ge$ 90%, Issuer Cap = 0% $\le$ 8%).

### Two-Sentence AI-Closed Judgment
> The CIO's objection against Candidate D firmly holds because allocating 96% to equities and 0% to fixed income completely abandons the strategic asset allocation intent of **S4** (the 60% equity / 40% bond policy benchmark). Furthermore, exposing the reserve to unmitigated equity drawdowns guarantees a catastrophic breach of **S9** (the 10% maximum calendar-year loss ceiling) during any standard equity market downturn.

### Skeptical Colleague Check
> If a partner analyst submits a candidate seeking to boost yield via an aggressive allocation to private real estate or high-turnover tactical credit, I would cite **S8** (mandatory 90% liquidity within 5 business days) and **S7** (annual turnover capped at 25% without committee approval) to disqualify the proposal before optimization.

---

## 6. Two AI Operational Interpretation Dispositions

Per the common course prompt, two competing interpretations were evaluated against the dated facts:

### Interpretation 1: Relative-Return / Benchmark-Tracking Mandate
- **Proposed Formulation:** Minimize tracking error against the 60/40 benchmark while targeting CPI + 4% over rolling 5 years; treat the 10% calendar-year loss statement as an informal aspiration secondary to benchmark tracking.
- **Disposition:** **REQUIRES CLARIFICATION** (Governing Facts: **S9** & **S10**).
- **Reasoning:** While S4 explicitly provides a 60/40 benchmark, the CIO never declared whether tracking error takes priority over capital preservation. If the 60/40 benchmark suffers a -15% down year (as in 2008 or 2022), this interpretation guarantees a breach of S9.

### Interpretation 2: Absolute-Return / Downside-Protected Liability Mandate
- **Proposed Formulation:** Maximize expected return subject to an absolute 1-year Value-at-Risk / CVaR loss constraint $\le 10\%$; dynamically shift capital into short-term cash/Treasuries to protect the $3.0M liquidity floor.
- **Disposition:** **UNSUPPORTED** (Governing Facts: **S5** & **S9**).
- **Reasoning:** S5 explicitly forbids derivatives, borrowing, and short sales. In a long-only cash/bond/equity universe, absolute downside floor protection without options requires holding prohibitive cash allocations (>60%), which guarantees the portfolio will fail the S2 real return objective of CPI + 4%.

---

## 7. Escalation Question & Investment Policy Statement (IPS) Mapping

### Core Escalation Question for the CIO
> **"Before we select an optimization algorithm, what explicit mathematical utility function governs the pilot (e.g., maximizing expected return above CPI + 4% vs. minimizing tracking error relative to the 60/40 benchmark), and how must the 'no calendar-year loss greater than 10%' constraint be enforced when market drawdowns dictate an unavoidable breach?"**

### What Answer Would Change Portfolio Design?
- **If Tracking Error Primary:** The optimizer will bound asset weights tightly around 60% equities and 40% bonds, accepting drawdown risk in broad market declines.
- **If Loss Avoidance Primary:** The optimizer must cap equity weight well below 30% and shift the bulk of the portfolio into short-duration Treasuries and cash, intentionally subordinating the CPI + 4% target.

### Why Checkable Rules Are Insufficient
Negative rules merely define the perimeter of mathematical feasibility; they do not establish fiduciary optimality. Candidate D satisfies every checkable constraint yet constitutes an uncompensated gamble against the foundation's strategic benchmark and risk appetite.

### Investment Policy Statement (IPS) Triangulation
1. **IPS Definition:** A formal contractual charter between asset owners and fiduciaries detailing investment governance, return hurdles, risk budgets, and accountability standards.
2. **Dual Mechanism:** Balances **Objectives** (desired financial targets and risk appetite) against **Constraints** (operational boundaries such as liquidity, time horizon, regulations, and unique circumstances).
3. **S1–S10 IPS Mapping:**
   - *Return Objective:* **S2** (CPI + 4% real net return).
   - *Risk Objective / Budget:* **S9** (Unquantified 10% loss threshold).
   - *Time Horizon:* **S1** (7-year horizon with annual rebalance).
   - *Liquidity Constraints:* **S3** ($0.75M quarterly payout / $3.0M reserve floor) and **S8** (90% in 5 business days).
   - *Legal & Mandate Constraints:* **S5** (Long-only, no leverage/derivatives) and **S6** (8% single-issuer cap).
   - *Asset Allocation & Benchmark Preference:* **S4** (60/40 benchmark) and **S7** (25% turnover limit).
   - *Missing Governance:* **S10** (Undefined optimization utility function).

---

## 8. 60-Second Investment Committee Defense

> *"Mr. Chairman and Members of the Committee: Before allocating a single dollar of the $100 million reserve or selecting an optimizer, we established an immutable decision contract. Our mechanical rule engine confirms that Candidate A satisfies every checkable constraint—providing a robust 14% liquidity reserve well above our $3.0 million legal distribution floor, 100% 5-day liquidity, and zero single-issuer concentration. In contrast, Candidates B and C fail multiple liquidity and reserve hurdles, while Candidate D demonstrates the danger of naive optimization: it technically passes all coded screens but gambles 96% of the foundation's capital in equities with zero bonds, repudiating your 60/40 policy benchmark.*  
> *Most critically, we must not run an optimizer until the Committee resolves Statement 9: in a long-only portfolio without derivatives, an absolute 10% calendar-year loss ceiling is mathematically incompatible with targeting CPI + 4% in equity bear markets. We recommend authorizing the pilot only after the Committee defines whether tracking error or drawdown CVaR governs our optimization objective."*

---

## 9. AI Disclosure & Attestation

- **AI Tools Used:** Codex (OpenAI) & Antigravity (Google DeepMind) for instruction summarization, standard-library script syntax structuring, and candidate reconciliation formatting.
- **Student Ownership:** S1–S10 classifications, rationales, Candidate D judgments, skeptical colleague review, CIO escalation questions, IPS mapping, and 60-second defense were authored, reviewed, and finalized by Oladapo Olaniyan.
- **Truth Attestation:** I attest that all calculations, code outputs, and analytical responses represent verified work completed for FIN 43900.

---

## 10. Personal Growth Note (Ungraded)

Before this lab, I viewed portfolio constraints as simple bounds entered into a solver like Excel Solver or Python `scipy.optimize`. This exercise showed me that optimization is dangerous without a clear decision contract: an algorithm will gladly exploit unconstrained dimensions (like Candidate D holding 96% equities and 0% bonds) while technically satisfying every negative rule. I now feel confident classifying client statements into objectives versus unverifiable promises and defending mandate boundaries to an investment committee, though formalizing multi-period CVaR constraints under fat-tailed distribution assumptions still feels like an area I want to deepen.

---

## 11. Brightspace Copy-Paste Submission Block

```text
================================================================================
FIN 43900 LAB 13 CHECKOUT SUBMISSION
Student Name: Oladapo Olaniyan
Email: oolaniy@purdue.edu
Course: FIN 43900 — AI Finance Applications, Fall 2026
Lab Date: October 15, 2026
Session Token: CFA Investment
In-Person Attendance: Attended (Confirmed by Oladapo Olaniyan)
Case: Meridian Foundation Reserve ($100M Reserve)
================================================================================

1. REPOSITORY & SCRIPT DELIVERABLES:
- Worksheet (.md): https://github.com/Dapize-Mo/FIN43900-AI-Finance-Applications/blob/main/labs/lab-13/lab-13-mandate-defense-worksheet.md
- Rule Checker (mandate.py): https://github.com/Dapize-Mo/FIN43900-AI-Finance-Applications/blob/main/labs/lab-13/mandate.py
- Checkout Package: https://github.com/Dapize-Mo/FIN43900-AI-Finance-Applications/blob/main/labs/lab-13/lab-13-checkout.md
- Lab Directory: https://github.com/Dapize-Mo/FIN43900-AI-Finance-Applications/tree/main/labs/lab-13

2. S1-S10 CLASSIFICATIONS & RATIONALES:
- S1 (7-yr horizon, annual rebalance): HARD CONSTRAINT — Binding temporal and governance rebalancing rule.
- S2 (CPI + 4% net over rolling 5-yr): OBJECTIVE — Core measurable real-return performance hurdle.
- S3 ($0.75M quarterly payout, 12-mo liquid reserve): HARD CONSTRAINT — Non-negotiable $3.0M (3.0%) cash/Treasury floor.
- S4 (60% global equity / 40% US IG bonds): PREFERENCE — Strategic asset allocation benchmark guiding balance.
- S5 (Long-only, no borrowing/shorting/derivatives): HARD CONSTRAINT — Absolute negative screen on leverage and instruments.
- S6 (No single issuer > 8%): HARD CONSTRAINT — Absolute concentration ceiling for corporate issuers.
- S7 (Turnover <= 25% without approval): PREFERENCE — Trading volume ceiling permitting approved exceptions.
- S8 (>= 90% liquid within 5 business days): HARD CONSTRAINT — Non-negotiable portfolio liquidity hurdle.
- S9 ("Cannot have calendar-year loss > 10%"): UNVERIFIABLE PROMISE — Absolute market guarantee lacking risk metric, breach rule, or probability.
- S10 (No sector/ESG/tax preference; undefined pilot goal): MISSING — Essential optimization utility function absent.

3. CANDIDATE RECONCILIATION SUMMARY:
- Candidate A: Allocation 100%, Min 0.0%, Reserve 14.0% (>=3.0%), Liquidity 100% (>=90%), Issuer 0.0% (<=8%). VERDICT: PASSES ALL CHECKABLE RULES.
- Candidate B: Reserve 1.0% (FAIL), Liquidity 85.0% (FAIL), Issuer 9.0% (FAIL). VERDICT: FAILS 3 RULES.
- Candidate C: Reserve 2.0% (FAIL), Liquidity 100% (PASS), Issuer 8.0% (PASS). VERDICT: FAILS 1 RULE (Reserve floor).
- Candidate D: Allocation 100%, Min 0.0%, Reserve 4.0%, Liquidity 100%, Issuer 0.0%. VERDICT: PASSES ALL RULES (Exploits omitted fixed income constraint; 96% equity / 0% bond).
- Candidate A Negative Probe: Cash set to -2.0%, Global Equity to 64.0%. VERDICT: Long-only FAILS (-2.0%); other checks pass; original restored.

4. CANDIDATE D JUDGMENT & SKEPTICAL COLLEAGUE CHECK:
- Candidate D Judgment: The objection holds. Candidate D eliminates all bonds, violating the strategic asset allocation intent of S4 (60/40 benchmark) and creating extreme drawdown risk that guarantees a breach of S9 during equity bear markets.
- Skeptical Colleague Check: If a colleague introduces illiquid real estate or high-turnover tactical funds, cite S8 (90% liquid in 5 days) and S7 (turnover <= 25%) to reject it prior to optimization.

5. TWO AI OPERATIONAL INTERPRETATIONS:
- Interpretation 1 (Benchmark-Tracking Mandate): REQUIRES CLARIFICATION (S9 & S10). Prioritizing tracking error to 60/40 benchmark breaches S9 during equity bear markets.
- Interpretation 2 (Absolute-Return Downside Protection): UNSUPPORTED (S5 & S9). Long-only universe without derivatives cannot eliminate 10% loss risk without holding >60% cash, which fails S2 (CPI + 4%).

6. CIO ESCALATION QUESTION & DESIGN REVERSAL:
- Question: "What explicit utility function governs the pilot (maximizing return vs minimizing tracking error to 60/40), and how must the 10% calendar-year loss constraint be enforced given that absolute loss truncation is impossible in long-only equities?"
- Reversal Fact: If tracking error is selected, the portfolio remains anchored near 60/40. If downside loss is strictly enforced, equity weight must collapse below 30% into cash and Treasuries.

7. 60-SECOND COMMITTEE DEFENSE:
Candidate A is the only compliant candidate, providing 14% liquidity reserves against our $3.0M annual payout floor. Candidates B and C breach statutory liquidity and concentration rules. Candidate D proves that checkable constraints alone are insufficient: it satisfies all code rules while reckless taking a 96% equity bet with zero bonds. The Committee must clarify whether tracking error or drawdown risk governs before any optimizer is deployed.

8. GROWTH NOTE:
Before this lab, I viewed portfolio constraints as simple bounds entered into a solver. This exercise showed me that an optimizer will exploit unconstrained boundaries (like Candidate D holding 96% equities) while technically passing all screens. I now feel confident building a standard-library mandate engine and translating qualitative CIO requests into formal IPS objectives and constraints.
================================================================================
```
