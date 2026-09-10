# FIN 43900 — AI Finance Applications

**Course Workspace & Research Repository**  
**Purdue University** · Mitchell E. Daniels, Jr. School of Business · Fall 2026  
**Instructor:** Dr. Xinde "Cinder" Zhang  
**Student / Author:** **Oladapo Olaniyan**  
**Target Coverage Security:** PepsiCo, Inc. (NASDAQ: `PEP` | CIK: `0000077476`)  

---

## 📌 Repository Overview

This repository serves as the official working workspace for course materials, audited financial evidence ledgers, Python models, and research reports for **FIN 43900**. 

All work adheres to the course's **DRIVER framework**, source evidence hierarchy (audited SEC filings > reconciled disclosures > market series), and mandatory AI disclosure standards.

---

## 📂 Labs & Deliverables Directory

| Lab / Session | Date | Topic | Key Deliverables & Quick Links | Status |
|---|---|---|---|:---:|
| **Lab 03** | Sep 1, 2026 | **The Valuation Contract & Edition A Baseline** | • [`edition-a-baseline.md`](labs/lab-03/edition-a-baseline.md)<br>• [`Project_1_Edition_A_Baseline_PEP.pdf`](labs/lab-03/Project_1_Edition_A_Baseline_PEP.pdf) | ✅ Submitted |
| **Lab 04** | Sep 3, 2026 | **Know Your Company: Deep Read & First Report** | • 📋 [**Checkout Submission (`checkout.md`)**](labs/lab-04/PEP-research/checkout.md)<br>• 📄 [**Research Report (`PepsiCo_2026-09-03_report.md`)**](labs/lab-04/PEP-research/PepsiCo_2026-09-03_report.md)<br>• 📑 [**Added Sources (`sources.md`)**](labs/lab-04/PEP-research/sources.md)<br>• 📊 [**Executive PDF Report**](labs/lab-04/PepsiCo_FY2024_10K_MDA_Report.pdf)<br>• 🔢 [**Evidence Ledger CSV**](labs/lab-04/pep_evidence_ledger_lab04.csv)<br>• 🐍 [**Python Bridge Script**](labs/lab-04/valuation_bridge_lab04.py) | ✅ Submitted |
| **Lab 05** | Sep 8, 2026 | **FCFF DCF Engine & Synthetic Validation** | • 📋 [**Checkout Submission (`lab-05-checkout.md`)**](labs/lab-05/lab-05-checkout.md)<br>• 🐍 [**DCF Engine (`labs/lab-05/dcf.py`)**](labs/lab-05/dcf.py)<br>• 🔢 [**Synthetic Benchmark Case**](labs/lab-05/dcf_case.csv) | ✅ Submitted |
| **Lab 06** | Sep 10, 2026 | **Sensitivity Analysis, Reverse DCF & Recommendation** | • 📋 [**Checkout Submission (`lab-06-checkout.md`)**](labs/lab-06/lab-06-checkout.md)<br>• 🔄 [**Reverse DCF Script (`pep_dcf_model_lab06.py`)**](labs/lab-06/pep_dcf_model_lab06.py)<br>• 📊 [**Sensitivity Grid CSV (`pep_sensitivity_grid.csv`)**](labs/lab-06/pep_sensitivity_grid.csv)<br>• 📄 [**Sourced Inputs Table (`pep_inputs.md`)**](labs/lab-06/pep_inputs.md)<br>• 📂 [**Lab 06 Directory README**](labs/lab-06/README.md) | ✅ Live / Submitted |

---

## 📑 Lab 06 Active Valuation & Reverse DCF Package

For Lab 06 (Session 6, Session Token: `Reverse DCF`), materials are organized in:  
👉 [**`labs/lab-06/`**](labs/lab-06/)

- [**`lab-06-checkout.md`**](labs/lab-06/lab-06-checkout.md) — Brightspace submission package including 5 Merit Anchors (Sensitivity Grid, Reverse DCF, Sourced Inputs, Reasonableness, and Watch-Defer Call).
- [**`pep_dcf_model_lab06.py`**](labs/lab-06/pep_dcf_model_lab06.py) — Python DCF engine executing synthetic validation, PepsiCo scenarios, WACC/\(g\) sensitivity table, and Reverse DCF bisection search.
- [**`pep_sensitivity_grid.csv`**](labs/lab-06/pep_sensitivity_grid.csv) — Exported 5x4 valuation matrix.

---

## 🛠️ Reproducibility & Model Verification

All valuation bridge figures and DCF models can be executed locally:

```bash
# Run the Lab 06 DCF engine, sensitivity grid, and reverse DCF
python labs/lab-06/pep_dcf_model_lab06.py
```

- **PepsiCo Base Case Valuation:** $140.73 / share ($229,731.6M EV across 1,378.0M diluted shares)
- **Observed Market Price:** $143.21 / share (Feb 4, 2025 Nasdaq Close)
- **Reverse DCF Implied FCFF CAGR:** 3.73% per year (+0.33 percentage point uniform shift)

---

## 📜 Academic Integrity & AI Policy Compliance

- **Author:** Oladapo Olaniyan (olaniyan@purdue.edu)
- **Teammate:** `kogbuef@purdue.edu`
- **Course:** FIN 43900 — AI Finance Applications, Purdue University
