================================================================================
FIN 43900 LAB 21 (WEEK 14 STUDIO) CHECKOUT — BRIGHTSPACE SUBMISSION
Student Name: Oladapo Olaniyan
Email: oolaniy@purdue.edu
Course: FIN 43900 — AI Finance Applications, Daniels School of Business, Purdue University
Session: Week 14 Studio Lab (Tuesday, November 24 Practice Session)
Lab Date: 11/24/2026
Topic: AI Robo Advisor Implementation & Enhancement
Tutorial Video: https://youtu.be/Bm0qwSymvX8 (Dr. Z: Build based on existing repo)
Base Open-Source Repository: matvix90/ai-robo-advisor
Session Token: RoboAdvisorPractice
================================================================================

FIELD 1: LAB DATE & SESSION METADATA
- Lab Date: 11/24/2026 (November 24, 2026)
- Session: Week 14 Applied Decision-System Studio (Tuesday Practice Session — No in-person meeting)
- Session Token: RoboAdvisorPractice
- Course: FIN 43900 — AI Finance Applications, Daniels School of Business, Purdue University
- Student Name: Oladapo Olaniyan
- Email: oolaniy@purdue.edu
- Target Implementation: AI Robo Advisor Multi-Agent Decision System
- Tutorial Reference: Dr. Z YouTube Walkthrough (https://youtu.be/Bm0qwSymvX8)
- Base Open-Source Repository: https://github.com/matvix90/ai-robo-advisor
- Local Workspace Directory: labs/lab-21-robo-advisor/
- GitHub Directory: https://github.com/Dapize-Mo/FIN43900-AI-Finance-Applications/tree/main/labs/lab-21-robo-advisor

FIELD 2: TEAMMATES, COLLABORATION & PERSONAL CONTRIBUTION
- Teammates / Learning Partners: Independent Thanksgiving week studio practice assigned by Dr. Z.
- Personal Contribution: Independently authored the entire AI Robo Advisor decision system package:
  * Extracted and analyzed the 50-minute tutorial video transcript and identified core pain points (Polygon API rate limits, lack of session persistence, clunky CLI);
  * Implemented the four-stage multi-agent architecture in models.py and robo_engine.py (Investment Agent, Strategy Formulation Agent, ETF Portfolio Construction Agent, Analyst Agents, and Orchestrator);
  * Developed the dual-source market data engine (data_engine.py) utilizing keyless yfinance with local file caching and graceful Polygon fallback;
  * Designed state persistence and progress auto-recovery (storage.py);
  * Built the interactive Streamlit web dashboard (app.py) with Plotly allocation donut charts, cumulative return backtests, KPI scorecards, and decision memo export;
  * Completed the optional task by building a Markowitz MPT Modern Portfolio Theory quantitative optimization engine (MPTQuantitativeEngine) for side-by-side comparison;
  * Authored and verified the 9-test pytest suite (tests/test_robo_advisor.py) with 100% passing results.

FIELD 3: CORE QUESTION & DECISION DEFINITION
- Core Question: How can an open-source AI robo-advisor (matvix90/ai-robo-advisor) be replicated, made robust against market data API failures, and upgraded into an interactive institutional decision platform?
- Decision Answer: By replacing brittle paid data endpoints with a keyless multi-asset market data engine (yfinance), implementing persistent session caching so users never lose progress, embedding four specialist fiduciary auditor agents (Fees, Diversification, Alignment, Performance), and providing a side-by-side quantitative Markowitz Efficient Frontier comparison in an interactive Streamlit UI.

FIELD 4: ROBOT ADVISOR IMPLEMENTATION SUMMARY & TUTORIAL CONCORDANCE
- The application faithfully reproduces the multi-agent orchestration demonstrated in Dr. Z's tutorial:
  1. Questionnaire Agent: Captures 15 investor parameters across risk profile, time horizon, emergency reserves, market downturn reaction, and capital constraints.
  2. Risk Scoring Engine: Calculates an objective composite score (1-100) combining psychological tolerance, time horizon, and loss capacity.
  3. Strategy Formulation Agent: Determines macroeconomic asset allocation across Equities, Fixed Income, Real Estate, and Cash equivalents.
  4. ETF Construction Agent: Selects ultra-low-cost, highly liquid institutional ETFs (VTI, VXUS, BND, IEF, VNQ, BIL) summing to exact 100% weight.
  5. Multi-Agent Audit:
     - Fees Agent: Audits weighted TER against the 0.15% (15 bps) fiduciary threshold.
     - Diversification Agent: Calculates Herfindahl-Hirschman Index (HHI) and effective holding counts.
     - Alignment Agent: Audits equity risk and emergency cash buffers against user constraints.
     - Performance Agent: Computes historical 2-year daily CAGR, Volatility, Sharpe Ratio, Max Drawdown, Alpha, and Beta vs benchmark.
  6. Fiduciary Orchestrator: Issues overall disposition (APPROVED vs. REVISION_REQUIRED).

FIELD 5: CODEX ENHANCEMENTS OVER BASE OPEN-SOURCE REPO
1. Keyless Dual-Source Market Data: Replaced the Polygon.io 5-call/min rate-limited dependency (which crashed during Dr. Z's video) with a robust yfinance engine with local JSON caching, zero API cost, and no 429 rate limit exceptions.
2. State Persistence & Auto-Recovery: Implemented save_profile() and load_profile() to ensure questionnaire progress is preserved across runs, directly resolving Dr. Z's recommendation at minute 42:25.
3. Interactive Streamlit Web UI: Upgraded from terminal prompts to a modern multi-tab web dashboard featuring interactive sliders, Plotly visualizations, live backtest curves, and downloadable Markdown decision memos.
4. Deterministic Modern Portfolio Theory Heuristics: Added capital market assumptions and algorithmic MPT fallback so the system functions reliably even without active LLM API credits.

FIELD 6: OPTIONAL OPEN-SOURCE COMPARISON: MARKOWITZ MPT OPTIMIZER
- Completed the optional task: "Find another open-source GitHub repo and make a new version of yours."
- Comparative Architecture: Integrated classical Markowitz Modern Portfolio Theory (MPT) Mean-Variance Optimization (scipy.optimize SLSQP) alongside the AI Multi-Agent portfolio:
  * Minimum Volatility Portfolio: Mathematically minimizes portfolio variance subject to asset bounds [2%, 70%] and sum(w) = 1.0.
  * Maximum Sharpe Ratio Portfolio: Maximizes risk-adjusted excess return over risk-free rate (4.0%).
  * Key Insight: The AI Multi-Agent portfolio balances mathematical efficiency with behavioral mandate alignment (e.g. maintaining explicit cash liquidity buffers and international diversification) that raw unconstrained quadratic optimizers often ignore.

FIELD 7: TEST VERIFICATION RESULTS
- Pytest Command: python -m pytest labs/lab-21-robo-advisor/tests/test_robo_advisor.py -v
- Result: 9 PASSED in 1.96s (100% pass rate across questionnaire validation, risk scoring monotonicity, strategy allocation sums, ETF holdings integrity, fee audits, diversification audits, storage persistence, MPT optimization, and full pipeline execution).

FIELD 8: COLD-RUN COMMANDS
- Run Interactive Web UI: streamlit run labs/lab-21-robo-advisor/app.py
- Run Terminal CLI: python labs/lab-21-robo-advisor/cli.py
- Run Test Suite: python -m pytest labs/lab-21-robo-advisor/tests/test_robo_advisor.py -v
================================================================================
