# Lab 08 — Deal Evidence and Valuation Triangulation

**Student Analyst:** Oladapo Olaniyan  
**Course:** FIN 43900 — AI Finance Applications, Purdue University  
**Target Security:** PepsiCo, Inc. (NASDAQ: `PEP` | CIK: `0000077476`)  
**Date:** September 15, 2026  

---

## Workspace Directory Structure

```
labs/lab-08/
├── README.md                           # Lab 08 instructions, setup, and summary
├── triangulation_model.py              # Python model for triangulation & normalization checks
├── deal_audit_broadcom_vmware.md       # Primary source audit of Broadcom/VMware & Kellanova/Mars
└── lab-08-checkout.md                  # Official Brightspace merit checkout submission document
```

---

## Key Valuation Deliverables & Execution Instructions

### 1. Triangulation Model Execution
To execute the model and verify synthetic precedent checkpoints + PepsiCo triangulation:
```bash
python labs/lab-08/triangulation_model.py
```
**Valuation Triangulation Summary for PepsiCo (`PEP`):**
- **FCFF DCF Base Case (Lab 06):** **$140.73** per share (Supported Range: $101.07 – $219.87).
- **Trading Comparables (Lab 07):** P/E **$138.08** | EV/EBITDA **$168.00** per share (Clean Peer Set: KO, KDP, MDLZ).
- **Precedent Deal Evidence:** EV/EBITDA **$170.39** per share (Kellanova / Mars 16.4x EV/EBITDA).
- **Current Market Price:** **$143.21** per share (Feb 4, 2025).

### 2. Changed-Normalization Robustness Test
- **Reported EBITDA ($16,500M) EV Comps Value:** **$168.00** / share.
- **Normalized EBITDA ($18,311M) EV Comps Value:** **$189.29** / share (+$21.29 shift).

---

## Artifact Links
* **Python Triangulation Model:** [`triangulation_model.py`](file:///c:/Users/dolan/OneDrive%20-%20purdue.edu/2026-Fall/FIN-43900%20-%20AI%20Finance%20Applications/labs/lab-08/triangulation_model.py)
* **Deal Audit Document:** [`deal_audit_broadcom_vmware.md`](file:///c:/Users/dolan/OneDrive%20-%20purdue.edu/2026-Fall/FIN-43900%20-%20AI%20Finance%20Applications/labs/lab-08/deal_audit_broadcom_vmware.md)
* **Brightspace Checkout Submission:** [`lab-08-checkout.md`](file:///c:/Users/dolan/OneDrive%20-%20purdue.edu/2026-Fall/FIN-43900%20-%20AI%20Finance%20Applications/labs/lab-08/lab-08-checkout.md)
