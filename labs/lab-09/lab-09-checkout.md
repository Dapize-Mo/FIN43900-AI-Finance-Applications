# Lab 09 — Merit Checkout: Pro-Forma Build (Engine & Known Answer)

**Student Name:** Oladapo Olaniyan  
**Teammate / Partner:** `kogbuef@purdue.edu`  
**Course:** FIN 43900 — AI Finance Applications, Purdue University  
**Date:** September 22, 2026  
**Session Token:** `Beta 1-2-3`  
**Repository Link:** [`labs/lab-09`](https://github.com/Dapize-Mo/FIN43900-AI-Finance-Applications/tree/main/labs/lab-09)  

---

## 1. Header & Team Contribution

* **Lab Date:** September 22, 2026
* **Teammates / Learning Partners:** `kogbuef@purdue.edu` (Collaborative 3-statement pro-forma engine construction, ABG assumption auditing, `proforma.py` verification, and swap-and-break balance testing).

---

## 2. Decision Frame & Guiding Question

> **Question:** *What are five years of a company's statements worth, built from assumptions you can defend, and how do you know the statements are right?*

* **Target Company:** Asbury Automotive Group, Inc. (NYSE: `ABG`)
* **Decision Context:** Equity valuation via 5-year pro-forma Free Cash Flow to Equity (FCFE) and terminal value discounting.
* **Why Cash is Computed Last:** Cash is the balancing line on the balance sheet. It absorbs operating net income, working capital investments, debt servicing, capital expenditures, and financing activities (revolver draw/repayment, share buybacks).

---

## 3. Asbury Automotive Group (`ABG`) Known-Answer Grid

| Financial Line | FY2026E | FY2027E | FY2028E | FY2029E | FY2030E |
| --- | ---: | ---: | ---: | ---: | ---: |
| **Revenue ($M)** | **18,323.0** | 18,652.8 | 18,988.5 | 19,330.3 | **19,678.3** |
| **Operating Income ($M)** | **844.2** | 890.3 | 938.1 | 954.5 | **971.4** |
| **Net Income ($M)** | **413.6** | 452.8 | 493.1 | 510.1 | **527.5** |
| **Free Cash Flow to Equity ($M)** | **211.4** | 255.1 | 299.7 | 320.9 | **342.3** |
| **Year-End Cash ($M)** | **101.8** | 206.9 | 356.6 | 527.5 | **719.8** |
| **Balance Sheet Gap ($M)** | **0.0** | **0.0** | **0.0** | **0.0** | **0.0** |

* **PV of 5-Year FCFE:** **$1,059.87M**
* **Terminal Value (PV):** **$4,177.46M** (Undiscounted TV = **$6,727.85M**)
* **Total Equity Value:** **$5,237.34M**
* **Shares Outstanding:** **17.951349M**
* **Value per Share:** **$291.75** (Target Known Answer Matched)
* **Terminal Value Share:** **79.8%** (~80% of total value)

---

## 4. Model Refusal & Swap-and-Break Test

* **Assertion Function (`assert_balanced`):** `proforma.py` executes `assert_balanced` for every projected year. If `Assets - (Liabilities + Equity) != 0`, execution terminates immediately.
* **Swap-and-Break Result:** Forcing FY2026E cash to opening cash ($40.4M) instead of the computed figure ($101.8M) causes the model to refuse, raising `ValueError` naming **FY2026E** and a balance gap of **-$61.4M**.

---

## 5. Floor Plan Mechanics & Economic Meaning

1. **What it is:** Floor plan financing is specialized inventory debt provided by automobile manufacturers' finance arms (e.g., Ford Credit, Toyota Financial) or commercial banks to finance dealership inventory.
2. **How it works in pro-forma:** Moves dynamically with inventory ($2,027.0M / $2,135.8M ≈ 94.91% of inventory). Interest is computed on opening floor plan balances (4.67%). Changes in floor plan financing are included inside FCFE as operating working capital financing.
3. **Impact of removing floor plan:** If floor plan financing is omitted, the dealership must fund $2.1B+ of inventory out of operating cash flow, driving projected cash down to approximately **-$1.1B**.

---

## 6. GitHub File Links

* **Pro-Forma Engine Script:** [`proforma.py`](https://github.com/Dapize-Mo/FIN43900-AI-Finance-Applications/tree/main/labs/lab-09/proforma.py)
* **Human Baseline Artifact:** [`lab09-human-baseline.md`](https://github.com/Dapize-Mo/FIN43900-AI-Finance-Applications/tree/main/labs/lab-09/lab09-human-baseline.md)
* **Lab README:** [`README.md`](https://github.com/Dapize-Mo/FIN43900-AI-Finance-Applications/tree/main/labs/lab-09/README.md)

---

## 7. In-Person Attendance & Truth Attestation

I completed this work in today’s class with the teammate (`kogbuef@purdue.edu`) listed above, and this checkout is truthful. All reported calculations and valuation numbers were verified by running `proforma.py`.

**Student Signature:** Oladapo Olaniyan  
**Date:** September 22, 2026  

---

## 8. Ungraded Growth Note

*What can you do now that you could not do before this lab, and what still feels shaky?*

> Before this lab, I viewed 3-statement financial modeling as a manual accounting exercise rather than an interconnected dynamic engine. Now, I understand how to programmatically link revenue growth, working capital ratios, floor plan inventory debt, revolving credit logic, and FCFE discounting into a single automated Python model that enforces balance sheet integrity at every step. What still feels shaky is selecting and defending long-term operating margin improvement assumptions when projecting companies outside automotive retail.
