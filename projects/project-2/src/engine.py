"""
FIN 43900 — Project 2: Investment Management Application
Portfolio Math, Optimization Engine & Stress Testing Framework

Author: Oladapo Olaniyan (oolaniy@purdue.edu)
Institution: Mitchell E. Daniels, Jr. School of Business, Purdue University
"""

import math
from typing import Any, Dict, List, Optional, Tuple
import pandas as pd
import numpy as np

from .mandate import (
    SLEEVES,
    BASE_CORRELATION,
    TARGET_RETURN,
    RESERVE_BUFFER_FLOOR,
    check_mandate,
)


def build_covariance(
    sleeves: List[Dict[str, Any]],
    correlation: List[List[float]],
) -> List[List[float]]:
    """Builds covariance matrix Sigma_ij = rho_ij * sigma_i * sigma_j."""
    n = len(sleeves)
    cov = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            cov[i][j] = correlation[i][j] * sleeves[i]["volatility"] * sleeves[j]["volatility"]
    return cov


def compute_expected_return(weights: List[float], sleeves: List[Dict[str, Any]]) -> float:
    """Computes expected portfolio return: sum(w_i * r_i)."""
    return sum(w * s["return"] for w, s in zip(weights, sleeves))


def compute_portfolio_variance(weights: List[float], cov: List[List[float]]) -> float:
    """Computes portfolio variance: w^T * Sigma * w."""
    n = len(weights)
    var = 0.0
    for i in range(n):
        for j in range(n):
            var += weights[i] * weights[j] * cov[i][j]
    return max(0.0, var)


def compute_portfolio_volatility(weights: List[float], cov: List[List[float]]) -> float:
    """Computes portfolio annualized volatility: sqrt(variance)."""
    return math.sqrt(compute_portfolio_variance(weights, cov))


def compute_sharpe_ratio(
    expected_return: float,
    volatility: float,
    risk_free_rate: float = 0.035,
) -> float:
    """Computes Sharpe ratio: (E[R] - Rf) / vol."""
    if volatility <= 1e-9:
        return 0.0
    return (expected_return - risk_free_rate) / volatility


def evaluate_portfolio(
    name: str,
    weights: List[float],
    sleeves: List[Dict[str, Any]],
    cov: List[List[float]],
    target_return: float = TARGET_RETURN,
    reserve_min: float = RESERVE_BUFFER_FLOOR,
    transaction_cost_bps: float = 0.0,
) -> Dict[str, Any]:
    """
    Evaluates risk, return, Sharpe, reserve metrics, and mandate pass/fail status.
    """
    gross_ret = compute_expected_return(weights, sleeves)
    cost_drag = transaction_cost_bps / 10_000.0
    net_ret = gross_ret - cost_drag
    vol = compute_portfolio_volatility(weights, cov)
    sharpe = compute_sharpe_ratio(net_ret, vol, risk_free_rate=sleeves[0]["return"])

    mandate_audit = check_mandate(
        weights=weights,
        expected_return=net_ret,
        sleeves=sleeves,
        target_return=target_return,
        reserve_min=reserve_min,
    )

    return {
        "name": name,
        "weights": weights,
        "gross_return": gross_ret,
        "net_return": net_ret,
        "volatility": vol,
        "sharpe": sharpe,
        "reserve_weight": mandate_audit["reserve_weight"],
        "mandate_verdict": mandate_audit["verdict"],
        "audit": mandate_audit,
    }


def get_equal_weights(n: int = 4) -> List[float]:
    """Baseline 1: Equal Weight (1/N)."""
    return [1.0 / n] * n


def get_benchmark_weights() -> List[float]:
    """
    Baseline 2: Meridian Strategic Policy Benchmark.
    0% Bills, 0% 10-Yr, 40% IG Bonds (LQD), 60% Global Equity (VT).
    """
    return [0.0, 0.0, 0.40, 0.60]


def generate_weight_grid(n: int, step_pct: int = 2):
    """
    Generates all long-only portfolio allocations summing to 100%
    in step_pct increments (default 2% granularity).
    """
    total_steps = 100 // step_pct

    def helper(dim: int, rem: int):
        if dim == 1:
            yield (rem,)
            return
        for val in range(0, rem + 1):
            for rest in helper(dim - 1, rem - val):
                yield (val,) + rest

    for w_tuple in helper(n, total_steps):
        yield [x * (step_pct / 100.0) for x in w_tuple]


def optimize_constrained_mix(
    sleeves: List[Dict[str, Any]],
    cov: List[List[float]],
    target_return: float = TARGET_RETURN,
    reserve_min: float = RESERVE_BUFFER_FLOOR,
    step_pct: int = 2,
    transaction_cost_bps: float = 0.0,
) -> Optional[Dict[str, Any]]:
    """
    Finds the lowest-volatility portfolio meeting all hard mandate constraints:
      - Long-only: w_i >= 0, sum(w_i) = 1.0
      - Reserve buffer: w_bills + w_10yr >= reserve_min (3.0%)
      - Net return >= target_return (6.5%)
    """
    best_weights = None
    min_vol = float("inf")
    best_eval = None

    cost_drag = transaction_cost_bps / 10_000.0

    for w in generate_weight_grid(len(sleeves), step_pct=step_pct):
        gross_ret = compute_expected_return(w, sleeves)
        net_ret = gross_ret - cost_drag
        if net_ret < target_return - 1e-6:
            continue

        reserve_w = sum(w[i] for i, s in enumerate(sleeves) if s.get("reserve_eligible", False))
        if reserve_w < reserve_min - 1e-6:
            continue

        vol = compute_portfolio_volatility(w, cov)
        if vol < min_vol:
            min_vol = vol
            best_weights = w

    if best_weights is None:
        return None

    return evaluate_portfolio(
        name="Constrained Minimum-Variance Portfolio",
        weights=best_weights,
        sleeves=sleeves,
        cov=cov,
        target_return=target_return,
        reserve_min=reserve_min,
        transaction_cost_bps=transaction_cost_bps,
    )


def run_stress_test(
    sleeves: List[Dict[str, Any]],
    base_corr: List[List[float]],
    equity_return_haircut_bps: float = 0.0,
    credit_spread_shock_bps: float = 0.0,
    equity_bond_corr_shock: float = 0.0,
    reserve_floor_override: Optional[float] = None,
    transaction_cost_bps: float = 0.0,
) -> Dict[str, Any]:
    """
    Conducts comprehensive stress testing across:
      1. Expected return estimates haircut
      2. Credit & Equity correlation spikes (regime breakdown)
      3. Transaction cost slippage
      4. Higher liquidity/reserve floor
    And evaluates whether the process triggers the STOP / KILL rule.
    """
    stressed_sleeves = [dict(s) for s in sleeves]
    # Apply return haircuts
    stressed_sleeves[3]["return"] -= (equity_return_haircut_bps / 10_000.0)  # Equity (VT)
    stressed_sleeves[2]["return"] -= (credit_spread_shock_bps / 10_000.0)   # IG Bonds (LQD)

    # Apply correlation shock between 10-Yr Treasury & Equity, IG Bonds & Equity
    n = len(sleeves)
    stressed_corr = [row[:] for row in base_corr]
    if equity_bond_corr_shock != 0.0:
        # Shock correlation between 10-yr (idx 1) and Equity (idx 3)
        new_c13 = min(0.95, max(-0.95, stressed_corr[1][3] + equity_bond_corr_shock))
        stressed_corr[1][3] = new_c13
        stressed_corr[3][1] = new_c13

        # Shock correlation between IG (idx 2) and Equity (idx 3)
        new_c23 = min(0.95, max(-0.95, stressed_corr[2][3] + equity_bond_corr_shock * 0.5))
        stressed_corr[2][3] = new_c23
        stressed_corr[3][2] = new_c23

    cov_stressed = build_covariance(stressed_sleeves, stressed_corr)

    res_floor = reserve_floor_override if reserve_floor_override is not None else RESERVE_BUFFER_FLOOR

    # Run optimization under stress
    opt_result = optimize_constrained_mix(
        sleeves=stressed_sleeves,
        cov=cov_stressed,
        target_return=TARGET_RETURN,
        reserve_min=res_floor,
        step_pct=2,
        transaction_cost_bps=transaction_cost_bps,
    )

    # Process Kill / Stop Condition Evaluation:
    # 1. Infeasible optimization: No portfolio exists meeting 6.5% return and reserve floor.
    # 2. Risk explosion: Volatility exceeds 12.0% (exceeding committee risk tolerance).
    # 3. Severe drag: Return drops below 5.5% (net real return < 3.0%).
    is_killed = False
    kill_reason = "PROCESS STABLE: All mandate parameters met within risk tolerance bounds."

    if opt_result is None:
        is_killed = True
        kill_reason = "KILL TRIGGER ACTIVATED: Optimization infeasible. No portfolio exists meeting both 6.50% net return and 3.0% reserve buffer under current shocks."
    elif opt_result["volatility"] > 0.120:
        is_killed = True
        kill_reason = f"KILL TRIGGER ACTIVATED: Portfolio volatility ({opt_result['volatility']*100:.2f}%) breaches 12.00% maximum committee risk tolerance."
    elif opt_result["net_return"] < TARGET_RETURN:
        is_killed = True
        kill_reason = f"KILL TRIGGER ACTIVATED: Net return ({opt_result['net_return']*100:.2f}%) falls below 6.50% CPI+4% mandate hurdle."

    return {
        "stressed_sleeves": stressed_sleeves,
        "stressed_corr": stressed_corr,
        "stressed_cov": cov_stressed,
        "result": opt_result,
        "is_killed": is_killed,
        "kill_reason": kill_reason,
    }


def estimate_from_historical_prices(prices_df: pd.DataFrame) -> Dict[str, Any]:
    """
    Computes sample returns, annualized volatilities, and correlation matrix
    from historical monthly prices (assuming 12 observations/year).
    """
    numeric_df = prices_df.drop(columns=["Date"], errors="ignore").select_dtypes(include=[np.number])
    monthly_returns = numeric_df.pct_change().dropna()

    ann_returns = (1.0 + monthly_returns.mean()) ** 12 - 1.0
    ann_vol = monthly_returns.std() * math.sqrt(12)
    sample_corr = monthly_returns.corr()

    return {
        "annualized_returns": ann_returns.to_dict(),
        "annualized_volatilities": ann_vol.to_dict(),
        "sample_correlation": sample_corr.values.tolist(),
        "columns": list(numeric_df.columns),
    }

