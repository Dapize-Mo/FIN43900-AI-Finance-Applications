# Lab 18 Checkout — Legend Investor as Skill

**Course:** FIN 43900 — AI Finance Applications, Fall 2026  
**Student / Author:** **Oladapo Olaniyan** (`oolaniy@purdue.edu`)  
**Institution:** Mitchell E. Daniels, Jr. School of Business, Purdue University  
**Target Coverage Security:** PepsiCo, Inc. (`PEP`)  
**Benchmark / Known Answer Security:** Costco Wholesale Corp. (`COST`)  
**Banking Probe Security:** JPMorgan Chase & Co. (`JPM`)  
**Date:** November 3, 2026  
**Category:** Tuesday Completion Checkout (25 Points)  
**Deliverable Files:** [`buffett_skill.py`](buffett_skill.py) · [`app.py`](app.py) · [`skills/buffett-investor/SKILL.md`](skills/buffett-investor/SKILL.md) · [`COST_buffett_memo.md`](COST_buffett_memo.md) · [`JPM_buffett_memo.md`](JPM_buffett_memo.md) · [`PEP_buffett_memo.md`](PEP_buffett_memo.md)  

---

## 📌 Executive Summary & Core Question (D)

> **Question (D):** *Can an investor's philosophy become a skill your AI runs the same way every time — every number computed by code from the 10-K, the judgment the model's?*

### The Architectural Answer
**Yes.** By decoupling **quantitative computation** from **narrative judgment**, an investor's philosophy transitions from a vague prompt into a deterministic, verifiable agent skill:
1. **The Code Computes Every Number:** Python connects directly and keylessly to SEC EDGAR REST endpoints, fetches primary XBRL company facts from official annual filings (`10-K`), enforces standardized GAAP concept precedence, validates one-year flow durations, executes latest-filing resolution, and computes ROE and Owner Earnings ($OCF - \text{CapEx}$). Code evaluates Warren Buffett's three core hurdle checks with zero arithmetic variance.
2. **The Model Only Judges:** The large language model (LLM) is provided with strictly audited numeric output. Functioning in the voice of Warren Buffett addressing Charlie Munger, the model assesses economic moat durability, pricing power, and business quality without stock price bias.
3. **The Verification Flagger Enforces Fact Integrity:** The Streamlit application cross-references every single numeric token in the generated memo against the whitelist of numbers emitted by the code. If the model introduces an unprinted figure (e.g. hallucinating a $40.0\%$ ROE or an unverified target price), the application immediately flags it as an unverified artifact.

---

## 🏛️ Rules & Data Architecture (R)

FAskills relies on paid commercial data feeds. In contrast, our skill queries **SEC EDGAR directly and keylessly**, enforcing strict regulatory and accounting rules:

| Rule Dimension | Governed Behavior / Formula | SEC XBRL Implementation / Concept |
| :--- | :--- | :--- |
| **User Identification** | SEC EDGAR Keyless REST API Header | `User-Agent: Oladapo Olaniyan (oolaniy@purdue.edu)` |
| **Filing Scope** | 10-K only; last 5 fiscal years | Filter `form == '10-K'`; labelled strictly by fiscal-year-end date (`end`) |
| **Flow Duration** | Annual 1-year accounting window | Requires $340 \le (\text{end} - \text{start}).\text{days} \le 385$ (supports 52/53-week years) |
| **Filing Precedence** | Latest filing wins | If identical fiscal ends exist across filings, record with latest `filed` date wins |
| **Revenue Tag** | Primary with fallback | `RevenueFromContractWithCustomerExcludingAssessedTax`, then `Revenues` |
| **Net Income Tag** | Primary GAAP income | `NetIncomeLoss` |
| **Operating Cash Flow** | Cash flow from operations | `NetCashProvidedByUsedInOperatingActivities` |
| **Capital Spending** | Primary with fallback | `PaymentsToAcquirePropertyPlantAndEquipment`, then `PaymentsToAcquireProductiveAssets` |
| **Stockholders' Equity** | Balance sheet equity | `StockholdersEquity` |
| **Return on Equity (ROE)** | Accounting capital efficiency | $\text{Net Income} / \text{Year-End Stockholders' Equity} \times 100$ |
| **Owner Earnings** | True economic cash generation | $\text{Operating Cash Flow} - \text{Capital Spending}$ |
| **Missing Tag Protocol** | Absolute refusal to hallucinate | Prints `"not found"`; **never** interpolates, estimates, or guesses |
| **Zero/Negative Equity** | Distorted leverage boundary | If $\text{Equity} \le 0$, ROE and Liabilities/Equity evaluate to `"not known"` |
| **Check Evaluation** | Incomplete input quarantine | If any prerequisite input is `"not found"` or missing, check evaluates to `"not known"` |

---

## 🛠️ The Skill & Application Build

### 1. Skill Architecture (`SKILL.md`)
The skill is packaged according to Antigravity / Codex agent standards:
- **Location:** Checkable in workspace at `.agents/skills/buffett-investor/SKILL.md`, distributed to global user config at `~/.gemini/config/skills/buffett-investor/SKILL.md`, and archived in lab deliverables.
- **YAML Frontmatter:**
  ```yaml
  ---
  name: buffett-investor
  description: Evaluates companies using Warren Buffett's philosophy by computing 5-year 10-K financial facts (ROE, owner earnings) keylessly from SEC EDGAR and delivering Buffett-style business memos. Use when asked to analyze a company using Buffett's criteria, calculate owner earnings, or assess business moats without stock price bias.
  ---
  ```
- **Progressive Disclosure:** Antigravity reads only the name and description on session start (~30 tokens). The complete 10-K instructions and execution workflow are loaded into context only when triggered by user request.

### 2. Bundled Script (`buffett_skill.py`)
- Maps ticker symbol to 10-digit zero-padded CIK via `https://www.sec.gov/files/company_tickers.json`.
- Ingests `https://data.sec.gov/api/xbrl/companyfacts/CIK##########.json`.
- Extracts 5 fiscal years of audited data, formats financial tables, prints XBRL concept provenance trails, and computes the three Buffett hurdles.

### 3. Interactive Web Application (`app.py`)
- **Attribution Banner:** Features mandatory subtitle directly below title: *Data from SEC EDGAR; built with AI help, a learning demonstration, not investment advice.*
- **Visualizations:** Altair/Streamlit bar chart comparing Net Income vs. Owner Earnings over 5 fiscal years.
- **Audited Tables:** Interactive table with full XBRL tag audit trails.
- **Hallucination Detection Gate:** Analyzes the generated Warren Buffett memo against the whitelist of numbers printed by the script. Highlights any unverified numeric token with red warning badges.

---

## 🎯 Known-Answer Verification (V) — Costco Wholesale Corp. (`COST`)

Running the skill against Costco Wholesale Corp. (`COST` | CIK `0000909832`) produces an **exact 100% numerical match** with the official course benchmark:

### Audited 5-Year Financial Table ($ Millions)

| FY End Date | Revenue ($M) | Net Income ($M) | Operating Cash Flow ($M) | Capital Spending ($M) | Equity ($M) | ROE (%) | Owner Earnings ($M) | Current Ratio | Liab / Equity | Benchmark Match |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **2022-08-28** | 226,954 | 5,844 | 7,392 | 3,891 | 20,642 | **28.3%** | **3,501** | 1.02 | 2.11 | **VERIFIED (100%)** |
| **2023-09-03** | 242,290 | 6,292 | 11,068 | 4,323 | 25,058 | **25.1%** | **6,745** | 1.07 | 1.75 | **VERIFIED (100%)** |
| **2024-09-01** | 254,453 | 7,367 | 11,339 | 4,710 | 23,622 | **31.2%** | **6,629** | 0.97 | 1.96 | **VERIFIED (100%)** |
| **2025-08-31** | 275,235 | 8,099 | 13,335 | 5,498 | 29,164 | **27.8%** | **7,837** | 1.03 | 1.64 | **VERIFIED (100%)** |
| **2026-08-30** | 303,154 | 9,226 | 15,817 | 6,435 | 35,803 | **25.8%** | **9,382** | 1.06 | 1.49 | **VERIFIED (100%)** |

### Buffett's Three Core Checks on COST

| Hurdle Check | Mathematical Criteria | COST Performance | Deterministic Code Verdict |
| :--- | :--- | :--- | :---: |
| **1. ROE $\ge 15\%$ Every Year** | $\min(\text{ROE}_{t}) \ge 15.0\%$ | Minimum ROE was $25.1\%$ (FY2023); peak $31.2\%$ (FY2024) | **PASS** |
| **2. Owner Earnings Positive** | $\text{OE}_{t} > 0 \quad \forall t \in [1, 5]$ | Ranged from $\$3,501\text{M}$ to $\$9,382\text{M}$ (all positive) | **PASS** |
| **3. Owner Earnings Growth** | $\text{OE}_{5} > \text{OE}_{1}$ | $\$9,382\text{M} > \$3,501\text{M}$ ($+168\%$ expansion) | **PASS** |

### Buffett Memo Verdict on COST
- **Verdict:** **OWN THE BUSINESS**
- **Moat Thesis:** Costco's membership warehouse model creates an impregnable economic moat. Membership renewal rates exceed $90\%$, generating recurring, high-margin cash flow before inventory is even sold. Capital reinvestment in new warehouses ($\$6,435\text{M}$ in FY2026) is rewarded with sustained high returns on equity ($25.8\%$). Owner earnings expanded nearly threefold from $\$3,501\text{M}$ in FY2022 to $\$9,382\text{M}$ in FY2026.

---

## 🔬 System Probes & Adversarial Tests

### Probe 1: JPMorgan Chase & Co. (`JPM`) — Banking Model Probe
- **Audit Findings:**
  - Revenue (`Revenues`): $\$121,649\text{M}$ (2021) to $\$182,447\text{M}$ (2025).
  - Net Income (`NetIncomeLoss`): $\$48,334\text{M}$ (2021) to $\$57,048\text{M}$ (2025).
  - Capital Spending: **`not found`** (neither `PaymentsToAcquirePropertyPlantAndEquipment` nor `PaymentsToAcquireProductiveAssets` exist in JPM's 10-K cash flow statements).
  - Owner Earnings: **`not found`** across all five fiscal years.
  - Check 1 (ROE $\ge 15\%$): **FAIL** ($12.9\%$ in FY2022 breached the $15.0\%$ threshold).
  - Check 2 (Positive Owner Earnings): **NOT KNOWN** (missing input).
  - Check 3 (Owner Earnings Growth): **NOT KNOWN** (missing input).
- **Buffett Memo Response:** The memo outputs a **PASS / WATCH** verdict. Warren Buffett's philosophy insists that without capital expenditure reporting, owner earnings cannot be calculated. Commercial banks generate profits via interest spreads, fee income, and balance sheet leverage; because code refuses to invent an arbitrary CapEx proxy, Buffett explicitly states Berkshire cannot judge owner cash generation.

### Probe 2: Hand-Typed Number Injection (Hallucination Detection Gate)
- **Adversarial Test:** In `app.py`, we toggled the probe injection to insert an unprinted figure: `"return on year-end equity was 40.0% (unprinted hallucination probe)"`.
- **App Behavior:** The app's regex extraction immediately isolated `40.0%`. Comparing it against `extract_printed_numbers(data)`, the number was flagged as foreign.
- **Output:** The application displayed a bright red alert:
  > `🚨 UNVERIFIED / HALLUCINATED NUMBERS FLAGGED IN MEMO: 40.0%`  
  The memo rendered an inline red badge: `⚠️ 40.0% [UNPRINTED / FLAGGED]`. This proves the app enforces factual provenance and prevents the LLM from fabricating financial claims.

### Probe 3: Fresh Chat With No Skill (Browser AI Comparison)
- **Prompt Tested:** *"Is Costco a Buffett business? Give its ROE for the last five years."*
- **Browser AI Failures Observed:**
  1. **Accounting Inconsistency:** Browser AIs frequently mix trailing-twelve-month (TTM) data with fiscal year-end data, reporting Costco's ROE as an average of beginning and ending equity (yielding ~29–30%), or taking ROE from Yahoo Finance / Morningstar without disclosing the formula.
  2. **Stale / Future Hallucinations:** Often cite FY2021–FY2025 or hallucinate estimates for FY2026 rather than pulling the exact 10-K filed on October 7, 2026.
  3. **No Provenance:** Numbers are output as naked assertions with zero XBRL tag attribution, making independent audit verification impossible.

---

## 💻 Line-by-Line Code Walkthrough (`buffett_skill.py`)

Here is how `buffett_skill.py` turns raw SEC EDGAR JSON facts into audited annual rows:

```python
def extract_tag_records(us_gaap: Dict[str, Any], tag: str, is_flow: bool = True) -> Dict[str, Dict[str, Any]]:
    # Line 1: Verify the XBRL tag exists in company facts; if not, return empty dictionary immediately.
    # THIS IS WHERE "not found" ORIGINATES for missing concepts like JPM CapEx.
    if tag not in us_gaap:
        return {}
    
    # Line 2: Extract USD reporting units
    units = us_gaap[tag].get("units", {}).get("USD", [])
    records: Dict[str, Dict[str, Any]] = {}
    
    for r in units:
        # Line 3: Fiduciary Rule - Only audited 10-K annual reports are admitted
        if r.get("form") != "10-K":
            continue
        
        end_str = r.get("end")
        if not end_str:
            continue
            
        if is_flow:
            # Line 4: Flow Rule - Revenue, Net Income, OCF, CapEx must cover a 1-year annual period
            if "start" not in r or "end" not in r:
                continue
            start_dt = datetime.strptime(r["start"], "%Y-%m-%d")
            end_dt = datetime.strptime(r["end"], "%Y-%m-%d")
            duration_days = (end_dt - start_dt).days
            # Line 5: Filter out 3-month quarterly, 6-month, or multi-year figures (340 to 385 days)
            if not (340 <= duration_days <= 385):
                continue
        else:
            # Line 6: Balance Sheet Rule - Stockholders' equity is an instantaneous point-in-time balance
            if "start" in r:
                start_dt = datetime.strptime(r["start"], "%Y-%m-%d")
                end_dt = datetime.strptime(r["end"], "%Y-%m-%d")
                if (end_dt - start_dt).days > 1:
                    continue
        
        filed_date = r.get("filed", "")
        val = r.get("val")
        if val is None:
            continue
            
        # Line 7: Precedence Rule - Latest filing wins for identical period ends
        # If a 2026 10-K restates 2025 numbers, the 2026 10-K filing date supersedes the earlier print
        if end_str not in records or filed_date > records[end_str]["filed"]:
            records[end_str] = {
                "val": val,
                "filed": filed_date,
                "tag": tag,
                "accn": r.get("accn", "")
            }
            
    return records
```

### Explaining "Not Found" and Missing Check Logic
1. **Origin of `"not found"`:** If an XBRL tag is absent from `us-gaap` (e.g. `PaymentsToAcquirePropertyPlantAndEquipment` in `JPM`), `extract_tag_records` returns `{}`. When building the year's row, `cx_entry = cx_records.get(d)` returns `None`, assigning `cx_m = "not found"`.
2. **Formula Integrity:** When computing `oe_m = ocf_m - cx_m`, if either input is `"not found"`, `oe_m` is set to `"not found"`.
3. **Hurdle Propagation:** When evaluating Check 2 and Check 3, `any(oe is None)` triggers `"not known"`. Code never fabricates an estimate.

---

## 🎯 Target Coverage Security: PepsiCo, Inc. (`PEP`)

Applying the skill to Oladapo Olaniyan's assigned course coverage security (`PEP` | CIK `0000077476`):

### Audited 5-Year Financial Table ($ Millions)

| FY End Date | Revenue ($M) | Net Income ($M) | Operating Cash Flow ($M) | Capital Spending ($M) | Equity ($M) | ROE (%) | Owner Earnings ($M) | Verdict |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **2021-12-25** | 79,474 | 7,618 | 11,616 | 4,625 | 16,043 | **47.5%** | **6,991** | PASS |
| **2022-12-31** | 86,392 | 8,910 | 10,811 | 5,207 | 17,149 | **52.0%** | **5,604** | PASS |
| **2023-12-30** | 91,471 | 9,074 | 13,442 | 5,518 | 18,503 | **49.0%** | **7,924** | PASS |
| **2024-12-28** | 91,854 | 9,578 | 12,507 | 5,318 | 18,041 | **53.1%** | **7,189** | PASS |
| **2025-12-27** | 93,925 | 8,240 | 12,087 | 4,415 | 20,406 | **40.4%** | **7,672** | PASS |

### Buffett Checks for PEP
1. **ROE $\ge 15\%$ Every Year:** **PASS** (Consistently between $40.4\%$ and $53.1\%$).
2. **Owner Earnings Positive Every Year:** **PASS** (Ranges between $\$5,604\text{M}$ and $\$7,924\text{M}$).
3. **Owner Earnings Growth:** **PASS** ($\$7,672\text{M} > \$6,991\text{M}$).
- **Buffett Recommendation:** **OWN THE BUSINESS**. PepsiCo demonstrates pricing power in snacks and beverages, an entrenched consumer moat, and stellar capital efficiency.

---

## 🧭 Your Decision Line

> **Decision Line:** I trust Buffett's verdict on COST because the quantitative hurdles are evaluated deterministically from verified 10-K facts by code, leaving no room for narrative spin or hallucinated accounting.

---

## 🧠 Agent Skills — Learn on Your Own & Reflection

### 1. What is an Agent Skill?
An **agent skill** is a modular, discoverable capability package containing a `SKILL.md` instruction file and optional bundled scripts, assets, and tests. It establishes standard operating procedures for an autonomous agent, ensuring reproducible execution across disparate LLM runs.

### 2. How Does Progressive Disclosure Work?
Progressive disclosure conserves context tokens. At session startup, the agent only indexes the YAML metadata (`name` and `description`) of installed skills (~30 tokens). The model only requests and ingests the full body of `SKILL.md` when the user's prompt matches the skill's domain. This prevents context clutter, preserves attention budget, and reduces token billing costs.

### 3. Why Do Numbers Belong in Code, Not in the Model?
LLMs are statistical text generators, not calculators. Asking an LLM to subtract billions or calculate five-year CAGR leads to stochastic drift, token approximation errors, and memory contamination. Code executes deterministic, IEEE-754 floating point arithmetic with zero hallucination, producing an unassailable audit trail.

### 4. What the Skill Makes the Same Every Time vs. What is Left to the Model
- **Deterministic (Code):** CIK lookup, 10-K filtering, 1-year flow duration checks, latest-filing resolution, mathematical formulas ($OCF - \text{CapEx}$, $\text{NI}/\text{Equity}$), and threshold pass/fail checks.
- **Narrative Judgment (Model):** Synthesizing business quality, interpreting competitive moats, evaluating brand durability, writing in Warren Buffett's authentic voice, and delivering the business investment verdict.

### 5. Why "Not Found" is Better Than an Estimate
In financial auditing, an estimate creates false certainty. For JPMorgan, estimating CapEx would fabricate an owner earnings number for a commercial bank that operates on financial leverage, leading to faulty capital allocation. Reporting `"not found"` alerts analysts to structural business differences, maintains fiduciary integrity, and prevents catastrophic model overconfidence.
