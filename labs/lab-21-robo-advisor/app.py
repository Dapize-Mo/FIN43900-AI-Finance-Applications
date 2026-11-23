"""
FIN 43900 — AI Finance Applications
Module: Interactive Streamlit Web Application — AI Robo Advisor
Author: Oladapo Olaniyan
Date: November 2026

Interactive web UI fulfilling the assignment to improve the Robo Advisor with Codex:
- Modern visual dashboard replacing terminal UI
- Keyless live market data via yfinance
- State persistence & session resumption
- Multi-agent fiduciary audit tabs
- Side-by-side comparison with Markowitz MPT Quantitative Optimizer
"""

import os
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

from models import (
    Benchmarks,
    Currency,
    IncomeLevel,
    InvestmentGoal,
    InvestmentHorizon,
    InvestmentKnowledge,
    InvestmentPriority,
    InvestmentPurpose,
    LiquidityNeed,
    MarketDownturnReaction,
    PortfolioPreference,
    RiskProfile,
    StockExchange,
)
from data_engine import MarketDataEngine
from robo_engine import (
    MPTQuantitativeEngine,
    calculate_risk_score,
    run_robo_advisor_pipeline,
)
from storage import load_profile, save_profile

st.set_page_config(
    page_title="AI Robo Advisor — FIN 43900",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# === Header ===
st.title("🤖 AI Robo Advisor — Multi-Agent Decision System")
st.caption(
    "FIN 43900: AI Finance Applications | Daniels School of Business, Purdue University | "
    "**Student:** Oladapo Olaniyan | **Session:** Week 14 Studio Lab"
)

# Initialize Session State
if "preference" not in st.session_state:
    saved = load_profile()
    if saved:
        st.session_state["preference"] = saved
    else:
        st.session_state["preference"] = PortfolioPreference(
            age=32,
            investment_knowledge=InvestmentKnowledge.INTERMEDIATE,
            income_level=IncomeLevel.FROM_60K_TO_100K,
            goal=InvestmentGoal.WEALTH_BUILDING,
            investment_purpose=InvestmentPurpose.GROW_WEALTH,
            investment_horizon=InvestmentHorizon.LONG_TERM,
            liquidity_need=LiquidityNeed.FROM_3_TO_5_YEARS,
            risk_profile=RiskProfile.MODERATE_AGGRESSIVE,
            downturn_reaction=MarketDownturnReaction.HOLD,
            investment_priority=InvestmentPriority.BALANCED,
            max_loss_tolerance=0.15,
            has_emergency_fund=True,
            initial_investment=25000.0,
            recurring_contribution=1000.0,
            benchmark=Benchmarks.SPY
        )

pref_init = st.session_state["preference"]

# === Sidebar: Questionnaire & Settings ===
with st.sidebar:
    st.header("📋 Investor Profile Questionnaire")
    st.info("💡 Auto-recovery active. Inputs are persisted across sessions.")

    with st.expander("👤 1. Personal & Financial Capacity", expanded=True):
        age = st.slider("Age", 18, 90, int(pref_init.age))
        knowledge = st.selectbox(
            "Investment Knowledge",
            options=list(InvestmentKnowledge),
            index=list(InvestmentKnowledge).index(pref_init.investment_knowledge),
            format_func=lambda x: x.value
        )
        income = st.selectbox(
            "Annual Income Level",
            options=list(IncomeLevel),
            index=list(IncomeLevel).index(pref_init.income_level),
            format_func=lambda x: x.value
        )
        has_ef = st.toggle("Maintains 3-6 Mo. Emergency Fund", value=pref_init.has_emergency_fund)

    with st.expander("🎯 2. Goals & Time Horizon", expanded=True):
        goal = st.selectbox(
            "Primary Investment Goal",
            options=list(InvestmentGoal),
            index=list(InvestmentGoal).index(pref_init.goal),
            format_func=lambda x: x.value
        )
        purpose = st.selectbox(
            "Investment Purpose",
            options=list(InvestmentPurpose),
            index=list(InvestmentPurpose).index(pref_init.investment_purpose),
            format_func=lambda x: x.value
        )
        horizon = st.selectbox(
            "Investment Time Horizon",
            options=list(InvestmentHorizon),
            index=list(InvestmentHorizon).index(pref_init.investment_horizon),
            format_func=lambda x: x.value
        )
        liquidity = st.selectbox(
            "When Funds May Be Needed",
            options=list(LiquidityNeed),
            index=list(LiquidityNeed).index(pref_init.liquidity_need),
            format_func=lambda x: x.value
        )

    with st.expander("⚖️ 3. Risk Tolerance & Priorities", expanded=True):
        risk_prof = st.selectbox(
            "Subjective Risk Profile",
            options=list(RiskProfile),
            index=list(RiskProfile).index(pref_init.risk_profile),
            format_func=lambda x: x.value
        )
        reaction = st.selectbox(
            "Reaction to -20% Market Drop",
            options=list(MarketDownturnReaction),
            index=list(MarketDownturnReaction).index(pref_init.downturn_reaction),
            format_func=lambda x: x.value
        )
        priority = st.selectbox(
            "Portfolio Core Priority",
            options=list(InvestmentPriority),
            index=list(InvestmentPriority).index(pref_init.investment_priority),
            format_func=lambda x: x.value
        )
        loss_tol = st.slider(
            "Max Tolerable 1-Yr Loss (%)", 5, 40, int(pref_init.max_loss_tolerance * 100)
        ) / 100.0

    with st.expander("💰 4. Capital & Benchmark", expanded=True):
        initial_cap = st.number_input(
            "Initial Investment ($)", min_value=1000.0, max_value=10000000.0,
            value=float(pref_init.initial_investment), step=1000.0
        )
        recurring_cap = st.number_input(
            "Monthly Contribution ($)", min_value=0.0, max_value=500000.0,
            value=float(pref_init.recurring_contribution), step=100.0
        )
        benchmark = st.selectbox(
            "Benchmark ETF",
            options=list(Benchmarks),
            index=list(Benchmarks).index(pref_init.benchmark),
            format_func=lambda x: f"{x.value} — {x.description[:35]}..."
        )

    # Save preference into session state
    current_pref = PortfolioPreference(
        age=age,
        investment_knowledge=knowledge,
        income_level=income,
        goal=goal,
        investment_purpose=purpose,
        investment_horizon=horizon,
        liquidity_need=liquidity,
        risk_profile=risk_prof,
        downturn_reaction=reaction,
        investment_priority=priority,
        max_loss_tolerance=loss_tol,
        has_emergency_fund=has_ef,
        initial_investment=initial_cap,
        recurring_contribution=recurring_cap,
        currency=Currency.USD,
        stock_exchange=StockExchange.NYSE,
        benchmark=benchmark
    )
    st.session_state["preference"] = current_pref

    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if st.button("💾 Save Profile"):
            save_profile(current_pref)
            st.success("Profile saved!")
    with col_btn2:
        include_mpt = st.checkbox("Include MPT Optimizer", value=True)

# === Execute Pipeline ===
data_engine = MarketDataEngine()
report = run_robo_advisor_pipeline(current_pref, data_engine)

# === Top KPI Cards ===
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.metric("Objective Risk Score", f"{report.calculated_risk_score:.1f} / 100")
with col2:
    status_color = "🟢" if report.fiduciary_verdict == "APPROVED" else "🟡"
    st.metric("Fiduciary Status", f"{status_color} {report.fiduciary_verdict}")
with col3:
    st.metric("Expected CAGR", f"{report.portfolio_metrics.cagr * 100:.2f}%")
with col4:
    st.metric("Ann. Volatility", f"{report.portfolio_metrics.annualized_volatility * 100:.2f}%")
with col5:
    st.metric("Weighted TER", f"{report.weighted_expense_ratio * 100:.1f} bps")

st.divider()

# === Navigation Tabs ===
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Portfolio Allocation",
    "📈 Backtest & Performance",
    "🛡️ Multi-Agent Fiduciary Audit",
    "🔬 MPT Quantitative Optimizer",
    "📑 Decision Memo Export"
])

# === Tab 1: Portfolio Allocation ===
with tab1:
    col_t1, col_t2 = st.columns([1, 1.2])

    with col_t1:
        st.subheader("Asset Allocation Targets")
        strat = report.portfolio.strategy
        st.markdown(f"**Strategy:** {strat.strategy_name}")
        st.caption(strat.rationale)

        alloc_data = [
            {"Asset Class": "Equities", "Weight": strat.target_allocation.equities},
            {"Asset Class": "Fixed Income", "Weight": strat.target_allocation.fixed_income},
            {"Asset Class": "Real Estate / REITs", "Weight": strat.target_allocation.real_estate_commodities},
            {"Asset Class": "Cash / T-Bills", "Weight": strat.target_allocation.cash_equivalents},
        ]
        df_alloc = pd.DataFrame(alloc_data)
        df_alloc = df_alloc[df_alloc["Weight"] > 0]

        fig_donut = px.pie(
            df_alloc, values="Weight", names="Asset Class",
            hole=0.45,
            color_discrete_sequence=px.colors.qualitative.Prism,
            title="Strategic Asset Class Allocation"
        )
        fig_donut.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_donut, use_container_width=True)

    with col_t2:
        st.subheader("Constructed ETF Holdings")
        holdings_records = []
        for h in report.portfolio.holdings:
            alloc_dollars = h.weight * current_pref.initial_investment
            holdings_records.append({
                "Symbol": h.symbol,
                "Name": h.name,
                "Asset Class": h.asset_class,
                "Weight (%)": f"{h.weight * 100:.1f}%",
                "Allocation ($)": f"${alloc_dollars:,.2f}",
                "Expense Ratio (TER)": f"{h.expense_ratio:.2f}%"
            })
        st.dataframe(pd.DataFrame(holdings_records), hide_index=True, use_container_width=True)

        st.markdown("#### Portfolio Structural Summary")
        st.markdown(f"- **Total Capital Deployed:** ${current_pref.initial_investment:,.2f}")
        st.markdown(f"- **Planned Monthly Inflow:** ${current_pref.recurring_contribution:,.2f} / month")
        st.markdown(f"- **Effective Number of Holdings (1/HHI):** {1.0 / report.diversification_hhi:.1f}")
        st.markdown(f"- **Blended Fiduciary Expense Ratio:** {report.weighted_expense_ratio:.3f}% ({report.weighted_expense_ratio * 100:.1f} bps)")

# === Tab 2: Backtest & Performance ===
with tab2:
    st.subheader("Historical 2-Year Daily Performance Analysis")
    st.caption(f"Historical backtest comparing the constructed multi-agent portfolio vs. benchmark ({current_pref.benchmark.value}).")

    tickers = [h.symbol for h in report.portfolio.holdings]
    bench_sym = current_pref.benchmark.value
    price_df = data_engine.fetch_multi_asset_prices(tickers + [bench_sym])

    if not price_df.empty:
        # Calculate normalized growth
        weight_map = {h.symbol: h.weight for h in report.portfolio.holdings}
        port_series = pd.Series(0.0, index=price_df.index)
        for sym in tickers:
            if sym in price_df:
                port_series += (price_df[sym] / price_df[sym].iloc[0]) * weight_map[sym]
        
        bench_norm = price_df[bench_sym] / price_df[bench_sym].iloc[0] if bench_sym in price_df else port_series

        perf_chart_df = pd.DataFrame({
            "AI Robo Advisor Portfolio": port_series * 100.0,
            f"Benchmark ({bench_sym})": bench_norm * 100.0
        })

        fig_perf = px.line(
            perf_chart_df,
            labels={"value": "Portfolio Value ($100 Base)", "index": "Date"},
            title="Cumulative Growth of $100 (2-Year Daily History)"
        )
        st.plotly_chart(fig_perf, use_container_width=True)

    # Comparative Metric Grid
    pm = report.portfolio_metrics
    bm = report.benchmark_metrics
    comp_df = pd.DataFrame({
        "Metric": [
            "CAGR (Annualized Return)",
            "Annualized Volatility",
            "Sharpe Ratio (Rf = 4.0%)",
            "Maximum Drawdown",
            "Jensen's Alpha (Annualized)",
            "Beta vs Benchmark"
        ],
        "AI Portfolio": [
            f"{pm.cagr * 100:.2f}%",
            f"{pm.annualized_volatility * 100:.2f}%",
            f"{pm.sharpe_ratio:.2f}",
            f"{pm.max_drawdown * 100:.2f}%",
            f"{pm.alpha * 100:.2f}%",
            f"{pm.beta:.2f}"
        ],
        f"Benchmark ({bench_sym})": [
            f"{bm.cagr * 100:.2f}%",
            f"{bm.annualized_volatility * 100:.2f}%",
            f"{bm.sharpe_ratio:.2f}",
            f"{bm.max_drawdown * 100:.2f}%",
            "0.00%",
            "1.00"
        ]
    })
    st.table(comp_df)

# === Tab 3: Multi-Agent Fiduciary Audit ===
with tab3:
    st.subheader("Multi-Agent Institutional Audit Verdicts")
    st.write(
        "Following the architecture from the tutorial video, four autonomous specialist agents "
        "independently stress-test and evaluate the constructed portfolio."
    )

    verdicts = report.agent_verdicts
    for key, v in verdicts.items():
        badge = "✅ PASS" if v.passed else "⚠️ ATTENTION"
        with st.expander(f"{badge} — {v.agent_name} (Score: {v.score:.1f}/100)", expanded=True):
            st.markdown(f"**Findings:** {v.summary}")
            if v.recommendations:
                st.markdown("**Actionable Agent Recommendations:**")
                for rec in v.recommendations:
                    st.markdown(f"- {rec}")
            else:
                st.success("No compliance adjustments required by this agent.")

    st.subheader("Synthesis Summary & Actionable Advice")
    st.info(report.executive_summary)
    if report.actionable_advice:
        st.markdown("### Concrete Action Items:")
        for adv in report.actionable_advice:
            st.markdown(f"- {adv}")

# === Tab 4: MPT Quantitative Optimizer (Second Architecture) ===
with tab4:
    st.subheader("Comparative Analysis: AI Robo Advisor vs. Classical MPT Frontier")
    st.markdown(
        "**Optional Extension Completed:** Compares the AI multi-agent qualitative/heuristic asset allocation "
        "against an algorithmic Markowitz Modern Portfolio Theory (MPT) mean-variance optimizer over the same ETF universe."
    )

    if include_mpt:
        tickers = [h.symbol for h in report.portfolio.holdings]
        mpt_results = MPTQuantitativeEngine.optimize_efficient_frontier(tickers, data_engine)

        min_vol = mpt_results["min_vol_portfolio"]
        max_sharpe = mpt_results["max_sharpe_portfolio"]

        col_m1, col_m2, col_m3 = st.columns(3)
        with col_m1:
            st.markdown("#### 1. AI Multi-Agent Portfolio")
            st.markdown(f"- **CAGR:** {report.portfolio_metrics.cagr*100:.2f}%")
            st.markdown(f"- **Volatility:** {report.portfolio_metrics.annualized_volatility*100:.2f}%")
            st.markdown(f"- **Sharpe Ratio:** {report.portfolio_metrics.sharpe_ratio:.2f}")
            st.caption("Heuristic mandate alignment + behavioral risk calibration.")

        with col_m2:
            st.markdown("#### 2. MPT Minimum Volatility")
            st.markdown(f"- **Expected Return:** {min_vol['expected_return']*100:.2f}%")
            st.markdown(f"- **Volatility:** {min_vol['volatility']*100:.2f}%")
            st.markdown(f"- **Sharpe Ratio:** {min_vol['sharpe_ratio']:.2f}")
            st.caption("Mathematically minimizes portfolio variance.")

        with col_m3:
            st.markdown("#### 3. MPT Maximum Sharpe")
            st.markdown(f"- **Expected Return:** {max_sharpe['expected_return']*100:.2f}%")
            st.markdown(f"- **Volatility:** {max_sharpe['volatility']*100:.2f}%")
            st.markdown(f"- **Sharpe Ratio:** {max_sharpe['sharpe_ratio']:.2f}")
            st.caption("Maximizes risk-adjusted excess return over risk-free rate.")

        st.markdown("#### Comparative Weight Allocations")
        comp_weights = []
        for sym in tickers:
            ai_w = next(h.weight for h in report.portfolio.holdings if h.symbol == sym)
            comp_weights.append({
                "ETF Symbol": sym,
                "AI Agent Weight": f"{ai_w * 100:.1f}%",
                "MPT Min Volatility Weight": f"{min_vol['weights'].get(sym, 0.0) * 100:.1f}%",
                "MPT Max Sharpe Weight": f"{max_sharpe['weights'].get(sym, 0.0) * 100:.1f}%",
            })
        st.dataframe(pd.DataFrame(comp_weights), hide_index=True, use_container_width=True)

# === Tab 5: Decision Memo Export ===
with tab5:
    st.subheader("Formal Investment Committee Decision Memorandum")
    st.caption("Export-ready markdown memorandum adhering to institutional governance standards.")

    memo_md = f"""# INVESTMENT COMMITTEE DECISION MEMORANDUM
**To:** Investment Review Board  
**From:** Oladapo Olaniyan (FIN 43900 AI Finance Applications)  
**Date:** November 24, 2026  
**Subject:** AI Robo Advisor Portfolio Recommendation & Fiduciary Validation  

---

### 1. Executive Summary & Recommendation
The AI Robo Advisor multi-agent decision system has formulated the **{report.portfolio.strategy.strategy_name}** for client account deployment. Based on an objective risk profile score of **{report.calculated_risk_score:.1f} / 100**, initial capital of **${current_pref.initial_investment:,.2f}**, and a **{current_pref.investment_horizon.value}** investment horizon, the system issues a fiduciary disposition of **[{report.fiduciary_verdict}]**.

### 2. Strategic Asset Allocation & Holdings
- **Equities ({report.portfolio.strategy.target_allocation.equities*100:.1f}%):** Broad US equity diversification via VTI combined with international developed and emerging exposure via VXUS.
- **Fixed Income ({report.portfolio.strategy.target_allocation.fixed_income*100:.1f}%):** High-grade intermediate core credit and Treasuries via BND and IEF.
- **Real Estate ({report.portfolio.strategy.target_allocation.real_estate_commodities*100:.1f}%):** Real asset inflation hedge via VNQ.
- **Cash Equivalents ({report.portfolio.strategy.target_allocation.cash_equivalents*100:.1f}%):** Ultra-short sovereign liquidity buffer via BIL.

**Blended Fiduciary Expense Ratio:** {report.weighted_expense_ratio:.3f}% ({report.weighted_expense_ratio*100:.1f} basis points).

### 3. Historical Backtest & Risk-Adjusted Performance (2-Year Daily)
| Performance Metric | Portfolio | Benchmark ({current_pref.benchmark.value}) |
| :--- | :--- | :--- |
| **CAGR (Annual Return)** | {report.portfolio_metrics.cagr*100:.2f}% | {report.benchmark_metrics.cagr*100:.2f}% |
| **Annualized Volatility** | {report.portfolio_metrics.annualized_volatility*100:.2f}% | {report.benchmark_metrics.annualized_volatility*100:.2f}% |
| **Sharpe Ratio (Rf=4%)** | {report.portfolio_metrics.sharpe_ratio:.2f} | {report.benchmark_metrics.sharpe_ratio:.2f} |
| **Maximum Drawdown** | {report.portfolio_metrics.max_drawdown*100:.2f}% | {report.benchmark_metrics.max_drawdown*100:.2f}% |
| **Jensen's Alpha** | {report.portfolio_metrics.alpha*100:.2f}% | 0.00% |
| **Portfolio Beta** | {report.portfolio_metrics.beta:.2f} | 1.00 |

### 4. Multi-Agent Audit Summary
- **Fees Agent:** {report.agent_verdicts['fees'].summary}
- **Diversification Agent:** {report.agent_verdicts['diversification'].summary}
- **Mandate Alignment Agent:** {report.agent_verdicts['alignment'].summary}
- **Performance Agent:** {report.agent_verdicts['performance'].summary}

---
*Signed and Submitted for Course Credit:*  
**Oladapo Olaniyan**  
FIN 43900 — AI Finance Applications, Daniels School of Business, Purdue University
"""

    st.text_area("Decision Memo (Markdown)", memo_md, height=400)
    st.download_button(
        label="📥 Download Decision Memorandum (.md)",
        data=memo_md,
        file_name="Robo_Advisor_Decision_Memo.md",
        mime="text/markdown"
    )
