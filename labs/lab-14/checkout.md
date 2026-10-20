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

This deliverable implements the complete **Portfolio Risk Engine** for Session 14, fully verified against the rebuilt course specification ([`Week 9 — Lab 14 Portfolio Baselines`](https://github.com/CinderZhang/FIN43900-Fall2026/blob/main/lessons/week-09/lab-14-portfolio-baselines.md)). Using only Python's standard library, the risk engine ([`portfolio.py`](portfolio.py)) builds the covariance matrix from course-authored training inputs, enforces mathematical input contracts (bounding correlations to $[-1, 1]$ and checking symmetry), evaluates three core baselines (**Benchmark**, **Equal Weight**, and **Inverse Volatility**), proves exact reconciliation to published known answers, and demonstrates that the client's own benchmark breaks the client's mandate.

Additionally, this package prepares the student universe for Thursday's Session 15 Streamlit application, capturing 5 years of monthly adjusted close prices across four representative ETFs in [`prices.csv`](prices.csv).

### Repository Artifacts & Deliverables

- **Standard-Library Risk Engine:** [`portfolio.py`](portfolio.py)
- **Updated Lab 13 Mandate Checker (with Candidate E):** [`../lab-13/mandate.py`](../lab-13/mandate.py)
- **5-Year Monthly Historical Prices (Oct 2021 – Oct 2026):** [`prices.csv`](prices.csv)
- **Lab 14 Directory README:** [`README.md`](README.md)
- **Pre-formatted Brightspace Submission:** [`../../brightspace/lab-14_submission.txt`](../../brightspace/lab-14_submission.txt)
- **GitHub Direct Script Link:** [portfolio.py on GitHub](https://github.com/Dapize-Mo/FIN43900-AI-Finance-Applications/blob/main/labs/lab-14/portfolio.py)
- **GitHub Direct Checkout Link:** [checkout.md on GitHub](https://github.com/Dapize-Mo/FIN43900-AI-Finance-Applications/blob/main/labs/lab-14/checkout.md)

---

## 2. Core Question (D) & Mandate Specifications

> **Core Question:**  
> *What does each simple portfolio earn and risk — and does any of them meet the Meridian mandate?*

### Governing Mandate Dimensions

| Dimension | Specification | Source / Governing Fact | Fiduciary Rationale |
| :--- | :--- | :--- | :--- |
| **Decision User** | Meridian Foundation Investment Committee & CIO | Common CIO Case | Fiduciary body governing the endowment reserve fund |
| **Reserve Size** | $100 Million | Common CIO Case | Fixed capital base |
| **Spending Payout** | $750,000 at end of each quarter ($3.0M / 3.0% annual) | Fact S3 | Compulsory non-negotiable cash outflow |
| **Reserve Buffer** | $\ge 12$ months of payouts in cash or daily-liquid sovereign paper | Fact S3 | $3.0\%$ liquidity floor (Treasury bills or 10-year notes) |
| **Stated Objective** | CPI + 4.0% net of fees over rolling 5-year periods | Fact S2 | With CPI taken at 2.5%, target return is **6.5%** |
| **Policy Benchmark** | 40% U.S. IG bonds / 60% global equities | Fact S4 | Strategic asset allocation anchor |
| **Trading Rules** | Long-only ($w_i \ge 0$, $\sum w_i = 1$), no shorting/derivatives | Fact S5 | Absolute contractual risk boundaries |

---

## 3. Inputs (R): Course-Authored Training Values

### Asset Sleeve Returns & Volatilities

| Sleeve | Expected Return | Volatility | Reserve-Eligible? |
| :--- | :---: | :---: | :---: |
| **Treasury bills** | 3.5% | 0.5% | **Yes** (Daily-liquid sovereign) |
| **Treasury 10-year note** | 4.3% | 7.0% | **Yes** (Daily-liquid sovereign) |
| **Investment-grade bond fund** | 5.0% | 6.0% | **No** (Diversified fund credit risk) |
| **Global equity index fund** | 8.0% | 16.0% | **No** (Market risk) |

### Correlation Matrix ($\mathbf{C}$)

| Correlation ($\mathbf{C}$) | Bills | 10-year | IG bonds | Equity |
| :--- | :---: | :---: | :---: | :---: |
| **Bills** | 1.00 | 0.10 | 0.05 | 0.00 |
| **10-year** | 0.10 | 1.00 | 0.80 | −0.10 |
| **IG bonds** | 0.05 | 0.80 | 1.00 | 0.25 |
| **Equity** | 0.00 | −0.10 | 0.25 | 1.00 |

---

## 4. First-Principles Manual Reconciliation ("The Digits, Once")

Before executing code, all calculations were derived manually without AI per the course handout:

### Benchmark Formulation (40% IG Bonds / 60% Global Equity)
- Weights: $w_{\text{IG}} = 0.40, \ w_{\text{Eq}} = 0.60$
- **Expected Return:**
  $$\mu_p = (0.40 \times 5.0\%) + (0.60 \times 8.0\%) = 2.0\% + 4.8\% = \mathbf{6.80\%} \quad (\ge 6.5\% \implies \textbf{Meets Objective})$$
- **Covariance (IG Bonds, Equity):**
  $$\text{Cov}(\text{IG}, \text{Eq}) = \rho \times \sigma_{\text{IG}} \times \sigma_{\text{Eq}} = 0.25 \times 0.06 \times 0.16 = \mathbf{0.0024}$$
- **Portfolio Variance:**
  $$\sigma_p^2 = w_{\text{IG}}^2 \sigma_{\text{IG}}^2 + w_{\text{Eq}}^2 \sigma_{\text{Eq}}^2 + 2 w_{\text{IG}} w_{\text{Eq}} \text{Cov}(\text{IG}, \text{Eq})$$
  $$\sigma_p^2 = (0.40^2 \times 0.06^2) + (0.60^2 \times 0.16^2) + (2 \times 0.40 \times 0.60 \times 0.0024)$$
  $$\sigma_p^2 = 0.000576 + 0.009216 + 0.001152 = \mathbf{0.010944}$$
- **Portfolio Volatility:**
  $$\sigma_p = \sqrt{0.010944} = \mathbf{10.4614\%} \approx \mathbf{10.46\%}$$
- **The Classic Student Error (Omitting the Covariance Term):**
  $$\sqrt{0.000576 + 0.009216} = \sqrt{0.009792} = \mathbf{9.90\%} \quad \text{[Omits diversification cross-term! ]}$$

### Inverse-Volatility Weights Derivation
- Reciprocals of Volatilities ($1 / \sigma$):
  - Bills: $1 / 0.005 = 200.0$
  - 10-year note: $1 / 0.070 = 14.2857$
  - IG bonds: $1 / 0.060 = 16.6667$
  - Global equity: $1 / 0.160 = 6.2500$
  - **Sum of Reciprocals:** $200.0 + 14.2857 + 16.6667 + 6.2500 = \mathbf{237.2024}$
- Normalized Weights:
  - Bills: $200.0 / 237.2024 = \mathbf{84.3\%}$
  - 10-year note: $14.2857 / 237.2024 = \mathbf{6.0\%}$
  - IG bonds: $16.6667 / 237.2024 = \mathbf{7.0\%}$
  - Global equity: $6.2500 / 237.2024 = \mathbf{2.6\%}$
  - Reserve-eligible (Bills + 10-year): $84.3\% + 6.0\% = \mathbf{90.3\%}$

---

## 5. Proving It on the Known Answer (V)

The risk engine [`portfolio.py`](portfolio.py) was executed and yielded the exact published answers:

| Portfolio | Weights: bills / 10-year / IG / equity | Expected Return | Volatility | Reserve-Eligible | Meets 6.5% Objective? |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Benchmark** | $0.0 \ / \ 0.0 \ / \ 40.0 \ / \ 60.0$ | **6.80%** | **10.46%** | **0.0%** | **yes** |
| **Equal weight** | $25.0 \ / \ 25.0 \ / \ 25.0 \ / \ 25.0$ | **5.20%** | **5.21%** | **50.0%** | **no** |
| **Inverse volatility** | $84.3 \ / \ 6.0 \ / \ 7.0 \ / \ 2.6$ | **3.77%** | **1.05%** | **90.3%** | **no** |

### Mechanical Probes & Stress Checks

1. **Correlation Sensitivity Probe (IG–Equity Correlation $\to 0.50$):**
   - With correlation increased from $0.25$ to $0.50$, the covariance term doubles from $0.001152$ to $0.002304$.
   - New Variance: $0.009792 + 0.002304 = 0.012096$.
   - New Volatility: $\sqrt{0.012096} = \mathbf{11.00\%}$ *(exact match to expected probe value)*.
2. **Error Refusal / Validation Check:**
   - Setting IG–Equity correlation to $1.3$ causes `validate_correlation()` to immediately reject the inputs:
     `ValueError: Correlation value 1.3 at (2, 3) is outside the valid range [-1.0, 1.0].`
   - An asymmetric matrix similarly raises an explicit `ValueError`.
3. **Mandate Defense Breach (Candidate E):**
   - Added Benchmark to `mandate.py` as **Candidate E** ($0\%$ Bills, $0\%$ 10-year, $40\%$ IG Fund, $60\%$ Equity Fund).
   - `python mandate.py` result:
     `Reserve eligible: 0.0% / 3.0% minimum (FAIL) — Verdict: fails 1 rule(s)`
   - **Crucial Fiduciary Insight:** The client's own stated benchmark (S4) directly breaks the client's mandatory reserve rule (S3).

---

## 6. Diversification & Fiduciary Reflections

### 1. How Diversification Works
Portfolio variance includes cross-asset covariance terms ($2 w_i w_j \sigma_i \sigma_j \rho_{ij}$). When correlation $\rho_{ij} < 1.0$, the combined asset movements do not compound linearly; idiosyncratic shocks in one asset partially offset shocks in another. If correlation were $+1.0$, portfolio volatility would be a simple weighted average ($w_1 \sigma_1 + w_2 \sigma_2 = 0.40(6\%) + 0.60(16\%) = 12.0\%$). Because $\rho = 0.25$, actual volatility drops to **10.46%**, creating an uncompensated risk reduction.

### 2. Why Inverse Volatility Piles Into Bills
Inverse volatility weights each asset strictly proportional to $1 / \sigma_i$ without considering expected returns. Treasury bills have an ultra-low standalone volatility of $0.5\%$ ($0.005$), yielding a reciprocal of $200.0$. In contrast, global equities have $\sigma = 16.0\%$, yielding a reciprocal of only $6.25$. Because $200.0$ represents $84.3\%$ of the aggregate reciprocal sum ($237.2$), the rule allocates over eight-tenths of the reserve to cash equivalents, collapsing expected return to $3.77\%$ and failing the purchasing-power objective.

### 3. Which Baseline to Show the CIO First
**Show the Benchmark (40/60) first.**  
*Rationale:* It represents the foundation's strategic policy reference (S4) and proves that achieving the real return hurdle of 6.5% is attainable ($6.80\%$). However, showing that the Benchmark holds **0.0% reserve-eligible assets** immediately forces the CIO and committee to confront the mandate collision between S4 (benchmark tracking) and S3 ($3.0M liquidity reserve floor). It demonstrates that any viable portfolio must carve out cash/Treasuries from the equity/bond allocation.

---

## 7. Thursday Universe & Historical Price Dataset (`prices.csv`)

For Thursday's Streamlit application (Session 15), four liquid ETFs were selected to represent each required mandate sleeve:

| Role | Fund Name | Ticker | Expense Ratio | Mandate Eligibility |
| :--- | :--- | :---: | :---: | :--- |
| **Cash and reserve** | SPDR Bloomberg 1-3 Month T-Bill ETF | `BIL` | 0.14% | Reserve-Eligible (S3) |
| **Government bonds** | iShares 7-10 Year Treasury Bond ETF | `IEF` | 0.15% | Reserve-Eligible (S3) |
| **Fixed income** | iShares iBoxx $ Investment Grade Corporate Bond ETF | `LQD` | 0.14% | Non-Reserve (S4) |
| **Equity** | Vanguard Total World Stock ETF | `VT` | 0.07% | Non-Reserve (S4) |

### Historical Price Dataset Summary
- **File:** [`prices.csv`](prices.csv)
- **Source:** Yahoo Finance Monthly Historical Data (`Adj Close`)
- **Download Date:** October 20, 2026
- **History Range:** November 1, 2021 – October 1, 2026 (60 monthly observations / 5 full years)
- **Format:** Date first (`YYYY-MM-DD`), oldest month first, followed by tickers: `Date,BIL,IEF,LQD,VT`.

---

## 8. Growth Note (Ungraded & Personal)

> **Growth Note:**  
> Before this lab, I understood diversification intuitively as "not putting all your eggs in one basket," but deriving the benchmark's volatility by hand showed me the exact algebra: how the covariance cross-term drives risk reduction. Seeing that the classic student error gives 9.90% while the true volatility is 10.46% cemented why correlations cannot be ignored. I also found it eye-opening that the client's own benchmark fails the client's liquidity reserve rule—it proved to me that fiduciary mandate analysis requires auditing the interaction between rules before writing a single line of optimization code.
