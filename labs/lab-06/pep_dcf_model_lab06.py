"""FIN 43900 Lab 06 — Sensitivity, Reverse DCF, and Conditional Recommendation.

Target Company: PepsiCo, Inc. (PEP | CIK: 0000077476)
Author / Student: Oladapo Olaniyan
Teammate: kogbuef@purdue.edu
Filing: SEC Form 10-K for Fiscal Year Ended December 28, 2024

This script implements the required four functions:
1. project_fcff(inputs)
2. value_dcf(inputs, projected_fcff)
3. sensitivity_table(inputs, wacc_values, terminal_growth_values)
4. reverse_dcf_for_growth(inputs, observed_price, lower, upper)

It validates against the official training case (dcf_case.csv / dcf_expected_output.csv),
then executes PepsiCo scenarios (Low, Base, High), WACC/g sensitivity grid,
terminal value concentration, and reverse DCF for market price.
"""

from __future__ import annotations

from pathlib import Path
import pandas as pd
import numpy as np


# ==============================================================================
# CORE DCF ENGINE (STUDENT_WORK IMPLEMENTATIONS)
# ==============================================================================

def validate_case(inputs: dict[str, float]) -> None:
    """Validate boundary conditions: g < WACC, positive shares, positive starting FCFF."""
    if inputs["terminal_growth"] >= inputs["wacc"]:
        raise ValueError("Terminal growth must be strictly less than WACC")
    if inputs["diluted_shares"] <= 0:
        raise ValueError("Diluted shares must be positive")
    if inputs["starting_fcff"] <= 0:
        raise ValueError("Starting FCFF must be positive")
    for year in range(1, 6):
        growth = inputs.get(f"growth_year_{year}", 0.0)
        if growth <= -1.0:
            raise ValueError(f"Year {year} growth cannot be -100% or lower")


def project_fcff(inputs: dict[str, float]) -> list[float]:
    """Sequentially project five annual FCFF values from starting FCFF."""
    projected = []
    current_fcff = float(inputs["starting_fcff"])
    for year in range(1, 6):
        growth_rate = float(inputs[f"growth_year_{year}"])
        current_fcff = current_fcff * (1.0 + growth_rate)
        projected.append(current_fcff)
    return projected


def value_dcf(inputs: dict[str, float], projected_fcff: list[float]) -> dict[str, float]:
    """Discount explicit FCFF, terminal value, and bridge enterprise value to diluted equity."""
    wacc = float(inputs["wacc"])
    terminal_growth = float(inputs["terminal_growth"])
    diluted_shares = float(inputs["diluted_shares"])
    nonoperating_cash = float(inputs.get("nonoperating_cash", 0.0))
    debt = float(inputs.get("debt", 0.0))

    # 1. Present value of explicit 5-year cash flows
    pv_explicit = 0.0
    for t, fcff_t in enumerate(projected_fcff, start=1):
        pv_explicit += fcff_t / ((1.0 + wacc) ** t)

    # 2. Gordon-growth terminal value at end of Year 5
    fcff_5 = projected_fcff[-1]
    if wacc <= terminal_growth:
        terminal_value_year_5 = np.nan
        pv_tv = np.nan
        ev = np.nan
        tv_share = np.nan
        equity_val = np.nan
        per_share = np.nan
    else:
        terminal_value_year_5 = (fcff_5 * (1.0 + terminal_growth)) / (wacc - terminal_growth)
        pv_tv = terminal_value_year_5 / ((1.0 + wacc) ** 5)
        ev = pv_explicit + pv_tv
        tv_share = pv_tv / ev if ev > 0 else np.nan
        equity_val = ev + nonoperating_cash - debt
        per_share = equity_val / diluted_shares

    results = {
        "pv_explicit_fcff": pv_explicit,
        "terminal_value_year_5": terminal_value_year_5,
        "pv_terminal_value": pv_tv,
        "enterprise_value": ev,
        "common_equity_value": equity_val,
        "value_per_diluted_share": per_share,
        "terminal_value_share": tv_share,
    }
    for t, fcff_t in enumerate(projected_fcff, start=1):
        results[f"fcff_year_{t}"] = fcff_t

    return results


def sensitivity_table(
    inputs: dict[str, float], wacc_values: list[float], terminal_growth_values: list[float]
) -> pd.DataFrame:
    """Return per-share values indexed by terminal growth (rows) and WACC (columns).
    
    Blanks (sets NaN) any cell where terminal growth >= WACC.
    """
    projected = project_fcff(inputs)
    table_dict: dict[float, list[float]] = {w: [] for w in wacc_values}

    for g in terminal_growth_values:
        for w in wacc_values:
            if g >= w:
                table_dict[w].append(np.nan)
            else:
                temp_inputs = inputs.copy()
                temp_inputs["wacc"] = w
                temp_inputs["terminal_growth"] = g
                val_dict = value_dcf(temp_inputs, projected)
                table_dict[w].append(val_dict["value_per_diluted_share"])

    df = pd.DataFrame(table_dict, index=terminal_growth_values)
    df.index.name = "Terminal Growth (g)"
    return df


def check_monotonicity(grid: pd.DataFrame) -> tuple[bool, str]:
    """Verify that per-share value strictly falls as WACC increases and rises as g increases."""
    # Check across columns (WACC increasing -> value should decrease)
    for g_idx, row in grid.iterrows():
        valid_row = row.dropna()
        if len(valid_row) > 1:
            diffs = np.diff(valid_row.values)
            if not (diffs < 0).all():
                return False, f"WACC monotonicity failed at g={g_idx}"

    # Check down rows (g increasing -> value should increase)
    for col in grid.columns:
        valid_col = grid[col].dropna()
        if len(valid_col) > 1:
            diffs = np.diff(valid_col.values)
            if not (diffs > 0).all():
                return False, f"Growth monotonicity failed at WACC={col}"

    return True, "Passed: Value strictly decreases with higher WACC and strictly increases with higher g."


def reverse_dcf_for_growth(
    inputs: dict[str, float], observed_price: float, lower: float = -0.10, upper: float = 0.30
) -> float:
    """Solve for constant 5-year FCFF growth rate that matches the observed market price."""
    wacc = float(inputs["wacc"])
    terminal_growth = float(inputs["terminal_growth"])
    diluted_shares = float(inputs["diluted_shares"])
    nonoperating_cash = float(inputs.get("nonoperating_cash", 0.0))
    debt = float(inputs.get("debt", 0.0))

    target_equity_value = observed_price * diluted_shares
    target_ev = target_equity_value + debt - nonoperating_cash
    starting_fcff = float(inputs["starting_fcff"])

    def ev_from_cgr(cgr: float) -> float:
        cur = starting_fcff
        pv_exp = 0.0
        for year in range(1, 6):
            cur *= (1.0 + cgr)
            pv_exp += cur / ((1.0 + wacc) ** year)
        tv = (cur * (1.0 + terminal_growth)) / (wacc - terminal_growth)
        pv_tv = tv / ((1.0 + wacc) ** 5)
        return pv_exp + pv_tv

    low = lower
    high = upper
    for _ in range(100):
        mid = (low + high) / 2.0
        ev_mid = ev_from_cgr(mid)
        if ev_mid < target_ev:
            low = mid
        else:
            high = mid

    return mid


# ==============================================================================
# VALIDATION AGAINST TRAINING CASE
# ==============================================================================

def run_synthetic_training_validation() -> bool:
    print("=" * 80)
    print("STEP 1: VALIDATING DCF ENGINE AGAINST SYNTHETIC TRAINING CASE")
    print("=" * 80)

    # Official training case parameters from dcf_case.csv
    synth_inputs = {
        "starting_fcff": 100.0,
        "growth_year_1": 0.08,
        "growth_year_2": 0.06,
        "growth_year_3": 0.05,
        "growth_year_4": 0.04,
        "growth_year_5": 0.03,
        "wacc": 0.10,
        "terminal_growth": 0.03,
        "nonoperating_cash": 50.0,
        "debt": 300.0,
        "diluted_shares": 50.0,
    }

    validate_case(synth_inputs)
    projected = project_fcff(synth_inputs)
    results = value_dcf(synth_inputs, projected)

    # Expected values from dcf_expected_output.csv
    expected = {
        "fcff_year_1": (108.000000, 0.01),
        "fcff_year_2": (114.480000, 0.01),
        "fcff_year_3": (120.204000, 0.01),
        "fcff_year_4": (125.012160, 0.01),
        "fcff_year_5": (128.762525, 0.01),
        "pv_explicit_fcff": (448.440817, 0.01),
        "terminal_value_year_5": (1894.648579, 0.01),
        "pv_terminal_value": (1176.427703, 0.01),
        "enterprise_value": (1624.868520, 0.01),
        "common_equity_value": (1374.868520, 0.01),
        "value_per_diluted_share": (27.497370, 0.01),
        "terminal_value_share": (0.724014, 0.0002),
    }

    all_passed = True
    print(f"{'Metric':<25}{'Model Value':<16}{'Expected':<16}{'Diff':<14}{'Status'}")
    print("-" * 75)
    for key, (exp_val, tol) in expected.items():
        act_val = results[key]
        diff = abs(act_val - exp_val)
        status = "PASSED" if diff <= tol else "FAILED"
        if status == "FAILED":
            all_passed = False
        print(f"{key:<25}{act_val:<16.6f}{exp_val:<16.6f}{diff:<14.6e}{status}")

    print("-" * 75)
    print(f"Overall Synthetic Training Validation: {'ALL TESTS PASSED' if all_passed else 'FAILED'}\n")
    return all_passed


# ==============================================================================
# PEPSICO (PEP) DCF & SENSITIVITY ANALYSIS
# ==============================================================================

def run_pepsico_analysis():
    print("=" * 80)
    print("STEP 2: PEPSICO (PEP) DCF VALUATION & SCENARIO ANALYSIS")
    print("=" * 80)

    # Base financial facts sourced from SEC Form 10-K (FY ended 2024-12-28)
    # Normalized Core FCFF Starting Base = $9,688.59M
    # Cash & non-operating assets = $8,505.0M
    # Total debt = $44,306.0M -> Net debt = $35,801.0M
    # Diluted shares = 1,378.0M shares

    base_inputs = {
        "starting_fcff": 9688.59,
        "growth_year_1": 0.030,
        "growth_year_2": 0.035,
        "growth_year_3": 0.040,
        "growth_year_4": 0.035,
        "growth_year_5": 0.030,
        "wacc": 0.070,
        "terminal_growth": 0.025,
        "nonoperating_cash": 8505.0,
        "debt": 44306.0,
        "diluted_shares": 1378.0,
    }

    # Low (Bear) Case: Persistent volume elasticity wall, pricing resistance, margin compression
    low_inputs = {
        "starting_fcff": 9688.59,
        "growth_year_1": 0.015,
        "growth_year_2": 0.020,
        "growth_year_3": 0.020,
        "growth_year_4": 0.015,
        "growth_year_5": 0.015,
        "wacc": 0.075,
        "terminal_growth": 0.020,
        "nonoperating_cash": 8505.0,
        "debt": 44306.0,
        "diluted_shares": 1378.0,
    }

    # High (Bull) Case: Successful price-pack rebalancing, international acceleration, margin expansion
    high_inputs = {
        "starting_fcff": 9688.59,
        "growth_year_1": 0.050,
        "growth_year_2": 0.050,
        "growth_year_3": 0.045,
        "growth_year_4": 0.040,
        "growth_year_5": 0.035,
        "wacc": 0.065,
        "terminal_growth": 0.025,
        "nonoperating_cash": 8505.0,
        "debt": 44306.0,
        "diluted_shares": 1378.0,
    }

    scenarios = {
        "Low (Bear) Case": low_inputs,
        "Base Case": base_inputs,
        "High (Bull) Case": high_inputs,
    }

    scenario_outputs = {}
    print(f"{'Scenario':<18}{'EV ($M)':<16}{'Equity ($M)':<16}{'Per Share':<14}{'TV Share':<12}")
    print("-" * 75)
    for name, sc_inp in scenarios.items():
        proj = project_fcff(sc_inp)
        res = value_dcf(sc_inp, proj)
        scenario_outputs[name] = res
        print(
            f"{name:<18}${res['enterprise_value']:<15,.1f}${res['common_equity_value']:<15,.1f}"
            f"${res['value_per_diluted_share']:<13.2f}{res['terminal_value_share']:<12.1%}"
        )

    print("\n" + "=" * 80)
    print("STEP 3: WACC & TERMINAL GROWTH SENSITIVITY GRID (BASE OPERATING INPUTS)")
    print("=" * 80)

    wacc_range = [0.060, 0.065, 0.070, 0.075, 0.080]
    g_range = [0.015, 0.020, 0.025, 0.030]

    grid = sensitivity_table(base_inputs, wacc_range, g_range)
    # Format grid for display
    formatted_grid = grid.map(lambda v: f"${v:.2f}" if pd.notnull(v) else "BLANK (g>=WACC)")
    print(formatted_grid)

    mono_passed, mono_msg = check_monotonicity(grid)
    print(f"\nMonotonicity Check: {mono_msg}")

    print("\n" + "=" * 80)
    print("STEP 4: REVERSE DCF (OBSERVED MARKET PRICE)")
    print("=" * 80)

    observed_market_price = 143.21  # Close on Feb 4, 2025 earnings release
    implied_cgr = reverse_dcf_for_growth(base_inputs, observed_market_price)
    print(f"Target Observed Market Price:      ${observed_market_price:.2f} per share")
    print(f"As-of Date & Source:               February 4, 2025 (Nasdaq / SEC Earnings Release)")
    print(f"Solved Implied 5-Year FCFF Growth: {implied_cgr:.2%}")
    print(f"Economic Meaning:                  At WACC=7.0% and g=2.5%, PepsiCo must compound")
    print(f"                                   annual FCFF at {implied_cgr:.2%} per year to justify")
    print(f"                                   its current market price of ${observed_market_price:.2f}.")

    # Save outputs to CSV
    output_dir = Path(__file__).resolve().parent
    grid.to_csv(output_dir / "pep_sensitivity_grid.csv")
    print(f"\nSaved sensitivity grid to: {output_dir / 'pep_sensitivity_grid.csv'}")

    return scenario_outputs, grid, implied_cgr


if __name__ == "__main__":
    run_synthetic_training_validation()
    run_pepsico_analysis()
