# Lab 05 — Build and Validate an FCFF DCF Engine

**Target Company:** PepsiCo, Inc. (NASDAQ: `PEP` | CIK: `0000077476`)  
**Student Analyst:** Oladapo Olaniyan  
**Teammate:** kogbuef@purdue.edu  
**Course:** FIN 43900 — AI Finance Applications, Purdue University  
**Date:** September 8, 2026 (Tuesday Session 05)  

---

## Directory Contents

| File | Description |
|---|---|
| [`dcf_starter.py`](dcf_starter.py) / [`dcf.py`](dcf.py) | Full Python DCF engine implementing `project_fcff`, `value_dcf`, `sensitivity_table`, `reverse_dcf_for_growth`, training-case validation, boundary checks, and PepsiCo transfer. |
| [`dcf_case.csv`](dcf_case.csv) | Official 11 input values for the synthetic known-answer training case. |
| [`dcf_expected_output.csv`](dcf_expected_output.csv) | Official 12 target values and tolerances for known-answer validation. |
| [`pep_inputs_lab05.md`](pep_inputs_lab05.md) | Sourced input table for PepsiCo, Inc. transferred from Week 2 SEC Form 10-K evidence ledger. |
| [`lab-05-checkout.md`](lab-05-checkout.md) | Official Brightspace checkout submission package ready for copy-paste submission. |

---

## How to Execute

To validate the engine against synthetic checkpoints and view PepsiCo transfer outputs:

```bash
python labs/lab-05/dcf_starter.py
```
