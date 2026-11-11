# FIN 43900 — Project 2: Investment Management Application

**Author / Student Analyst:** **Oladapo Olaniyan** (`oolaniy@purdue.edu`)  
**Institution:** Mitchell E. Daniels, Jr. School of Business, Purdue University  
**Course:** FIN 43900 — AI Finance Applications, Fall 2026  
**Client / Case:** Meridian Foundation Reserve ($100 Million Portfolio)  
**Governing Standard:** Federal Reserve SR 26-2 Model Risk Management  

---

## 🏛️ Mandatory Fiduciary & AI Disclosures (Base Requirement 8)

> **1. AI Tool Disclosure:** Anthropic Claude (Claude 3.5 Sonnet / Claude Opus 5.5) and Google Antigravity were utilized in designing analytical scripts, unit testing architecture, visualization ergonomics, and formatting optimization. All mathematical derivations, input validations, fiduciary constraints, and investment decisions were directed, verified, and finalized independently by the student analyst.  
> **2. Ownership & Academic Notice:** The analysis, models, interpretations, and committee recommendations presented herein are solely the author's work; this application is an educational simulation developed for academic demonstration in FIN 43900 at Purdue University, not personalized investment advice.

---

## 🚀 Quickstart: Single-Command Cold Run (Base Requirement 1)

- **Live Deployed App (Streamlit Community Cloud):** [Meridian Reserve Portfolio App](https://dapize-mo-fin43900-ai-finance-appli-projectsproject-2app-kxfhnr.streamlit.app/)

A reviewer or stranger can clone this repository, install requirements, and launch the web app with no prior setup or coaching:

```bash
# 1. Navigate to Project 2 directory
cd projects/project-2

# 2. Install dependencies (standard Python environment)
pip install -r requirements.txt

# 3. Launch the Streamlit application
streamlit run app.py
```

*The application automatically loads local price history (`data/prices.csv`) and point-in-time inflation datasets (`data/pit_macro.csv`), requiring no external API keys or credentials to operate.*

---

## 📊 Project 2 Base Requirements Verification Map

| Requirement | Implementation in Repository | Key Fiduciary Output / Metric |
| :--- | :--- | :--- |
| **1. The App Runs** | [`app.py`](app.py) via Streamlit | Standalone multi-tab institutional dashboard runnable cold |
| **2. Mandate** | [`src/mandate.py`](src/mandate.py) | $100M reserve, 3.0% reserve-eligible buffer floor, 6.50% net hurdle |
| **3. Two Baselines & Portfolio** | `app.py` (Tab 1 & 2) & [`src/engine.py`](src/engine.py) | **Equal Weight** (Fails Return), **Benchmark** (Fails Buffer), **Constrained Optimal** (PASSES ALL) |
| **4. Point-in-Time Signal** | [`src/point_in_time.py`](src/point_in_time.py) & `data/pit_macro.csv` | ALFRED CPI vintage audit proving 60-month historical revisions + Data Card |
| **5. Stress Run & Kill Condition** | `app.py` (Tab 4) & [`src/engine.py`](src/engine.py) | Return shocks, credit spread widening, and volatility stop rule (> 12.00%) |
| **6. Locked Changed-Input Record** | [`docs/validation-and-ai-use.md`](docs/validation-and-ai-use.md) | Pre-run AI-off prediction on equity return haircut (-100 bps) committed to Git |
| **7. Final Recommendation** | [`docs/decision-memo.md`](docs/decision-memo.md) | Fiduciary recommendation to allocate to Constrained Optimal Portfolio |
| **8. Two Opening Statements** | README, Memo, and all 3 video transcripts | Disclosures prominent at the head of every deliverable |

---

## 📂 Repository Structure

```
projects/project-2/
├── README.md                      # Single-command run guide & base requirement map
├── requirements.txt              # Standard Python dependencies (streamlit, pandas, etc.)
├── app.py                         # Standalone interactive Streamlit fiduciary web app
├── src/
│   ├── __init__.py
│   ├── engine.py                  # Covariance math, grid search optimization, stress testing
│   ├── mandate.py                 # Algorithmic compliance checks across Meridian covenants
│   └── point_in_time.py           # Dual-timestamp ALFRED signal engine & Data Card
├── data/
│   ├── prices.csv                 # 5-Year historical monthly prices for BIL, IEF, LQD, VT
│   └── pit_macro.csv              # ALFRED vintage audit data proving seasonal restatements
├── docs/
│   ├── decision-memo.md           # Formal Investment Committee Decision Memorandum
│   └── validation-and-ai-use.md   # Model risk audit (SR 26-2) & Locked Changed-Input Record
└── submission/
    ├── manifest.md                # Submission manifest linking every GitHub artifact
    └── transcripts/
        ├── transcript-video-1.txt # Research evolution & verified AI output transcript
        ├── transcript-video-2.txt # Technical code and test walkthrough transcript
        └── transcript-video-3.txt # Investment Committee presentation & live demo transcript
```

---

## 📈 Summary of Fiduciary Findings

1. **Benchmark Covenant Breach:** The Meridian Foundation's policy benchmark (60% Global Equity `VT` / 40% IG Corporate Bonds `LQD`) holds **zero sovereign liquidity**, breaching the legal requirement to hold 12 months of quarterly spending ($3.0M / 3.0%) in U.S. Treasury bills or notes.
2. **Equal Weight Return Drag:** The transparent Equal Weight baseline ($25\%$ per sleeve) holds ample liquidity ($50\%$), but generates only **5.20% net return**, falling 130 bps short of the CPI + 4.0% (**6.50%**) purchasing power hurdle.
3. **The Constrained Solution:** The Constrained Optimal Portfolio allocates **52% VT, 40% LQD, 5% IEF, and 3% BIL**, achieving:
   - **Net Return:** 6.50% (exactly meeting the hurdle net of costs)
   - **Annualized Volatility:** 9.30% (a 116 bps risk reduction vs. benchmark's 10.46%)
   - **Reserve Buffer:** 8.0% ($8.0M; a 2.67x coverage ratio over the required 12-month spending floor)
   - **Mandate Verdict:** **100% PASS** on all legal and investment constraints.

