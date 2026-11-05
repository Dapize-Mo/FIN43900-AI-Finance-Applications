# FIN 43900 Lab 19 Checkout — Legend Panel

**Student Name:** Oladapo Olaniyan  
**Email:** `oolaniy@purdue.edu`  
**Course:** FIN 43900 — AI Finance Applications, Mitchell E. Daniels, Jr. School of Business, Purdue University  
**Session:** Session 19 (Week 11, Thursday Merit Checkout — 25 Points)  
**Lab Date:** 11/05/2026 (November 5, 2026)  
**Session Token:** `wood`  
**Target Coverage Security:** PepsiCo, Inc. (`PEP`)  
**Project 2 Fund Largest Holding:** Apple Inc. (`AAPL`) (from Vanguard Total World Stock ETF `VT`)  
**Benchmark Known-Answer Security:** Costco Wholesale Corp. (`COST`)  
**Financial Institution Probe:** JPMorgan Chase & Co. (`JPM`)  
**Interactive Streamlit App:** [`labs/lab-19/app.py`](app.py)  
**Live Deployed App (Streamlit Community Cloud):** [Legend Panel (Buffett · Graham · Burry) · Lab 19 · Streamlit](https://dapize-mo-fin43900-ai-finance-applications-labslab-19app-gk16xc.streamlit.app/)  
**Publish / Deploy Link:** [Deploy Legend Panel App](https://share.streamlit.io/deploy?repository=Dapize-Mo/FIN43900-AI-Finance-Applications&branch=main&mainModule=labs/lab-19/app.py)  

---

## 1. Core Question & Decision Definition (D)

> **Core Question (D):** *When three investors' skills read the same 10-K facts, where do they agree, where do they split — and would you trust the panel?*

### Architectural Foundation
1. **Decoupling Arithmetic Computation from Narrative Judgment:**
   - **Code computes every single number** deterministically from primary SEC EDGAR 10-K XBRL facts (zero arithmetic hallucinations, 100% computational reproducibility).
   - **The agent personas supply qualitative investment philosophy only** (Warren Buffett evaluates moat and owner earnings; Benjamin Graham evaluates balance sheet margin of safety and earnings stability; Michael Burry evaluates forensic cash conversion and debt cushion).
   - **The verification gate flags any number in any memo** not explicitly printed by the underlying Python extraction script.
2. **Honest Accounting Principle:**
   - A value missing from SEC filings prints strictly as `"not found"`, never an estimated, interpolated, or guessed figure.
   - A quantitative hurdle with a missing input or undefined arithmetic condition (e.g., negative equity or missing CapEx) resolves strictly to `"not known"`.

---

## 2. Teammates, Collaboration & Personal Contribution

- **Teammates / Learning Partners:** Paired with **J. Maffei** (`maffeij@purdue.edu` | Target Company: Oracle Corp. — `ORCL`) for:
  1. *Five-minute pre-screen discussion (no screens):* Debated how Graham and Burry read Costco differently from Buffett before inspecting code. We established that while Buffett prizes Costco's high ROE and customer brand loyalty, Graham's strict liquidationist mindset penalizes Costco's sub-2.0 current ratio, whereas Burry's forensic lens approves because operating cash flow consistently dwarfs net income with bounded leverage.
  2. *Line-by-line code explanation:* Walked through the Graham check evaluation function, specifically examining how missing balance sheet items default safely to `"not known"` without crashing.
  3. *Partner attack debate:* Exchanged 2-sentence bear and bull arguments on `PEP` and `AAPL` grounded exclusively in the panel table.
- **Personal Contribution:** Independently designed and authored:
  - Two new agent skills (`graham-investor` and `burry-investor`) co-located with `buffett-investor` in `labs/lab-19/skills/` and registered across global (`~/.gemini/config/skills/`) and project (`.agents/skills/`) directories.
  - Complete Python extraction and evaluation engine [`panel_skill.py`](panel_skill.py) supporting all 8 hurdles across 3 legendary investors.
  - Interactive Streamlit application [`app.py`](app.py) with side-by-side 3-column memo view, interactive Graham threshold slider (2.0 vs 1.0), dynamic Altair charts, and automated multi-memo hallucination detector.
  - Full empirical verification across four companies (`COST`, `PEP`, `AAPL`, `JPM`).

---

## 3. Criterion 1: Known-Answer Reproduction (Costco — `COST`)

### A. 5-Year Primary Ratios & Financial Fact Verification
The keyless SEC EDGAR REST API extracted 10-K annual facts for Costco Wholesale Corp. (`CIK: 0000909832`) across fiscal years 2022 through 2026. Every ratio matches the official course known-answer table exactly to two decimal places:

| FY End | Net Income ($M) | Op Cash Flow ($M) | CapEx ($M) | Owner Earn ($M) | Stockholders' Equity ($M) | ROE % | Current Ratio | Liabilities ÷ Equity |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| **2022-08-28** | 5,844 | 7,392 | 3,891 | 3,501 | 20,642 | **28.3%** | **1.02** | **2.11** |
| **2023-09-03** | 6,292 | 11,068 | 4,323 | 6,745 | 25,058 | **25.1%** | **1.07** | **1.75** |
| **2024-09-01** | 7,367 | 11,339 | 4,710 | 6,629 | 23,622 | **31.2%** | **0.97** | **1.96** |
| **2025-08-31** | 8,099 | 13,335 | 5,498 | 7,837 | 29,164 | **27.8%** | **1.03** | **1.64** |
| **2026-08-30** | 9,226 | 15,817 | 6,435 | 9,382 | 35,803 | **25.8%** | **1.06** | **1.49** |

*Primary XBRL Tag Provenance:*
- Current Assets: `AssetsCurrent` (FY26: $46,582M)
- Current Liabilities: `LiabilitiesCurrent` (FY26: $43,952M) $\rightarrow \text{Current Ratio} = 46,582 / 43,952 = \mathbf{1.06}$
- Total Liabilities: `Liabilities` (FY26: $53,242M)
- Stockholders' Equity: `StockholdersEquity` (FY26: $35,803M) $\rightarrow \text{Liabilities} \div \text{Equity} = 53,242 / 35,803 = \mathbf{1.49}$

### B. The Panel on COST (Default Hurdles)

| Investor | Check Description | Hurdle Rule | Observed Value | Status |
|---|---|---|---|---|
| **Buffett** | Return on Equity | $\ge 15.0\%$ every year | 28.3%, 25.1%, 31.2%, 27.8%, 25.8% | **PASS** |
| **Buffett** | Owner Earnings Positivity | $> 0$ every year | 3,501M, 6,745M, 6,629M, 7,837M, 9,382M | **PASS** |
| **Buffett** | Owner Earnings Growth | Year 5 > Year 1 | $9,382\text{M} > 3,501\text{M}$ | **PASS** |
| **Graham** | Current Ratio Safety | $\ge 2.0$ latest year | $1.06 < 2.0$ hurdle | **FAIL** |
| **Graham** | Net Income Stability | $> 0$ every year | 5,844M, 6,292M, 7,367M, 8,099M, 9,226M | **PASS** |
| **Graham** | Net Income Growth | Year 5 > Year 1 | $9,226\text{M} > 5,844\text{M}$ | **PASS** |
| **Burry** | Earnings Quality (Cash Backing) | $\text{OCF} \ge \text{NI}$ every year | OCF exceeded NI in all 5 years | **PASS** |
| **Burry** | Leverage Ceiling | $\text{Liabilities} \le 2.0\times \text{Equity}$ | $1.49 \le 2.0$ ceiling | **PASS** |

- **Warren Buffett:** **3 of 3 PASS** $\rightarrow$ Verdict: **OWN THE BUSINESS**
- **Benjamin Graham:** **2 of 3 PASS** (Current ratio fails at 1.06) $\rightarrow$ Verdict: **REJECT / SPECULATIVE**
- **Michael Burry:** **2 of 2 PASS** $\rightarrow$ Verdict: **PASS FORENSIC SCREEN**

### C. Threshold Probe Verification (A Threshold is a Design Choice)
- **Experiment:** We lowered Graham's current-ratio hurdle in `panel_skill.py` and `app.py` from **2.0 to 1.0**.
- **Observed Result:** Under the 1.0 threshold, Costco's latest current ratio ($1.06$) now satisfies the hurdle ($1.06 \ge 1.0$).
- **Verdict Shift:** Graham's status flips from **FAIL** to **PASS**, raising his score to **3 of 3 PASS** and converting his verdict from **REJECT / SPECULATIVE** to **DEFENSIVE INVESTMENT**.
- **Threshold Decision Line:**
  > *Threshold Decision:* Graham threshold kept at 2.0 (classical defensive investor margin of safety); lowered to 1.0 for capital-efficient negative-working-capital retailers like Costco.

---

## 4. Criterion 2: Numbers in Code & Hallucination Flagger Gate

### A. Strict Number Provenance
Every numeric token appearing in all three investment memos originates strictly from the values extracted and printed by `panel_skill.py`. The language model supplies the synthesis narrative, persona framing, and qualitative reasoning, but never generates an ungrounded financial figure.

### B. Automated Hallucination Flagger Architecture
In `app.py`, the function `extract_printed_numbers(data)` builds an authoritative set of all valid tokens:
- Primary line items ($M), calculated ratios to 1 and 2 decimals, fiscal-year date components, CIK digits, and rule constants (`15.0`, `2.0`, `1.0`, etc.).
- The auditing function `audit_memo_numbers(memo_text, allowed_numbers)` runs a regular expression scanner `(?<![A-Za-z0-9_])(?:\$)?([0-9]+(?:,[0-9]{3})*(?:\.[0-9]+)?)(?:%)?(?![A-Za-z0-9_])` over the entire text of **all three memos**.
- Any number not present in the allowed set is immediately wrapped in `<mark style='background-color: #ffcccc; color: #cc0000; font-weight: bold;'>⚠️ TOKEN [UNPRINTED]</mark>` and surfaced in a Streamlit error banner.

### C. Empirical Flagger Probe Results
1. **Clean Baseline Execution:**
   - Buffett Memo: `0 unprinted numbers` $\rightarrow$ `✅ Zero Hallucinations: 100% verified numbers.`
   - Graham Memo: `0 unprinted numbers` $\rightarrow$ `✅ Zero Hallucinations: 100% verified numbers.`
   - Burry Memo: `0 unprinted numbers` $\rightarrow$ `✅ Zero Hallucinations: 100% verified numbers.`
2. **Adversarial Injection Probe:**
   - When the sidebar checkbox *"Inject unprinted number probe"* was checked, unprinted strings (`40.0%`, `$99,999`, `888,888`) were injected into the memo streams.
   - The flagger caught **100% of injected numbers instantly**, highlighting them in bold red text and reporting:
     `⚠️ Flagger Alert: Unprinted numbers: ['40.0%', '$99,999']` (Graham) and `['888,888']` (Burry).

---

## 5. Criterion 3: Honest Gaps ("Not Found" and "Not Known" Preserved)

### A. The JPMorgan Chase & Co. (`JPM`) Financial Institution Probe
Commercial banking balance sheets and cash flow statements differ fundamentally from industrial firms. We tested `panel_skill.py` on JPMorgan Chase (`CIK: 0000019617`):

| FY End | Net Income ($M) | Op Cash Flow ($M) | CapEx ($M) | Owner Earn ($M) | Stockholders' Equity ($M) | Total Liabilities ($M) | ROE % | Current Ratio | Liabilities ÷ Equity |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **2021-12-31** | 48,334 | 78,084 | **not found** | **not found** | 294,127 | 3,449,440 | 16.4% | **not found** | 11.73 |
| **2022-12-31** | 37,676 | 107,119 | **not found** | **not found** | 292,332 | 3,373,411 | 12.9% | **not found** | 11.54 |
| **2023-12-31** | 49,552 | 12,974 | **not found** | **not found** | 327,878 | 3,547,515 | 15.1% | **not found** | 10.82 |
| **2024-12-31** | 58,471 | -42,012 | **not found** | **not found** | 344,758 | 3,658,056 | 17.0% | **not found** | 10.61 |
| **2025-12-31** | 57,048 | -147,782 | **not found** | **not found** | 362,438 | 4,062,462 | 15.7% | **not found** | 11.21 |

### B. Audit Handling
1. **Capital Expenditures:** Tag `PaymentsToAcquirePropertyPlantAndEquipment` does not exist in standard bank 10-Ks. The script printed `"not found"`.
2. **Owner Earnings:** Because $\text{Owner Earnings} = \text{OCF} - \text{CapEx}$, missing CapEx rendered owner earnings strictly `"not found"`.
3. **Buffett Owner Earnings Checks:** Resolved strictly to `"not known"`, yielding Buffett verdict: `PASS / WATCH (CANNOT JUDGE)`.
4. **Current Ratio:** Banks do not classify current assets or current liabilities (`AssetsCurrent` and `LiabilitiesCurrent` are `"not found"`). Graham's current ratio check resolved to `"not known"`, yielding verdict: `INSUFFICIENT DATA / WATCH`.
5. **Burry Leverage Check:** Liabilities to equity ($11.21$) exceeded $2.0$, correctly triggering **FAIL**.
6. **Integrity Rule:** **Zero estimates were made.** Missing concepts were quarantined rather than papered over with guesses.

---

## 6. Criterion 4: Your Company Run (PepsiCo `PEP` & Apple `AAPL`)

### A. Target Coverage Security: PepsiCo, Inc. (`PEP`)

#### 1. Audited 5-Year Financials ($ Millions)
| FY End | Revenue | Net Income | OCF | CapEx | Owner Earn | Equity | Liabilities | ROE % | Current Ratio | Liab ÷ Equity |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **2021-12-25** | 79,474 | 7,618 | 11,616 | 4,625 | 6,991 | 16,043 | 76,226 | 47.5% | 0.83 | 4.75 |
| **2022-12-31** | 86,392 | 8,910 | 10,811 | 5,207 | 5,604 | 17,149 | 74,914 | 52.0% | 0.80 | 4.37 |
| **2023-12-30** | 91,471 | 9,074 | 13,442 | 5,518 | 7,924 | 18,503 | 81,858 | 49.0% | 0.85 | 4.42 |
| **2024-12-28** | 91,854 | 9,578 | 12,507 | 5,318 | 7,189 | 18,041 | 81,296 | 53.1% | 0.82 | 4.51 |
| **2025-12-27** | 93,925 | 8,240 | 12,087 | 4,415 | 7,672 | 20,406 | 86,852 | 40.4% | 0.85 | 4.26 |

#### 2. Panel Table on PEP
| Investor | Check Description | Status | Evidence |
|---|---|---|---|
| **Buffett** | ROE of 15% or more every year | **PASS** | 47.5%, 52.0%, 49.0%, 53.1%, 40.4% (All > 15%) |
| **Buffett** | Owner earnings positive every year | **PASS** | 6,991M, 5,604M, 7,924M, 7,189M, 7,672M (All > 0) |
| **Buffett** | Owner earnings grew, first year to last | **PASS** | 7,672M > 6,991M |
| **Graham** | Current ratio of 2.0 or more, latest year | **FAIL** | Latest CR: 0.85 vs 2.0 hurdle (fails even at 1.0) |
| **Graham** | Net income positive every year | **PASS** | Net income positive all 5 years |
| **Graham** | Net income grew, first year to last | **PASS** | 8,240M > 7,618M |
| **Burry** | Operating cash flow >= Net income every year | **PASS** | OCF exceeded NI in all 5 fiscal years |
| **Burry** | Liabilities <= 2.0x Equity, latest year | **FAIL** | Latest Liab ÷ Equity: 4.26 vs 2.0 ceiling |

- **Buffett Verdict:** **OWN THE BUSINESS** (3 of 3 Pass)
- **Graham Verdict:** **REJECT / SPECULATIVE** (2 of 3 Pass)
- **Burry Verdict:** **FAIL FORENSIC SCREEN** (1 of 2 Pass)

---

### B. Project 2 Fund Top Holding: Apple Inc. (`AAPL`)

#### 1. Audited 5-Year Financials ($ Millions)
| FY End | Revenue | Net Income | OCF | CapEx | Owner Earn | Equity | Liabilities | ROE % | Current Ratio | Liab ÷ Equity |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **2022-09-24** | 394,328 | 99,803 | 122,151 | 10,708 | 111,443 | 50,672 | 302,083 | 197.0% | 0.88 | 5.96 |
| **2023-09-30** | 383,285 | 96,995 | 110,543 | 10,959 | 99,584 | 62,146 | 290,437 | 156.1% | 0.99 | 4.67 |
| **2024-09-28** | 391,035 | 93,736 | 118,254 | 9,447 | 108,807 | 56,950 | 308,030 | 164.6% | 0.87 | 5.41 |
| **2025-09-27** | 416,161 | 112,010 | 111,482 | 12,715 | 98,767 | 73,733 | 285,508 | 151.9% | 0.89 | 3.87 |
| **2026-09-26** | 478,834 | 132,175 | 145,097 | 9,041 | 136,056 | 112,093 | 292,455 | 117.9% | 1.02 | 2.61 |

#### 2. Panel Table on AAPL
| Investor | Check Description | Status | Evidence |
|---|---|---|---|
| **Buffett** | ROE of 15% or more every year | **PASS** | 197.0%, 156.1%, 164.6%, 151.9%, 117.9% (All > 15%) |
| **Buffett** | Owner earnings positive every year | **PASS** | $98.8B to $136.1B (All > 0) |
| **Buffett** | Owner earnings grew, first year to last | **PASS** | 136,056M > 111,443M |
| **Graham** | Current ratio of 2.0 or more, latest year | **FAIL** | Latest CR: 1.02 vs 2.0 hurdle (fails 2.0; passes 1.0) |
| **Graham** | Net income positive every year | **PASS** | Net income positive all 5 years |
| **Graham** | Net income grew, first year to last | **PASS** | 132,175M > 99,803M |
| **Burry** | Operating cash flow >= Net income every year | **FAIL** | FY 2025: OCF of 111,482M < Net Income of 112,010M |
| **Burry** | Liabilities <= 2.0x Equity, latest year | **FAIL** | Latest Liab ÷ Equity: 2.61 vs 2.0 ceiling |

- **Buffett Verdict:** **OWN THE BUSINESS** (3 of 3 Pass)
- **Graham Verdict:** **REJECT / SPECULATIVE** (2 of 3 Pass at 2.0 hurdle)
- **Burry Verdict:** **FAIL FORENSIC SCREEN** (0 of 2 Pass)

---

## 7. Criterion 5: Fiduciary Decision for Project 2

> **Question:** *Would you let this panel screen companies for your Project 2 — yes, no, or only with a condition?*

### Decision: **YES, ONLY WITH A CONDITION.**

### The Fiduciary Condition:
> **The legend panel may serve only as a multi-perspective qualitative diagnostic filter, never as an unconstrained automated capital allocation decision.**
> 
> Specifically, the following three implementation rules are mandatory:
> 1. **Sector-Specific Liquidity Parameterization:** Graham's working capital threshold cannot be applied uniformly. For capital-efficient retail and technology platforms operating with negative working capital cycles (e.g., Costco with CR $1.06$ and Apple with CR $1.02$), the hurdle must be calibrated to $1.0$. Applying a rigid $2.0$ hurdle penalizes modern supply-chain efficiency and discards premier franchises.
> 2. **Financial Institution Quarantine:** Companies in the financial sector (e.g., `JPM`) must be quarantined from industrial CapEx hurdles and evaluated under bank-specific regulatory capital metrics (e.g., Common Equity Tier 1 — CET1 ratio) rather than owner earnings.
> 3. **Disagreement as a Triangulation Signal:** Disagreements across the panel must not be averaged into a composite score. When Buffett approves while Graham and Burry fail (as with `PEP` and `AAPL`), the split signals a crucial investment trade-off: **phenomenal consumer pricing power and capital productivity (Buffett) achieved alongside high structural leverage (Burry) and minimal working capital buffer (Graham).**

---

## 8. Explain the Code (Line-by-Line Walkthrough)

During the collaborative session, I walked through the Graham and Burry check evaluation functions in `panel_skill.py`:

```python
# Graham Check 1: Working Capital Hurdle with Parameterized Threshold
latest_cr = cr_list[-1]
if latest_cr is None:
    graham_c1 = "not known"
elif latest_cr >= graham_cr_threshold:
    graham_c1 = "pass"
else:
    graham_c1 = "fail"

# Graham Check 2: Five-Year Net Income Positivity
if any(ni is None for ni in ni_list):
    graham_c2 = "not known"
elif all(ni > 0 for ni in ni_list):
    graham_c2 = "pass"
else:
    graham_c2 = "fail"

# Graham Check 3: Net Income Expansion
if ni_list[0] is None or ni_list[-1] is None:
    graham_c3 = "not known"
elif ni_list[-1] > ni_list[0]:
    graham_c3 = "pass"
else:
    graham_c3 = "fail"
```

### Explaining Missing Inputs to Partner
- **Question from Partner:** *What does the code do if an enterprise does not report current assets or current liabilities (e.g., a commercial bank)?*
- **Response grounded in code:** In `get_panel_metrics()`, if `ca_entry` or `cl_entry` is missing, `cr_val` is set to `"not found"` and `None` is appended to `cr_list`. When evaluating `latest_cr`, the code checks `if latest_cr is None:` and immediately assigns `"not known"`. The code never crashes on `NoneType` or attempts division by zero, and Graham's verdict safely defaults to `INSUFFICIENT DATA / WATCH`.

---

## 9. Partner Attack: Bull vs. Bear Case Debate

### On PepsiCo, Inc. (`PEP`)
- **Partner's Bear Case (Burry/Graham Persona):**  
  *"PepsiCo is a leveraged enterprise masquerading as a defensive consumer staple. Total liabilities of \$86,852 million dwarf equity of \$20,406 million (a dangerous 4.26x leverage ratio), while a current ratio of 0.85 leaves zero cushion if refinancing rates surge."*
- **My Bull Case (Buffett Persona):**  
  *"PepsiCo generates an astonishing 40.4% to 53.1% ROE and produced \$7,672 million in owner cash flow in 2025 because Frito-Lay and beverages command unrivaled global pricing power. Working capital is kept lean precisely because inventory turns into consumer cash daily, leaving competitors powerless to erode its franchise."*

### On Apple Inc. (`AAPL`)
- **Partner's Bear Case (Burry Persona):**  
  *"In FY 2025, operating cash flow lagged net income (\$111,482 million OCF vs \$112,010 million NI), revealing an earnings quality crack where accounting income was not backed by cash. Combined with \$292,455 million in liabilities against \$112,093 million of equity (2.61x), Apple has exhausted its safe leverage capacity."*
- **My Bull Case (Buffett Persona):**  
  *"Apple generated an unprecedented \$136,056 million in owner earnings in FY 2026 and delivered a 117.9% ROE, proving it is the greatest consumer habit and software ecosystem ever engineered. The modest leverage was used to retire shares and reward owners, not cover operational shortfalls."*

---

## 10. A Panel of AI Agents — Learn on Your Own

1. **What is a panel of AI agents?**  
   A panel of AI agents is an ensemble architecture where multiple specialized agent personas, governed by distinct prompt definitions and quantitative rule functions, independently evaluate the exact same underlying ground-truth data source without cross-contaminating one another.
2. **How does it work — why do three personas on the same facts disagree?**  
   They disagree because each persona embeds a different financial objective function:
   - *Buffett's objective function:* Maximize franchise return on capital (ROE) and owner cash generation, ignoring market price fluctuations and balance sheet tightness.
   - *Graham's objective function:* Minimize downside risk of permanent capital loss via liquidation safety margins (current ratio >= 2.0, consistent positive earnings).
   - *Burry's objective function:* Detect accounting manipulation, divergence between cash flows and reported earnings, and excessive debt burdens that make firms vulnerable to macro shocks.
3. **Why this matters for quantitative finance:**  
   A single AI model prompt tends to converge toward bland consensus or mirror whatever tone is suggested in the prompt. By orchestrating a panel with deterministic code-checked hurdles, the investor forces conflicting investment philosophies to debate the same audited facts, highlighting critical risks that a monolithic model would smooth over.

---

## 11. Reflect & Personal Growth Note

> **Personal Growth Note (Ungraded, for student alone):**  
> Before this lab, I viewed agent personas as purely creative text-generation styles, often vulnerable to making up numbers or agreeing with whatever prompt was fed to them. Now, I can build an architecture that completely strips arithmetic authority away from the model, executes multi-investor hurdle tests deterministically in code from primary SEC EDGAR facts, and runs an automated gate that catches any unprinted claim across three simultaneous memos. What still feels challenging is establishing systematic, statistically sound criteria for when a traditional threshold (like Graham's 2.0) should be adapted to modern corporate balance sheets versus when modifying it constitutes post-hoc rationalization.

---

## 12. Attendance Declaration, Truth Attestation & Receipt

- **In-Person Attendance Declaration:** I hereby declare that I attended the live in-class laboratory session in LILY G420 / RAWL 2070 on Thursday, November 5, 2026.
- **Truth Attestation:** I attest that all code, empirical calculations, and analytical findings recorded in this checkout package represent my own authentic work, conducted in collaboration with my designated learning partner and utilizing AI tools strictly in accordance with course policy.
- **Verification Receipt:** Authenticated Brightspace checkout submission recorded under Purdue student ID for Oladapo Olaniyan (`oolaniy@purdue.edu`).

