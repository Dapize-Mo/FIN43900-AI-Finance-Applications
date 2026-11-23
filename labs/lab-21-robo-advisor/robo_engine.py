"""
FIN 43900 — AI Finance Applications
Module: Multi-Agent Robo Advisor Intelligence & MPT Quantitative Engine
Author: Oladapo Olaniyan
Date: November 2026

Replicates and extends the multi-agent architecture from matvix90/ai-robo-advisor
demonstrated in Dr. Z's tutorial video (Investment Agent -> Portfolio Agent ->
Analyst Agents -> Orchestrator) and introduces an MPT Modern Portfolio Theory
quantitative optimizer for comparative analysis.
"""

from typing import Dict, List, Tuple, Optional, Any
import numpy as np
import pandas as pd
from scipy.optimize import minimize

from models import (
    AgentAuditVerdict,
    AssetAllocationTarget,
    Benchmarks,
    FullRoboAdvisorReport,
    InvestmentGoal,
    InvestmentHorizon,
    MarketDownturnReaction,
    PerformanceMetrics,
    Portfolio,
    PortfolioHolding,
    PortfolioPreference,
    PortfolioStrategy,
    RiskProfile,
)
from data_engine import MarketDataEngine, calculate_performance_metrics


# === 1. Risk Scoring Engine ===
def calculate_risk_score(pref: PortfolioPreference) -> float:
    """
    Computes an objective, normalized risk score (1.0 to 100.0)
    combining psychological tolerance, financial capacity, and investment horizon.
    """
    # Baseline from declared Risk Profile (Weight: 35%)
    profile_scores = {
        RiskProfile.ULTRA_CONSERVATIVE: 10.0,
        RiskProfile.CONSERVATIVE: 25.0,
        RiskProfile.MODERATE_CONSERVATIVE: 40.0,
        RiskProfile.MODERATE: 55.0,
        RiskProfile.MODERATE_AGGRESSIVE: 70.0,
        RiskProfile.AGGRESSIVE: 85.0,
        RiskProfile.ULTRA_AGGRESSIVE: 98.0,
    }
    score_profile = profile_scores.get(pref.risk_profile, 50.0)

    # Time Horizon Score (Weight: 25%)
    horizon_scores = {
        InvestmentHorizon.SHORT_TERM: 20.0,
        InvestmentHorizon.MEDIUM_TERM: 50.0,
        InvestmentHorizon.LONG_TERM: 80.0,
        InvestmentHorizon.VERY_LONG_TERM: 95.0,
    }
    score_horizon = horizon_scores.get(pref.investment_horizon, 50.0)

    # Market Downturn Reaction Score (Weight: 20%)
    reaction_scores = {
        MarketDownturnReaction.SELL_ALL: 5.0,
        MarketDownturnReaction.SELL_SOME: 30.0,
        MarketDownturnReaction.HOLD: 65.0,
        MarketDownturnReaction.BUY_MORE: 95.0,
    }
    score_reaction = reaction_scores.get(pref.downturn_reaction, 60.0)

    # Financial Capacity: Age, Emergency Fund, Loss Tolerance (Weight: 20%)
    age_factor = max(10.0, 100.0 - float(pref.age))
    ef_bonus = 10.0 if pref.has_emergency_fund else -15.0
    loss_factor = min(pref.max_loss_tolerance * 250.0, 100.0)
    score_capacity = 0.4 * age_factor + 0.3 * loss_factor + 0.3 * (50.0 + ef_bonus)

    composite = (
        0.35 * score_profile +
        0.25 * score_horizon +
        0.20 * score_reaction +
        0.20 * score_capacity
    )
    return float(np.clip(composite, 5.0, 98.0))


# === 2. Investment Strategy Formulation Agent ===
def formulate_strategy(pref: PortfolioPreference, risk_score: float) -> PortfolioStrategy:
    """
    Investment Agent: Formulates target macro asset allocations
    and capital market return/volatility expectations.
    """
    # Equity allocation scales smoothly with risk score
    equity_weight = float(np.clip((risk_score - 10.0) / 90.0 * 0.75 + 0.15, 0.10, 0.90))
    
    # Real Estate sleeve allocation (0% to 10%)
    if pref.goal in [InvestmentGoal.WEALTH_BUILDING, InvestmentGoal.INCOME_GENERATION]:
        re_weight = 0.08 if risk_score > 40.0 else 0.05
    else:
        re_weight = 0.03 if risk_score > 50.0 else 0.0

    # Cash sleeve for short-term liquidity
    if pref.investment_horizon == InvestmentHorizon.SHORT_TERM or not pref.has_emergency_fund:
        cash_weight = 0.15
    else:
        cash_weight = 0.02

    # Fixed income captures remainder
    fixed_income_weight = float(max(0.0, 1.0 - (equity_weight + re_weight + cash_weight)))

    # Re-normalize to exact 1.0
    total = equity_weight + fixed_income_weight + re_weight + cash_weight
    target = AssetAllocationTarget(
        equities=round(equity_weight / total, 3),
        fixed_income=round(fixed_income_weight / total, 3),
        real_estate_commodities=round(re_weight / total, 3),
        cash_equivalents=round(cash_weight / total, 3)
    )

    # Capital market assumptions (CMA) expected metrics
    exp_return = target.equities * 0.085 + target.fixed_income * 0.045 + target.real_estate_commodities * 0.075 + target.cash_equivalents * 0.040
    exp_vol = target.equities * 0.160 + target.fixed_income * 0.055 + target.real_estate_commodities * 0.180 + target.cash_equivalents * 0.005

    strategy_name = (
        "Aggressive Growth Mandate" if risk_score >= 75 else
        "Moderate Growth & Capital Appreciation" if risk_score >= 50 else
        "Balanced Income & Growth" if risk_score >= 35 else
        "Conservative Capital Preservation"
    )

    rationale = (
        f"Calibrated for risk score {risk_score:.1f}/100 and horizon '{pref.investment_horizon.value}'. "
        f"Allocates {target.equities*100:.1f}% to diversified equities, {target.fixed_income*100:.1f}% to high-grade fixed income, "
        f"{target.real_estate_commodities*100:.1f}% to real assets, and {target.cash_equivalents*100:.1f}% to cash liquidity reserves."
    )

    return PortfolioStrategy(
        strategy_name=strategy_name,
        target_allocation=target,
        expected_annual_return=round(exp_return, 4),
        expected_annual_volatility=round(exp_vol, 4),
        rationale=rationale
    )


# === 3. Portfolio Construction Agent ===
def build_etf_portfolio(strategy: PortfolioStrategy, benchmark: Benchmarks) -> Portfolio:
    """
    Portfolio Agent: Populates macro asset allocations with ultra-low-cost,
    highly liquid Vanguard/iShares ETFs.
    """
    target = strategy.target_allocation
    holdings: List[PortfolioHolding] = []

    # Equities: 70% US Total Market (VTI) / 30% International (VXUS)
    us_eq = target.equities * 0.70
    intl_eq = target.equities * 0.30
    if us_eq > 0.01:
        holdings.append(PortfolioHolding(
            symbol="VTI", name="Vanguard Total Stock Market ETF",
            asset_class="Equity", sub_category="US Broad Equities",
            weight=round(us_eq, 4), expense_ratio=0.03
        ))
    if intl_eq > 0.01:
        holdings.append(PortfolioHolding(
            symbol="VXUS", name="Vanguard Total International Stock ETF",
            asset_class="Equity", sub_category="Global Ex-US Equities",
            weight=round(intl_eq, 4), expense_ratio=0.07
        ))

    # Fixed Income: 75% US Aggregate (BND) / 25% Intermediate Treasury (IEF)
    if target.fixed_income > 0.01:
        bnd_w = target.fixed_income * 0.75
        ief_w = target.fixed_income * 0.25
        holdings.append(PortfolioHolding(
            symbol="BND", name="Vanguard Total Bond Market ETF",
            asset_class="Fixed Income", sub_category="US Aggregate Core Bond",
            weight=round(bnd_w, 4), expense_ratio=0.03
        ))
        if ief_w > 0.01:
            holdings.append(PortfolioHolding(
                symbol="IEF", name="iShares 7-10 Year Treasury Bond ETF",
                asset_class="Fixed Income", sub_category="Intermediate US Treasury",
                weight=round(ief_w, 4), expense_ratio=0.15
            ))

    # Real Estate: Vanguard Real Estate (VNQ)
    if target.real_estate_commodities > 0.01:
        holdings.append(PortfolioHolding(
            symbol="VNQ", name="Vanguard Real Estate ETF",
            asset_class="Real Estate", sub_category="US REITs",
            weight=round(target.real_estate_commodities, 4), expense_ratio=0.13
        ))

    # Cash Equivalents: SPDR 1-3 Month T-Bill (BIL)
    if target.cash_equivalents > 0.01:
        holdings.append(PortfolioHolding(
            symbol="BIL", name="SPDR Bloomberg 1-3 Month T-Bill ETF",
            asset_class="Cash", sub_category="Ultra-Short Sovereign Treasury",
            weight=round(target.cash_equivalents, 4), expense_ratio=0.14
        ))

    # Normalize weights so they sum exactly to 1.0000
    total_w = sum(h.weight for h in holdings)
    for h in holdings:
        h.weight = round(h.weight / total_w, 4)

    # Adjust rounding discrepancy on largest holding
    diff = 1.0 - sum(h.weight for h in holdings)
    if abs(diff) > 1e-5 and holdings:
        holdings[0].weight = round(holdings[0].weight + diff, 4)

    return Portfolio(
        strategy=strategy,
        holdings=holdings,
        benchmark=benchmark
    )


# === 4. Analyst Sub-Agents ===
def audit_fees(portfolio: Portfolio) -> AgentAuditVerdict:
    """Fees Agent: Audits Total Expense Ratio (TER) and checks against fiduciary ceiling."""
    weighted_ter = sum(h.weight * h.expense_ratio for h in portfolio.holdings)
    passed = weighted_ter <= 0.15  # 15 bps threshold
    score = max(0.0, 100.0 - weighted_ter * 400.0)

    recommendations = []
    for h in portfolio.holdings:
        if h.expense_ratio > 0.20:
            recommendations.append(f"Consider replacing {h.symbol} ({h.expense_ratio:.2f}% TER) with an ultra-low-cost index alternative.")

    summary = (
        f"Weighted Expense Ratio is {weighted_ter:.3f}% ({weighted_ter*100:.1f} bps). "
        f"Meets fiduciary institutional cost efficiency standard (< 0.15%)." if passed else
        f"Weighted Expense Ratio is {weighted_ter:.3f}% ({weighted_ter*100:.1f} bps), exceeding 15 bps ceiling."
    )

    return AgentAuditVerdict(
        agent_name="Fees & Expense Auditor",
        passed=passed,
        score=round(score, 1),
        summary=summary,
        recommendations=recommendations
    )


def audit_diversification(portfolio: Portfolio) -> AgentAuditVerdict:
    """Diversification Agent: Computes HHI concentration and asset class breadth."""
    weights = [h.weight for h in portfolio.holdings]
    hhi = sum(w**2 for w in weights)
    effective_n = 1.0 / hhi if hhi > 0 else 0.0

    asset_classes = set(h.asset_class for h in portfolio.holdings)
    passed = hhi < 0.40 and len(asset_classes) >= 2
    score = min(100.0, effective_n * 22.0)

    recommendations = []
    if hhi >= 0.40:
        recommendations.append(f"Portfolio concentration is high (HHI: {hhi:.3f}, Effective N: {effective_n:.1f}). Add complementary asset classes.")
    if "Equity" in asset_classes and not any(h.symbol == "VXUS" for h in portfolio.holdings):
        recommendations.append("Lacks international ex-US equity exposure. Add VXUS for global geographical diversification.")

    summary = (
        f"HHI concentration score is {hhi:.3f} with an effective holding count of {effective_n:.1f} across {len(asset_classes)} distinct asset sleeves. Diversification approved."
        if passed else
        f"HHI score is {hhi:.3f} (above 0.40 threshold). Over-concentrated in primary holding."
    )

    return AgentAuditVerdict(
        agent_name="Diversification & Breadth Auditor",
        passed=passed,
        score=round(score, 1),
        summary=summary,
        recommendations=recommendations
    )


def audit_alignment(portfolio: Portfolio, pref: PortfolioPreference, risk_score: float) -> AgentAuditVerdict:
    """Alignment Agent: Verifies that constructed portfolio aligns with user risk tolerance and liquidity."""
    target_eq = portfolio.strategy.target_allocation.equities
    recommendations = []
    passed = True

    # 1. Equity risk alignment
    if risk_score < 35.0 and target_eq > 0.45:
        passed = False
        recommendations.append("Equity exposure exceeds conservative risk capacity. Reduce equities below 40%.")
    elif risk_score > 75.0 and target_eq < 0.65:
        recommendations.append("Equity exposure may be conservative for aggressive wealth building goals.")

    # 2. Emergency reserve liquidity check
    cash_w = portfolio.strategy.target_allocation.cash_equivalents
    if not pref.has_emergency_fund and cash_w < 0.10:
        passed = False
        recommendations.append("User reported no emergency fund. Fiduciary mandate requires at least 10% cash/T-Bills buffer.")

    score = 90.0 if passed else 60.0
    summary = (
        f"Portfolio strategy alignment verified. Equity allocation ({target_eq*100:.1f}%) and cash reserves match user risk tolerance and stated time horizon."
        if passed else
        "Mandate alignment issues detected. Please review risk tolerance or emergency cash requirements."
    )

    return AgentAuditVerdict(
        agent_name="Mandate Alignment Auditor",
        passed=passed,
        score=score,
        summary=summary,
        recommendations=recommendations
    )


def audit_performance(
    portfolio: Portfolio,
    data_engine: MarketDataEngine
) -> Tuple[AgentAuditVerdict, PerformanceMetrics, PerformanceMetrics]:
    """Performance Agent: Analyzes 2-year historical CAGR, Volatility, Sharpe, Drawdown vs Benchmark."""
    tickers = [h.symbol for h in portfolio.holdings]
    bench_ticker = portfolio.benchmark.value
    all_tickers = tickers + [bench_ticker]

    price_df = data_engine.fetch_multi_asset_prices(all_tickers)
    weight_map = {h.symbol: h.weight for h in portfolio.holdings}

    # Construct weighted portfolio price index
    port_prices = pd.Series(0.0, index=price_df.index)
    for sym in tickers:
        if sym in price_df:
            port_prices += price_df[sym] * weight_map[sym]
        else:
            port_prices += price_df.iloc[:, 0] * weight_map[sym]

    bench_prices = price_df[bench_ticker] if bench_ticker in price_df else price_df.iloc[:, -1]
    port_metrics, bench_metrics = calculate_performance_metrics(port_prices, bench_prices)

    # Performance audit criteria
    passed = port_metrics.sharpe_ratio >= 0.30 and port_metrics.max_drawdown >= -0.35
    score = min(100.0, max(20.0, 50.0 + port_metrics.sharpe_ratio * 40.0 + port_metrics.alpha * 500.0))

    recommendations = []
    if port_metrics.sharpe_ratio < 0.50:
        recommendations.append(f"Historical Sharpe ratio ({port_metrics.sharpe_ratio:.2f}) is modest. Consider optimizing weights for risk-adjusted return.")
    if abs(port_metrics.max_drawdown) > 0.25:
        recommendations.append(f"Historical Max Drawdown reached {port_metrics.max_drawdown*100:.1f}%. Increase fixed income allocation to cushion downturns.")

    summary = (
        f"Historical performance validated: CAGR: {port_metrics.cagr*100:.2f}%, Volatility: {port_metrics.annualized_volatility*100:.2f}%, "
        f"Sharpe: {port_metrics.sharpe_ratio:.2f}, Max Drawdown: {port_metrics.max_drawdown*100:.1f}%, Alpha: {port_metrics.alpha*100:.2f}% vs {bench_ticker}."
    )

    verdict = AgentAuditVerdict(
        agent_name="Quantitative Performance Auditor",
        passed=passed,
        score=round(score, 1),
        summary=summary,
        recommendations=recommendations
    )
    return verdict, port_metrics, bench_metrics


# === 5. Analysis Orchestrator ===
def run_robo_advisor_pipeline(
    pref: PortfolioPreference,
    data_engine: Optional[MarketDataEngine] = None
) -> FullRoboAdvisorReport:
    """
    End-to-end execution of the multi-agent Robo Advisor pipeline.
    """
    if data_engine is None:
        data_engine = MarketDataEngine()

    # Step 1: Calculate Risk Score
    risk_score = calculate_risk_score(pref)

    # Step 2: Formulate Strategy
    strategy = formulate_strategy(pref, risk_score)

    # Step 3: Build Portfolio
    portfolio = build_etf_portfolio(strategy, pref.benchmark)

    # Step 4: Run Sub-Agents
    fees_verdict = audit_fees(portfolio)
    div_verdict = audit_diversification(portfolio)
    align_verdict = audit_alignment(portfolio, pref, risk_score)
    perf_verdict, port_metrics, bench_metrics = audit_performance(portfolio, data_engine)

    agent_verdicts = {
        "fees": fees_verdict,
        "diversification": div_verdict,
        "alignment": align_verdict,
        "performance": perf_verdict,
    }

    # Step 5: Orchestrate Synthesis
    all_passed = all(v.passed for v in agent_verdicts.values())
    avg_score = np.mean([v.score for v in agent_verdicts.values()])
    fiduciary_verdict = "APPROVED" if (all_passed and avg_score >= 70.0) else "REVISION_REQUIRED"

    all_recommendations = []
    for v in agent_verdicts.values():
        all_recommendations.extend(v.recommendations)

    weighted_ter = sum(h.weight * h.expense_ratio for h in portfolio.holdings)
    hhi = sum(h.weight**2 for h in portfolio.holdings)

    exec_summary = (
        f"AI Robo Advisor has formulated the '{strategy.strategy_name}' for Oladapo Olaniyan "
        f"with a composite risk score of {risk_score:.1f}/100. The allocation spans {len(portfolio.holdings)} institutional ETFs "
        f"with an ultra-low weighted TER of {weighted_ter:.3f}% ({weighted_ter*100:.1f} bps). "
        f"Overall fiduciary disposition: {fiduciary_verdict} (Composite Health Score: {avg_score:.1f}/100)."
    )

    return FullRoboAdvisorReport(
        investor_name="Oladapo Olaniyan",
        preference=pref,
        calculated_risk_score=round(risk_score, 1),
        portfolio=portfolio,
        portfolio_metrics=port_metrics,
        benchmark_metrics=bench_metrics,
        weighted_expense_ratio=round(weighted_ter, 4),
        diversification_hhi=round(hhi, 4),
        agent_verdicts=agent_verdicts,
        fiduciary_verdict=fiduciary_verdict,
        executive_summary=exec_summary,
        actionable_advice=all_recommendations
    )


# === 6. Optional Comparative Engine: Markowitz MPT Optimizer ===
class MPTQuantitativeEngine:
    """
    Implements a classical Markowitz Modern Portfolio Theory (MPT) mean-variance
    optimizer as an open-source comparative architecture.
    """

    @staticmethod
    def optimize_efficient_frontier(
        tickers: List[str],
        data_engine: MarketDataEngine,
        target_annual_return: Optional[float] = None,
        risk_free_rate: float = 0.04
    ) -> Dict[str, Any]:
        """Computes Minimum Volatility and Maximum Sharpe optimal portfolios."""
        df_prices = data_engine.fetch_multi_asset_prices(tickers)
        ret_df = df_prices.pct_change().dropna()
        n = len(tickers)

        mean_rets = ret_df.mean() * 252
        cov_matrix = ret_df.cov() * 252

        # 1. Minimum Volatility Optimization
        def min_vol(w):
            return np.sqrt(np.dot(w.T, np.dot(cov_matrix, w)))

        bounds = tuple((0.02, 0.70) for _ in range(n))
        constraints = {"type": "eq", "fun": lambda w: np.sum(w) - 1.0}
        w0 = np.array([1.0 / n] * n)

        res_min_vol = minimize(min_vol, w0, method="SLSQP", bounds=bounds, constraints=constraints)
        w_min_vol = res_min_vol.x if res_min_vol.success else w0

        # 2. Maximum Sharpe Ratio Optimization
        def neg_sharpe(w):
            p_ret = np.sum(mean_rets * w)
            p_vol = np.sqrt(np.dot(w.T, np.dot(cov_matrix, w)))
            return -(p_ret - risk_free_rate) / p_vol if p_vol > 1e-4 else 0.0

        res_max_sharpe = minimize(neg_sharpe, w0, method="SLSQP", bounds=bounds, constraints=constraints)
        w_max_sharpe = res_max_sharpe.x if res_max_sharpe.success else w0

        # Format weights dictionary
        min_vol_dict = {tickers[i]: round(float(w_min_vol[i]), 4) for i in range(n)}
        max_sharpe_dict = {tickers[i]: round(float(w_max_sharpe[i]), 4) for i in range(n)}

        vol_min = float(min_vol(w_min_vol))
        ret_min = float(np.sum(mean_rets * w_min_vol))
        sharpe_min = (ret_min - risk_free_rate) / vol_min if vol_min > 0 else 0.0

        vol_max_s = float(min_vol(w_max_sharpe))
        ret_max_s = float(np.sum(mean_rets * w_max_sharpe))
        sharpe_max = (ret_max_s - risk_free_rate) / vol_max_s if vol_max_s > 0 else 0.0

        return {
            "tickers": tickers,
            "min_vol_portfolio": {
                "weights": min_vol_dict,
                "expected_return": round(ret_min, 4),
                "volatility": round(vol_min, 4),
                "sharpe_ratio": round(sharpe_min, 2)
            },
            "max_sharpe_portfolio": {
                "weights": max_sharpe_dict,
                "expected_return": round(ret_max_s, 4),
                "volatility": round(vol_max_s, 4),
                "sharpe_ratio": round(sharpe_max, 2)
            }
        }
