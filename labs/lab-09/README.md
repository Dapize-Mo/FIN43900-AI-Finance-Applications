# Lab 09 — Pro-Forma Build: The Engine and the Known Answer

**Student Analyst:** Oladapo Olaniyan  
**Teammate / Partner:** `kogbuef@purdue.edu`  
**Course:** FIN 43900 — AI Finance Applications, Purdue University  
**Date:** September 22, 2026  
**Target Security:** Asbury Automotive Group, Inc. (NYSE: `ABG`)  

---

## Workspace Directory Structure

```
labs/lab-09/
├── README.md                           # Lab 09 instructions, setup, assumptions, and summary
├── proforma.py                         # 3-statement pro-forma Python engine & ABG valuation model
├── lab09-human-baseline.md             # Human baseline artifact for Pro-Forma ABG known answer
└── lab-09-checkout.md                  # Official Brightspace merit checkout submission document
```

---

## Key Pro-Forma Deliverables & Execution Instructions

### 1. Python Pro-Forma Model Execution
To execute the 3-statement pro-forma engine and reproduce the Asbury Automotive Group (`ABG`) target valuation:
```bash
python labs/lab-09/proforma.py
```

### 2. Verified ABG Known Answers (2026E – 2030E)

| Metric | FY2026E | FY2027E | FY2028E | FY2029E | FY2030E |
|---|---:|---:|---:|---:|---:|
| **Revenue ($M)** | **18,323.0** | 18,652.8 | 18,988.5 | 19,330.3 | **19,678.3** |
| **Operating Income ($M)** | **844.2** | 890.3 | 938.1 | 954.5 | **971.4** |
| **Net Income ($M)** | **413.6** | 452.8 | 493.1 | 510.1 | **527.5** |
| **FCFE ($M)** | **211.4** | 255.1 | 299.7 | 320.9 | **342.3** |
| **Year-End Cash ($M)** | **101.8** | 206.9 | 356.6 | 527.5 | **719.8** |
| **Balance Gap Check ($M)** | **0.0** | **0.0** | **0.0** | **0.0** | **0.0** |

* **PV of 5-Year FCFE:** **$1,059.87M**
* **Terminal Value (TV):** **$6,727.85M** (PV: **$4,177.46M**)
* **Total Equity Value:** **$5,237.34M**
* **Shares Outstanding:** **17.951349M**
* **Value per Share:** **$291.75** (Target Known Answer)
* **Terminal Value Share:** **79.8%** (~80% of total value)

---

## Artifact Links
* **Python Pro-Forma Engine:** [`proforma.py`](file:///c:/Users/dolan/OneDrive%20-%20purdue.edu/2026-Fall/FIN-43900%20-%20AI%20Finance%20Applications/labs/lab-09/proforma.py)
* **Human Baseline Switch Artifact:** [`lab09-human-baseline.md`](file:///c:/Users/dolan/OneDrive%20-%20purdue.edu/2026-Fall/FIN-43900%20-%20AI%20Finance%20Applications/labs/lab-09/lab09-human-baseline.md)
* **Brightspace Checkout Submission:** [`lab-09-checkout.md`](file:///c:/Users/dolan/OneDrive%20-%20purdue.edu/2026-Fall/FIN-43900%20-%20AI%20Finance%20Applications/labs/lab-09/lab-09-checkout.md)
