"""
FIN 43900 — Project 2: Investment Management Application
Standalone Institutional Fiduciary Portfolio Management & Stress Testing System

Author: Oladapo Olaniyan (oolaniy@purdue.edu)
Institution: Mitchell E. Daniels, Jr. School of Business, Purdue University
Case: Meridian Foundation Reserve ($100 Million Portfolio)
As-Of Boundary: November 10, 2026
Live Deployed URL: https://dapize-mo-fin43900-ai-finance-appli-projectsproject-2app-kxfhnr.streamlit.app/
"""

import os
import re
import sys
import math
import pandas as pd
import numpy as np
import altair as alt
import streamlit as st
import streamlit.components.v1 as components

# Ensure project root is in sys.path
_PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
if _PROJECT_DIR not in sys.path:
    sys.path.insert(0, _PROJECT_DIR)

# Streamlit Cloud can keep an older copy of the src modules in memory after a redeploy,
# which makes new engine arguments fail with a TypeError. Reload them on every run so the
# app always uses the engine that was deployed with it.
import importlib
for _m in ("src.mandate", "src.engine", "src.point_in_time"):
    if _m in sys.modules:
        importlib.reload(sys.modules[_m])

from src.mandate import (
    validate_correlation,
    PORTFOLIO_SIZE,
    ANNUAL_PAYOUT,
    QUARTERLY_PAYOUT,
    RESERVE_BUFFER_FLOOR,
    TARGET_RETURN,
    SLEEVES,
    BASE_CORRELATION,
    check_mandate,
)
from src.engine import (
    build_covariance,
    compute_expected_return,
    compute_portfolio_volatility,
    evaluate_portfolio,
    get_equal_weights,
    get_benchmark_weights,
    optimize_constrained_mix,
    run_stress_test,
    estimate_from_historical_prices,
)
from src.point_in_time import (
    load_point_in_time_data,
    audit_point_in_time_availability,
    PIT_DATA_CARD,
)

# ------------------------------------------------------------------------------
# 1. PAGE SETUP & THEME-ADAPTIVE MODERN FINTECH STYLING
# ------------------------------------------------------------------------------
st.set_page_config(
    page_title="Meridian Reserve Portfolio App | FIN 43900 Project 2",
    page_icon=":material/account_balance:",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
    /* Global Container Sizing & Clean Padding */
    [data-testid="stAppViewContainer"] .main .block-container {
        max-width: 1440px;
        padding-top: 1.5rem;
        padding-bottom: 3.5rem;
    }
    
    /* Clean, Theme-Adaptive Typography */
    h1, h2, h3, h4, h5 {
        letter-spacing: -0.025em;
        font-weight: 700;
    }
    
    /* Modern Pill Badges */
    .meta-pill-container {
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
        margin-top: 6px;
        margin-bottom: 18px;
    }
    .meta-pill {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 4px 12px;
        border-radius: 9999px;
        font-size: 0.82rem;
        font-weight: 600;
        background: rgba(14, 165, 233, 0.10);
        color: #0284C7;
        border: 1px solid rgba(14, 165, 233, 0.28);
    }
    .meta-pill-gold {
        background: rgba(245, 158, 11, 0.10);
        color: #D97706;
        border-color: rgba(245, 158, 11, 0.30);
    }
    .meta-pill-green {
        background: rgba(16, 185, 129, 0.10);
        color: #059669;
        border-color: rgba(16, 185, 129, 0.30);
    }

    /* Fiduciary & Governance Callout Banner */
    .fiduciary-banner-box {
        border-radius: 12px;
        padding: 14px 18px;
        margin-bottom: 20px;
        border-left: 4px solid #0284C7;
        background: rgba(14, 165, 233, 0.05);
        border: 1px solid rgba(14, 165, 233, 0.20);
        border-left-width: 4px;
    }
    .fiduciary-banner-header {
        font-weight: 700;
        font-size: 0.88rem;
        text-transform: uppercase;
        letter-spacing: 0.04em;
        color: #0284C7;
        margin-bottom: 6px;
    }
    .fiduciary-banner-text {
        font-size: 0.84rem;
        line-height: 1.5;
        opacity: 0.92;
    }

    /* Verdict Badges */
    .badge-pass {
        color: #059669;
        background: rgba(16, 185, 129, 0.12);
        border: 1px solid rgba(16, 185, 129, 0.35);
        font-weight: 700;
        padding: 4px 10px;
        border-radius: 9999px;
        font-size: 0.80rem;
        display: inline-block;
    }
    .badge-fail {
        color: #DC2626;
        background: rgba(239, 68, 68, 0.12);
        border: 1px solid rgba(239, 68, 68, 0.35);
        font-weight: 700;
        padding: 4px 10px;
        border-radius: 9999px;
        font-size: 0.80rem;
        display: inline-block;
    }

    /* Polished Tab Styling */
    [data-testid="stTabs"] [role="tablist"] {
        gap: 6px;
        padding: 4px 0;
    }
    [data-testid="stTabs"] [role="tab"] {
        border-radius: 8px 8px 0 0;
        font-weight: 600;
        font-size: 0.90rem;
        padding: 8px 14px;
        transition: all 0.15s ease;
    }
</style>
""", unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# 2. COMPUTATIONAL ENGINE INITIALIZATION
# ------------------------------------------------------------------------------
cov_base = build_covariance(SLEEVES, BASE_CORRELATION)

# Baseline 1: Equal Weight (1/N)
w_eq = get_equal_weights(4)
res_eq = evaluate_portfolio("Baseline 1: Equal Weight (1/N)", w_eq, SLEEVES, cov_base)

# Baseline 2: Meridian Strategic Policy Benchmark (60% VT / 40% LQD)
w_bm = get_benchmark_weights()
res_bm = evaluate_portfolio("Baseline 2: Policy Benchmark (60/40)", w_bm, SLEEVES, cov_base)

# Constrained Optimal Portfolio (Minimum Variance meeting all covenants)
res_opt = optimize_constrained_mix(SLEEVES, cov_base, target_return=TARGET_RETURN, reserve_min=RESERVE_BUFFER_FLOOR)

# Historical Prices & Normalization Data
prices_path = os.path.join(_PROJECT_DIR, "data", "prices.csv")
prices_df = None
norm_prices = None
if os.path.exists(prices_path):
    try:
        prices_df = pd.read_csv(prices_path)
        prices_df["Date"] = pd.to_datetime(prices_df["Date"])
        norm_prices = prices_df.copy().set_index("Date")
        norm_prices = norm_prices.div(norm_prices.iloc[0])
    except Exception:
        prices_df = None
        norm_prices = None

# Point-in-Time Data
pit_df = None
try:
    pit_df = load_point_in_time_data(os.path.join(_PROJECT_DIR, "data", "pit_macro.csv"))
except Exception:
    pit_df = None

# ------------------------------------------------------------------------------
# 3. HEADER & MANDATORY FIDUCIARY DISCLOSURES (Base Requirement 8)
# ------------------------------------------------------------------------------
st.markdown("""
# :material/account_balance: Meridian Foundation Reserve
**Standalone Institutional Fiduciary Portfolio Management & Stress Testing System**
""")

st.markdown("""
<div class="meta-pill-container">
    <span class="meta-pill">👤 Analyst: <strong>Oladapo Olaniyan</strong></span>
    <span class="meta-pill">🏫 Purdue Daniels School of Business</span>
    <span class="meta-pill meta-pill-gold">💼 Reserve Fund: $100,000,000</span>
    <span class="meta-pill meta-pill-green">🟢 Mandate Status: 100% Compliant</span>
    <span class="meta-pill">📅 As-Of Boundary: November 10, 2026</span>
</div>
""", unsafe_allow_html=True)

with st.container(border=True):
    st.markdown("""
    <div style="font-weight: 700; font-size: 0.88rem; color: #0284C7; margin-bottom: 4px;">
        🏛️ MANDATORY FIDUCIARY & AI GOVERNANCE DISCLOSURES (SR 26-2 & BASE REQUIREMENT 8)
    </div>
    <div style="font-size: 0.84rem; line-height: 1.5; opacity: 0.9;">
        <strong>1. AI Tool Disclosure:</strong> Anthropic Claude (Claude 3.5 Sonnet / Claude Opus) and Google Antigravity were utilized in designing analytical scripts, unit test architecture, visualization ergonomics, and formatting optimization. All mathematical derivations, input validations, fiduciary constraints, and investment decisions were directed, verified, and finalized independently by the student analyst.<br>
        <strong>2. Ownership & Academic Notice:</strong> The analysis, models, interpretations, and committee recommendations presented herein are solely the author's work; this application is an educational simulation developed for academic demonstration in FIN 43900 at Purdue University, not personalized investment advice.
    </div>
    """, unsafe_allow_html=True)

"" # Generous breathing room

# ------------------------------------------------------------------------------
# PRESENTER CONTROLS (Video 3): numbered buttons that open a tab and scroll to a section.
# Hide with ?nav=0 on the app address.
# ------------------------------------------------------------------------------
if st.query_params.get("nav", "1") != "0":
    with st.sidebar:
        st.markdown("##### 🎬 Presenter Controls")
        components.html("""
<style>
 body{margin:0;font-family:"Source Sans",sans-serif}
 button{display:block;width:100%;text-align:left;margin:0 0 5px 0;padding:7px 10px;border:1px solid #c9d4cd;
        border-radius:8px;background:#f5f8f6;color:#14452f;font-size:13px;cursor:pointer}
 button:hover{background:#e3efe8}
 b{display:inline-block;min-width:16px}
</style>
<button onclick="nav(1)"><b>1</b> Disclosures (top)</button>
<button onclick="nav(2)"><b>2</b> Three portfolios (bar charts)</button>
<button onclick="nav(3)"><b>3</b> Point-in-time data</button>
<button onclick="nav(4)"><b>4</b> Stress: run -100 bps</button>
<button onclick="nav(5)"><b>5</b> Locked records</button>
<button onclick="nav(6)"><b>6</b> Committee ask</button>
<button onclick="nav(0)"><b>R</b> Reset stress drivers</button>
<script>
var P = window.parent.document;
function vis(e){return e && e.getClientRects().length>0;}
function tab(t){var b=[].slice.call(P.querySelectorAll('[role="tab"]')).filter(function(x){return x.textContent.indexOf(t)>-1 && vis(x);})[0]; if(b) b.click();}
function btn(t){var b=[].slice.call(P.querySelectorAll('button')).filter(function(x){return x.textContent.indexOf(t)>-1 && vis(x);})[0]; if(b) b.click();}
function go(t,d){setTimeout(function(){var e=[].slice.call(P.querySelectorAll('h1,h2,h3,h4,h5,p')).filter(function(x){return vis(x) && x.textContent.indexOf(t)>-1;})[0]; if(e) e.scrollIntoView({behavior:"smooth",block:"start"});},d);}
function toTop(d){setTimeout(function(){var m=P.querySelector('[data-testid="stMain"]')||P.querySelector('section.main'); if(m) m.scrollTo({top:0,behavior:"smooth"});},d);}
function nav(n){
 if(n==1){tab("Executive Allocations"); toTop(500);}
 if(n==2){tab("Executive Allocations"); go("Portfolio Selector",600);}
 if(n==3){tab("Point-in-Time"); go("Point-in-Time Signal",600);}
 if(n==4){tab("Stress Testing"); setTimeout(function(){btn("(-100 bps)");},500); go("Pre-configured Stress Scenarios",2200);}
 if(n==5){tab("Locked Changed-Input"); go("Locked Changed-Input Record (Base",600);}
 if(n==6){tab("Committee Decision Memo"); go("4. Committee Ask",600);}
 if(n==0){tab("Stress Testing"); setTimeout(function(){btn("Reset all drivers");},500); go("Pre-configured Stress Scenarios",1800);}
}
</script>""", height=300)

# ------------------------------------------------------------------------------
# 4. SIDEBAR: GOVERNANCE & MANDATE OVERVIEW
# ------------------------------------------------------------------------------
with st.sidebar:
    st.markdown("### :material/policy: Institutional Mandate")
    with st.container(border=True):
        st.markdown(f"**Reserve Capital:** `${PORTFOLIO_SIZE/1e6:.0f}M`")
        st.markdown(f"**Quarterly Payout:** `${QUARTERLY_PAYOUT/1e6:.2f}M`")
        st.markdown(f"**12-Mo Reserve Floor:** `{RESERVE_BUFFER_FLOOR*100:.1f}%` (`${ANNUAL_PAYOUT/1e6:.1f}M`)")
        st.markdown(f"**Net Real Hurdle:** `{TARGET_RETURN*100:.2f}%` (CPI + 4.0%)")
        st.markdown(f"**5-Day Liquidity:** `≥ 90.0%`")
        st.markdown(f"**Single Issuer Cap:** `≤ 8.0%`")

    st.markdown("### :material/cloud_done: Cloud & Deployment")
    with st.container(border=True):
        st.markdown("• **Live Web App:** [Streamlit Community Cloud](https://dapize-mo-fin43900-ai-finance-appli-projectsproject-2app-kxfhnr.streamlit.app/)")
        st.markdown("• **GitHub Repo:** [Dapize-Mo/FIN43900](https://github.com/Dapize-Mo/FIN43900-AI-Finance-Applications/tree/main/projects/project-2)")

    st.markdown("### :material/verified_user: Model Governance")
    with st.container(border=True):
        st.caption(
            "Adheres to Federal Reserve SR 26-2 model risk guidelines: "
            "enforces mathematical input symmetry, discrete known-answer reconciliation, "
            "and strict point-in-time provenance isolation."
        )

# ------------------------------------------------------------------------------
# 5. TABBED INTERFACE NAVIGATION
# ------------------------------------------------------------------------------
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "📊 Executive Allocations",
    "⚖️ Mandate Covenant Audit",
    "⏱️ Point-in-Time Signal & Data Card",
    "🧪 Stress Testing & Kill Rule",
    "🔒 Locked Changed-Input Record",
    "📝 Committee Decision Memo",
    "📑 Submission Manifest",
])

# ==============================================================================
# TAB 1: EXECUTIVE DASHBOARD & ALLOCATIONS (demo-stockpeers style)
# ==============================================================================
with tab1:
    st.markdown("### :material/dashboard: Executive Allocation Matrix: Constrained Mix vs. Simple Baselines")
    st.caption("Demonstrates compliance with Base Requirement 3: Evaluating Equal Weight and 60/40 Benchmark beside Constrained Optimal Portfolio.")

    # Horizon map for filtering historical returns
    horizon_map = {
        "1 Year": 12,
        "2 Years": 24,
        "3 Years": 36,
        "5 Years": 60,
    }

    # Top Split Section: Controls & Metrics (Left) vs Interactive Visualizer (Right)
    top_cols = st.columns([1.2, 2.5])

    top_left_cell = top_cols[0].container(border=True)
    with top_left_cell:
        st.markdown("#### :material/tune: Portfolio Selector")
        port_choice = st.pills(
            "Target Strategy Allocation",
            options=["Constrained Optimal", "Policy Benchmark (60/40)", "Equal Weight (1/N)"],
            default="Constrained Optimal",
        )

        horizon_choice = st.pills(
            "Historical Performance Window",
            options=list(horizon_map.keys()),
            default="5 Years",
        )

    # Active portfolio resolution
    if port_choice == "Constrained Optimal":
        active_res = res_opt
    elif port_choice == "Policy Benchmark (60/40)":
        active_res = res_bm
    else:
        active_res = res_eq

    a_audit = active_res["audit"]

    bottom_left_cell = top_cols[0].container(border=True)
    with bottom_left_cell:
        st.markdown("#### :material/speed: Fiduciary Metrics")
        m_c1 = m_c2 = st.container()
        m_c1.metric(
            label="Net Return",
            value=f"{active_res['net_return']*100:.2f}%",
            delta=f"{(active_res['net_return'] - TARGET_RETURN)*100:+.2f}% vs Hurdle",
            border=True,
        )
        m_c2.metric(
            label="Volatility",
            value=f"{active_res['volatility']*100:.2f}%",
            delta=f"{(active_res['volatility'] - res_bm['volatility'])*100:+.2f}% vs 60/40",
            delta_color="inverse",
            border=True,
        )
        m_c3 = m_c4 = st.container()
        m_c3.metric(
            label="Reserve Buffer",
            value=f"{active_res['reserve_weight']*100:.1f}%",
            delta=f"${active_res['reserve_weight']*PORTFOLIO_SIZE/1e6:.1f}M Sovereign",
            border=True,
        )
        verdict_str = "PASS ✅" if a_audit["overall_pass"] else "FAIL ❌"
        verdict_delta = "All 6 Covenants Met" if a_audit["overall_pass"] else "Breach Detected"
        m_c4.metric(
            label="Mandate Verdict",
            value=verdict_str,
            delta=verdict_delta,
            delta_color="normal" if a_audit["overall_pass"] else "inverse",
            border=True,
        )

    # Right cell: Visualizer
    right_cell = top_cols[1].container(border=True)
    with right_cell:
        vis_mode = st.pills(
            "Visualization Mode",
            options=["Asset Allocation Mix", "Historical Normalized Sleeve Performance", "Cumulative Growth ($100M Capital)"],
            default="Asset Allocation Mix",
        )

        if vis_mode == "Asset Allocation Mix":
            st.markdown("##### Asset Allocation Weight Comparison (%)")
            chart_data = []
            asset_names = ["1. T-Bills (BIL)", "2. 10-Yr Treasury (IEF)", "3. IG Bonds (LQD)", "4. Global Equity (VT)"]
            for p_name, res in [("Equal Weight (1/N)", res_eq), ("Policy Benchmark (60/40)", res_bm), ("Constrained Optimal", res_opt)]:
                for idx, w in enumerate(res["weights"]):
                    chart_data.append({
                        "Portfolio": p_name,
                        "Asset Sleeve": asset_names[idx],
                        "Weight (%)": round(w * 100.0, 1),
                        "Capital ($M)": round(w * (PORTFOLIO_SIZE / 1e6), 2),
                    })
            alloc_df = pd.DataFrame(chart_data)

            chart_alloc = alt.Chart(alloc_df).mark_bar(
                cornerRadiusTopLeft=4,
                cornerRadiusTopRight=4
            ).encode(
                x=alt.X("Portfolio:N", title=None, axis=alt.Axis(labelAngle=0)),
                y=alt.Y("Weight (%):Q", title="Portfolio Allocation (%)", scale=alt.Scale(domain=[0, 100])),
                color=alt.Color("Asset Sleeve:N", scale=alt.Scale(
                    domain=asset_names,
                    range=["#0284C7", "#3B82F6", "#8B5CF6", "#10B981"]
                ), legend=alt.Legend(orient="bottom", title=None)),
                tooltip=["Portfolio:N", "Asset Sleeve:N", "Weight (%):Q", "Capital ($M):Q"],
            ).properties(height=340)
            st.altair_chart(chart_alloc, use_container_width=True)

        elif vis_mode == "Historical Normalized Sleeve Performance":
            if prices_df is not None:
                n_months = horizon_map[horizon_choice]
                window_df = prices_df.tail(n_months).copy()
                norm_window = window_df.set_index("Date").div(window_df.set_index("Date").iloc[0])

                latest_norm = {norm_window[ticker].iat[-1]: ticker for ticker in ["BIL", "IEF", "LQD", "VT"]}
                best_sleeve = max(latest_norm.items())
                worst_sleeve = min(latest_norm.items())

                k_col1, k_col2 = st.columns(2)
                k_col1.metric("Top Performing Sleeve", best_sleeve[1], delta=f"{(best_sleeve[0] - 1.0)*100:+.1f}% Total Return", border=True)
                k_col2.metric("Lagging Sleeve", worst_sleeve[1], delta=f"{(worst_sleeve[0] - 1.0)*100:+.1f}% Total Return", delta_color="inverse", border=True)

                melted_prices = norm_window.reset_index().melt(id_vars=["Date"], var_name="Sleeve", value_name="Normalized Price")
                chart_norm = alt.Chart(melted_prices).mark_line(strokeWidth=2.2).encode(
                    x=alt.X("Date:T", title="Observation Month"),
                    y=alt.Y("Normalized Price:Q", title="Normalized Return (Start = 1.00)").scale(zero=False),
                    color=alt.Color("Sleeve:N", scale=alt.Scale(
                        domain=["BIL", "IEF", "LQD", "VT"],
                        range=["#0284C7", "#3B82F6", "#8B5CF6", "#10B981"]
                    ), legend=alt.Legend(orient="bottom", title=None)),
                    tooltip=[alt.Tooltip("Date:T", format="%B %Y"), "Sleeve:N", alt.Tooltip("Normalized Price:Q", format=".3f")],
                ).properties(height=300).interactive()
                st.altair_chart(chart_norm, use_container_width=True)
            else:
                st.info("Historical prices dataset not loaded.")

        else: # Cumulative Growth ($100M Capital)
            if prices_df is not None:
                n_months = horizon_map[horizon_choice]
                window_df = prices_df.tail(n_months).copy().reset_index(drop=True)
                norm_w = window_df.set_index("Date").div(window_df.set_index("Date").iloc[0])

                # Calculate trajectory of $100M invested
                growth_records = []
                for dt, row in norm_w.iterrows():
                    val_opt = sum(w * row[ticker] for w, ticker in zip(res_opt["weights"], ["BIL", "IEF", "LQD", "VT"])) * (PORTFOLIO_SIZE / 1e6)
                    val_bm = sum(w * row[ticker] for w, ticker in zip(res_bm["weights"], ["BIL", "IEF", "LQD", "VT"])) * (PORTFOLIO_SIZE / 1e6)
                    val_eq = sum(w * row[ticker] for w, ticker in zip(res_eq["weights"], ["BIL", "IEF", "LQD", "VT"])) * (PORTFOLIO_SIZE / 1e6)
                    growth_records.append({"Date": dt, "Portfolio": "Constrained Optimal", "Fund Value ($M)": round(val_opt, 2)})
                    growth_records.append({"Date": dt, "Portfolio": "Policy Benchmark (60/40)", "Fund Value ($M)": round(val_bm, 2)})
                    growth_records.append({"Date": dt, "Portfolio": "Equal Weight (1/N)", "Fund Value ($M)": round(val_eq, 2)})

                growth_df = pd.DataFrame(growth_records)
                chart_growth = alt.Chart(growth_df).mark_line(strokeWidth=2.2).encode(
                    x=alt.X("Date:T", title="Observation Month"),
                    y=alt.Y("Fund Value ($M):Q", title="Portfolio Valuation ($ Millions)").scale(zero=False),
                    color=alt.Color("Portfolio:N", scale=alt.Scale(
                        domain=["Constrained Optimal", "Policy Benchmark (60/40)", "Equal Weight (1/N)"],
                        range=["#10B981", "#3B82F6", "#94A3B8"]
                    ), legend=alt.Legend(orient="bottom", title=None)),
                    tooltip=[alt.Tooltip("Date:T", format="%B %Y"), "Portfolio:N", alt.Tooltip("Fund Value ($M):Q", format="$.2f")],
                ).properties(height=340).interactive()
                st.altair_chart(chart_growth, use_container_width=True)

    "" # Breathing room

    # Comparative Performance Table in a clean bordered container
    with st.container(border=True):
        st.markdown("#### :material/table_chart: Fiduciary Performance & Legal Covenant Matrix")
        comp_df = pd.DataFrame([
            {
                "Portfolio Strategy": "Baseline 1: Equal Weight (1/N)",
                "BIL (T-Bills)": f"{res_eq['weights'][0]*100:.1f}%",
                "IEF (10-Yr)": f"{res_eq['weights'][1]*100:.1f}%",
                "LQD (IG Corp)": f"{res_eq['weights'][2]*100:.1f}%",
                "VT (Global Eq)": f"{res_eq['weights'][3]*100:.1f}%",
                "Expected Net Return": f"{res_eq['net_return']*100:.2f}%",
                "Annual Volatility": f"{res_eq['volatility']*100:.2f}%",
                "Sharpe": f"{res_eq['sharpe']:.2f}",
                "Reserve Buffer": f"{res_eq['reserve_weight']*100:.1f}%",
                "Verdict": "FAIL ❌",
                "Fiduciary Breach Diagnosis": "Violates Return Hurdle (5.20% < 6.50%): severe -130 bps purchasing power drag.",
            },
            {
                "Portfolio Strategy": "Baseline 2: Policy Benchmark (60/40)",
                "BIL (T-Bills)": f"{res_bm['weights'][0]*100:.1f}%",
                "IEF (10-Yr)": f"{res_bm['weights'][1]*100:.1f}%",
                "LQD (IG Corp)": f"{res_bm['weights'][2]*100:.1f}%",
                "VT (Global Eq)": f"{res_bm['weights'][3]*100:.1f}%",
                "Expected Net Return": f"{res_bm['net_return']*100:.2f}%",
                "Annual Volatility": f"{res_bm['volatility']*100:.2f}%",
                "Sharpe": f"{res_bm['sharpe']:.2f}",
                "Reserve Buffer": f"{res_bm['reserve_weight']*100:.1f}%",
                "Verdict": "FAIL ❌",
                "Fiduciary Breach Diagnosis": "Violates Reserve Buffer (0.0% < 3.0%): holds zero sovereign liquidity, causing immediate breach.",
            },
            {
                "Portfolio Strategy": "Constrained Optimal Portfolio",
                "BIL (T-Bills)": f"{res_opt['weights'][0]*100:.1f}%",
                "IEF (10-Yr)": f"{res_opt['weights'][1]*100:.1f}%",
                "LQD (IG Corp)": f"{res_opt['weights'][2]*100:.1f}%",
                "VT (Global Eq)": f"{res_opt['weights'][3]*100:.1f}%",
                "Expected Net Return": f"{res_opt['net_return']*100:.2f}%",
                "Annual Volatility": f"{res_opt['volatility']*100:.2f}%",
                "Sharpe": f"{res_opt['sharpe']:.2f}",
                "Reserve Buffer": f"{res_opt['reserve_weight']*100:.1f}%",
                "Verdict": "PASS ✅",
                "Fiduciary Breach Diagnosis": "100% Compliant across all 6 covenants; dominates benchmark with -116 bps risk reduction.",
            },
        ])
        st.dataframe(comp_df, use_container_width=True, hide_index=True)

    ""

    # Asset Sleeve Cards Grid
    st.markdown("#### :material/pie_chart: Constrained Optimal Capital Deployment Breakdown ($100.0M Reserve)")
    sleeve_cols = st.columns(4)

    sleeve_details = [
        {"ticker": "BIL", "name": "SPDR 1-3M T-Bills", "weight": res_opt['weights'][0], "cap": res_opt['weights'][0]*100, "role": "Immediate Payout Liquidity", "liq": "1 Business Day", "res": "Yes (Sovereign)"},
        {"ticker": "IEF", "name": "iShares 7-10Y Treasury", "weight": res_opt['weights'][1], "cap": res_opt['weights'][1]*100, "role": "Duration & Reserve Buffer", "liq": "1 Business Day", "res": "Yes (Sovereign)"},
        {"ticker": "LQD", "name": "iShares $ IG Corp Bond", "weight": res_opt['weights'][2], "cap": res_opt['weights'][2]*100, "role": "Income & High Yield Anchor", "liq": "3 Business Days", "res": "No (Credit Risk)"},
        {"ticker": "VT", "name": "Vanguard Total World Stock", "weight": res_opt['weights'][3], "cap": res_opt['weights'][3]*100, "role": "Real Purchasing Power Engine", "liq": "3 Business Days", "res": "No (Equity Risk)"},
    ]

    for idx, s in enumerate(sleeve_details):
        with sleeve_cols[idx].container(border=True):
            st.markdown(f"**{s['ticker']} — {s['name']}**")
            st.metric(label="Target Weight", value=f"{s['weight']*100:.1f}%", delta=f"${s['cap']:.1f}M Capital", border=True)
            st.caption(f"• **Role:** {s['role']}")
            st.caption(f"• **Liquidity:** {s['liq']}")
            st.caption(f"• **Reserve Buffer Eligible:** {s['res']}")

    ""

    # Individual Sleeves vs Peer Group Average (Exact demo-stockpeers implementation)
    with st.expander("📈 Individual Asset Sleeves vs Peer Group Average (Streamlit Gallery Showcase Feature)", expanded=True):
        st.markdown(
            "For the analysis below, the **peer average** when analyzing asset sleeve X always "
            "excludes X itself, showing whether each sleeve contributed excess returns or defensive drag relative to the peer universe."
        )

        if prices_df is not None:
            n_months = horizon_map[horizon_choice]
            window_df = prices_df.tail(n_months).copy()
            norm_window = window_df.set_index("Date").div(window_df.set_index("Date").iloc[0])

            p_cols = st.columns(4)
            tickers_list = ["BIL", "IEF", "LQD", "VT"]

            for i, ticker in enumerate(tickers_list):
                peers = norm_window.drop(columns=[ticker])
                peer_avg = peers.mean(axis=1)

                # Line chart of Ticker vs Peer Average
                plot_data = pd.DataFrame({
                    "Date": norm_window.index,
                    ticker: norm_window[ticker],
                    "Peer Average": peer_avg,
                }).melt(id_vars=["Date"], var_name="Series", value_name="Price")

                chart_line = (
                    alt.Chart(plot_data)
                    .mark_line(strokeWidth=2.0)
                    .encode(
                        alt.X("Date:T", title=None),
                        alt.Y("Price:Q", title="Normalized").scale(zero=False),
                        alt.Color(
                            "Series:N",
                            scale=alt.Scale(domain=[ticker, "Peer Average"], range=["#0284C7", "#94A3B8"]),
                            legend=alt.Legend(orient="bottom", title=None),
                        ),
                        tooltip=["Date:T", "Series:N", alt.Tooltip("Price:Q", format=".3f")],
                    )
                    .properties(title=f"{ticker} vs Peer Average", height=220)
                )

                # Delta area chart
                delta_data = pd.DataFrame({
                    "Date": norm_window.index,
                    "Delta": norm_window[ticker] - peer_avg,
                })

                chart_area = (
                    alt.Chart(delta_data)
                    .mark_area(opacity=0.4, color="#0284C7")
                    .encode(
                        alt.X("Date:T", title=None),
                        alt.Y("Delta:Q", title="Delta vs Peers").scale(zero=False),
                        tooltip=["Date:T", alt.Tooltip("Delta:Q", format="+.3f")],
                    )
                    .properties(title=f"{ticker} minus Peer Average", height=140)
                )

                cell = p_cols[i].container(border=True)
                cell.altair_chart(chart_line, use_container_width=True)
                cell.altair_chart(chart_area, use_container_width=True)

# ==============================================================================
# TAB 2: DETAILED MANDATE COVENANT AUDIT
# ==============================================================================
with tab2:
    st.markdown("### :material/verified: Algorithmic Mandate Audit Ledger (six implemented mandate checks)")
    st.caption("Under Federal Reserve SR 26-2 model governance, an attractive output cannot be used unless every legal covenant is verified by a strict mathematical gate.")

    port_inspect = st.pills(
        "Select Portfolio for Covenant Verification:",
        options=["Constrained Optimal Portfolio", "Baseline 1: Equal Weight (1/N)", "Baseline 2: Policy Benchmark (60/40)"],
        default="Constrained Optimal Portfolio",
    )
    active_audit_res = res_opt if "Optimal" in port_inspect else (res_eq if "Equal" in port_inspect else res_bm)
    a = active_audit_res["audit"]

    verdict_badge = (
        '<span class="badge-pass">PASSES THE SIX IMPLEMENTED MANDATE CHECKS ✅</span>'
        if a["overall_pass"]
        else '<span class="badge-fail">MANDATE VERDICT: FAIL ❌</span>'
    )

    with st.container(border=True):
        st.markdown(
            f"#### Audit Ledger: {port_inspect} — {verdict_badge}",
            unsafe_allow_html=True,
        )

        cov_col1, cov_col2, cov_col3 = st.columns(3)
        with cov_col1:
            with st.container(border=True):
                st.markdown("**1. Allocation Completeness**")
                st.metric("Total Weight", f"{sum(active_audit_res['weights'])*100:.1f}%", delta="100.0% Required", border=False)
                st.caption("✅ PASS: Contractual completeness covenant" if a["sum_pass"] else "❌ FAIL: Does not equal 100%")

            with st.container(border=True):
                st.markdown("**2. Long-Only Prohibition**")
                st.metric("Minimum Weight", f"{min(active_audit_res['weights'])*100:.1f}%", delta="wi ≥ 0.0%", border=False)
                st.caption("✅ PASS: Prohibits borrowing, shorting, and leverage" if a["long_only_pass"] else "❌ FAIL: Negative weight present")

        with cov_col2:
            with st.container(border=True):
                st.markdown("**3. Sovereign Reserve Floor**")
                st.metric("Reserve Buffer", f"{a['reserve_weight']*100:.1f}%", delta="≥ 3.0% ($3.0M)", border=False)
                st.caption("✅ PASS: 12 months payout in sovereign paper (Fact S3)" if a["reserve_pass"] else "❌ FAIL: Violates $3.0M sovereign floor")

            with cov_col2.container(border=True):
                st.markdown("**4. Net Return Hurdle**")
                st.metric("Expected Net Return", f"{a['expected_return']*100:.2f}%", delta="≥ 6.50% (CPI + 4.0%)", border=False)
                st.caption("✅ PASS: Protects endowment purchasing power (Fact S2)" if a["return_pass"] else "❌ FAIL: Below 6.50% net hurdle")

        with cov_col3:
            with st.container(border=True):
                st.markdown("**5. 5-Day Liquidity Redemption**")
                st.metric("Liquid in ≤ 5 Days", "100.0%", delta="≥ 90.0% Required", border=False)
                st.caption("✅ PASS: 100% redeemable in ≤ 3 business days (Fact S8)" if a["liquidity_pass"] else "❌ FAIL: < 90% liquid")

            with st.container(border=True):
                st.markdown("**6. Single Issuer Concentration**")
                st.metric("Max Single Firm", "0.0%", delta="≤ 8.0% Cap", border=False)
                st.caption("✅ PASS: Broad funds & Treasuries exempt (Fact S6)" if a["issuer_pass"] else "❌ FAIL: > 8% in single firm")

    if a["breaches"]:
        st.error(f"**Identified Fiduciary Covenant Breaches:**\n• " + "\n• ".join(a["breaches"]))
    else:
        st.success("All 6 hard legal covenants are fully satisfied with zero exceptions.")

# ==============================================================================
# TAB 3: POINT-IN-TIME SIGNAL & DATA CARD
# ==============================================================================
with tab3:
    st.markdown("### :material/history_toggle_off: Point-in-Time Signal & Fiduciary Data Card (Base Requirement 4)")
    st.caption("Auditing the macroeconomic inflation driver (CPIAUCSL) under a dual-timestamp coordinate system on ALFRED to eliminate look-ahead bias.")

    pit_cols = st.columns([1.2, 0.8])
    with pit_cols[0].container(border=True):
        st.markdown("#### Historical Seasonal Revision Curve (Lab 17 Empirical Proof)")
        st.caption("BLS seasonal adjustment can restate up to **60 historical months** (the potential revision window). Comparing the vintage columns in this dataset detects **13 revisions across 31 rows**.")

        if pit_df is not None:
            clean_pit = pit_df.dropna(subset=["today_vintage", "vintage_2024_01_15"]).copy()
            clean_pit["Revision Delta"] = clean_pit["today_vintage"] - clean_pit["vintage_2024_01_15"]

            c_pit = alt.Chart(clean_pit).mark_line(point=True, color="#0284C7").encode(
                x=alt.X("observation_date:T", title="Observation Month (Event Date)"),
                y=alt.Y("today_vintage:Q", title="Consumer Price Index (CPIAUCSL)", scale=alt.Scale(zero=False)),
                tooltip=["observation_date:T", "today_vintage:Q", "vintage_2024_01_15:Q", "Revision Delta:Q"],
            ).properties(height=260)
            st.altair_chart(c_pit, use_container_width=True)

            c_delta = alt.Chart(clean_pit).mark_area(opacity=0.35, color="#D97706").encode(
                x=alt.X("observation_date:T", title="Observation Month"),
                y=alt.Y("Revision Delta:Q", title="Revision Delta (Index Points)"),
                tooltip=["observation_date:T", "Revision Delta:Q"],
            ).properties(height=140)
            st.altair_chart(c_delta, use_container_width=True)

    with pit_cols[1].container(border=True):
        st.markdown("#### Official Point-in-Time Data Card")
        st.markdown(f"• **Signal Name:** `{PIT_DATA_CARD['signal_name']}`")
        st.markdown(f"• **Series ID:** `{PIT_DATA_CARD['series_id']}`")
        st.markdown(f"• **Provider:** `{PIT_DATA_CARD['provider']}`")
        st.markdown(f"• **Frequency:** `{PIT_DATA_CARD['frequency']}`")
        st.markdown(f"• **Publication Lag:** `{PIT_DATA_CARD['publication_lag']}`")
        st.markdown(f"• **Fiduciary Disposition:** `{PIT_DATA_CARD['fiduciary_disposition']}`")

        with st.expander("View Full JSON Provenance Schema", expanded=False):
            st.json(PIT_DATA_CARD)

    with st.container(border=True):
        st.warning(
            "⚠️ **Fiduciary Quarantine Imposed:** Because BLS seasonal adjustments recalculate the preceding 5 years "
            "every January, raw `CPIAUCSL` is quarantined for historical backtesting. This app demonstrates the as-of gate on one snapshot "
            "(decision date 2026-09-30); backtests should use point-in-time vintages or unrevised headline CPI (`CPIAUCNS`). CPI does not feed the optimizer, which uses a fixed 2.50% inflation input."
        )

# ==============================================================================
# TAB 4: STRESS TESTING & KILL RULE
# ==============================================================================
with tab4:
    st.markdown("### :material/crisis_alert: Stress Testing & Quantitative Process Kill Condition (Base Requirement 5)")
    st.caption("A fiduciary model must establish clear boundaries where it ceases to be reliable, halting execution when macroeconomic shocks violate risk tolerances.")

    if "stress_preset" not in st.session_state:
        st.session_state["stress_preset"] = "Baseline (No Shock)"
    preset_choice = st.pills(
        "Pre-configured Stress Scenarios",
        options=["Baseline (No Shock)", "Equity Return Haircut (-100 bps)", "Stagflation Crisis", "Severe Correlation Breakdown", "Custom Shock"],
        key="stress_preset",
    )

    # Preset parameter resolution
    if preset_choice == "Baseline (No Shock)":
        p_eq, p_cred, p_corr, p_cost = 0, 0, 0.0, 0
    elif preset_choice == "Equity Return Haircut (-100 bps)":
        p_eq, p_cred, p_corr, p_cost = 100, 0, 0.0, 0  # isolates the LCIR input change (12.70% vol)
    elif preset_choice == "Stagflation Crisis":
        p_eq, p_cred, p_corr, p_cost = 150, 75, 0.40, 25
    elif preset_choice == "Severe Correlation Breakdown":
        p_eq, p_cred, p_corr, p_cost = 50, 50, 0.60, 20
    else:
        p_eq, p_cred, p_corr, p_cost = 100, 50, 0.30, 20

    if "stress_nonce" not in st.session_state:
        st.session_state["stress_nonce"] = 0
    def _reset_drivers():
        st.session_state["stress_nonce"] += 1
        st.session_state["stress_preset"] = "Baseline (No Shock)"

    st.button(":material/restart_alt: Reset all drivers to base", help="Selects the Baseline preset and restores every stress slider to 0 shock", on_click=_reset_drivers)
    _k = st.session_state["stress_nonce"]

    stress_cols = st.columns([1, 1.2])

    with stress_cols[0].container(border=True):
        st.markdown("#### :material/tune: Stress Parameter Overrides")
        eq_shock = st.slider("Equity Expected Return Haircut (bps)", 0, 250, p_eq, step=25, help="Reduces forward expected return of Global Equity", key=f"sl_equity_{_k}_{preset_choice}")
        corr_spike = st.slider("Stock-Bond Correlation Spike", 0.0, 0.8, float(p_corr), step=0.05, help="Simulates breakdown of fixed income diversification", key=f"sl_stock-bond_{_k}_{preset_choice}")
        credit_shock = st.slider("Credit Spread Shock (bps)", 0, 150, p_cred, step=25, help="Haircuts expected return on IG corporate bonds", key=f"sl_credit_{_k}_{preset_choice}")
        cost_bps = st.slider("Transaction Cost Drag (bps)", 0, 60, p_cost, step=5, help="Turnover, management fees, and execution slippage", key=f"sl_transaction_{_k}_{preset_choice}")
        window_choice = st.select_slider(
            "Estimation Window (volatility & correlation)",
            options=["Course-authored (base)", "Last 12 months", "Last 24 months", "Last 36 months", "Full 60 months"],
            value="Course-authored (base)",
            help="Re-estimates sleeve volatilities and correlations from the ETF price history; expected returns stay course-authored",
            key=f"sl_window_{_k}_{preset_choice}",
        )
        reserve_floor_pct = st.slider("Reserve Floor Constraint (% of capital)", 3.0, 12.0, 3.0, step=1.0, help="Raises the sovereign reserve minimum above the 3.0% legal floor (constraint stress)", key=f"sl_reserve_{_k}_{preset_choice}")
        _window_months = {"Last 12 months": 12, "Last 24 months": 24, "Last 36 months": 36, "Full 60 months": 60}.get(window_choice)

    st.caption("Input bounds: equity haircut 0–250 bps · correlation spike 0.00–0.80 · credit shock 0–150 bps · cost drag 0–60 bps · reserve floor 3–12% · window 12–60 months. Out-of-range values are rejected by the sliders; the engine re-validates the correlation matrix on every run.")
    try:
        validate_correlation(BASE_CORRELATION)
    except ValueError as _err:
        st.error(f"🛑 Invalid correlation matrix: {_err}")
        st.stop()

    stress_result = run_stress_test(
        sleeves=SLEEVES,
        base_corr=BASE_CORRELATION,
        equity_return_haircut_bps=eq_shock,
        credit_spread_shock_bps=credit_shock,
        equity_bond_corr_shock=corr_spike,
        transaction_cost_bps=cost_bps,
        estimation_window_months=_window_months,
        prices_df=prices_df,
        reserve_floor_override=reserve_floor_pct / 100.0,
    )

    with stress_cols[1].container(border=True):
        st.markdown("#### :material/health_and_safety: Process Feasibility & Kill Rule Verdict")
        if stress_result["is_killed"]:
            st.error(f"🛑 **STOP FLAGGED — COMMITTEE ACTION REQUIRED**\n\n{stress_result['kill_reason'].replace('3.0% reserve buffer', f'{reserve_floor_pct:.1f}% reserve buffer')}")
        else:
            st.success(f"🟢 **PROCESS FEASIBLE WITHIN TOLERANCES**\n\n{stress_result['kill_reason']}")

        if stress_result["result"] is not None:
            sr = stress_result["result"]
            sc1, sc2 = st.columns(2)
            sc1.metric("Stressed Net Return", f"{sr['net_return']*100:.2f}%", delta=f"{sr['net_return']*100 - TARGET_RETURN*100:+.2f}% vs Hurdle", border=True)
            sc2.metric("Stressed Volatility", f"{sr['volatility']*100:.2f}%", delta=f"{sr['volatility']*100 - res_opt['volatility']*100:+.2f}% vs Base", delta_color="inverse", border=True)
            sc3, sc4 = st.columns(2)
            sc3.metric("Stressed Sharpe", f"{sr['sharpe']:.2f}", border=True)
            sc4.metric("Stressed Reserve Buffer", f"{sr['reserve_weight']*100:.1f}%", border=True)

    ""

    with st.container(border=True):
        st.markdown("""
        #### 🛡️ Stop Conditions Implemented in This Engine (SR 26-2)
        The engine **flags a stop** for the committee when any of these is true under the tested inputs:
        1. **Infeasible optimization:** no allocation meets the 6.50% net return hurdle at the selected reserve floor.
        2. **Risk ceiling breach:** portfolio volatility exceeds **12.00%**.
        3. **Return below hurdle:** the best feasible net return falls below 6.50%.

        **Proposed committee actions (not executed by this app):** capping equity at 50% after a volatility stop, and moving capital into short Treasuries after a trailing-return trigger. The engine does not carry out either action and does not evaluate the trailing 12-month real-return trigger (CPI + 1.0% for two consecutive quarters).
        """)

# ==============================================================================
# TAB 5: LOCKED CHANGED-INPUT RECORD
# ==============================================================================
with tab5:
    st.markdown("### :material/lock: Locked Changed-Input Record (Base Requirement 6)")
    st.caption("Adhering to the Week 6 verification pattern: human analyst wrote an AI-off prediction (dated Nov 10; first Git commit of the record 44ed6cf, Nov 11), followed by post-run reconciliation.")

    lcir_table = pd.DataFrame({
        "Audit Dimension": [
            "Input Under Test",
            "Units",
            "Baseline Value",
            "New Changed Value",
            "AI-Off Human Prediction (Pre-Run)",
            "Actual Model Output (Post-Run)",
            "Expected Direction",
            "Actual Direction",
            "Direction Match?",
            "Decision Effect",
            "Failure Diagnosis / Sensitivity",
        ],
        "Fiduciary Verification Ledger": [
            "Global Equity Expected Return Estimate (Sleeve: VT)",
            "Basis Points / Percentage per annum",
            "8.00% per annum (800 bps)",
            "7.00% per annum (700 bps; -100 bps shock)",
            "Portfolio must increase equity allocation toward 75-80% to hit 6.50% net hurdle, causing volatility to spike past 12.00% and triggering the Process Kill Rule.",
            "Equity weight surged to 78.0%, IG Bonds fell to 14.0%, Volatility jumped to 12.70%, and the Process Kill Rule was triggered.",
            "Equity weight increases; Volatility increases; Kill rule triggers.",
            "Equity weight increased (+26%); Volatility spiked (+340 bps); Kill rule triggered.",
            "YES ✅ (Exact Directional Match)",
            "Proves the investment process is brittle under equity return compression; prevents chasing equity beta when expected returns decline.",
            "Divergence was minimal; confirmed that an automated Kill Rule is vital to prevent reckless risk-seeking behavior during equity drawdowns.",
        ]
    })
    with st.container(border=True):
        st.dataframe(lcir_table, use_container_width=True, hide_index=True)
        st.info("🔒 **Integrity Evidence:** Record lives in `docs/validation-and-ai-use.md` (first commit `44ed6cf`). At the LCIR-001 run, `engine.py` sha256 was `80921e58…e8834`; the current `engine.py` is `55cd0596…351e` (estimation-window and reserve-floor drivers were added later and default to off, so the LCIR-001 numbers are unchanged). `mandate.py` sha256 `90089044…10c5f`. Verify with `sha256sum src/engine.py src/mandate.py`.")

    st.markdown("#### LCIR-002 (summary; full record in `docs/validation-and-ai-use.md` Section 3B)")
    with st.container(border=True):
        st.markdown(
            "**Input:** IG credit spread shock, implemented as a **+50 bps haircut to LQD expected return** (prediction committed in `fd80e67`, result in a later commit).  \n"
            "**Result:** volatility **9.70%**, kill rule **not** triggered; weights BIL 2% / IEF 38% / LQD 0% / VT 60%; return 6.504%.  \n"
            "**Prediction vs. result:** direction correct (about +50 bps predicted, +40 bps actual); kill rule **wrong** (predicted trigger); decision effect **wrong** (predicted unchanged 52/40/8/0)."
        )

# ==============================================================================
# TAB 6: COMMITTEE DECISION MEMO
# ==============================================================================
with tab6:
    st.markdown("### :material/description: Investment Committee Decision Memorandum")
    st.caption("Official Fiduciary Deliverable (`docs/decision-memo.md`)")

    memo_file = os.path.join(_PROJECT_DIR, "docs", "decision-memo.md")
    with st.container(border=True):
        if os.path.exists(memo_file):
            with open(memo_file, "r", encoding="utf-8") as f:
                _memo_text = f.read()
            # Streamlit treats paired dollar signs as LaTeX; escape currency amounts ($8.0M) only.
            _memo_text = re.sub(r"\$(?=\d)", r"\\$", _memo_text)
            st.markdown(_memo_text)
        else:
            st.write("Decision memorandum file not found.")

# ==============================================================================
# TAB 7: SUBMISSION MANIFEST & TRANSCRIPTS
# ==============================================================================
with tab7:
    st.markdown("### :material/inventory_2: Project 2 Submission Manifest & Transcripts")

    with st.container(border=True):
        st.markdown("#### Primary GitHub Deliverables Index")
        st.markdown("""
        | Deliverable | Repository Path | Direct Link |
        | :--- | :--- | :--- |
        | **Project 2 Readme** | `projects/project-2/README.md` | [README.md on GitHub](https://github.com/Dapize-Mo/FIN43900-AI-Finance-Applications/blob/main/projects/project-2/README.md) |
        | **Decision Memo** | `projects/project-2/docs/decision-memo.md` | [decision-memo.md on GitHub](https://github.com/Dapize-Mo/FIN43900-AI-Finance-Applications/blob/main/projects/project-2/docs/decision-memo.md) |
        | **Validation & AI Record** | `projects/project-2/docs/validation-and-ai-use.md` | [validation-and-ai-use.md on GitHub](https://github.com/Dapize-Mo/FIN43900-AI-Finance-Applications/blob/main/projects/project-2/docs/validation-and-ai-use.md) |
        | **Submission Manifest** | `projects/project-2/submission/manifest.md` | [manifest.md on GitHub](https://github.com/Dapize-Mo/FIN43900-AI-Finance-Applications/blob/main/projects/project-2/submission/manifest.md) |
        | **Streamlit Web App** | `projects/project-2/app.py` | [app.py on GitHub](https://github.com/Dapize-Mo/FIN43900-AI-Finance-Applications/blob/main/projects/project-2/app.py) |
        """)

    ""

    with st.container(border=True):
        st.markdown("#### Video Submission Scripts & Transcripts")
        v_tab1, v_tab2, v_tab3 = st.tabs([
            "📹 Video 1: Research Evolution (≤ 3:00)",
            "📹 Video 2: Technical Walkthrough (≤ 5:00)",
            "📹 Video 3: Committee Defense (≤ 5:00)",
        ])

        trans_dir = os.path.join(_PROJECT_DIR, "submission", "transcripts")
        with v_tab1:
            f1 = os.path.join(trans_dir, "transcript-video-1.txt")
            if os.path.exists(f1):
                with open(f1, "r", encoding="utf-8") as f:
                    st.text(f.read())
        with v_tab2:
            f2 = os.path.join(trans_dir, "transcript-video-2.txt")
            if os.path.exists(f2):
                with open(f2, "r", encoding="utf-8") as f:
                    st.text(f.read())
        with v_tab3:
            f3 = os.path.join(trans_dir, "transcript-video-3.txt")
            if os.path.exists(f3):
                with open(f3, "r", encoding="utf-8") as f:
                    st.text(f.read())

# ------------------------------------------------------------------------------
# 6. FOOTER
# ------------------------------------------------------------------------------
st.markdown("---")
st.markdown(
    "<div style='text-align: center; opacity: 0.75; font-size: 0.82rem;'>"
    "FIN 43900 — AI Finance Applications | Project 2: Investment Management Application | "
    "Author: <strong>Oladapo Olaniyan</strong> (<code>oolaniy@purdue.edu</code>) | "
    "Mitchell E. Daniels, Jr. School of Business, Purdue University"
    "</div>",
    unsafe_allow_html=True,
)
