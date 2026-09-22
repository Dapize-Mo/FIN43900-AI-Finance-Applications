# Lab 09 — Human Baseline: Pro-Forma Engine & ABG Known Answer

**Timestamp:** 2026-09-22 14:15:00 EST  
**Student Analyst:** Oladapo Olaniyan  
**Teammate / Partner:** `kogbuef@purdue.edu`  
**Course:** FIN 43900 — AI Finance Applications, Purdue University  
**Target Case:** Asbury Automotive Group, Inc. (`ABG`)  

---

## 1. Core Principles & Decision Question

**Question:** *What are five years of a company's statements worth, built from assumptions you can defend, and how do you know the statements are right?*

### Three Core Judgments:
1. **Organic Revenue Growth & Margin Expansion:** Revenue grows at 1.8% annually; Gross Margin fixed at 17.05%; SG&A ratio improves from 66.5% to 64.5% of gross profit.
2. **Capital Structure & Debt Amortization:** Scheduled debt repayment of $150.0M/year reduces opening term debt ($3,572.0M), while share buybacks of $150.0M/year reduce equity. Floor plan inventory financing moves dynamically with inventory ($2,027.0M / $2,135.8M ratio).
3. **Cash Computed Last & Revolver Balancing:** Cash is computed as opening cash + FCFE − buybacks. If cash falls below minimum ($25.0M), a revolving line of credit is drawn; if cash exceeds minimum and revolver is outstanding, revolver is repaid first.

---

## 2. ABG Assumption Set & Opening Balance Sheet (FY2025 Base)

* **Opening Balance Sheet (USD Millions):**  
  Revenue $17,999.0 · Inventory $2,135.8 · PP&E $3,070.4 · Other Assets $6,371.6 · Cash $40.4 · Floor Plan $2,027.0 · Term Debt $3,572.0 · Other Liabilities $2,127.5 · Equity $3,891.7.

* **Key Ratios:**  
  * Depreciation Ratio = $82.4\text{M} / \$3,070.4\text{M} = 2.6837\%$  
  * Inventory Days Ratio = $\$2,135.8\text{M} / (\$17,999.0\text{M} - \$3,071.7\text{M}) = 0.143079$  
  * Floor Plan Ratio = $\$2,027.0\text{M} / \$2,135.8\text{M} = 94.9059\%$  
  * Working Capital Change = $0.8\%$ of $\Delta\text{Revenue}$  

---

## 3. Human Known-Answer Verification Record

| Financial Line | FY2026E | FY2027E | FY2028E | FY2029E | FY2030E |
|---|---:|---:|---:|---:|---:|
| **Revenue** | **$18,323.0M** | $18,652.8M | $18,988.5M | $19,330.3M | **$19,678.3M** |
| **Operating Income (EBIT)** | **$844.2M** | $890.3M | $938.1M | $954.5M | **$971.4M** |
| **Net Income** | **$413.6M** | $452.8M | $493.1M | $510.1M | **$527.5M** |
| **Free Cash Flow (FCFE)** | **$211.4M** | $255.1M | $299.7M | $320.9M | **$342.3M** |
| **Cash (Year End)** | **$101.8M** | $206.9M | $356.6M | $527.5M | **$719.8M** |
| **Assets − Liab − Equity** | **0.0** | **0.0** | **0.0** | **0.0** | **0.0** |

* **Equity Value per Share:** **$291.75** (Target Match)
* **Terminal Value Share:** **79.8%** (~80% of total value)

---

## 4. Model Integrity & Swap-and-Break Refusal Test

* **Refusal Assertion (`assert_balanced`):** Hard failure raised if $\text{Assets} - (\text{Liabilities} + \text{Equity}) \neq 0$.
* **Break Test:** Forcing FY2026E cash to opening cash ($40.4\text{M}$) instead of calculated cash ($101.8\text{M}$) causes `proforma.py` to refuse execution, naming **FY2026E** and reporting a balance gap of **$-61.4\text{M}$** (the unrecorded cash flow change).
