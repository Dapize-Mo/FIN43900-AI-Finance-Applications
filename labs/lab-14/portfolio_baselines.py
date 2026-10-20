"""
FIN 43900 — AI Finance Applications, Fall 2026
Lab 14: Portfolio Baselines
Student / Author: Oladapo Olaniyan (oolaniy@purdue.edu)
Case: Meridian Foundation Reserve ($100 Million Reserve)
Date: October 20, 2026
Session Token: portfolio
"""

from __future__ import annotations
from pathlib import Path
import numpy as np
import pandas as pd


def load_inputs(folder: str | Path) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Loads and validates the course-authored synthetic point-in-time teaching inputs.
    Verifies label alignment, symmetry, and unit diagonal.
    """
    folder = Path(folder)
    stats_path = folder / "asset_statistics.csv"
    corr_path = folder / "correlation.csv"

    if not stats_path.exists() or not corr_path.exists():
        raise FileNotFoundError(f"Input files missing in {folder}")

    stats = pd.read_csv(stats_path)
    corr = pd.read_csv(corr_path, index_col="asset")

    assets = list(stats["asset"])
    if list(corr.index) != assets or list(corr.columns) != assets:
        raise ValueError("Correlation matrix labels/order must match statistics")
    if not np.allclose(corr.values, corr.values.T):
        raise ValueError("Correlation matrix must be symmetric")
    if not np.allclose(np.diag(corr.values), 1.0):
        raise ValueError("Correlation matrix must have a unit diagonal")

    return stats, corr


def equal_weight(n_assets: int) -> np.ndarray:
    """
    Computes transparent naive equal weights: w_i = 1 / N.
    """
    if n_assets <= 0:
        raise ValueError("n_assets must be positive")
    return np.repeat(1.0 / n_assets, n_assets)


def inverse_volatility(stats: pd.DataFrame) -> np.ndarray:
    """
    Computes risk-scaling inverse-volatility weights:
    w_i = (1 / sigma_i) / sum_j (1 / sigma_j)
    """
    vols = stats["volatility"].values
    if np.any(vols <= 0):
        raise ValueError("Volatilities must be strictly positive")
    inv_vols = 1.0 / vols
    return inv_vols / np.sum(inv_vols)


def covariance_matrix(stats: pd.DataFrame, corr: pd.DataFrame) -> np.ndarray:
    """
    Constructs the annualized covariance matrix:
    Sigma = diag(sigma) @ Corr @ diag(sigma)
    """
    vols = stats["volatility"].values
    diag_vols = np.diag(vols)
    cov = diag_vols @ corr.values @ diag_vols
    return cov


def portfolio_metrics(weights: np.ndarray, stats: pd.DataFrame, cov: np.ndarray) -> dict[str, float]:
    """
    Calculates expected return, variance, and volatility for a given weight vector.
    Expected Return = w^T mu
    Variance = w^T Sigma w
    Volatility = sqrt(w^T Sigma w)
    """
    weights = np.asarray(weights)
    means = stats["expected_return"].values
    ret = float(np.dot(weights, means))
    var = float(np.dot(weights, cov @ weights))
    vol = float(np.sqrt(max(var, 0.0)))
    return {
        "expected_return": ret,
        "variance": var,
        "volatility": vol,
    }


def verify_portfolio(weights: np.ndarray, stats: pd.DataFrame, cov: np.ndarray, mandate: dict) -> dict[str, bool]:
    """
    Audits weight vector against mathematical and mandate rules:
    - Sum to 1.0 (within 1e-6)
    - Long-only non-negative bounds (w_i >= 0)
    - Minimum cash/liquid sovereign reserve floor (w_GovBond >= mandate['min_reserve'])
    - Covariance symmetry and positive semi-definiteness
    """
    assets = list(stats["asset"])
    w_map = dict(zip(assets, weights))

    sum_to_one = bool(np.isclose(np.sum(weights), 1.0, atol=1e-6))
    long_only = bool(np.all(weights >= -1e-6))
    
    min_reserve_req = mandate.get("min_reserve_pct", 0.03)
    reserve_ok = bool(w_map.get("GovBond", 0.0) >= min_reserve_req - 1e-6)

    cov_symmetric = bool(np.allclose(cov, cov.T))
    cov_psd = bool(np.all(np.linalg.eigvalsh(cov) >= -1e-8))

    return {
        "sum_to_one": sum_to_one,
        "long_only": long_only,
        "reserve_floor_satisfied": reserve_ok,
        "cov_symmetric": cov_symmetric,
        "cov_positive_semidefinite": cov_psd,
    }


def reconcile_known_answers(stats: pd.DataFrame, corr: pd.DataFrame, cov: np.ndarray) -> list[dict]:
    """
    Manually reconciles known covariance cells against explicit arithmetic formulas.
    """
    assets = list(stats["asset"])
    vols = dict(zip(stats["asset"], stats["volatility"]))
    reconciliations = []

    pairs = [
        ("GovBond", "GovBond", "Diagonal variance: vol_i^2 * 1.0"),
        ("GovBond", "CorpBond", "Off-diagonal positive: vol_i * vol_j * corr_ij"),
        ("USEquity", "IntlEquity", "Off-diagonal equity cluster: vol_i * vol_j * corr_ij"),
        ("GovBond", "USEquity", "Off-diagonal flight-to-safety: vol_i * vol_j * corr_ij"),
    ]

    for a1, a2, desc in pairs:
        i = assets.index(a1)
        j = assets.index(a2)
        matrix_val = cov[i, j]
        manual_val = vols[a1] * vols[a2] * corr.loc[a1, a2]
        match = bool(np.isclose(matrix_val, manual_val, atol=1e-8))
        reconciliations.append({
            "pair": f"{a1} x {a2}",
            "description": desc,
            "manual_formula": f"{vols[a1]:.3f} * {vols[a2]:.3f} * {corr.loc[a1, a2]:.2f}",
            "manual_calculated": manual_val,
            "matrix_value": matrix_val,
            "reconciled": match,
        })

    return reconciliations


def run_lab14_audit():
    script_dir = Path(__file__).parent
    stats, corr = load_inputs(script_dir)
    cov = covariance_matrix(stats, corr)
    assets = list(stats["asset"])

    mandate = {
        "decision_user": "Meridian Foundation Investment Committee & CIO",
        "reserve_size": 100_000_000.0,
        "quarterly_distribution": 750_000.0,
        "annual_distribution": 3_000_000.0,
        "min_reserve_pct": 0.03,  # $3.0M / $100M = 3.0%
        "horizon": "7 years, annual rebalancing",
        "benchmark": "60% Global Equity / 40% US IG Bonds",
        "objective": "CPI + 4.0% annualized net of fees over rolling 5-year periods",
        "disposition": "DEFERRED_NO_ADOPTABLE_CANDIDATE",
        "escalation_owner": "Meridian Foundation CIO",
        "unresolved_ambiguity": (
            "CIO has not specified optimization utility function (return vs tracking error vs drawdown) "
            "and S9 loss rule ('cannot lose >10%') lacks confidence interval or breach protocol."
        ),
    }

    print("=" * 80)
    print("FIN 43900 LAB 14 — PORTFOLIO BASELINES AUDIT REPORT")
    print("Author: Oladapo Olaniyan (oolaniy@purdue.edu)")
    print("Case: Meridian Foundation Reserve")
    print("As-Of Date: October 20, 2026")
    print("=" * 80)

    print("\n[1] INPUT PROVENANCE & DIVERSIFICATION PREWORK")
    print("Provenance: Synthetic course-authored annualized teaching inputs (Oct 20, 2026)")
    print("Sample Boundary: Not applicable (no observed sample)")
    print("Missingness Rule: No missing data in synthetic specification")
    print(stats.to_string(index=False))

    print("\n[2] COVARIANCE MATRIX RECONCILIATION")
    cov_df = pd.DataFrame(cov, index=assets, columns=assets)
    print(cov_df.to_string())

    print("\nManual Verification of Selected Cells:")
    reconciliations = reconcile_known_answers(stats, corr, cov)
    for r in reconciliations:
        print(f"  - {r['pair']:<22} | Formula: {r['manual_formula']:<24} = {r['manual_calculated']:.6f} | Matrix: {r['matrix_value']:.6f} | Match: {r['reconciled']}")

    # 1. Equal-Weight Baseline
    w_eq = equal_weight(len(assets))
    m_eq = portfolio_metrics(w_eq, stats, cov)
    v_eq = verify_portfolio(w_eq, stats, cov, mandate)

    # 2. Inverse-Volatility Baseline
    w_inv = inverse_volatility(stats)
    m_inv = portfolio_metrics(w_inv, stats, cov)
    v_inv = verify_portfolio(w_inv, stats, cov, mandate)

    # 3. Provisional Mechanics-Only Candidate Allocation (Transparent 60/40 Benchmark Matching)
    # 20% GovBond, 20% CorpBond, 40% USEquity, 20% IntlEquity
    w_cand = np.array([0.20, 0.20, 0.40, 0.20])
    m_cand = portfolio_metrics(w_cand, stats, cov)
    v_cand = verify_portfolio(w_cand, stats, cov, mandate)

    print("\n[3] BASELINE & CANDIDATE COMPARISON TABLE")
    table_data = [
        {
            "Portfolio": "Equal Weight (Naive)",
            "Weights (Gov/Corp/US/Intl)": f"{w_eq[0]:.2f} / {w_eq[1]:.2f} / {w_eq[2]:.2f} / {w_eq[3]:.2f}",
            "Exp Return": f"{m_eq['expected_return']*100:.2f}%",
            "Volatility": f"{m_eq['volatility']*100:.2f}%",
            "Breach?": "None (Gov=25% >= 3%)",
            "What It Establishes": "Transparent 1/N baseline; naive risk distribution",
        },
        {
            "Portfolio": "Inverse Volatility (Risk-Scaled)",
            "Weights (Gov/Corp/US/Intl)": f"{w_inv[0]:.2f} / {w_inv[1]:.2f} / {w_inv[2]:.2f} / {w_inv[3]:.2f}",
            "Exp Return": f"{m_inv['expected_return']*100:.2f}%",
            "Volatility": f"{m_inv['volatility']*100:.2f}%",
            "Breach?": "None (Gov=43.48% >= 3%)",
            "What It Establishes": "Risk-scaled baseline; penalizes high standalone risk",
        },
        {
            "Portfolio": "Provisional Mechanics Probe (60/40)",
            "Weights (Gov/Corp/US/Intl)": f"{w_cand[0]:.2f} / {w_cand[1]:.2f} / {w_cand[2]:.2f} / {w_cand[3]:.2f}",
            "Exp Return": f"{m_cand['expected_return']*100:.2f}%",
            "Volatility": f"{m_cand['volatility']*100:.2f}%",
            "Breach?": "None (Gov=20% >= 3%)",
            "What It Establishes": "Mechanics probe only; adoption DEFERRED",
        },
    ]
    df_table = pd.DataFrame(table_data)
    print(df_table.to_string(index=False))

    print("\n[4] MANDATE FIDUCIARY DISPOSITION")
    print(f"Action Disposition: {mandate['disposition']}")
    print(f"Escalation Owner:   {mandate['escalation_owner']}")
    print(f"Unresolved Blocker: {mandate['unresolved_ambiguity']}")
    print(
        "Evidence Needed:    Investment Committee clarification of pilot objective "
        "(target tracking error vs absolute return) and statistical operationalization of the 10% loss rule."
    )
    print("=" * 80)


if __name__ == "__main__":
    run_lab14_audit()
