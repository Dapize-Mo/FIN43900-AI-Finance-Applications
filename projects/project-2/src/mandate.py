"""
FIN 43900 — Project 2: Investment Management Application
Mandate Specification & Rule Verification Engine

Author: Oladapo Olaniyan (oolaniy@purdue.edu)
Institution: Mitchell E. Daniels, Jr. School of Business, Purdue University
Case: Meridian Foundation Reserve ($100 Million Portfolio)
"""

from typing import Any, Dict, List, Tuple

# ==============================================================================
# GOVERNING MANDATE CONSTANTS (Lab 13 & 14 Authority)
# ==============================================================================

PORTFOLIO_SIZE = 100_000_000.0  # $100 Million Reserve
QUARTERLY_PAYOUT = 750_000.0    # $0.75 Million per quarter
ANNUAL_PAYOUT = QUARTERLY_PAYOUT * 4.0  # $3.0 Million per year (3.0%)
RESERVE_BUFFER_FLOOR = ANNUAL_PAYOUT / PORTFOLIO_SIZE  # 0.030 (3.0% minimum)

INFLATION_BENCHMARK = 0.025     # 2.5% Long-term CPI baseline
REAL_RETURN_HURDLE = 0.040      # 4.0% Real net return over rolling 5-year periods
TARGET_RETURN = INFLATION_BENCHMARK + REAL_RETURN_HURDLE  # 6.5% Net Hurdle

LIQUIDITY_WINDOW_DAYS = 5       # Max redemption window
MIN_LIQUIDITY_RATIO = 0.90      # 90% of assets must be redeemable within 5 days
MAX_SINGLE_ISSUER_WEIGHT = 0.08 # 8.0% Single issuer cap (exempt: Treasuries & broad funds)

# Universe of Sleeves with Fiduciary Classifications
SLEEVES = [
    {
        "ticker": "BIL",
        "name": "Treasury bills (SPDR 1-3M T-Bill)",
        "return": 0.035,
        "volatility": 0.005,
        "reserve_eligible": True,
        "days_to_liquidate": 1,
        "is_exempt_issuer": True,
    },
    {
        "ticker": "IEF",
        "name": "Treasury 10-year note (iShares 7-10Y Treasury)",
        "return": 0.043,
        "volatility": 0.070,
        "reserve_eligible": True,
        "days_to_liquidate": 1,
        "is_exempt_issuer": True,
    },
    {
        "ticker": "LQD",
        "name": "Investment-grade bond fund (iShares iBoxx $ IG)",
        "return": 0.050,
        "volatility": 0.060,
        "reserve_eligible": False,
        "days_to_liquidate": 3,
        "is_exempt_issuer": True,  # Diversified fund
    },
    {
        "ticker": "VT",
        "name": "Global equity index fund (Vanguard Total World)",
        "return": 0.080,
        "volatility": 0.160,
        "reserve_eligible": False,
        "days_to_liquidate": 2,
        "is_exempt_issuer": True,  # Diversified fund
    },
]

# Baseline Correlation Matrix (Bills, 10-Year, IG Bonds, Global Equity)
BASE_CORRELATION = [
    [1.00,  0.10,  0.05,  0.00],
    [0.10,  1.00,  0.80, -0.10],
    [0.05,  0.80,  1.00,  0.25],
    [0.00, -0.10,  0.25,  1.00],
]


def check_mandate(
    weights: List[float],
    expected_return: float,
    sleeves: List[Dict[str, Any]] = SLEEVES,
    target_return: float = TARGET_RETURN,
    reserve_min: float = RESERVE_BUFFER_FLOOR,
) -> Dict[str, Any]:
    """
    Audits a candidate portfolio against every rule in the Meridian Mandate.
    Returns audit verdicts and specific rule breach notes.
    """
    # 1. Allocation Sum check
    alloc_sum = sum(weights)
    sum_pass = abs(alloc_sum - 1.0) <= 1e-4

    # 2. Long-only constraint
    long_only_pass = all(w >= -1e-6 for w in weights)

    # 3. Reserve Buffer Floor (12 months payout in sovereign paper/cash)
    reserve_weight = sum(w for w, s in zip(weights, sleeves) if s.get("reserve_eligible", False))
    reserve_pass = reserve_weight >= (reserve_min - 1e-6)

    # 4. Return Hurdle (CPI + 4.0% = 6.5%)
    return_pass = expected_return >= (target_return - 1e-6)

    # 5. 5-Day Liquidity floor (90%)
    liquid_weight = sum(w for w, s in zip(weights, sleeves) if s.get("days_to_liquidate", 0) <= LIQUIDITY_WINDOW_DAYS)
    liquidity_pass = liquid_weight >= (MIN_LIQUIDITY_RATIO - 1e-6)

    # 6. Single Issuer Cap (8% for non-exempt)
    issuer_pass = True
    for w, s in zip(weights, sleeves):
        if not s.get("is_exempt_issuer", False) and w > (MAX_SINGLE_ISSUER_WEIGHT + 1e-6):
            issuer_pass = False
            break

    # Overall Fiduciary Verdict
    overall_pass = sum_pass and long_only_pass and reserve_pass and return_pass and liquidity_pass and issuer_pass

    # Breached rules list
    breaches = []
    if not sum_pass:
        breaches.append(f"Allocation sum ({alloc_sum * 100:.1f}%) != 100.0%")
    if not long_only_pass:
        breaches.append("Violates long-only rule (negative weight present)")
    if not reserve_pass:
        breaches.append(f"Reserve buffer ({reserve_weight * 100:.1f}%) < required floor ({reserve_min * 100:.1f}%)")
    if not return_pass:
        breaches.append(f"Expected return ({expected_return * 100:.2f}%) < target hurdle ({target_return * 100:.2f}%)")
    if not liquidity_pass:
        breaches.append(f"5-day liquidity ({liquid_weight * 100:.1f}%) < required minimum (90.0%)")
    if not issuer_pass:
        breaches.append("Exceeds 8.0% single non-exempt issuer cap")

    return {
        "verdict": "PASS" if overall_pass else "FAIL",
        "overall_pass": overall_pass,
        "sum_pass": sum_pass,
        "long_only_pass": long_only_pass,
        "reserve_pass": reserve_pass,
        "return_pass": return_pass,
        "liquidity_pass": liquidity_pass,
        "issuer_pass": issuer_pass,
        "reserve_weight": reserve_weight,
        "expected_return": expected_return,
        "breaches": breaches,
    }

