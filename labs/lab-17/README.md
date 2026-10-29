# Lab 17 — Point-in-Time Audit

**Course:** FIN 43900 — AI Finance Applications, Fall 2026  
**Student / Author:** **Oladapo Olaniyan** (`oolaniy@purdue.edu`)  
**Teammate / Learning Partner:** **J. Maffei** (`maffeij@purdue.edu` | Target Company: Oracle Corp. — `ORCL`)  
**Institution:** Mitchell E. Daniels, Jr. School of Business, Purdue University  
**Case / Project Universe:** Meridian Foundation Reserve & Project 2 Macro Environment (`BIL`, `IEF`, `LQD`, `VT` | Macro Series: `CPIAUCSL`)  
**Date:** October 29, 2026  
**Session Token:** `X+AI`  
**Category:** Thursday Merit Checkout (25 Points)

---

## 📌 Controlling Instructions & Source Hierarchy

- **Course Instruction:** [Week 10 — Lab 17 Point-in-Time Audit](https://github.com/CinderZhang/FIN43900-Fall2026/blob/main/lessons/week-10/lab-17-point-in-time.md)
- **Session Slides:** [Session 17 Slides](https://github.com/CinderZhang/FIN43900-Fall2026/blob/main/lessons/week-10/slides-session-17.md)
- **Student Handout:** [Student Handout — Point-in-Time](https://github.com/CinderZhang/FIN43900-Fall2026/blob/main/lessons/week-10/student-handout.md)
- **Required Prework:** [ALFRED Vintage Architecture](https://github.com/CinderZhang/FIN43900-Fall2026/blob/main/lessons/week-10/student-prework.md)
- **Reference API Docs:** [Federal Reserve Bank of St. Louis FRED / ALFRED](https://fred.stlouisfed.org)

---

## 🚀 Deliverables & Files

1. **Interactive FRED/ALFRED Streamlit Web Application:** [`asof_app.py`](asof_app.py)  
   A high-performance Streamlit application downloading live CSV feeds from FRED and ALFRED:
   - Fetches today's values from `https://fred.stlouisfed.org/graph/fredgraph.csv?id=SERIES`.
   - Fetches historical point-in-time vintage values from `https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=SERIES&vintage_date=YYYY-MM-DD`.
   - Caches downloads using `@st.cache_data` and sanitizes missing values (`.`).
   - Interactive sidebar with preselected default interest rates (`BAA`, `FEDFUNDS`, `DGS10`, `MORTGAGE30US`), custom series input box, customizable start date, and "as known on" vintage date.
   - Line charts for each series with publication cutoff annotations and a complete audit ledger table tracking publication lag (late values) and subsequent historical revisions.
   - Isolated fault-tolerant error boundaries for invalid series IDs.
2. **Comprehensive Checkout Report:** [`checkout.md`](checkout.md)  
   Exhaustive analytical writeup addressing all five merit criteria: Core Question (D), Dual-Timestamp Representation (R), Streamlit Implementation (I), Known-Answer Proof & Probes (V), Student Series Deep Dive & Data Card (E), Code Walkthrough & Line-by-Line Explanation, Partner Attack & Rebuttal, Fiduciary Call for Project 2, and Point-in-Time Learnings & Reflection.
3. **Brightspace Quiz Submission Text:** [`../../brightspace/lab-17_submission.txt`](../../brightspace/lab-17_submission.txt)  
   Pre-formatted, clean text block structured for the authenticated Brightspace checkout quiz.

---

## 🎯 Verification & Known-Answer Summary

### 1. The 5 October 2026 Official Known Answer
Setting the **"As known on" Date** to **`2026-10-05`** verifies the exact published answers:

| Series ID | FRED Series Name | Last Date Known on 5 Oct 2026 | Value Known Then | Value Measured Today | Late Values (Lag) | Revised Values | Status |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **`BAA`** | Moody's Baa Corporate Bond Yield | **2026-09-01** (Sept 2026) | **6.47** | 6.47 | 0 | 0 | **VERIFIED** |
| **`FEDFUNDS`** | Effective Federal Funds Rate | **2026-09-01** (Sept 2026) | **3.75** | 3.75 | 0 | 0 | **VERIFIED** |
| **`DGS10`** | 10-Year Treasury Yield | **2026-10-02** | **5.28** | 4.99 | 16 | 0 | **VERIFIED** |
| **`MORTGAGE30US`** | 30-Year Mortgage Rate | **2026-10-01** | **7.28** | 7.24 | 4 | 0 | **VERIFIED** |

### 2. The PAYEMS Revision Probe (15 January 2025)
- **Last Date Known as of 15 Jan 2025:** December 2024 (`2024-12-01`)
- **Value Known Then:** **`159,536`** thousand jobs
- **Value Measured Today:** **`158,316`** thousand jobs (down by 1,220,000 jobs)
- **Late Values Today:** **`21`** months
- **Revised Values Count:** **`381`** months (proves distinct historical ALFRED archive retrieval; strictly non-zero)

### 3. Student Chosen Series: `CPIAUCSL` (Consumer Price Index)
- **Data Card Summary:** Monthly, Index 1982-1984=100, Seasonally Adjusted, BLS source.
- **Publication Lag:** ~10–15 days post month-end. As of September 30, 2026, September CPI (336.298) was unknowable; latest print was August 2026 (334.131).
- **Revision History:** Probing vintage January 15, 2024 against today reveals **60 historical monthly prints revised** due to BLS annual 5-year seasonal factor re-estimation.
- **Fiduciary Disposition for Project 2:** **QUARANTINE**. Admitted only under dynamic point-in-time API calls (`as_of_date = decision_date`) with a mandatory $t-1$ month lag, or by substituting the unrevised non-seasonally adjusted series `CPIAUCNS`.

---

## 💻 How to Run the Application

Execute the following command from the workspace directory:
```powershell
streamlit run labs/lab-17/asof_app.py
```
Or directly using the project's Python virtual environment:
```powershell
& "c:\Users\dolan\Code\school\Fall-2026\FIN-43900\workspace\.venv\Scripts\streamlit.exe" run "c:\Users\dolan\Code\school\Fall-2026\FIN-43900\workspace\labs\lab-17\asof_app.py"
```
The browser will automatically launch with interactive charts, date controls, and the point-in-time audit ledger.
