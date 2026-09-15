# Lab 07 — Comparable-Company Policy and Implied Range

**Student Analyst:** Oladapo Olaniyan  
**Course:** FIN 43900 — AI Finance Applications, Purdue University  
**Target Security:** PepsiCo, Inc. (NASDAQ: `PEP` | CIK: `0000077476`)  
**Date:** September 15, 2026  

---

## Workspace Directory Structure

```
labs/lab-07/
├── README.md               # Lab 07 instructions, setup, and summary
├── comps_model.py          # Python model for synthetic reconciliation & PepsiCo peer multiples
├── pep_peer_policy.md      # Formal peer policy, AI candidate audit log, and borderline test
└── lab-07-checkout.md      # Official Brightspace checkout submission document
```

---

## Key Valuation Deliverables & Execution Instructions

### 1. Synthetic Checkpoint Reconciliation
To execute the model and verify synthetic known answers:
```bash
python labs/lab-07/comps_model.py
```
**Expected Synthetic Checkpoints (All Passed):**
- `median_ev_to_ebitda`: **13.0000**
- `median_price_to_earnings`: **15.0000**
- `trading_ev_to_ebitda_per_share`: **$15.8000**
- `trading_price_to_earnings_per_share`: **$12.0000**
- `precedent_transaction_per_share`: **$17.4000**

### 2. PepsiCo Implied Valuation Summary
- **Target Denominators:** EBITDA = $16,500M | Net Income = $9,100M | Cash = $8,505M | Debt = $44,306M | Diluted Shares = 1,378M.
- **Full Peer Set (KO, KDP, MDLZ, KHC):** EV/EBITDA Implied Value = **$156.41** | P/E Implied Value = **$133.61**.
- **Clean Peer Set (Excl. Borderline Peer KHC):** EV/EBITDA Implied Value = **$167.96** | P/E Implied Value = **$138.08**.
- **Current Market Price:** **$143.21** per share (Feb 4, 2025).

---

## Artifact Links
* **Python Peer Valuation Engine:** [`comps_model.py`](file:///c:/Users/dolan/OneDrive%20-%20purdue.edu/2026-Fall/FIN-43900%20-%20AI%20Finance%20Applications/labs/lab-07/comps_model.py)
* **Peer Policy & AI Audit Log:** [`pep_peer_policy.md`](file:///c:/Users/dolan/OneDrive%20-%20purdue.edu/2026-Fall/FIN-43900%20-%20AI%20Finance%20Applications/labs/lab-07/pep_peer_policy.md)
* **Brightspace Checkout Submission:** [`lab-07-checkout.md`](file:///c:/Users/dolan/OneDrive%20-%20purdue.edu/2026-Fall/FIN-43900%20-%20AI%20Finance%20Applications/labs/lab-07/lab-07-checkout.md)
