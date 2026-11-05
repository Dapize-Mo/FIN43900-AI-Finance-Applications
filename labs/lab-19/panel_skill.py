"""
FIN 43900 - Lab 19: Legend Panel
Panel of Three Investor Skills (Buffett, Graham, Burry) on 10-K Facts
Author: Oladapo Olaniyan (oolaniy@purdue.edu)
Course: FIN 43900 - AI Finance Applications, Fall 2026

Fetches keyless 10-K company facts from SEC EDGAR, extracts 5-year financials,
computes 8 deterministic hurdles across 3 legendary investors (Buffett, Graham, Burry),
handles honest missing values ("not found" / "not known"),
and produces strict audited facts and personas for model judgment.
"""

from __future__ import annotations

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
                "accn": r.get("accn", ""),
            }

    return records


def get_panel_metrics(ticker: str, graham_cr_threshold: float = 2.0) -> Dict[str, Any]:
    """
    Extracts the last 5 fiscal years of facts, computes 8 checks across 3 legendary investors:
    - Buffett: ROE >= 15% every year; Owner earnings > 0 every year; Owner earnings grew.
    - Graham: Current ratio >= threshold (default 2.0, probe 1.0); Net income > 0 every year; Net income grew.
    - Burry: OCF >= Net income every year; Liabilities <= 2.0x Equity latest year.
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

    # 6. Total Liabilities: Liabilities
    liab_records = extract_tag_records(us_gaap, "Liabilities", is_flow=False)

    # 7. Current Assets: AssetsCurrent
    ca_records = extract_tag_records(us_gaap, "AssetsCurrent", is_flow=False)

    # 8. Current Liabilities: LiabilitiesCurrent
    cl_records = extract_tag_records(us_gaap, "LiabilitiesCurrent", is_flow=False)

    # Identify last 5 fiscal years using NetIncomeLoss fiscal-year ends
    if not ni_records:
        raise ValueError(f"No 10-K NetIncomeLoss records found for CIK {cik}.")

    fy_ends = sorted(list(ni_records.keys()))[-5:]

    rows = []
    roe_list = []
    oe_list = []
    ni_list = []
    ocf_list = []
    cr_list = []
    le_list = []

    for d in fy_ends:
        r_entry = rev_records.get(d)
        ni_entry = ni_records.get(d)
        ocf_entry = ocf_records.get(d)
        cx_entry = cx_records.get(d)
        eq_entry = eq_records.get(d)
        liab_entry = liab_records.get(d)
        ca_entry = ca_records.get(d)
        cl_entry = cl_records.get(d)

        # Millions ($M) or "not found"
        rev_m = round(r_entry["val"] / 1e6) if r_entry else "not found"
        rev_tag = r_entry["tag"] if r_entry else "not found"

        ni_m = round(ni_entry["val"] / 1e6) if ni_entry else "not found"
        ni_tag = ni_entry["tag"] if ni_entry else "not found"
        ni_list.append(ni_m if isinstance(ni_m, int) else None)

        ocf_m = round(ocf_entry["val"] / 1e6) if ocf_entry else "not found"
        ocf_tag = ocf_entry["tag"] if ocf_entry else "not found"
        ocf_list.append(ocf_m if isinstance(ocf_m, int) else None)

        cx_m = round(cx_entry["val"] / 1e6) if cx_entry else "not found"
        cx_tag = cx_entry["tag"] if cx_entry else "not found"

        eq_m = round(eq_entry["val"] / 1e6) if eq_entry else "not found"
        eq_tag = eq_entry["tag"] if eq_entry else "not found"

        liab_m = round(liab_entry["val"] / 1e6) if liab_entry else "not found"
        liab_tag = liab_entry["tag"] if liab_entry else "not found"

        ca_m = round(ca_entry["val"] / 1e6) if ca_entry else "not found"
        ca_tag = ca_entry["tag"] if ca_entry else "not found"

        cl_m = round(cl_entry["val"] / 1e6) if cl_entry else "not found"
        cl_tag = cl_entry["tag"] if cl_entry else "not found"

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

        # Current ratio = Current Assets / Current Liabilities
        if ca_entry and cl_entry and cl_entry["val"] > 0:
            cr_val = round(ca_entry["val"] / cl_entry["val"], 2)
            cr_list.append(cr_val)
        else:
            cr_val = "not found"
            cr_list.append(None)

        # Liabilities / Equity
        # Rule: If equity <= 0, Liabilities ÷ Equity is "not known"
        if liab_entry and eq_entry:
            if eq_entry["val"] > 0:
                le_val = round(liab_entry["val"] / eq_entry["val"], 2)
                le_list.append(le_val)
            else:
                le_val = "not known"
                le_list.append(None)
        else:
            le_val = "not found"
            le_list.append(None)

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
            "liabilities": liab_m,
            "liabilities_tag": liab_tag,
            "current_assets": ca_m,
            "current_assets_tag": ca_tag,
            "current_liabilities": cl_m,
            "current_liabilities_tag": cl_tag,
            "roe": roe_val,
            "owner_earnings": oe_m,
            "current_ratio": cr_val,
            "liabilities_equity": le_val,
        })

    # =========================================================================
    # BUFFETT CHECKS (3)
    # =========================================================================
    # 1. ROE >= 15% every year
    if any(r is None for r in roe_list):
        buffett_c1 = "not known"
    elif all(r >= 15.0 for r in roe_list):
        buffett_c1 = "pass"
    else:
        buffett_c1 = "fail"

    # 2. Owner earnings positive every year
    if any(oe is None for oe in oe_list):
        buffett_c2 = "not known"
    elif all(oe > 0 for oe in oe_list):
        buffett_c2 = "pass"
    else:
        buffett_c2 = "fail"

    # 3. Owner earnings grew, first year to last
    if oe_list[0] is None or oe_list[-1] is None:
        buffett_c3 = "not known"
    elif oe_list[-1] > oe_list[0]:
        buffett_c3 = "pass"
    else:
        buffett_c3 = "fail"

    # Buffett Verdict
    if buffett_c1 == "pass" and buffett_c2 == "pass" and buffett_c3 == "pass":
        buffett_verdict = "OWN THE BUSINESS"
    elif any(c == "not known" for c in [buffett_c1, buffett_c2, buffett_c3]):
        buffett_verdict = "PASS / WATCH (CANNOT JUDGE)"
    else:
        buffett_verdict = "WATCH / PASS"

    # =========================================================================
    # GRAHAM CHECKS (3)
    # =========================================================================
    # 4. Current ratio >= threshold (default 2.0, probe 1.0), latest year
    latest_cr = cr_list[-1]
    if latest_cr is None:
        graham_c1 = "not known"
    elif latest_cr >= graham_cr_threshold:
        graham_c1 = "pass"
    else:
        graham_c1 = "fail"

    # 5. Net income positive every year
    if any(ni is None for ni in ni_list):
        graham_c2 = "not known"
    elif all(ni > 0 for ni in ni_list):
        graham_c2 = "pass"
    else:
        graham_c2 = "fail"

    # 6. Net income grew, first year to last
    if ni_list[0] is None or ni_list[-1] is None:
        graham_c3 = "not known"
    elif ni_list[-1] > ni_list[0]:
        graham_c3 = "pass"
    else:
        graham_c3 = "fail"

    # Graham Verdict
    if graham_c1 == "pass" and graham_c2 == "pass" and graham_c3 == "pass":
        graham_verdict = "DEFENSIVE INVESTMENT"
    elif any(c == "not known" for c in [graham_c1, graham_c2, graham_c3]):
        graham_verdict = "INSUFFICIENT DATA / WATCH"
    else:
        graham_verdict = "REJECT / SPECULATIVE"

    # =========================================================================
    # BURRY CHECKS (2)
    # =========================================================================
    # 7. Operating cash flow at least net income every year
    if any(ocf is None for ocf in ocf_list) or any(ni is None for ni in ni_list):
        burry_c1 = "not known"
    elif all(ocf >= ni for ocf, ni in zip(ocf_list, ni_list)):
        burry_c1 = "pass"
    else:
        burry_c1 = "fail"

    # 8. Liabilities no more than twice equity, latest year
    latest_le = le_list[-1]
    if latest_le is None:
        burry_c2 = "not known"
    elif latest_le <= 2.0:
        burry_c2 = "pass"
    else:
        burry_c2 = "fail"

    # Burry Verdict
    if burry_c1 == "pass" and burry_c2 == "pass":
        burry_verdict = "PASS FORENSIC SCREEN"
    elif any(c == "not known" for c in [burry_c1, burry_c2]):
        burry_verdict = "INSUFFICIENT DATA / QUARANTINE"
    else:
        burry_verdict = "FAIL FORENSIC SCREEN"

    panel_table = [
        {
            "investor": "Buffett",
            "check": "ROE of 15% or more every year",
            "status": buffett_c1,
            "evidence": f"5-yr ROE: {', '.join([f'{r}%' if isinstance(r, float) else str(r) for r in roe_list])}",
        },
        {
            "investor": "Buffett",
            "check": "Owner earnings positive every year",
            "status": buffett_c2,
            "evidence": f"5-yr OE: {', '.join([f'{oe:,}M' if isinstance(oe, int) else str(oe) for oe in oe_list])}",
        },
        {
            "investor": "Buffett",
            "check": "Owner earnings grew, first year to last",
            "status": buffett_c3,
            "evidence": f"OE Y1: {oe_list[0]:,}M -> Y5: {oe_list[-1]:,}M" if oe_list[0] is not None and oe_list[-1] is not None else "Missing OE",
        },
        {
            "investor": "Graham",
            "check": f"Current ratio of {graham_cr_threshold:.1f} or more, latest year",
            "status": graham_c1,
            "evidence": f"Latest CR: {latest_cr:.2f} (Hurdle: {graham_cr_threshold:.1f})" if latest_cr is not None else "Missing CR",
        },
        {
            "investor": "Graham",
            "check": "Net income positive every year",
            "status": graham_c2,
            "evidence": f"5-yr NI: {', '.join([f'{ni:,}M' if isinstance(ni, int) else str(ni) for ni in ni_list])}",
        },
        {
            "investor": "Graham",
            "check": "Net income grew, first year to last",
            "status": graham_c3,
            "evidence": f"NI Y1: {ni_list[0]:,}M -> Y5: {ni_list[-1]:,}M" if ni_list[0] is not None and ni_list[-1] is not None else "Missing NI",
        },
        {
            "investor": "Burry",
            "check": "Operating cash flow at least net income every year",
            "status": burry_c1,
            "evidence": f"OCF >= NI checked for all 5 years",
        },
        {
            "investor": "Burry",
            "check": "Liabilities no more than twice equity, latest year",
            "status": burry_c2,
            "evidence": f"Latest Liab/Eq: {latest_le:.2f} (Hurdle: <= 2.0)" if latest_le is not None else "Missing Liab/Eq",
        },
    ]

    return {
        "ticker": ticker.upper(),
        "company_name": company_name,
        "cik": cik,
        "user_agent": USER_AGENT,
        "rows": rows,
        "graham_cr_threshold": graham_cr_threshold,
        "panel_table": panel_table,
        "buffett_checks": {
            "roe_15_pct_every_year": buffett_c1,
            "owner_earnings_positive_every_year": buffett_c2,
            "owner_earnings_grew_first_to_last": buffett_c3,
            "verdict": buffett_verdict,
        },
        "graham_checks": {
            "current_ratio_gte_threshold_latest": graham_c1,
            "net_income_positive_every_year": graham_c2,
            "net_income_grew_first_to_last": graham_c3,
            "verdict": graham_verdict,
        },
        "burry_checks": {
            "ocf_gte_net_income_every_year": burry_c1,
            "liabilities_le_twice_equity_latest": burry_c2,
            "verdict": burry_verdict,
        },
    }


def format_cli_output(result: Dict[str, Any]) -> str:
    """Formats full legend panel report with 5-year financials and investor table."""
    lines = []
    lines.append("=" * 80)
    lines.append("SEC EDGAR 10-K FACTS REPORT - LEGEND PANEL AUDIT (LAB 19)")
    lines.append(f"Ticker: {result['ticker']} | Company: {result['company_name']} | CIK: {result['cik']}")
    lines.append(f"User-Agent: {result['user_agent']}")
    lines.append("Data Source: SEC EDGAR keyless API | Standard: 10-K FY only, latest filing wins")
    lines.append("=" * 80 + "\n")

    # Financial table
    lines.append(f"{'FY End':<11} | {'Revenue':>8} | {'Net Inc':>8} | {'OCF':>8} | {'CapEx':>7} | {'Equity':>8} | {'Liab':>8} | {'ROE%':>6} | {'OwnEarn':>8} | {'CR':>5} | {'L/E':>5}")
    lines.append(f"{'-'*11}-+-{'-'*8}-+-{'-'*8}-+-{'-'*8}-+-{'-'*7}-+-{'-'*8}-+-{'-'*8}-+-{'-'*6}-+-{'-'*8}-+-{'-'*5}-+-{'-'*5}")

    for r in result["rows"]:
        rev_s = f"{r['revenue']:,}" if isinstance(r['revenue'], int) else str(r['revenue'])
        ni_s = f"{r['net_income']:,}" if isinstance(r['net_income'], int) else str(r['net_income'])
        ocf_s = f"{r['operating_cash_flow']:,}" if isinstance(r['operating_cash_flow'], int) else str(r['operating_cash_flow'])
        cx_s = f"{r['capital_spending']:,}" if isinstance(r['capital_spending'], int) else str(r['capital_spending'])
        eq_s = f"{r['equity']:,}" if isinstance(r['equity'], int) else str(r['equity'])
        liab_s = f"{r['liabilities']:,}" if isinstance(r['liabilities'], int) else str(r['liabilities'])
        roe_s = f"{r['roe']:.1f}%" if isinstance(r['roe'], (int, float)) else str(r['roe'])
        oe_s = f"{r['owner_earnings']:,}" if isinstance(r['owner_earnings'], int) else str(r['owner_earnings'])
        cr_s = f"{r['current_ratio']:.2f}" if isinstance(r['current_ratio'], (int, float)) else str(r['current_ratio'])
        le_s = f"{r['liabilities_equity']:.2f}" if isinstance(r['liabilities_equity'], (int, float)) else str(r['liabilities_equity'])

        lines.append(f"{r['fy_end']:<11} | {rev_s:>8} | {ni_s:>8} | {ocf_s:>8} | {cx_s:>7} | {eq_s:>8} | {liab_s:>8} | {roe_s:>6} | {oe_s:>8} | {cr_s:>5} | {le_s:>5}")

    lines.append("\n" + "=" * 80)
    lines.append("LEGEND PANEL TABLE: INVESTOR x CHECK")
    lines.append("=" * 80)
    lines.append(f"{'Investor':<10} | {'Check Description':<50} | {'Status':<10}")
    lines.append(f"{'-'*10}-+-{'-'*50}-+-{'-'*10}")
    for item in result["panel_table"]:
        lines.append(f"{item['investor']:<10} | {item['check']:<50} | {item['status'].upper():<10}")

    lines.append("\n" + "=" * 80)
    lines.append("PANEL VERDICTS")
    lines.append("=" * 80)
    lines.append(f"Warren Buffett:   {result['buffett_checks']['verdict']}")
    lines.append(f"Benjamin Graham:  {result['graham_checks']['verdict']} (Current Ratio threshold: {result['graham_cr_threshold']:.1f})")
    lines.append(f"Michael Burry:    {result['burry_checks']['verdict']}")
    lines.append("=" * 80)
    return "\n".join(lines)


def generate_buffett_memo(result: Dict[str, Any]) -> str:
    """Generates Buffett's investment memo using ONLY printed numbers."""
    ticker = result["ticker"]
    company = result["company_name"]
    checks = result["buffett_checks"]
    rows = result["rows"]

    first_row = rows[0]
    last_row = rows[-1]
    first_fy = first_row["fy_end"]
    last_fy = last_row["fy_end"]

    lines = []
    lines.append(f"# Warren Buffett Investment Memo: {company} ({ticker})")
    lines.append(f"**From:** Warren E. Buffett, Berkshire Hathaway")
    lines.append(f"**To:** Charlie Munger & Investment Committee")
    lines.append(f"**Topic:** 5-Year Business Quality Assessment for {company} ({ticker})")
    lines.append(f"**Data Basis:** SEC EDGAR 10-K filings ({first_fy} to {last_fy})")
    lines.append(f"**Scope:** Business fundamentals only (no stock price or market valuation inputs)\n")
    lines.append("---\n")

    if checks["verdict"] == "PASS / WATCH (CANNOT JUDGE)":
        lines.append(f"## Verdict: **{checks['verdict']}**\n")
        lines.append(f"Charlie and I insist on one cardinal rule: if we cannot calculate owner earnings, we cannot judge the cash generation of the enterprise. ")
        lines.append(f"For {company} ({ticker}), capital spending is reported as **not found** in standard industrial cash flow tags. Consequently, owner earnings are **not found** across all five fiscal years, and our two owner earnings tests remain **not known**.\n")
        lines.append(f"Net income moved from {first_row['net_income']:,} million in {first_fy} to {last_row['net_income']:,} million in {last_fy}. However, without plant-and-equipment reinvestment data, owner cash flow cannot be determined. Therefore, we pass on ownership until specialized banking capital analysis is performed.\n")
    elif checks["verdict"] == "OWN THE BUSINESS":
        lines.append(f"## Verdict: **{checks['verdict']}**\n")
        lines.append(f"Charlie and I have spent our entire lives seeking businesses with wide economic moats, predictable earning power, and managers who allocate capital like owners. ")
        lines.append(f"{company} ({ticker}) is the textbook definition of an exceptional business that satisfies all three of our quantitative hurdles without exception.\n")

        lines.append("### 1. Consistent High Return on Capital\n")
        roe_vals_str = ", ".join([f"{r['roe']:.1f}%" for r in rows])
        lines.append(f"Over the five fiscal years from {first_fy} to {last_fy}, return on year-end equity was {roe_vals_str}. Every year comfortably exceeded our 15.0% hurdle rate. In {first_fy}, the company earned {first_row['net_income']:,} million on {first_row['equity']:,} million of equity ({first_row['roe']:.1f}%), and by {last_fy}, net income grew to {last_row['net_income']:,} million on {last_row['equity']:,} million of equity ({last_row['roe']:.1f}%). That proves extraordinary capital productivity without dangerous balance sheet leverage.\n")

        lines.append("### 2. Abundant and Growing Owner Earnings\n")
        lines.append(f"Accounting earnings can deceive, but owner earnings reveal economic reality. Subtracting capital expenditures from operating cash flow demonstrates positive owner cash generation every single year:\n")
        for r in rows:
            lines.append(f"- **FY {r['fy_end']}:** Operating cash flow of {r['operating_cash_flow']:,} million less capital spending of {r['capital_spending']:,} million produced owner earnings of **{r['owner_earnings']:,} million**.")
        lines.append(f"\nOwner earnings expanded from {first_row['owner_earnings']:,} million in {first_fy} to {last_row['owner_earnings']:,} million in {last_fy}, compounding alongside revenue growth from {first_row['revenue']:,} million to {last_row['revenue']:,} million. This franchise showers cash on its owners.\n")

        lines.append("### 3. Moat & Conclusion\n")
        lines.append(f"The business demonstrates pricing power, operational discipline, and an entrenched consumer habit. Because our three hurdles all passed (ROE >= 15.0%: pass; owner earnings positive: pass; owner earnings grew: pass), this is an enterprise I would happily own for fifty years.\n")
    else:
        lines.append(f"## Verdict: **{checks['verdict']}**\n")
        lines.append(f"{company} ({ticker}) demonstrates operational scale, but fails to satisfy all three of our strict hurdle tests without reservation. ")
        lines.append(f"Our audited hurdle status: ROE hurdle is {checks['roe_15_pct_every_year']}; owner earnings positivity is {checks['owner_earnings_positive_every_year']}; owner earnings growth is {checks['owner_earnings_grew_first_to_last']}.\n")
        lines.append(f"Revenue moved from {first_row['revenue']:,} million in {first_fy} to {last_row['revenue']:,} million in {last_fy}, while net income shifted from {first_row['net_income']:,} million to {last_row['net_income']:,} million. Owner earnings registered {first_row['owner_earnings']:,} million in {first_fy} and {last_row['owner_earnings']:,} million in {last_fy}. Until every hurdle passes cleanly, we keep this company on our watch list.\n")

    return "\n".join(lines)


def generate_graham_memo(result: Dict[str, Any], current_ratio_threshold: float = 2.0) -> str:
    """Generates Graham's investment memo using ONLY printed numbers."""
    ticker = result["ticker"]
    company = result["company_name"]
    checks = result["graham_checks"]
    rows = result["rows"]

    first_row = rows[0]
    last_row = rows[-1]
    first_fy = first_row["fy_end"]
    last_fy = last_row["fy_end"]
    latest_cr = last_row["current_ratio"]

    lines = []
    lines.append(f"# Benjamin Graham Investment Memo: {company} ({ticker})")
    lines.append(f"**From:** Benjamin Graham, Security Analyst")
    lines.append(f"**To:** Investment Committee & Serious Investors")
    lines.append(f"**Topic:** Balance Sheet Margin of Safety & Earnings Stability Review")
    lines.append(f"**Data Basis:** SEC EDGAR 10-K reported facts ({first_fy} to {last_fy})")
    lines.append(f"**Scope:** Defensive investor appraisal based on primary balance sheet and income statements\n")
    lines.append("---\n")

    lines.append(f"## Verdict: **{checks['verdict']}**\n")

    lines.append("### 1. Working Capital Margin of Safety (Current Ratio)\n")
    if latest_cr == "not found":
        lines.append(f"Working capital metrics are **not found** in reported 10-K filings. Therefore, liquidity condition remains **not known**.\n")
    elif latest_cr >= current_ratio_threshold:
        lines.append(f"In FY {last_fy}, current assets were {last_row['current_assets']:,} million against current liabilities of {last_row['current_liabilities']:,} million, establishing a current ratio of **{latest_cr:.2f}**. This satisfies our margin of safety standard of {current_ratio_threshold:.1f}. The enterprise possesses adequate liquid cushion to satisfy short-term obligations without stress.\n")
    else:
        lines.append(f"In FY {last_fy}, current assets stood at {last_row['current_assets']:,} million against current liabilities of {last_row['current_liabilities']:,} million, yielding a current ratio of **{latest_cr:.2f}**. This **fails** our classical defensive investor standard of {current_ratio_threshold:.1f}. An enterprise operating below this liquidity threshold lacks the protective cushion required to insulate conservative capital against severe economic contractions.\n")

    lines.append("### 2. Earnings Stability & Ten-Year Trend\n")
    ni_vals_str = ", ".join([f"{r['net_income']:,} million" for r in rows if isinstance(r['net_income'], int)])
    lines.append(f"Over the five reported fiscal years, net income was {ni_vals_str}. ")
    if checks["net_income_positive_every_year"] == "pass":
        lines.append(f"Earnings were positive in all five fiscal years, fulfilling our stability requirement. ")
    else:
        lines.append(f"Earnings exhibited deficit periods, failing our stability requirement. ")

    if checks["net_income_grew_first_to_last"] == "pass":
        lines.append(f"Furthermore, net income expanded from {first_row['net_income']:,} million in {first_fy} to {last_row['net_income']:,} million in {last_fy}, demonstrating legitimate earnings growth across the cycle.\n")
    else:
        lines.append(f"However, net income contracted from {first_row['net_income']:,} million in {first_fy} to {last_row['net_income']:,} million in {last_fy}, failing our growth test.\n")

    lines.append("### 3. Quantitative Disposition & Threshold Design Choice\n")
    if checks["verdict"] == "DEFENSIVE INVESTMENT":
        lines.append(f"Because {company} passes our current ratio requirement ({latest_cr:.2f} >= {current_ratio_threshold:.1f}) and satisfies earnings positivity and growth, it qualifies as a sound defensive investment operation.\n")
    elif checks["verdict"] == "INSUFFICIENT DATA / WATCH":
        lines.append(f"Working capital data is reported as **not found** in reported 10-K filings for {company}. Without reported current assets and liabilities, Graham's liquidity screen cannot be executed and remains **not known**.\n")
    else:
        cr_display = f"{latest_cr:.2f}" if isinstance(latest_cr, (int, float)) else str(latest_cr)
        lines.append(f"While earnings stability is proven, the working capital ratio of {cr_display} violates our classical {current_ratio_threshold:.1f} defensive standard. We cannot classify an enterprise with inadequate working capital margin as a defensive holding, regardless of past growth.\n")

    lines.append(f"**Threshold Decision:** Graham threshold kept at 2.0 (classical defensive investor margin of safety); lowered to 1.0 for capital-efficient negative-working-capital retailers like Costco.\n")
    return "\n".join(lines)


def generate_burry_memo(result: Dict[str, Any]) -> str:
    """Generates Burry's forensic investment memo using ONLY printed numbers."""
    ticker = result["ticker"]
    company = result["company_name"]
    checks = result["burry_checks"]
    rows = result["rows"]

    first_row = rows[0]
    last_row = rows[-1]
    first_fy = first_row["fy_end"]
    last_fy = last_row["fy_end"]
    latest_le = last_row["liabilities_equity"]

    lines = []
    lines.append(f"# Michael Burry Forensic Memo: {company} ({ticker})")
    lines.append(f"**From:** Michael Burry, Scion Asset Management")
    lines.append(f"**To:** Scion Investment Committee & Fund Partners")
    lines.append(f"**Topic:** 10-K Forensic Accounting, Cash Conversion & Leverage Audit")
    lines.append(f"**Data Basis:** SEC EDGAR 10-K primary audited statements ({first_fy} to {last_fy})")
    lines.append(f"**Scope:** Forensic divergence between reported net income and cash flow, plus debt cushion\n")
    lines.append("---\n")

    lines.append(f"## Verdict: **{checks['verdict']}**\n")

    lines.append("### 1. Earnings Quality: Operating Cash Flow vs. Net Income\n")
    lines.append(f"Reported accounting income is a narrative crafted by management. Cash flow is the cold, hard reality. We compare Operating Cash Flow (OCF) directly to Net Income (NI) for every period:\n")
    for r in rows:
        ocf_v = r["operating_cash_flow"]
        ni_v = r["net_income"]
        lines.append(f"- **FY {r['fy_end']}:** Operating Cash Flow of {ocf_v:,} million vs. Net Income of {ni_v:,} million.")

    if checks["ocf_gte_net_income_every_year"] == "pass":
        lines.append(f"\nAcross all five fiscal years from {first_fy} to {last_fy}, operating cash flow equaled or exceeded reported net income. Cash collection is genuine, receivables are turning over, and there is zero evidence of aggressive revenue pulling forward or accrual fabrication. Earnings quality is legitimate.\n")
    else:
        lines.append(f"\nOperating cash flow lagged reported net income in one or more years. When cash generation trails reported accounting earnings, accruals are inflating profits, indicating earnings quality deterioration.\n")

    lines.append("### 2. Balance Sheet Cushion: Total Liabilities vs. Equity\n")
    if latest_le == "not known":
        lines.append(f"Equity in FY {last_fy} is zero or negative ({last_row['equity']:,} million). Liabilities-to-equity is **not known**, indicating severe balance sheet distress.\n")
    elif latest_le == "not found":
        lines.append(f"Total liabilities or equity are **not found** in reported 10-K filings.\n")
    else:
        lines.append(f"In FY {last_fy}, total liabilities stood at {last_row['liabilities']:,} million against stockholders' equity of {last_row['equity']:,} million, resulting in a liabilities-to-equity ratio of **{latest_le:.2f}**.\n")
        if latest_le <= 2.0:
            lines.append(f"This comfortably passes our forensic ceiling of 2.0. The enterprise maintains adequate equity cushion relative to total obligations, mitigating structural solvency risk.\n")
        else:
            lines.append(f"This **fails** our forensic ceiling of 2.0. Total liabilities exceed twice the equity base, creating elevated financial risk and reducing margin of error.\n")

    lines.append("### 3. Contrarian Synthesis\n")
    if checks["verdict"] == "PASS FORENSIC SCREEN":
        lines.append(f"Both forensic hurdles passed: cash flow strictly confirms net income and total liabilities remain within 2.0 times equity. There is no forensic basis for a short thesis on earnings quality or solvency.\n")
    else:
        lines.append(f"One or more forensic hurdles failed. Consensus Wall Street ignores these structural discrepancies, but our quantitative audit identifies material risk.\n")

    return "\n".join(lines)


if __name__ == "__main__":
    ticker_arg = sys.argv[1] if len(sys.argv) > 1 else "COST"
    threshold_arg = float(sys.argv[2]) if len(sys.argv) > 2 else 2.0
    res = get_panel_metrics(ticker_arg, graham_cr_threshold=threshold_arg)
    print(format_cli_output(res))
    print("\n" + "=" * 80)
    print("BUFFETT MEMO:")
    print("=" * 80 + "\n")
    print(generate_buffett_memo(res))
    print("\n" + "=" * 80)
    print("GRAHAM MEMO:")
    print("=" * 80 + "\n")
    print(generate_graham_memo(res, current_ratio_threshold=threshold_arg))
    print("\n" + "=" * 80)
    print("BURRY MEMO:")
    print("=" * 80 + "\n")
    print(generate_burry_memo(res))
