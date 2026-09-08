"""FIN 43900 Week 3 Lab 05 — Build and Validate an FCFF DCF Engine

Student Analyst: Oladapo Olaniyan
Teammate: kogbuef@purdue.edu
Course: FIN 43900 — AI Finance Applications, Purdue University
Date: September 8, 2026

This module implements the 4 required STUDENT_WORK functions for Lab 05:
1. project_fcff
2. value_dcf
3. sensitivity_table
4. reverse_dcf_for_growth
It validates the engine against the official 12 synthetic training checkpoints and executes
the target company transfer for PepsiCo, Inc. (PEP).
"""

from __future__ import annotations

from pathlib import Path
import numpy as np
import pandas as pd


def load_named_values(path: str | Path, name_column: str, value_column: str) -> dict[str, float]:
    table = pd.read_csv(path)
    if name_column not in table or value_column not in table:
        raise ValueError(f"Required columns absent: {name_column}, {value_column}")
    if table[name_column].duplicated().any():
        raise ValueError(f"Duplicate names in {name_column}")
    return table.set_index(name_column)[value_column].astype(float).to_dict()


def validate_case(inputs: dict[str, float]) -> None:
    if inputs["terminal_growth"] >= inputs["wacc"]:
        raise ValueError("Terminal growth must be strictly less than WACC")
    if inputs["diluted_shares"] <= 0:
        raise ValueError("Diluted shares must be positive")
    if inputs["starting_fcff"] <= 0:
        raise ValueError("Training-case starting FCFF must be positive")
    for year in range(1, 6):
        growth = inputs[f"growth_year_{year}"]
        if growth <= -1:
            raise ValueError(f"Year {year} growth cannot be -100% or lower")


def project_fcff(inputs: dict[str, float]) -> list[float]:
    """STUDENT_WORK: sequentially project five annual FCFF values from starting FCFF."""
    fcff_list = []
    current_fcff = inputs["starting_fcff"]
    for year in range(1, 6):
        growth = inputs[f"growth_year_{year}"]
        current_fcff = current_fcff * (1.0 + growth)
        fcff_list.append(current_fcff)
    return fcff_list


def value_dcf(inputs: dict[str, float], projected_fcff: list[float]) -> dict[str, float]:
    """STUDENT_WORK: discount explicit FCFF, terminal value, and the equity bridge."""
    wacc = inputs["wacc"]
    g = inputs["terminal_growth"]
    
    if g >= wacc:
        raise ValueError(f"Invalid parameters: terminal growth ({g:.4f}) >= WACC ({wacc:.4f})")

    # Discount explicit cash flows
    pv_fcff_list = [cf / ((1.0 + wacc) ** t) for t, cf in enumerate(projected_fcff, start=1)]
    pv_explicit_fcff = sum(pv_fcff_list)

    # Gordon Growth Terminal Value at end of Year 5
    fcff_5 = projected_fcff[4]
    terminal_value_year_5 = (fcff_5 * (1.0 + g)) / (wacc - g)
    pv_terminal_value = terminal_value_year_5 / ((1.0 + wacc) ** 5)

    # Enterprise and Equity Bridge
    enterprise_value = pv_explicit_fcff + pv_terminal_value
    common_equity_value = enterprise_value + inputs["nonoperating_cash"] - inputs["debt"]
    value_per_diluted_share = common_equity_value / inputs["diluted_shares"]
    terminal_value_share = pv_terminal_value / enterprise_value

    result = {
        "fcff_year_1": projected_fcff[0],
        "fcff_year_2": projected_fcff[1],
        "fcff_year_3": projected_fcff[2],
        "fcff_year_4": projected_fcff[3],
        "fcff_year_5": projected_fcff[4],
        "pv_explicit_fcff": pv_explicit_fcff,
        "terminal_value_year_5": terminal_value_year_5,
        "pv_terminal_value": pv_terminal_value,
        "enterprise_value": enterprise_value,
        "common_equity_value": common_equity_value,
        "value_per_diluted_share": value_per_diluted_share,
        "terminal_value_share": terminal_value_share,
    }
    return result


def sensitivity_table(
    inputs: dict[str, float], wacc_values: list[float], terminal_growth_values: list[float]
) -> pd.DataFrame:
    """STUDENT_WORK: return per-share values indexed by WACC and terminal growth."""
    grid = pd.DataFrame(index=terminal_growth_values, columns=wacc_values, dtype=float)
    for g in terminal_growth_values:
        for w in wacc_values:
            if g >= w:
                grid.loc[g, w] = np.nan
            else:
                temp_inputs = inputs.copy()
                temp_inputs["wacc"] = w
                temp_inputs["terminal_growth"] = g
                proj = project_fcff(temp_inputs)
                val = value_dcf(temp_inputs, proj)
                grid.loc[g, w] = val["value_per_diluted_share"]
    return grid


def reverse_dcf_for_growth(
    inputs: dict[str, float], observed_price: float, lower: float = -0.05, upper: float = 0.10, tol: float = 1e-6
) -> float:
    """STUDENT_WORK: solve uniform growth rate shift using bisection search."""
    def calc_price(shift: float) -> float:
        temp_inputs = inputs.copy()
        for yr in range(1, 6):
            temp_inputs[f"growth_year_{yr}"] += shift
        proj = project_fcff(temp_inputs)
        val = value_dcf(temp_inputs, proj)
        return val["value_per_diluted_share"]

    f_lower = calc_price(lower) - observed_price
    f_upper = calc_price(upper) - observed_price

    if f_lower * f_upper > 0:
        raise ValueError(f"Root not bracketed between lower={lower} and upper={upper}")

    for _ in range(100):
        mid = (lower + upper) / 2.0
        f_mid = calc_price(mid) - observed_price
        if abs(f_mid) < tol or (upper - lower) / 2.0 < tol:
            return mid
        if f_lower * f_mid < 0:
            upper = mid
            f_upper = f_mid
        else:
            lower = mid
            f_lower = f_mid
    return (lower + upper) / 2.0


def main() -> None:
    folder = Path(__file__).resolve().parent
    inputs = load_named_values(folder / "dcf_case.csv", "input", "value")
    expected_table = pd.read_csv(folder / "dcf_expected_output.csv")
    validate_case(inputs)

    print("================================================================================")
    print("LAB 05: DCF ENGINE VALIDATION (SYNTHETIC KNOWN-ANSWER CASE)")
    print("Analyst: Oladapo Olaniyan | Teammate: kogbuef@purdue.edu")
    print("================================================================================")

    projected = project_fcff(inputs)
    results = value_dcf(inputs, projected)

    all_passed = True
    print(f"{'Metric':<25} {'Model Value':<15} {'Expected':<15} {'Tolerance':<12} {'Status'}")
    print("-" * 75)
    for _, row in expected_table.iterrows():
        metric = row["output"]
        exp_val = row["expected_value"]
        tol = row["tolerance"]
        act_val = results[metric]
        diff = abs(act_val - exp_val)
        passed = diff <= tol
        if not passed:
            all_passed = False
        status_str = "PASSED" if passed else "FAILED"
        print(f"{metric:<25} {act_val:<15.6f} {exp_val:<15.6f} {tol:<12.4f} {status_str}")

    print("-" * 75)
    if all_passed:
        print("SYNTHETIC VALIDATION RESULT: ALL 12 CHECKPOINTS PASSED PERFECTLY!\n")
    else:
        print("SYNTHETIC VALIDATION RESULT: SOME CHECKPOINTS FAILED.\n")

    # PepsiCo Transfer Case
    print("================================================================================")
    print("TARGET COMPANY TRANSFER: PEPSICO, INC. (PEP)")
    print("================================================================================")
    pep_inputs = {
        "starting_fcff": 9688.59,  # Core Normalized FCFF FY2024 ($M)
        "growth_year_1": 0.030,
        "growth_year_2": 0.035,
        "growth_year_3": 0.040,
        "growth_year_4": 0.035,
        "growth_year_5": 0.030,
        "wacc": 0.070,
        "terminal_growth": 0.025,
        "nonoperating_cash": 8505.0,  # Cash & Cash Equivalents ($M)
        "debt": 44306.0,  # Total Debt ($M)
        "diluted_shares": 1378.0,  # Diluted Common Shares (M)
    }

    validate_case(pep_inputs)
    pep_proj = project_fcff(pep_inputs)
    pep_res = value_dcf(pep_inputs, pep_proj)

    print(f"PepsiCo Base Case EV:           ${pep_res['enterprise_value']:,.1f}M")
    print(f"PepsiCo Base Case Equity Value: ${pep_res['common_equity_value']:,.1f}M")
    print(f"PepsiCo Per Diluted Share:      ${pep_res['value_per_diluted_share']:.2f}")
    print(f"PepsiCo TV Share of EV:          {pep_res['terminal_value_share']*100:.1f}%")
    
    target_price = 143.21
    solved_shift = reverse_dcf_for_growth(pep_inputs, target_price)
    print(f"Reverse DCF Shift for ${target_price}: +{solved_shift*100:.2f} percentage points")
    print(f"Implied 5-Year CAGR:            {(0.034 + solved_shift)*100:.2f}% per year")
    print("================================================================================")


if __name__ == "__main__":
    main()
