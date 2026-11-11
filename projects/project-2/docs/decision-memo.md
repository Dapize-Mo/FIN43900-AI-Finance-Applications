# Investment Committee Decision Memo — Meridian Foundation Reserve

**To:** Investment Committee & Chief Investment Officer, Meridian Foundation  
**From:** Oladapo Olaniyan, Senior Portfolio Analyst (`oolaniy@purdue.edu`)  
**Date:** November 10, 2026  
**Subject:** Fiduciary Asset Allocation Recommendation & Mandate Compliance Audit ($100M Reserve)  
**Governance Standard:** Federal Reserve SR 26-2 Model Risk Management / CFA Institute Asset Allocation Standards  

---

### Mandatory Fiduciary & AI Disclosures

> **1. AI Tool Disclosure:** Anthropic Claude (Claude 3.5 Sonnet / Claude Opus) and Google Antigravity were utilized in designing analytical scripts, visualization ergonomics, and formatting optimization. All mathematical derivations, input validations, fiduciary constraints, and investment decisions were directed, verified, and finalized independently by the student analyst.  
> **2. Ownership & Academic Notice:** The analysis, models, interpretations, and committee recommendations presented herein are solely the author's work; this memorandum is an educational simulation developed for academic demonstration in FIN 43900 at Purdue University, not personalized investment advice.

---

## 1. Executive Decision & Recommendation

We recommend that the Investment Committee **ALLOCATE TO THE CONSTRAINED OPTIMAL PORTFOLIO** under a governed transition structure, rather than adopting the unconstrained policy benchmark.

| Portfolio Option | Net Expected Return | Annualized Volatility | Sharpe Ratio | Reserve Buffer ($\ge 3.0\%$) | Mandate Verdict | Primary Fiduciary Finding |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **Baseline 1: Equal Weight ($1/N$)** | 5.20% | 5.21% | 0.33 | 50.0% | **FAIL** | Violates 6.50% net return hurdle (drags -130 bps) |
| **Baseline 2: Policy Benchmark (60/40)** | 6.80% | 10.46% | 0.32 | 0.0% | **FAIL** | Violates 3.0% reserve buffer floor (holds $0 in Treasuries) |
| **Constrained Optimal Portfolio** | **6.50%** | **9.30%** | **0.32** | **8.0%** | **PASS** | Fully compliant; dominates benchmark on risk (-116 bps vol) |

### The Core Problem with the Status Quo
The Foundation's current policy benchmark (60% Global Equity / 40% Investment Grade Corporate Bonds) suffers from a critical contractual flaw: **it holds zero reserve-eligible sovereign liquidity**. Under Fact S3 of the Meridian Mandate, the Foundation is legally obligated to maintain at least 12 months of quarterly spending payouts ($3.0M / 3.0%) in cash or daily-liquid sovereign securities (U.S. Treasury bills or notes). Corporate bond funds (`LQD`) carry credit spread risk and settlement lags, disqualifying them from the reserve buffer. Adopting the benchmark as written creates an immediate covenant breach.

Conversely, a naive equal-weight allocation ($25\%$ in each sleeve) provides abundant liquidity ($50\%$), but severely penalizes the endowment, delivering only **5.20% net return** against the CPI + 4.0% (**6.50%**) hurdle, guaranteeing long-term purchasing power erosion.

---

## 2. Recommended Asset Allocation & Rebalancing Bands

To satisfy the real return objective while strictly honoring all liquidity, concentration, and long-only mandates, we recommend deploying capital across the following target weights and tolerance bands:

| Asset Sleeve | Target Ticker | Fiduciary Role | Target Weight | Minimum Band | Maximum Band | Target Capital ($100M) |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: |
| **Global Equity** | `VT` | Real return engine | **52.0%** | 48.0% | 55.0% | $52,000,000 |
| **U.S. IG Corporate Bonds** | `LQD` | Income & yield generation | **40.0%** | 36.0% | 44.0% | $40,000,000 |
| **U.S. 10-Year Treasury Notes** | `IEF` | Duration & reserve buffer | **5.0%** | 3.0% | 8.0% | $5,000,000 |
| **U.S. Treasury Bills / Cash** | `BIL` | Immediate payout reserve | **3.0%** | 3.0% | 5.0% | $3,000,000 |
| **Total Portfolio** | — | — | **100.0%** | — | — | **$100,000,000** |

*Note: Total sovereign reserve-eligible paper is 8.0% ($8.0M), providing an immediate 2.67x coverage ratio over the required 12-month spending buffer ($3.0M).*

---

## 3. Stress Testing & Quantitative Stop / Kill Condition

In compliance with SR 26-2 outcome analysis, the portfolio engine was subjected to multi-factor macro stress shocks:
1. **Equity Return Haircut:** Evaluated from 8.0% down to 6.50%.
2. **Correlation Breakdown:** Shocked stock-bond correlation from -0.10 to +0.40.
3. **Execution Friction:** Factored 20 bps annual turnover and management drag.

### The Stop / Kill Condition
The process establishes an explicit, quantitative **PROCESS KILL CONDITION**:
> **Trigger Rule:** If forward equity return expectations fall below **7.00%** (a 100 bps haircut from base estimates), the portfolio optimization engine becomes unstable: attempting to satisfy the 6.50% net hurdle requires equity concentration to rise above 75%, forcing portfolio volatility past **12.00%** (violating the Foundation's maximum volatility tolerance).

**Mandatory Action Upon Trigger:**
If the Kill Condition is triggered, active optimization is immediately suspended. Discretion is revoked from the manager, equity exposure is capped at 50%, and the remaining 50% is locked into sovereign Treasuries (`BIL` / `IEF`) until the Investment Committee formally votes to either lower the quarterly spending distribution rate or accept a lower real return hurdle.

---

## 4. Point-in-Time Data Governance (ALFRED Audit)

Macroeconomic signals governing the inflation hurdle (`CPIAUCSL`) were audited using Federal Reserve Bank of St. Louis ALFRED vintages. Modern FRED series reflect retroactive annual 5-year seasonal factor revisions (altering 60 historical monthly prints). Naive backtests using modern series introduce severe look-ahead bias. Under our governance framework, `CPIAUCSL` is placed under **Fiduciary Quarantine**: monthly inflation is verified strictly on point-in-time publication dates ($t_{\text{pub}} \le t_{\text{decision}}$) or benchmarked against unrevised headline figures (`CPIAUCNS`).

---

## 5. Ongoing Monitoring Triggers & Committee Action

We request that the Investment Committee approve:
1. **Immediate Execution:** Rebalance the $100M reserve to the Constrained Optimal Portfolio targets.
2. **Quarterly Liquidity Review:** Sweep excess cash flow into `BIL` to maintain the 12-month $3.0M spending buffer.
3. **Reversal Triggers:** Mandatory committee convening if:
   - Rolling 12-month net real return falls below CPI + 1.0% (3.5% total return) for two consecutive quarters.
   - 10-year Treasury yield drops below 3.0%, impairing sovereign reserve income.
   - Annual tracking error relative to the 60/40 benchmark exceeds 250 bps.

