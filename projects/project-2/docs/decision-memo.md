# Investment Committee Decision Memo — Meridian Foundation Reserve

**To:** Investment Committee & Chief Investment Officer, Meridian Foundation  
**From:** Oladapo Olaniyan, Senior Portfolio Analyst (`oolaniy@purdue.edu`)  
**Date:** November 10, 2026  
**Subject:** Fiduciary Asset Allocation Recommendation & Mandate Compliance Audit ($100M Reserve)  
**Governance Standard:** Federal Reserve SR 26-2 Model Risk Management / CFA Institute Asset Allocation Standards  

---

### Mandatory Fiduciary & AI Disclosures

> **1. AI Tool Disclosure:** Anthropic Claude and Google Antigravity supported code structure, tests, and formatting. Oladapo Olaniyan directed, independently checked, and owns all models, inputs, and recommendations.  
> **2. Ownership & Academic Notice:** This is the author's own work, an educational simulation for FIN 43900 at Purdue University. It is not personalized investment advice.  

---

## 1. Decision

**Recommendation: ALLOCATE** to the Constrained Optimal Portfolio, under the monitoring triggers in Section 4. The 60/40 policy benchmark is not adoptable as written.

| Portfolio | Net return | Volatility | Sharpe | Reserve buffer (min 3.0%) | Mandate verdict | Finding |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| Equal Weight (1/N) | 5.20% | 5.21% | 0.33 | 50.0% | **FAIL** | Misses the 6.50% hurdle (-130 bps) |
| 60/40 Benchmark | 6.80% | 10.46% | 0.32 | 0.0% | **FAIL** | Holds $0 in Treasuries; breaks Fact S3 |
| **Constrained Optimal** | **6.50%** | **9.30%** | **0.32** | **8.0%** | **PASS** | Passes the six implemented mandate checks; -116 bps vol vs. benchmark |

Fact S3 requires 12 months of payouts ($3.0M, 3.0%) in cash or daily-liquid Treasuries. `LQD` credit funds do not qualify, so the benchmark breaches the mandate on day one. Equal weight is liquid but earns only 5.20% against the CPI + 4.0% (6.50%) hurdle.

## 2. Allocation Range

| Sleeve | Ticker | Target | Band | Capital |
| :--- | :--- | :---: | :---: | :---: |
| Global Equity | `VT` | **52.0%** | 48.0-55.0% | $52,000,000 |
| IG Corporate Bonds | `LQD` | **40.0%** | 36.0-44.0% | $40,000,000 |
| 10-Year Treasuries | `IEF` | **8.0%** | 3.0-10.0% | $8,000,000 |
| T-Bills / Cash | `BIL` | **0.0%** | 0.0-3.0% | $0 |

Sovereign reserve paper is 8.0% ($8.0M), 2.67x the required $3.0M buffer. Bands are tolerances, not approvals: each mix needs a fresh mandate check (48% VT / 39% LQD / 10% IEF / 3% BIL earns 6.325% and misses the hurdle). Returns assume zero trading costs; headroom at target is 0.4 bp.

## 3. Stress Test and Stop Condition

The engine stresses returns, credit spreads, correlations, costs, the estimation window and the reserve floor (ranges in the app).

**Stop condition:** at the tested input of 7.00% forward equity return (-100 bps), the 6.50% hurdle forces equity to 78% and volatility to 12.70%, above the modeled 12.00% committee ceiling, so the engine flags a stop (LCIR-001; 7.00% is a tested input, not an exact boundary). **Proposed committee action** (not enforced by the engine): cap equity at 50%, hold the rest in Treasuries (`BIL`/`IEF`), and vote on lowering the payout rate or the real-return hurdle. LCIR-002 (a 50 bp haircut to `LQD` expected return) gave volatility 9.70% and no stop; the optimizer exits `LQD` for 38% `IEF` / 60% `VT`, so the analyst's prediction was partly wrong. The 12.00% ceiling is a modeled limit; the mandate's 10% calendar-year loss statement (S9) is unverifiable as written and stays open for the committee.

## 4. Committee Ask and Reversal Triggers

The Committee is asked to (1) approve rebalancing the $100M to the targets above, (2) sweep excess cash quarterly into `BIL`/`IEF` to keep the $3.0M buffer, and (3) reconvene if any of these occurs:

- Rolling 12-month net real return is below CPI + 1.0% for two consecutive quarters.
- The 10-year Treasury yield falls below 3.0%.
- Annual tracking error versus the 60/40 benchmark exceeds 250 bps.

Governing facts (Lab 13): seven-year horizon with annual rebalancing (S1), a CPI + 4.0% objective over rolling five years, and committee approval for turnover above 25% a year (S7).

## 5. Data Governance

Inflation (`CPIAUCSL`) is audited against ALFRED vintages: values not yet published by the decision date are excluded ($t_{\text{pub}} \le t_{\text{decision}}$). The app shows this for one snapshot (decision date 2026-09-30: September CPI excluded, August 334.131 returned); the data file has fixed vintage columns, not per-observation publication dates. CPI does not feed the optimizer, which uses a fixed 2.50% inflation input. Details: `docs/validation-and-ai-use.md`.
