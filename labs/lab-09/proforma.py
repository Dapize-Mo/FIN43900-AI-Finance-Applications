"""FIN 43900 Lab 09 — Pro-Forma Financial Engine and ABG Valuation.

Student Analyst: Oladapo Olaniyan
Teammate / Partner: kogbuef@purdue.edu
Course: FIN 43900 — AI Finance Applications, Purdue University

This script projects five years (2026–2030) of Income Statement, Balance Sheet,
and Cash Flow for Asbury Automotive Group (ABG) using documented assumptions.
"""

from __future__ import annotations


def assert_balanced(year: int, assets: float, liabilities_and_equity: float, threshold: float = 1e-3) -> None:
    """Check balance sheet equation: Assets - (Liabilities + Equity) == 0."""
    gap = assets - liabilities_and_equity
    if abs(gap) > threshold:
        raise ValueError(f"Balance sheet fail in {year}E: Gap = {gap:+.4f} (Assets: {assets:.1f}, Liab+Eq: {liabilities_and_equity:.1f})")


def run_proforma() -> float:
    # Opening Balance Sheet (FY2025 USD Millions)
    prior_rev = 17999.0
    op_inv = 2135.8
    op_ppe = 3070.4
    op_other_assets = 6371.6
    op_cash = 40.4
    op_fp = 2027.0
    op_debt = 3572.0
    op_revolver = 0.0
    op_other_liab = 2127.5
    op_eq = 3891.7

    # History Ratios & Parameters
    dep_ratio = 82.4 / 3070.4
    inv_ratio = 2135.8 / (17999.0 - 3071.7)
    fp_ratio = 2027.0 / 2135.8

    # Assumption Set
    growth = 0.018
    gross_margin = 0.1705
    sga_ratios = [0.665, 0.655, 0.645, 0.645, 0.645]
    impairment = 120.0
    capex = 250.0
    tax_rate = 0.255
    min_cash = 25.0
    repayment = 150.0
    buyback = 150.0
    r_fp = 0.0467
    r_debt = 0.0544
    r_rev = 0.0600
    ke = 0.10
    g_term = 0.025
    shares = 17.951349

    years = [2026, 2027, 2028, 2029, 2030]
    
    rev_hist, ebit_hist, ni_hist, fcfe_hist, cash_hist = [], [], [], [], []

    print("=" * 80)
    print("FIN 43900 Lab 09 — Asbury Automotive Group (ABG) 3-Statement Pro-Forma Model")
    print("Analyst: Oladapo Olaniyan | Teammate: kogbuef@purdue.edu")
    print("=" * 80)
    print(f"{'Metric / Year':<25} {'2026E':>10} {'2027E':>10} {'2028E':>10} {'2029E':>10} {'2030E':>10}")
    print("-" * 80)

    fcfes = []

    for i, y in enumerate(years):
        # 1. Income Statement Order
        rev = prior_rev * (1 + growth)
        gp = rev * gross_margin
        cogs = rev - gp
        sga = gp * sga_ratios[i]
        dep = op_ppe * dep_ratio
        ebit = gp - sga - dep - impairment
        interest = op_fp * r_fp + op_debt * r_debt + op_revolver * r_rev
        pretax = ebit - interest
        tax = max(0.0, pretax) * tax_rate
        ni = pretax - tax

        # 2. Balance Sheet except Cash
        inv = cogs * inv_ratio
        fp = inv * fp_ratio
        ppe = op_ppe + capex - dep
        delta_rev = rev - prior_rev
        delta_wc = 0.008 * delta_rev
        other_assets = op_other_assets + delta_wc - impairment
        debt = op_debt - repayment
        other_liab = op_other_liab
        eq = op_eq + ni - buyback

        # Working Capital Changes
        delta_inv = inv - op_inv
        delta_fp = fp - op_fp

        # 3. Free Cash Flow to Equity (FCFE)
        fcfe = ni + dep + impairment - capex - delta_inv - delta_wc + delta_fp - repayment
        fcfes.append(fcfe)

        # 4. Cash & Revolver Balancing
        uncapped_cash = op_cash + fcfe - buyback
        if uncapped_cash < min_cash:
            rev_needed = min_cash - uncapped_cash
            revolver = op_revolver + rev_needed
            cash = min_cash
        elif op_revolver > 0 and uncapped_cash > min_cash:
            repay = min(op_revolver, uncapped_cash - min_cash)
            revolver = op_revolver - repay
            cash = uncapped_cash - repay
        else:
            revolver = 0.0
            cash = uncapped_cash

        # 5. Balance Check
        assets = cash + inv + ppe + other_assets
        liab_eq = fp + debt + revolver + other_liab + eq
        assert_balanced(y, assets, liab_eq)

        # Store for display
        rev_hist.append(rev)
        ebit_hist.append(ebit)
        ni_hist.append(ni)
        fcfe_hist.append(fcfe)
        cash_hist.append(cash)

        # Advance opening balance sheet to next year
        prior_rev = rev
        op_inv, op_ppe, op_other_assets, op_cash = inv, ppe, other_assets, cash
        op_fp, op_debt, op_revolver, op_other_liab, op_eq = fp, debt, revolver, other_liab, eq

    # Print Summary Tables
    print(f"{'Revenue':<25} {rev_hist[0]:>10.1f} {rev_hist[1]:>10.1f} {rev_hist[2]:>10.1f} {rev_hist[3]:>10.1f} {rev_hist[4]:>10.1f}")
    print(f"{'Operating Income (EBIT)':<25} {ebit_hist[0]:>10.1f} {ebit_hist[1]:>10.1f} {ebit_hist[2]:>10.1f} {ebit_hist[3]:>10.1f} {ebit_hist[4]:>10.1f}")
    print(f"{'Net Income':<25} {ni_hist[0]:>10.1f} {ni_hist[1]:>10.1f} {ni_hist[2]:>10.1f} {ni_hist[3]:>10.1f} {ni_hist[4]:>10.1f}")
    print(f"{'Free Cash Flow (FCFE)':<25} {fcfe_hist[0]:>10.1f} {fcfe_hist[1]:>10.1f} {fcfe_hist[2]:>10.1f} {fcfe_hist[3]:>10.1f} {fcfe_hist[4]:>10.1f}")
    print(f"{'Cash (Year End)':<25} {cash_hist[0]:>10.1f} {cash_hist[1]:>10.1f} {cash_hist[2]:>10.1f} {cash_hist[3]:>10.1f} {cash_hist[4]:>10.1f}")
    print(f"{'Assets - Liab - Equity':<25} {0.0:>10.1f} {0.0:>10.1f} {0.0:>10.1f} {0.0:>10.1f} {0.0:>10.1f}")
    print("-" * 80)

    # 6. Valuation
    pv_fcfe = sum(fcfes[t] / ((1 + ke) ** (t + 1)) for t in range(5))
    tv = (fcfes[-1] + repayment) * (1 + g_term) / (ke - g_term)
    pv_tv = tv / ((1 + ke) ** 5)
    total_equity_val = pv_fcfe + pv_tv
    val_per_share = total_equity_val / shares
    tv_share = (pv_tv / total_equity_val) * 100

    print("\n--- VALUATION SUMMARY ---")
    print(f"PV of 5-Year FCFE:        ${pv_fcfe:.2f}M")
    print(f"Terminal Value (TV):      ${tv:.2f}M  (PV: ${pv_tv:.2f}M)")
    print(f"Total Equity Value:       ${total_equity_val:.2f}M")
    print(f"Shares Outstanding:       {shares:.6f}M")
    print(f"Value per Share:          ${val_per_share:.2f} (Target Known Answer: $291.75)")
    print(f"Terminal Value Share:     {tv_share:.1f}%")
    print("=" * 80)

    return val_per_share


if __name__ == "__main__":
    run_proforma()
