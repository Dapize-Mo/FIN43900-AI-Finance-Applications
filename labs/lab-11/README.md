# FIN 43900 Lab 11 — Credit Stress and Covenant Headroom

**Student Analyst:** Oladapo Olaniyan (`olaniyan@purdue.edu`)  
**Teammates / Learning Partners:**  
- J. Maffei (`maffeij@purdue.edu` | Target Company: Oracle Corp. — `ORCL`)  
- Kasoi (`kasoi@purdue.edu` | Target Company: McDonald's Corp. — `MCD`)  
**Course:** FIN 43900 — AI Finance Applications, Purdue University  
**Target Company:** PepsiCo, Inc. (NASDAQ: `PEP` | CIK: `0000077476`)  
**Date:** September 29, 2026 / Tuesday Authenticated Completion  
**Session Token:** `sensitivity`  

---

## Overview

This directory contains the complete Lab 11 checkout deliverables for synthetic credit stress modeling, covenant headroom evaluation, decision state classification, and target-company stress propagation for PepsiCo, Inc. (`PEP`).

---

## Files in this Directory

- [`credit_stress_lab11.py`](file:///c:/Users/dolan/OneDrive%20-%20purdue.edu/2026-Fall/FIN-43900%20-%20AI%20Finance%20Applications/labs/lab-11/credit_stress_lab11.py): Complete Python credit stress engine implementing `load_scenarios()`, `calculate_stress_metrics()`, `test_covenants()`, `committee_action()`, and PepsiCo target stress testing.
- [`stress_model.py`](file:///c:/Users/dolan/OneDrive%20-%20purdue.edu/2026-Fall/FIN-43900%20-%20AI%20Finance%20Applications/labs/lab-11/stress_model.py): Execution entry wrapper script.
- [`stress_scenarios.csv`](file:///c:/Users/dolan/OneDrive%20-%20purdue.edu/2026-Fall/FIN-43900%20-%20AI%20Finance%20Applications/labs/lab-11/stress_scenarios.csv): Synthetic scenario input dataset.
- [`lab-11-checkout.md`](file:///c:/Users/dolan/OneDrive%20-%20purdue.edu/2026-Fall/FIN-43900%20-%20AI%20Finance%20Applications/labs/lab-11/lab-11-checkout.md): Formatted merit checkout deliverable report with Brightspace Question 2 copy-paste text block.
- [`README.md`](file:///c:/Users/dolan/OneDrive%20-%20purdue.edu/2026-Fall/FIN-43900%20-%20AI%20Finance%20Applications/labs/lab-11/README.md): Overview document.

---

## Execution & Verification Instructions

To execute the credit stress model and print the scenario metrics, covenant test matrix, and PepsiCo downside stress results:

```bash
python labs/lab-11/credit_stress_lab11.py
```

Or run the execution wrapper:

```bash
python labs/lab-11/stress_model.py
```
