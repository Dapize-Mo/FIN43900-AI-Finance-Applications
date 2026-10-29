# FIN 43900 Lab 17 — Point-in-Time Audit: Live FRED/ALFRED Rates App

**Course:** FIN 43900 — AI Finance Applications, Fall 2026  
**Student Analyst / Author:** **Oladapo Olaniyan** (`oolaniy@purdue.edu`)  
**Teammate / Learning Partner:** **J. Maffei** (`maffeij@purdue.edu` | Target Company: Oracle Corp. — `ORCL`)  
**Institution:** Mitchell E. Daniels, Jr. School of Business, Purdue University  
**Case / Project Universe:** Meridian Foundation Reserve & Project 2 Macro Environment (`BIL`, `IEF`, `LQD`, `VT` | Target Equity: `PEP` | Macro Series: `CPIAUCSL`)  
**Lab Date:** October 29, 2026  
**Session:** Session 17 (Week 10, Thursday Merit Checkout — 25 Points)  
**Brightspace Item:** Lab 17 — Point-in-Time Audit (Thursday Merit Checkout)  
**Session Token:** `X+AI`  
**Live Deployed Web Application:** [FRED/ALFRED Point-in-Time Rates App · Streamlit](https://fin43900-ai-finance-applications-wmi2hv4j245qhhgeuktnpc.streamlit.app/)  
**GitHub Direct Application Link:** [`asof_app.py` on GitHub](https://github.com/Dapize-Mo/FIN43900-AI-Finance-Applications/blob/main/labs/lab-17/asof_app.py)  
**GitHub Direct README Link:** [`README.md` on GitHub](https://github.com/Dapize-Mo/FIN43900-AI-Finance-Applications/blob/main/labs/lab-17/README.md)  
**GitHub Direct Checkout Link:** [`checkout.md` on GitHub](https://github.com/Dapize-Mo/FIN43900-AI-Finance-Applications/blob/main/labs/lab-17/checkout.md)  

---

## 📌 1. Executive Summary & Core Question (D)

> **Core Question (D):**  
> *Was each number in your series knowable on the day you would have traded on it — and may Project 2 use it?*

In quantitative portfolio management, machine learning models, and rule-based investment strategies, backtests routinely exhibit inflated returns and understated volatility due to **temporal contamination** (look-ahead bias). Analysts frequently download "historical" data files that silently embed subsequent releases, revisions, and restatements mapped retrospectively to the reference event date. A trading rule backtested on such data assumes market participants possessed omniscience.

In Lab 16, we constructed a standard-library provenance gate on a synthetic 12-row dataset to master the four rules of point-in-time admission (quarantining unauthenticated tickers, eliminating duplicates, filtering post-dated releases, and selecting the latest valid revision). In **Lab 17**, we scale this governance framework to live production data by building [`asof_app.py`](asof_app.py)—an interactive, FRED-style rates application powered by Streamlit that retrieves live observations from both **FRED** (Federal Reserve Economic Data, modern vintage) and **ALFRED** (ArchivaL Federal Reserve Economic Data, point-in-time vintage as of any user-selected historical date).

### Key Empirical Findings:
1. **Known Answer Reproduction:** Evaluated on the official benchmark vintage of **5 October 2026**, our app autonomously reproduces all four official course known answers:
   - `BAA`: Last known = September 2026 | Value = **6.47**
   - `FEDFUNDS`: Last known = September 2026 | Value = **3.75**
   - `DGS10`: Last known = 2 October 2026 | Value = **5.28**
   - `MORTGAGE30US`: Last known = 1 October 2026 | Value = **7.28**
2. **The Revision Probe (`PAYEMS`):** Audited on **15 January 2025**, the December 2024 nonfarm payrolls print read **159,536** thousand jobs as known then. In today's FRED vintage, that same observation has been revised downward to **158,316** thousand, with **381** total historical monthly prints revised across the series. This rigorously validates that the app queries distinct historical vintages rather than reading modern data twice.
3. **Student Chosen Series (`CPIAUCSL`):** For our Project 2 macroeconomic inflation driver, evaluating vintage **30 September 2026** confirms that the September 2026 CPI observation (336.298) did not exist; only August 2026 (334.131) was knowable. Furthermore, probing vintage **15 January 2024** against today proves that **60 historical months** were subsequently revised due to the Bureau of Labor Statistics' (BLS) annual 5-year seasonal factor re-estimation.
4. **Fiduciary Disposition:** We issue an explicit **QUARANTINE** on `CPIAUCSL` for Project 2. It may be admitted only under a point-in-time API query architecture (`as_of_date = decision_date`) or by substituting the unrevised non-seasonally adjusted index (`CPIAUCNS`).

---

## 2. Data Representation & Dual-Timestamp Architecture (R)

### A. FRED vs. ALFRED Architecture

Financial and macroeconomic data cannot be treated as scalar time series $(t, x_t)$ with a single timestamp. Robust data engineering requires a two-dimensional temporal coordinate system:

$$\text{Observation} = \mathcal{O}(t_{\text{event}}, t_{\text{pub}}, v)$$

- **Event Time ($t_{\text{event}}$):** The reference period during which the underlying economic activity occurred (e.g., month of September 2026, or trading day of October 2, 2026).
- **Publication Time ($t_{\text{pub}}$ / Vintage Date $v$):** The exact calendar timestamp when the data was compiled, verified, and transmitted into the public domain by the reporting agency.

| Source Platform | API Endpoint / CSV Pattern | Temporal Meaning | Role in Strategy Development |
| :--- | :--- | :--- | :--- |
| **FRED** | `https://fred.stlouisfed.org/graph/fredgraph.csv?id=SERIES` | Modern "finalized" series ($v = \text{today}$) | Current monitoring, reporting, unconstrained analysis |
| **ALFRED** | `https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=SERIES&vintage_date=YYYY-MM-DD` | Point-in-time vintage as known on $v$ ($t_{\text{pub}} \le v$) | **Mandatory** for backtesting, strategy validation, and ML training |

### B. Core Course Series

| Series ID | Official Name & Coverage | Frequency | Source Agency | Typical Publication Lag | Revision Behavior |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **`BAA`** | Moody's Baa Corporate Bond Yield | Monthly | Moody's Investors Service | 1–3 business days after month-end | Virtually none (market yield aggregation) |
| **`FEDFUNDS`** | Effective Federal Funds Rate | Monthly | Federal Reserve Board | 1 business day after month-end | Virtually none (volume-weighted transaction average) |
| **`DGS10`** | 10-Year Treasury Constant Maturity Yield | Daily | Federal Reserve Board | Next business day ($t+1$) | None (market constant maturity yield) |
| **`MORTGAGE30US`** | 30-Year Fixed Rate Mortgage Average | Weekly | Freddie Mac | Every Thursday morning | Rare (survey methodology) |
| **`PAYEMS`** *(Probe)* | Total Nonfarm Payroll Employment | Monthly | Bureau of Labor Statistics | First Friday of following month | **Extreme** (revised monthly for 2 months, annually in benchmark) |
| **`CPIAUCSL`** *(Ours)* | Consumer Price Index for All Urban Consumers: All Items | Monthly | Bureau of Labor Statistics | 10–15 days after month-end | **Material** (seasonal adjustment factors revised annually for 5 years) |

---

## 3. App Implementation & Architecture (I)

The Streamlit web application [`asof_app.py`](asof_app.py) was built from first principles to deliver a responsive, production-ready interface matching FRED design conventions.

### A. Technical Specifications Met
1. **Public CSV Endpoints:** Direct HTTP requests using Python's standard `urllib.request` library without requiring third-party API keys or credentials.
2. **High-Performance Caching:** Both `download_fred_series` and `download_alfred_series` are decorated with `@st.cache_data(ttl=3600)`, ensuring repeated runs and UI adjustments execute instantly without re-querying the St. Louis Fed servers.
3. **Missing Value Sanitization:** Replaces string `.` characters (FRED's representation of market holidays or missing data days) with `np.nan`, co-erces data types to numeric floats, and drops invalid rows.
4. **Interactive Sidebar:**
   - Multi-select preloaded with all four default series (`BAA`, `FEDFUNDS`, `DGS10`, `MORTGAGE30US`).
   - Free-form text input allowing users to enter custom series IDs (e.g., `CPIAUCSL`, `PAYEMS`, `UNRATE`).
   - Start Date selector defaulting to `2020-01-01`.
   - "As known on" Vintage Date selector defaulting to `today` (`2026-10-29`).
5. **Mandated Header & Disclaimer:**
   - Prominently displays:  
     `*data from FRED and ALFRED, Federal Reserve Bank of St. Louis, downloaded today; built with AI help, a learning demonstration, not investment advice.*`
6. **Visualization Suite:**
   - Renders individual interactive line charts for each selected series spanning `start_date` to today.
   - Embeds a clear caption directly underneath each chart detailing the exact observation date and value known on the vintage date versus today's modern print.
7. **Audit & Revision Ledger Table:**
   - Displays all required columns: Series ID (hyperlinked to FRED), Last Date Known Then, Value Known Then, Last Date Measured Today, Value Today, Late Observations Count (lag), and Revised Observations Count (revisions on identical dates).
8. **Fault-Tolerant Error Handling:**
   - If an invalid or unauthenticated series ID is entered, the app catches the `HTTPError 404` or parsing error, displays an isolated warning for that specific series, and renders all remaining valid series uninterrupted.

### B. Application Deployment & Execution
- **Live Streamlit Community Cloud Application:** [FRED/ALFRED Point-in-Time Rates App · Streamlit](https://fin43900-ai-finance-applications-wmi2hv4j245qhhgeuktnpc.streamlit.app/)
- **Local Run Command:**
```powershell
streamlit run labs/lab-17/asof_app.py
```
*(Or when operating within the `.venv` virtual environment:)*
```powershell
& "c:\Users\dolan\Code\school\Fall-2026\FIN-43900\workspace\.venv\Scripts\streamlit.exe" run labs/lab-17/asof_app.py
```

---

## 4. Verification & Known-Answer Proof (V)

### A. The 5 October 2026 Official Known Answer
Setting the **"As known on" Date** to **`2026-10-05`** in the application yields the following ledger:

| Series ID | FRED Link | Last Date Known on 5 Oct 2026 | Value Known on 5 Oct 2026 | Last Date Measured Today (29 Oct 2026) | Value Measured Today | Late Observations (Lag) | Revised Observations | Reconciled? |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **`BAA`** | [BAA](https://fred.stlouisfed.org/series/BAA) | **2026-09-01** (September) | **6.47** | 2026-09-01 | 6.47 | 0 | 0 | **EXACT MATCH** |
| **`FEDFUNDS`** | [FEDFUNDS](https://fred.stlouisfed.org/series/FEDFUNDS) | **2026-09-01** (September) | **3.75** | 2026-09-01 | 3.75 | 0 | 0 | **EXACT MATCH** |
| **`DGS10`** | [DGS10](https://fred.stlouisfed.org/series/DGS10) | **2026-10-02** | **5.28** | 2026-10-27 | 4.99 | 16 | 0 | **EXACT MATCH** |
| **`MORTGAGE30US`** | [MORTGAGE30US](https://fred.stlouisfed.org/series/MORTGAGE30US) | **2026-10-01** | **7.28** | 2026-10-29 | 7.24 | 4 | 0 | **EXACT MATCH** |

#### Analytical Verification:
- **`BAA` & `FEDFUNDS`:** On October 5, 2026, September 2026 was complete, and both monthly releases had been published (values: 6.47% and 3.75%). Because October 2026 is still in progress as of October 29, no additional monthly prints exist (`Late = 0`). Neither series has undergone revision (`Revised = 0`).
- **`DGS10`:** On October 5, 2026, the latest trading day published by the Fed was Friday, October 2, 2026 (yield: 5.28%). By October 29, market trading advanced through October 27, yielding 16 new trading day observations (`Late = 16`). Daily Treasury yields are final and unrevised (`Revised = 0`).
- **`MORTGAGE30US`:** Freddie Mac publishes weekly mortgage rates on Thursday mornings. October 1, 2026 was the latest Thursday release prior to October 5 (rate: 7.28%). Today's vintage includes four subsequent Thursday releases (October 8, 15, 22, and 29), yielding `Late = 4` and `Revised = 0`.

---

### B. The PAYEMS Revision Probe (15 January 2025)
To rigorously verify that the application communicates with ALFRED's historical archives and does not simply read modern data twice, we probe the Total Nonfarm Payroll Employment series (`PAYEMS`) as of **15 January 2025**:

| Metric Dimension | Vintage as of 15 January 2025 | Today's Vintage (29 October 2026) | Empirical Discrepancy / Significance |
| :--- | :---: | :---: | :--- |
| **Last Observation Date Known** | **2024-12-01** (December 2024) | 2026-09-01 (September 2026) | Today includes 21 additional months of employment prints |
| **December 2024 Value** | **159,536** thousand | **158,316** thousand | Modern data is **1,220,000 jobs lower** than reported on 15 Jan 2025 |
| **Late Observations Count** | — | **21 months** | Identifies the extensive subsequent release history |
| **Revised Observations Count** | — | **381 months** | Over 31 years of historical employment prints were restated |

#### Probe Conclusion:
The revised count of **381** is dramatically greater than zero. On January 15, 2025, the BLS's preliminary December 2024 print indicated an economy adding robust employment (159.536M). Modern benchmark revisions erased over 1.2 million of those jobs from the historical record. A backtest running on modern data would evaluate market conditions using economic strength metrics that no market participant observed during January 2025.

---

## 5. Student Chosen Series Deep Dive: CPIAUCSL (E)

### A. Context & Role in Project 2
For our Project 2 Investment Management universe (`BIL`, `IEF`, `LQD`, `VT`) and target equity `PEP`, inflation is the single most critical macroeconomic state variable:
- **Treasuries (`IEF`):** Rising inflation erodes fixed coupon purchasing power and forces duration repricing.
- **Credit (`LQD`):** Elevated inflation compresses corporate operating margins and widens credit default spreads.
- **Cash Reserve (`BIL`):** Inflation drives Federal Reserve monetary policy, dictating the risk-free reserve yield.
- **Global Equities (`VT` / `PEP`):** Determines cost-of-goods-sold pressure (agricultural inputs, packaging) and dictates the equity cost of capital ($r_{\text{equity}}$).

### B. The Formal Data Card: `CPIAUCSL`

| Field | Formal Specification & Verification |
| :--- | :--- |
| **Series ID** | **`CPIAUCSL`** |
| **Series Name** | Consumer Price Index for All Urban Consumers: All Items |
| **Source Agency** | U.S. Bureau of Labor Statistics (BLS) |
| **Official FRED Link** | [fred.stlouisfed.org/series/CPIAUCSL](https://fred.stlouisfed.org/series/CPIAUCSL) |
| **Official ALFRED Link** | [alfred.stlouisfed.org/series?id=CPIAUCSL](https://alfred.stlouisfed.org/series?id=CPIAUCSL) |
| **Economic Measure** | Measures the average monthly change in prices paid by urban consumers for a market basket of consumer goods and services (headline U.S. consumer price inflation). |
| **Units & Scale** | Index $1982-1984 = 100$, Monthly, Seasonally Adjusted (`SA`). |
| **Publication Lag** | Published approximately **10 to 15 calendar days following the close of the reference month** (e.g., September CPI is published mid-October). A trade on month-end $M$ cannot observe month $M$'s index print. |
| **Revision Policy** | **Subject to significant retroactive revisions.** While raw unadjusted prices (`CPIAUCNS`) are unrevised, seasonally adjusted CPI (`CPIAUCSL`) undergoes annual recalculation of seasonal adjustment factors every February, recalculating the preceding **five full calendar years (60 months)**. |
| **Download Date** | October 29, 2026 (Live ALFRED/FRED Public CSV pull). |

#### Hand-Verified Observations (Direct from FRED Page):
1. **2026-09-01:** **`336.298`** (Published October 13, 2026)
2. **2026-08-01:** **`334.131`** (Published September 11, 2026)
3. **2026-07-01:** **`332.813`** (Published August 14, 2026)

---

### C. Empirical Point-in-Time Audits of `CPIAUCSL`

#### Audit 1: End of Last Month (`vintage_date = 2026-09-30`)
- **Last Observation Date Known:** **`2026-08-01`** (August 2026)
- **Value Known Then:** **`334.131`**
- **Last Observation Date Measured Today:** **`2026-09-01`** (September 2026)
- **Value Measured Today:** **`336.298`**
- **Late Observations (Lag):** **`1`** (The September 2026 print was published in mid-October)
- **Revised Observations:** **`0`**

*Empirical Finding:* On September 30, 2026, an asset allocation model rebalancing the Meridian Foundation Reserve could **not** know September's inflation figure. The latest knowable print was August 2026. Conditioning a September 30 rebalance on September CPI represents an unadulterated look-ahead leak of **2.167 index points (+0.65%)**.

#### Audit 2: Historical Seasonal Revision Audit (`vintage_date = 2024-01-15`)
- Auditing the January 15, 2024 vintage against today's modern FRED series reveals:
  - Total historical monthly prints revised: **`60`**
  - Observations spanning from 2019 through 2023 were retroactively modified by the BLS in February 2024 and February 2025 during annual seasonal factor updates.

---

## 6. Code Walkthrough & Line-by-Line Explanation

During the peer code walkthrough, we analyzed the point-in-time extraction engine in `asof_app.py`:

```python
@st.cache_data(ttl=3600, show_spinner=False)
def download_alfred_series(series_id: str, vintage_date: str) -> pd.DataFrame:
    # Line 1: Construct the St. Louis Fed ALFRED public CSV endpoint with series ID and vintage date parameters
    url = f"https://alfred.stlouisfed.org/graph/alfredgraph.csv?id={series_id}&vintage_date={vintage_date}"
    
    # Line 2: Package the request with a standard browser User-Agent header to prevent automated scraping blocks
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
    
    # Line 3: Execute the HTTP request with a 10-second timeout, trapping HTTPError 404 for unknown series
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            content = resp.read().decode("utf-8")
    except urllib.error.HTTPError as e:
        raise ValueError(f"Series ID '{series_id}' with vintage '{vintage_date}' not found on ALFRED (HTTP {e.code}: {e.reason}).") from e
    except urllib.error.URLError as e:
        raise ConnectionError(f"Network error accessing ALFRED for '{series_id}': {e.reason}") from e

    # Line 4: Check if ALFRED returned an HTML error boundary rather than structured tabular CSV data
    if "<!DOCTYPE" in content or "<html" in content.lower():
        raise ValueError(f"ALFRED returned an invalid response for series ID '{series_id}' with vintage '{vintage_date}'.")

    # Line 5: Stream the decoded CSV string into an in-memory Pandas DataFrame
    df = pd.read_csv(io.StringIO(content))
    if df.empty or len(df.columns) < 2:
        raise ValueError(f"No valid data columns found in ALFRED for series ID '{series_id}'.")

    # Line 6: Sanitize FRED's '.' missing day characters to NaN and coerce to numeric floats
    val_col = df.columns[1]
    df[val_col] = pd.to_numeric(df[val_col].astype(str).str.strip().replace(".", np.nan), errors="coerce")
    
    # Line 7: Parse ISO date strings to datetime objects and sort chronologically
    df["observation_date"] = pd.to_datetime(df["observation_date"])
    df = df.dropna(subset=[val_col]).rename(columns={val_col: "vintage_value"}).sort_values("observation_date").reset_index(drop=True)
    
    # Line 8: Return the sanitized, point-in-time DataFrame
    return df
```

### Partner Code Walkthrough Exchange
- **Question Posed by Partner (J. Maffei):** *"Why does the function use `val_col = df.columns[1]` instead of hardcoding `series_id` as the column name?"*
- **My Answer:** *"Because when ALFRED downloads a vintage CSV, the column header dynamically appends the vintage date (e.g., `CPIAUCSL_20240115` instead of `CPIAUCSL`). Referencing `df.columns[1]` dynamically extracts whatever vintage-suffixed identifier ALFRED provides without brittle string formatting, allowing the function to generalize to any FRED series."*

---

## 7. Partner Attack & Empirical Defense

### Partner Attack (J. Maffei):
> *"You claim in your data card that `CPIAUCSL` is an acceptable macroeconomic indicator, but you also show that 60 prior months were retroactively altered by the BLS. In an asset allocation mandate like Meridian Foundation, how can you trust a series whose historical numbers shift beneath your feet every February?"*

### Empirical Rebuttal (Two Sentences with Evidence):
> *"While headline `CPIAUCSL` does experience annual seasonal factor revisions spanning five years—as proven by our app revealing 60 revised prints between the January 2024 vintage and today—this revision risk is completely neutralized by enforcing an as-of query architecture that ingests only the specific vintage available on each historical rebalance date. Furthermore, if a strategy cannot tolerate seasonal adjustments, the unadjusted index `CPIAUCNS` can be admitted as a zero-revision alternative that provides identical long-term purchasing power tracking without retroactive modification."*

---

## 8. The Fiduciary Call for Project 2

### Official Disposition: **QUARANTINE**

```
================================================================================
PROJECT 2 FIDUCIARY ADMISSION STATUS: QUARANTINE
Target Series: CPIAUCSL (Consumer Price Index for All Urban Consumers: All Items)
Mandate: Meridian Foundation Reserve ($100M Reserve Allocation: BIL, IEF, LQD, VT)
================================================================================
```

### Fiduciary Rationale:
1. **Publication Lag:** `CPIAUCSL` is published 10 to 15 days after the calendar month closes. Any backtest rebalancing monthly on the last trading day that feeds the current month's CPI into its risk model is guilty of severe look-ahead bias.
2. **Seasonal Revisions:** The BLS retroactively re-estimates seasonal factors across 60 historical months each February. Modern downloaded files contain smoothed historical trends that were physically unknowable to a portfolio manager in past years.

### The Explicit Operational As-Of Rule:
To utilize `CPIAUCSL` in Project 2, the pipeline must enforce:
$$\text{Information Set}(\tau) = \left\{ \mathcal{O}(t_{\text{event}}, t_{\text{pub}}, v) \;\middle|\; t_{\text{pub}} \le \tau \quad \text{and} \quad t_{\text{event}} \le \tau - 14\text{ days} \right\}$$
Every rebalance execution on date $\tau$ must dynamically request ALFRED vintage `vintage_date = tau`. The feature pipeline must lag inflation observations by at least $t-1$ month (or 15 days). Modern static CSV downloads are strictly prohibited in the backtest harness.

### Condition to Admit:
Admit to active Project 2 backtesting and live paper trading **only if**:
1. The backtest harness queries point-in-time ALFRED vintages per rebalancing period, OR
2. The portfolio manager switches the inflation input to **`CPIAUCNS`** (Consumer Price Index for All Urban Consumers: Not Seasonally Adjusted), which is unrevised once published and eliminates revision bias entirely.

---

## 9. Data Card — Learn on Your Own & Reflection

### 1. What is a Data Card?
A data card is a formal, standardized provenance and specification document that defines the operational characteristics of an incoming dataset before it is admitted to an algorithmic model or trading pipeline. Analogous to an engineering specification sheet or a nutrition facts label, it catalogs the asset's origin, collection methodology, reference frequency, publication timestamps, reporting delays, licensing constraints, revision policies, and empirical validation points.

### 2. How Does It Work — Which Fields Stop a Leak Before It Starts?
- **The Publication Lag Field:** Establishes the exact temporal barrier between economic occurrence and public dissemination. It explicitly prevents look-ahead leaks by forbidding an algorithm from conditioning capital decisions on month $M$'s performance until date $M + \text{Lag}$.
- **The Revision Policy Field:** Flags whether historical observations are volatile and subject to restatement (such as GDP, nonfarm payrolls, and seasonally adjusted inflation). By documenting the frequency and depth of revisions, it stops modelers from training on finalized modern data and forces the implementation of point-in-time vintage architectures.
- **The As-Of Vintage Anchor:** Explicitly binds every row to its publication timestamp, ensuring that historical backtests replicate the exact information universe available at the moment of execution.

### 3. Why "Cleaned the Data" is Not a Data Card
Stating that an analyst "cleaned the data" is an opaque, subjective, and unverifiable claim that conceals critical assumptions. "Cleaning" often acts as a euphemism for deleting inconvenient outliers, silently forward-filling missing rows across non-trading periods, or swallowing post-dated revisions that inject future alpha. A data card is transparent, audit-ready, and reproducible: it does not claim the data was "cleaned"; rather, it defines the mathematical rules of admission, quantifies the exact publication delay, specifies the source URL, and provides hand-verified primary benchmarks that any independent auditor can replicate.

### 4. Reflection: Publication Lag and Backtest Distortion
- **Publication Lag of `CPIAUCSL`:** The series is published mid-month (10–15 days post month-end). On September 30, 2026, our app demonstrated that the September print of 336.298 did not exist on ALFRED; the latest knowable print was August (334.131).
- **What a Naive Backtest Would Have Overstated:**
  A naive backtest running on modern FRED data would assume that on September 30, the portfolio manager knew inflation was surging to 336.298. The algorithm would preemptively dump long-duration Treasuries (`IEF`) and credit (`LQD`) to hide in cash (`BIL`), perfectly capturing the yield curve repricing. In real life, on September 30, the manager had no such information, would have held duration through the inflation release, and would have incurred full market drawdowns. Furthermore, using today's smoothed seasonal factors for 2019–2024 erases historical inflation volatility, falsely boosting the strategy's backtested Sharpe ratio and giving the investment committee a dangerously fraudulent impression of portfolio stability.

---

## 10. Conclusion & Attestation

All empirical figures in this document were compiled through direct API execution against live FRED and ALFRED repositories. All known answers and probes have been reproduced to exact precision.

- **Student Attestation:** I, **Oladapo Olaniyan**, affirm that this checkout deliverable and the accompanying application [`asof_app.py`](asof_app.py) represent my own individual intellectual and programming work completed during the in-person class session on October 29, 2026, in collaboration with peer partner J. Maffei.
