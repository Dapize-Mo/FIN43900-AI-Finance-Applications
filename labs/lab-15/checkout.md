# FIN 43900 Lab 15 — Portfolio Stability Decision

**Course:** FIN 43900 — AI Finance Applications, Purdue University  
**Student Analyst:** **Oladapo Olaniyan** (`oolaniy@purdue.edu`)  
**Teammate / Learning Partner:** **J. Maffei** (`maffeij@purdue.edu` | Target Company: Oracle Corp. — `ORCL`)  
**Institution:** Mitchell E. Daniels, Jr. School of Business, Purdue University  
**Case:** Meridian Foundation Reserve ($100 Million Reserve) & Student Universe  
**Lab Date:** October 22, 2026  
**Brightspace Item:** Lab 15 — Portfolio Stability Decision (Thursday Merit Checkout, 25 Points)  
**Session Token:** `webapp`  
**GitHub Direct Script Link:** [portfolio.py on GitHub](https://github.com/Dapize-Mo/FIN43900-AI-Finance-Applications/blob/main/labs/lab-15/portfolio.py)  
**GitHub Direct App Link:** [app.py on GitHub](https://github.com/Dapize-Mo/FIN43900-AI-Finance-Applications/blob/main/labs/lab-15/app.py)  
**GitHub Direct Checkout Link:** [checkout.md on GitHub](https://github.com/Dapize-Mo/FIN43900-AI-Finance-Applications/blob/main/labs/lab-15/checkout.md)  
**Live Streamlit App:** [Portfolio Stability Decision](https://fin439-lab15-portfolio-stability.streamlit.app/)  

---

## 📌 1. Executive Summary & Core Question (D)

> **Core Question (D):**  
> *Which mix carries the least risk while meeting the mandate — and does the answer survive a one-point change in one estimate?*

This checkout deliverable documents the transformation of the Tuesday Lab 14 Python risk engine into an interactive **Streamlit web application** ([`app.py`](app.py)). The application connects directly to [`portfolio.py`](portfolio.py) to find the minimum-variance long-only portfolio satisfying the mandate's target return hurdle ($\ge 6.50\%$) and liquidity reserve floor ($\ge 3.0\%$).

Through systematic stress testing, this analysis reveals the fundamental vulnerability of portfolio optimization: **estimation risk and parameter hypersensitivity**. On the Meridian training case, a single 1.0-point adjustment in equity return expectations ($8.0\% \to 7.0\%$) forces the optimizer to shift **25 points of portfolio capital** (moving equity from $55\%$ to $80\%$). On our empirical student universe (`BIL`, `IEF`, `LQD`, `VT`), shifting between 5-year and 3-year historical estimation windows triggers an identical **25-point capital swing** (shifting T-bills from $60\%$ to $85\%$). Because the optimizer acts as an "error maximizer," we formally conclude: **PILOT, NOT ADOPT**, with adoption strictly contingent on committee-approved forward-looking Capital Market Assumptions (CMAs).

---

## 2. Training Set Verification (V): Meridian Foundation Known Answers

The application imports calculation routines and training inputs directly from [`portfolio.py`](portfolio.py) without duplicating mathematical logic.

### Meridian Baseline vs. Equity Shock ($8.0\% \to 7.0\%$)

| Run Specification | Weights: Bills / 10-year / IG / Equity | Expected Return | Portfolio Volatility | Reserve-Eligible Weight | Mandate Status |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Meridian As Loaded** | **`0 / 20 / 25 / 55`** | **6.51%** | **9.44%** | **20.0%** | Feasible ($\ge 6.5\%$ ret, $\ge 3\%$ res) |
| **Equity Return $8.0\% \to 7.0\%$** | **`0 / 10 / 10 / 80`** | **6.53%** | **12.94%** | **10.0%** | Feasible |
| **Absolute Shift** | `0 / -10 / -10 / +25` | — | $+3.50\%$ | $-10.0\%$ | **Largest Shift: 25 points** |

- **Verification Confirmation:** Both runs reproduce the exact published course known answers down to the second decimal.
- **Economic Insight:** When equity return is reduced by just 100 basis points, safe fixed-income assets can no longer support the 6.50% return hurdle. To avoid mathematical infeasibility, the optimizer aggressively strips 10 points from 10-year Treasuries and 10 points from IG bonds, concentrating 80% into equity and driving portfolio volatility from **9.44% to 12.94%**.

### Proving Direct Engine Connection (IG–Equity Correlation to 0.50)

To verify that [`app.py`](app.py) directly references the underlying calculation engine in [`portfolio.py`](portfolio.py):

1. In `portfolio.py`, the off-diagonal correlation between Investment Grade bonds and Global Equities was changed from `0.25` to `0.50` in both symmetric cells.
2. The Streamlit browser page was refreshed without changing the objective ($6.5\%$) or reserve floor ($3.0\%$).
3. **Engine Probe Result:**
   - Optimal Weights: **`0 / 40 / 0 / 60`**
   - Expected Return: **`6.52%`**
   - Portfolio Volatility: **`9.73%`**
   - Reserve-Eligible Weight: **`40.0%`**
4. The correlation was restored to `0.25`, immediately returning the display to `0 / 20 / 25 / 55` at `6.51%` and `9.44%`. This proves zero copied math exists in `app.py`.

---

## 3. Data Provenance & Historical Estimation (R)

For the empirical analysis, five years of monthly adjusted close prices were compiled in [`prices.csv`](prices.csv).

### Asset Universe & Mandate Classification

| Sleeve Role | Representative Fund | Ticker | Data Source | Download Date | Mandate Eligibility |
| :--- | :--- | :---: | :--- | :---: | :--- |
| **Cash and reserve** | SPDR Bloomberg 1-3 Month T-Bill ETF | `BIL` | Yahoo Finance (`Adj Close`) | Oct 20, 2026 | **Reserve-Eligible** (S3 Sovereign) |
| **Government bonds** | iShares 7-10 Year Treasury Bond ETF | `IEF` | Yahoo Finance (`Adj Close`) | Oct 20, 2026 | **Reserve-Eligible** (S3 Sovereign) |
| **Fixed income** | iShares iBoxx $ Inv Grade Corporate Bond ETF | `LQD` | Yahoo Finance (`Adj Close`) | Oct 20, 2026 | **Non-Reserve** (Credit / Fund Risk) |
| **Global equity** | Vanguard Total World Stock ETF | `VT` | Yahoo Finance (`Adj Close`) | Oct 20, 2026 | **Non-Reserve** (Market Equity Risk) |

*Important Disclosure:* A five-year historical average represents past realized sample path, **not a forward-looking forecast**. All annualized parameters below are strictly designated as **`estimates`**.

### Parameter Estimation Mechanics

- Monthly return: $R_t = (P_t - P_{t-1}) / P_{t-1}$
- Annualized Expected Return: $\hat{\mu} = \bar{R}_{\text{monthly}} \times 12$
- Annualized Sample Volatility: $\hat{\sigma} = s_{\text{monthly}} \times \sqrt{12}$
- Correlation: Sample Pearson correlation coefficient $\hat{\rho}_{ij} = \frac{\sum (R_{i,t} - \bar{R}_i)(R_{j,t} - \bar{R}_j)}{(N-1) s_i s_j}$

### Estimated Parameter Comparison: 60 Months vs. Last 36 Months

| Asset Ticker | 60-Month Return (Est) | 60-Month Vol (Est) | 36-Month Return (Est) | 36-Month Vol (Est) | Regime Shift Explanation |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **`BIL`** | **3.71%** | **0.47%** | **4.30%** | **0.22%** | Higher cash yield following Fed rate hikes; near-zero vol |
| **`IEF`** | **-1.67%** | **7.73%** | **4.17%** | **6.56%** | Suffered massive 2022 duration losses; recovered post-2023 |
| **`LQD`** | **-0.63%** | **9.89%** | **6.10%** | **7.66%** | 2022 rate drawdown suppressed 5-yr return; rebounded strongly |
| **`VT`** | **11.61%** | **14.84%** | **21.26%** | **11.43%** | Trailing 36 months captures massive global tech-led equity bull market |

#### 60-Month Correlation Matrix

```text
        BIL     IEF     LQD      VT
BIL   1.000   0.238   0.287   0.237
IEF   0.238   1.000   0.938   0.644
LQD   0.287   0.938   1.000   0.798
VT    0.237   0.644   0.798   1.000
```

#### Last 36-Month Correlation Matrix

```text
        BIL     IEF     LQD      VT
BIL   1.000   0.168   0.247   0.216
IEF   0.168   1.000   0.933   0.518
LQD   0.247   0.933   1.000   0.662
VT    0.216   0.518   0.662   1.000
```

---

## 4. Student Universe Optimization & Stability Results

We applied the client's mandatory constraints:

- **Objective:** $\ge 6.50\%$ annualized expected return.
- **Reserve Rule:** $\ge 3.0\%$ in daily-liquid sovereign paper (`BIL` or `IEF`).
- **Policy Boundaries:** Long-only, 5-point grid steps ($w_i \ge 0, \sum w_i = 1.0$).

### Search Results Across Historical Estimation Windows

| Horizon Window | Optimal Allocation (BIL / IEF / LQD / VT) | Expected Return (Est) | Portfolio Volatility (Est) | Reserve-Eligible Weight | Mandate Feasibility |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **All Months (60 mo)** | **`60 / 0 / 0 / 40`** | **6.87%** | **6.01%** | **60.0%** | Meets Mandate |
| **Last 36 Months** | **`85 / 0 / 0 / 15`** | **6.84%** | **1.76%** | **85.0%** | Meets Mandate |
| **Window Shift** | `+25 / 0 / 0 / -25` | $-0.03\%$ | $-4.25\%$ | $+25.0\%$ | **Largest Shift: 25 points** |

### Stability Diagnosis: Horizon Sensitivity

Moving from a 5-year sample to a 3-year sample shifts **25% of the total endowment reserve** ($25 Million on a $100M fund):

- In the 36-month window, `VT` delivered an annualized return of **21.26%**.
- Because equities were extraordinarily high-yielding, the optimizer required only a small **15% equity allocation** to clear the 6.50% target ($0.85 \times 4.30\% + 0.15 \times 21.26\% = 6.84\%$).
- The optimizer dumped the remaining **85% into ultra-safe T-bills (`BIL`)**, driving reported volatility down to an artificially tranquil **1.76%**.
- In contrast, across the full 60 months (which includes the 2022 market decline), `VT` earned a more moderate 11.61%, forcing the optimizer to hold **40% in equities and 60% in T-bills**, with volatility rising to **6.01%**.

### Infeasibility Handling

If the investment committee raises the return objective above the highest available asset return (e.g. $> 11.61\%$ for the 60-month dataset or $> 21.26\%$ for the 36-month dataset), the engine prints and displays **"no mix meets the objective"**. Per course rules, **we never lower the client's objective to manufacture an artificial mix**.

---

## 5. Partner Attack & Defense

> **Partner Attack Scenario:**  
> A skeptical partner opens the Streamlit application, reviews the trailing 36-month inputs, and immediately challenges the **21.26% annualized return for `VT`** as unrealistic recency bias. The partner reduces `VT`'s return box to **10.00%**.

### Two-Sentence Fiduciary Response

"The optimizer's radical 25-point reallocation back into equities (shifting allocation from 85/0/0/15 to 60/0/0/40 and spiking volatility from 1.76% to 4.60%) proves that the ultra-safe 85% T-bill portfolio was a fleeting byproduct of trailing bull-market equity returns rather than a stable asset allocation. Under any normalized forward-looking equity risk premium, the model is compelled to aggressively increase equity exposure to clear the foundation's 6.50% purchasing power hurdle."

*(Note: If the partner further cuts equity return to 8.00%, the allocation swings by 50 points to `35 / 0 / 10 / 55`, with volatility escalating to 6.83%).*

---

## 6. The Fiduciary Call: Adopt, Pilot, or Reject?

### The Decision: **PILOT, NOT ADOPT**

### Specific Condition Tied to Stress Results

> **Fiduciary Call:**  
> **"Pilot, not adopt:** Across both the Meridian training set and our empirical ETF universe, the optimizer exhibits extreme parameter hypersensitivity—a single 1-point change in equity expectations shifts 25 points of capital into equities, and changing historical sampling windows moves 25 points between cash and equities. We pilot this mix solely as a provisional analytical benchmark, and will adopt a live implementation portfolio only after the Investment Committee and CIO formally approve forward-looking Capital Market Assumptions (CMAs) anchored to long-term macroeconomic fundamentals, accompanied by mandatory portfolio sleeve minimums and maximums (e.g., maximum 60% equity, minimum 20% fixed income) to prevent optimizer corner solutions."

---

## 7. Code Walkthrough: Grid Search Engine

Below is the annotated search routine in [`portfolio.py`](portfolio.py):

```python
def search_lowest_risk_mix(
    sleeves: List[Dict[str, Any]],
    cov: List[List[float]],
    objective: float = 0.065,
    reserve_min: float = 0.030,
    step: int = 5,
) -> Optional[Dict[str, Any]]:
    best_weights: Optional[List[float]] = None
    best_volatility = float("inf")
    best_return = 0.0
    best_reserve = 0.0
    n = len(sleeves)

    # 1. Iterate across all long-only weight combinations in 5-point steps summing to 100%
    for weights in generate_weight_grid(n, step=step):
        ret = compute_expected_return(weights, sleeves)
        reserve = compute_reserve_weight(weights, sleeves)

        # 2. Hard feasibility test: must clear both the return target and reserve floor
        if ret >= (objective - 1e-9) and reserve >= (reserve_min - 1e-9):
            vol = compute_portfolio_volatility(weights, cov)

            # 3. Track the feasible mix that minimizes total portfolio volatility
            if vol < best_volatility - 1e-9:
                best_volatility = vol
                best_weights = weights
                best_return = ret
                best_reserve = reserve

    # 4. Return None if no combination satisfies the constraints
    if best_weights is None:
        return None

    return {
        "weights": best_weights,
        "return": best_return,
        "volatility": best_volatility,
        "reserve": best_reserve,
        "meets_objective": True,
    }
```

### Partner Question & Code Explanation

- **Partner's Question:** *"Why is `1e-9` subtracted from `objective` and `reserve_min` in the comparison?"*
- **Answer from the Code:** In Python, standard floating-point arithmetic introduces tiny rounding inaccuracies (e.g. $0.05 + 0.10 = 0.15000000000000002$ or $0.065 - 0.065 = 1.38 \times 10^{-17}$). Using a strict tolerance of `1e-9` prevents valid portfolio mixes that hit exactly 6.500000% from being falsely discarded due to machine precision noise.

---

## 8. Estimation Risk: Learn on Your Own

### 1. What is Estimation Risk?

Estimation risk is the financial risk that an optimization model treats statistical sample estimates (historical sample means, sample standard deviations, and correlation coefficients) as exact, known parameters. Because historical data contains sample noise, regime changes, and estimation error, an allocation optimized purely on historical estimates is fitted to past sample noise rather than the true underlying distribution of returns.

### 2. How Does It Work — Why Does an Optimizer Amplify Errors?

As demonstrated by Richard Michaud (1989), mean-variance optimizers are fundamentally **"error maximizers"**.

1. The optimization objective rewards higher expected returns linearly while penalizing portfolio variance quadratically.
2. If an asset's expected return is overestimated due to a favorable sample window (such as `VT`'s 21.26% return over the last 36 months), the optimizer treats this asset as artificially productive and over-allocates capital to it.
3. Conversely, if an asset suffered a temporary drawdown in the sample period (such as `IEF`'s -1.67% return over 5 years due to the 2022 rate shock), the optimizer treats it as structurally impaired and zeroes it out completely.
4. Consequently, small estimation errors in expected returns are magnified into massive, erratic shifts in recommended portfolio weights.

### 3. Explaining Estimation Risk Using Our Largest Weight Change

In our student dataset, the choice between looking at a 5-year sample vs. a 3-year sample changed the trailing equity return from 11.61% to 21.26%. This difference caused the optimizer to swing **25% of the portfolio ($25 Million)** between equities and Treasury bills. If a CIO blindly deployed the 36-month mix (85% T-bills, 15% equity) expecting 6.84% return, but equity returns subsequently reverted to a historical 8% mean, the portfolio would earn only $4.85\%$, massively failing the foundation's 6.50% spending mandate.

---

## 9. Reflection & Personal Growth Note

### 1. Why Did the Lowest-Risk Mix Move So Far?

The lowest-risk mix moved so dramatically because the portfolio constraints create a tight boundary along the efficient frontier. When equity return is lowered from 8.0% to 7.0%, the lower-risk sleeves (bills at 3.5%, 10-year notes at 4.3%, IG bonds at 5.0%) cannot generate enough return to reach 6.50%. The only mathematical lever remaining to clear the return hurdle is to massively ramp up the equity allocation from 55% to 80%, despite the severe penalty in portfolio volatility.

### 2. What Would You Need to See Before You Adopted It?

Before recommending live portfolio adoption to the Investment Committee, I would require:

1. **Bayesian Shrinkage / Black-Litterman Priors:** Blending historical returns with a global equilibrium market benchmark to shrink extreme sample means toward economic reality.
2. **Minimum & Maximum Allocation Bands:** Enforcing policy bands (e.g. $15\% \le \text{Equity} \le 60\%$, $10\% \le \text{IG Bonds} \le 40\%$) to prevent the optimizer from establishing 0% or 80% corner solutions.
3. **Multi-Regime Stress Testing:** Simulating asset performance across stagflationary, recessionary, and rate-hiking environments rather than relying on a single backward-looking window.

### Growth Note (Personal & Ungraded)

> **Personal Growth Note:**  
> Moving from the command-line calculations of Lab 14 to an interactive Streamlit app in Lab 15 made the theoretical concept of "estimation risk" concrete. It was striking to see that changing a single return box by 1.0% caused the optimizer to reallocate a quarter of a $100 Million endowment. This exercise showed me that quantitative finance is not about blindly trusting algorithms, but understanding their failure modes. A true fiduciary does not present an "optimal" mix as gospel; they test how fragile that optimum is before putting real capital at risk.
