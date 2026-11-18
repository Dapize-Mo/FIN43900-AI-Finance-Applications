# Investment Committee Decision Memo — Meridian Foundation Reserve

**To:** Investment Committee & Chief Investment Officer, Meridian Foundation  
**From:** Oladapo Olaniyan, Senior Portfolio Analyst (`oolaniy@purdue.edu`)  
**Date:** November 10, 2026  
**Subject:** Fiduciary Asset Allocation Recommendation & Mandate Compliance Audit ($100M Reserve)  
**Governance Standard:** Federal Reserve SR 26-2 Model Risk Management / CFA Institute Asset Allocation Standards  

---

### Mandatory Fiduciary & AI Disclosures

> **1. AI Tool Disclosure:** Anthropic Claude (Claude 3.5 Sonnet / Claude Opus) and Google Antigravity were utilized in designing analytical scripts, visualization ergonomics, and formatting optimization. All mathematical derivations, input validations, fiduciary constraints, and investment decisions were directed, verified, and finalized independently by the student analyst.  

---

## 1. Decision

**Recommendation: ALLOCATE** to the Constrained Optimal Portfolio, under the monitoring triggers in Section 4. The 60/40 policy benchmark is not adoptable as written.

| Portfolio | Net return | Volatility | Sharpe | Reserve buffer (min 3.0%) | Mandate verdict | Finding |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| Equal Weight (1/N) | 5.20% | 5.21% | 0.33 | 50.0% | **FAIL** | Misses the 6.50% hurdle (-130 bps) |
| 60/40 Benchmark | 6.80% | 10.46% | 0.32 | 0.0% | **FAIL** | Holds $0 in Treasuries; breaks Fact S3 |
| **Constrained Optimal** | **6.50%** | **9.30%** | **0.32** | **8.0%** | **PASS** | Meets all six covenants; -116 bps vol vs. benchmark |

Fact S3 requires 12 months of payouts ($3.0M, 3.0%) in cash or daily-liquid Treasuries. `LQD` credit funds do not qualify, so the benchmark breaches the mandate on day one. Equal weight is liquid but earns only 5.20% against the CPI + 4.0% (6.50%) hurdle.

## 2. Allocation Range

| Sleeve | Ticker | Target | Band | Capital |
| :--- | :--- | :---: | :---: | :---: |
| Global Equity | `VT` | **52.0%** | 48.0-55.0% | $52,000,000 |
| IG Corporate Bonds | `LQD` | **40.0%** | 36.0-44.0% | $40,000,000 |
| 10-Year Treasuries | `IEF` | **8.0%** | 3.0-10.0% | $8,000,000 |
| T-Bills / Cash | `BIL` | **0.0%** | 0.0-3.0% | $0 |

Sovereign reserve paper is 8.0% ($8.0M), 2.67x the required $3.0M buffer.

## 3. Stress Test and Stop Condition

The engine was stressed on estimates (equity haircut 0-250 bps, credit spread 0-150 bps), correlations (stock-bond spike up to +0.80), costs (0-60 bps), the estimation window (12-60 months of prices) and constraints (reserve floor 3-12%).

**Process kill condition:** if forward equity return falls below **7.00%** (-100 bps), the 6.50% hurdle forces equity to 78% and volatility to 12.70%, above the **12.00%** committee ceiling. Optimization stops, equity is capped at 50% with the rest in Treasuries (`BIL`/`IEF`), and the committee must vote to lower the payout rate or the real-return hurdle. Locked Changed-Input Records in `docs/validation-and-ai-use.md` test this input (LCIR-001) and a +50 bps credit spread shock (LCIR-002: volatility 9.70%, no kill, optimizer exits `LQD` for 38% `IEF` / 60% `VT`, so the analyst's prediction was partly wrong).

## 4. Committee Ask and Reversal Triggers

The Committee is asked to (1) approve rebalancing the $100M to the targets above, (2) sweep excess cash quarterly into `BIL`/`IEF` to keep the $3.0M buffer, and (3) reconvene if any of these occurs:
- Rolling 12-month net real return is below CPI + 1.0% for two consecutive quarters.
- The 10-year Treasury yield falls below 3.0%.
- Annual tracking error versus the 60/40 benchmark exceeds 250 bps.

## 5. Data Governance

Inflation (`CPIAUCSL`) is audited with ALFRED vintages: modern series carry retroactive seasonal revisions, so decisions use only values published by the decision date ($t_{\text{pub}} \le t_{\text{decision}}$). Method and limits are in `docs/validation-and-ai-use.md`.
