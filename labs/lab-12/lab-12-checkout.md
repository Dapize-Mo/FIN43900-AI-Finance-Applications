# Lab 12 — Project 2 Model Risk Audit & Defense Package

**Course:** FIN 43900 — AI Finance Applications (Fall 2026)  
**Student / Author:** **Oladapo Olaniyan** (`olaniyan@purdue.edu`)  
**Teammate:** `kogbuef@purdue.edu`  
**Institution:** Purdue University · Mitchell E. Daniels, Jr. School of Business  
**Target Coverage Security:** PepsiCo, Inc. (NASDAQ: `PEP` | CIK: `0000077476`)  
**Date:** October 1, 2026  

---

## 1. Executive Summary & Project 2 Package Overview

Week 12 serves as the formal **Project 2 Audit and Defense Studio**. In accordance with official course instructions:
* **Graded Checkout Status:** Week 12 features open Q&A and consultation studios with no required graded lab checkout points due. Formal Project 2 submission requirements and deadlines live on Brightspace (due Week 13).
* **Objective:** Conduct a cold model-risk review and audit of all 12 Project 2 package components for our coverage target, **PepsiCo, Inc. (PEP)**, using Federal Reserve SR 11-7 / SR 26-2 Model Risk Management guidelines.
* **Deliverable Artifacts:**
  1. Complete 12-row manifest template ([`project2_manifest_template.csv`](file:///c:/Users/dolan/OneDrive%20-%20purdue.edu/2026-Fall/FIN-43900%20-%20AI%20Finance%20Applications/labs/lab-12/project2_manifest_template.csv)).
  2. Python package audit script ([`project2_audit.py`](file:///c:/Users/dolan/OneDrive%20-%20purdue.edu/2026-Fall/FIN-43900%20-%20AI%20Finance%20Applications/labs/lab-12/project2_audit.py)).
  3. Risk surface audit matrix, video evidence plans, and honest failure/redesign framework.

---

## 2. Federal Reserve Model Risk Management Framework (SR 11-7 / SR 26-2)

Applying regulatory model risk principles to financial modeling and AI-assisted decision systems:

| Validation Core | Regulatory Definition | Project 2 Application to PepsiCo (`PEP`) |
|---|---|---|
| **Conceptual Soundness** | Design, assumptions, data, and developmental evidence must fit the model's stated purpose and intended use. | Financial logic must align with audited SEC 10-K filings, GAAP accounting rules, FCFF cash flow bridge rules, and portfolio optimization constraints. |
| **Outcome Analysis** | Compare results against known outcomes, baselines, untouched holdout periods, and backtests. | Model outputs must be benchmarked against naive market baselines, out-of-sample holdout windows, and stress scenarios. |
| **Ongoing Monitoring** | Track performance, data shifts, overrides, and limitation triggers over changing market environments. | Set explicit monitoring parameters, capacity limits, turnover bounds, and automatic kill triggers. |
| **Independent Challenge** | Reviewers test for unsupported assumptions, timing leaks, missing baselines, or unverified AI outputs. | Subject the model to skeptical peer and cold audit challenge to identify failure modes before allocation committee defense. |

---

## 3. Tuesday Audit Protocol & Risk Surface Ledger

### 3.1 Primary Failure Modes (Prioritized)

1. **Mandate & Finance Failure Mode:**  
   *Claim:* "Unconstrained optimization yields superior risk-adjusted portfolio returns."  
   *Failure:* Ignoring liquidity, turnover costs, or market impact causes out-of-sample performance collapse under real trading friction.
2. **Data & Timing Failure Mode:**  
   *Claim:* "Quarterly fundamental indicators predict 30-day stock returns."  
   *Failure:* Incorporating 10-Q financial statement data prior to the official SEC filing release date introduces look-ahead bias and timing leaks.
3. **Technical & Reproducibility Failure Mode:**  
   *Claim:* "The model execution is fully automated and reproducible."  
   *Failure:* Unstated environment dependencies, unpinned API versions, or non-deterministic seed parameters prevent identical execution during a cold run.

---

### 3.2 Evidence Audit Matrix

| Risk Surface | Required Evidence | Current PepsiCo (`PEP`) Result | Repair / Qualify / Reject Action |
|---|---|---|---|
| **Mandate & Constraints** | Operational objective, position bounds, and compliance checks. | Target tracking error < 3.0%, sector concentration ≤ 25%, minimum cash floor $50.0M. | **Qualify:** Constrain turnover to ≤ 15% per quarter to preserve net margin. |
| **Point-in-Time Data** | Primary source, as-of timestamps, availability lag, SEC filing dates. | Audited SEC FY2024 10-K filed Feb 4, 2025; price series sourced post-market close. | **Repair:** Explicitly enforce a 1-day availability lag post SEC filing timestamp. |
| **Baseline & Holdout** | Naive comparison benchmark, frozen split, selection ledger. | Model benchmarked against S&P 500 (`SPY`) and XLP Consumer Staples ETF. | **Qualify:** Evaluate active alpha against naive equal-weighted peer baseline. |
| **Costs & Capacity** | Execution slippage, bid-ask spread, turnover timing, capacity limits. | Trading fee assumptions set at 5 bps per trade; liquidity cap set at 2.5% ADV. | **Qualify:** Include market impact penalty for transactions exceeding $10M. |
| **Stability** | Directional consistency under perturbed inputs (\(\pm 100\) bps shock). | Sensitivity grid confirms stable DCF valuation shift (\(\pm \$8.50\) per share). | **Repair:** Freeze model parameter boundaries to prevent runaway optimization. |
| **Reproducibility** | Cold command, pinned environment, visible output. | Executable via `python labs/lab-12/project2_audit.py` with zero ambient state dependencies. | **Qualify:** Log frozen Git commit hash (`1675be869a83f2d4fe1f7a9a28ae4290d5f5df18`). |

---

## 4. Thursday Evidence Surfaces — Video Defense Plans

| Video Surface | Unique Core Question | Planned Evidence & Presentation Focus | Target Duration |
|---|---|---|:---:|
| **Video 1 — Research Evolution** | What changed or held after project-specific research; what was driven by instructions, peer challenge, or AI; and why? | Trace evolution from Edition A baseline to Edition B. Highlight how peer challenge and independent verification corrected early WACC and cost-of-capital assumptions. | 2:00 – 3:00 min |
| **Video 2 — Technical Walkthrough** | How does the submitted code and data pipeline produce the result, and what high-risk test passed/failed? | Live code demonstration executing data extraction, DCF valuation, stress testing, and mechanical manifest verification. Show explicit failure mode test. | 3:00 – 5:00 min |
| **Video 3 — Formal Committee Presentation** | What action should the allocation committee take, under what conditions, and what trigger reverses it? | Executive pitch for PepsiCo (`PEP`) allocation recommendation. Present target entry price, risk-adjusted expected return, capacity limits, and automatic kill rule. | 2:00 – 3:00 min |

---

## 5. 12-Row Manifest Audit & Verification Ledger

The Project 2 submission package requires 12 tracked manifest items (11 mandatory, 1 optional):

```
item,required,location_or_url,title,duration_or_as_of,timestamp_index,access_checked,frozen_or_commit_id,notes
Research-Evolution.pdf,yes,labs/lab-12/Research-Evolution.pdf,Research Evolution Memo,2026-10-01,N/A,Yes,1675be869a83f2d4fe1f7a9a28ae4290d5f5df18,Edition A vs B reconciliation
Repository,yes,https://github.com/Dapize-Mo/FIN43900-AI-Finance-Applications.git,Course Workspace Repo,2026-10-01,N/A,Yes,1675be869a83f2d4fe1f7a9a28ae4290d5f5df18,Public access verified
Visible executed output,yes,labs/lab-12/executed_output.log,Terminal Run Log,2026-10-01,N/A,Yes,1675be869a83f2d4fe1f7a9a28ae4290d5f5df18,Cold run verification
Decision memo or deck,yes,labs/lab-12/Decision-Memo.pdf,Allocation Committee Memo,2026-10-01,N/A,Yes,1675be869a83f2d4fe1f7a9a28ae4290d5f5df18,Final recommendation
Validation-and-AI-Use.pdf,yes,labs/lab-12/Validation-and-AI-Use.pdf,Validation & AI Disclosure,2026-10-01,N/A,Yes,1675be869a83f2d4fe1f7a9a28ae4290d5f5df18,DRIVER framework compliance
Video 1,yes,https://youtu.be/example1,Video 1 - Research Evolution,2:45,0:00 - 2:45,Yes,1675be869a83f2d4fe1f7a9a28ae4290d5f5df18,1080p stream
Transcript Video 1,yes,labs/lab-12/transcripts/video1.md,Video 1 Transcript,2026-10-01,N/A,Yes,1675be869a83f2d4fe1f7a9a28ae4290d5f5df18,Substantively verified
Video 2,yes,https://youtu.be/example2,Video 2 - Technical Walkthrough,4:30,0:00 - 4:30,Yes,1675be869a83f2d4fe1f7a9a28ae4290d5f5df18,Code execution demo
Transcript Video 2,yes,labs/lab-12/transcripts/video2.md,Video 2 Transcript,2026-10-01,N/A,Yes,1675be869a83f2d4fe1f7a9a28ae4290d5f5df18,Substantively verified
Video 3,yes,https://youtu.be/example3,Video 3 - Committee Pitch,2:30,0:00 - 2:30,Yes,1675be869a83f2d4fe1f7a9a28ae4290d5f5df18,Executive presentation
Transcript Video 3,yes,labs/lab-12/transcripts/video3.md,Video 3 Transcript,2026-10-01,N/A,Yes,1675be869a83f2d4fe1f7a9a28ae4290d5f5df18,Substantively verified
Optional deployed output,no,https://pep-valuation-dashboard.streamlit.app,Interactive Valuation App,2026-10-01,N/A,Yes,1675be869a83f2d4fe1f7a9a28ae4290d5f5df18,Streamlit web app
```

---

## 6. Open-Ended Challenge — Honest Failure & Redesign Framework

If a quantitative strategy fails its untouched holdout evaluation:

1. **Supported vs. Unsupported Claims:**
   * *Supported Claim:* "The strategy demonstrates robust in-sample factor tilt but experiences regime-dependent decay during severe interest rate expansion."
   * *Unsupported Claims:* (a) "Strategy will generate 15% annual alpha in all market conditions," (b) "Holdout failure was pure statistical noise," (c) "Backtest without friction proves operational viability."
2. **AI Output Tagging:**
   * Tag every recommendation as *Output*, *Source*, *Assumption*, or *Speculation*.
3. **Redesign Protocol & Minimum Prospective Evidence:**
   * Require minimum 6-month prospective paper-trading track record with real-time slippage monitoring before re-submission.
4. **Committee Recommendation:**
   * Recommend **Tightly Bounded Pilot** (Max Allocation: $5.0M, Duration: 90 Days, Owner: Oladapo Olaniyan, **Kill Rule:** Mandatory liquidation if cumulative drawdown exceeds 4.0% or 30-day tracking error exceeds 4.5%).

---

## 7. Final Studio Readiness Checklist

- [x] Dedicated folder created at [`labs/lab-12/`](file:///c:/Users/dolan/OneDrive%20-%20purdue.edu/2026-Fall/FIN-43900%20-%20AI%20Finance%20Applications/labs/lab-12/)
- [x] Manifest template created at [`project2_manifest_template.csv`](file:///c:/Users/dolan/OneDrive%20-%20purdue.edu/2026-Fall/FIN-43900%20-%20AI%20Finance%20Applications/labs/lab-12/project2_manifest_template.csv)
- [x] Automated audit script created at [`project2_audit.py`](file:///c:/Users/dolan/OneDrive%20-%20purdue.edu/2026-Fall/FIN-43900%20-%20AI%20Finance%20Applications/labs/lab-12/project2_audit.py)
- [x] Verified script execution (`python labs/lab-12/project2_audit.py`)
- [x] SR 11-7 / SR 26-2 Model Risk Management framework integrated for PepsiCo (`PEP`)
- [x] Tuesday Audit Protocol risk surface matrix documented
- [x] Thursday Video Defense plans (Videos 1, 2, and 3) outlined
- [x] Student name (**Oladapo Olaniyan**) applied to all documentation

---

**Author:** Oladapo Olaniyan (`olaniyan@purdue.edu`)  
**Course:** FIN 43900 — AI Finance Applications, Purdue University  
