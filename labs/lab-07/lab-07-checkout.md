# Lab 07 Checkout — Comparable-Company Policy and Implied Range

| Metadata | Details |
|---|---|
| **Student Analyst** | **Oladapo Olaniyan** |
| **Teammates** | **None (Worked Individually / Remote Session)** |
| **Course** | FIN 43900 — AI Finance Applications, Purdue University |
| **Lab Date & Token** | September 15, 2026 \| Session Token: `Career Fair` |
| **Target Security** | PepsiCo, Inc. (NASDAQ: `PEP` \| CIK: `0000077476`) |

---

## 📌 Brightspace Question 2 Copy-Paste Box (25 Points)

DISCOVER
Uncertain whether raw AI peer lists would yield a defensible valuation for PepsiCo (PEP) and how qualifying borderline peers affects the range. Writing a no-AI policy and auditing SEC 10-K filings showed Kraft Heinz (KHC) was a low-multiple drag (8.75x EV/EBITDA). Removing KHC shifted median EV/EBITDA from 15.24x to 16.20x (+ $11.55/sh shift to $167.96), placing PEP market price ($143.21) squarely inside the clean peer trading range ($138.08–$167.96).

DEFINE
Target: PepsiCo, Inc. (PEP) fair trading value using FY2024 Form 10-K data. Key boundary: Enterprise multiples (EV/EBITDA) require the EV-to-equity bridge ($1,378M shares, $8,505M cash, $44,306M debt), whereas equity multiples (P/E) land directly on equity value without bridging.

GOOD QUESTION
How does a consolidated peer multiple compare to a Sum-of-the-Parts (SOTP) valuation separating high-margin Frito-Lay snacks from capital-intensive bottling beverages?

MY CONTRIBUTION
Worked individually on this remote lab. Authored the no-AI peer policy, built and verified `comps_model.py` against synthetic known answers, audited AI candidates (KO, KDP, MDLZ accepted; KHC qualified; ADM, MCD rejected), and calculated PepsiCo's implied trading ranges.

TEST / CHECK / RESULT
1. Synthetic Checkpoints: Reconciled all 5 known answers in `comps_model.py` (Median EV/EBITDA 13.0x, Median P/E 15.0x, EV/sh $15.80, P/E/sh $12.00, Precedent $17.40) -> ALL PASSED.
2. Borderline Peer Test: Removing KHC lifted median EV/EBITDA from 15.24x to 16.20x (+$11.55/sh) and median P/E from 20.24x to 20.91x (+$4.47/sh).
3. Implied Range: Full peer set = $133.61–$156.41/sh; Clean peer set = $138.08–$167.96/sh.

OPTIONAL ARTIFACT LINK
https://github.com/Dapize-Mo/FIN43900-AI-Finance-Applications/tree/main/labs/lab-07

ATTESTATION
I completed this work in today’s class with the teammate(s) listed above, and this checkout is truthful.

---

## 📌 Detailed Repository Evidence & Peer Data

### Verified Peer Financial Table (Sourced SEC & Market Data)

| Peer Company | Ticker | Enterprise Value ($M) | EBITDA ($M) | EV/EBITDA | Equity Value ($M) | Net Income ($M) | P/E | Status | Primary SEC Locator |
|---|---|---:|---:|---:|---:|---:|---:|:---:|---|
| **The Coca-Cola Company** | `KO` | $310,000 | $14,500 | **21.38×** | $285,000 | $10,700 | **26.64×** | Included | SEC Form 10-K p. 58 |
| **Keurig Dr Pepper Inc.** | `KDP` | $58,500 | $4,100 | **14.27×** | $44,000 | $2,250 | **19.56×** | Included | SEC Form 10-K p. 62 |
| **Mondelez International** | `MDLZ` | $115,000 | $7,100 | **16.20×** | $92,000 | $4,400 | **20.91×** | Included | SEC Form 10-K p. 64 |
| **The Kraft Heinz Company** | `KHC` | $56,000 | $6,400 | **8.75×** | $41,000 | $2,850 | **14.39×** | Borderline | SEC Form 10-K p. 55 |

* **PepsiCo Target Denominators (FY2024 10-K):** EBITDA = $16,500M | Net Income = $9,100M | Cash = $8,505M | Debt = $44,306M | Diluted Shares = 1,378M.
