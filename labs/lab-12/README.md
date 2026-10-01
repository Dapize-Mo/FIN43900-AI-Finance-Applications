# Lab 12 — Project 2 Audit and Defense Studio

**Course:** FIN 43900 — AI Finance Applications (Fall 2026)  
**Student / Author:** **Oladapo Olaniyan**  
**Institution:** Purdue University · Mitchell E. Daniels, Jr. School of Business  
**Target Coverage Security:** PepsiCo, Inc. (NASDAQ: `PEP` | CIK: `0000077476`)  

---

## 📌 Overview & Official Status

Week 12 is designated as the **Project 2 Audit and Defense Studio**. Per official course guidelines:
- **Graded Checkout Status:** Both Week 12 class meetings are open Q&A and consultation studios. **There is no required graded lab checkout or lab points due for Week 12.** Formal Project 2 submission mechanics and deadlines are governed by Brightspace (due Week 13).
- **Primary Objective:** Prepare, audit, and pressure-test all **Project 2** deliverables prior to submission using Federal Reserve SR 11-7 / SR 26-2 Model Risk Management principles and mechanical package validation scripts.

---

## 📂 Directory Contents

| File / Asset | Description | Quick Link |
|---|---|:---:|
| `project2_manifest_template.csv` | 12-row package manifest template (11 required + 1 optional) | [`project2_manifest_template.csv`](file:///c:/Users/dolan/OneDrive%20-%20purdue.edu/2026-Fall/FIN-43900%20-%20AI%20Finance%20Applications/labs/lab-12/project2_manifest_template.csv) |
| `project2_audit.py` | Python mechanical manifest validation and gap detection script | [`project2_audit.py`](file:///c:/Users/dolan/OneDrive%20-%20purdue.edu/2026-Fall/FIN-43900%20-%20AI%20Finance%20Applications/labs/lab-12/project2_audit.py) |
| `lab-12-checkout.md` | Comprehensive Project 2 Model Risk Audit & Defense Package | [`lab-12-checkout.md`](file:///c:/Users/dolan/OneDrive%20-%20purdue.edu/2026-Fall/FIN-43900%20-%20AI%20Finance%20Applications/labs/lab-12/lab-12-checkout.md) |

---

## 🛠️ Mechanical Package Verification

To run the automated manifest audit script locally:

```bash
python labs/lab-12/project2_audit.py
```

The script inspects `project2_manifest_template.csv` for required columns, row count (12), valid URLs/locations, verified access flags, frozen commit IDs, and video timestamp indices.

---

## 🏛️ Federal Reserve Model Risk Management Framework (SR 11-7 / SR 26-2)

1. **Conceptual Soundness:** Design, assumptions, data, and developmental evidence fit stated purpose.
2. **Outcome Analysis:** Model results compared against holdouts, baselines, backtests, and known outcomes.
3. **Ongoing Monitoring:** Tracking limitations, market shifts, overrides, and performance triggers over time.
4. **Independent Challenge:** Reviewers test for mandate, point-in-time data, baseline/holdout, cost/capacity, stability, and reproducibility failure modes.

---

**Author:** Oladapo Olaniyan (olaniyan@purdue.edu)  
**Teammate:** `kogbuef@purdue.edu`  
