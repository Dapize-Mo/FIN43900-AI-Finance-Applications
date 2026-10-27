# Lab 16 — Provenance Gate

**Course:** FIN 43900 — AI Finance Applications, Fall 2026  
**Student / Author:** Oladapo Olaniyan (`oolaniy@purdue.edu`)  
**Teammate / Learning Partner:** J. Maffei (`maffeij@purdue.edu` | Target Company: Oracle Corp. — `ORCL`)  
**Institution:** Mitchell E. Daniels, Jr. School of Business, Purdue University  
**Case:** Fictional Card-Spend Retail Index (Retailers `AAA`, `BBB`, `CCC`)  
**Date:** October 27, 2026  
**Session Token:** `bond`  
**Category:** Tuesday Authenticated Completion Checkout (25 or 0)

---

## 📌 Controlling Instructions & Source Hierarchy

- **Course Instruction:** [Week 10 — Lab 16 Provenance Gate](https://github.com/CinderZhang/FIN43900-Fall2026/blob/main/lessons/week-10/lab-16-provenance-gate.md)
- **Session Slides:** [Session 16 Slides](https://github.com/CinderZhang/FIN43900-Fall2026/blob/main/lessons/week-10/slides-session-16.md)
- **Student Handout:** [Student Handout — Point-in-Time](https://github.com/CinderZhang/FIN43900-Fall2026/blob/main/lessons/week-10/student-handout.md)
- **Required Prework:** [ALFRED Vintage Architecture](https://github.com/CinderZhang/FIN43900-Fall2026/blob/main/lessons/week-10/student-prework.md)
- **Open-Ended Challenge:** [The Revised Surprise](https://github.com/CinderZhang/FIN43900-Fall2026/blob/main/lessons/week-10/open-ended-challenge.md)

---

## 🚀 Deliverables & Files

1. **Standard-Library Point-in-Time Engine:** [`asof.py`](asof.py)  
   Python script built using Python's standard library only. Implements the four course rules strictly in sequence:
   - Rule 1: Quarantine rows with missing ticker (`Row 11`).
   - Rule 2: Remove exact duplicate rows (`Row 7`).
   - Rule 3: Remove rows published after decision date (`Rows 3, 8, 10`).
   - Rule 4: Where multiple publications exist for a (ticker, month), keep the latest published on or before the decision date (`Row 2` replaced by revision `Row 4`).
   - Dynamic Signal Calculation: Computes as-of and naive signals, look-ahead leaks, and supports CLI dates for partner break testing (`python asof.py 2026-04-15`).
2. **Comprehensive Checkout Report:** [`checkout.md`](checkout.md)  
   Detailed analytical writeup answering all syllabus checkout dimensions: Core Question (D), Training Data & Rules (R), Filter Implementation (I), Known-Answer Proof & Row Funnel (V), Partner Code Walkthrough & Swap-and-Break, Point-in-Time Learnings & Reflection, and the Open-Ended Challenge Protocol.
3. **Brightspace Submission Block:** [`../../brightspace/lab-16_submission.txt`](../../brightspace/lab-16_submission.txt)  
   Clean, pre-formatted, easy-to-copy plain text block formatted specifically for the authenticated Brightspace checkout quiz.

---

## 🎯 Verification & Known-Answer Summary

### 1. The Row Funnel (Decision Date: 2026-03-31)

| Funnel Step | Rule Purpose | Rows Removed | Count | Surviving Row IDs |
| :--- | :--- | :---: | :---: | :--- |
| **Initial Input** | Raw input table | — | 12 | 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12 |
| **Rule 1** | Quarantined: no ticker | **`11`** | 1 | 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12 |
| **Rule 2** | Exact duplicate (BBB 2026-02 duplicate) | **`7`** | 1 | 1, 2, 3, 4, 5, 6, 8, 9, 10, 12 |
| **Rule 3** | Published after 31 March 2026 | **`3, 8, 10`** | 3 | 1, 2, 4, 5, 6, 9, 12 |
| **Rule 4** | Older vintage replaced by revision | **`2`** | 1 | **1, 4, 5, 6, 9, 12** |
| **As-of Panel** | **Final Knowable Universe** | — | **6** | **`[1, 4, 5, 6, 9, 12]`** |

*Verification Confirmation:* The output of `asof.py` reproduces the official course known-answer funnel row for row.

### 2. Signal Comparison: As-Of (Knowable) vs. Naive (Look-Ahead Leak)

| Ticker | Latest As-Of Month | As-Of Signal (Knowable) | Latest Naive Month | Naive Signal (Look-Ahead) | Look-Ahead Leak (Naive − As-Of) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **AAA** | February 2026 | **+1.98%** (`103.0 / 101.0 - 1`) | March 2026 | **+5.83%** (`109.0 / 103.0 - 1`) | **+3.85 percentage points** |
| **BBB** | February 2026 | **−1.02%** (`97.0 / 98.0 - 1`) | March 2026 | **−5.15%** (`92.0 / 97.0 - 1`) | **−4.13 percentage points** |
| **CCC** | February 2026 | **+0.91%** (`111.0 / 110.0 - 1`) | February 2026 | **+1.82%** (`112.0 / 110.0 - 1`, revised) | **+0.91 percentage points** |

*Classic Pitfall Check:* If Rule 4 had erroneously kept Row 2 (initial Feb release of 104.0) instead of Row 4 (revised Feb release of 103.0 published March 25), AAA's as-of signal would have been `104.0 / 101.0 - 1 = +2.97%`. Our engine correctly selected Row 4, yielding the authenticated known answer **`+1.98%`**.

---

## 🔬 The Digits, Once: First-Principles Trace (AAA)

For a portfolio manager trading on **31 March 2026**:
1. **Knowable Rows:**
   - January 2026: Measured index `101.0`, published `2026-02-10` (`Row 1`). Knowable on March 31.
   - February 2026 (Initial): Measured index `104.0`, published `2026-03-10` (`Row 2`). Knowable, but superseded.
   - February 2026 (Revision): Measured index `103.0`, published `2026-03-25` (`Row 4`). Knowable on March 31 and supersedes Row 2.
   - March 2026: Measured index `109.0`, published `2026-04-10` (`Row 3`). **Unknowable on March 31** (published 10 days in the future).
2. **As-Of Signal Calculation:**
   $$\text{Signal}_{\text{as-of}} = \frac{\text{Index}_{\text{Feb (revised)}}}{\text{Index}_{\text{Jan}}} - 1 = \frac{103.0}{101.0} - 1 = +1.9802\% \to \mathbf{+1.98\%}$$
3. **Naive Signal Calculation (Look-Ahead Backtest):**
   $$\text{Signal}_{\text{naive}} = \frac{\text{Index}_{\text{Mar}}}{\text{Index}_{\text{Feb (revised)}}} - 1 = \frac{109.0}{103.0} - 1 = +5.8252\% \to \mathbf{+5.83\%}$$
4. **The Look-Ahead Leak:**
   $$\text{Leak} = +5.83\% - (+1.98\%) = \mathbf{+3.85 \text{ points}}$$
   Nobody in the market had access to the March index of 109.0 on March 31. Backtests that feed on latest published files falsely attribute this 3.85-point gain to algorithmic alpha, whereas it is pure temporal contamination.

---

## 🔄 Partner Swap-and-Break Test

- **Test Action:** Execute `asof.py` with decision date advanced to **`2026-04-15`** (`python asof.py 2026-04-15`).
- **Mechanism:** On April 15, all rows published between April 1 and April 15 (Row 3 published 04-10, Row 8 published 04-10, and Row 10 published 04-05) cross the provenance gate and become legally knowable.
- **Result:**
  - Rule 3 removes **0 rows** (`[]`).
  - Rule 4 replaces Row 2 with Row 4 for AAA, and replaces Row 12 with Row 10 for CCC.
  - As-of signals become:
    * AAA: **+5.83% (March)**
    * BBB: **−5.15% (March)**
    * CCC: **+1.82% (February)**
  - **Verdict:** The As-of signal becomes identical to the Naive signal ticker for ticker. The look-ahead leak drops to exactly **0.00 percentage points**.

---

## 💻 Running the Script

```bash
# Navigate to lab directory
cd c:\Users\dolan\Code\school\Fall-2026\FIN-43900\workspace\labs\lab-16

# Run baseline as-of provenance filter (decision date = 2026-03-31)
python asof.py

# Run partner swap-and-break test (decision date = 2026-04-15)
python asof.py 2026-04-15
```
