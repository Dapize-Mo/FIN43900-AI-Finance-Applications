# Lab 20 Checkout — Project 2 Readiness

**Course:** FIN 43900 — AI Finance Applications, Fall 2026  
**Student / Author:** **Oladapo Olaniyan** (`oolaniy@purdue.edu`)  
**Institution:** Mitchell E. Daniels, Jr. School of Business, Purdue University  
**Case / Mandate:** Meridian Foundation Reserve ($100 Million Portfolio)  
**Target Coverage Security:** PepsiCo, Inc. (`PEP`)  
**Top Fund Holding Security:** Apple Inc. (`AAPL`) / Vanguard Total World Stock ETF (`VT`)  
**Date:** November 17, 2026  
**Category:** Tuesday Completion Checkout (25 Points) — *The 20th and Final Lab Checkout of FIN 43900*  
**Session Token:** `readiness` *(or live in-class verification word)*  
**Live Deployed App (Streamlit Community Cloud):** [Meridian Reserve Portfolio App · Streamlit](https://dapize-mo-fin43900-ai-finance-appli-projectsproject-2app-kxfhnr.streamlit.app/)  
**GitHub Repository:** [Dapize-Mo/FIN43900-AI-Finance-Applications](https://github.com/Dapize-Mo/FIN43900-AI-Finance-Applications)  
**Project 2 Directory:** [`projects/project-2/`](../../projects/project-2/)  
**Readiness Audit Script:** [`audit_project2_readiness.py`](audit_project2_readiness.py)  

---

## 📌 Executive Summary & Core Question (D)

> **Core Question (D):**  
> *Could a committee member who has never met you reach your decision from your repository — and does the decision survive one changed input?*

### The Architectural Answer

**Yes.** Through the completion of this readiness audit, we prove that an independent reviewer, trustee, or committee member can clone our repository from GitHub alone, execute the single command documented in the README, interactively inspect all baseline portfolios and the Constrained Optimal Portfolio, and arrive at the exact same fiduciary decision without any prior coaching or undocumented dependencies:

1. **The Code Computes Every Number:** Python modules ([`src/engine.py`](../../projects/project-2/src/engine.py), [`src/mandate.py`](../../projects/project-2/src/mandate.py), [`src/point_in_time.py`](../../projects/project-2/src/point_in_time.py)) calculate portfolio variance, covariance matrices, net returns, and liquidity buffers deterministically from primary price histories ([`data/prices.csv`](../../projects/project-2/data/prices.csv)) and course parameters, achieving 100% test pass on known answers.
2. **The Visible Output Matches the Memorandum Exactly:** Every number presented to the committee in the Decision Memorandum ([`docs/decision-memo.md`](../../projects/project-2/docs/decision-memo.md)) matches the code output and the live interactive Streamlit application to the basis point:
   - **Baseline 1 (Equal Weight 1/N):** 5.20% Net Return | 5.21% Volatility | 50.0% Reserve Buffer $\rightarrow$ **FAIL** (violates 6.50% net return hurdle).
   - **Baseline 2 (Policy Benchmark 60/40):** 6.80% Net Return | 10.46% Volatility | 0.0% Reserve Buffer $\rightarrow$ **FAIL** (violates 3.0% sovereign liquidity covenant).
   - **Constrained Optimal Portfolio:** **6.50% Net Return** | **9.30% Volatility** | **8.0% Reserve Buffer** $\rightarrow$ **PASS** (100% compliant; dominates benchmark by -116 bps risk).
3. **The Decision Survives the Changed Input & Halts Safely:** Subjecting the portfolio engine to a human-predicted -100 bps equity shock (from 8.00% to 7.00%) forces equity weight to 78.0% and drives portfolio volatility to 12.70%, cleanly triggering the quantitative **Process Kill Rule** and halting automated rebalancing.

---

## 🏛️ Rules & Readiness Architecture (R)

In accordance with official course rulings, our repository satisfies every criterion of the stranger test across all six manifest dimensions:

| Manifest Component | Readiness Standard | Exact Repository File & Evidence | Audit Status |
| :--- | :--- | :--- | :---: |
| **1. The Tool** | A teammate moves one control and reads the mandate verdict | [`projects/project-2/app.py`](../../projects/project-2/app.py)<br>[Live Streamlit Cloud Deployment](https://dapize-mo-fin43900-ai-finance-appli-projectsproject-2app-kxfhnr.streamlit.app/) | **PASS** |
| **2. Repository & Run Guide** | A README with the one command that produces the visible result | [`projects/project-2/README.md`](../../projects/project-2/README.md)<br>`cd projects/project-2; streamlit run app.py` | **PASS** |
| **3. Visible Output on GitHub** | Decision numbers readable on GitHub without running anything | [`projects/project-2/README.md`](../../projects/project-2/README.md) & [`projects/project-2/submission/manifest.md`](../../projects/project-2/submission/manifest.md) | **PASS** |
| **4. Decision Memo** | Same numbers, dates, and conditions as the engine output | [`projects/project-2/docs/decision-memo.md`](../../projects/project-2/docs/decision-memo.md)<br>Recommends Constrained Optimal Mix (52/40/8/0) | **PASS** |
| **5. Validation & AI Use** | Baselines, mandate check, stress run, and Locked Changed-Input Record | [`projects/project-2/docs/validation-and-ai-use.md`](../../projects/project-2/docs/validation-and-ai-use.md)<br>Aligned with Federal Reserve SR 26-2 | **PASS** |
| **6. Videos 1–3 & Transcripts** | Links work; each video answers its distinct rubric question | [`projects/project-2/submission/transcripts/`](../../projects/project-2/submission/transcripts/)<br>Transcripts 1, 2, and 3 fully documented | **PASS** |

---

## 🤝 The Cold Run by Learning Partner (I)

- **Learning Partner / Reviewer:** **J. Maffei** (`maffeij@purdue.edu`)  
  *Partner Target Security:* Oracle Corp. (`ORCL`) / Meridian Project 2 Repository  
- **Protocol:** Partner was provided with only the GitHub repository link ([`https://github.com/Dapize-Mo/FIN43900-AI-Finance-Applications`](https://github.com/Dapize-Mo/FIN43900-AI-Finance-Applications)) and instructed to clone into an isolated testing directory, open only the Project 2 README, execute commands without verbal coaching or assistance, and record all observations.

### Partner Cold-Run Observation Record

1. **Exact Commands Executed:**
   ```bash
   git clone https://github.com/Dapize-Mo/FIN43900-AI-Finance-Applications.git
   cd FIN43900-AI-Finance-Applications/projects/project-2
   pip install -r requirements.txt
   python tests/test_known_answers.py
   streamlit run app.py
   ```
2. **Elapsed Time to Visible Result:**
   - **3 minutes 30 seconds** from initial terminal `git clone` to browser dashboard rendering live with all KPI metrics and mandate verdicts.
3. **First Failure / Clarification Encountered:**
   - *Observation:* When initially running `python -m pytest tests/` from the repository root instead of changing into `projects/project-2/`, pytest looked for root packages.
   - *Resolution / Guidance:* README already specified `cd projects/project-2` as Step 1. To guarantee bulletproof execution regardless of execution directory, `tests/test_known_answers.py` contains `sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))`. When following the README's explicit `cd projects/project-2`, the cold run executed with **zero errors**.
4. **Where the Result Is:**
   - Terminal test output printed `All tests passed` (5/5 PASSED).
   - Streamlit browser displayed the interactive dashboard:
     * Executive Overview: 5 KPI cards (Total Reserve Fund, Annual Payout Floor, Net Return Hurdle, Optimal Volatility 9.30%, Reserve Coverage).
     * Tab 1: Three-way comparison table proving Equal Weight and Benchmark covenant failures.
     * Tab 2: Granular mandate audit verifying all Fact S1–S10 constraints.
     * Tab 4: Interactive stress test slider confirming Process Kill Rule activation.

---

## 🔬 One Changed Input — Predicted First (V)

In compliance with Base Requirement 6 and the Week 6 verification pattern, the following test was designed, predicted without AI assistance, committed to Git prior to execution, and rerun:

### Locked Changed-Input Record (`LCIR-FIN43900-P2-001`)

```yaml
locked_changed_input_record:
  record_id: "LCIR-FIN43900-P2-001"
  timestamp_committed: "2026-11-10T19:30:00Z"
  human_analyst: "Oladapo Olaniyan"
  input_under_test: "Global Equity Expected Return Estimate (Sleeve: VT / Vanguard Total World Stock)"
  parameter_units: "Basis points / percentage return per annum"
  baseline_value: 0.0800  # 8.00% per annum (800 bps)
  changed_value: 0.0700   # 7.00% per annum (700 bps; -100 bps macro return shock)

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
    stressed_equity_weight: 0.7800   # 78.0% (surged +26.0% from base 52.0%)
    stressed_ig_bond_weight: 0.1400  # 14.0% (collapsed -26.0% from base 40.0%)
    stressed_treasury_weight: 0.0800 # 8.0% (held exactly at reserve floor)
    stressed_net_return: 0.06504     # 6.504% (cleared 6.50% hurdle)
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
```

---

## 💻 Explain the Code (Six Minutes, No AI)

During the six-minute peer review exchange, I opened the core block of [`src/engine.py`](../../projects/project-2/src/engine.py) (lines 138–180) and [`src/mandate.py`](../../projects/project-2/src/mandate.py) (lines 30–75) and walked through the algorithm line by line:

### Code Walkthrough Block
```python
def optimize_constrained_mix(
    sleeves: List[Dict[str, Any]],
    cov: List[List[float]],
    target_return: float = TARGET_RETURN,
    reserve_min: float = RESERVE_BUFFER_FLOOR,
    step_pct: int = 2,
    transaction_cost_bps: float = 0.0,
) -> Optional[Dict[str, Any]]:
    best_weights = None
    min_vol = float("inf")
    cost_drag = transaction_cost_bps / 10_000.0

    for w in generate_weight_grid(len(sleeves), step_pct=step_pct):
        gross_ret = compute_expected_return(w, sleeves)
        net_ret = gross_ret - cost_drag
        if net_ret < target_return - 1e-6:
            continue

        reserve_w = sum(w[i] for i, s in enumerate(sleeves) if s.get("reserve_eligible", False))
        if reserve_w < reserve_min - 1e-6:
            continue

        vol = compute_portfolio_volatility(w, cov)
        if vol < min_vol:
            min_vol = vol
            best_weights = w
    ...
```

### Partner Question & Code Answer
- **Partner's Question:**  
  *"How does your optimizer ensure that corporate bond holdings (`LQD`) are strictly disqualified from satisfying the Foundation's 12-month $3.0M liquidity reserve, and why doesn't corporate yield solve the liquidity buffer?"*
- **Answer from Code:**  
  In [`src/mandate.py`](../../projects/project-2/src/mandate.py) lines 50–57, `LQD` is explicitly defined with `"reserve_eligible": False` because corporate bond funds carry credit spread duration and market liquidation settlement friction, violating Fact S3 of the Meridian charter. In `optimize_constrained_mix` line 164, the reserve buffer is calculated strictly as:
  ```python
  reserve_w = sum(w[i] for i, s in enumerate(sleeves) if s.get("reserve_eligible", False))
  ```
  Only `BIL` and `IEF` have `"reserve_eligible": True`. Even if `LQD` constitutes 40% of the portfolio, `reserve_w` evaluates strictly to `w[0] + w[1]`. In the 60/40 benchmark, `w[0] + w[1] == 0.0%`, triggering an immediate covenant violation. The optimizer selects 8.0% `IEF` (Treasury 10-Year Notes) because its 4.30% yield and duration hedging satisfy the 3.0% floor with minimum return drag.

---

## 🛠️ Fix One Thing (E)

- **Cold-Run Finding:**  
  Partner noticed that while the instructions in `projects/project-2/README.md` clearly specify running from within `projects/project-2`, running test commands or audit scripts from the repository root workspace can encounter module import ambiguity if `sys.path` does not include the project subdirectory.
- **Action Taken & Pushed:**  
  1. Verified that [`src/engine.py`](../../projects/project-2/src/engine.py), [`src/point_in_time.py`](../../projects/project-2/src/point_in_time.py), and [`tests/test_known_answers.py`](../../projects/project-2/tests/test_known_answers.py) utilize explicit relative imports and dynamic `sys.path.insert(0, ...)` anchors.
  2. Built and added [`labs/lab-20/audit_project2_readiness.py`](audit_project2_readiness.py) to provide a single, automated, multi-level verification harness validating all 15 required manifest files, re-running all baseline calculations, verifying the Process Kill Condition, and cross-checking data cards with zero manual overhead.
  3. Partner executed the audit script; cold run completed cleanly with zero warnings or errors.

---

## 🎯 Official Decision Line

**"ALLOCATE TO THE CONSTRAINED OPTIMAL PORTFOLIO (52% VT / 40% LQD / 8% IEF / 0% BIL) delivering 6.50% net return and 8.0% sovereign liquidity at 9.30% annualized volatility; STOP AND SUSPEND OPTIMIZATION if forward equity return expectations fall below 7.00%, which triggers the 12.00% volatility Process Kill Rule."**

---

## 🪞 Reflect

1. **What the cold run found that I could not see:**  
   The cold run revealed how deeply authors take their working environment for granted. When developing an application, one assumes the terminal is already located in `projects/project-2/`, dependencies are pre-installed in `.venv`, and data paths resolve naturally. Having an independent partner execute strictly from the README highlighted that path resilience, explicit working-directory instructions, and zero-configuration local fallbacks (`prices.csv` bundled locally) are essential to prevent a reviewer from stalling before seeing the first chart.
2. **What I will not touch before the deadline (Monday, November 23, 2026):**  
   I will **not touch** the core mathematical optimization algorithm (`src/engine.py`), the governing mandate constraint definitions (`src/mandate.py`), or the verified baseline asset allocations (52% Global Equity / 40% IG Corporate / 8% 10-Yr Treasuries / 0% Cash). The quantitative core is mathematically sound, fully audited against SR 26-2, and proven on known answers. Any pre-deadline work will be strictly limited to rehearsing video recordings and formatting final presentation slides.

---

## 📦 Verified Deliverables & Artifact Index

All deliverables for Lab 20 and Project 2 are permanently versioned on GitHub:

- **Lab 20 Checkout Document:** [`labs/lab-20/checkout.md`](checkout.md)
- **Lab 20 Readiness Audit Script:** [`labs/lab-20/audit_project2_readiness.py`](audit_project2_readiness.py)
- **Lab 20 Brightspace Submission Text:** [`brightspace/lab-20_submission.txt`](../../brightspace/lab-20_submission.txt)
- **Project 2 README & Quickstart:** [`projects/project-2/README.md`](../../projects/project-2/README.md)
- **Investment Committee Decision Memo:** [`projects/project-2/docs/decision-memo.md`](../../projects/project-2/docs/decision-memo.md)
- **Validation & AI Use Record (SR 26-2 & LCIR):** [`projects/project-2/docs/validation-and-ai-use.md`](../../projects/project-2/docs/validation-and-ai-use.md)
- **Streamlit Web Application Source:** [`projects/project-2/app.py`](../../projects/project-2/app.py)
- **Known-Answer Unit Tests:** [`projects/project-2/tests/test_known_answers.py`](../../projects/project-2/tests/test_known_answers.py)
- **Submission Manifest & Video Transcripts:** [`projects/project-2/submission/manifest.md`](../../projects/project-2/submission/manifest.md)
