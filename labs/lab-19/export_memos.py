import sys
from pathlib import Path
from panel_skill import get_panel_metrics, generate_buffett_memo, generate_graham_memo, generate_burry_memo

def export_all():
    tickers = ["COST", "PEP", "AAPL", "JPM"]
    out_dir = Path(__file__).parent
    for ticker in tickers:
        data = get_panel_metrics(ticker, graham_cr_threshold=2.0)
        b_memo = generate_buffett_memo(data)
        g_memo = generate_graham_memo(data, current_ratio_threshold=2.0)
        m_memo = generate_burry_memo(data)

        lines = [
            f"# Legend Panel Audit Report: {data['company_name']} ({ticker})",
            f"**Date:** November 5, 2026 | **Student:** Oladapo Olaniyan (oolaniy@purdue.edu)  ",
            f"**Course:** FIN 43900 — AI Finance Applications, Daniels School of Business, Purdue University  ",
            f"**Data Source:** SEC EDGAR 10-K Primary Audited Facts (Latest Filing Wins)  ",
            "",
            "---",
            "",
            "## 1. Panel Table: Investor × Check",
            "| Investor | Check Description | Status | Evidence |",
            "|---|---|---|---|",
        ]
        for item in data["panel_table"]:
            lines.append(f"| {item['investor']} | {item['check']} | **{item['status'].upper()}** | {item['evidence']} |")

        lines.extend([
            "",
            "---",
            "",
            "## 2. Warren Buffett Memo",
            b_memo,
            "",
            "---",
            "",
            "## 3. Benjamin Graham Memo",
            g_memo,
            "",
            "---",
            "",
            "## 4. Michael Burry Memo",
            m_memo,
            "",
        ])

        out_path = out_dir / f"{ticker}_panel_memo.md"
        out_path.write_text("\n".join(lines).strip() + "\n", encoding="utf-8")
        print(f"Exported: {out_path.name}")

if __name__ == "__main__":
    export_all()

