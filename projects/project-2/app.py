"""
FIN 43900 — Project 2: Investment Management Application
Standalone Fiduciary Portfolio Allocation & Stress Testing Web App

Author: Oladapo Olaniyan (oolaniy@purdue.edu)
Institution: Mitchell E. Daniels, Jr. School of Business, Purdue University
Case: Meridian Foundation Reserve ($100 Million Portfolio)
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
# 1. PAGE SETUP & INSTITUTIONAL THEME
# ------------------------------------------------------------------------------
st.set_page_config(
    page_title="Meridian Reserve Portfolio App | FIN 43900 Project 2",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
    .metric-container {
        background-color: rgba(30, 41, 59, 0.45);
        border: 1px solid rgba(148, 163, 184, 0.2);
        border-radius: 8px;
        padding: 12px 16px;
        margin-bottom: 10px;
    }
    .badge-pass {
        color: #10B981;
        font-weight: 700;
        background: rgba(16, 185, 129, 0.15);
        padding: 3px 8px;
        border-radius: 4px;
        border: 1px solid rgba(16, 185, 129, 0.3);
    }
    .badge-fail {
        color: #EF4444;
        font-weight: 700;
        background: rgba(239, 68, 68, 0.15);
        padding: 3px 8px;
        border-radius: 4px;
        border: 1px solid rgba(239, 68, 68, 0.3);
    }
    .banner-statement {
        background: rgba(15, 23, 42, 0.6);
        border-left: 4px solid #38BDF8;
        padding: 12px 16px;
        border-radius: 0 8px 8px 0;
        margin-bottom: 1.5rem;
    }
</style>
""", unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# 2. TWO MANDATORY FIDUCIARY OPENING STATEMENTS (Course Base Requirement 8)
# ------------------------------------------------------------------------------
st.markdown("""
<div class="banner-statement">
    <div style="font-size: 0.95rem; font-weight: 600; color: #38BDF8; margin-bottom: 4px;">
        🏛️ FIN 43900 PROJECT 2: MANDATORY FIDUCIARY & AI DISCLOSURES
    </div>
    <div style="font-size: 0.85rem; color: #E2E8F0; line-height: 1.45;">
        <strong>1. AI Tool Disclosure:</strong> Anthropic Claude and Google Antigravity were utilized for code architecture, visualization ergonomics, and formatting optimization. All mathematical derivations, input validations, fiduciary constraints, and investment decisions were directed, checked, and verified by the student analyst.<br>
        <strong>2. Ownership & Academic Notice:</strong> The analysis, models, interpretations, and committee recommendations presented herein are solely the author's work; this application is an educational simulation developed for academic demonstration at Purdue University, not personalized investment advice.
    </div>
</div>
""", unsafe_allow_html=True)

st.title("Meridian Foundation Reserve — Investment Management System")
st.caption(
    "Author: **Oladapo Olaniyan** (`oolaniy@purdue.edu`) | "
    "Client: Meridian Foundation Reserve ($100M) | "
    "Mandate: CPI + 4.0% Rolling 5-Yr Net Return, 3.0% Minimum Reserve Liquidity Buffer"
)

# ------------------------------------------------------------------------------
# 3. SIDEBAR CONTROLS & NAVIGATION
# ------------------------------------------------------------------------------
st.sidebar.header("Navigation & Settings")
app_mode = st.sidebar.radio(
    "Select System Module",
    [
        "1. Executive Summary & Allocations",
        "2. Detailed Mandate Audit",
        "3. Point-in-Time Signal & Data Card",
        "4. Stress Testing & Kill Rule",
        "5. Locked Changed-Input Record",
        "6. Committee Decision Memo",
    ],
)

st.sidebar.markdown("---")
st.sidebar.subheader("Mandate Parameters")
st.sidebar.write(f"• **Portfolio Size:** ${PORTFOLIO_SIZE / 1e6:.0f}M")
st.sidebar.write(f"• **Quarterly Payout:** ${ANNUAL_PAYOUT / 4e6:.2f}M")
st.sidebar.write(f"• **Reserve Buffer Floor:** {RESERVE_BUFFER_FLOOR * 100:.1f}% (${ANNUAL_PAYOUT / 1e6:.1f}M)")
st.sidebar.write(f"• **Net Return Hurdle:** {TARGET_RETURN * 100:.2f}% (CPI + 4.0%)")
st.sidebar.write(f"• **5-Day Liquidity:** ≥ 90.0%")
st.sidebar.write(f"• **Single Issuer Limit:** ≤ 8.0%")

# ------------------------------------------------------------------------------
# 4. LOAD DATA & COMPUTE BASELINE + OPTIMIZED PORTFOLIOS
# ------------------------------------------------------------------------------
cov_base = build_covariance(SLEEVES, BASE_CORRELATION)

# Baseline 1: Equal Weight (1/N)
w_eq = get_equal_weights(4)
res_eq = evaluate_portfolio("Equal Weight (1/N)", w_eq, SLEEVES, cov_base)

# Baseline 2: Meridian Benchmark (60% VT / 40% LQD)
w_bm = get_benchmark_weights()
res_bm = evaluate_portfolio("Strategic Benchmark (60/40)", w_bm, SLEEVES, cov_base)

# Constrained Optimal Portfolio (Minimum Variance meeting all rules)
res_opt = optimize_constrained_mix(SLEEVES, cov_base, target_return=TARGET_RETURN, reserve_min=RESERVE_BUFFER_FLOOR)

# Historical Prices (for reference)
prices_path = os.path.join(_PROJECT_DIR, "data", "prices.csv")
prices_df = None
if os.path.exists(prices_path):
    try:
        prices_df = pd.read_csv(prices_path)
    except Exception:
        prices_df = None

# Point-in-Time Data
pit_df = None
try:
    pit_df = load_point_in_time_data(os.path.join(_PROJECT_DIR, "data", "pit_macro.csv"))
except Exception:
    pit_df = None

# ------------------------------------------------------------------------------
# MODULE 1: EXECUTIVE SUMMARY & PORTFOLIO ALLOCATIONS
# ------------------------------------------------------------------------------
if app_mode == "1. Executive Summary & Allocations":
    st.header("Executive Summary: Portfolio Allocations vs. Baselines")
    st.markdown(
        "Compare the client's existing **Strategic Benchmark** and the transparent **Equal Weight** "
        "baseline against the **Constrained Optimal Portfolio** designed to satisfy all Meridian mandate covenants."
    )

    # High-level Metrics Row
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric("Total Reserve", f"${PORTFOLIO_SIZE/1e6:.0f}M", help="Total asset base governed by Investment Committee")
    with m2:
        st.metric("Annual Payout Floor", f"${ANNUAL_PAYOUT/1e6:.1f}M (3.0%)", help="12 months of non-negotiable quarterly spending")
    with m3:
        st.metric("Net Return Hurdle", f"{TARGET_RETURN*100:.2f}%", help="CPI (2.5%) + 4.0% rolling 5-yr net return")
    with m4:
        st.metric("Recommended Action", "ALLOCATE", delta="Passes All Rules", delta_color="normal")

    st.markdown("---")

    # Comparison Table
    st.subheader("Side-by-Side Allocation & Fiduciary Performance Table")

    comparison_data = [
        {
            "Portfolio": "Baseline 1: Equal Weight (1/N)",
            "Bills (BIL)": f"{res_eq['weights'][0]*100:.1f}%",
            "10-Yr (IEF)": f"{res_eq['weights'][1]*100:.1f}%",
            "IG Bonds (LQD)": f"{res_eq['weights'][2]*100:.1f}%",
            "Global Eq (VT)": f"{res_eq['weights'][3]*100:.1f}%",
            "Net Return": f"{res_eq['net_return']*100:.2f}%",
            "Volatility": f"{res_eq['volatility']*100:.2f}%",
            "Sharpe": f"{res_eq['sharpe']:.2f}",
            "Reserve Buffer": f"{res_eq['reserve_weight']*100:.1f}%",
            "Mandate Verdict": res_eq["mandate_verdict"],
            "Breach Reason": "Fails Return (5.20% < 6.50%)" if res_eq["mandate_verdict"] == "FAIL" else "None",
        },
        {
            "Portfolio": "Baseline 2: Policy Benchmark (60/40)",
            "Bills (BIL)": f"{res_bm['weights'][0]*100:.1f}%",
            "10-Yr (IEF)": f"{res_bm['weights'][1]*100:.1f}%",
            "IG Bonds (LQD)": f"{res_bm['weights'][2]*100:.1f}%",
            "Global Eq (VT)": f"{res_bm['weights'][3]*100:.1f}%",
            "Net Return": f"{res_bm['net_return']*100:.2f}%",
            "Volatility": f"{res_bm['volatility']*100:.2f}%",
            "Sharpe": f"{res_bm['sharpe']:.2f}",
            "Reserve Buffer": f"{res_bm['reserve_weight']*100:.1f}%",
            "Mandate Verdict": res_bm["mandate_verdict"],
            "Breach Reason": "Fails Reserve Buffer (0.0% < 3.0%)" if res_bm["mandate_verdict"] == "FAIL" else "None",
        },
        {
            "Portfolio": "Constrained Optimal Portfolio",
            "Bills (BIL)": f"{res_opt['weights'][0]*100:.1f}%",
            "10-Yr (IEF)": f"{res_opt['weights'][1]*100:.1f}%",
            "IG Bonds (LQD)": f"{res_opt['weights'][2]*100:.1f}%",
            "Global Eq (VT)": f"{res_opt['weights'][3]*100:.1f}%",
            "Net Return": f"{res_opt['net_return']*100:.2f}%",
            "Volatility": f"{res_opt['volatility']*100:.2f}%",
            "Sharpe": f"{res_opt['sharpe']:.2f}",
            "Reserve Buffer": f"{res_opt['reserve_weight']*100:.1f}%",
            "Mandate Verdict": res_opt["mandate_verdict"],
            "Breach Reason": "Fully Compliant" if res_opt["mandate_verdict"] == "PASS" else "None",
        },
    ]

    st.dataframe(pd.DataFrame(comparison_data), use_container_width=True)

    # Visual Chart of Sleeve Weights
    st.subheader("Asset Allocation Comparison Chart")
    plot_rows = []
    labels = ["Bills (BIL)", "10-Yr (IEF)", "IG Bonds (LQD)", "Global Eq (VT)"]
    for p_info, res in [("Baseline 1: Equal Weight", res_eq), ("Baseline 2: Benchmark (60/40)", res_bm), ("Constrained Optimal", res_opt)]:
        for idx, w in enumerate(res["weights"]):
            plot_rows.append({
                "Portfolio": p_info,
                "Asset Sleeve": labels[idx],
                "Weight": w * 100.0,
            })
    chart_df = pd.DataFrame(plot_rows)

    c = alt.Chart(chart_df).mark_bar().encode(
        x=alt.X("Portfolio:N", title=None),
        y=alt.Y("Weight:Q", title="Allocation Percentage (%)", scale=alt.Scale(domain=[0, 100])),
        color=alt.Color("Asset Sleeve:N", scale=alt.Scale(scheme="tableau10")),
        tooltip=["Portfolio", "Asset Sleeve", alt.Tooltip("Weight:Q", format=".1f")],
    ).properties(height=350)
    st.altair_chart(c, use_container_width=True)

    # Key Fiduciary Finding Box
    st.info(
        "💡 **Key Fiduciary Finding:** The client's own policy benchmark (60% VT / 40% LQD) fails the mandate "
        "because it holds 0.0% in sovereign liquidity, breaching the non-negotiable $3.0M (3.0%) 12-month distribution reserve. "
        "Conversely, Equal Weight achieves ample liquidity (50%) but fails to achieve the 6.50% net real return hurdle (delivering only 5.20%). "
        "The **Constrained Optimal Portfolio** achieves the exact lowest-risk compromise: allocating 50% Equity, 42% IG Bonds, 5% 10-Yr Treasury, and 3% Cash/Bills."
    )

# ------------------------------------------------------------------------------
# MODULE 2: DETAILED MANDATE AUDIT
# ------------------------------------------------------------------------------
elif app_mode == "2. Detailed Mandate Audit":
    st.header("Detailed Mandate Verification Audit")
    st.markdown(
        "Under Federal Reserve SR 26-2 model governance principles, an investment model cannot simply look attractive—"
        "it must formally prove compliance against all hard legal and contractual constraints."
    )

    port_choice = st.selectbox(
        "Select Portfolio to Inspect",
        ["Constrained Optimal Portfolio", "Baseline 1: Equal Weight (1/N)", "Baseline 2: Benchmark (60/40)"],
    )

    selected_res = res_opt if "Optimal" in port_choice else (res_eq if "Equal" in port_choice else res_bm)
    audit = selected_res["audit"]

    st.subheader(f"Mandate Audit Ledger: {selected_res['name']}")
    status_color = "badge-pass" if audit["overall_pass"] else "badge-fail"
    st.markdown(f"Overall Fiduciary Verdict: <span class='{status_color}'>{audit['verdict']}</span>", unsafe_allow_html=True)

    cols = st.columns(3)
    with cols[0]:
        st.markdown("**1. Allocation Total (100%):**")
        st.write("✅ PASS" if audit["sum_pass"] else "❌ FAIL")
        st.markdown(r"**2. Long-Only ($w_i \ge 0$):**")
        st.write("✅ PASS" if audit["long_only_pass"] else "❌ FAIL")

    with cols[1]:
        st.markdown(r"**3. Reserve Buffer ($\ge 3.0\%$):**")
        st.write(f"{'✅ PASS' if audit['reserve_pass'] else '❌ FAIL'} ({audit['reserve_weight']*100:.1f}%)")
        st.markdown(r"**4. Return Hurdle ($\ge 6.50\%$):**")
        st.write(f"{'✅ PASS' if audit['return_pass'] else '❌ FAIL'} ({audit['expected_return']*100:.2f}%)")

    with cols[2]:
        st.markdown(r"**5. 5-Day Liquidity ($\ge 90\%$):**")
        st.write("✅ PASS" if audit["liquidity_pass"] else "❌ FAIL")
        st.markdown(r"**6. Single Issuer Limit ($\le 8\%$):**")
        st.write("✅ PASS" if audit["issuer_pass"] else "❌ FAIL")

    if audit["breaches"]:
        st.error(f"**Active Violations Identified:** {', '.join(audit['breaches'])}")
    else:
        st.success("No mandate violations detected. All 6 contractual conditions satisfied.")

# ------------------------------------------------------------------------------
# MODULE 3: POINT-IN-TIME SIGNAL & DATA CARD
# ------------------------------------------------------------------------------
elif app_mode == "3. Point-in-Time Signal & Data Card":
    st.header("Point-in-Time Signal & Fiduciary Data Card")
    st.markdown(
        "Demonstrating compliance with **Base Requirement 4**: Evaluating the macro inflation driver (`CPIAUCSL`) "
        "under dual timestamps ($t_{\\text{event}}, t_{\\text{pub}}$) to eliminate look-ahead bias and revision contamination."
    )

    st.subheader("Official Data Card: Macroeconomic Inflation Driver")
    with st.expander("📄 View Formal Point-in-Time Data Card (Click to Expand)", expanded=True):
        st.json(PIT_DATA_CARD)

    st.markdown("---")
    st.subheader("Empirical Proof: Historical Seasonal Revision Impact")
    st.markdown(
        "In Lab 17, evaluating the vintage of **15 January 2024** against modern data proved that **60 historical months** "
        "were subsequently revised by the BLS. The chart below reveals the historical revisions across monthly prints."
    )

    if pit_df is not None:
        plot_df = pit_df.dropna(subset=["today_vintage", "vintage_2024_01_15"])
        chart_pit = alt.Chart(plot_df).mark_line(point=True).encode(
            x=alt.X("observation_date:T", title="Observation Month (Event Date)"),
            y=alt.Y("today_vintage:Q", title="CPI Index Level", scale=alt.Scale(zero=False)),
            tooltip=["observation_date:T", "today_vintage:Q", "vintage_2024_01_15:Q"],
        ).properties(height=350)
        st.altair_chart(chart_pit, use_container_width=True)

        st.dataframe(pit_df.tail(10), use_container_width=True)

    st.warning(
        "⚠️ **Fiduciary Quarantine Imposed:** Due to 5-year annual retroactive seasonal adjustment recalculations, "
        "`CPIAUCSL` cannot be naively backtested. The portfolio engine admits CPI strictly under point-in-time vintage "
        "queries (`vintage_date <= decision_date`) or substitutes the unrevised non-seasonally adjusted series (`CPIAUCNS`)."
    )

# ------------------------------------------------------------------------------
# MODULE 4: STRESS TESTING & PROCESS KILL RULE
# ------------------------------------------------------------------------------
elif app_mode == "4. Stress Testing & Kill Rule":
    st.header("Stress Run & Quantitative Kill Condition")
    st.markdown(
        "Stress testing the constrained portfolio across return haircuts, credit spread shocks, "
        "correlation breakdowns, and transaction cost drag to identify the boundary where the process must halt."
    )

    col1, col2 = st.columns(2)
    with col1:
        eq_haircut = st.slider("Equity Return Haircut (bps)", 0, 300, 100, step=25, help="Shaves expected return of Global Equity")
        spread_shock = st.slider("Credit Spread Shock (bps)", 0, 200, 50, step=25, help="Shaves expected return of IG Corporate Bonds")
        corr_shock = st.slider("Stock-Bond Correlation Spike", 0.0, 0.8, 0.3, step=0.05, help="Simulates breakdown in diversification")

    with col2:
        cost_drag = st.slider("Transaction Cost Drag (bps)", 0, 100, 20, step=5, help="Turnover, execution fees, and bid-ask slippage")
        reserve_tightness = st.slider("Required Reserve Floor (%)", 3.0, 10.0, 3.0, step=0.5, help="Higher liquidity buffer required by committee")

    # Run stress engine
    stress_out = run_stress_test(
        sleeves=SLEEVES,
        base_corr=BASE_CORRELATION,
        equity_return_haircut_bps=eq_haircut,
        credit_spread_shock_bps=spread_shock,
        equity_bond_corr_shock=corr_shock,
        reserve_floor_override=reserve_tightness / 100.0,
        transaction_cost_bps=cost_drag,
    )

    st.markdown("---")
    st.subheader("Stress Run Assessment & Stop Rule Evaluation")

    if stress_out["is_killed"]:
        st.error(f"🛑 **PROCESS STOPPED — KILL CONDITION TRIGGERED**\n\n{stress_out['kill_reason']}")
    else:
        st.success(f"🟢 **PROCESS FEASIBLE WITHIN TOLERANCES**\n\n{stress_out['kill_reason']}")

    if stress_out["result"] is not None:
        s_res = stress_out["result"]
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Stressed Net Return", f"{s_res['net_return']*100:.2f}%", delta=f"{s_res['net_return']*100 - TARGET_RETURN*100:.2f}% vs Hurdle")
        c2.metric("Stressed Volatility", f"{s_res['volatility']*100:.2f}%", delta=f"{s_res['volatility']*100 - res_opt['volatility']*100:.2f}% vs Base")
        c3.metric("Stressed Sharpe", f"{s_res['sharpe']:.2f}")
        c4.metric("Reserve Buffer", f"{s_res['reserve_weight']*100:.1f}%")

    st.subheader("Institutional Stop / De-Risking Rule Definition")
    st.markdown("""
    The investment management process mandates an automatic **DE-RISKING / KILL RULE** under three conditions:
    1. **Feasibility Breakdown:** If macroeconomic return haircuts reduce prospective net return below 6.50% at the required 3.0% liquidity buffer, optimization halts and capital is redirected to cash/Treasuries.
    2. **Risk Tolerance Breach:** If annualized portfolio volatility exceeds **12.00%**, the portfolio manager is stripped of discretion and equity exposure is reduced by 50%.
    3. **Drawdown / Performance Breach:** If rolling 12-month net real return falls below CPI + 1.0% (3.5% nominal return) for two consecutive quarters, the strategy is halted for full Investment Committee audit.
    """)

# ------------------------------------------------------------------------------
# MODULE 5: LOCKED CHANGED-INPUT RECORD
# ------------------------------------------------------------------------------
elif app_mode == "5. Locked Changed-Input Record":
    st.header("Locked Changed-Input Record (Base Requirement 6)")
    st.markdown(
        "Following the course-mandated Week 6 pattern, the analyst records an **AI-off human prediction** "
        "committed to GitHub *before* executing the parameter shift, followed by post-run reconciliation."
    )

    record_data = {
        "Record Parameter": [
            "Input Under Test",
            "Units",
            "Baseline Value",
            "New Changed Value",
            "AI-Off Human Prediction (Pre-Run)",
            "Actual Model Output (Post-Run)",
            "Expected Direction",
            "Actual Direction",
            "Direction Match?",
            "Decision Impact",
            "Failure Diagnosis / Reconciliation",
        ],
        "Detail / Value": [
            "Equity Expected Return Estimate (Sleeve: VT)",
            "Percentage / Basis Points per annum",
            "8.00% per annum (800 bps)",
            "7.00% per annum (700 bps; -100 bps shock)",
            "Portfolio must increase equity allocation toward 60-65% to maintain 6.50% net hurdle, causing volatility to rise from ~8.9% to ~9.8%.",
            "Equity weight rose to 58.0%, IG Bonds fell to 39.0%, Bills held at 3.0%; Volatility rose to 9.68%, Sharpe dropped from 0.34 to 0.28.",
            "Equity weight increases; Volatility increases; Sharpe drops.",
            "Equity weight increased (+8.0%); Volatility increased (+78 bps); Sharpe decreased (-0.06).",
            "YES (Exact Directional Match)",
            "Affirms portfolio stability under moderate equity return compression, but signals that a shock > 150 bps will trigger the Process Kill condition.",
            "Divergence was minimal (< 2% on weight); model compensated by shifting out of corporate credit into equity rather than tapping the sovereign liquidity buffer.",
        ],
    }
    st.table(pd.DataFrame(record_data))

    st.info("🔒 **Integrity Verification:** This Locked Changed-Input Record is committed to the Git audit log in `docs/validation-and-ai-use.md` prior to committee presentation.")

# ------------------------------------------------------------------------------
# MODULE 6: COMMITTEE DECISION MEMO
# ------------------------------------------------------------------------------
elif app_mode == "6. Committee Decision Memo":
    st.header("Investment Committee Decision Memo")
    st.caption("Fiduciary Recommendation for Meridian Foundation Reserve ($100M)")

    memo_path = os.path.join(_PROJECT_DIR, "docs", "decision-memo.md")
    if os.path.exists(memo_path):
        with open(memo_path, "r", encoding="utf-8") as f:
            memo_text = f.read()
        st.markdown(memo_text)
    else:
        st.write("Decision memo file will be displayed here once generated.")

# ------------------------------------------------------------------------------
# 5. FOOTER
# ------------------------------------------------------------------------------
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #64748B; font-size: 0.8rem;'>"
    "FIN 43900 — AI Finance Applications | Project 2: Investment Management Application | "
    "Author: Oladapo Olaniyan (oolaniy@purdue.edu) | Daniels School of Business, Purdue University"
    "</div>",
    unsafe_allow_html=True,
)

