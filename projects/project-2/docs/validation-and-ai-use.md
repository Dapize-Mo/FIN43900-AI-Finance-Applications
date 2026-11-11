# Validation, Model Risk Governance & AI Use Record

**Project:** FIN 43900 — Project 2: Investment Management Application  
**Student Analyst / Author:** **Oladapo Olaniyan** (`oolaniy@purdue.edu`)  
**Institution:** Mitchell E. Daniels, Jr. School of Business, Purdue University  
**Case / Client:** Meridian Foundation Reserve ($100 Million Portfolio)  
**As-Of Boundary:** November 10, 2026  
**Regulatory / Professional Reference:** Federal Reserve SR 26-2 ("Supervisory Guidance on Model Risk Management"), Sections V: Conceptual Soundness, Outcome Analysis, and Ongoing Monitoring  

---

### Mandatory Fiduciary & AI Disclosures

> **1. AI Tool Disclosure:** Anthropic Claude (Claude 3.5 Sonnet / Claude Opus 5.5) and Google Antigravity were utilized in designing analytical scripts, unit testing architecture, visualization ergonomics, and formatting optimization. All mathematical derivations, input validations, fiduciary constraints, and investment decisions were directed, verified, and finalized independently by the student analyst.  
> **2. Ownership & Academic Notice:** The analysis, models, interpretations, and committee recommendations presented herein are solely the author's work; this document is an educational simulation developed for academic demonstration in FIN 43900 at Purdue University, not personalized investment advice.

---

## 1. As-Of Boundary & Primary Data Sources

All modeling, optimization, and validation operations respect a strict temporal boundary of **November 10, 2026**.

| Dataset / Source | Frequency / Period | Provider / Agency | Primary Role | Boundary / Vintage Control |
| :--- | :--- | :--- | :--- | :--- |
| **ETF Sleeve Historical Prices** | Monthly (Nov 2021 – Oct 2026) | Yahoo Finance / S&P Dow Jones | Sample covariance, return & volatility benchmark | 5-Year historical sample; split- and dividend-adjusted |
| **Course-Authored Expected Values** | Parameterized | FIN 43900 Instructional Team | Governing forward-looking inputs for portfolio optimization | Fixed contractual values (Bills: 3.5%, 10Y: 4.3%, IG: 5.0%, Equity: 8.0%) |
| **ALFRED Macroeconomic Series** | Monthly (2020 – 2026) | Federal Reserve Bank of St. Louis / BLS | Point-in-time inflation audit (`CPIAUCSL`) | Dual timestamp ($t_{\text{event}}, t_{\text{pub}}$); evaluated across historical vintages |
| **Meridian Foundation Mandate** | Fact Set S1–S10 | Meridian Foundation Case (Lab 13) | Contractual governance & hard constraints | Governing institutional law |

---

## 2. Model Risk Management Framework (Federal Reserve SR 26-2 Alignment)

Federal Reserve SR 26-2 provides the professional standard for assessing whether an independent challenger should accept or reject an analytical financial model. While SR 26-2 explicitly excludes generative AI from its scope, we apply its three core pillars directly to our financial decision engine:

### A. Conceptual Soundness
- **Mathematical Integrity:** The covariance matrix is constructed as $\Sigma_{ij} = \rho_{ij} \sigma_i \sigma_j$. Input correlation matrices are validated to ensure symmetry ($\rho_{ij} = \rho_{ji}$), unit diagonals ($\rho_{ii} = 1.0$), and bounded intervals ($\rho_{ij} \in [-1, 1]$).
- **Mandate Fidelity:** The objective function minimizes variance subject to legal and contractual covenants: long-only weights ($\sum w_i = 1$, $w_i \ge 0$), non-negotiable liquidity floor ($w_{\text{Bills}} + w_{\text{10Y}} \ge 3.0\%$), and net real return hurdle ($E[R_{\text{net}}] \ge 6.50\%$).
- **Fiduciary Defect in Status Quo:** Proved that the Foundation's 60/40 benchmark conceptually breaches the mandate because diversified credit funds (`LQD`) cannot satisfy sovereign liquidity demands.

### B. Outcome Analysis & Baseline Reconciliation
- **Known-Answer Reconciliation:** Evaluated three simple baselines against published course anchors:
  - *Baseline 1 (Equal Weight):* Expected return 5.20%, Volatility 5.21%, Reserve Buffer 50.0% -> **FAILS return hurdle**.
  - *Baseline 2 (Policy Benchmark):* Expected return 6.80%, Volatility 10.46%, Reserve Buffer 0.0% -> **FAILS reserve buffer**.
  - *Constrained Optimal Portfolio:* Expected return 6.50%, Volatility 9.30%, Reserve Buffer 8.0% -> **PASSES all rules**.
- **Efficiency Dominance:** The Constrained Optimal Portfolio achieves lower volatility (9.30%) than the Policy Benchmark (10.46%) while unlocking $8.0M in legal liquidity.

### C. Ongoing Monitoring & Point-in-Time Data Governance
- **Vintage Audit of CPI (`CPIAUCSL`):** Provenance gate testing revealed that `CPIAUCSL` underwent seasonal revisions across 60 historical months when comparing vintage 2024-01-15 to modern releases.
- **Fiduciary Quarantine:** The engine strictly quarantines unadjusted macro feeds for backtesting, requiring exact publication-lag matching or substitution with unrevised headline CPI (`CPIAUCNS`).

---

## 3. The Locked Changed-Input Record (Base Requirement 6)

In strict adherence to the Week 6 verification pattern, the following test was designed, predicted without AI, and committed to the Git audit trail prior to execution.

```yaml
locked_changed_input_record:
  record_id: "LCIR-FIN43900-P2-001"
  timestamp_committed: "2026-11-10T19:30:00Z"
  human_analyst: "Oladapo Olaniyan"
  input_under_test: "Global Equity Expected Return Estimate (Sleeve: VT / Global Equity Index Fund)"
  parameter_units: "Percentage points / basis points per annum"
  baseline_value: 0.0800  # 8.00% per annum (800 bps)
  changed_value: 0.0700   # 7.00% per annum (700 bps; -100 bps macro shock)

  pre_run_human_prediction_ai_off: |
    If forward global equity returns drop by 100 bps from 8.00% to 7.00%, the optimization
    engine will be forced to aggressively reallocate capital from lower-yielding fixed income
    into equity in order to clear the non-negotiable 6.50% net return hurdle. 
    Consequently:
      1. Equity weight will surge toward 75-80%.
      2. IG corporate bond weight will drop significantly.
      3. Portfolio volatility will rise sharply, likely approaching or breaching 12.00%.
      4. This will trigger the quantitative Process Kill Condition.

  actual_model_output_post_run:
    stressed_equity_weight: 0.7800  # 78.0% (surged +26.0% from base 52.0%)
    stressed_ig_bond_weight: 0.1400  # 14.0% (collapsed -26.0% from base 40.0%)
    stressed_treasury_weight: 0.0800 # 8.0% (held exactly at reserve floor)
    stressed_net_return: 0.06504     # 6.504% (barely cleared hurdle)
    stressed_volatility: 0.1270      # 12.70% (spiked +340 bps from base 9.30%)
    kill_rule_triggered: True
    kill_reason: "KILL TRIGGER ACTIVATED: Portfolio volatility (12.70%) breaches 12.00% maximum committee risk tolerance."

  directional_evaluation:
    expected_direction: "Equity weight increases; Volatility increases; Kill rule triggers."
    actual_direction: "Equity weight increased to 78%; Volatility increased to 12.70%; Kill rule triggered."
    direction_match: True

  decision_effect: |
    Proves that the investment management process is brittle under equity return compression.
    If long-term equity returns fall below 7.00%, the Foundation CANNOT meet its 6.50% net
    hurdle without violating committee volatility limits. The committee must lower its spending
    payout rate rather than chasing equity beta.

  failure_diagnosis_and_sensitivity: |
    The prediction was directional and magnitude accurate. The optimizer exhausted all credit
    duration capacity, shifting entirely into equities because corporate credit (at 5.0%) could
    not mathematically bridge the return deficit. This confirms the critical necessity of an
    automated Process Kill Rule to prevent catastrophic risk-seeking behavior.
```

---

## 4. Verification Test Suite & Quantitative Checks

Automated programmatic unit checks verified the analytical engine before deployment:

| Test ID | Test Description | Input / Condition | Expected Result | Actual Result | Status |
| :--- | :--- | :--- | :--- | :--- | :---: |
| **TEST-01** | Correlation Matrix Symmetry | $\rho_{ij} == \rho_{ji}$ across $4 \times 4$ | Symmetric, unit diagonals | Symmetric, max error $< 10^{-12}$ | **PASS** |
| **TEST-02** | Equal Weight Known Answer | $w = [0.25, 0.25, 0.25, 0.25]$ | Ret: 5.20%, Vol: 5.21%, Res: 50.0% | Ret: 5.20%, Vol: 5.21%, Res: 50.0% | **PASS** |
| **TEST-03** | Benchmark Known Answer | $w = [0.0, 0.0, 0.40, 0.60]$ | Ret: 6.80%, Vol: 10.46%, Res: 0.0% | Ret: 6.80%, Vol: 10.46%, Res: 0.0% | **PASS** |
| **TEST-04** | Constrained Optimizer | Min vol s.t. Ret $\ge 6.5\%$, Res $\ge 3\%$ | Vol $< 10.46\%$, Ret $\ge 6.5\%$ | Vol: 9.30%, Ret: 6.50%, Res: 8.0% | **PASS** |
| **TEST-05** | Mandate Covenant Checker | Test Benchmark allocation | FAIL (Reserve buffer 0% < 3%) | FAIL with specific rule breach | **PASS** |
| **TEST-06** | ALFRED Provenance Gate | Test Sept 2026 CPI on 2026-09-30 | Unknowable / Post-dated | Quarantined; not released until mid-Oct | **PASS** |

---

## 5. Material AI Uses & Human Verification Ledger

| Date | AI Tool / Model | Specific Interaction / Prompt Objective | Generated Output Disposition | Human Verification & Control Check |
| :--- | :--- | :--- | :--- | :--- |
| **2026-11-10** | Claude 3.5 Sonnet / Antigravity | Scaffolding Streamlit UI tabs, container layouts, and Altair chart syntax | Accepted structure; refined theme CSS and responsive card containers | Manually verified Streamlit execution and verified no missing packages or layout bugs |
| **2026-11-10** | Claude Opus 5.5 | Grid search generator recursion and constraint pruning logic | Reused standard library generator algorithm | Checked algebraic correctness of weight vectors and verified grid step granularity |
| **2026-11-10** | Claude 3.5 Sonnet | Drafting Federal Reserve SR 26-2 model risk governance terminology | Adapted conceptual soundness and outcome analysis headers | Audited directly against official Federal Reserve SR 26-2 text; ensured exclusion of LLM claims |
| **2026-11-10** | Antigravity Engine | Locked Changed-Input Record schema validation | Adopted YAML structured record | Independently wrote pre-run prediction without AI before executing code |

---

## 6. Known Model Limitations & Fiduciary Caveats

1. **Static Covariance Assumption:** The optimization engine assumes a stationary covariance matrix. During acute liquidity crises (e.g., March 2020), correlations between corporate debt and equities approach unity, temporarily eliminating diversification benefits.
2. **Discrete Grid Step Granularity:** The weight search operates at a 2.0% step grid. Exact continuous quadratic programming might locate a marginally more optimal mix (within 2–5 bps of volatility), but the 2% grid provides practical trading granularity that respects realistic minimum ticket sizes.
3. **Execution Drag & Liquidity Haircuts:** While 5-day liquidity exceeds 90%, large-scale block liquidation of $40M in `LQD` during market dislocations could incur bid-ask slippage exceeding the baseline 20 bps model buffer.

