"""FIN 43900 Week 3 Lab 05 — Build and Validate an FCFF DCF Engine

Student Analyst: Oladapo Olaniyan
Teammate: kogbuef@purdue.edu
Course: FIN 43900 — AI Finance Applications, Purdue University
Date: September 8, 2026
"""

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
    fcff_list = []
    current_fcff = inputs["starting_fcff"]
    for year in range(1, 6):
        growth = inputs[f"growth_year_{year}"]
        current_fcff = current_fcff * (1.0 + growth)
        fcff_list.append(current_fcff)
    return fcff_list


def value_dcf(inputs: dict[str, float], projected_fcff: list[float]) -> dict[str, float]:
    wacc = inputs["wacc"]
    g = inputs["terminal_growth"]
    
    if g >= wacc:
        raise ValueError(f"Invalid parameters: terminal growth ({g:.4f}) >= WACC ({wacc:.4f})")

    pv_fcff_list = [cf / ((1.0 + wacc) ** t) for t, cf in enumerate(projected_fcff, start=1)]
    pv_explicit_fcff = sum(pv_fcff_list)

    fcff_5 = projected_fcff[4]
    terminal_value_year_5 = (fcff_5 * (1.0 + g)) / (wacc - g)
    pv_terminal_value = terminal_value_year_5 / ((1.0 + wacc) ** 5)

    enterprise_value = pv_explicit_fcff + pv_terminal_value
    common_equity_value = enterprise_value + inputs["nonoperating_cash"] - inputs["debt"]
    value_per_diluted_share = common_equity_value / inputs["diluted_shares"]
    terminal_value_share = pv_terminal_value / enterprise_value

    return {
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


if __name__ == "__main__":
    main()
