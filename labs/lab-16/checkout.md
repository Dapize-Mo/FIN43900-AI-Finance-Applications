# FIN 43900 Lab 16 — Provenance Gate: Point-in-Time Admission

**Course:** FIN 43900 — AI Finance Applications, Purdue University  
**Student Analyst:** **Oladapo Olaniyan** (`oolaniy@purdue.edu`)  
**Teammate / Learning Partner:** **J. Maffei** (`maffeij@purdue.edu` | Target Company: Oracle Corp. — `ORCL`)  
**Institution:** Mitchell E. Daniels, Jr. School of Business, Purdue University  
**Case:** Fictional Card-Spend Retail Index (Retailers `AAA`, `BBB`, `CCC`)  
**Lab Date:** October 27, 2026  
**Brightspace Item:** Lab 16 — Provenance Gate (Tuesday Authenticated Completion Checkout, 25 Points)  
**Session Token:** `bond`  
**GitHub Direct Script Link:** [asof.py on GitHub](https://github.com/Dapize-Mo/FIN43900-AI-Finance-Applications/blob/main/labs/lab-16/asof.py)  
**GitHub Direct README Link:** [README.md on GitHub](https://github.com/Dapize-Mo/FIN43900-AI-Finance-Applications/blob/main/labs/lab-16/README.md)  
**GitHub Direct Checkout Link:** [checkout.md on GitHub](https://github.com/Dapize-Mo/FIN43900-AI-Finance-Applications/blob/main/labs/lab-16/checkout.md)  

---

## 📌 1. Executive Summary & Core Question (D)

> **Core Question (D):**  
> *On the day you would have traded, what did this data actually say — and how much of what you see now came later?*

In quantitative finance and AI-driven portfolio management, backtest results are routinely invalidated by **temporal contamination**, commonly known as **look-ahead bias**. Data vendors frequently deliver historical files that include subsequent revisions, restatements, and post-dated releases mapped retroactively to the measurement period. A model trained or backtested on this "point-in-the-future" data executes trades using information that no human or machine could have possessed on the historical trading date.

This lab constructs a strict, standard-library **provenance gate** ([`asof.py`](asof.py)) that enforces point-in-time data admission. Evaluated on a training dataset of card-spend indices for three retail tickers (`AAA`, `BBB`, `CCC`) under an active trading decision date of **31 March 2026**, our filter:
1. Reconstructs the exact information set available to a portfolio manager on March 31, 2026.
2. Eliminates unidentifiable records (`Row 11`), exact duplicate transmissions (`Row 7`), post-dated releases (`Rows 3, 8, 10`), and superseded vintage releases (`Row 2`).
3. Computes the genuine **As-Of signal** and benchmarks it against a **Naive signal** (which naively swallows latest publications regardless of date).
4. Demonstrates that for ticker `AAA`, the naive signal falsely claims a **+5.83%** growth signal (based on March card spend published April 10), whereas the true knowable signal was only **+1.98%** (February card spend revised March 25). The difference—**+3.85 percentage points**—represents an invisible "leak" of future information that would corrupt capital allocation.

---

## 2. Temporal Architecture & Representation (R)

### A. The Core Temporal Distinction: Event Time vs. Publication Time

Every economic and financial observation possesses two fundamentally distinct timestamps:
- **Month Measured (Event Time / Reference Period):** The historical window during which the underlying economic activity transpired (e.g., consumer credit card transactions occurring during January or February 2026).
- **Published On (Publication Time / Knowledge Horizon):** The exact calendar day when the metric was compiled, audited, and made publicly accessible to market participants (e.g., February 10, March 10, March 25).

A trade executed on **31 March 2026** can legally and physically condition its allocation **only** on records whose `Published On` date is $\le \text{2026-03-31}$.

### B. The Raw Training Dataset

The raw dataset contains 12 transmission rows covering three retail companies:

| Row | Ticker | Month Measured | Published On | Index Value | Anomaly / Vintage Context |
| :---: | :---: | :---: | :---: | :---: | :--- |
| **1** | `AAA` | 2026-01 | 2026-02-10 | 101.0 | Initial release for Jan 2026 |
| **2** | `AAA` | 2026-02 | 2026-03-10 | 104.0 | Initial release for Feb 2026 |
| **3** | `AAA` | 2026-03 | 2026-04-10 | 109.0 | March data published in April (Post-Decision Date) |
| **4** | `AAA` | 2026-02 | 2026-03-25 | 103.0 | Upward revision of Feb 2026 published before March 31 |
| **5** | `BBB` | 2026-01 | 2026-02-10 | 98.0 | Initial release for Jan 2026 |
| **6** | `BBB` | 2026-02 | 2026-03-10 | 97.0 | Initial release for Feb 2026 |
| **7** | `BBB` | 2026-02 | 2026-03-10 | 97.0 | Exact duplicate transmission of Row 6 |
| **8** | `BBB` | 2026-03 | 2026-04-10 | 92.0 | March data published in April (Post-Decision Date) |
| **9** | `CCC` | 2026-01 | 2026-02-10 | 110.0 | Initial release for Jan 2026 |
| **10** | `CCC` | 2026-02 | 2026-04-05 | 112.0 | Late revision of Feb 2026 published April 5 (Post-Decision Date) |
| **11** | *(Empty)* | 2026-02 | 2026-03-10 | 99.0 | Missing ticker / Unidentified corporate issuer |
| **12** | `CCC` | 2026-02 | 2026-03-10 | 111.0 | Initial release for Feb 2026 |

---

## 3. Order of Operations & Filter Implementation (I)

The provenance gate must execute its filtering rules in an exact, deterministic order. Deviating from this order changes the output universe and produces mathematical errors.

### The Four Rules (in Strict Sequence):

1. **Rule 1: Quarantine Rows with No Ticker:**  
   *Operational Logic:* Any record lacking an authenticated ticker identity cannot be safely mapped to a portfolio asset. It is quarantined immediately to prevent cross-contamination.  
   *Result:* Removes `Row 11` (empty ticker string).

2. **Rule 2: Remove Exact Duplicates:**  
   *Operational Logic:* Multiple transmissions containing the exact same `(ticker, month_measured, published_on, index)` represent database ping duplicates or communication re-transmissions.  
   *Result:* Removes `Row 7` (an exact duplicate of `Row 6` for BBB).

3. **Rule 3: Remove Rows Published After the Decision Date:**  
   *Operational Logic:* The decision date is **31 March 2026**. Any record with `published_on > 2026-03-31` represents future information unavailable on the trading desk.  
   *Result:* Removes `Row 3` (AAA March, pub 2026-04-10), `Row 8` (BBB March, pub 2026-04-10), and `Row 10` (CCC Feb revision, pub 2026-04-05).

4. **Rule 4: Retain the Latest Revision Published by the Decision Date:**  
   *Operational Logic:* Where a single ticker and measurement month has multiple published vintages surviving Rules 1–3, the portfolio manager must trade on the most recently updated knowledge. Older vintages are superseded and discarded.  
   *Result:* For `(AAA, 2026-02)`, `Row 2` (published March 10, index 104.0) is superseded by `Row 4` (published March 25, index 103.0). `Row 2` is removed.

```python
# Code snippet from asof.py illustrating Rule 4 grouping and vintage pruning:
groups = {}
for r in after_r3:
    key = (r["ticker"], r["month_measured"])
    if key not in groups:
        groups[key] = []
    groups[key].append(r)

r4_removed = []
after_r4 = []
for key, rows in groups.items():
    if len(rows) == 1:
        after_r4.append(rows[0])
    else:
        # Sort chronologically by published_on; tie-break by row number
        sorted_vintages = sorted(rows, key=lambda x: (x["published_on"], x["row"]))
        latest_vintage = sorted_vintages[-1]
        for older_vintage in sorted_vintages[:-1]:
            r4_removed.append(older_vintage["row"])
        after_r4.append(latest_vintage)
```

---

## 4. Verification & Known-Answer Proof (V)

### A. The Authenticated Row Funnel

The execution of `asof.py` outputs the exact funnel required by the course specification:

| Funnel Step | Rule Purpose | Rows Removed | Count | Surviving Row IDs |
| :--- | :--- | :---: | :---: | :--- |
| **Initial Input** | Raw input table | — | 12 | 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12 |
| **Rule 1** | Quarantined: no ticker | **`11`** | 1 | 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12 |
| **Rule 2** | Exact duplicate (BBB 2026-02) | **`7`** | 1 | 1, 2, 3, 4, 5, 6, 8, 9, 10, 12 |
| **Rule 3** | Published after 31 March 2026 | **`3, 8, 10`** | 3 | 1, 2, 4, 5, 6, 9, 12 |
| **Rule 4** | Older vintage replaced by revision | **`2`** | 1 | **1, 4, 5, 6, 9, 12** |
| **As-of Panel** | **Final Knowable Universe** | — | **6** | **`[1, 4, 5, 6, 9, 12]`** |

### B. Surviving As-Of Panel

| Row | Ticker | Month Measured | Published On | Index Value | Vintage Status on 31 March 2026 |
| :---: | :---: | :---: | :---: | :---: | :--- |
| **1** | `AAA` | 2026-01 | 2026-02-10 | 101.00 | Initial release (knowable baseline) |
| **4** | `AAA` | 2026-02 | 2026-03-25 | 103.00 | Valid revision (superseded Row 2 prior to decision date) |
| **5** | `BBB` | 2026-01 | 2026-02-10 | 98.00 | Initial release (knowable baseline) |
| **6** | `BBB` | 2026-02 | 2026-03-10 | 97.00 | Initial release (knowable observation) |
| **9** | `CCC` | 2026-01 | 2026-02-10 | 110.00 | Initial release (knowable baseline) |
| **12** | `CCC` | 2026-02 | 2026-03-10 | 111.00 | Initial release (Row 10 revision unknowable until April 5) |

---

## 5. Signal Derivation: "The Digits, Once"

Signal definition:
$$\text{Signal} = \left(\frac{\text{Index}_{\text{latest knowable month}}}{\text{Index}_{\text{previous month}}} - 1\right) \times 100$$

### 1. Ticker `AAA`:
- **As-Of Information Set:** Previous month = Jan (`101.0`), Latest month = Feb revised (`103.0`).
  $$\text{Signal}_{\text{as-of}} = \frac{103.0}{101.0} - 1 = \frac{2.0}{101.0} = +0.019802 \to \mathbf{+1.98\% \text{ (February)}}$$
- **Naive Information Set:** Uses March index (`109.0`, published April 10) over Feb revised (`103.0`).
  $$\text{Signal}_{\text{naive}} = \frac{109.0}{103.0} - 1 = \frac{6.0}{103.0} = +0.058252 \to \mathbf{+5.83\% \text{ (March)}}$$
- **The Look-Ahead Leak:** $+5.83\% - (+1.98\%) = \mathbf{+3.85 \text{ percentage points}}$.
- *Crucial Error Check:* If an algorithm failed to apply Rule 4 and kept `Row 2` (`104.0`), AAA's as-of signal would compute to $\frac{104.0}{101.0} - 1 = +2.97\%$. Our code correctly yields **`+1.98%`**.

### 2. Ticker `BBB`:
- **As-Of Information Set:** Previous month = Jan (`98.0`), Latest month = Feb (`97.0`).
  $$\text{Signal}_{\text{as-of}} = \frac{97.0}{98.0} - 1 = \frac{-1.0}{98.0} = -0.010204 \to \mathbf{-1.02\% \text{ (February)}}$$
- **Naive Information Set:** Uses March index (`92.0`, published April 10) over Feb (`97.0`).
  $$\text{Signal}_{\text{naive}} = \frac{92.0}{97.0} - 1 = \frac{-5.0}{97.0} = -0.051546 \to \mathbf{-5.15\% \text{ (March)}}$$
- **The Look-Ahead Leak:** $-5.15\% - (-1.02\%) = \mathbf{-4.13 \text{ percentage points}}$ (severe hidden deterioration unseen on March 31).

### 3. Ticker `CCC`:
- **As-Of Information Set:** Previous month = Jan (`110.0`), Latest month = Feb (`111.0` from Row 12; Row 10 was published April 5).
  $$\text{Signal}_{\text{as-of}} = \frac{111.0}{110.0} - 1 = \frac{1.0}{110.0} = +0.009091 \to \mathbf{+0.91\% \text{ (February)}}$$
- **Naive Information Set:** No March observation exists, but naive replaces Feb index `111.0` with April revision `112.0` (Row 10).
  $$\text{Signal}_{\text{naive}} = \frac{112.0}{110.0} - 1 = \frac{2.0}{110.0} = +0.018182 \to \mathbf{+1.82\% \text{ (February, revised)}}$$
- **The Look-Ahead Leak:** $+1.82\% - (+0.91\%) = \mathbf{+0.91 \text{ percentage points}}$ of revision contamination.

---

## 6. Code Walkthrough & Partner Break Attack

### A. Line-by-Line Code Explanation (Rule 4)

During peer code walkthrough with partner J. Maffei, we examined the revision tracking engine in `asof.py`:
1. `groups = {}`: Constructs an associative hash table keyed by tuple `(ticker, month_measured)`. This clusters all surviving vintage publications for a specific asset and economic period.
2. `sorted_vintages = sorted(rows, key=lambda x: (x["published_on"], x["row"]))`: Lexicographically orders vintages by publication date, ensuring the latest legal release appears at index `[-1]`.
3. `for older_vintage in sorted_vintages[:-1]: r4_removed.append(older_vintage["row"])`: Explicitly logs superseded vintages to the removal funnel rather than silently dropping them. This maintains full auditability.

### B. Partner Quiz Exchange

- **Question Posed by Partner (J. Maffei):** *"Why does CCC have Row 12 in the As-Of panel, but Row 10 in the Naive panel, even though Row 10 has an index value of 112.0 and measures the exact same month?"*
- **My Answer:** *"Because the provenance gate evaluates publication date before revisions (Rule 3 before Rule 4). Row 10 was published on 2026-04-05, five days after our 2026-03-31 decision date. It is legally unknowable on March 31, so Rule 3 drops it. That leaves Row 12 as the sole knowable vintage for February CCC. In the naive run, publication dates are ignored, allowing Row 10 to supersede Row 12."*

### C. Partner Swap-and-Break Test (`decision_date = 2026-04-15`)

To test the robustness of the filter, we set the decision date to **`2026-04-15`** (`python asof.py 2026-04-15`):
- **Output:**
  - Rule 3 removes **0 rows** (`[]`) because all observations in the table were published on or before April 10.
  - In Rule 4, Row 10 supersedes Row 12 for CCC, while Row 4 continues to supersede Row 2 for AAA.
  - As-of panel expands to 8 rows: `[1, 3, 4, 5, 6, 8, 9, 10]`.
  - Resulting Signals:
    * `AAA`: **+5.83% (March)**
    * `BBB`: **−5.15% (March)**
    * `CCC`: **+1.82% (February)**
  - **Deduction:** The As-Of signal becomes identical to the Naive signal ticker for ticker. The look-ahead leak collapses to exactly **0.00 points**, proving that the gap between the two columns is strictly equal to what had not yet been published on March 31.

---

## 7. Point-in-Time Learnings & Reflections

### 1. What is Look-Ahead Bias?
Look-ahead bias occurs when information from the future is inadvertently introduced into historical model estimation, feature engineering, or backtesting. In quantitative finance, it artificially boosts performance metrics (Sharpe ratio, hit rate, CAGR) because the algorithm is allowed to "predict" events using data that reflects those very outcomes. When transitioned to live capital, the strategy collapses because real-time execution can only observe historical releases.

### 2. How Does It Work Across Event Time, Publication Time, and Revisions?
- **Event Time (Lag):** Macroeconomic and retail indicators are never known instantaneously. A month's sales require weeks to aggregate and report. Assuming that March sales are known on March 31 is physically impossible.
- **Publication Time (Vintage):** The true knowledge frontier advances only on release dates.
- **Revisions:** Economic data is routinely revised (e.g., initial prints vs. final GDP/CPI releases). Using finalized modern files creates "revision bias," where backtests trade on refined figures that were unknown during the initial print.

### 3. Which Rule Removed the Row That Mattered Most?
**Rule 3 (Published after decision date)** removed the rows that mattered most (`Rows 3, 8, 10`). By eliminating Row 3 (AAA March spend of 109.0) and Row 8 (BBB March spend of 92.0), Rule 3 prevented the model from trading on momentum shifts that had not yet occurred in the public domain. Secondarily, **Rule 4** prevented the classic +2.97% error by correctly honoring the March 25 revision (`Row 4`).

### 4. What a Backtest Built on the Naive Column Would Claim
A naive backtest would claim that ticker `AAA` was experiencing an explosive retail surge (+5.83%) and allocate maximum overweight capital to AAA on March 31. In reality, on March 31, AAA's latest knowable trend was a modest +1.98%. Conversely, it would aggressively short `BBB` on March 31 due to its −5.15% drop, even though BBB's decline was completely invisible until April 10. Such a backtest produces fictitious alpha that evaporates under real market conditions.

---

## 8. Open-Ended Challenge Protocol: "The Revised Surprise"

### Scenario Context
A third-party alternative data vendor republishes last month's dataset after correcting **8% of historical records**, but supplies **only the latest revised file** (refusing or unable to supply timestamped historical vintages). An exploratory backtest on this revised file shows significant predictive power for equity returns.

### Fiduciary Protocol Specification

| Dimension | Fiduciary Requirement & Decision Rule |
| :--- | :--- |
| **1. Information Set** | The vendor file is tainted by retroactive revision bias. The 8% corrected records were modified with the benefit of hindsight. Only the original uncorrected transmissions represent the legitimate historical information set. |
| **2. Evidence Request** | Formally issue a **Data Provenance & Vintage Audit Request** to the vendor demanding point-in-time files: exact row-level `as_of_date`, `publication_timestamp`, and pre-revision historical values for all corrected records. |
| **3. Test Start** | **Quarantine all historical backtests.** Immediate cessation of retrospective strategy optimization on the revised file. Retrospective backfilling does not constitute point-in-time proof. |
| **4. Frozen Rule** | **Preregister a Prospective Test:** Freeze the signal definition, calculation code, and portfolio rebalancing rules as of today (`2026-10-27`). Ingest new vendor files prospectively in real time without allowing retroactive overwrites. |
| **5. Claim Limit** | No marketing, capital allocation, or performance claims may cite backtests constructed from the revised file. Any displayed performance must be explicitly labeled as **"Synthetic Post-Revision Backtest — Contaminated by Revision Look-Ahead"**. |
| **6. Reversal Condition** | The series may be admitted to live production **only if**: (a) The vendor provides verified historical point-in-time vintages matching the provenance gate, OR (b) A minimum of 6 months of prospective live paper trading confirms statistically significant predictive power. Otherwise: **PERMANENT REJECTION**. |

---

## 9. Conclusion & Brightspace Attestation

All calculations in [`asof.py`](asof.py) execute autonomously from first principles using Python's standard library. All outputs reconcile precisely to the official course known answers.

- **Author Attestation:** I, **Oladapo Olaniyan**, hereby certify that this checkout deliverable represents my own verified academic work completed during the in-person class session on October 27, 2026, in collaboration with peer partner J. Maffei.
