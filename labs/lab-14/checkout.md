# FIN 43900 Lab 14 — Portfolio Baselines

**Course:** FIN 43900 — AI Finance Applications, Purdue University  
**Student Analyst:** **Oladapo Olaniyan** (`oolaniy@purdue.edu`)  
**Institution:** Mitchell E. Daniels, Jr. School of Business, Purdue University  
**Case:** Meridian Foundation Reserve ($100 Million Reserve)  
**Lab Date:** October 20, 2026  
**Brightspace Item:** Lab 14 — Portfolio Baselines (Tuesday Authenticated Completion, 25 Points)  
**Session Token:** `[Announced in Class / Room Token]`  

---

## 📌 1. Executive Summary & Repository Artifacts

This checkout establishes the quantitative baseline foundations and constraint verification engine for the **$100 million Meridian Foundation Reserve**. Rather than rushing to unconstrained mathematical solvers that produce fragile and extreme corner solutions, this analysis formalizes the portfolio input contract, derives transparent naive and risk-scaled baselines, reconciles the underlying covariance structure from first principles, and evaluates a provisional mechanics candidate against the Week 8 mandate.

Because the Meridian Foundation CIO has not authorized an operational optimization objective function (e.g., return maximization vs. benchmark tracking error vs. drawdown limitation) and because statement S9 ("cannot have a calendar-year loss greater than 10%") remains an unoperationalized qualitative assertion lacking a statistical confidence interval or breach protocol, the fiduciary action disposition is formally recorded as:

$$\mathbf{DEFERRED\_NO\_ADOPTABLE\_CANDIDATE}$$

### Artifacts & Deliverables

- **Python Baseline & Audit Script:** [`portfolio_baselines.py`](portfolio_baselines.py)
- **Course Synthetic Asset Statistics:** [`asset_statistics.csv`](asset_statistics.csv)
- **Course Synthetic Correlation Matrix:** [`correlation.csv`](correlation.csv)
- **Directory Overview:** [`README.md`](README.md)
- **Pre-formatted Brightspace Submission:** [`../../brightspace/lab-14_submission.txt`](../../brightspace/lab-14_submission.txt)
- **GitHub Direct Script Link:** [portfolio_baselines.py on GitHub](https://github.com/Dapize-Mo/FIN43900-AI-Finance-Applications/blob/main/labs/lab-14/portfolio_baselines.py)
- **GitHub Direct Checkout Link:** [checkout.md on GitHub](https://github.com/Dapize-Mo/FIN43900-AI-Finance-Applications/blob/main/labs/lab-14/checkout.md)

---

## 2. Decision Contract & Mandate Specifications

| Dimension | Specification | Source / Governing Fact | Fiduciary Rationale |
| :--- | :--- | :--- | :--- |
| **Decision User** | Meridian Foundation Investment Committee & CIO | Week 8 Common CIO Case | Fiduciary body governing the endowment reserve fund |
| **Immediate Action** | Propose policy baselines, constraint audits, and conditional deferral | Week 9 Handout § Role | Establish baseline risk benchmarks before algorithmic optimization |
| **Horizon** | Seven (7) years with quarterly review & annual rebalancing | Fact S1 | Long-term capital preservation aligned with payout commitments |
| **Investable Universe** | 4 Asset Classes: `GovBond`, `CorpBond`, `USEquity`, `IntlEquity` | Week 9 Starter Files | Course synthetic asset classes representing the global opportunity set |
| **Stated Objective** | CPI + 4.0% annualized net of fees over rolling 5-year periods | Fact S2 | Long-term real purchasing power preservation target |
| **Policy Benchmark** | 60% Global Equity / 40% U.S. Investment-Grade Bonds | Fact S4 | Strategic asset allocation anchor and counterfactual hurdle |
| **Hard Constraints** | 1. Long-only ($w_i \ge 0$, $\sum w_i = 1$, no shorting/derivatives/borrowing)<br>2. Minimum 12-month liquid reserve: $\ge \$3.0\text{M}$ ($3.0\%$) in cash / sovereign paper (`GovBond`)<br>3. Single issuer concentration cap $\le 8\%$ (for individual corporate issuers)<br>4. Liquidity floor: $\ge 90\%$ redeemable within 5 business days | Facts S3, S5, S6, S8 | Non-negotiable structural and liquidity risk boundaries |

---

## 3. Input Provenance, Boundary Definitions & Prework

### Input Provenance & Boundaries
- **Data Provenance:** `COURSE_SYNTHETIC_TEACHING_INPUTS` — Course-authored synthetic point-in-time teaching inputs published for the October 20, 2026 session.
- **Sample Boundary:** `Not applicable — no observed sample`. These are synthetic parameters, not econometric estimates from historical time series.
- **As-Of Boundary:** `October 20, 2026 course release`.
- **Return / Volatility Units & Frequency:** Annualized decimals ($0.040 = 4.0\%$).
- **Missingness Policy:** `None`. Complete specification with zero missing observations.

### Human-First Prework Predictions (Completed Independently Before AI)
1. **Most Highly Correlated Asset Pair:** `USEquity` and `IntlEquity`  
   *Rationale:* Both assets represent global equity risk factors and corporate earnings cycles, sharing systemic macroeconomic exposure. In the teaching matrix, correlation is $+0.75$.
2. **Asset Expected to Receive Largest Inverse-Volatility Weight:** `GovBond`  
   *Rationale:* `GovBond` exhibits the lowest standalone annualized volatility ($\sigma = 6.0\%$), giving it the largest reciprocal volatility ($1 / 0.060 = 16.67$). Under risk-scaling, it must receive the largest allocation.
3. **Mandate Constraint That Could Bind:** The **Liquidity Reserve Floor (S3)** requiring $\ge 3.0\%$ in cash or daily-liquid sovereign securities (`GovBond`), or the **60/40 Benchmark Alignment (S4)** during optimization trade-offs.

---

## 4. Covariance Matrix Derivation & Independent Manual Reconciliation

### Governing Formulation
For volatility vector $\boldsymbol{\sigma} = [\sigma_1, \dots, \sigma_n]^T$ and correlation matrix $\mathbf{C}$:
$$\boldsymbol{\Sigma} = \text{diag}(\boldsymbol{\sigma}) \times \mathbf{C} \times \text{diag}(\boldsymbol{\sigma}) \quad \Longleftrightarrow \quad \Sigma_{ij} = \sigma_i \times \sigma_j \times C_{ij}$$

### Input Parameters
$$\boldsymbol{\mu} = \begin{bmatrix} 0.040 \\ 0.055 \\ 0.085 \\ 0.080 \end{bmatrix}, \quad \boldsymbol{\sigma} = \begin{bmatrix} 0.060 \\ 0.090 \\ 0.180 \\ 0.200 \end{bmatrix}, \quad \mathbf{C} = \begin{bmatrix} 1.00 & 0.35 & -0.10 & -0.05 \\ 0.35 & 1.00 & 0.25 & 0.20 \\ -0.10 & 0.25 & 1.00 & 0.75 \\ -0.05 & 0.20 & 0.75 & 1.00 \end{bmatrix}$$

### Resulting Annualized Covariance Matrix ($\boldsymbol{\Sigma}$)
| Asset | `GovBond` | `CorpBond` | `USEquity` | `IntlEquity` |
| :--- | :---: | :---: | :---: | :---: |
| **`GovBond`** | **0.003600** | **0.001890** | **-0.001080** | **-0.000600** |
| **`CorpBond`** | **0.001890** | **0.008100** | **0.004050** | **0.003600** |
| **`USEquity`** | **-0.001080** | **0.004050** | **0.032400** | **0.027000** |
| **`IntlEquity`** | **-0.000600** | **0.003600** | **0.027000** | **0.040000** |

### Independent Manual Verification of Known Cells (Without AI)
To guarantee numerical integrity without circular reliance on code:
1. **Diagonal Cell ($\text{GovBond} \times \text{GovBond}$):**
   $$\text{Cov}(\text{GovBond}, \text{GovBond}) = \sigma_{\text{Gov}}^2 \times C_{\text{Gov},\text{Gov}} = (0.060)^2 \times 1.00 = \mathbf{0.003600} \quad \text{[Exact Match]}$$
2. **Off-Diagonal Fixed Income ($\text{GovBond} \times \text{CorpBond}$):**
   $$\text{Cov}(\text{GovBond}, \text{CorpBond}) = 0.060 \times 0.090 \times 0.35 = 0.0054 \times 0.35 = \mathbf{0.001890} \quad \text{[Exact Match]}$$
3. **Off-Diagonal Equity Cluster ($\text{USEquity} \times \text{IntlEquity}$):**
   $$\text{Cov}(\text{USEquity}, \text{IntlEquity}) = 0.180 \times 0.200 \times 0.75 = 0.0360 \times 0.75 = \mathbf{0.027000} \quad \text{[Exact Match]}$$
4. **Flight-to-Safety Negative Cross-Asset ($\text{GovBond} \times \text{USEquity}$):**
   $$\text{Cov}(\text{GovBond}, \text{USEquity}) = 0.060 \times 0.180 \times (-0.10) = 0.0108 \times (-0.10) = \mathbf{-0.001080} \quad \text{[Exact Match]}$$

---

## 5. Baselines vs. Provisional Candidate Comparison

### Mathematical Baseline Formulations
- **Portfolio Expected Return:** $\mu_p = \mathbf{w}^T \boldsymbol{\mu}$
- **Portfolio Variance:** $\sigma_p^2 = \mathbf{w}^T \boldsymbol{\Sigma} \mathbf{w}$
- **Portfolio Volatility:** $\sigma_p = \sqrt{\sigma_p^2}$

### Baseline Specifications & Calculations
1. **Equal-Weight Baseline ($1/N$ Naive):**
   - Weights: $w_i = 0.25$ for all four assets ($[0.25, 0.25, 0.25, 0.25]$).
   - Expected Return:
     $$\mu_{p,\text{eq}} = 0.25(0.040) + 0.25(0.055) + 0.25(0.085) + 0.25(0.080) = \mathbf{6.500\%}$$
   - Portfolio Variance: $\sigma_{p,\text{eq}}^2 = 0.00961425$
   - Portfolio Volatility: $\sigma_{p,\text{eq}} = \sqrt{0.00961425} = \mathbf{9.805\%}$
2. **Inverse-Volatility Baseline (Risk-Scaled):**
   - Reciprocals: $1/0.060 = 16.667$, $1/0.090 = 11.111$, $1/0.180 = 5.556$, $1/0.200 = 5.000$ (Sum $= 38.333 = 115/3$).
   - Exact Normalized Weights:
     - $\text{GovBond} = \frac{10}{23} \approx \mathbf{43.478\%}$
     - $\text{CorpBond} = \frac{20}{69} \approx \mathbf{28.986\%}$
     - $\text{USEquity} = \frac{10}{69} \approx \mathbf{14.493\%}$
     - $\text{IntlEquity} = \frac{3}{23} \approx \mathbf{13.043\%}$
   - Expected Return:
     $$\mu_{p,\text{inv}} = \frac{10}{23}(0.040) + \frac{20}{69}(0.055) + \frac{10}{69}(0.085) + \frac{3}{23}(0.080) = \mathbf{5.609\%}$$
   - Portfolio Variance: $\sigma_{p,\text{inv}}^2 = 0.00462758$
   - Portfolio Volatility: $\sigma_{p,\text{inv}} = \sqrt{0.00462758} = \mathbf{6.803\%}$
3. **Provisional Mechanics Candidate Allocation (Transparent 60/40 Policy Benchmark Match):**
   - Objective: Mechanics test only; transparent match to Meridian strategic benchmark ($60\%$ Equity / $40\%$ Fixed Income).
   - Weights: $\text{GovBond} = 20.0\%$, $\text{CorpBond} = 20.0\%$, $\text{USEquity} = 40.0\%$, $\text{IntlEquity} = 20.0\%$.
   - Expected Return: $0.20(0.040) + 0.20(0.055) + 0.40(0.085) + 0.20(0.080) = \mathbf{6.900\%}$.
   - Portfolio Variance: $\sigma_{p,\text{cand}}^2 = 0.01243800$
   - Portfolio Volatility: $\sigma_{p,\text{cand}} = \sqrt{0.01243800} = \mathbf{11.153\%}$.

### Comparative Results Table (Student Handout Format)

| Portfolio | Weight Summary (`Gov`/`Corp`/`US`/`Intl`) | Expected Return | Volatility | Constraint Breach? | What It Establishes |
| :--- | :---: | :---: | :---: | :--- | :--- |
| **Equal Weight** | $25.0\% \ / \ 25.0\% \ / \ 25.0\% \ / \ 25.0\%$ | **6.50%** | **9.80%** | **None** (`GovBond` $25\% \ge 3\%$) | Transparent naive baseline; benchmark for evaluating active complexity |
| **Inverse Volatility** | $43.48\% \ / \ 28.99\% \ / \ 14.49\% \ / \ 13.04\%$ | **5.61%** | **6.80%** | **None** (`GovBond` $43.48\% \ge 3\%$) | Risk-scaling baseline; penalizes high standalone risk without estimating covariances |
| **Provisional Candidate (60/40)** | $20.0\% \ / \ 20.0\% \ / \ 40.0\% \ / \ 20.0\%$ | **6.90%** | **11.15%** | **None** (`GovBond` $20\% \ge 3\%$) | Conditional mechanics probe; practices algebra; adoption **DEFERRED** |

---

## 6. Mechanical Constraint Audit & Verification

All three portfolios and matrix structures passed automated mathematical verification in [`portfolio_baselines.py`](portfolio_baselines.py):

| Verification Check | Standard / Requirement | Result | Evidence / Audit Metric |
| :--- | :--- | :---: | :--- |
| **Sum to One** | $\sum_{i=1}^4 w_i = 1.000000$ | **PASSED** | $\sum w_{\text{eq}} = 1.000$, $\sum w_{\text{inv}} = 1.000$, $\sum w_{\text{cand}} = 1.000$ |
| **Long-Only Bounds** | $w_i \ge 0.0$ for all assets | **PASSED** | Minimum weight across all baselines is $13.043\% > 0$ |
| **Reserve Floor (S3)** | $w_{\text{GovBond}} \ge 3.0\%$ ($\ge \$3.0\text{M}$) | **PASSED** | `GovBond` weights: Eq $= 25.0\%$, Inv $= 43.48\%$, Cand $= 20.0\%$ (all $\ge 3.0\%$) |
| **Covariance Symmetry** | $\boldsymbol{\Sigma} = \boldsymbol{\Sigma}^T$ | **PASSED** | $\max |\boldsymbol{\Sigma} - \boldsymbol{\Sigma}^T| = 0.0$ |
| **Positive Semi-Definiteness** | All eigenvalues $\lambda_i \ge 0$ | **PASSED** | Eigenvalues: $[0.002241, 0.006900, 0.010468, 0.064491]$ (all strictly positive) |

---

## 7. AI Disclosures & Governance Disposition

### Accepted AI Suggestion
- **Suggestion:** Use NumPy matrix broadcasting and matrix multiplication `diag(vols) @ corr @ diag(vols)` to assemble the covariance matrix and inspect eigenvalues (`np.linalg.eigvalsh`) to confirm positive semi-definiteness automatically.
- **Disposition:** **ACCEPTED.** It ensures computational vectorization, eliminates nested looping errors, and enforces mathematical covariance validity.

### Rejected / Qualified AI Suggestion
- **Suggestion:** An AI prompt proposed running an unconstrained quadratic solver to find the "optimal" maximum Sharpe ratio portfolio (allocating $76.2\%$ to `GovBond`, $14.2\%$ to `CorpBond`, $5.8\%$ to `USEquity`, and $3.8\%$ to `IntlEquity`) and recommending it for immediate adoption.
- **Disposition:** **REJECTED.** The CIO case deliberately omitted the optimization objective (S10) and stated an unenforceable loss constraint (S9). Delivering an optimizer's corner solution without committee authorization violates the fiduciary decision contract. Per course rules, this is labeled `DEFERRED_NO_ADOPTABLE_CANDIDATE`.

---

## 8. Fiduciary Deferral & Escalation Protocol

```
================================================================================
MANDATE FIDUCIARY DISPOSITION: DEFERRED_NO_ADOPTABLE_CANDIDATE
================================================================================
ESCALATION OWNER: Meridian Foundation Chief Investment Officer (CIO)

UNRESOLVED AMBIGUITY:
1. The CIO and Investment Committee have not specified the mathematical objective 
   function for the portfolio (e.g., maximize expected return, minimize variance, 
   minimize tracking error relative to the 60/40 benchmark, or maximize payout safety).
2. Statement S9 ("cannot have a calendar-year loss greater than 10%") remains an 
   unverifiable promise lacking a statistical confidence interval (e.g., 95% 1-year VaR) 
   and an operational response protocol if a market crash breaches the boundary.

EVIDENCE NEEDED TO RESUME:
1. Written Investment Committee authorization of the governing utility function.
2. Formal operationalization of the downside risk constraint into a measurable metric 
   (e.g., 1-year 95% CVaR <= 10% or policy equity cap).
================================================================================
```

---

## 9. Growth Note (Ungraded & Personal)

> **Growth Note:**  
> Before this lab, I thought portfolio construction started with running an optimizer in Python and printing weights. Today's lab showed me why professional asset allocation begins with establishing unshakeable transparent baselines (Equal-Weight and Inverse-Volatility) and auditing the data provenance and covariance matrix first. I now clearly understand how diversification mathematically arises from covariance terms rather than standalone risk, and I feel confident reconciling covariance matrices by hand and standing my ground when a client mandate lacks the mathematical clarity required for optimization.
