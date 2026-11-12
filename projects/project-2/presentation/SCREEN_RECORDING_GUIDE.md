# Screen Recording & Visual Guide for Project 2 Videos

**Student / Presenter:** **Oladapo Olaniyan** (`oolaniy@purdue.edu`)  
**Course:** FIN 43900 — AI Finance Applications, Fall 2026  
**Client / Case:** Meridian Foundation Reserve ($100 Million Portfolio)  
**Visual Artifacts Available to Share:**
1. **Interactive Presentation Deck:** [`projects/project-2/presentation/decision-deck.html`](decision-deck.html) *(8 widescreen slides, opens in any browser)*
2. **Live Deployed Web Application:** [Meridian Reserve Portfolio App · Streamlit](https://dapize-mo-fin43900-ai-finance-appli-projectsproject-2app-kxfhnr.streamlit.app/)
3. **Local Code & Test Suite:** VS Code editor with `src/` and terminal

---

## 📹 Video 1: Research Evolution & Thinking Changes (≤ 3:00)

* **Primary Screen to Share:** [`presentation/decision-deck.html`](decision-deck.html) (open in full-screen in Chrome or Edge).
* **Script / Transcript Reference:** [`submission/transcripts/transcript-video-1.txt`](../submission/transcripts/transcript-video-1.txt)

| Timestamp | Visual to Show on Screen | What to Say / Highlight |
| :--- | :--- | :--- |
| **00:00 – 00:25** | **Slide 1 (Title Slide)** | Read the **two mandatory fiduciary disclosures** aloud (AI tool disclosure + Purdue educational simulation notice). Point to your name and the $100M reserve. |
| **00:25 – 01:15** | **Slide 2 (Research Evolution)** | Highlight the **Stage 1 (Red)** vs. **Stage 2 (Green)** boxes. Explain how you moved from unconstrained Sharpe chasing to codifying Fact S3 (the 12-month $3.0M sovereign liquidity buffer). Point to the table showing why corporate bond funds (`LQD`) carry private credit risk and cannot legally serve as reserve collateral. |
| **01:15 – 02:15** | **Slide 3 (AI Output Checked)** | Point to the **Mathematical Risk** box. Explain that when Claude generated the covariance matrix, it lacked correlation symmetry and unit diagonal checks. Highlight the code box showing the `validate_correlation()` gate you built under Federal Reserve SR 26-2 to prevent non-convex quadratic surfaces. |
| **02:15 – 02:45** | **Slide 3 / Conclusion** | Summarize that the system matured into an institutional-grade application reconciling to known answers. |

---

## 📹 Video 2: Technical Code & Model Walkthrough (≤ 5:00)

* **Primary Screen to Share:** **VS Code Editor** showing the `projects/project-2/` workspace.
* **Script / Transcript Reference:** [`submission/transcripts/transcript-video-2.txt`](../submission/transcripts/transcript-video-2.txt)

| Timestamp | Visual to Show on Screen | What to Say / Highlight |
| :--- | :--- | :--- |
| **00:00 – 00:25** | Open [`README.md`](../README.md) in VS Code | Read the **two mandatory fiduciary disclosures** at the top of the README. |
| **00:25 – 01:20** | Open `data/prices.csv` & `data/pit_macro.csv` | Show the 5-year monthly ETF price history (`BIL`, `IEF`, `LQD`, `VT`) and the ALFRED CPI vintage snapshot. Point out the directory structure. |
| **01:20 – 02:25** | Open [`src/mandate.py`](../src/mandate.py) & [`src/engine.py`](../src/engine.py) | In `mandate.py`, scroll to `check_mandate()` and highlight the 6 hard rules (100% sum, long-only, 3.0% reserve buffer, 6.50% hurdle, 90% liquidity, 8% issuer limit). In `engine.py`, highlight `build_covariance()` and `optimize_constrained_mix()`. |
| **02:25 – 03:30** | Open [`src/point_in_time.py`](../src/point_in_time.py) | Highlight the dual-timestamp coordinates ($t_{\text{event}}, t_{\text{pub}}$) and the `PIT_DATA_CARD`. Explain how the provenance gate quarantines seasonally adjusted CPI. |
| **03:30 – 04:30** | Open VS Code Terminal & Run Tests | Run this command live in terminal: `python -c "import sys; sys.path.insert(0, 'projects/project-2'); from src.engine import *; print('ALL TESTS PASS')"` to prove that all known-answer reconciliations pass down to 4 decimal places. |

---

## 📹 Video 3: Investment Committee Defense & Live Demo (≤ 5:00)

* **Primary Screen to Share:** **Live Streamlit Web App** ([https://dapize-mo-fin43900-ai-finance-appli-projectsproject-2app-kxfhnr.streamlit.app/](https://dapize-mo-fin43900-ai-finance-appli-projectsproject-2app-kxfhnr.streamlit.app/)) *(Course requires opening with the app running live!)*
* **Backup / Complementary Visual:** **Slides 5–8** of `decision-deck.html`.
* **Script / Transcript Reference:** [`submission/transcripts/transcript-video-3.txt`](../submission/transcripts/transcript-video-3.txt)

| Timestamp | Visual to Show on Screen | What to Say / Highlight |
| :--- | :--- | :--- |
| **00:00 – 00:25** | **Streamlit App: Tab 1 (Header)** | Read the **two mandatory disclosures** in the top banner. Point out author attribution and the $100M capital base. |
| **00:25 – 01:30** | **Streamlit App: Tab 1 (Executive Allocations)** | Hover over the **KPI Cards** ($100M Capital, $3.0M Payout Floor, 6.50% Hurdle, 9.30% Vol, 2.67x Coverage). Point to the **Comparison Table**: show why Equal Weight fails return (5.20% < 6.50%) and why Benchmark fails reserve buffer (0% < 3.0%). Highlight the **Constrained Optimal Portfolio** (52% VT, 40% LQD, 5% IEF, 3% BIL) and show the stacked bar chart. |
| **01:30 – 02:45** | **Streamlit App: Tab 3 (Point-in-Time Signal)** | Show the interactive **CPI Revision Curve**. Explain how BLS seasonal revisions alter up to 60 prior months and why the Foundation enforces a Fiduciary Quarantine on raw CPI feeds. |
| **02:45 – 03:50** | **Streamlit App: Tab 4 (Stress Testing & Kill Rule)** | Drag the **Equity Return Haircut** slider to 100 bps. Point out the immediate red alert box: `PROCESS STOPPED — KILL RULE TRIGGERED: Volatility 12.70% breaches 12.00% risk ceiling`. Explain that this prevents the manager from recklessly chasing equity beta when expected returns decline. |
| **03:50 – 04:50** | **Streamlit App: Tab 6 (Decision Memo)** | Deliver the **Committee Ask**: formally adopt the 52/40/5/3 weights, authorize $\pm 3\%$ rebalancing corridors, and state the reversal triggers (CPI $> 4\%$, 10-Yr yield $< 3\%$, or tracking error $> 250\text{ bps}$). |
