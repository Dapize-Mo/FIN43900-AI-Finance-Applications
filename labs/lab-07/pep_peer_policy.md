# PepsiCo, Inc. (`PEP`) Peer Policy & Candidate Disposition Log

**Student Analyst:** Oladapo Olaniyan  
**Course:** FIN 43900 — AI Finance Applications, Purdue University  
**Target Security:** PepsiCo, Inc. (NASDAQ: `PEP` | CIK: `0000077476`)  
**Date:** September 15, 2026  

---

## 1. Explicit No-AI Peer Inclusion & Exclusion Policy

Before querying any LLM (Codex, Gemini) or screening databases, the following peer selection policy was established:

### Inclusion Criteria
1. **Business Model & Diversification:** Global commercialized consumer packaged goods (CPG) companies operating in non-alcoholic beverages and/or packaged snack foods.
2. **Capital Structure & Scale:** Enterprise Value > $30 Billion; proven global distribution network and brand moat.
3. **Financial Maturity & Cash Generation:** Consistently profitable, public reporting with audited SEC Form 10-K / IFRS filings, generating annual EBITDA > $3 Billion.
4. **Geography & Regulatory Context:** Multi-national sales presence across North America, Europe, and emerging markets.

### Exclusion Criteria
1. **Agribusiness & Commodity Traders:** Pure-play grain, agricultural processing, or ingredient traders (e.g., Archer-Daniels-Midland `ADM`, Bunge `BG`) due to extreme commodity margin volatility and lack of consumer brand equity.
2. **Retail Distributors & Restaurants:** Quick-service restaurant operators (e.g., McDonald's `MCD`, Yum! Brands `YUM`) or grocery retailers (e.g., Walmart `WMT`, Kroger `KR`) which operate under completely different margin structures and capital intensity.
3. **Private & Non-Public Entities:** Unlisted enterprise entities (e.g., Mars, Incorporated) lacking publicly filed quarterly/annual audited financial metrics.

---

## 2. AI Candidate Audit & Disposition Log

We prompted OpenAI Codex and Gemini 3.6 Flash independently with the exact inclusion/exclusion policy above. Below is the audited disposition of every suggested candidate:

| Candidate Suggested by AI | Ticker | AI Model | Verification Status | Human Policy Audit & Disposition | Primary Source SEC Locator / Date |
|---|---|---|:---:|---|---|
| **The Coca-Cola Company** | `KO` | Codex & Gemini | **ACCEPTED** | Primary direct competitor in non-alcoholic beverages. Matches scale, brand strength, and cash flow profile. | SEC Form 10-K FY2024 (p. 58) |
| **Keurig Dr Pepper Inc.** | `KDP` | Codex & Gemini | **ACCEPTED** | Direct liquid beverage peer in North America. Matches commercial economics despite lower international exposure. | SEC Form 10-K FY2024 (p. 62) |
| **Mondelez International, Inc.** | `MDLZ` | Codex & Gemini | **ACCEPTED** | Primary peer in global snack foods (biscuits, confectionery). Matches PepsiCo's Frito-Lay North America (FLNA) division economics. | SEC Form 10-K FY2024 (p. 64) |
| **The Kraft Heinz Company** | `KHC` | Gemini | **QUALIFIED / BORDERLINE** | Packaged food peer, but exhibits lower organic growth, higher financial leverage, and ongoing portfolio restructuring. Retained for full set, qualified in sensitivity test. | SEC Form 10-K FY2024 (p. 55) |
| **Archer-Daniels-Midland** | `ADM` | Codex | **REJECTED** | Fails Exclusion Rule #1 (Agribusiness/commodity trader). Margin structure tied to grain processing, not consumer branded products. | SEC Form 10-K FY2024 (p. 42) |
| **McDonald's Corporation** | `MCD` | Gemini | **REJECTED** | Fails Exclusion Rule #2 (Restaurant operator). Franchise model economics differ fundamentally from CPG beverage/snack manufacturing. | SEC Form 10-K FY2024 (p. 48) |

---

## 3. Verified Peer Financial Table (As-of Feb 2025 / FY2024 Filings)

| Company Name | Ticker | Enterprise Value ($M) | EBITDA ($M) | EV/EBITDA | Equity Value ($M) | Net Income ($M) | P/E | Inclusion Status |
|---|---|---:|---:|---:|---:|---:|---:|:---:|
| **The Coca-Cola Company** | `KO` | $310,000 | $14,500 | **21.38×** | $285,000 | $10,700 | **26.64×** | Core Included |
| **Keurig Dr Pepper Inc.** | `KDP` | $58,500 | $4,100 | **14.27×** | $44,000 | $2,250 | **19.56×** | Core Included |
| **Mondelez International** | `MDLZ` | $115,000 | $7,100 | **16.20×** | $92,000 | $4,400 | **20.91×** | Core Included |
| **The Kraft Heinz Company** | `KHC` | $56,000 | $6,400 | **8.75×** | $41,000 | $2,850 | **14.39×** | Borderline Peer |

* **Full Peer Set Medians (4 Peers):** Median EV/EBITDA = **15.235×** | Median P/E = **20.235×**  
* **Clean Peer Set Medians (Excl. KHC):** Median EV/EBITDA = **16.20×** | Median P/E = **20.91×**  

---

## 4. Borderline Peer Removal Test & Interpretation

### Test Setup
We qualify **The Kraft Heinz Company (`KHC`)** as a borderline peer. KHC trades at a depressed EV/EBITDA of 8.75× and P/E of 14.39× due to sluggish volume growth (-3.2% in FY2024) and high net debt relative to EBITDA. Removing KHC yields a core 3-peer set (`KO`, `KDP`, `MDLZ`).

### Implied Valuation Impact on PepsiCo (`PEP`)
* **PepsiCo Financial Denominators:** EBITDA = $16,500M | Net Income = $9,100M | Cash = $8,505M | Debt = $44,306M | Diluted Shares = 1,378M.

| Valuation Route | Full Peer Set (4 Peers) | Clean Peer Set (Excl. KHC) | Implied Value Shift ($/share) | Economic Interpretation |
|---|---:|---:|---:|---|
| **Trading EV/EBITDA** | **$156.41** per share | **$167.96** per share | **+$11.55** per share (+7.4%) | Removing KHC eliminates the drag of a low-multiple packaged food peer, aligning PepsiCo's EV/EBITDA closer to premium beverage/snack peers (`MDLZ`, `KO`). |
| **Trading P/E** | **$133.61** per share | **$138.08** per share | **+$4.47** per share (+3.3%) | Equity multiple shift reflects higher earnings quality of the core peer set without KHC's debt overhang. |

---

## 5. Peer Policy Conclusion & Method Disagreement

The trading comparables method yields an implied range of **$133.61 to $167.96** per share for PepsiCo. 

* **P/E vs. EV/EBITDA Disagreement:** Notice that P/E yields lower values ($133.61 – $138.08) than EV/EBITDA ($156.41 – $167.96). This occurs because PepsiCo carries substantial net debt ($35.8 Billion net debt; debt-to-EBITDA ~2.7×), causing interest expense ($771M in FY2024) to reduce net income. P/E incorporates this leverage drag directly, whereas EV/EBITDA isolates operating business profitability before capital structure effects.
