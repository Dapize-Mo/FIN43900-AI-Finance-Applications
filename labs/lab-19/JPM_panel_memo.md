# Legend Panel Audit Report: JPMORGAN CHASE & CO (JPM)
**Date:** November 5, 2026 | **Student:** Oladapo Olaniyan (oolaniy@purdue.edu)  
**Course:** FIN 43900 — AI Finance Applications, Daniels School of Business, Purdue University  
**Data Source:** SEC EDGAR 10-K Primary Audited Facts (Latest Filing Wins)  

---

## 1. Panel Table: Investor × Check
| Investor | Check Description | Status | Evidence |
|---|---|---|---|
| Buffett | ROE of 15% or more every year | **FAIL** | 5-yr ROE: 16.4%, 12.9%, 15.1%, 17.0%, 15.7% |
| Buffett | Owner earnings positive every year | **NOT KNOWN** | 5-yr OE: None, None, None, None, None |
| Buffett | Owner earnings grew, first year to last | **NOT KNOWN** | Missing OE |
| Graham | Current ratio of 2.0 or more, latest year | **NOT KNOWN** | Missing CR |
| Graham | Net income positive every year | **PASS** | 5-yr NI: 48,334M, 37,676M, 49,552M, 58,471M, 57,048M |
| Graham | Net income grew, first year to last | **PASS** | NI Y1: 48,334M -> Y5: 57,048M |
| Burry | Operating cash flow at least net income every year | **FAIL** | OCF >= NI checked for all 5 years |
| Burry | Liabilities no more than twice equity, latest year | **FAIL** | Latest Liab/Eq: 11.21 (Hurdle: <= 2.0) |

---

## 2. Warren Buffett Memo
# Warren Buffett Investment Memo: JPMORGAN CHASE & CO (JPM)
**From:** Warren E. Buffett, Berkshire Hathaway
**To:** Charlie Munger & Investment Committee
**Topic:** 5-Year Business Quality Assessment for JPMORGAN CHASE & CO (JPM)
**Data Basis:** SEC EDGAR 10-K filings (2021-12-31 to 2025-12-31)
**Scope:** Business fundamentals only (no stock price or market valuation inputs)

---

## Verdict: **PASS / WATCH (CANNOT JUDGE)**

Charlie and I insist on one cardinal rule: if we cannot calculate owner earnings, we cannot judge the cash generation of the enterprise. 
For JPMORGAN CHASE & CO (JPM), capital spending is reported as **not found** in standard industrial cash flow tags. Consequently, owner earnings are **not found** across all five fiscal years, and our two owner earnings tests remain **not known**.

Net income moved from 48,334 million in 2021-12-31 to 57,048 million in 2025-12-31. However, without plant-and-equipment reinvestment data, owner cash flow cannot be determined. Therefore, we pass on ownership until specialized banking capital analysis is performed.


---

## 3. Benjamin Graham Memo
# Benjamin Graham Investment Memo: JPMORGAN CHASE & CO (JPM)
**From:** Benjamin Graham, Security Analyst
**To:** Investment Committee & Serious Investors
**Topic:** Balance Sheet Margin of Safety & Earnings Stability Review
**Data Basis:** SEC EDGAR 10-K reported facts (2021-12-31 to 2025-12-31)
**Scope:** Defensive investor appraisal based on primary balance sheet and income statements

---

## Verdict: **INSUFFICIENT DATA / WATCH**

### 1. Working Capital Margin of Safety (Current Ratio)

Working capital metrics are **not found** in reported 10-K filings. Therefore, liquidity condition remains **not known**.

### 2. Earnings Stability & Ten-Year Trend

Over the five reported fiscal years, net income was 48,334 million, 37,676 million, 49,552 million, 58,471 million, 57,048 million. 
Earnings were positive in all five fiscal years, fulfilling our stability requirement. 
Furthermore, net income expanded from 48,334 million in 2021-12-31 to 57,048 million in 2025-12-31, demonstrating legitimate earnings growth across the cycle.

### 3. Quantitative Disposition & Threshold Design Choice

Working capital data is reported as **not found** in reported 10-K filings for JPMORGAN CHASE & CO. Without reported current assets and liabilities, Graham's liquidity screen cannot be executed and remains **not known**.

**Threshold Decision:** Graham threshold kept at 2.0 (classical defensive investor margin of safety); lowered to 1.0 for capital-efficient negative-working-capital retailers like Costco.


---

## 4. Michael Burry Memo
# Michael Burry Forensic Memo: JPMORGAN CHASE & CO (JPM)
**From:** Michael Burry, Scion Asset Management
**To:** Scion Investment Committee & Fund Partners
**Topic:** 10-K Forensic Accounting, Cash Conversion & Leverage Audit
**Data Basis:** SEC EDGAR 10-K primary audited statements (2021-12-31 to 2025-12-31)
**Scope:** Forensic divergence between reported net income and cash flow, plus debt cushion

---

## Verdict: **FAIL FORENSIC SCREEN**

### 1. Earnings Quality: Operating Cash Flow vs. Net Income

Reported accounting income is a narrative crafted by management. Cash flow is the cold, hard reality. We compare Operating Cash Flow (OCF) directly to Net Income (NI) for every period:

- **FY 2021-12-31:** Operating Cash Flow of 78,084 million vs. Net Income of 48,334 million.
- **FY 2022-12-31:** Operating Cash Flow of 107,119 million vs. Net Income of 37,676 million.
- **FY 2023-12-31:** Operating Cash Flow of 12,974 million vs. Net Income of 49,552 million.
- **FY 2024-12-31:** Operating Cash Flow of -42,012 million vs. Net Income of 58,471 million.
- **FY 2025-12-31:** Operating Cash Flow of -147,782 million vs. Net Income of 57,048 million.

Operating cash flow lagged reported net income in one or more years. When cash generation trails reported accounting earnings, accruals are inflating profits, indicating earnings quality deterioration.

### 2. Balance Sheet Cushion: Total Liabilities vs. Equity

In FY 2025-12-31, total liabilities stood at 4,062,462 million against stockholders' equity of 362,438 million, resulting in a liabilities-to-equity ratio of **11.21**.

This **fails** our forensic ceiling of 2.0. Total liabilities exceed twice the equity base, creating elevated financial risk and reducing margin of error.

### 3. Contrarian Synthesis

One or more forensic hurdles failed. Consensus Wall Street ignores these structural discrepancies, but our quantitative audit identifies material risk.
