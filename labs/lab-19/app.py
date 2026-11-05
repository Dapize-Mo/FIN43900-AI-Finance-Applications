"""
FIN 43900 - Lab 19: Legend Panel
Interactive Streamlit Application
Author: Oladapo Olaniyan (oolaniy@purdue.edu)
Course: FIN 43900 - AI Finance Applications, Fall 2026

Streamlit application providing:
1. Panel Table: Investor x Check (Buffett, Graham, Burry) with pass, fail, or not known.
2. Three Investor Verdicts and Memos displayed side by side in polished cards.
3. Automated Hallucination Detection Gate across ALL THREE memos (flags unprinted numbers).
4. Interactive Graham Current Ratio threshold slider/toggle (default 2.0, probe 1.0).
5. 5-year SEC EDGAR 10-K audited fact table with XBRL provenance tags and interactive charts.
6. Mandatory course attribution and learning disclaimer.
"""

from __future__ import annotations

import re
import streamlit as st
import pandas as pd
import altair as alt
from panel_skill import (
    get_panel_metrics,
    generate_buffett_memo,
    generate_graham_memo,
    generate_burry_memo,
)

# Page Configuration
st.set_page_config(
    page_title="Legend Panel (Buffett · Graham · Burry) · Lab 19",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom Styling (Theme-Adaptive Professional Fintech Aesthetic)
st.markdown("""
<style>
    /* Metric Cards */
    div[data-testid="stMetricValue"] {
        font-size: 1.35rem;
        font-weight: 700;
    }
    /* Section Headings */
    h1, h2, h3, h4 {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }
    /* Status Badge Styling */
    .status-badge {
        display: inline-block;
        padding: 4px 10px;
        border-radius: 12px;
        font-size: 0.85rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .badge-pass {
        background-color: rgba(16, 185, 129, 0.18);
        color: #10b981;
        border: 1px solid rgba(16, 185, 129, 0.4);
    }
    .badge-fail {
        background-color: rgba(239, 68, 68, 0.18);
        color: #ef4444;
        border: 1px solid rgba(239, 68, 68, 0.4);
    }
    .badge-unknown {
        background-color: rgba(245, 158, 11, 0.18);
        color: #f59e0b;
        border: 1px solid rgba(245, 158, 11, 0.4);
    }
    /* Investor Cards - Theme Adaptive */
    .investor-card {
        border-radius: 12px;
        padding: 14px 16px;
        margin-bottom: 12px;
        transition: transform 0.15s ease;
    }
    .investor-buffett {
        background: rgba(16, 185, 129, 0.08);
        border: 1px solid rgba(16, 185, 129, 0.35);
    }
    .investor-graham {
        background: rgba(59, 130, 246, 0.08);
        border: 1px solid rgba(59, 130, 246, 0.35);
    }
    .investor-burry {
        background: rgba(239, 68, 68, 0.08);
        border: 1px solid rgba(239, 68, 68, 0.35);
    }
    /* Memo container text formatting */
    .memo-container {
        font-size: 0.92rem;
        line-height: 1.55;
    }
    .memo-container h3 {
        font-size: 1.15rem;
        margin-top: 14px;
        margin-bottom: 6px;
    }
    .memo-container h4 {
        font-size: 1.05rem;
        margin-top: 12px;
        margin-bottom: 4px;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar Controls
with st.sidebar:
    st.header("⚙️ Audit Controls")

    # Quick Ticker Selector
    if "current_ticker" not in st.session_state:
        st.session_state["current_ticker"] = "COST"

    st.subheader("🎯 Quick Select Security")
    btn_col1, btn_col2 = st.columns(2)
    with btn_col1:
        if st.button("COST (Benchmark)", use_container_width=True):
            st.session_state["current_ticker"] = "COST"
        if st.button("AAPL (VT Top)", use_container_width=True):
            st.session_state["current_ticker"] = "AAPL"
    with btn_col2:
        if st.button("PEP (Target)", use_container_width=True):
            st.session_state["current_ticker"] = "PEP"
        if st.button("JPM (Bank Probe)", use_container_width=True):
            st.session_state["current_ticker"] = "JPM"

    ticker_options = ["COST", "PEP", "AAPL", "JPM", "CUSTOM"]
    current_index = ticker_options.index(st.session_state["current_ticker"]) if st.session_state["current_ticker"] in ticker_options else 4

    ticker_choice = st.selectbox(
        "Active Ticker Symbol:",
        options=ticker_options,
        index=current_index,
        help="COST: Benchmark known answer | PEP: Target coverage | AAPL: Project 2 fund top holding | JPM: Banking probe",
    )

    if ticker_choice == "CUSTOM":
        ticker_input = st.text_input("Enter Custom Ticker:", value="MSFT").upper().strip()
        st.session_state["current_ticker"] = ticker_input
    else:
        ticker_input = ticker_choice
        st.session_state["current_ticker"] = ticker_choice

    st.markdown("---")
    st.subheader("🔬 Graham Threshold Probe")
    graham_threshold = st.slider(
        "Graham Current Ratio Hurdle:",
        min_value=0.5,
        max_value=3.0,
        value=2.0,
        step=0.1,
        help="Classical defensive standard is 2.0. Probing at 1.0 tests whether capital-efficient retailers like COST pass.",
    )
    if graham_threshold == 1.0:
        st.info("💡 **Active Probe (1.0):** Graham threshold lowered to 1.0 $\\rightarrow$ COST flips from **FAIL** to **PASS**!")
    elif graham_threshold == 2.0:
        st.success("📌 **Default Hurdle (2.0):** Strict Graham classical defensive margin of safety.")

    st.markdown("---")
    st.subheader("🛡️ Hallucination Flagger Probe")
    inject_hand_probe = st.checkbox(
        "Inject unprinted numbers",
        value=False,
        help="Demonstrates the active gate by injecting unprinted numbers (40.0% ROE, $99,999M) into the memos.",
    )

    st.markdown("---")
    st.markdown("### 📌 Session Info")
    st.markdown("- **Lab:** Lab 19 (Thursday Merit)")
    st.markdown("- **Date:** Nov 5, 2026")
    st.markdown("- **Session Token:** `wood`")
    st.markdown("- **Partner:** J. Maffei (`ORCL`)")


# Fetch Data
@st.cache_data(show_spinner="Connecting keylessly to SEC EDGAR API...")
def load_data(ticker: str, threshold: float):
    return get_panel_metrics(ticker, graham_cr_threshold=threshold)

try:
    data = load_data(ticker_input, graham_threshold)
except Exception as e:
    st.error(f"Error fetching SEC EDGAR facts for '{ticker_input}': {str(e)}")
    st.stop()


# Helper to collect all verified numbers printed by the script
def extract_printed_numbers(data_dict: dict) -> set:
    """Extracts all numbers printed by the code into a normalized set for validation."""
    printed = set()
    for r in data_dict["rows"]:
        for k in [
            "revenue", "net_income", "operating_cash_flow", "capital_spending",
            "equity", "liabilities", "current_assets", "current_liabilities",
            "roe", "owner_earnings", "current_ratio", "liabilities_equity",
        ]:
            val = r.get(k)
            if isinstance(val, (int, float)):
                printed.add(str(val))
                if isinstance(val, float):
                    printed.add(f"{val:.1f}")
                    printed.add(f"{val:.2f}")
                if isinstance(val, int):
                    printed.add(f"{val:,}")
                    printed.add(str(val))
            d_parts = r["fy_end"].split("-")
            for p in d_parts:
                printed.add(p)
                try:
                    printed.add(str(int(p)))
                except ValueError:
                    pass
    printed.update([
        "15", "15.0", "1", "2", "3", "5", "10", "20", "50", "0", "0.0",
        f"{graham_threshold:.1f}", f"{graham_threshold:.2f}", str(graham_threshold),
        "2.0", "1.0",
    ])
    printed.add(str(int(data_dict["cik"])))
    return printed


def audit_memo_numbers(memo_text: str, allowed_numbers: set):
    """
    Finds every number in the memo and flags numbers not printed by the script.
    Returns (flagged_numbers, highlighted_memo_html).
    """
    number_pattern = re.compile(r"(?<![A-Za-z0-9_])(?:\$)?([0-9]+(?:,[0-9]{3})*(?:\.[0-9]+)?)(?:%)?(?![A-Za-z0-9_])")
    flagged = []

    def replace_match(match):
        raw_token = match.group(0)
        num_str = match.group(1).replace(",", "")
        is_allowed = (
            num_str in allowed_numbers
            or match.group(1) in allowed_numbers
            or f"{float(num_str):.1f}" in allowed_numbers
            or f"{float(num_str):.2f}" in allowed_numbers
            or str(int(float(num_str))) in allowed_numbers
        )
        if is_allowed:
            return raw_token
        else:
            flagged.append(raw_token)
            return f"<mark style='background-color: #ffcccc; color: #cc0000; font-weight: bold; padding: 2px 4px; border-radius: 4px;'>⚠️ {raw_token} [UNPRINTED]</mark>"

    highlighted_text = number_pattern.sub(replace_match, memo_text)
    return flagged, highlighted_text


# Header: Clean Responsive Flex Header
st.markdown("""
<div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; margin-bottom: 6px;">
    <h1 style="font-size: 2.15rem; font-weight: 800; margin: 0; letter-spacing: -0.5px;">
        ⚖️ Legend Panel: Three Investor Skills on 10-K Facts
    </h1>
    <span style="background: rgba(59, 130, 246, 0.15); color: #3b82f6; padding: 5px 14px; border-radius: 20px; font-size: 0.85rem; font-weight: 700; border: 1px solid rgba(59, 130, 246, 0.35);">
        Lab 19 · Thursday Merit Checkout
    </span>
</div>
""", unsafe_allow_html=True)
st.caption("Data from SEC EDGAR; built with AI help, a learning demonstration, not investment advice.")
st.markdown("**Author:** **Oladapo Olaniyan** (`oolaniy@purdue.edu`) | **Course:** FIN 43900 — AI Finance Applications, Daniels School of Business, Purdue University")

# Company Metadata Bar (Clean institutional style)
first_fy = data['rows'][0]['fy_end']
last_fy = data['rows'][-1]['fy_end']

st.markdown(f"""
<div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.1); border-radius: 12px; padding: 14px 18px; margin: 12px 0 16px 0;">
    <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 12px;">
        <div>
            <span style="font-size: 1.45rem; font-weight: 800; letter-spacing: -0.3px;">{data['company_name']}</span>
            <span style="background: rgba(16, 185, 129, 0.2); color: #10b981; padding: 3px 10px; border-radius: 6px; font-weight: 800; font-size: 0.95rem; margin-left: 8px;">{data['ticker']}</span>
            <div style="font-size: 0.82rem; opacity: 0.75; margin-top: 3px;">CIK: <code>{data['cik']}</code> | User-Agent: <code>{data['user_agent']}</code></div>
        </div>
        <div style="display: flex; gap: 10px; flex-wrap: wrap;">
            <div style="background: rgba(255,255,255,0.05); padding: 6px 12px; border-radius: 8px; border: 1px solid rgba(255,255,255,0.08); font-size: 0.82rem;">
                <span style="opacity: 0.6; display: block; font-size: 0.7rem; font-weight: 600;">STANDARD</span>
                <strong>10-K Annual (Latest Wins)</strong>
            </div>
            <div style="background: rgba(255,255,255,0.05); padding: 6px 12px; border-radius: 8px; border: 1px solid rgba(255,255,255,0.08); font-size: 0.82rem;">
                <span style="opacity: 0.6; display: block; font-size: 0.7rem; font-weight: 600;">CURRENCY</span>
                <strong>USD ($ Millions)</strong>
            </div>
            <div style="background: rgba(255,255,255,0.05); padding: 6px 12px; border-radius: 8px; border: 1px solid rgba(255,255,255,0.08); font-size: 0.82rem;">
                <span style="opacity: 0.6; display: block; font-size: 0.7rem; font-weight: 600;">WINDOW</span>
                <strong>{first_fy} → {last_fy}</strong>
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Top Summary Row: Investor Verdicts
col_v1, col_v2, col_v3 = st.columns(3)

b_v = data["buffett_checks"]["verdict"]
g_v = data["graham_checks"]["verdict"]
m_v = data["burry_checks"]["verdict"]

with col_v1:
    with st.container(border=True):
        st.markdown("""
        <div class="investor-card investor-buffett">
            <h4 style="margin:0; font-size: 1.15rem; font-weight: 700;">🐂 Warren Buffett</h4>
            <small style="opacity: 0.8;">Moat & Owner Earnings Philosophy</small>
        </div>
        """, unsafe_allow_html=True)
        if b_v == "OWN THE BUSINESS":
            st.success(f"**Verdict:** {b_v} (3/3 Pass)")
        elif "WATCH" in b_v:
            st.warning(f"**Verdict:** {b_v}")
        else:
            st.error(f"**Verdict:** {b_v}")
        st.caption(r"Criteria: ROE $\ge$ 15%, Owner Earnings > 0, Owner Earnings Grew")

with col_v2:
    with st.container(border=True):
        st.markdown(f"""
        <div class="investor-card investor-graham">
            <h4 style="margin:0; font-size: 1.15rem; font-weight: 700;">🛡️ Benjamin Graham</h4>
            <small style="opacity: 0.8;">Margin of Safety & Liquidity Philosophy</small>
        </div>
        """, unsafe_allow_html=True)
        if g_v == "DEFENSIVE INVESTMENT":
            st.success(f"**Verdict:** {g_v} (3/3 Pass)")
        elif "INSUFFICIENT" in g_v:
            st.warning(f"**Verdict:** {g_v}")
        else:
            st.error(f"**Verdict:** {g_v} (CR Hurdle: {graham_threshold:.1f})")
        st.caption(rf"Criteria: Current Ratio $\ge$ {graham_threshold:.1f}, Positive Net Income, Net Income Grew")

with col_v3:
    with st.container(border=True):
        st.markdown("""
        <div class="investor-card investor-burry">
            <h4 style="margin:0; font-size: 1.15rem; font-weight: 700;">🔍 Michael Burry</h4>
            <small style="opacity: 0.8;">Forensic Accounting & Cash Flow Skepticism</small>
        </div>
        """, unsafe_allow_html=True)
        if m_v == "PASS FORENSIC SCREEN":
            st.success(f"**Verdict:** {m_v} (2/2 Pass)")
        elif "INSUFFICIENT" in m_v:
            st.warning(f"**Verdict:** {m_v}")
        else:
            st.error(f"**Verdict:** {m_v}")
        st.caption(r"Criteria: OCF $\ge$ Net Income every year, Liabilities $\le$ 2.0x Equity")

st.write("")

# Tabbed Layout for Clean Presentation
tab_panel, tab_financials, tab_methodology = st.tabs([
    "📋 The Legend Panel (Table & Memos)",
    "📊 Audited 10-K Financials & Charts",
    "🎓 Methodology, Probe & Decision",
])

# =============================================================================
# TAB 1: THE LEGEND PANEL (TABLE & SIDE-BY-SIDE MEMOS)
# =============================================================================
with tab_panel:
    st.subheader("📋 Panel Table: Investor × Check")
    st.markdown("Each hurdle is evaluated deterministically in code from primary 10-K reported facts. Missing tags strictly produce `not found` and unresolved hurdles remain `not known`.")

    panel_df = pd.DataFrame(data["panel_table"])

    def color_status(val):
        if val == "pass":
            return "background-color: rgba(16, 185, 129, 0.18); color: #10b981; font-weight: 700;"
        elif val == "fail":
            return "background-color: rgba(239, 68, 68, 0.18); color: #ef4444; font-weight: 700;"
        else:
            return "background-color: rgba(245, 158, 11, 0.18); color: #f59e0b; font-weight: 700;"

    styled_panel = panel_df.style.map(color_status, subset=["status"])
    st.dataframe(styled_panel, use_container_width=True, hide_index=True)

    st.markdown("---")
    st.subheader("📝 Audited Investor Memos (Side-by-Side)")
    st.caption("All numbers printed by code. The automated Hallucination Detection Gate scans all three memos simultaneously.")

    # Helper function to resize memo headers for clean 3-column layout
    def format_memo_for_column(raw_memo: str, company_name: str, ticker: str) -> str:
        # Replace top # heading with clean subheader
        memo = re.sub(r"^# .+$", "", raw_memo, flags=re.MULTILINE).strip()
        # Scale down ## and ### to fit column nicely
        memo = re.sub(r"^## ", "#### ", memo, flags=re.MULTILINE)
        memo = re.sub(r"^### ", "##### ", memo, flags=re.MULTILINE)
        return memo

    buffett_raw = generate_buffett_memo(data)
    graham_raw = generate_graham_memo(data, current_ratio_threshold=graham_threshold)
    burry_raw = generate_burry_memo(data)

    if inject_hand_probe:
        graham_raw += "\n\n*Probe Injection:* Unprinted speculation claims 40.0% return and $99,999 in hidden off-balance sheet liabilities."
        burry_raw += "\n\n*Probe Injection:* Speculative whisper number estimates revenue of 888,888 million."

    allowed_nums = extract_printed_numbers(data)

    b_flags, b_html = audit_memo_numbers(format_memo_for_column(buffett_raw, data['company_name'], data['ticker']), allowed_nums)
    g_flags, g_html = audit_memo_numbers(format_memo_for_column(graham_raw, data['company_name'], data['ticker']), allowed_nums)
    m_flags, m_html = audit_memo_numbers(format_memo_for_column(burry_raw, data['company_name'], data['ticker']), allowed_nums)

    col_m1, col_m2, col_m3 = st.columns(3)

    with col_m1:
        with st.container(border=True):
            st.markdown(f"#### 🐂 Warren Buffett Memo\n*{data['company_name']} ({data['ticker']})*")
            if not b_flags:
                st.success("✅ **Zero Hallucinations:** 100% verified.")
            else:
                st.error(f"⚠️ **Flagger Alert:** {b_flags}")
            st.markdown(f"<div class='memo-container'>{b_html}</div>", unsafe_allow_html=True)

    with col_m2:
        with st.container(border=True):
            st.markdown(f"#### 🛡️ Benjamin Graham Memo\n*{data['company_name']} ({data['ticker']})*")
            if not g_flags:
                st.success("✅ **Zero Hallucinations:** 100% verified.")
            else:
                st.error(f"⚠️ **Flagger Alert:** {g_flags}")
            st.markdown(f"<div class='memo-container'>{g_html}</div>", unsafe_allow_html=True)

    with col_m3:
        with st.container(border=True):
            st.markdown(f"#### 🔍 Michael Burry Memo\n*{data['company_name']} ({data['ticker']})*")
            if not m_flags:
                st.success("✅ **Zero Hallucinations:** 100% verified.")
            else:
                st.error(f"⚠️ **Flagger Alert:** {m_flags}")
            st.markdown(f"<div class='memo-container'>{m_html}</div>", unsafe_allow_html=True)

# =============================================================================
# TAB 2: AUDITED 10-K FINANCIALS & CHARTS
# =============================================================================
with tab_financials:
    st.subheader("📊 5-Year Primary Financial Facts ($ Millions)")
    table_rows = []
    for r in data["rows"]:
        table_rows.append({
            "FY End": r["fy_end"],
            "Revenue": f"{r['revenue']:,}" if isinstance(r['revenue'], int) else str(r['revenue']),
            "Net Income": f"{r['net_income']:,}" if isinstance(r['net_income'], int) else str(r['net_income']),
            "Op Cash Flow": f"{r['operating_cash_flow']:,}" if isinstance(r['operating_cash_flow'], int) else str(r['operating_cash_flow']),
            "CapEx": f"{r['capital_spending']:,}" if isinstance(r['capital_spending'], int) else str(r['capital_spending']),
            "Owner Earnings": f"{r['owner_earnings']:,}" if isinstance(r['owner_earnings'], int) else str(r['owner_earnings']),
            "Stockholders' Equity": f"{r['equity']:,}" if isinstance(r['equity'], int) else str(r['equity']),
            "Total Liabilities": f"{r['liabilities']:,}" if isinstance(r['liabilities'], int) else str(r['liabilities']),
            "ROE (%)": f"{r['roe']:.1f}%" if isinstance(r['roe'], (int, float)) else str(r['roe']),
            "Current Ratio": f"{r['current_ratio']:.2f}" if isinstance(r['current_ratio'], (int, float)) else str(r['current_ratio']),
            "Liabilities ÷ Equity": f"{r['liabilities_equity']:.2f}" if isinstance(r['liabilities_equity'], (int, float)) else str(r['liabilities_equity']),
        })

    fact_df = pd.DataFrame(table_rows)
    st.dataframe(fact_df, use_container_width=True, hide_index=True)

    with st.expander("🔍 Inspect Primary XBRL US-GAAP Tag Provenance"):
        tag_rows = []
        for r in data["rows"]:
            tag_rows.append({
                "FY End": r["fy_end"],
                "Revenue Tag": r["revenue_tag"],
                "Net Income Tag": r["net_income_tag"],
                "OCF Tag": r["operating_cash_flow_tag"],
                "CapEx Tag": r["capital_spending_tag"],
                "Equity Tag": r["equity_tag"],
                "Liabilities Tag": r["liabilities_tag"],
                "Current Assets Tag": r["current_assets_tag"],
                "Current Liabilities Tag": r["current_liabilities_tag"],
            })
        st.dataframe(pd.DataFrame(tag_rows), use_container_width=True, hide_index=True)

    st.write("")
    st.subheader("📈 Multi-Investor Financial Visualizations")
    chart_col1, chart_col2 = st.columns(2)

    raw_chart_rows = []
    for r in data["rows"]:
        if isinstance(r["net_income"], int) and isinstance(r["operating_cash_flow"], int):
            raw_chart_rows.append({
                "FY End": r["fy_end"],
                "Net Income": r["net_income"],
                "Operating Cash Flow": r["operating_cash_flow"],
                "Owner Earnings": r["owner_earnings"] if isinstance(r["owner_earnings"], int) else 0,
                "Current Ratio": float(r["current_ratio"]) if isinstance(r["current_ratio"], (int, float)) else None,
                "Liab_Equity": float(r["liabilities_equity"]) if isinstance(r["liabilities_equity"], (int, float)) else None,
            })
    chart_df = pd.DataFrame(raw_chart_rows)

    with chart_col1:
        st.markdown("**Earnings Quality: Net Income vs. Operating Cash Flow vs. Owner Earnings**")
        if not chart_df.empty:
            melted_earnings = pd.melt(
                chart_df,
                id_vars=["FY End"],
                value_vars=["Net Income", "Operating Cash Flow", "Owner Earnings"],
                var_name="Metric",
                value_name="USD ($ Millions)",
            )
            c1 = (
                alt.Chart(melted_earnings)
                .mark_bar()
                .encode(
                    x=alt.X("FY End:N", title="Fiscal Year End"),
                    y=alt.Y("USD ($ Millions):Q", title="USD ($ Millions)"),
                    color=alt.Color(
                        "Metric:N",
                        scale=alt.Scale(
                            domain=["Net Income", "Operating Cash Flow", "Owner Earnings"],
                            range=["#2563eb", "#10b981", "#f59e0b"],
                        ),
                    ),
                    xOffset="Metric:N",
                )
                .properties(height=320)
            )
            st.altair_chart(c1, use_container_width=True)

    with chart_col2:
        st.markdown(f"**Working Capital Safety: Current Ratio vs. Graham Hurdle ({graham_threshold:.1f})**")
        if not chart_df.empty and chart_df["Current Ratio"].notna().any():
            cr_clean = chart_df.dropna(subset=["Current Ratio"])
            c2_base = alt.Chart(cr_clean).mark_line(point=True, color="#ef4444", strokeWidth=3).encode(
                x=alt.X("FY End:N", title="Fiscal Year End"),
                y=alt.Y("Current Ratio:Q", title="Current Ratio", scale=alt.Scale(zero=False)),
            )
            rule = alt.Chart(pd.DataFrame({"Hurdle": [graham_threshold]})).mark_rule(
                color="#64748b", strokeDash=[6, 4], strokeWidth=2
            ).encode(y="Hurdle:Q")
            st.altair_chart((c2_base + rule).properties(height=320), use_container_width=True)

# =============================================================================
# TAB 3: METHODOLOGY, PROBE & FIDUCIARY DECISION
# =============================================================================
with tab_methodology:
    col_syn1, col_syn2 = st.columns(2)

    with col_syn1:
        with st.container(border=True):
            st.markdown(r"""
            ### 🧠 Why Three Personas on the Same Facts Disagree
            1. **Different Objective Functions:**
               - **Warren Buffett** prioritizes durable competitive advantage, consumer habits, pricing power, and high ROE ($\ge 15\%$). He tolerates lean working capital if owner cash flow compounds.
               - **Benjamin Graham** prioritizes liquidation safety and downside protection. A current ratio below 2.0 indicates working capital vulnerability during severe credit panics.
               - **Michael Burry** prioritizes forensic accounting skepticism, hunting for earnings manipulation where operating cash flow lags reported net income, or debt burdens exceeding twice equity.
            2. **Costco (`COST`) as Archetype:**
               - **Buffett:** Approves (3/3). Extraordinary ROE (25–31%) and owner earnings compounding from $3.5B to $9.4B.
               - **Graham:** Rejects (2/3). Current ratio of 1.06 violates the classical 2.0 defensive hurdle.
               - **Burry:** Approves (2/2). Cash flow exceeds net income every year ($15.8B vs $9.2B); liabilities to equity is 1.49 $\le$ 2.0.
            """)

    with col_syn2:
        with st.container(border=True):
            st.markdown(f"""
            ### ⚖️ Project 2 Fiduciary Screening Decision
            **Question:** *Would you let this panel screen companies for your Project 2 — yes, no, or only with a condition?*

            **Decision:** **YES, ONLY WITH A CONDITION.**

            **The Mandatory Three-Part Condition:**
            1. **Sector-Specific Liquidity Calibration:** Graham's working capital threshold must be parameterized. Modern negative-working-capital retailers (e.g. Costco) and tech giants (e.g. Apple) operate safely near 1.0; imposing a rigid 2.0 hurdle penalizes supply-chain excellence.
            2. **Financial Institution Quarantine:** Banking institutions (e.g. `JPM`) must be quarantined from industrial CapEx hurdles and evaluated using bank-specific capital ratios (e.g. CET1) rather than owner earnings.
            3. **Disagreement as a Triangulation Signal:** Never average divergent votes into a composite score. When Buffett passes but Graham and Burry fail (as with `PEP` and `AAPL`), the split surfaces the essential investment trade-off: **exceptional franchise power achieved with high leverage and minimal working capital.**
            """)
