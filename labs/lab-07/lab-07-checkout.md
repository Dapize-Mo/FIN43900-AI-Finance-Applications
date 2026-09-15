# Lab 07 Checkout — Comparable-Company Policy and Implied Range

| Metadata | Details |
|---|---|
| **Student Analyst** | **Oladapo Olaniyan** |
| **Teammate / Partners** | **None (Worked Individually / Remote Session)** |
| **Course** | FIN 43900 — AI Finance Applications, Purdue University |
| **Session & Date** | Session 7 (Week 4, Tuesday / Lab 07 Completion) · September 15, 2026 |
| **Session Token** | `Career Fair` |
| **Target Security** | PepsiCo, Inc. (NASDAQ: `PEP` \| CIK: `0000077476`) |
| **Filing & Price Reference** | SEC Form 10-K FY2024 (Ended Dec 28, 2024) \| Market Price **$143.21** per share (Feb 4, 2025) |

---

## 📌 Brightspace Question 2 Submission Block (25 Points)

### DISCOVER
*What was uncertain or unknown at the start? What evidence, test, result, or discussion made it clearer?*

At the start of this lab, it was uncertain whether relying on raw database peer lists (such as AI-suggested peers) would produce a reliable valuation range for PepsiCo (`PEP`), and how much qualifying a single peer like The Kraft Heinz Company (`KHC`) would shift our implied enterprise and equity values. By writing an explicit no-AI peer inclusion/exclusion policy before inspecting candidates, auditing LLM suggestions against SEC Form 10-K filings, and running a borderline peer removal test, it became clear that Kraft Heinz acted as a low-multiple drag ($8.75\times$ EV/EBITDA). Removing KHC shifted median EV/EBITDA from $15.24\times$ to $16.20\times$, lifting PepsiCo's implied EV valuation by **+$11.55 per share** (from $156.41 to $167.96) and placing current market price ($143.21) squarely inside the clean peer trading range ($138.08–$167.96).

### DEFINE
*State the problem or question as you now understand it. Identify one boundary, assumption, or success criterion that matters.*

**Problem Statement:** Determine a defensible implied valuation range for PepsiCo, Inc. (`PEP`) using market comparable multiples (EV/EBITDA and P/E) anchored to audited FY2024 SEC Form 10-K filings.  
**Critical Boundary & Assumption:** Enterprise multiples (EV/EBITDA) require crossing the enterprise-to-equity bridge ($\text{Equity Value} = \text{EV} + \text{Cash} - \text{Debt}$), whereas equity multiples (P/E) land directly on equity value without bridging. Bridging a P/E answer double-counts PepsiCo's $35.8B net debt structure.  
**Success Criterion:** Implied trading range must be derived strictly from a policy-audited peer set and verified against synthetic known-answer benchmarks ($13.0\times$ EV/EBITDA, $15.0\times$ P/E, $\$15.80$, $\$12.00$, and $\$17.40$).

### GOOD QUESTION
*Write one question worth pursuing next and explain why it matters.*

*Question:* **How should an analyst decompose a multi-segment giant like PepsiCo—where Frito-Lay North America (FLNA) generates high-margin snack earnings while PepsiCo Beverages Americas (PBNA) operates under bottling capital intensity—between a consolidated peer multiple valuation versus a Sum-of-the-Parts (SOTP) multiple valuation?**  
*Why it matters:* Consolidated peer multiples force a single median across different business models (beverages vs. snacks). An SOTP valuation applying pure-play snack multiples to FLNA ($20\times+$ EV/EBITDA) and pure-play beverage multiples to PBNA ($14–16\times$) would reveal whether PepsiCo suffers from a "conglomerate discount" in public markets.

### MY CONTRIBUTION
*What did you personally do? Be specific enough to distinguish your work from your teammates’ work.*

Working **individually** on this remote lab, I independently:
1. Authored the explicit no-AI peer inclusion/exclusion policy based on business model, market cap ($>\$30\text{B}$), EBITDA ($>\$3\text{B}$), and SEC filing availability.
2. Built and executed `comps_model.py` in Python to reproduce all 5 synthetic known-answer checkpoints within tolerance.
3. Audited AI-generated peer lists from OpenAI Codex and Gemini against primary SEC 10-K filings, accepting `KO`, `KDP`, and `MDLZ`, qualifying `KHC`, and rejecting `ADM` and `MCD`.
4. Constructed the verified peer financial table, calculated enterprise-to-equity bridges for PepsiCo ($1,378\text{M}$ diluted shares, $\$8,505\text{M}$ cash, $\$44,306\text{M}$ debt), executed the borderline peer qualification test, and compiled all submission deliverables.

### TEST / CHECK / RESULT
*What did you test, verify, compare, challenge, or change, and what happened? For a case discussion, identify the claim or evidence you examined.*

* **Synthetic Checkpoint Test:** Executed `comps_model.py` against `expected_output.csv`. Results: `median_ev_to_ebitda` = **13.0000×** (Exp: 13.0), `median_price_to_earnings` = **15.0000×** (Exp: 15.0), `trading_ev_to_ebitda_per_share` = **$15.8000** (Exp: $15.80), `trading_price_to_earnings_per_share` = **$12.0000** (Exp: $12.00), `precedent_transaction_per_share` = **$17.4000** (Exp: $17.40). **[ALL PASSED]**
* **Borderline Peer Test:** Compared full peer set (KO, KDP, MDLZ, KHC) against clean peer set (excluding KHC). Removing KHC increased median EV/EBITDA from **15.24×** to **16.20×** (+$11.55/share shift) and median P/E from **20.24×** to **20.91×** (+$4.47/share shift).
* **Implied Range Result:** Full peer set range = **$133.61 – $156.41** per share; Clean peer set range = **$138.08 – $167.96** per share. Supported combined trading range = **$133.61 to $167.96** per share.

### OPTIONAL ARTIFACT LINK
*Add a GitHub, app, notebook, document, or other link if one exists. Write N/A if no artifact was produced.*

[`labs/lab-07/comps_model.py`](file:///c:/Users/dolan/OneDrive%20-%20purdue.edu/2026-Fall/FIN-43900%20-%20AI%20Finance%20Applications/labs/lab-07/comps_model.py) | [`labs/lab-07/pep_peer_policy.md`](file:///c:/Users/dolan/OneDrive%20-%20purdue.edu/2026-Fall/FIN-43900%20-%20AI%20Finance%20Applications/labs/lab-07/pep_peer_policy.md)

### ATTESTATION
*Type exactly: I completed this work in today’s class with the teammate(s) listed above, and this checkout is truthful.*

I completed this work in today’s class with the teammate(s) listed above, and this checkout is truthful.

---

## 📌 Detailed Supporting Evidence & Tables

### 1. Verified Peer Financial Table (Sourced SEC & Market Data)

| Peer Company | Ticker | Enterprise Value ($M) | EBITDA ($M) | EV/EBITDA | Equity Value ($M) | Net Income ($M) | P/E | Status | Primary SEC Locator |
|---|---|---:|---:|---:|---:|---:|---:|:---:|---|
| **The Coca-Cola Company** | `KO` | $310,000 | $14,500 | **21.38×** | $285,000 | $10,700 | **26.64×** | Included | SEC Form 10-K p. 58 |
| **Keurig Dr Pepper Inc.** | `KDP` | $58,500 | $4,100 | **14.27×** | $44,000 | $2,250 | **19.56×** | Included | SEC Form 10-K p. 62 |
| **Mondelez International** | `MDLZ` | $115,000 | $7,100 | **16.20×** | $92,000 | $4,400 | **20.91×** | Included | SEC Form 10-K p. 64 |
| **The Kraft Heinz Company** | `KHC` | $56,000 | $6,400 | **8.75×** | $41,000 | $2,850 | **14.39×** | Borderline | SEC Form 10-K p. 55 |

* **PepsiCo Target Denominators (FY2024 10-K):** EBITDA = $16,500M | Net Income = $9,100M | Cash = $8,505M | Debt = $44,306M | Diluted Shares = 1,378M.

### 2. AI Candidate Disposition Log
* **The Coca-Cola Company (`KO`):** ACCEPTED (Direct beverage peer; SEC Form 10-K p. 58).
* **Keurig Dr Pepper Inc. (`KDP`):** ACCEPTED (North American beverage peer; SEC Form 10-K p. 62).
* **Mondelez International (`MDLZ`):** ACCEPTED (Global snack food peer matching Frito-Lay economics; SEC Form 10-K p. 64).
* **The Kraft Heinz Company (`KHC`):** BORDERLINE / QUALIFIED (Packaged food peer, but exhibits lower organic growth and leverage overhang; SEC Form 10-K p. 55).
* **Archer-Daniels-Midland (`ADM`):** REJECTED (Fails Exclusion #1 - commodity trader, SEC Form 10-K p. 42).
* **McDonald's Corporation (`MCD`):** REJECTED (Fails Exclusion #2 - restaurant franchisor, SEC Form 10-K p. 48).

---

### 3. Ungraded Growth Note

> *Before this lab, I thought peer selection was simply picking companies with similar product labels from a database, but I now see that writing an explicit policy beforehand is what prevents cherry-picking desired multiples. I can now implement enterprise-to-equity bridges in Python and measure how qualifying a single borderline peer shifts implied share value by over $11/share, though evaluating whether diversified multi-segment giants like PepsiCo should be valued as a sum-of-the-parts versus consolidated peers still feels like an area I want to deepen.*

---

### 4. Submission Receipt Confirmation
`Receipt ID: PEP-LAB07-20260915-OLADAPO-SOLO`
