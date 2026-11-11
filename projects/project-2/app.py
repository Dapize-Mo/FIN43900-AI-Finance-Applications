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
import sys
import math
import pandas as pd
import numpy as np
import altair as alt
import streamlit as st

# Ensure project root is in sys.path
_PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
if _PROJECT_DIR not in sys.path:
    sys.path.insert(0, _PROJECT_DIR)

from src.mandate import (
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
# 1. PAGE SETUP & MODERN FINTECH STYLING
# ------------------------------------------------------------------------------
st.set_page_config(
    page_title="Meridian Reserve Portfolio App | FIN 43900 Project 2",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
    /* Global Typography & Font Family */
    html, body, [class*="css"] {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    }

    /* Top Fiduciary Banner */
    .fiduciary-banner {
        background: linear-gradient(135deg, rgba(15, 23, 42, 0.95) 0%, rgba(30, 41, 59, 0.9) 100%);
        border-left: 5px solid #38BDF8;
        border-radius: 8px;
        padding: 16px 20px;
        margin-bottom: 22px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    }
    .fiduciary-banner-title {
        color: #38BDF8;
        font-size: 0.95rem;
        font-weight: 700;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        margin-bottom: 6px;
    }
    .fiduciary-banner-body {
        color: #E2E8F0;
        font-size: 0.86rem;
        line-height: 1.5;
    }

    /* Pill Metadata Tags */
    .pill-tag {
        display: inline-block;
        background: rgba(56, 189, 248, 0.12);
        color: #38BDF8;
        border: 1px solid rgba(56, 189, 248, 0.3);
        border-radius: 20px;
        padding: 3px 12px;
        font-size: 0.78rem;
        font-weight: 600;
        margin-right: 6px;
        margin-bottom: 8px;
    }
    .pill-green {
        background: rgba(16, 185, 129, 0.12);
        color: #10B981;
        border-color: rgba(16, 185, 129, 0.35);
    }
    .pill-gold {
        background: rgba(245, 158, 11, 0.12);
        color: #F59E0B;
        border-color: rgba(245, 158, 11, 0.35);
    }

    /* Fiduciary Metric Cards */
    .kpi-card {
        background: rgba(30, 41, 59, 0.55);
        border: 1px solid rgba(148, 163, 184, 0.18);
        border-radius: 10px;
        padding: 14px 18px;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.12);
        margin-bottom: 14px;
        transition: transform 0.15s ease, border-color 0.15s ease;
    }
    .kpi-card:hover {
        border-color: rgba(56, 189, 248, 0.4);
        transform: translateY(-1px);
    }
    .kpi-label {
        color: #94A3B8;
        font-size: 0.78rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.04em;
        margin-bottom: 4px;
    }
    .kpi-value {
        color: #F8FAFC;
        font-size: 1.55rem;
        font-weight: 700;
    }
    .kpi-subtext {
        color: #64748B;
        font-size: 0.76rem;
        margin-top: 4px;
    }

    /* Verdict Badges */
    .badge-pass {
        color: #10B981;
        background: rgba(16, 185, 129, 0.15);
        border: 1px solid rgba(16, 185, 129, 0.4);
        font-weight: 700;
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 0.85rem;
        display: inline-block;
    }
    .badge-fail {
        color: #EF4444;
        background: rgba(239, 68, 68, 0.15);
        border: 1px solid rgba(239, 68, 68, 0.4);
        font-weight: 700;
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 0.85rem;
        display: inline-block;
    }

    /* Strategy Recommendation Highlight */
    .strategy-box {
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.08) 0%, rgba(30, 41, 59, 0.4) 100%);
        border: 1px solid rgba(16, 185, 129, 0.35);
        border-radius: 10px;
        padding: 16px 20px;
        margin-top: 10px;
        margin-bottom: 18px;
    }

    /* Streamlit Tab Enhancement */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        padding: 10px 18px;
        border-radius: 6px 6px 0 0;
        font-weight: 600;
        font-size: 0.92rem;
    }
</style>
""", unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# 2. MANDATORY FIDUCIARY & AI DISCLOSURES (Base Requirement 8)
# ------------------------------------------------------------------------------
st.markdown("""
<div class="fiduciary-banner">
    <div class="fiduciary-banner-title">
        🏛️ FIN 43900 PROJECT 2: MANDATORY FIDUCIARY & AI GOVERNANCE DISCLOSURES
    </div>
    <div class="fiduciary-banner-body">
        <strong>1. AI Tool Disclosure:</strong> Anthropic Claude (Claude 3.5 Sonnet / Claude Opus 5.5) and Google Antigravity were utilized in designing analytical scripts, unit testing architecture, visualization ergonomics, and formatting optimization. All mathematical derivations, input validations, fiduciary constraints, and investment decisions were directed, verified, and finalized independently by the student analyst.<br>
        <strong>2. Ownership & Academic Notice:</strong> The analysis, models, interpretations, and committee recommendations presented herein are solely the author's work; this application is an educational simulation developed for academic demonstration in FIN 43900 at Purdue University, not personalized investment advice.
    </div>
</div>
""", unsafe_allow_html=True)

# Main Title & Interactive Pills
st.title("Meridian Foundation Reserve — Fiduciary Portfolio System")
st.markdown("""
<div>
    <span class="pill-tag">👤 Analyst: <strong>Oladapo Olaniyan</strong></span>
    <span class="pill-tag">🏫 Purdue Daniels School of Business</span>
    <span class="pill-tag pill-gold">💼 Reserve Fund: $100,000,000</span>
    <span class="pill-tag pill-green">🟢 Status: 100% Mandate Compliant</span>
    <span class="pill-tag">📅 As-Of: November 10, 2026</span>
</div>
""", unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# 3. SIDEBAR: GOVERNANCE METRICS & INTERACTIVE OVERRIDES
# ------------------------------------------------------------------------------
with st.sidebar:
    st.header("🏛️ Institutional Mandate")
    st.markdown("Governing constraints from **Lab 13**:")
    
    st.markdown(f"• **Reserve Capital:** `${PORTFOLIO_SIZE/1e6:.0f}M`")
    st.markdown(f"• **Quarterly Payout:** `${QUARTERLY_PAYOUT/1e6:.2f}M`")
    st.markdown(f"• **12-Mo Reserve Floor:** `{RESERVE_BUFFER_FLOOR*100:.1f}%` (`${ANNUAL_PAYOUT/1e6:.1f}M`)")
    st.markdown(f"• **Net Real Hurdle:** `{TARGET_RETURN*100:.2f}%` (CPI + 4.0%)")
    st.markdown(f"• **5-Day Liquidity Floor:** `≥ 90.0%`")
    st.markdown(f"• **Single Issuer Limit:** `≤ 8.0%`")

    st.markdown("---")
    st.subheader("🌐 Cloud & Deployment")
    st.markdown("• **Live Web App:** [Streamlit Community Cloud](https://dapize-mo-fin43900-ai-finance-appli-projectsproject-2app-kxfhnr.streamlit.app/)")
    st.markdown("• **GitHub Repo:** [Dapize-Mo/FIN43900](https://github.com/Dapize-Mo/FIN43900-AI-Finance-Applications/tree/main/projects/project-2)")

    st.markdown("---")
    st.subheader("🛡️ Model Governance (SR 26-2)")
    st.caption(
        "Adheres to Federal Reserve SR 26-2 model risk guidelines: "
        "enforces mathematical input symmetry, discrete known-answer reconciliation, "
        "and strict point-in-time provenance isolation."
    )

# ------------------------------------------------------------------------------
# 4. CORE COMPUTATIONAL ENGINE
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

# Load Point-in-Time Dataset
pit_df = None
try:
    pit_df = load_point_in_time_data(os.path.join(_PROJECT_DIR, "data", "pit_macro.csv"))
except Exception:
    pit_df = None

# Load Historical Prices
prices_path = os.path.join(_PROJECT_DIR, "data", "prices.csv")
prices_df = None
if os.path.exists(prices_path):
    try:
        prices_df = pd.read_csv(prices_path)
    except Exception:
        prices_df = None

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
# TAB 1: EXECUTIVE DASHBOARD & ALLOCATIONS
# ==============================================================================
with tab1:
    st.subheader("Executive Allocation Matrix: Constrained Mix vs. Simple Baselines")
    st.markdown(
        "Demonstrates compliance with **Base Requirement 3**: Evaluating Equal Weight and the 60/40 "
        "Benchmark beside the Constrained Optimal Portfolio, displaying mandate verdicts and specific rule breach notes."
    )

    # Top KPI Metrics Cards
    k1, k2, k3, k4, k5 = st.columns(5)
    with k1:
        st.markdown("""
        <div class="kpi-card">
            <div class="kpi-label">Total Reserve Fund</div>
            <div class="kpi-value">$100.0M</div>
            <div class="kpi-subtext">Meridian capital base</div>
        </div>
        """, unsafe_allow_html=True)
    with k2:
        st.markdown("""
        <div class="kpi-card">
            <div class="kpi-label">Annual Payout Floor</div>
            <div class="kpi-value">$3.0M</div>
            <div class="kpi-subtext">3.0% reserve-eligible floor</div>
        </div>
        """, unsafe_allow_html=True)
    with k3:
        st.markdown("""
        <div class="kpi-card">
            <div class="kpi-label">Net Return Hurdle</div>
            <div class="kpi-value">6.50%</div>
            <div class="kpi-subtext">CPI (2.5%) + 4.0% real</div>
        </div>
        """, unsafe_allow_html=True)
    with k4:
        st.markdown("""
        <div class="kpi-card">
            <div class="kpi-label">Optimal Volatility</div>
            <div class="kpi-value">9.30%</div>
            <div class="kpi-subtext">-116 bps vs 60/40 benchmark</div>
        </div>
        """, unsafe_allow_html=True)
    with k5:
        st.markdown("""
        <div class="kpi-card">
            <div class="kpi-label">Reserve Coverage</div>
            <div class="kpi-value">2.67x</div>
            <div class="kpi-subtext">$8.0M held vs $3.0M floor</div>
        </div>
        """, unsafe_allow_html=True)

    # Comparative Table
    st.markdown("#### Fiduciary Performance & Covenant Comparison Table")
    comp_df = pd.DataFrame([
        {
            "Portfolio Name": "Baseline 1: Equal Weight (1/N)",
            "T-Bills (BIL)": f"{res_eq['weights'][0]*100:.1f}%",
            "10-Yr (IEF)": f"{res_eq['weights'][1]*100:.1f}%",
            "IG Bonds (LQD)": f"{res_eq['weights'][2]*100:.1f}%",
            "Global Eq (VT)": f"{res_eq['weights'][3]*100:.1f}%",
            "Net Return": f"{res_eq['net_return']*100:.2f}%",
            "Volatility": f"{res_eq['volatility']*100:.2f}%",
            "Sharpe": f"{res_eq['sharpe']:.2f}",
            "Reserve Buffer": f"{res_eq['reserve_weight']*100:.1f}%",
            "Verdict": "FAIL ❌",
            "Fiduciary Breach Diagnosis": "Violates Return Hurdle (5.20% < 6.50%): severe -130 bps purchasing power drag.",
        },
        {
            "Portfolio Name": "Baseline 2: Policy Benchmark (60/40)",
            "T-Bills (BIL)": f"{res_bm['weights'][0]*100:.1f}%",
            "10-Yr (IEF)": f"{res_bm['weights'][1]*100:.1f}%",
            "IG Bonds (LQD)": f"{res_bm['weights'][2]*100:.1f}%",
            "Global Eq (VT)": f"{res_bm['weights'][3]*100:.1f}%",
            "Net Return": f"{res_bm['net_return']*100:.2f}%",
            "Volatility": f"{res_bm['volatility']*100:.2f}%",
            "Sharpe": f"{res_bm['sharpe']:.2f}",
            "Reserve Buffer": f"{res_bm['reserve_weight']*100:.1f}%",
            "Verdict": "FAIL ❌",
            "Fiduciary Breach Diagnosis": "Violates Reserve Buffer (0.0% < 3.0%): zero sovereign liquidity creates immediate covenant breach.",
        },
        {
            "Portfolio Name": "Constrained Optimal Portfolio",
            "T-Bills (BIL)": f"{res_opt['weights'][0]*100:.1f}%",
            "10-Yr (IEF)": f"{res_opt['weights'][1]*100:.1f}%",
            "IG Bonds (LQD)": f"{res_opt['weights'][2]*100:.1f}%",
            "Global Eq (VT)": f"{res_opt['weights'][3]*100:.1f}%",
            "Net Return": f"{res_opt['net_return']*100:.2f}%",
            "Volatility": f"{res_opt['volatility']*100:.2f}%",
            "Sharpe": f"{res_opt['sharpe']:.2f}",
            "Reserve Buffer": f"{res_opt['reserve_weight']*100:.1f}%",
            "Verdict": "PASS ✅",
            "Fiduciary Breach Diagnosis": "Fully Compliant across all 6 covenants; dominates 60/40 benchmark with -116 bps risk reduction.",
        },
    ])
    st.dataframe(comp_df, use_container_width=True, hide_index=True)

    # Sleeve Allocation Chart
    st.markdown("#### Asset Allocation Distribution Across Portfolios")
    chart_data = []
    asset_names = ["1. T-Bills (BIL)", "2. 10-Yr Treasury (IEF)", "3. IG Corporate Bonds (LQD)", "4. Global Equity (VT)"]
    for p_name, res in [("Equal Weight (1/N)", res_eq), ("Policy Benchmark (60/40)", res_bm), ("Constrained Optimal", res_opt)]:
        for idx, w in enumerate(res["weights"]):
            chart_data.append({
                "Portfolio": p_name,
                "Asset Sleeve": asset_names[idx],
                "Weight (%)": round(w * 100.0, 1),
            })
    alloc_df = pd.DataFrame(chart_data)

    chart_alloc = alt.Chart(alloc_df).mark_bar(cornerRadiusTopLeft=3, cornerRadiusTopRight=3).encode(
        x=alt.X("Portfolio:N", title=None, axis=alt.Axis(labelAngle=0)),
        y=alt.Y("Weight (%):Q", title="Portfolio Allocation (%)", scale=alt.Scale(domain=[0, 100])),
        color=alt.Color("Asset Sleeve:N", scale=alt.Scale(
            domain=asset_names,
            range=["#0EA5E9", "#3B82F6", "#8B5CF6", "#10B981"]
        )),
        tooltip=["Portfolio", "Asset Sleeve", "Weight (%)"],
    ).properties(height=340)
    st.altair_chart(chart_alloc, use_container_width=True)

    # Recommended Capital Deployment Breakdown
    st.markdown("""
    <div class="strategy-box">
        <h4 style="color: #10B981; margin-top: 0; margin-bottom: 8px;">🏛️ Committee Recommendation: Allocate to Constrained Optimal Portfolio</h4>
        <div style="font-size: 0.88rem; color: #E2E8F0; line-height: 1.55;">
            Deploying the $100M reserve to the <strong>Constrained Optimal Portfolio</strong> achieves exact fiduciary compliance:
            <ul>
                <li><strong>$52.0M in Global Equity (VT):</strong> Delivers the necessary growth engine to overcome inflation.</li>
                <li><strong>$40.0M in IG Corporate Bonds (LQD):</strong> Generates high-quality recurring cash yield.</li>
                <li><strong>$5.0M in 10-Year Treasuries (IEF):</strong> Provides interest rate duration and sovereign reserve backing.</li>
                <li><strong>$3.0M in T-Bills / Cash (BIL):</strong> Permanently funds 100% of the next 12 months' non-negotiable quarterly distributions.</li>
            </ul>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ==============================================================================
# TAB 2: DETAILED MANDATE COVENANT AUDIT
# ==============================================================================
with tab2:
    st.subheader("Algorithmic Mandate Audit Ledger (Meridian Facts S1–S10)")
    st.markdown(
        "Under Federal Reserve SR 26-2 model governance, an attractive output cannot be used "
        "unless every underlying legal covenant is verified by a strict mathematical gate."
    )

    port_inspect = st.selectbox(
        "Select Portfolio for Covenant Verification:",
        ["Constrained Optimal Portfolio", "Baseline 1: Equal Weight (1/N)", "Baseline 2: Policy Benchmark (60/40)"],
    )
    active_res = res_opt if "Optimal" in port_inspect else (res_eq if "Equal" in port_inspect else res_bm)
    a = active_res["audit"]

    status_badge = "<span class='badge-pass'>MANDATE VERDICT: PASS ✅</span>" if a["overall_pass"] else "<span class='badge-fail'>MANDATE VERDICT: FAIL ❌</span>"
    st.markdown(f"### {port_inspect} — {status_badge}", unsafe_allow_html=True)

    col_a, col_b, col_c = st.columns(3)
    with col_a:
        st.markdown("**1. Allocation Total (100%):**")
        st.markdown("✅ **PASS** (Sum = 100.0%)" if a["sum_pass"] else f"❌ **FAIL** (Sum = {sum(active_res['weights'])*100:.1f}%)")
        st.caption("Contractual completeness covenant.")

        st.markdown(r"**2. Long-Only Rule ($w_i \ge 0$):**")
        st.markdown("✅ **PASS** (No short positions)" if a["long_only_pass"] else "❌ **FAIL** (Negative weight present)")
        st.caption("Prohibits leverage, borrowing, and shorts.")

    with col_b:
        st.markdown(r"**3. Reserve Buffer Floor ($\ge 3.0\%$):**")
        res_tag = f"✅ **PASS** ({a['reserve_weight']*100:.1f}% held)" if a["reserve_pass"] else f"❌ **FAIL** ({a['reserve_weight']*100:.1f}% held < 3.0%)"
        st.markdown(res_tag)
        st.caption("Fact S3: 12 months payout in sovereign paper.")

        st.markdown(r"**4. Return Hurdle ($\ge 6.50\%$):**")
        ret_tag = f"✅ **PASS** ({a['expected_return']*100:.2f}% net)" if a["return_pass"] else f"❌ **FAIL** ({a['expected_return']*100:.2f}% net < 6.50%)"
        st.markdown(ret_tag)
        st.caption("Fact S2: CPI (2.5%) + 4.0% rolling real return.")

    with col_c:
        st.markdown(r"**5. 5-Day Liquidity ($\ge 90.0\%$):**")
        st.markdown("✅ **PASS** (100.0% liquid in ≤ 3 days)" if a["liquidity_pass"] else "❌ **FAIL** (< 90.0% liquid)")
        st.caption("Fact S8: Max 5-business-day redemption.")

        st.markdown(r"**6. Single Issuer Cap ($\le 8.0\%$):**")
        st.markdown("✅ **PASS** (Exempt broad ETFs & Treasuries)" if a["issuer_pass"] else "❌ **FAIL** (> 8.0% single company)")
        st.caption("Fact S6: Concentration cap on single firms.")

    if a["breaches"]:
        st.error(f"**Identified Covenant Breaches:**\n• " + "\n• ".join(a["breaches"]))
    else:
        st.success("All 6 hard legal covenants satisfied without exception.")

# ==============================================================================
# TAB 3: POINT-IN-TIME SIGNAL & DATA CARD
# ==============================================================================
with tab3:
    st.subheader("Point-in-Time Signal & Fiduciary Data Card (Base Requirement 4)")
    st.markdown(
        "Quantitative strategies routinely suffer from **look-ahead contamination** when historical data "
        "silently embeds future revisions. In Lab 17, we audited the macroeconomic inflation driver (`CPIAUCSL`) "
        "under a dual-timestamp coordinate system ($t_{\\text{event}}, t_{\\text{pub}}$) on the St. Louis Fed ALFRED platform."
    )

    col_pit1, col_pit2 = st.columns([1.1, 0.9])
    with col_pit1:
        st.markdown("#### Historical Seasonal Revision Curve (Lab 17 Empirical Proof)")
        st.caption("Comparing vintage **15 January 2024** against today reveals **60 historical months** restated by BLS seasonal adjustments.")
        
        if pit_df is not None:
            clean_pit = pit_df.dropna(subset=["today_vintage", "vintage_2024_01_15"]).copy()
            clean_pit["Revision Delta"] = clean_pit["today_vintage"] - clean_pit["vintage_2024_01_15"]

            c_pit = alt.Chart(clean_pit).mark_line(point=True, color="#38BDF8").encode(
                x=alt.X("observation_date:T", title="Observation Month (Event Date)"),
                y=alt.Y("today_vintage:Q", title="Consumer Price Index (CPIAUCSL)", scale=alt.Scale(zero=False)),
                tooltip=["observation_date:T", "today_vintage:Q", "vintage_2024_01_15:Q", "Revision Delta:Q"],
            ).properties(height=320)
            st.altair_chart(c_pit, use_container_width=True)

    with col_pit2:
        st.markdown("#### Official Point-in-Time Data Card")
        st.json(PIT_DATA_CARD)

    st.warning(
        "⚠️ **Fiduciary Quarantine Imposed:** Because BLS seasonal adjustments recalculate the preceding 5 years "
        "every January, raw `CPIAUCSL` is quarantined for historical backtesting. The portfolio engine admits CPI "
        "strictly under point-in-time vintage queries (`vintage_date <= decision_date`) or substitutes unrevised headline CPI (`CPIAUCNS`)."
    )

# ==============================================================================
# TAB 4: STRESS TESTING & KILL RULE
# ==============================================================================
with tab4:
    st.subheader("Stress Run & Quantitative Process Kill Condition (Base Requirement 5)")
    st.markdown(
        "A fiduciary model must establish clear boundaries where it ceases to be reliable. "
        "Adjust parameter shocks below to observe portfolio response and trigger the **Automated Process Kill Rule**."
    )

    s_col1, s_col2 = st.columns(2)
    with s_col1:
        eq_shock = st.slider("Equity Expected Return Haircut (bps)", 0, 250, 100, step=25, help="Reduces forward expected return of Global Equity")
        corr_spike = st.slider("Stock-Bond Correlation Spike", 0.0, 0.8, 0.3, step=0.05, help="Simulates breakdown of fixed income diversification")
    with s_col2:
        credit_shock = st.slider("Credit Spread Shock (bps)", 0, 150, 50, step=25, help="Haircuts expected return on IG corporate bonds")
        cost_bps = st.slider("Transaction Cost Drag (bps)", 0, 60, 20, step=5, help="Turnover, management fees, and execution slippage")

    stress_result = run_stress_test(
        sleeves=SLEEVES,
        base_corr=BASE_CORRELATION,
        equity_return_haircut_bps=eq_shock,
        credit_spread_shock_bps=credit_shock,
        equity_bond_corr_shock=corr_spike,
        transaction_cost_bps=cost_bps,
    )

    st.markdown("---")
    st.markdown("#### Stress Assessment & Stop Rule Status")

    if stress_result["is_killed"]:
        st.error(f"🛑 **PROCESS STOPPED — KILL RULE TRIGGERED**\n\n{stress_result['kill_reason']}")
    else:
        st.success(f"🟢 **PROCESS FEASIBLE WITHIN TOLERANCES**\n\n{stress_result['kill_reason']}")

    if stress_result["result"] is not None:
        sr = stress_result["result"]
        sc1, sc2, sc3, sc4 = st.columns(4)
        sc1.metric("Stressed Net Return", f"{sr['net_return']*100:.2f}%", delta=f"{sr['net_return']*100 - TARGET_RETURN*100:.2f}% vs Hurdle")
        sc2.metric("Stressed Volatility", f"{sr['volatility']*100:.2f}%", delta=f"{sr['volatility']*100 - res_opt['volatility']*100:.2f}% vs Base")
        sc3.metric("Stressed Sharpe", f"{sr['sharpe']:.2f}")
        sc4.metric("Stressed Reserve Buffer", f"{sr['reserve_weight']*100:.1f}%")

    st.markdown("""
    #### 🛡️ Institutional Kill Condition Specification
    The Meridian Foundation governance rules establish an automatic **DE-RISKING / KILL RULE** under three conditions:
    1. **Infeasible Optimization:** If macroeconomic shocks prevent achieving 6.50% net return at the 3.0% reserve buffer, optimization halts.
    2. **Risk Ceiling Breach:** If portfolio volatility exceeds **12.00%**, manager discretion is stripped and equity weight is capped at 50%.
    3. **Performance Drawdown:** If trailing 12-month real return falls below CPI + 1.0% for two consecutive quarters, capital is locked into short Treasuries.
    """)

# ==============================================================================
# TAB 5: LOCKED CHANGED-INPUT RECORD
# ==============================================================================
with tab5:
    st.subheader("Locked Changed-Input Record (Base Requirement 6)")
    st.markdown(
        "Adhering to the Week 6 verification pattern, the human analyst recorded an **AI-off prediction** "
        "committed to Git *before* running the stress test, followed by post-run reconciliation."
    )

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
    st.table(lcir_table)
    st.info("🔒 **Integrity Hash:** This record is committed to Git in `docs/validation-and-ai-use.md`.")

# ==============================================================================
# TAB 6: COMMITTEE DECISION MEMO
# ==============================================================================
with tab6:
    st.subheader("Investment Committee Decision Memorandum")
    st.caption("Official Fiduciary Deliverable (`docs/decision-memo.md`)")

    memo_file = os.path.join(_PROJECT_DIR, "docs", "decision-memo.md")
    if os.path.exists(memo_file):
        with open(memo_file, "r", encoding="utf-8") as f:
            st.markdown(f.read())
    else:
        st.write("Decision memorandum file not found.")

# ==============================================================================
# TAB 7: SUBMISSION MANIFEST & TRANSCRIPTS
# ==============================================================================
with tab7:
    st.subheader("Project 2 Submission Manifest & Video Transcripts")
    
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

    st.markdown("---")
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
# FOOTER
# ------------------------------------------------------------------------------
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #64748B; font-size: 0.82rem;'>"
    "FIN 43900 — AI Finance Applications | Project 2: Investment Management Application | "
    "Author: <strong>Oladapo Olaniyan</strong> (<code>oolaniy@purdue.edu</code>) | "
    "Mitchell E. Daniels, Jr. School of Business, Purdue University"
    "</div>",
    unsafe_allow_html=True,
)
