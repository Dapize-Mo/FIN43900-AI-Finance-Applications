# Lab 18 — Legend Investor as Skill

**Course:** FIN 43900 — AI Finance Applications, Fall 2026  
**Student / Author:** **Oladapo Olaniyan** (`oolaniy@purdue.edu`)  
**Institution:** Mitchell E. Daniels, Jr. School of Business, Purdue University  
**Target Coverage Security:** PepsiCo, Inc. (`PEP`) | **Known Answer Security:** Costco Wholesale Corp. (`COST`) | **Banking Probe:** JPMorgan Chase & Co. (`JPM`)  
**Date:** November 3, 2026  
**Category:** Tuesday Completion Checkout (25 Points)  
**Streamlit App:** `labs/lab-18/app.py`  

---

## 📌 Controlling Instructions & Source Hierarchy

- **Course Instruction:** [Week 11 — Lab 18 Legend Investor as Skill](https://github.com/CinderZhang/FIN43900-Fall2026/blob/main/lessons/week-11/lab-18-legend-investor-as-skill.md)
- **Session Slides:** [Session 18 Slides](https://github.com/CinderZhang/FIN43900-Fall2026/blob/main/lessons/week-11/slides-session-18.md)
- **Student Handout:** [Student Handout — Investors as Skills](https://github.com/CinderZhang/FIN43900-Fall2026/blob/main/lessons/week-11/student-handout.md)
- **Required Prework:** [Week 11 Prework](https://github.com/CinderZhang/FIN43900-Fall2026/blob/main/lessons/week-11/student-prework.md)
- **FAskills Warren Buffett Expert:** [Buffett's Page](https://github.com/CinderZhang/FAskills/blob/main/financial-researcher/experts/warren_buffett.md)
- **SEC EDGAR API Docs:** [SEC EDGAR Application Programming Interfaces](https://www.sec.gov/search-filings/edgar-application-programming-interfaces)

---

## 🚀 Deliverables & Files

1. **Agent Skill Definition (`SKILL.md`):** [`skills/buffett-investor/SKILL.md`](skills/buffett-investor/SKILL.md)  
   Discovered globally at `~/.gemini/config/skills/buffett-investor/SKILL.md` and project-level at `.agents/skills/buffett-investor/SKILL.md`. Configures progressive disclosure frontmatter, SEC EDGAR keyless extraction parameters, 10-K flow filtering rules, Buffett's 3 checks, and memo generation instructions.
2. **Bundled Python Extraction & Audit Script:** [`buffett_skill.py`](buffett_skill.py)  
   - Keyless SEC EDGAR REST integration with mandatory student User-Agent (`Oladapo Olaniyan (oolaniy@purdue.edu)`).
   - Enforces 10-K only, 1-year annual flows (~340–385 days), and latest-filing-wins precedence.
   - Primary and fallback XBRL concept mapping (`RevenueFromContractWithCustomerExcludingAssessedTax` -> `Revenues`; `PaymentsToAcquirePropertyPlantAndEquipment` -> `PaymentsToAcquireProductiveAssets`).
   - Computes Owner Earnings ($OCF - \text{CapEx}$), ROE ($\text{Net Income} / \text{Equity}$), and Buffett's three core hurdles deterministically in code.
   - Strictly enforces `"not found"` (no estimates) and `"not known"` when equity $\le 0$ or inputs are missing.
3. **Interactive Streamlit Web Application:** [`app.py`](app.py)  
   - Title with mandatory course attribution: *Data from SEC EDGAR; built with AI help, a learning demonstration, not investment advice.*
   - Visualizes 5-year Net Income vs. Owner Earnings bar chart.
   - Displays complete 5-year 10-K audited fact table with XBRL provenance tags.
   - Renders Warren Buffett memo and runs an automated **Hallucination Detection Gate** (flags any number in the memo not printed by code).
   - Sidebar toggle to inject hand-typed unprinted numbers (e.g., $40.0\%$) to prove active flagger enforcement.
4. **Audited Investment Memos:**
   - Costco Wholesale Corp. (`COST`): [`COST_buffett_memo.md`](COST_buffett_memo.md) (Verdict: **OWN THE BUSINESS**, 3 of 3 checks passed).
   - JPMorgan Chase & Co. (`JPM`): [`JPM_buffett_memo.md`](JPM_buffett_memo.md) (Verdict: **PASS / WATCH**, CapEx `"not found"`, checks `"not known"`).
   - Target Coverage PepsiCo, Inc. (`PEP`): [`PEP_buffett_memo.md`](PEP_buffett_memo.md) (Verdict: **OWN THE BUSINESS**, 3 of 3 checks passed).
5. **Comprehensive Checkout Report:** [`checkout.md`](checkout.md)  
   Full analytical writeup addressing Question (D), Rules (R), Build, Known-Answer Proof & Probes (V), Line-by-Line Code Explanation, Decision Line, Agent Skills Analysis, and Reflection.
6. **Brightspace Quiz Submission Text:** [`../../brightspace/lab-18_submission.txt`](../../brightspace/lab-18_submission.txt)  
   Clean, pre-formatted copy-paste response ready for Brightspace checkout quiz.

---

## 🎯 Verification & Known-Answer Summary

### 1. Costco Wholesale Corp. (`COST`) — 100% Exact Match ($ Millions)

| FY End | Revenue | Net Income | Operating Cash Flow | Capital Spending | Equity | ROE % | Owner Earnings | Status |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **2022-08-28** | 226,954 | 5,844 | 7,392 | 3,891 | 20,642 | 28.3% | 3,501 | **VERIFIED** |
| **2023-09-03** | 242,290 | 6,292 | 11,068 | 4,323 | 25,058 | 25.1% | 6,745 | **VERIFIED** |
| **2024-09-01** | 254,453 | 7,367 | 11,339 | 4,710 | 23,622 | 31.2% | 6,629 | **VERIFIED** |
| **2025-08-31** | 275,235 | 8,099 | 13,335 | 5,498 | 29,164 | 27.8% | 7,837 | **VERIFIED** |
| **2026-08-30** | 303,154 | 9,226 | 15,817 | 6,435 | 35,803 | 25.8% | 9,382 | **VERIFIED** |

| Buffett's Hurdle Check | COST Code Result | Course Official Benchmark |
| :--- | :---: | :---: |
| 1. ROE of 15% or more every year | **PASS** | `pass` |
| 2. Owner earnings positive every year | **PASS** | `pass` |
| 3. Owner earnings grew, first year to last | **PASS** | `pass` |

### 2. Probes Summary

1. **JPMorgan Chase (`JPM`)**: Capital spending is `"not found"`; Owner earnings is `"not found"`; Checks 2 and 3 evaluate to `"not known"`. Buffett memo accurately passes on business ownership because owner earnings cannot be judged for commercial banks.
2. **Hand-Typed Number Injection**: Injecting `40.0%` ROE into the memo text immediately triggers the red alert banner in `app.py`: `⚠️ 40.0% [UNPRINTED / FLAGGED]`.
3. **Browser AI / Zero-Skill Comparison**: A generic browser AI without SEC EDGAR extraction conflates trailing-twelve-month numbers, uses non-GAAP adjusted earnings, or averages equity, producing inconsistent ROE values with zero provenance trail.

---

## 💻 How to Run the Application

Execute from the project workspace:
```powershell
streamlit run labs/lab-18/app.py
```
Or directly using the virtual environment:
```powershell
& "c:\Users\dolan\Code\school\Fall-2026\FIN-43900\workspace\.venv\Scripts\streamlit.exe" run "c:\Users\dolan\Code\school\Fall-2026\FIN-43900\workspace\labs\lab-18\app.py"
```
To run the extraction script via CLI:
```powershell
& "c:\Users\dolan\Code\school\Fall-2026\FIN-43900\workspace\.venv\Scripts\python.exe" "c:\Users\dolan\Code\school\Fall-2026\FIN-43900\workspace\labs\lab-18\buffett_skill.py" COST
```
