# Lab 19 — Legend Panel

**Course:** FIN 43900 — AI Finance Applications, Fall 2026  
**Student / Author:** **Oladapo Olaniyan** (`oolaniy@purdue.edu`)  
**Institution:** Mitchell E. Daniels, Jr. School of Business, Purdue University  
**Target Coverage Security:** PepsiCo, Inc. (`PEP`)  
**Project 2 Fund Largest Holding:** Apple Inc. (`AAPL`) (from Vanguard Total World Stock ETF `VT`)  
**Known Answer Benchmark:** Costco Wholesale Corp. (`COST`)  
**Financial Institution Probe:** JPMorgan Chase & Co. (`JPM`)  
**Date:** November 5, 2026  
**Category:** Thursday Merit Checkout (0–25 Points)  
**Streamlit App File:** `labs/lab-19/app.py`  
**Deploy to Streamlit Community Cloud:** [Publish / Deploy Legend Panel App](https://share.streamlit.io/deploy?repository=Dapize-Mo/FIN43900-AI-Finance-Applications&branch=main&mainModule=labs/lab-19/app.py)  

---

## 📌 Controlling Instructions & Source Hierarchy

- **Official Assignment:** [Week 11 — Lab 19 Legend Panel](https://github.com/CinderZhang/FIN43900-Fall2026/blob/main/lessons/week-11/lab-19-legend-panel.md)
- **Session Slides:** [Session 19 Slides](https://github.com/CinderZhang/FIN43900-Fall2026/blob/main/lessons/week-11/slides-session-19.md)
- **Student Handout:** [Student Handout — Investors as Skills](https://github.com/CinderZhang/FIN43900-Fall2026/blob/main/lessons/week-11/student-handout.md)
- **Required Prework:** [Week 11 Prework](https://github.com/CinderZhang/FIN43900-Fall2026/blob/main/lessons/week-11/student-prework.md)
- **FAskills Expert Personas:** [Ben Graham](https://github.com/CinderZhang/FAskills/blob/main/financial-researcher/experts/ben_graham.md) · [Michael Burry](https://github.com/CinderZhang/FAskills/blob/main/financial-researcher/experts/michael_burry.md) · [Warren Buffett](https://github.com/CinderZhang/FAskills/blob/main/financial-researcher/experts/warren_buffett.md)
- **SEC EDGAR API Docs:** [SEC EDGAR Application Programming Interfaces](https://www.sec.gov/search-filings/edgar-application-programming-interfaces)

---

## 🚀 Deliverables & Files

1. **Agent Skills (`SKILL.md`):**
   - [`skills/graham-investor/SKILL.md`](skills/graham-investor/SKILL.md): Benjamin Graham classical defensive investor skill (working capital safety, earnings stability, earnings growth).
   - [`skills/burry-investor/SKILL.md`](skills/burry-investor/SKILL.md): Michael Burry forensic accounting skill (operating cash flow vs. net income, total liabilities vs. equity).
   - [`skills/buffett-investor/SKILL.md`](skills/buffett-investor/SKILL.md): Warren Buffett franchise moat skill (ROE >= 15%, positive owner earnings, owner earnings growth).
   - Discovered across global (`~/.gemini/config/skills/`) and workspace (`.agents/skills/`) paths.
2. **Deterministic Extraction & Legend Panel Engine:** [`panel_skill.py`](panel_skill.py)
   - Keyless SEC EDGAR REST integration with student User-Agent (`Oladapo Olaniyan (oolaniy@purdue.edu)`).
   - Enforces 10-K only, 1-year annual flows (~340–385 days), latest-filing-wins precedence.
   - Extracts `AssetsCurrent`, `LiabilitiesCurrent`, `Liabilities`, `StockholdersEquity`, `NetIncomeLoss`, `NetCashProvidedByUsedInOperatingActivities`, `PaymentsToAcquirePropertyPlantAndEquipment` / `PaymentsToAcquireProductiveAssets`, `RevenueFromContractWithCustomerExcludingAssessedTax` / `Revenues`.
   - Computes 8 deterministic hurdles across Buffett, Graham, and Burry.
   - Enforces strict missing-value rules (`"not found"` and `"not known"`).
3. **Interactive Streamlit Web Application:** [`app.py`](app.py)
   - Mandatory course attribution and learning disclaimer.
   - Panel Table: Investor × Check (pass / fail / not known).
   - Three Investor Verdicts and Memos side by side in columns.
   - Automated Hallucination Detection Gate across ALL THREE memos.
   - Dynamic Graham Current Ratio threshold slider/toggle (default 2.0; probe 1.0).
   - 5-year SEC EDGAR fact table with primary XBRL provenance tags and Altair charts.
4. **Audited Investment Memos:**
   - Costco Wholesale Corp. (`COST`): [`COST_panel_memo.md`](COST_panel_memo.md) (Known answer benchmark: Buffett 3/3, Graham 2/3 with CR fail at 1.06, Burry 2/2).
   - PepsiCo, Inc. (`PEP`): [`PEP_panel_memo.md`](PEP_panel_memo.md) (Target coverage: Buffett 3/3 pass, Graham fail on CR 0.85, Burry fail on leverage 4.26).
   - Apple Inc. (`AAPL`): [`AAPL_panel_memo.md`](AAPL_panel_memo.md) (Project 2 fund largest holding: Buffett 3/3 pass, Graham fail on CR 1.02, Burry fail on FY25 OCF < NI and leverage 2.61).
   - JPMorgan Chase & Co. (`JPM`): [`JPM_panel_memo.md`](JPM_panel_memo.md) (Honest missing facts: CapEx not found -> owner earnings not known).
5. **Comprehensive Checkout Report:** [`checkout.md`](checkout.md)
   - Rigorous Thursday merit report covering all 5 rubric criteria, code explanation, bull/bear partner attack, threshold design choice analysis, panel AI agent theory, and personal growth note.
6. **Brightspace Quiz Submission:** [`../../brightspace/lab-19_submission.txt`](../../brightspace/lab-19_submission.txt)
   - Clean, pre-formatted copy-paste response ready for Brightspace quiz attempt.

---

## 📊 Summary of Known-Answer Reproduction (Costco — `COST`)

### 5-Year Primary Ratios & Financials ($ Millions)
| FY End | Revenue | Net Income | OCF | CapEx | Owner Earn | Equity | Liabilities | ROE % | Current Ratio | Liab ÷ Equity |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 2022-08-28 | 226,954 | 5,844 | 7,392 | 3,891 | 3,501 | 20,642 | 43,519 | 28.3% | **1.02** | **2.11** |
| 2023-09-03 | 242,290 | 6,292 | 11,068 | 4,323 | 6,745 | 25,058 | 43,936 | 25.1% | **1.07** | **1.75** |
| 2024-09-01 | 254,453 | 7,367 | 11,339 | 4,710 | 6,629 | 23,622 | 46,209 | 31.2% | **0.97** | **1.96** |
| 2025-08-31 | 275,235 | 8,099 | 13,335 | 5,498 | 7,837 | 29,164 | 47,935 | 27.8% | **1.03** | **1.64** |
| 2026-08-30 | 303,154 | 9,226 | 15,817 | 6,435 | 9,382 | 35,803 | 53,242 | 25.8% | **1.06** | **1.49** |

### Panel Table on COST
| Investor | Check Description | Hurdle Rule | Observed Value | Status |
|---|---|---|---|---|
| **Buffett** | Return on Equity | >= 15.0% every year | 28.3%, 25.1%, 31.2%, 27.8%, 25.8% | **PASS** |
| **Buffett** | Owner Earnings Positivity | > 0 every year | 3,501M, 6,745M, 6,629M, 7,837M, 9,382M | **PASS** |
| **Buffett** | Owner Earnings Growth | Year 5 > Year 1 | 9,382M > 3,501M | **PASS** |
| **Graham** | Current Ratio Safety | >= 2.0 latest year | 1.06 vs 2.0 hurdle | **FAIL** |
| **Graham** | Net Income Stability | > 0 every year | 5,844M, 6,292M, 7,367M, 8,099M, 9,226M | **PASS** |
| **Graham** | Net Income Growth | Year 5 > Year 1 | 9,226M > 5,844M | **PASS** |
| **Burry** | Earnings Quality (Cash Backing) | OCF >= NI every year | 7.4B>=5.8B, 11.1B>=6.3B, 11.3B>=7.4B, 13.3B>=8.1B, 15.8B>=9.2B | **PASS** |
| **Burry** | Leverage Cushion | Liab ÷ Equity <= 2.0 | 1.49 vs 2.0 ceiling | **PASS** |

**Verdicts:** Buffett: **OWN THE BUSINESS** (3/3) | Graham: **REJECT / SPECULATIVE** (2/3) | Burry: **PASS FORENSIC SCREEN** (2/2)  
**Probe Verification:** Lowering Graham's current ratio hurdle to 1.0 flips Graham's status to **PASS** (1.06 >= 1.0), changing Graham's verdict to **DEFENSIVE INVESTMENT** (3/3).

---

## 💻 How to Run

### Command-Line Execution
```bash
# Run panel audit on Costco (known answer) with default 2.0 Graham threshold
python labs/lab-19/panel_skill.py COST 2.0

# Run Graham threshold probe at 1.0 (flips COST Graham check to PASS)
python labs/lab-19/panel_skill.py COST 1.0

# Run panel audit on Target Coverage (PepsiCo)
python labs/lab-19/panel_skill.py PEP 2.0

# Run panel audit on Project 2 fund largest holding (Apple)
python labs/lab-19/panel_skill.py AAPL 2.0

# Run panel audit on Banking probe (JPMorgan Chase - tests honest missing CapEx)
python labs/lab-19/panel_skill.py JPM 2.0
```

### Launch Interactive Streamlit Web Application
```bash
streamlit run labs/lab-19/app.py
```

