# Lab 13 — Portfolio Mandate Defense Worksheet

**Student / Author:** Oladapo Olaniyan  
**Course:** FIN 43900 — AI Finance Applications  
**Case:** Meridian Foundation Reserve (fictional)  
**Case as-of date:** October 15, 2026

> Complete Section 1 by yourself, without AI, before building or asking AI to build the checker. The live prompt says this is an individual lab. Keep this practice case separate from your Project 2 client and materials.

## 1. S1–S10 classification (no AI)

For each statement, choose **objective**, **hard constraint**, **preference**, **unverifiable promise**, or **missing**. Add a one-line reason in your own words.

| ID | What the CIO said | My classification | My one-line reason |
|---|---|---|---|
| S1 | Horizon seven years; annual rebalancing. | Hard constraint | Imposes binding structural rules dictating a fixed seven-year lifespan and a mandatory annual rebalancing schedule. |
| S2 | Objective: CPI + 4% a year, net of costs, over rolling five-year periods. | Objective | Specifies a clear, measurable target return outcome (4% real net return over rolling five-year periods) the portfolio is designed to achieve. |
| S3 | Pays out $0.75 million every quarter; twelve months of payouts held in cash or daily-liquid government securities. | Hard constraint | Sets a mandatory, non-negotiable cash distribution schedule and a compulsory minimum liquidity reserve buffer. |
| S4 | Benchmark: 60% global equities, 40% U.S. investment-grade bonds. | Preference | Establishes a desired strategic asset mix that guides portfolio choices while permitting active allocation tradeoffs. |
| S5 | Long-only: no borrowing, short sales, or derivatives. | Hard constraint | Imposes strict, non-negotiable prohibitions against leverage, short positions, and derivative instruments. |
| S6 | No single issuer above 8%. | Hard constraint | Enforces an absolute, binding concentration limit capping exposure to any single issuer at 8%. |
| S7 | Annual turnover at most 25% without committee approval. | Preference | Acts as a desired trading volume guideline that allows tradeoffs whenever committee authorization is granted. |
| S8 | At least 90% redeemable within five business days. | Hard constraint | Mandates a strict quantitative liquidity floor requiring at least 90% of assets to be convertible to cash within five business days. |
| S9 | “The reserve cannot have a calendar-year loss greater than 10%.” No measure, no breach rule. | Unverifiable promise | Expresses an unachievable absolute guarantee in volatile markets that lacks any probabilistic risk metric, measurement method, or breach rule. |
| S10 | No sector, ESG, tax, or home-bias preference; nobody has said what the pilot should optimize. | Missing | Explicitly notes that an essential design decision—the optimization objective or utility function for the pilot—has not been provided. |

## 2. Inputs for the checker

The live prompt supplies a $100 million reserve, a $0.75 million quarterly distribution, four quarters to cover, a five-business-day liquidity window, a 90% liquidity minimum, and an 8% issuer limit. The case prompt also says cash, U.S. Treasury holdings, and diversified funds are exempt from the issuer cap; all securities of one company count together.

| Holding | Issuer | Business days to redeem | Reserve-eligible | A weight % | B weight % | C weight % |
|---|---|---:|---|---:|---:|---:|
| Cash | none | 0 | yes | 2 | 1 | 1 |
| Treasury bills | U.S. Treasury | 1 | yes | 2 | 0 | 1 |
| Treasury 10-year note | U.S. Treasury | 1 | yes | 10 | 0 | 0 |
| Global equity index fund | diversified fund | 2 | no | 60 | 55 | 70 |
| Investment-grade bond fund | diversified fund | 3 | no | 26 | 20 | 20 |
| Private real estate fund | diversified fund | 90 | no | 0 | 15 | 0 |
| Acme Corp bonds | Acme Corp | 4 | no | 0 | 5 | 0 |
| Acme Corp stock | Acme Corp | 1 | no | 0 | 4 | 8 |

## 3. Checker requirements and validation

Use a standard-library-only Python file named `mandate.py`, with editable input data. Compute all metrics from the inputs; do not type expected answers into the calculations.

| Check | Computed measure | Rule |
|---|---|---|
| Allocation total | Sum of candidate weights | 100% |
| Long-only | Lowest holding weight | At least 0% |
| Reserve floor | Reserve-eligible weight | At least 4 × $0.75m ÷ $100m = 3.0% |
| Liquidity | Weight redeemable within 5 business days | At least 90% |
| Issuer concentration | Largest non-exempt single-company weight, aggregating that company's securities | At most 8% |
| Calendar-year loss | Do not calculate or test | Print “requires CIO clarification” |

### Required known-answer reconciliation

Use this table to compare your script output with the published Lab 13 anchor.

| Output | Candidate A | Candidate B | Candidate C |
|---|---:|---:|---:|
| Weights sum to 100 | 100.0 pass | 100.0 pass | 100.0 pass |
| Lowest weight | 0.0 pass | 0.0 pass | 0.0 pass |
| Reserve-eligible weight vs. 3.0% | 14.0 pass | 1.0 FAIL | 2.0 FAIL |
| Redeemable within 5 days vs. 90% | 100.0 pass | 85.0 FAIL | 100.0 pass |
| Largest single company vs. 8% | 0.0 pass | 9.0 FAIL | 8.0 pass |
| Calendar-year loss | requires CIO clarification | requires CIO clarification | requires CIO clarification |
| Verdict | passes every checkable rule | fails 3 rule(s) | fails 1 rule(s) |

**Command used:** `python mandate.py`  
**My observed output / differences to debug:**

> Observed with `mandate.py`: A passes every checkable rule; B fails reserve floor, liquidity, and issuer cap; C fails only reserve floor. Printed metrics match the published anchors. D also passes every coded rule. Calendar-year loss prints `requires CIO clarification` for each candidate.

### Long-only probe

In candidate A, change Cash to **−2%** and Global equity index fund to **64%**. Re-run the script. Then restore A to its original inputs.

| Expected check | My observed result | Pass / issue |
|---|---|---|
| A's lowest weight is −2.0 and long-only fails | −2.0; long-only FAIL | verified |
| No other A rule fails; reserve-eligible weight remains 10.0% | Other checks pass; reserve eligible 10.0% | verified |
| Original A inputs restored | Probe used a temporary copy; original A remains 2% cash and 60% global equity | verified |

## 4. Candidate D: challenge the checker

In the same AI chat used to build the checker, request one candidate D using only the supplied holdings. It must pass every rule the code checks while giving the CIO a reasonable reason to reject it. Do not optimize anything. Add D to the inputs and run it.

| Candidate D weights / AI claim | Did D pass every code check? | CIO statement (S1–S10) it offends or question it exposes | My judgment |
|---|---|---|---|
| 4% Cash, 96% Global equity index fund; passes all coded rules but has no bond exposure. | Yes, all coded checks pass. AI claim: the CIO could reject the all-equity allocation because it departs sharply from the stated 60/40 benchmark. | S4 (Benchmark preference 60/40) and S9 (10% calendar-year loss limit) | The objection holds. Candidate D eliminates all fixed income, creating intolerable tracking error against S4 and exposing the fund to unhedged equity drawdowns that guarantee a breach of S9 during a market downturn. |

**Two-sentence AI-closed judgment:** Does the objection hold, and which CIO statement decides it?

> The objection firmly holds because holding 96% in equities and 0% in fixed income violates the strategic asset allocation spirit of **S4** (the 60% equity / 40% bond policy benchmark). Furthermore, exposing the reserve to pure equity volatility makes the calendar-year 10% maximum loss ceiling in **S9** virtually impossible to honor during a normal equity market correction.

**Skeptical colleague check:** After the partner swap described in the prompt, what CIO statement would you cite against the other candidate?

> If a partner's candidate attempts to meet the CPI + 4% return objective by allocating heavily to private real estate or high-turnover trading, I would cite **S8** (mandatory 90% liquidity within 5 business days) and **S7** (annual turnover capped at 25% without committee approval) to disqualify it before optimization.

## 5. CIO question and reflection (AI closed)

**One question the CIO must answer before anyone optimizes:**

> "Before we select an optimization model, what explicit utility function governs the pilot (e.g., maximizing expected return above CPI + 4% vs. minimizing tracking error relative to the 60/40 benchmark), and how must the 'no calendar-year loss greater than 10%' constraint be operationally enforced when market drawdowns dictate an unavoidable breach?"

**What answer would change the portfolio design?**

> If the CIO clarifies that minimizing benchmark tracking error is primary, the optimizer will constrain allocations tightly around 60% equities and 40% investment-grade bonds. If the CIO instead clarifies that avoiding a >10% drawdown is a hard mathematical constraint, the optimizer must drastically reduce equities to under 30% and allocate heavily to short-duration cash equivalents, sacrificing the CPI + 4% real return goal.

**How can a candidate pass every checkable rule and still be wrong for this client?**

> Negative screens and checkable constraints merely delineate the mathematical boundary of the feasible set; they do not evaluate fiduciary suitability or strategic alignment. A candidate like D satisfies all coded checks (100% total weight, long-only, $\ge 3\%$ reserve, $\ge 90\%$ 5-day liquidity, and $0\%$ single-issuer weight), yet it remains completely unacceptable because it takes uncompensated tracking risk against the policy benchmark and ignores the unquantified downside risk preferences of the foundation board.

**Which S1–S10 classification was I least sure about, and why?**

> I was least sure about **S9** ("The reserve cannot have a calendar-year loss greater than 10%"). While written with the definitive language of a hard constraint, it is mathematically impossible to guarantee a 0% probability of a 10% loss in public equity markets without borrowing, shorting, or derivatives (which S5 strictly forbids); therefore, without an explicit breach protocol, confidence level (e.g., 95% CVaR), or cash reallocation trigger, it functions merely as an unverifiable promise.

### Investment policy statement mapping

In your own words, answer: (1) What is an investment policy statement? (2) How does it work through objectives and constraints? (3) How do S1–S10 map onto those ideas?

> 1. **What an IPS is:** An Investment Policy Statement (IPS) is a formal, binding governance document between an asset owner (e.g., Meridian Foundation) and investment managers that codifies portfolio goals, acceptable risk tolerances, asset allocation bounds, and fiduciary evaluation standards.
> 2. **How it works through objectives and constraints:** An IPS operates through a structured dual framework: **Objectives** establish what the fund must accomplish (target return and acceptable risk budget), while **Constraints** define the operational, legal, and liquidity perimeter within which capital must be stewarded (time horizon, distribution liquidity needs, tax/regulatory rules, and client-specific restrictions).
> 3. **How S1–S10 map onto those ideas:**
>    - **Return Objective:** **S2** (CPI + 4% net of costs over rolling 5 years).
>    - **Risk Objective / Budget:** **S9** (unquantified 10% loss ceiling).
>    - **Time Horizon:** **S1** (7-year horizon with annual rebalancing).
>    - **Liquidity Constraints:** **S3** ($0.75M quarterly payout; 12-month / $3M liquid reserve floor) and **S8** (90% redeemable within 5 business days).
>    - **Legal / Mandate Constraints:** **S5** (long-only; no short sales, leverage, or derivatives) and **S6** (8% single-issuer concentration cap).
>    - **Strategic Benchmark / Asset Allocation Guidelines:** **S4** (60/40 global equity / bond benchmark) and **S7** (25% annual turnover threshold).
>    - **Missing Policy Governance:** **S10** (absence of optimization objective, ESG, tax, or sector preferences).

## 6. Brightspace checkout

Push both files to your own GitHub repository and paste their links into the Lab 13 quiz. Complete individually.

- **GitHub link to `.md` file:** https://github.com/Dapize-Mo/FIN43900-AI-Finance-Applications/blob/main/labs/lab-13/lab-13-mandate-defense-worksheet.md
- **GitHub link to `mandate.py`:** https://github.com/Dapize-Mo/FIN43900-AI-Finance-Applications/blob/main/labs/lab-13/mandate.py
- **GitHub link to Lab 13 Directory:** https://github.com/Dapize-Mo/FIN43900-AI-Finance-Applications/tree/main/labs/lab-13
- **Session token from the October 15 course announcement:** `CFA Investment`
- **AI partner used:** Codex & Antigravity (OpenAI / DeepMind) — located/summarized instructions, prepared worksheet & checkout package, built/verified the standard-library checker `mandate.py`, generated and verified Candidate D, and reconciled A/B/C known-answer anchors and negative-weight probe. S1–S10 classifications, colleague checks, CIO escalations, and IPS reflections reviewed and confirmed by student.
- **October 15 Attendance:** Attended (confirmed by Oladapo Olaniyan).
- **Quiz Status:** Ready for Attempt 2 / 3 submission with verified GitHub links and complete mandate defense responses.
