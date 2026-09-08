"""FIN 43900 Lab 06 — Sensitivity, Reverse DCF, and Conditional Recommendation.

Target Company: PepsiCo, Inc. (NASDAQ: PEP | CIK: 0000077476)
Author: Oladapo Olaniyan
Teammate: kogbuef@purdue.edu

One file, one command: python dcf.py prints:
1. The twelve lines matching the known answer
2. The sensitivity grid (with invalid cells marked for g >= WACC)
3. The reverse DCF solved shift via bisection search
Both the training case and the target company (PepsiCo) are executed.
"""

from __future__ import annotations
import numpy as np


# ==============================================================================
# CONFIGURABLE INPUTS BLOCK
# ==============================================================================

# Target Company: PepsiCo, Inc. (PEP)
PEP_INPUTS = {
    "starting_fcff": 9688.59,  # Normalized Core FY2024 unlevered FCFF (USD millions)
    "growth_rates": [0.030, 0.035, 0.040, 0.035, 0.030],  # 5-year forecast path
    "wacc": 0.070,             # 7.00% cost of capital estimate
    "terminal_growth": 0.025,  # 2.50% long-run GDP-capped terminal growth
    "cash": 8505.0,            # Non-operating cash & equivalents ($M)
    "debt": 44306.0,           # Total debt obligations ($M)
    "shares": 1378.0,          # Diluted common shares (millions)
    "target_price": 143.21,    # Nasdaq close on Feb 4, 2025 earnings release
    "wacc_grid": [0.060, 0.070, 0.080],
    "g_grid": [0.020, 0.025, 0.030],
}

# Training Case (Official Course Known-Answer Benchmark)
TRAINING_INPUTS = {
    "starting_fcff": 100.0,
    "growth_rates": [0.08, 0.06, 0.05, 0.04, 0.03],
    "wacc": 0.10,
    "terminal_growth": 0.03,
    "cash": 50.0,
    "debt": 300.0,
    "shares": 50.0,
    "target_price": 30.00,
    "wacc_grid": [0.09, 0.10, 0.11],
    "g_grid": [0.02, 0.03, 0.04],
}

# Bisection search parameters
LOWER_BOUND = -0.05  # -5 percentage points
UPPER_BOUND = 0.10   # +10 percentage points


# ==============================================================================
# CORE VALUATION & SENSITIVITY FUNCTIONS
# ==============================================================================

def run_dcf(inputs: dict, growth_shift: float = 0.0, override_wacc: float = None, override_g: float = None) -> dict:
    wacc = override_wacc if override_wacc is not None else inputs["wacc"]
    terminal_growth = override_g if override_g is not None else inputs["terminal_growth"]
    starting_fcff = inputs["starting_fcff"]
    base_growths = inputs["growth_rates"]
    cash = inputs["cash"]
    debt = inputs["debt"]
    shares = inputs["shares"]

    # 1. Five explicit years
    fcff_list = []
    pv_explicit = 0.0
    cur_fcff = starting_fcff
    for year_idx, base_g in enumerate(base_growths, start=1):
        shifted_g = base_g + growth_shift
        if shifted_g <= -1.0:
            raise ValueError(f"Growth rate in Year {year_idx} is -100% or below.")
        cur_fcff *= (1.0 + shifted_g)
        fcff_list.append(cur_fcff)
        pv_explicit += cur_fcff / ((1.0 + wacc) ** year_idx)

    # 2. Terminal Value
    if terminal_growth >= wacc:
        tv = np.nan
        pv_tv = np.nan
        ev = np.nan
        equity = np.nan
        per_share = np.nan
        tv_share = np.nan
    else:
        tv = (fcff_list[-1] * (1.0 + terminal_growth)) / (wacc - terminal_growth)
        pv_tv = tv / ((1.0 + wacc) ** 5)
        ev = pv_explicit + pv_tv
        equity = ev + cash - debt
        per_share = equity / shares
        tv_share = pv_tv / ev if ev > 0 else np.nan

    res = {
        "fcff_year_1": fcff_list[0],
        "fcff_year_2": fcff_list[1],
        "fcff_year_3": fcff_list[2],
        "fcff_year_4": fcff_list[3],
        "fcff_year_5": fcff_list[4],
        "pv_explicit_fcff": pv_explicit,
        "terminal_value_year_5": tv,
        "pv_terminal_value": pv_tv,
        "enterprise_value": ev,
        "common_equity_value": equity,
        "value_per_diluted_share": per_share,
        "terminal_value_share": tv_share,
    }
    return res


def print_twelve_lines(results: dict, label: str = ""):
    print(f"\nTwelve Standard Valuation Lines {label}:")
    print(f"  fcff_year_1:              {results['fcff_year_1']:,.6f}")
    print(f"  fcff_year_2:              {results['fcff_year_2']:,.6f}")
    print(f"  fcff_year_3:              {results['fcff_year_3']:,.6f}")
    print(f"  fcff_year_4:              {results['fcff_year_4']:,.6f}")
    print(f"  fcff_year_5:              {results['fcff_year_5']:,.6f}")
    print(f"  pv_explicit_fcff:         {results['pv_explicit_fcff']:,.6f}")
    print(f"  terminal_value_year_5:    {results['terminal_value_year_5']:,.6f}")
    print(f"  pv_terminal_value:        {results['pv_terminal_value']:,.6f}")
    print(f"  enterprise_value:         {results['enterprise_value']:,.6f}")
    print(f"  common_equity_value:      {results['common_equity_value']:,.6f}")
    print(f"  value_per_diluted_share:  {results['value_per_diluted_share']:,.6f}")
    print(f"  terminal_value_share:     {results['terminal_value_share']:,.6f}")


def generate_sensitivity_grid(inputs: dict) -> None:
    wacc_list = inputs["wacc_grid"]
    g_list = inputs["g_grid"]

    print("\nSensitivity Grid — Value per Diluted Share ($):")
    header = "WACC \\ g".ljust(12) + "".join(f"{g*100:.1f}%".rjust(12) for g in g_list)
    print(header)
    print("-" * len(header))

    for w in wacc_list:
        row_str = f"{w*100:.1f}%".ljust(12)
        for g in g_list:
            if g >= w:
                row_str += "INVALID".rjust(12)
            else:
                res = run_dcf(inputs, growth_shift=0.0, override_wacc=w, override_g=g)
                ps = res["value_per_diluted_share"]
                row_str += f"${ps:.2f}".rjust(12)
        print(row_str)


def run_reverse_dcf(inputs: dict, lower: float, upper: float) -> None:
    target = inputs["target_price"]
    wacc = inputs["wacc"]
    g = inputs["terminal_growth"]
    cash = inputs["cash"]
    debt = inputs["debt"]
    shares = inputs["shares"]

    # Boundary check for annual growth rates
    for idx, bg in enumerate(inputs["growth_rates"], start=1):
        if bg + lower <= -1.0:
            raise ValueError(f"Lower bound pushes Year {idx} growth below -100%")

    def get_price(shift: float) -> float:
        res = run_dcf(inputs, growth_shift=shift)
        return res["value_per_diluted_share"]

    p_low = get_price(lower)
    p_high = get_price(upper)

    print("\nReverse DCF:")
    print(f"  Target share price:         ${target:.2f}")
    print(f"  Inputs held fixed:          WACC={wacc*100:.2f}%, g={g*100:.2f}%, Cash=${cash:,.1f}M, Debt=${debt:,.1f}M, Shares={shares:,.1f}M")
    print(f"  Search bounds:              [{lower*100:+.1f} points, {upper*100:+.1f} points] -> reachable prices [${p_low:.2f}, ${p_high:.2f}]")

    if not (p_low <= target <= p_high or p_high <= target <= p_low):
        print(f"  Result:                     No solution in bracket [{lower*100:+.1f}%, {upper*100:+.1f}%]. Target price ${target:.2f} is outside reachable range.")
        return

    # Bisection
    low, high = lower, upper
    for _ in range(100):
        mid = (low + high) / 2.0
        p_mid = get_price(mid)
        if p_mid < target:
            low = mid
        else:
            high = mid

    shift_points = mid * 100.0
    print(f"  Solved uniform growth shift:{shift_points:+.2f} percentage points ({mid:+.4f})")
    print(f"  Solved per-share value:     ${get_price(mid):.2f}")
    print(f"  Implied 5-year growth path: {[round((gr + mid)*100, 2) for gr in inputs['growth_rates']]}%")


# ==============================================================================
# MAIN EXECUTION ROUTINE
# ==============================================================================

def main():
    print("=" * 80)
    print("FIN 43900 LAB 06 — DCF ENGINE, SENSITIVITY GRID & REVERSE DCF")
    print("Author: Oladapo Olaniyan | Teammate: kogbuef@purdue.edu")
    print("=" * 80)

    # 1. Official Training Case Check
    print("\n>>> BLOCK 1: TRAINING-CASE VERIFICATION (KNOWN ANSWER)")
    train_res = run_dcf(TRAINING_INPUTS)
    print_twelve_lines(train_res, "(Training Case)")
    generate_sensitivity_grid(TRAINING_INPUTS)
    run_reverse_dcf(TRAINING_INPUTS, lower=LOWER_BOUND, upper=UPPER_BOUND)

    # 2. PepsiCo Target Company Run
    print("\n" + "=" * 80)
    print(">>> BLOCK 2: PEPSICO, INC. (PEP) — TARGET COMPANY VALUATION")
    pep_res = run_dcf(PEP_INPUTS)
    print_twelve_lines(pep_res, "(PepsiCo, Inc. - Base Case)")
    generate_sensitivity_grid(PEP_INPUTS)
    run_reverse_dcf(PEP_INPUTS, lower=LOWER_BOUND, upper=UPPER_BOUND)

    print("\n" + "=" * 80)
    print("REASONABLENESS & CONDITIONAL CALL SUMMARY (PEP):")
    price = PEP_INPUTS["target_price"]
    val = pep_res["value_per_diluted_share"]
    ratio = val / price
    print(f"  Observed Market Price:      ${price:.2f} (Feb 4, 2025 Nasdaq Close)")
    print(f"  Model Fair Value per Share: ${val:.2f}")
    print(f"  Valuation Ratio (Val/Price):{ratio:.2f}x (Inside 0.5x–2.0x band: {'YES' if 0.5 <= ratio <= 2.0 else 'NO'})")
    print("  Conditional Call:           Watch-defer. Initiate if the price demands less growth than our forecast")
    print("                              (price below ~$125.00), or if FLNA prints two consecutive quarters of")
    print("                              positive organic volume growth without margin degradation.")
    print("                              Monitor: Frito-Lay North America quarterly organic volume in next 10-Q.")
    print("=" * 80)


if __name__ == "__main__":
    main()
