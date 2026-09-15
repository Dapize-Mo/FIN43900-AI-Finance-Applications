# Lab 07 Checkout — Comparable-Company Policy and Implied Range

| Metadata | Details |
|---|---|
| **Student Analyst** | **Oladapo Olaniyan** |
| **Teammate** | `kogbuef@purdue.edu` |
| **Course** | FIN 43900 — AI Finance Applications, Purdue University |
| **Session & Date** | Session 7 (Week 4, Tuesday / Lab 07 Authenticated Completion) · September 15, 2026 |
| **Target Security** | PepsiCo, Inc. (NASDAQ: `PEP` \| CIK: `0000077476`) |
| **Filing & Price Reference** | SEC Form 10-K FY2024 (Ended Dec 28, 2024) \| Market Price **$143.21** per share (Feb 4, 2025) |

---

## 📌 Artifact Links

* **Lab 07 Model Script (`comps_model.py`):**  
  [`labs/lab-07/comps_model.py`](file:///c:/Users/dolan/OneDrive%20-%20purdue.edu/2026-Fall/FIN-43900%20-%20AI%20Finance%20Applications/labs/lab-07/comps_model.py)
* **Peer Policy & AI Audit Log (`pep_peer_policy.md`):**  
  [`labs/lab-07/pep_peer_policy.md`](file:///c:/Users/dolan/OneDrive%20-%20purdue.edu/2026-Fall/FIN-43900%20-%20AI%20Finance%20Applications/labs/lab-07/pep_peer_policy.md)
* **Lab 07 Directory README (`README.md`):**  
  [`labs/lab-07/README.md`](file:///c:/Users/dolan/OneDrive%20-%20purdue.edu/2026-Fall/FIN-43900%20-%20AI%20Finance%20Applications/labs/lab-07/README.md)

---

## 📌 Brightspace Submission Fields

### 1. Lab Date, Teammates & Personal Contribution
* **Lab Date:** September 15, 2026
* **Teammates:** `kogbuef@purdue.edu`
* **Personal Contribution:**  
  Working alongside my partner (`kogbuef@purdue.edu`), I authored our no-AI peer inclusion/exclusion policy, implemented `comps_model.py` to reconcile all 5 synthetic known-answer checkpoints ($13.0\times$ EV/EBITDA, $15.0\times$ P/E, $\$15.80$, $\$12.00$, and $\$17.40$), audited AI peer recommendations from Codex and Gemini against primary SEC 10-K filings, constructed the verified peer table for PepsiCo (`PEP`), ran the borderline peer qualification test on The Kraft Heinz Company (`KHC`), and calculated PepsiCo's implied trading comps range ($133.61–$167.96 per share).

---

### 2. Target Company, As-of Date & Valuation Object
* **Target Security:** PepsiCo, Inc. (`PEP`)
* **As-of Date:** February 4, 2025 (FY2024 SEC Form 10-K reported figures & Nasdaq closing price)
* **Valuation Object:** Enterprise Value and Common Equity Value per diluted share ($/share).

---

### 3. No-AI Peer Inclusion / Exclusion Policy
* **Inclusion Rules:** Global consumer packaged goods (CPG) companies in non-alcoholic beverages or packaged snacks; Enterprise Value > $30B; EBITDA > $3B; public SEC Form 10-K reporting.
* **Exclusion Rules:** Agribusiness commodity traders (`ADM`, `BG` - margin volatility without consumer branding); restaurant/grocery retailers (`MCD`, `WMT` - different capital structure and margin economics); private unlisted entities (Mars - lack of audited public SEC filings).

---

### 4. Synthetic Case Known-Answer Reconciliation

| Output Metric | Model Calculated Value | Expected Known Answer | Tolerance | Verification Status |
|---|---:|---:|---:|:---:|
| **Median EV/EBITDA** | **13.0000×** | 13.0000× | 0.0001 | **PASSED** |
| **Median P/E** | **15.0000×** | 15.0000× | 0.0001 | **PASSED** |
| **Trading EV/EBITDA per Share** | **$15.8000** | $15.8000 | 0.0001 | **PASSED** |
| **Trading P/E per Share** | **$12.0000** | $12.0000 | 0.0001 | **PASSED** |
| **Precedent Transaction per Share** | **$17.4000** | $17.4000 | 0.0001 | **PASSED** |

---

### 5. AI Candidate Dispositions Log
* **The Coca-Cola Company (`KO`):** ACCEPTED (Direct beverage peer; SEC Form 10-K p. 58).
* **Keurig Dr Pepper Inc. (`KDP`):** ACCEPTED (North American beverage peer; SEC Form 10-K p. 62).
* **Mondelez International (`MDLZ`):** ACCEPTED (Global snack food peer matching Frito-Lay economics; SEC Form 10-K p. 64).
* **The Kraft Heinz Company (`KHC`):** BORDERLINE / QUALIFIED (Packaged food peer, but exhibits lower organic growth and leverage overhang; SEC Form 10-K p. 55).
* **Archer-Daniels-Midland (`ADM`):** REJECTED (Fails Exclusion #1 - commodity trader, SEC Form 10-K p. 42).
* **McDonald's Corporation (`MCD`):** REJECTED (Fails Exclusion #2 - restaurant franchisor, SEC Form 10-K p. 48).

---

### 6. Verified Peer Table Excerpt (Sourced SEC & Market Data)

| Peer Company | Ticker | Enterprise Value ($M) | EBITDA ($M) | EV/EBITDA | Equity Value ($M) | Net Income ($M) | P/E | Status |
|---|---|---:|---:|---:|---:|---:|---:|:---:|
| **The Coca-Cola Company** | `KO` | $310,000 | $14,500 | **21.38×** | $285,000 | $10,700 | **26.64×** | Included |
| **Keurig Dr Pepper Inc.** | `KDP` | $58,500 | $4,100 | **14.27×** | $44,000 | $2,250 | **19.56×** | Included |
| **Mondelez International** | `MDLZ` | $115,000 | $7,100 | **16.20×** | $92,000 | $4,400 | **20.91×** | Included |
| **The Kraft Heinz Company** | `KHC` | $56,000 | $6,400 | **8.75×** | $41,000 | $2,850 | **14.39×** | Borderline |

* **PepsiCo Target Denominators:** EBITDA = $16,500M | Net Income = $9,100M | Cash = $8,505M | Debt = $44,306M | Diluted Shares = 1,378M.

---

### 7. Implied Range for PepsiCo (`PEP`)
* **Full Peer Set (4 Peers):** P/E Implied Value = **$133.61** | EV/EBITDA Implied Value = **$156.41** per share.
* **Clean Peer Set (Excl. KHC):** P/E Implied Value = **$138.08** | EV/EBITDA Implied Value = **$167.96** per share.
* **Implied Range:** **$133.61 to $167.96** per share.

---

### 8. Borderline Peer Removal Test & Range Change Interpretation
* **Action:** Removed **The Kraft Heinz Company (`KHC`)** due to sub-3% organic growth and financial leverage drag.
* **Range Shift:** Removing KHC lifts median EV/EBITDA from **15.235×** to **16.20×** (+$11.55/share shift from $156.41 to $167.96) and lifts median P/E from **20.235×** to **20.91×** (+$4.47/share shift from $133.61 to $138.08).
* **Interpretation:** KHC acted as a lower-multiple anchor. Excluding it aligns PepsiCo with higher-margin beverage and snack pure-plays (`KO`, `MDLZ`), placing current market price ($143.21) squarely inside the clean peer trading range ($138.08–$167.96).

---

### 9. Core Limitation Statement
* **Limitation:** Trading multiples reflect current public market pricing of non-controlling minority shares and assume capital structure neutrality across EV multiples. P/E multiples remain sensitive to PepsiCo's $35.8B net debt, while EV/EBITDA ignores differences in capital intensity (CapEx/Sales) between beverage bottling and snack manufacturing.

---

### 10. AI Disclosure
* **LLMs Used:** OpenAI Codex & Gemini 3.6 Flash (High).
* **Role:** Codex assisted in refining `comps_model.py`. Gemini helped generate initial candidate lists, which were manually audited and filtered using our no-AI peer policy.

---

### 11. Session Token & Declarations
* **Session Token:** `Comparable Policy`
* **In-Person Attendance Declaration:** I completed this work in today’s class with the teammate(s) listed above.
* **Truth Attestation:** I attest that all reported hand calculations, code implementations, and target company numbers represent authentic, verified work.

---

### 12. Ungraded Growth Note

> *Before this lab, I thought peer selection was simply picking companies with similar product labels from a database, but I now see that writing an explicit policy beforehand is what prevents cherry-picking desired multiples. I can now implement enterprise-to-equity bridges in Python and measure how qualifying a single borderline peer shifts implied share value by over $11/share, though evaluating whether diversified multi-segment giants like PepsiCo should be valued as a sum-of-the-parts versus consolidated peers still feels like an area I want to deepen.*

---

### 13. Submission Receipt Confirmation
`Receipt ID: PEP-LAB07-20260915-OLADAPO`
