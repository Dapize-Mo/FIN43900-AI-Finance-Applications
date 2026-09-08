# Lab 05 Checkout — Build and Validate an FCFF DCF

| Metadata | Details |
|---|---|
| **Student Analyst** | **Oladapo Olaniyan** |
| **Teammate** | `kogbuef@purdue.edu` |
| **Course** | FIN 43900 — AI Finance Applications, Purdue University |
| **Session & Date** | Week 3 · Tuesday (Lab 05) · September 8, 2026 |
| **Target Company** | PepsiCo, Inc. (NASDAQ: `PEP` \| CIK: `0000077476`) |

---

## 1. Lab Date, Teammates & Personal Contribution

* **Lab Date:** Tuesday, September 8, 2026
* **Teammate:** `kogbuef@purdue.edu`
* **Personal Contribution:**  
  Working alongside my partner (`kogbuef@purdue.edu`), I drew the 5-step DCF model architecture from memory, hand-calculated the Year 1 FCFF ($108.00M) and its present value ($98.18M at 10% WACC), implemented the 4 `STUDENT_WORK` functions in `dcf_starter.py`, reconciled all 12 synthetic checkpoints against `dcf_expected_output.csv` ($27.50/share, 72.4% TV share), added boundary validation for $g \ge \text{WACC}$, transferred our sourced PepsiCo FY2024 SEC Form 10-K inputs yielding a $140.73/share Base Case (0.98x market price), and documented our unresolved WACC cost of debt assumption.

---

## 2. Stated DCF Convention and Output Unit

* **Convention:** Annual end-of-year Free Cash Flow to Firm (FCFF) in USD Millions, 5 explicit forecast years, Gordon-growth terminal value evaluated at the end of Year 5, discounted to Year 0 using annual compounding discount factor $(1 + \text{WACC})^t$.
* **Output Unit:** USD per diluted common share ($/share).

---

## 3. Hand-Calculated Year 1 FCFF and Present Value

* **Year 1 FCFF Calculation:**  
  $$\text{FCFF}_1 = \text{FCFF}_0 \times (1 + g_1) = 100.00 \times (1 + 0.08) = \mathbf{108.00 \text{ M USD}}$$

* **Year 1 Present Value Calculation (WACC = 10%):**  
  $$\text{PV}(\text{FCFF}_1) = \frac{108.00}{(1.10)^1} = \mathbf{98.1818 \text{ M USD}} \quad (\approx \mathbf{\$98.18\text{M}})$$

---

## 4. Synthetic Case Valuation Output Checkpoints

| Output Metric | Model Value | Expected Value | Tolerance | Status |
|---|---:|---:|---:|:---:|
| **Enterprise Value (EV)** | **$1,624.87M** | $1,624.87M | 0.01 | **PASSED** |
| **Common Equity Value** | **$1,374.87M** | $1,374.87M | 0.01 | **PASSED** |
| **Value per Diluted Share** | **$27.50** | $27.50 | 0.01 | **PASSED** |
| **Terminal Value Share of EV** | **72.40%** | 72.40% | 0.0002 | **PASSED** |

---

## 5. Passed Test & Corrected Failure

> [!NOTE]
> **One Passed Test (Known-Answer & Boundary Verification):**  
> The synthetic engine reproduced all 12 output rows in `dcf_expected_output.csv` within stated numerical tolerances. Boundary testing verified that feeding $g = 10\% \ge \text{WACC} = 10\%$ successfully threw a `ValueError("Terminal growth must be strictly less than WACC")`.

> [!IMPORTANT]
> **One Corrected Failure:**  
> * **Failure:** In initial testing, `terminal_value_year_5` computed to **$1,839.46M** instead of expected **$1,894.65M**.  
> * **Diagnosis:** The Gordon Growth numerator used raw $\text{FCFF}_5$ ($128.76M$) without multiplying by $(1 + g)$ to project Year 6 cash flow.  
> * **Fix:** Updated numerator to $\text{FCFF}_5 \times (1 + g) = 128.762525 \times 1.03 = 132.625401M$.  
> * **Re-test:** Terminal value landed on **$1,894.65M**, PV of TV hit **$1,176.43M**, and per-share value returned to **$27.50**.

---

## 6. Target-Company Transferred Rows & Unresolved Assumption

### Sourced PepsiCo Inputs (SEC Form 10-K FY2024)

| Input Name | Value | Unit | SEC Locator / Basis | Classification |
|---|---|---|---|---|
| `starting_fcff` | **$9,688.59M** | USD Millions | Cash Flows (p. 63) / Income Stmt (p. 61). OCF $12,680M + Interest $771M − CapEx $5,318M + Charges $1,811M | Core Normalized Reported Fact |
| `growth_year_1..5` | **3.0%, 3.5%, 4.0%, 3.5%, 3.0%** | Decimal | Item 7 MD&A Division Review (pp. 43–47) | Labeled Forecast Path |
| `terminal_growth` | **2.50%** | Decimal | BEA / FRED Long-run US Real GDP + Inflation Target | Economic Boundary |
| `nonoperating_cash` | **$8,505.0M** | USD Millions | Balance Sheet (p. 65), Cash & Equivalents | Reported Fact |
| `debt` | **$44,306.0M** | USD Millions | Balance Sheet (p. 65), Short ($7,842M) + Long Debt ($36,464M) | Reported Fact |
| `diluted_shares` | **1,378.0M** | Million Shares | Note 10 Net Income Per Share (p. 106) | Reported Fact |

### Unresolved Assumption Note
* **Unresolved Item:** `wacc_cost_of_debt`  
* **Details:** Cost of equity is anchored at 7.30% ($R_f=4.30\%, \beta=0.60, \text{ERP}=5.00\%$) and effective tax rate is 19.4%. However, the weighted average pre-tax cost of debt across PepsiCo's multi-tranche debt structure ($44.3B) requires full debt schedule extraction from Note 8 before Thursday's Session 6 sensitivity grid.

---

## 7. AI-Use Disclosure

* **Access Paths Used:** Gemini 3.6 Flash (High) in Antigravity IDE & OpenAI Codex (ChatGPT).
* **Roles:** Codex built and refined the 4 `STUDENT_WORK` functions in `dcf_starter.py`. Gemini verified hand calculations, audited boundary checks, and cross-referenced SEC EDGAR filing locators.

---

## 8. Session Token & Declarations

* **Session Token:** `DCF-BUILD-2026`
* **In-Person Attendance Declaration:** Attended in-person at Purdue University classroom.
* **Truth Attestation:** I attest that all reported hand calculations, code implementations, and target company numbers represent authentic work.

---

## 9. Readiness Sentence

> **"Ready — the synthetic engine reconciles all 12 known-answer checkpoints within tolerance and boundary checks refuse $g \ge \text{WACC}$. Unsafe — PepsiCo's cost-of-debt schedule across $44.3B in short and long-term notes needs full tranche breakdown. Next — pull Note 8 debt schedules to finalize WACC before Thursday's sensitivity grid."**

---

## 10. Ungraded Growth Note

> *What I can do now that I could not do before this lab:* I can build a clean, audited Python FCFF DCF model from scratch, hand-calculate every step of explicit cash flow compounding and terminal value discounting, and verify enterprise-to-equity bridges against primary SEC 10-K balance sheets.  
> *What still feels shaky:* Sourcing exact effective borrowing rates across complex multi-currency corporate debt schedules to refine WACC.
