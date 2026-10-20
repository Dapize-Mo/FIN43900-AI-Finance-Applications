"""FIN 43900 Lab 14 — Portfolio Risk Engine
Standard library only. Computes covariance, expected return, volatility,
and reserve-eligible metrics for simple baselines against the Meridian mandate.

Student / Author: Oladapo Olaniyan (oolaniy@purdue.edu)
Case: Meridian Foundation Reserve
Date: October 20, 2026
Session Token: portfolio
"""

import math
import sys

# ==============================================================================
# EDITABLE INPUTS (Course-authored training values, not market estimates)
# ==============================================================================

OBJECTIVE_RETURN = 0.065  # CPI (2.5%) + 4.0% = 6.5%

SLEEVES = [
    {"name": "Treasury bills", "return": 0.035, "volatility": 0.005, "reserve_eligible": True},
    {"name": "Treasury 10-year note", "return": 0.043, "volatility": 0.070, "reserve_eligible": True},
    {"name": "Investment-grade bond fund", "return": 0.050, "volatility": 0.060, "reserve_eligible": False},
    {"name": "Global equity index fund", "return": 0.080, "volatility": 0.160, "reserve_eligible": False},
]

# Correlation matrix matching sleeve order:
# [Bills, 10-year, IG bonds, Equity]
CORRELATION = [
    [1.00,  0.10,  0.05,  0.00],
    [0.10,  1.00,  0.80, -0.10],
    [0.05,  0.80,  1.00,  0.25],
    [0.00, -0.10,  0.25,  1.00],
]

# ==============================================================================
# CALCULATION FUNCTIONS (Modular & reusable for Thursday's Streamlit app)
# ==============================================================================

def validate_correlation(matrix: list[list[float]]) -> None:
    """Validate correlation matrix properties: square, bounds [-1, 1], and symmetry."""
    n = len(matrix)
    for i in range(n):
        if len(matrix[i]) != n:
            raise ValueError(f"Correlation matrix must be square: row {i} has {len(matrix[i])} items, expected {n}.")
        for j in range(n):
            val = matrix[i][j]
            if val < -1.0 or val > 1.0:
                raise ValueError(f"Correlation value {val} at ({i}, {j}) is outside the valid range [-1.0, 1.0].")
            if abs(matrix[i][j] - matrix[j][i]) > 1e-9:
                raise ValueError(f"Correlation matrix is not symmetric: ({i},{j})={matrix[i][j]} != ({j},{i})={matrix[j][i]}.")
        if abs(matrix[i][i] - 1.0) > 1e-9:
            raise ValueError(f"Diagonal correlation entry ({i},{i}) must be exactly 1.0, found {matrix[i][i]}.")


def build_covariance(sleeves: list[dict], corr: list[list[float]]) -> list[list[float]]:
    """Build covariance matrix: Cov(i, j) = corr[i][j] * vol[i] * vol[j]."""
    validate_correlation(corr)
    n = len(sleeves)
    cov = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            cov[i][j] = corr[i][j] * sleeves[i]["volatility"] * sleeves[j]["volatility"]
    return cov


def compute_expected_return(weights: list[float], sleeves: list[dict]) -> float:
    """Compute portfolio expected return: sum(w_i * r_i)."""
    return sum(w * s["return"] for w, s in zip(weights, sleeves))


def compute_portfolio_variance(weights: list[float], cov: list[list[float]]) -> float:
    """Compute portfolio variance: sum_i sum_j (w_i * w_j * cov[i][j])."""
    n = len(weights)
    var = 0.0
    for i in range(n):
        for j in range(n):
            var += weights[i] * weights[j] * cov[i][j]
    return var


def compute_portfolio_volatility(weights: list[float], cov: list[list[float]]) -> float:
    """Compute portfolio volatility: sqrt(variance)."""
    var = compute_portfolio_variance(weights, cov)
    return math.sqrt(max(0.0, var))


def compute_reserve_weight(weights: list[float], sleeves: list[dict]) -> float:
    """Compute sum of weights in reserve-eligible sleeves (Treasury bills + 10-year note)."""
    return sum(w for w, s in zip(weights, sleeves) if s["reserve_eligible"])


def get_benchmark_weights() -> list[float]:
    """Benchmark: 40% Investment-grade bond fund, 60% Global equity index fund."""
    return [0.0, 0.0, 0.40, 0.60]


def get_equal_weights(n: int) -> list[float]:
    """Equal weight: 1 / n per sleeve."""
    return [1.0 / n] * n


def get_inverse_volatility_weights(sleeves: list[dict]) -> list[float]:
    """Inverse volatility: each weight = (1 / vol) scaled to sum to 1.0."""
    inv_vols = [1.0 / s["volatility"] for s in sleeves]
    total_inv = sum(inv_vols)
    return [iv / total_inv for iv in inv_vols]


def evaluate_portfolio(name: str, weights: list[float], sleeves: list[dict], cov: list[list[float]], objective: float) -> dict:
    """Evaluate full suite of metrics for a named portfolio allocation."""
    ret = compute_expected_return(weights, sleeves)
    vol = compute_portfolio_volatility(weights, cov)
    reserve = compute_reserve_weight(weights, sleeves)
    meets = ret >= (objective - 1e-9)
    return {
        "name": name,
        "weights": weights,
        "return": ret,
        "volatility": vol,
        "reserve": reserve,
        "meets_objective": meets,
    }


def format_weights(weights: list[float]) -> str:
    """Format weights as 'bills / 10-year / IG / equity' in percent to one decimal."""
    return " / ".join(f"{w * 100.0:.1f}" for w in weights)


def print_portfolio_evaluation(result: dict) -> None:
    """Pretty-print portfolio results matching the Lab 14 specification."""
    w_str = format_weights(result["weights"])
    ret_pct = result["return"] * 100.0
    vol_pct = result["volatility"] * 100.0
    res_pct = result["reserve"] * 100.0
    meets_str = "yes" if result["meets_objective"] else "no"

    print(f"{result['name']}")
    print(f"  Weights (bills / 10-year / IG / equity): {w_str}")
    print(f"  Expected return: {ret_pct:.2f}%")
    print(f"  Volatility:      {vol_pct:.2f}%")
    print(f"  Reserve-eligible: {res_pct:.1f}%")
    print(f"  Meets {OBJECTIVE_RETURN*100:.1f}% objective: {meets_str}")
    print()


# ==============================================================================
# MAIN EXECUTION
# ==============================================================================

def main():
    print("=" * 70)
    print("FIN 43900 Lab 14 -- Portfolio Risk Engine")
    print("Author: Oladapo Olaniyan (oolaniy@purdue.edu)")
    print("Session Token: portfolio")
    print("Objective Return:", f"{OBJECTIVE_RETURN*100.0:.1f}%")
    print("=" * 70)
    print()

    # Build covariance matrix
    cov = build_covariance(SLEEVES, CORRELATION)

    # 1. Benchmark
    bench_weights = get_benchmark_weights()
    bench_res = evaluate_portfolio("Benchmark", bench_weights, SLEEVES, cov, OBJECTIVE_RETURN)
    print_portfolio_evaluation(bench_res)

    # 2. Equal weight
    eq_weights = get_equal_weights(len(SLEEVES))
    eq_res = evaluate_portfolio("Equal weight", eq_weights, SLEEVES, cov, OBJECTIVE_RETURN)
    print_portfolio_evaluation(eq_res)

    # 3. Inverse volatility
    inv_weights = get_inverse_volatility_weights(SLEEVES)
    inv_res = evaluate_portfolio("Inverse volatility", inv_weights, SLEEVES, cov, OBJECTIVE_RETURN)
    print_portfolio_evaluation(inv_res)

    # Print summary table matching Lab 14 known-answer verification
    print("-" * 70)
    print("KNOWN-ANSWER VERIFICATION SUMMARY")
    print("-" * 70)
    print(f"{'Portfolio':<20} {'Weights (bills/10y/IG/eq)':<26} {'Return':<8} {'Vol':<8} {'Reserve':<8} {'Meets 6.5%?'}")
    print("-" * 70)
    for res in [bench_res, eq_res, inv_res]:
        w_s = format_weights(res["weights"])
        r_s = f"{res['return']*100:.2f}"
        v_s = f"{res['volatility']*100:.2f}"
        res_s = f"{res['reserve']*100:.1f}"
        m_s = "yes" if res["meets_objective"] else "no"
        print(f"{res['name']:<20} {w_s:<26} {r_s:<8} {v_s:<8} {res_s:<8} {m_s}")
    print("-" * 70)


if __name__ == "__main__":
    main()
