# FIN 43900 — AI Finance Applications

**Course Workspace & Research Repository**  
**Purdue University** · Mitchell E. Daniels, Jr. School of Business · Fall 2026  
**Instructor:** Dr. Xinde "Cinder" Zhang  
**Student / Author:** **Oladapo Olaniyan**  
**Target Coverage Security:** PepsiCo, Inc. (NASDAQ: `PEP` | CIK: `0000077476`)  

---

## 📌 Repository Overview

This repository serves as the official, durable working workspace for course materials, audited financial evidence ledgers, Python models, and research reports for **FIN 43900**. 

All work adheres to the course's **DRIVER framework**, source evidence hierarchy (audited SEC filings > reconciled disclosures > market series), and mandatory AI disclosure standards.

---

## 📂 Labs & Deliverables Directory

| Lab / Session | Date | Topic | Key Deliverables & Quick Links | Status |
|---|---|---|---|:---:|
| **Lab 03** | Sep 1, 2026 | **The Valuation Contract & Edition A Baseline** | • [`edition-a-baseline.md`](labs/lab-03/edition-a-baseline.md)<br>• [`Project_1_Edition_A_Baseline_PEP.pdf`](labs/lab-03/Project_1_Edition_A_Baseline_PEP.pdf) | ✅ Submitted |
| **Lab 04** | Sep 3, 2026 | **Know Your Company: Deep Read & First Report** | • 📋 [**Checkout Submission (`checkout.md`)**](labs/lab-04/PEP-research/checkout.md)<br>• 📄 [**Research Report (`PepsiCo_2026-09-03_report.md`)**](labs/lab-04/PEP-research/PepsiCo_2026-09-03_report.md)<br>• 📑 [**Added Sources (`sources.md`)**](labs/lab-04/PEP-research/sources.md)<br>• 📊 [**Executive PDF Report**](labs/lab-04/PepsiCo_FY2024_10K_MDA_Report.pdf)<br>• 🔢 [**Evidence Ledger CSV**](labs/lab-04/pep_evidence_ledger_lab04.csv)<br>• 🐍 [**Python Bridge Script**](labs/lab-04/valuation_bridge_lab04.py) | ✅ Ready / Live |

---

## 📑 Lab 04 Active Research Package (`PEP-research`)

For Lab 04 (Week 2, Thursday), research materials are organized into the dedicated folder:  
👉 [**`labs/lab-04/PEP-research/`**](labs/lab-04/PEP-research/)

- [**`checkout.md`**](labs/lab-04/PEP-research/checkout.md) — Brightspace submission block including investment decision call (**Watch-Defer**), falsification condition, added external sources, personal contribution, and growth note.
- [**`PepsiCo_2026-09-03_report.md`**](labs/lab-04/PEP-research/PepsiCo_2026-09-03_report.md) — Full company research report with business model overview, segment reviews, contamination audit (normalizing $1,811M in one-time charges), historical comparison, management outlook, and mandatory course footer.
- [**`sources.md`**](labs/lab-04/PEP-research/sources.md) — Detailed citations for the 3 added external sources beyond the primary filing (FY2023 10-K, Q4 2024 earnings call transcript, and Feb 2025 dividend press release).

---

## 🛠️ Reproducibility & Model Verification

All valuation bridge figures and cash flow metrics can be independently executed and verified locally:

```bash
# Run the Lab 04 valuation bridge & sensitivity audit
python labs/lab-04/valuation_bridge_lab04.py
```

- **Reported GAAP EBIT:** $12,887.0M (14.03% Operating Margin)
- **Normalized Core EBIT:** $14,698.0M (16.00% Core Margin; $1,811M non-recurring normalization)
- **Net Debt Claim:** $35,801.0M ($44,306M total debt minus $8,505M cash)
- **Baseline Intrinsic Per-Share Value:** $169.96 / share (at $270,000M baseline EV across 1,378.0M diluted shares)

---

## 📜 Academic Integrity & AI Policy Compliance

- **Edition A Baseline:** Timestamped and locked prior to project-specific AI prompting.
- **AI Tooling Disclosure:** ChatGPT/Codex and Gemini were utilized as collaborative research studios for prompt refinement and architecture cross-examination; all data points, filing locators, accounting normalizations, and investment judgments were independently verified by the author.
- **Author:** Oladapo Olaniyan (olaniyan@purdue.edu)
