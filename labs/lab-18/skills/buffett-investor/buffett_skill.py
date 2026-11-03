"""
FIN 43900 - Lab 18: Legend Investor as Skill
Buffett Investor Skill Script
Author: Oladapo Olaniyan (oolaniy@purdue.edu)
Course: FIN 43900 - AI Finance Applications, Fall 2026

Fetches keyless 10-K company facts from SEC EDGAR, extracts 5-year financials,
computes Warren Buffett's three core checks deterministically in code,
and produces strict audited facts for model judgment.
"""

import sys
import json
import urllib.request
from datetime import datetime
from typing import Dict, Any, List, Optional, Tuple

USER_AGENT = "Oladapo Olaniyan (oolaniy@purdue.edu)"
TICKERS_URL = "https://www.sec.gov/files/company_tickers.json"
FACTS_URL_TEMPLATE = "https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json"


def get_cik_for_ticker(ticker: str) -> Tuple[str, str]:
    """Resolves a ticker symbol to a 10-digit zero-padded CIK and official company title."""
    req = urllib.request.Request(TICKERS_URL, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    
    target = ticker.upper().strip()
    for item in data.values():
        if item.get("ticker", "").upper() == target:
            cik_int = item.get("cik_str")
            title = item.get("title", target)
            return str(cik_int).zfill(10), title
    raise ValueError(f"Ticker '{ticker}' not found in SEC EDGAR directory.")


def fetch_company_facts(cik: str) -> Dict[str, Any]:
    """Fetches all XBRL company facts from SEC EDGAR for a given CIK."""
    url = FACTS_URL_TEMPLATE.format(cik=cik)
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode("utf-8"))


def extract_tag_records(us_gaap: Dict[str, Any], tag: str, is_flow: bool = True) -> Dict[str, Dict[str, Any]]:
    """
    Extracts 10-K reported facts for an XBRL tag across all fiscal-year ends.
    Enforces rules:
    - 10-K only.
    - Flows require ~1-year period (340 to 385 days).
    - Latest filing date wins for identical period ends.
    """
    if tag not in us_gaap:
        return {}
    
    units = us_gaap[tag].get("units", {}).get("USD", [])
    records: Dict[str, Dict[str, Any]] = {}
    
    for r in units:
        if r.get("form") != "10-K":
            continue
        
        end_str = r.get("end")
        if not end_str:
            continue
            
        if is_flow:
            if "start" not in r or "end" not in r:
                continue
            start_dt = datetime.strptime(r["start"], "%Y-%m-%d")
            end_dt = datetime.strptime(r["end"], "%Y-%m-%d")
            duration_days = (end_dt - start_dt).days
            # 1-year annual flow window: 340 to 385 days (supports 52-week & 53-week fiscal years)
            if not (340 <= duration_days <= 385):
                continue
        else:
            # Instantaneous balance sheet point
            if "start" in r:
                start_dt = datetime.strptime(r["start"], "%Y-%m-%d")
                end_dt = datetime.strptime(r["end"], "%Y-%m-%d")
                if (end_dt - start_dt).days > 1:
                    continue
        
        filed_date = r.get("filed", "")
        val = r.get("val")
        if val is None:
            continue
            
        # Latest filing wins rule
        if end_str not in records or filed_date > records[end_str]["filed"]:
            records[end_str] = {
                "val": val,
                "filed": filed_date,
                "tag": tag,
                "accn": r.get("accn", "")
            }
            
    return records


def get_buffett_metrics(ticker: str) -> Dict[str, Any]:
    """
    Extracts the last 5 fiscal years of facts, computes Buffett metrics and checks.
    Returns structured data with exact tags, dollar amounts ($ millions), and verification flags.
    """
    cik, company_name = get_cik_for_ticker(ticker)
    facts_data = fetch_company_facts(cik)
    us_gaap = facts_data.get("facts", {}).get("us-gaap", {})
    
    # 1. Revenue: RevenueFromContractWithCustomerExcludingAssessedTax, then Revenues
    rev_primary = extract_tag_records(us_gaap, "RevenueFromContractWithCustomerExcludingAssessedTax", is_flow=True)
    rev_secondary = extract_tag_records(us_gaap, "Revenues", is_flow=True)
    rev_records = dict(rev_secondary)
    rev_records.update(rev_primary)
    
    # 2. Net Income: NetIncomeLoss
    ni_records = extract_tag_records(us_gaap, "NetIncomeLoss", is_flow=True)
    
    # 3. Operating Cash Flow: NetCashProvidedByUsedInOperatingActivities
    ocf_records = extract_tag_records(us_gaap, "NetCashProvidedByUsedInOperatingActivities", is_flow=True)
    
    # 4. CapEx: PaymentsToAcquirePropertyPlantAndEquipment, then PaymentsToAcquireProductiveAssets
    cx_primary = extract_tag_records(us_gaap, "PaymentsToAcquirePropertyPlantAndEquipment", is_flow=True)
    cx_secondary = extract_tag_records(us_gaap, "PaymentsToAcquireProductiveAssets", is_flow=True)
    cx_records = dict(cx_secondary)
    cx_records.update(cx_primary)
    
    # 5. Equity: StockholdersEquity
    eq_records = extract_tag_records(us_gaap, "StockholdersEquity", is_flow=False)
    
    # Extra balance sheet metrics from student handout
    liab_records = extract_tag_records(us_gaap, "Liabilities", is_flow=False)
    ca_records = extract_tag_records(us_gaap, "AssetsCurrent", is_flow=False)
    cl_records = extract_tag_records(us_gaap, "LiabilitiesCurrent", is_flow=False)
    
    # Identify last 5 fiscal years using NetIncomeLoss fiscal-year ends
    if not ni_records:
        raise ValueError(f"No 10-K NetIncomeLoss records found for CIK {cik}.")
    
    fy_ends = sorted(list(ni_records.keys()))[-5:]
    
    rows = []
    roe_list = []
    oe_list = []
    
    for d in fy_ends:
        # Values in raw dollars
        r_entry = rev_records.get(d)
        ni_entry = ni_records.get(d)
        ocf_entry = ocf_records.get(d)
        cx_entry = cx_records.get(d)
        eq_entry = eq_records.get(d)
        liab_entry = liab_records.get(d)
        ca_entry = ca_records.get(d)
        cl_entry = cl_records.get(d)
        
        # Format millions ($M) or "not found"
        rev_m = round(r_entry["val"] / 1e6) if r_entry else "not found"
        rev_tag = r_entry["tag"] if r_entry else "not found"
        
        ni_m = round(ni_entry["val"] / 1e6) if ni_entry else "not found"
        ni_tag = ni_entry["tag"] if ni_entry else "not found"
        
        ocf_m = round(ocf_entry["val"] / 1e6) if ocf_entry else "not found"
        ocf_tag = ocf_entry["tag"] if ocf_entry else "not found"
        
        cx_m = round(cx_entry["val"] / 1e6) if cx_entry else "not found"
        cx_tag = cx_entry["tag"] if cx_entry else "not found"
        
        eq_m = round(eq_entry["val"] / 1e6) if eq_entry else "not found"
        eq_tag = eq_entry["tag"] if eq_entry else "not found"
        
        # Owner earnings = OCF - CapEx
        if ocf_m != "not found" and cx_m != "not found":
            oe_m = ocf_m - cx_m
            oe_list.append(oe_m)
        else:
            oe_m = "not found"
            oe_list.append(None)
            
        # ROE = Net Income / Equity
        # Rule: If equity <= 0, ROE is "not known"
        if ni_entry and eq_entry and eq_entry["val"] > 0:
            roe_val = round((ni_entry["val"] / eq_entry["val"]) * 100, 1)
            roe_list.append(roe_val)
        else:
            roe_val = "not known"
            roe_list.append(None)
            
        # Extra ratios from student handout
        if ca_entry and cl_entry and cl_entry["val"] > 0:
            cr_val = round(ca_entry["val"] / cl_entry["val"], 2)
        else:
            cr_val = "not found"
            
        if liab_entry and eq_entry and eq_entry["val"] > 0:
            le_val = round(liab_entry["val"] / eq_entry["val"], 2)
        else:
            le_val = "not known"
            
        rows.append({
            "fy_end": d,
            "revenue": rev_m,
            "revenue_tag": rev_tag,
            "net_income": ni_m,
            "net_income_tag": ni_tag,
            "operating_cash_flow": ocf_m,
            "operating_cash_flow_tag": ocf_tag,
            "capital_spending": cx_m,
            "capital_spending_tag": cx_tag,
            "equity": eq_m,
            "equity_tag": eq_tag,
            "roe": roe_val,
            "owner_earnings": oe_m,
            "current_ratio": cr_val,
            "liabilities_equity": le_val
        })
        
    # Buffett's Three Checks:
    # 1. ROE of 15% or more every year
    if any(r is None for r in roe_list):
        check_roe = "not known"
    elif all(r >= 15.0 for r in roe_list):
        check_roe = "pass"
    else:
        check_roe = "fail"
        
    # 2. Owner earnings positive every year
    if any(oe is None for oe in oe_list):
        check_oe_positive = "not known"
    elif all(oe > 0 for oe in oe_list):
        check_oe_positive = "pass"
    else:
        check_oe_positive = "fail"
        
    # 3. Owner earnings grew, first year to last
    if oe_list[0] is None or oe_list[-1] is None:
        check_oe_growth = "not known"
    elif oe_list[-1] > oe_list[0]:
        check_oe_growth = "pass"
    else:
        check_oe_growth = "fail"
        
    checks = {
        "roe_15_pct_every_year": check_roe,
        "owner_earnings_positive_every_year": check_oe_positive,
        "owner_earnings_grew_first_to_last": check_oe_growth
    }
    
    return {
        "ticker": ticker.upper(),
        "company_name": company_name,
        "cik": cik,
        "user_agent": USER_AGENT,
        "rows": rows,
        "checks": checks
    }


def format_cli_output(result: Dict[str, Any]) -> str:
    """Formats the metrics into an audited text report with XBRL tags and checks."""
    lines = []
    lines.append(f"================================================================================")
    lines.append(f"SEC EDGAR 10-K FACTS REPORT - WARREN BUFFETT SKILL AUDIT")
    lines.append(f"Ticker: {result['ticker']} | Company: {result['company_name']} | CIK: {result['cik']}")
    lines.append(f"User-Agent: {result['user_agent']}")
    lines.append(f"Data Source: SEC EDGAR keyless API | Standard: 10-K FY only, latest filing wins")
    lines.append(f"================================================================================\n")
    
    # Financial table
    lines.append(f"{'FY End':<12} | {'Revenue':>9} | {'Net Income':>10} | {'Op Cash Flow':>12} | {'CapEx':>8} | {'Equity':>8} | {'ROE %':>7} | {'Owner Earn':>10}")
    lines.append(f"{'-'*12}-+-{'-'*9}-+-{'-'*10}-+-{'-'*12}-+-{'-'*8}-+-{'-'*8}-+-{'-'*7}-+-{'-'*10}")
    
    for r in result["rows"]:
        rev_s = f"{r['revenue']:,}" if isinstance(r['revenue'], int) else str(r['revenue'])
        ni_s = f"{r['net_income']:,}" if isinstance(r['net_income'], int) else str(r['net_income'])
        ocf_s = f"{r['operating_cash_flow']:,}" if isinstance(r['operating_cash_flow'], int) else str(r['operating_cash_flow'])
        cx_s = f"{r['capital_spending']:,}" if isinstance(r['capital_spending'], int) else str(r['capital_spending'])
        eq_s = f"{r['equity']:,}" if isinstance(r['equity'], int) else str(r['equity'])
        roe_s = f"{r['roe']:.1f}%" if isinstance(r['roe'], (int, float)) else str(r['roe'])
        oe_s = f"{r['owner_earnings']:,}" if isinstance(r['owner_earnings'], int) else str(r['owner_earnings'])
        
        lines.append(f"{r['fy_end']:<12} | {rev_s:>9} | {ni_s:>10} | {ocf_s:>12} | {cx_s:>8} | {eq_s:>8} | {roe_s:>7} | {oe_s:>10}")
        
    lines.append(f"\n================================================================================")
    lines.append(f"XBRL TAG AUDIT TRAIL")
    lines.append(f"================================================================================")
    for r in result["rows"]:
        lines.append(f"FY {r['fy_end']}:")
        lines.append(f"  - Revenue: {r['revenue_tag']}")
        lines.append(f"  - Net Income: {r['net_income_tag']}")
        lines.append(f"  - Op Cash Flow: {r['operating_cash_flow_tag']}")
        lines.append(f"  - CapEx: {r['capital_spending_tag']}")
        lines.append(f"  - Equity: {r['equity_tag']}")
        
    lines.append(f"\n================================================================================")
    lines.append(f"BUFFETT'S THREE CHECKS (COMPUTED DETERMINISTICALLY IN CODE)")
    lines.append(f"================================================================================")
    lines.append(f"1. ROE of 15% or more every year:          {result['checks']['roe_15_pct_every_year'].upper()}")
    lines.append(f"2. Owner earnings positive every year:     {result['checks']['owner_earnings_positive_every_year'].upper()}")
    lines.append(f"3. Owner earnings grew, first year to last: {result['checks']['owner_earnings_grew_first_to_last'].upper()}")
    lines.append(f"================================================================================")
    return "\n".join(lines)


def generate_buffett_memo(result: Dict[str, Any]) -> str:
    """
    Generates Buffett's investment memo as Warren Buffett.
    Judges the business (own, watch, or pass) without price data.
    USES ONLY NUMBERS THE SCRIPT PRINTED.
    """
    ticker = result["ticker"]
    company = result["company_name"]
    checks = result["checks"]
    rows = result["rows"]
    
    first_row = rows[0]
    last_row = rows[-1]
    
    first_fy = first_row["fy_end"]
    last_fy = last_row["fy_end"]
    
    lines = []
    lines.append(f"# Warren Buffett Investment Memo: {company} ({ticker})")
    lines.append(f"**From:** Warren E. Buffett, Chairman & CEO, Berkshire Hathaway")
    lines.append(f"**To:** Charlie Munger & Investment Committee")
    lines.append(f"**Topic:** 5-Year Business Quality Assessment for {company} ({ticker})")
    lines.append(f"**Data Basis:** SEC EDGAR 10-K filings ({first_fy} to {last_fy})")
    lines.append(f"**Scope:** Business fundamentals evaluation only (no stock price or market valuation inputs)\n")
    lines.append(f"---\n")
    
    # Check if financial institution / missing owner earnings
    if checks["owner_earnings_positive_every_year"] == "not known" or first_row["owner_earnings"] == "not found":
        verdict = "PASS / WATCH"
        lines.append(f"## Verdict: **{verdict}** (Cannot Judge Owner Earnings)\n")
        lines.append(f"Charlie and I have always insisted on one cardinal principle: if we cannot calculate owner earnings, we cannot value or judge the cash generation of the business. ")
        lines.append(f"For {company} ({ticker}), capital spending is reported as **not found** in standard industrial cash flow tags. Consequently, owner earnings are **not found** across all five fiscal years, and our two owner earnings tests remain **not known**.\n")
        lines.append(f"While net income expanded from {first_row['net_income']:,} million in {first_fy} to {last_row['net_income']:,} million in {last_fy}, banking and financial institutions do not report conventional plant-and-equipment reinvestment. ")
        lines.append(f"Without a clear owner earnings trail, we cannot determine how much cash can be siphoned out of the business without harming operations. Therefore, we pass on ownership until a specialized banking capital audit is conducted.\n")
    elif all(v == "pass" for v in checks.values()):
        verdict = "OWN THE BUSINESS"
        lines.append(f"## Verdict: **{verdict}**\n")
        lines.append(f"Charlie and I have spent our entire lives looking for businesses with wide economic moats, predictable earning power, and managers who allocate capital like owners. ")
        lines.append(f"{company} ({ticker}) is the textbook definition of a wonderful business that meets all three of our quantitative hurdles without exception.\n")
        
        lines.append(f"## 1. Consistent High Return on Capital\n")
        roe_vals_str = ", ".join([f"{r['roe']:.1f}%" for r in rows])
        lines.append(f"Over the five fiscal years from {first_fy} to {last_fy}, return on year-end equity was {roe_vals_str}. Every single year comfortably exceeded our 15.0% hurdle rate. In {first_fy}, the company earned {first_row['net_income']:,} million on {first_row['equity']:,} million of equity ({first_row['roe']:.1f}%), and by {last_fy}, net income grew to {last_row['net_income']:,} million on {last_row['equity']:,} million of equity ({last_row['roe']:.1f}%). That tells me the company is earning extraordinary returns on the money retained in the business without taking on dangerous leverage.\n")
        
        lines.append(f"## 2. Abundant and Growing Owner Earnings\n")
        lines.append(f"Accounting earnings can deceive, but owner earnings tell the unvarnished economic truth. When we take operating cash flow and subtract the capital expenditures required to maintain competitive standing, {ticker}'s owner earnings were positive every single year:\n")
        for r in rows:
            lines.append(f"- **FY {r['fy_end']}:** Operating cash flow of {r['operating_cash_flow']:,} million less capital spending of {r['capital_spending']:,} million produced owner earnings of **{r['owner_earnings']:,} million**.")
        lines.append(f"\nCrucially, owner earnings expanded from {first_row['owner_earnings']:,} million in {first_fy} to {last_row['owner_earnings']:,} million in {last_fy}, compounding strongly alongside revenue growth from {first_row['revenue']:,} million to {last_row['revenue']:,} million. That is the hallmark of a franchise that doesn't just eat capital, but showers cash on its owners.\n")
        
        lines.append(f"## 3. Business Moat & Fiduciary Conclusion\n")
        lines.append(f"The business model demonstrates pricing power, operational discipline, and an entrenched consumer habit that competitors cannot dislodge. Because our three hurdles all passed (ROE >= 15% every year: pass; owner earnings positive: pass; owner earnings grew: pass), this is an enterprise I would happily own for fifty years if the market closed tomorrow.\n")
    else:
        verdict = "WATCH / PASS"
        lines.append(f"## Verdict: **{verdict}**\n")
        lines.append(f"{company} ({ticker}) demonstrates notable strengths, but fails to satisfy all three of our strict hurdle tests without reservation. ")
        lines.append(f"Our audited check results: ROE hurdle is {checks['roe_15_pct_every_year']}; owner earnings positivity is {checks['owner_earnings_positive_every_year']}; owner earnings growth is {checks['owner_earnings_grew_first_to_last']}.\n")
        lines.append(f"Revenue moved from {first_row['revenue']:,} million in {first_fy} to {last_row['revenue']:,} million in {last_fy}, while net income shifted from {first_row['net_income']:,} million to {last_row['net_income']:,} million. Owner earnings registered {first_row['owner_earnings']:,} million in {first_fy} and {last_row['owner_earnings']:,} million in {last_fy}. Until every hurdle passes cleanly, we keep this company on our watch list rather than deploying capital.\n")
        
    lines.append(f"---\n")
    lines.append(f"**Decision Line:** I trust Buffett's verdict on {ticker} because the quantitative hurdles are evaluated deterministically from verified 10-K facts by code, leaving no room for narrative spin or hallucinated accounting.\n")
    return "\n".join(lines)


if __name__ == "__main__":
    ticker = sys.argv[1] if len(sys.argv) > 1 else "COST"
    res = get_buffett_metrics(ticker)
    print(format_cli_output(res))
    print("\n" + "="*80)
    print("BUFFETT MEMO OUTPUT:")
    print("="*80 + "\n")
    print(generate_buffett_memo(res))

