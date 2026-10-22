"""FIN 43900 Lab 14 & 15 - Portfolio Risk & Stability Engine
Standard library only. Computes covariance, expected return, volatility,
reserve-eligible metrics for simple baselines against the Meridian mandate,
and provides grid search optimization and historical price estimation.

Student / Author: Oladapo Olaniyan (oolaniy@purdue.edu)
Case: Meridian Foundation Reserve ($100 Million Reserve)
Date: October 22, 2026
Course: FIN 43900 -- AI Finance Applications, Purdue University
Session Token: webapp
"""

import csv
import math
import sys
from typing import Any, Dict, List, Optional, Tuple, Union

# ==============================================================================
# EDITABLE INPUTS (Course-authored training values, not market estimates)
# ==============================================================================

OBJECTIVE_RETURN = 0.065  # CPI (2.5%) + 4.0% = 6.5%
RESERVE_MINIMUM = 0.030   # Minimum 3.0% reserve-eligible requirement

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
# CALCULATION FUNCTIONS (Lab 14 Foundation)
# ==============================================================================

def validate_correlation(matrix: List[List[float]]) -> None:
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


def build_covariance(sleeves: List[Dict[str, Any]], corr: List[List[float]]) -> List[List[float]]:
    """Build covariance matrix: Cov(i, j) = corr[i][j] * vol[i] * vol[j]."""
    validate_correlation(corr)
    n = len(sleeves)
    cov = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            cov[i][j] = corr[i][j] * sleeves[i]["volatility"] * sleeves[j]["volatility"]
    return cov


def compute_expected_return(weights: List[float], sleeves: List[Dict[str, Any]]) -> float:
    """Compute portfolio expected return: sum(w_i * r_i)."""
    return sum(w * s["return"] for w, s in zip(weights, sleeves))


def compute_portfolio_variance(weights: List[float], cov: List[List[float]]) -> float:
    """Compute portfolio variance: sum_i sum_j (w_i * w_j * cov[i][j])."""
    n = len(weights)
    var = 0.0
    for i in range(n):
        for j in range(n):
            var += weights[i] * weights[j] * cov[i][j]
    return var


def compute_portfolio_volatility(weights: List[float], cov: List[List[float]]) -> float:
    """Compute portfolio volatility: sqrt(variance)."""
    var = compute_portfolio_variance(weights, cov)
    return math.sqrt(max(0.0, var))


def compute_reserve_weight(weights: List[float], sleeves: List[Dict[str, Any]]) -> float:
    """Compute sum of weights in reserve-eligible sleeves (Treasury bills + 10-year note)."""
    return sum(w for w, s in zip(weights, sleeves) if s.get("reserve_eligible", False))


def get_benchmark_weights() -> List[float]:
    """Benchmark: 40% Investment-grade bond fund, 60% Global equity index fund."""
    return [0.0, 0.0, 0.40, 0.60]


def get_equal_weights(n: int) -> List[float]:
    """Equal weight: 1 / n per sleeve."""
    return [1.0 / n] * n


def get_inverse_volatility_weights(sleeves: List[Dict[str, Any]]) -> List[float]:
    """Inverse volatility: each weight = (1 / vol) scaled to sum to 1.0."""
    inv_vols = [1.0 / s["volatility"] for s in sleeves]
    total_inv = sum(inv_vols)
    return [iv / total_inv for iv in inv_vols]


def evaluate_portfolio(name: str, weights: List[float], sleeves: List[Dict[str, Any]], cov: List[List[float]], objective: float) -> Dict[str, Any]:
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


def format_weights(weights: List[float]) -> str:
    """Format weights as 'bills / 10-year / IG / equity' in percent to one decimal."""
    return " / ".join(f"{w * 100.0:.1f}" for w in weights)


def print_portfolio_evaluation(result: Dict[str, Any]) -> None:
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
# LAB 15 EXTENSIONS (Optimization Search & Historical Estimation)
# ==============================================================================

def generate_weight_grid(n: int, step: int = 5):
    """
    Generate all long-only portfolio weight vectors in step-point increments summing to 100%.
    Default step=5 yields 0.00, 0.05, 0.10, ..., 1.00.
    """
    total_steps = 100 // step

    def helper(dim: int, rem: int):
        if dim == 1:
            yield (rem,)
            return
        for val in range(0, rem + 1):
            for rest in helper(dim - 1, rem - val):
                yield (val,) + rest

    for w_tuple in helper(n, total_steps):
        yield [x * (step / 100.0) for x in w_tuple]


def search_lowest_risk_mix(
    sleeves: List[Dict[str, Any]],
    cov: List[List[float]],
    objective: float = 0.065,
    reserve_min: float = 0.030,
    step: int = 5,
) -> Optional[Dict[str, Any]]:
    """
    Searches every long-only mix of the assets in 5-point steps.
    Filters mixes whose expected return is >= objective and reserve-eligible weight >= reserve_min.
    Returns the mix with the lowest volatility, or None if no mix meets the objective.
    """
    best_weights: Optional[List[float]] = None
    best_volatility = float("inf")
    best_return = 0.0
    best_reserve = 0.0
    n = len(sleeves)

    for weights in generate_weight_grid(n, step=step):
        ret = compute_expected_return(weights, sleeves)
        reserve = compute_reserve_weight(weights, sleeves)

        # Check hard mandate feasibility constraints
        if ret >= (objective - 1e-9) and reserve >= (reserve_min - 1e-9):
            vol = compute_portfolio_volatility(weights, cov)
            if vol < best_volatility - 1e-9:
                best_volatility = vol
                best_weights = weights
                best_return = ret
                best_reserve = reserve

    if best_weights is None:
        return None

    return {
        "weights": best_weights,
        "return": best_return,
        "volatility": best_volatility,
        "reserve": best_reserve,
        "meets_objective": True,
    }


def estimate_from_prices(
    filepath_or_file: Union[str, Any],
    last_36: bool = False,
) -> Tuple[List[str], List[Dict[str, Any]], List[List[float]], int]:
    """
    Estimate annualized expected return (mean * 12), volatility (sample std * sqrt(12)),
    and correlation matrix from a CSV of monthly prices.
    CSV format: date first, oldest first, one column per ticker.
    Supports either a filesystem path (str) or a file-like object (StringIO / UploadedFile).
    """
    if isinstance(filepath_or_file, str):
        with open(filepath_or_file, "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f if line.strip()]
    else:
        # File-like object (Streamlit file uploader)
        raw_content = filepath_or_file.read()
        if isinstance(raw_content, bytes):
            text = raw_content.decode("utf-8")
        else:
            text = str(raw_content)
        lines = [line.strip() for line in text.splitlines() if line.strip()]

    reader = csv.reader(lines)
    header = next(reader)
    tickers = [t.strip() for t in header[1:]]
    num_assets = len(tickers)

    rows = []
    for r in reader:
        if not r or len(r) < num_assets + 1:
            continue
        date_str = r[0].strip()
        prices = [float(val) for val in r[1:]]
        rows.append((date_str, prices))

    if len(rows) < 2:
        raise ValueError("Prices CSV must contain at least 2 monthly price observations to calculate returns.")

    # Calculate simple monthly returns: R_t = (P_t - P_{t-1}) / P_{t-1}
    monthly_returns: List[List[float]] = [[] for _ in range(num_assets)]
    for t in range(1, len(rows)):
        prev_p = rows[t - 1][1]
        curr_p = rows[t][1]
        for i in range(num_assets):
            ret = (curr_p[i] - prev_p[i]) / prev_p[i]
            monthly_returns[i].append(ret)

    num_obs = len(monthly_returns[0])
    if last_36:
        if num_obs >= 36:
            monthly_returns = [m_ret[-36:] for m_ret in monthly_returns]
            num_obs = 36
        else:
            raise ValueError(f"Requested last 36 months, but file contains only {num_obs} monthly returns.")

    # Annualize: Mean * 12, Sample Std * sqrt(12)
    means: List[float] = []
    stds: List[float] = []
    sleeves: List[Dict[str, Any]] = []

    # Known reserve-eligible sovereign proxies
    sovereign_cash_or_bonds = {"BIL", "IEF", "SHV", "GOVT", "VGSH", "SGOV", "Treasury bills", "Treasury 10-year note"}

    for i in range(num_assets):
        rets = monthly_returns[i]
        m = sum(rets) / num_obs
        var = sum((x - m) ** 2 for x in rets) / (num_obs - 1)
        s = math.sqrt(var)
        ann_mean = m * 12.0
        ann_std = s * math.sqrt(12.0)
        means.append(ann_mean)
        stds.append(ann_std)

        is_reserve = tickers[i] in sovereign_cash_or_bonds
        sleeves.append({
            "name": tickers[i],
            "return": ann_mean,
            "volatility": ann_std,
            "reserve_eligible": is_reserve,
        })

    # Correlation Matrix
    corr = [[0.0] * num_assets for _ in range(num_assets)]
    for i in range(num_assets):
        corr[i][i] = 1.0
        m_i = sum(monthly_returns[i]) / num_obs
        s_i = stds[i] / math.sqrt(12.0)
        for j in range(i + 1, num_assets):
            m_j = sum(monthly_returns[j]) / num_obs
            s_j = stds[j] / math.sqrt(12.0)
            cov_sample = sum((monthly_returns[i][k] - m_i) * (monthly_returns[j][k] - m_j) for k in range(num_obs)) / (num_obs - 1)
            c = cov_sample / (s_i * s_j)
            corr[i][j] = c
            corr[j][i] = c

    return tickers, sleeves, corr, num_obs


# ==============================================================================
# MAIN EXECUTION (Matches Lab 14 Tuesday Output Exactly)
# ==============================================================================

def main():
    print("=" * 70)
    print("FIN 43900 Lab 15 -- Portfolio Risk & Stability Engine")
    print("Author: Oladapo Olaniyan (oolaniy@purdue.edu)")
    print("Session Token: webapp")
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
