# Primary Source Deal Audit — Broadcom / VMware & CPG Sector Precedents

**Student Analyst:** Oladapo Olaniyan  
**Course:** FIN 43900 — AI Finance Applications, Purdue University  
**Target Security:** PepsiCo, Inc. (`PEP`) | Transaction Audit Reference  
**Date:** September 15, 2026  

---

## 1. Broadcom / VMware Source Packet Audit

### Primary Source Map & Verified Terms

| Primary SEC / Official Document Source | Verified Announcement Date & Terms | Valuation Classification & Caution |
|---|---|---|
| [Broadcom Form 8-K (May 26, 2022)](https://www.sec.gov/Archives/edgar/data/1730168/000119312522161016/d525235d8k.htm) | VMware shareholders could elect **$142.50 cash** or **0.2520 Broadcom shares** per VMware share, subject to 50/50 aggregate proration. | **Equity Consideration.** Stock leg valuation is anchored to Broadcom's share price on May 25, 2022 ($531.63). Must not be confused with Enterprise Value. |
| [Broadcom Press Release (Exhibit 99.1)](https://www.sec.gov/Archives/edgar/data/1124610/00011931252216168/d362256dex991.htm) | Announced **~$61 Billion transaction equity value** plus assumption of **~$8 Billion VMware net debt**. Headline combined transaction value = **~$69 Billion**. | **Enterprise-Value-Like Bridge.** Sum of equity purchase price + assumed net debt. Subject to working capital and final cash adjustments. |
| [Broadcom Close Release (Nov 22, 2023)](https://investors.broadcom.com/news-releases/news-release-details/broadcom-completes-acquisition-vmware) | Acquisition completed following regulatory approvals; VMware stock ceased trading on NYSE. | **Status Confirmation.** Proves transaction closing; does not retroactively change announcement market inputs. |

---

### 2. Transaction Value Bridge

$$\begin{aligned}
\text{Stated Transaction Equity Value} &= \mathbf{\$61.0 \text{ Billion}} \\
\text{Plus Assumed Net Debt} &= \mathbf{+\$8.0 \text{ Billion}} \\
\hline
\text{Headline Enterprise Value (EV)} &= \mathbf{\$69.0 \text{ Billion}}
\end{aligned}$$

---

### 3. Denominator Rejection Rationale (Critical Audit Finding)

> [!CAUTION]
> **REJECTION OF PRO FORMA $8.5B EBITDA DENOMINATOR**  
> * **Tempting Denominator:** Press release Exhibit 99.1 mentions an estimated **$8.5 Billion** of pro forma EBITDA.  
> * **Reason for Rejection:** The $8.5B figure represents the **expected combined pro forma EBITDA contribution 3 years post-closing** (including cost synergies and software licensing transition), **NOT** VMware’s historical LTM EBITDA at announcement (~$4.7B).  
> * **Valuation Flaw:** Dividing the $69B headline EV by $8.5B yields an artificially low multiple of **8.12×**. Using forward post-synergy pro forma EBITDA in the denominator double-counts synergy value that the buyer has yet to realize.  
> * **Correct Multiple:** Based on true LTM EBITDA (~$4.7B), VMware's true transaction EV/EBITDA multiple was **~14.68×**.

---

## 4. Consumer Packaged Goods (CPG) Precedent Deal Audit

For PepsiCo (`PEP`), we audited the most relevant consumer packaged goods precedent transaction: **Mars, Incorporated acquisition of Kellanova (`K`)** announced in August 2024.

### Mars / Kellanova Deal Terms & Context
* **Announcement Date:** August 14, 2024
* **Offer Price:** $83.50 per share in cash.
* **Implied Enterprise Value:** **$35.9 Billion** (Equity Value $29.7B + Net Debt $6.2B).
* **Target LTM EBITDA:** ~$2.19 Billion.
* **Implied Precedent EV/EBITDA Multiple:** **16.40×**
* **Control & Synergy Context:** Mars paid a **33% premium** over Kellanova's unaffected 50-day VWAP. The 16.4x multiple includes a substantial control premium for 100% ownership and distribution scale synergies in global snacking.
* **Comparability to PepsiCo:** High business model comparability (packaged snacks & cereal, global distribution). However, 100% acquisition control premiums (16.4x) should not be applied directly to non-controlling minority public shares without haircutting for control value.
