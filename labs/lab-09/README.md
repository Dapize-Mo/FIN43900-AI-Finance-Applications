# Lab 09 — Credit Evidence and Ratio Conventions

**Student Analyst:** Oladapo Olaniyan  
**Teammate / Partner:** `kogbuef@purdue.edu`  
**Course:** FIN 43900 — AI Finance Applications, Purdue University  
**Date:** September 22, 2026  

---

## Workspace Directory Structure

```
labs/lab-09/
├── README.md                           # Lab 09 instructions, setup, ratio conventions, and summary
├── credit_cases.csv                    # Synthetic credit case dataset (Borrowers A–F)
├── lab09-human-baseline.md             # Witnessed human credit baseline switch artifact (AI-closed)
├── credit_screening_model.py           # Python model for ratio calculation, screening, & error costs
└── lab-09-checkout.md                  # Official Brightspace merit checkout submission document
```

---

## Key Credit Deliverables & Execution Instructions

### 1. Python Credit Model Execution
To execute the credit screening model, verify Borrower A known answers, and evaluate error metrics:
```bash
python labs/lab-09/credit_screening_model.py
```

**Known-Answer Verification (Borrower A):**
- **Leverage (Debt / EBITDA):** **4.00x** ($600M / $150M)
- **EBIT Interest Coverage:** **5.00x** (($150M - $30M) / $24M = $120M / $24M)
- **EBITDA Interest Coverage (Injected Conflict Check):** **6.25x** ($150M / $24M)
- **Current Ratio (Liquidity):** **1.25x** ($250M / $200M)
- **FCF / Debt Yield:** **8.3333%** (($100M - $50M) / $600M = $50M / $600M)

### 2. Confusion Matrix & Underwriting Error Metrics
- **True Positives (TP = 3):** Borrowers B, D, F correctly flagged for review/rejection.
- **True Negatives (TN = 2):** Borrowers A, C correctly approved.
- **False Positives (FP = 1):** Borrower E flagged for review due to liquidity (0.67x) despite actual outcome = 0 (Opportunity Cost).
- **False Negatives (FN = 0):** Zero defaults passed undetected (Loss Cost minimized).

---

## Artifact Links
* **Synthetic Credit Dataset:** [`credit_cases.csv`](file:///c:/Users/dolan/OneDrive%20-%20purdue.edu/2026-Fall/FIN-43900%20-%20AI%20Finance%20Applications/labs/lab-09/credit_cases.csv)
* **Human Baseline Switch Artifact:** [`lab09-human-baseline.md`](file:///c:/Users/dolan/OneDrive%20-%20purdue.edu/2026-Fall/FIN-43900%20-%20AI%20Finance%20Applications/labs/lab-09/lab09-human-baseline.md)
* **Python Screening Model:** [`credit_screening_model.py`](file:///c:/Users/dolan/OneDrive%20-%20purdue.edu/2026-Fall/FIN-43900%20-%20AI%20Finance%20Applications/labs/lab-09/credit_screening_model.py)
* **Brightspace Checkout Submission:** [`lab-09-checkout.md`](file:///c:/Users/dolan/OneDrive%20-%20purdue.edu/2026-Fall/FIN-43900%20-%20AI%20Finance%20Applications/labs/lab-09/lab-09-checkout.md)
