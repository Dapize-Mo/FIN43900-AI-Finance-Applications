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
| 4% Cash, 96% Global equity index fund; passes all coded rules but has no bond exposure. | Yes, all coded checks pass. AI claim: the CIO could reject the all-equity allocation because it departs sharply from the stated 60/40 benchmark. | Student judgment pending |

**Two-sentence AI-closed judgment:** Does the objection hold, and which CIO statement decides it?

> 

**Skeptical colleague check:** After the partner swap described in the prompt, what CIO statement would you cite against the other candidate?

> 

## 5. CIO question and reflection (AI closed)

**One question the CIO must answer before anyone optimizes:**

> 

**What answer would change the portfolio design?**

> 

**How can a candidate pass every checkable rule and still be wrong for this client?**

> 

**Which S1–S10 classification was I least sure about, and why?**

> 

### Investment policy statement mapping

In your own words, answer: (1) What is an investment policy statement? (2) How does it work through objectives and constraints? (3) How do S1–S10 map onto those ideas?

> 

## 6. Brightspace checkout

Push both files to your own GitHub repository and paste their links into the Lab 13 quiz. Complete individually.

- GitHub link to `.md` file: https://github.com/Dapize-Mo/FIN43900-AI-Finance-Applications/blob/main/labs/lab-13/lab-13-mandate-defense-worksheet.md
- GitHub link to `mandate.py`: https://github.com/Dapize-Mo/FIN43900-AI-Finance-Applications/blob/main/labs/lab-13/mandate.py
- Session token from the October 15 course announcement: `CFA Investment`
- AI partner used: Codex (OpenAI) — located/summarized instructions, prepared this worksheet, built/explained the standard-library checker, proposed Candidate D, and checked the A/B/C and negative-weight outputs. It did not supply the S1–S10 classifications or AI-closed reflections.
- October 15 Zoom attendance for optional 10-point bonus: attended (confirmed by Oladapo Olaniyan).
- Quiz attempt / receipt: Attempt 1 of 3 auto-submitted by the 55-minute timer on Oct. 15, 2026 at 3:03 p.m.; Brightspace showed Pending Evaluation. Last observed save status: 1 of 2 questions; Question 2 links were not saved.

