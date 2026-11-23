# FIN 43900 — AI Robo Advisor Decision System

**Author:** Oladapo Olaniyan  
**Course:** FIN 43900 — AI Finance Applications, Daniels School of Business, Purdue University  
**Date:** November 23, 2026  
**Session:** Week 14 Studio Lab (Tuesday, November 24 Practice Session)  
**Tutorial Video Reference:** [Dr. Z Tutorial — Build based on existing repo](https://youtu.be/Bm0qwSymvX8)  
**Base Open-Source Repository:** [`matvix90/ai-robo-advisor`](https://github.com/matvix90/ai-robo-advisor)  

---

## 1. Executive Overview & Assignment Context

In the class announcement posted on November 19, 2026, Dr. Z assigned students to implement and improve the AI Robo Advisor for practice during Thanksgiving week:

> *There is no in-person meeting this Tuesday, November 24. Your job will be to implement the Robo Advisor for practice.*  
> **Tasks:**  
> 1. *Implement the Robo Advisor by following the [tutorial video](https://youtu.be/Bm0qwSymvX8)*  
> 2. *Improve the app together with codex*  
> 3. *Optional: Find another Opensource GitHub repo and make a new version of yours.*  

This repository package contains a complete, robust, and production-ready implementation of the AI Robo Advisor, fulfilling all baseline tasks and the optional quantitative architecture comparison.

---

## 2. Architecture: Multi-Agent Investment Pipeline

Following the architectural design of `matvix90/ai-robo-advisor` demonstrated in Dr. Z's tutorial video, the system implements a four-stage multi-agent orchestration pipeline:

```
[User Questionnaire] 
       │
       ▼
[Investment Agent] ──▶ Computes Objective Risk Score (1-100) & Capital Capacity
       │
       ▼
[Strategy Agent] ───▶ Formulates Macro Asset Allocation (Equities, Bonds, Real Estate, Cash)
       │
       ▼
[Portfolio Agent] ──▶ Selects Premier Low-Cost ETFs (VTI, VXUS, BND, IEF, VNQ, BIL)
       │
       ▼
[Analyst Sub-Agents] ──┬─▶ [Fees Agent] (TER Audit < 0.15%)
                       ├─▶ [Diversification Agent] (HHI Concentration & Effective N)
                       ├─▶ [Mandate Alignment Agent] (Risk Tolerance & Liquidity Buffer)
                       └─▶ [Performance Agent] (2-Yr CAGR, Sharpe, Drawdown, Alpha, Beta)
       │
       ▼
[Analysis Orchestrator] ──▶ Fiduciary Disposition: [APPROVED] vs [REVISION_REQUIRED]
```

---

## 3. Key Enhancements Developed Together with Codex

In his 50-minute walkthrough, Dr. Z encountered several friction points and specifically recommended areas for student enhancement. Our implementation resolves each issue:

| Feature / Dimension | Original Base Repo (`matvix90`) | Video Pain Point Identified by Dr. Z | Our Codex Enhanced Implementation |
| :--- | :--- | :--- | :--- |
| **Financial Market Data** | Requires paid Polygon.io API key ($29/month) | Polygon free tier rate limit (5 calls/min) crashed the run with HTTP 429 | **Dual-Source Keyless Engine:** Uses `yfinance` as free primary data provider with automatic local caching, zero API cost, and optional throttled Polygon fallback. |
| **User Interface** | Primitive terminal CLI with text prompts | Clunky CLI requiring re-typing 15 questions upon any restart | **Interactive Streamlit Web Dashboard (`app.py`):** Visual sliders, Plotly donut allocation charts, cumulative backtest performance lines, KPI cards, and memo export. |
| **State Persistence** | In-memory only; crashed state lost completely | Dr. Z explicitly noted: *"Save progress after failed run so UX is much better"* | **Session Auto-Recovery (`storage.py`):** Saves preferences to JSON/SQLite so users resume instantly with zero repeated data entry. |
| **LLM Dependency & Failure** | Hard requirement on OpenAI API key | Quota exhaustion or API key failures halt the program entirely | **Hybrid Dual-Engine:** High-performance deterministic Modern Portfolio Theory (MPT) heuristics guarantee zero-downtime execution even without API keys. |
| **Second Architecture (Optional Task)** | None | "Find another open-source GitHub repo and make a new version" | **Markowitz MPT Quantitative Engine (`MPTQuantitativeEngine`):** Integrates classical mean-variance optimization (Maximum Sharpe & Minimum Volatility) for side-by-side comparison. |

---

## 4. Multi-Agent Audit Rules & Standards

The four specialist analyst agents enforce strict institutional governance:

1. **Fees & Expense Auditor:**
   - Evaluates weighted Total Expense Ratio (TER).
   - Fiduciary standard passes if blended TER $\le 0.15\%$ (15 bps).
   - Flags individual funds exceeding 20 bps.
2. **Diversification & Breadth Auditor:**
   - Computes Herfindahl-Hirschman Index: $\text{HHI} = \sum w_i^2$.
   - Effective holding count: $N_{\text{eff}} = 1 / \text{HHI}$.
   - Requires $\text{HHI} < 0.40$ and exposure across at least 2 distinct asset classes.
3. **Mandate Alignment Auditor:**
   - Verifies equity sleeve matches the objective risk score.
   - Enforces a minimum 10% cash/T-Bill liquidity buffer if no emergency fund exists.
4. **Quantitative Performance Auditor:**
   - Aligns 2-year daily adjusted close prices for portfolio ETFs vs. benchmark (SPY, ACWI, VT, QQQ, BND).
   - Computes CAGR, Annualized Volatility, Sharpe Ratio ($R_f = 4.0\%$), Maximum Drawdown, Jensen's Alpha, and Beta.

---

## 5. Quickstart & Cold-Run Guide

### Run Interactive Web Application (Recommended)
```powershell
cd C:\Users\dolan\Code\school\Fall-2026\FIN-43900\workspace
streamlit run labs/lab-21-robo-advisor/app.py
```

### Run Terminal CLI Questionnaire (Video Reproduction)
```powershell
cd C:\Users\dolan\Code\school\Fall-2026\FIN-43900\workspace
python labs/lab-21-robo-advisor/cli.py
```

### Run Automated Pytest Suite
```powershell
cd C:\Users\dolan\Code\school\Fall-2026\FIN-43900\workspace
python -m pytest labs/lab-21-robo-advisor/tests/test_robo_advisor.py -v
```

---

## 6. Test Suite Verification Results

```
============================= test session starts =============================
platform win32 -- Python 3.13.14, pytest-9.0.2, pluggy-1.6.0
collected 9 items

labs/lab-21-robo-advisor/tests/test_robo_advisor.py::test_preference_model_validation PASSED [ 11%]
labs/lab-21-robo-advisor/tests/test_robo_advisor.py::test_risk_score_monotonicity PASSED     [ 22%]
labs/lab-21-robo-advisor/tests/test_robo_advisor.py::test_strategy_asset_allocation_sum PASSED [ 33%]
labs/lab-21-robo-advisor/tests/test_robo_advisor.py::test_portfolio_holdings_integrity PASSED  [ 44%]
labs/lab-21-robo-advisor/tests/test_robo_advisor.py::test_fees_agent_audit PASSED            [ 55%]
labs/lab-21-robo-advisor/tests/test_robo_advisor.py::test_diversification_agent_audit PASSED [ 66%]
labs/lab-21-robo-advisor/tests/test_robo_advisor.py::test_storage_persistence PASSED         [ 77%]
labs/lab-21-robo-advisor/tests/test_robo_advisor.py::test_mpt_optimizer PASSED               [ 88%]
labs/lab-21-robo-advisor/tests/test_robo_advisor.py::test_full_pipeline_run PASSED           [100%]

============================== 9 passed in 1.96s ==============================
```
