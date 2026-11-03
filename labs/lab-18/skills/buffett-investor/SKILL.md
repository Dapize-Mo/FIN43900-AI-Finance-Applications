---
name: buffett-investor
description: Evaluates companies using Warren Buffett's philosophy by computing 5-year 10-K financial facts (ROE, owner earnings) keylessly from SEC EDGAR and delivering Buffett-style business memos. Use when asked to analyze a company using Buffett's criteria, calculate owner earnings, or assess business moats without stock price bias.
---

# Warren Buffett Legend Investor Skill

This skill executes Warren Buffett's foundational value-investing framework. It strictly adheres to the principle of **"numbers in code, judgment in the model"**:
- **Code computes every number** directly from primary SEC EDGAR 10-K XBRL facts.
- **The model provides narrative judgment only**, referencing strictly the printed numbers without hallucinating unprinted accounting metrics or price data.

## Rules Enforced by the Skill

1. **SEC EDGAR Keyless API**:
   - Company ticker mapping: `https://www.sec.gov/files/company_tickers.json`
   - Company facts: `https://data.sec.gov/api/xbrl/companyfacts/CIK##########.json`
   - User-Agent header: `Oladapo Olaniyan (oolaniy@purdue.edu)`
2. **10-K Only**: Facts are restricted to audited annual reports (`10-K`).
3. **1-Year Flow Window**: Revenue, Net Income, Operating Cash Flow, and CapEx require annual durations (~340 to 385 days).
4. **Latest Filing Wins**: If identical fiscal periods appear across multiple filings, the latest filing accession wins.
5. **XBRL Concept Precedence**:
   - Revenue: `RevenueFromContractWithCustomerExcludingAssessedTax`, then fallback to `Revenues`.
   - Net Income: `NetIncomeLoss`.
   - Operating Cash Flow: `NetCashProvidedByUsedInOperatingActivities`.
   - CapEx: `PaymentsToAcquirePropertyPlantAndEquipment`, then fallback to `PaymentsToAcquireProductiveAssets`.
   - Equity: `StockholdersEquity`.
6. **Owner Earnings**: `Operating Cash Flow - Capital Spending`.
7. **ROE**: `Net Income / Stockholders' Equity` (year-end equity).
8. **Missing Value Protocol**: If a tag is missing, print `"not found"` (never guess or estimate).
9. **Zero or Negative Equity**: If equity <= 0, ROE is `"not known"`.
10. **Missing Input Check Protocol**: If any input to a check is missing, the check evaluates to `"not known"`.

## Buffett's Three Core Checks (Computed in Code)

1. **ROE of 15% or more every year**: Pass if all 5 years have ROE >= 15.0%.
2. **Owner earnings positive every year**: Pass if all 5 years have Owner Earnings > 0.
3. **Owner earnings grew, first year to last**: Pass if Year 5 Owner Earnings > Year 1 Owner Earnings.

## Execution Procedure

When activated for a ticker:
1. Run the bundled script:
   ```bash
   python buffett_skill.py <TICKER>
   ```
2. Inspect the printed audited table and XBRL tag trail.
3. As Warren Buffett, draft a short memo (`<TICKER>_buffett_memo.md`) evaluating whether to **own the business**, **watch it**, or **pass**:
   - Judge the business quality and moat durability, **not the stock price** (no price or valuation data).
   - Use **only** numbers that the script printed.
   - If capital spending is `"not found"`, explicitly state that owner earnings cannot be judged (e.g. for financial institutions).
4. End with the student decision line explaining why the verdict is or is not trusted.
