"""
FIN 43900 — AI Finance Applications
Module: Automated Test Suite for AI Robo Advisor
Author: Oladapo Olaniyan
Date: November 2026

Comprehensive unit and integration tests verifying questionnaire validation,
multi-agent portfolio construction, risk calculations, caching, and MPT optimization.
"""

import sys
import os
import pytest
import numpy as np

# Ensure parent directory is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

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
from robo_engine import (
    MPTQuantitativeEngine,
    audit_alignment,
    audit_diversification,
    audit_fees,
    build_etf_portfolio,
    calculate_risk_score,
    formulate_strategy,
    run_robo_advisor_pipeline,
)
from data_engine import MarketDataEngine, calculate_performance_metrics
from storage import load_profile, save_profile


@pytest.fixture
def sample_preference() -> PortfolioPreference:
    return PortfolioPreference(
        age=30,
        investment_knowledge=InvestmentKnowledge.ADVANCED,
        income_level=IncomeLevel.FROM_100K_TO_150K,
        goal=InvestmentGoal.WEALTH_BUILDING,
        investment_purpose=InvestmentPurpose.GROW_WEALTH,
        investment_horizon=InvestmentHorizon.LONG_TERM,
        liquidity_need=LiquidityNeed.OVER_5_YEARS,
        risk_profile=RiskProfile.AGGRESSIVE,
        downturn_reaction=MarketDownturnReaction.BUY_MORE,
        investment_priority=InvestmentPriority.GROWTH,
        max_loss_tolerance=0.25,
        has_emergency_fund=True,
        initial_investment=50000.0,
        recurring_contribution=2000.0,
        currency=Currency.USD,
        stock_exchange=StockExchange.NYSE,
        benchmark=Benchmarks.SPY
    )


def test_preference_model_validation(sample_preference):
    """Verifies schema validation and defaults."""
    assert sample_preference.age == 30
    assert sample_preference.initial_investment == 50000.0
    assert sample_preference.benchmark == Benchmarks.SPY


def test_risk_score_monotonicity(sample_preference):
    """Verifies that conservative inputs yield lower risk scores than aggressive inputs."""
    aggressive_score = calculate_risk_score(sample_preference)

    conservative_pref = sample_preference.model_copy(update={
        "risk_profile": RiskProfile.ULTRA_CONSERVATIVE,
        "downturn_reaction": MarketDownturnReaction.SELL_ALL,
        "investment_horizon": InvestmentHorizon.SHORT_TERM,
        "max_loss_tolerance": 0.05
    })
    conservative_score = calculate_risk_score(conservative_pref)

    assert conservative_score < aggressive_score
    assert 5.0 <= conservative_score <= 100.0
    assert 5.0 <= aggressive_score <= 100.0


def test_strategy_asset_allocation_sum(sample_preference):
    """Verifies that strategy targets sum to 1.0 (100%)."""
    score = calculate_risk_score(sample_preference)
    strategy = formulate_strategy(sample_preference, score)
    alloc = strategy.target_allocation
    total_w = alloc.equities + alloc.fixed_income + alloc.real_estate_commodities + alloc.cash_equivalents
    assert abs(total_w - 1.0) < 1e-4


def test_portfolio_holdings_integrity(sample_preference):
    """Verifies that portfolio holdings weights sum to 1.0 and expense ratios are realistic."""
    score = calculate_risk_score(sample_preference)
    strategy = formulate_strategy(sample_preference, score)
    portfolio = build_etf_portfolio(strategy, sample_preference.benchmark)

    total_weight = sum(h.weight for h in portfolio.holdings)
    assert abs(total_weight - 1.0) < 1e-4

    for h in portfolio.holdings:
        assert h.weight > 0.0
        assert 0.0 <= h.expense_ratio <= 0.50
        assert len(h.symbol) >= 2


def test_fees_agent_audit(sample_preference):
    """Verifies fees agent correctly audits weighted expense ratio."""
    score = calculate_risk_score(sample_preference)
    strategy = formulate_strategy(sample_preference, score)
    portfolio = build_etf_portfolio(strategy, sample_preference.benchmark)
    verdict = audit_fees(portfolio)

    assert verdict.agent_name == "Fees & Expense Auditor"
    assert verdict.passed is True  # Vanguard/iShares ETFs are well below 15 bps
    assert verdict.score >= 70.0


def test_diversification_agent_audit(sample_preference):
    """Verifies diversification agent computes valid HHI and effective holding counts."""
    score = calculate_risk_score(sample_preference)
    strategy = formulate_strategy(sample_preference, score)
    portfolio = build_etf_portfolio(strategy, sample_preference.benchmark)
    verdict = audit_diversification(portfolio)

    assert verdict.agent_name == "Diversification & Breadth Auditor"
    assert verdict.score > 0.0


def test_storage_persistence(sample_preference):
    """Verifies state persistence saving and loading."""
    test_fname = "test_pytest_profile.json"
    saved_path = save_profile(sample_preference, filename=test_fname)
    assert os.path.exists(saved_path)

    # Test load
    loaded = load_profile(saved_path)
    assert loaded is not None
    assert loaded.age == sample_preference.age
    assert loaded.goal == sample_preference.goal

    # Clean up test file
    try:
        if os.path.exists(saved_path):
            os.remove(saved_path)
    except Exception:
        pass


def test_mpt_optimizer():
    """Verifies Markowitz MPT optimizer computes valid weights summing to 1.0."""
    tickers = ["VTI", "BND", "VNQ"]
    data_engine = MarketDataEngine()
    results = MPTQuantitativeEngine.optimize_efficient_frontier(tickers, data_engine)

    assert "min_vol_portfolio" in results
    assert "max_sharpe_portfolio" in results

    min_vol_weights = results["min_vol_portfolio"]["weights"]
    max_s_weights = results["max_sharpe_portfolio"]["weights"]

    assert abs(sum(min_vol_weights.values()) - 1.0) < 1e-3
    assert abs(sum(max_s_weights.values()) - 1.0) < 1e-3


def test_full_pipeline_run(sample_preference):
    """Verifies end-to-end execution of the multi-agent pipeline."""
    report = run_robo_advisor_pipeline(sample_preference)
    assert report.investor_name == "Oladapo Olaniyan"
    assert report.fiduciary_verdict in ["APPROVED", "REVISION_REQUIRED"]
    assert len(report.portfolio.holdings) >= 3
    assert report.portfolio_metrics.annualized_volatility > 0.0
