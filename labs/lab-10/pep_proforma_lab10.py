"""FIN 43900 Lab 10 — 3-Statement Pro-Forma Model & Valuation for PepsiCo, Inc. (PEP).

Student Analyst: Oladapo Olaniyan
Teammate / Partner: Kenechukwu Ogbuefi (kogbuef@purdue.edu)
Course: FIN 43900 — AI Finance Applications, Purdue University
Company: PepsiCo, Inc. (NASDAQ: PEP | CIK: 0000077476)
Filing Base: SEC Form 10-K for Fiscal Year Ended December 28, 2024

This script projects five years (2025E–2029E) of Income Statement, Balance Sheet,
and Cash Flow for PepsiCo, Inc., enforces zero-gap balance sheet checks in every year,
handles cash/revolver dynamics, and calculates an unforced per-share equity value.
"""

from __future__ import annotations


def assert_balanced(year: int, assets: float, liabilities_and_equity: float, threshold: float = 1e-3) -> None:
    """Check balance sheet equation: Assets - (Liabilities + Equity) == 0."""
    gap = assets - liabilities_and_equity
    if abs(gap) > threshold:
        raise ValueError(
            f"Balance sheet fail in {year}E: Gap = {gap:+.4f} "
            f"(Assets: ${assets:,.1f}M, Liab+Eq: ${liabilities_and_equity:,.1f}M)"
        )


def run_proforma_pep() -> float:
    # -------------------------------------------------------------------------
    # Opening Balance Sheet (FY2024 Actuals in USD Millions, SEC 10-K p. 65)
    # -------------------------------------------------------------------------
    prior_rev = 91854.0         # FY2024 Revenue
    op_cash = 8505.0            # Cash & Cash Equivalents
    op_inv = 5432.0             # Inventories
    op_ppe = 27890.0            # Property, Plant & Equipment (Net)
    op_other_assets = 58197.0   # Other Assets (Current & Non-Current)
    
    op_fp = 0.0                 # Floor Plan Notes Payable (Explicitly $0.0 for CPG company)
    op_st_liab = 28990.0        # Short-Term Debt & Current Liabilities
    op_debt = 36464.0           # Long-Term Debt
    op_revolver = 0.0           # Opening Credit Facility / Revolver Draw
    op_other_liab = 15655.0     # Other Non-Current Liabilities (Deferred taxes $4,858M + Other non-current $10,797M)
    op_eq = 18915.0             # PepsiCo Common Stockholders' Equity

    # Verify Opening Balance Sheet
    op_assets = op_cash + op_inv + op_ppe + op_other_assets
    op_liab_eq = op_fp + op_st_liab + op_debt + op_revolver + op_other_liab + op_eq
    assert_balanced(2024, op_assets, op_liab_eq)

    # -------------------------------------------------------------------------
    # Historical Ratios & Derived Parameters
    # -------------------------------------------------------------------------
    cogs_2024 = prior_rev - 49864.0  # FY2024 Cost of Sales = $41,990.0M
    dep_ratio = 3160.0 / op_ppe      # D&A / PP&E = ~11.33%
    inv_ratio = op_inv / cogs_2024   # Inventory / COGS = ~12.94% (47.2 days)
    fp_ratio = 0.0                   # Floor plan ratio = 0.0

    # -------------------------------------------------------------------------
    # Assumption Set (FY2025E – FY2029E)
    # -------------------------------------------------------------------------
    growth_rates = [0.030, 0.035, 0.040, 0.035, 0.030]  # Volume stabilization + pricing path
    gross_margin = 0.5430                                # 54.30% core gross margin
    sga_ratios = [0.740, 0.735, 0.730, 0.725, 0.720]      # Core SG&A % of Gross Profit (excl 2024 one-offs)
    impairment = 0.0                                     # Normalized going-forward basis
    annual_capex = 5300.0                                # Annual CapEx ($ Millions, ~5.5% rev)
    tax_rate = 0.195                                     # Effective tax rate (19.5%)
    min_cash = 4000.0                                    # Minimum operational cash floor ($M)
    annual_repayment = 1000.0                            # Annual net debt reduction ($M)
    total_shareholder_return = 7500.0                    # Annual Dividends + Buybacks ($M)
    
    r_debt = 0.0480  # Weighted average pre-tax cost of debt (4.80%)
    r_rev = 0.0550   # Revolver interest rate (5.50%)
    ke = 0.0700      # Cost of Equity (7.00% derived from Lab 06 WACC/CAPM)
    g_term = 0.0250  # Perpetual terminal growth rate (2.50%)
    shares = 1378.0  # Diluted common shares outstanding (Millions)

    years = [2025, 2026, 2027, 2028, 2029]

    rev_hist, ebit_hist, ni_hist, fcfe_hist, cash_hist, gap_hist = [], [], [], [], [], []
    fcfes = []

    print("=" * 85)
    print("FIN 43900 Lab 10 — PepsiCo, Inc. (PEP) 3-Statement Pro-Forma Model")
    print("Analyst: Oladapo Olaniyan | Teammate: Kenechukwu Ogbuefi (kogbuef@purdue.edu)")
    print("=" * 85)
    print(f"{'Metric / Year (USD $M)':<25} {'2025E':>10} {'2026E':>10} {'2027E':>10} {'2028E':>10} {'2029E':>10}")
    print("-" * 85)

    for i, y in enumerate(years):
        # 1. Income Statement Projection
        g = growth_rates[i]
        rev = prior_rev * (1 + g)
        gp = rev * gross_margin
        cogs = rev - gp
        sga = gp * sga_ratios[i]
        dep = op_ppe * dep_ratio
        ebit = gp - sga - dep - impairment
        interest = op_debt * r_debt + op_revolver * r_rev
        pretax = ebit - interest
        tax = max(0.0, pretax) * tax_rate
        ni = pretax - tax

        # 2. Balance Sheet Assets & Non-Cash Liabilities
        inv = cogs * inv_ratio
        fp = 0.0
        ppe = op_ppe + annual_capex - dep
        delta_rev = rev - prior_rev
        delta_wc = 0.015 * delta_rev  # Working capital change (~1.5% of incremental revenue)
        other_assets = op_other_assets + delta_wc - impairment
        debt = max(0.0, op_debt - annual_repayment)
        st_liab = op_st_liab
        other_liab = op_other_liab
        eq = op_eq + ni - total_shareholder_return

        # Working Capital Changes
        delta_inv = inv - op_inv

        # 3. Free Cash Flow to Equity (FCFE) Calculation
        fcfe = ni + dep + impairment - annual_capex - delta_inv - delta_wc - annual_repayment
        fcfes.append(fcfe)

        # 4. Cash & Revolver Balancing Logic
        uncapped_cash = op_cash + fcfe - total_shareholder_return
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

        # 5. Balance Sheet Equation Check
        assets = cash + inv + ppe + other_assets
        liab_eq = fp + st_liab + debt + revolver + other_liab + eq
        assert_balanced(y, assets, liab_eq)
        gap = assets - liab_eq

        # Store results for display
        rev_hist.append(rev)
        ebit_hist.append(ebit)
        ni_hist.append(ni)
        fcfe_hist.append(fcfe)
        cash_hist.append(cash)
        gap_hist.append(gap)

        # Advance balance sheet to next period
        prior_rev = rev
        op_inv, op_ppe, op_other_assets, op_cash = inv, ppe, other_assets, cash
        op_fp, op_st_liab, op_debt, op_revolver, op_other_liab, op_eq = (
            fp, st_liab, debt, revolver, other_liab, eq
        )

    # Print Financial Summary Grid
    print(f"{'Revenue':<25} {rev_hist[0]:>10.1f} {rev_hist[1]:>10.1f} {rev_hist[2]:>10.1f} {rev_hist[3]:>10.1f} {rev_hist[4]:>10.1f}")
    print(f"{'Operating Income (EBIT)':<25} {ebit_hist[0]:>10.1f} {ebit_hist[1]:>10.1f} {ebit_hist[2]:>10.1f} {ebit_hist[3]:>10.1f} {ebit_hist[4]:>10.1f}")
    print(f"{'Net Income':<25} {ni_hist[0]:>10.1f} {ni_hist[1]:>10.1f} {ni_hist[2]:>10.1f} {ni_hist[3]:>10.1f} {ni_hist[4]:>10.1f}")
    print(f"{'Free Cash Flow (FCFE)':<25} {fcfe_hist[0]:>10.1f} {fcfe_hist[1]:>10.1f} {fcfe_hist[2]:>10.1f} {fcfe_hist[3]:>10.1f} {fcfe_hist[4]:>10.1f}")
    print(f"{'Cash (Year End)':<25} {cash_hist[0]:>10.1f} {cash_hist[1]:>10.1f} {cash_hist[2]:>10.1f} {cash_hist[3]:>10.1f} {cash_hist[4]:>10.1f}")
    print(f"{'Assets - Liab - Equity':<25} {gap_hist[0]:>10.1f} {gap_hist[1]:>10.1f} {gap_hist[2]:>10.1f} {gap_hist[3]:>10.1f} {gap_hist[4]:>10.1f}")
    print("-" * 85)

    # 6. Discounted Free Cash Flow to Equity (FCFE) Valuation
    pv_fcfe = sum(fcfes[t] / ((1 + ke) ** (t + 1)) for t in range(5))
    terminal_fcfe = fcfes[-1] + annual_repayment
    tv = (terminal_fcfe * (1 + g_term)) / (ke - g_term)
    pv_tv = tv / ((1 + ke) ** 5)
    total_equity_val = pv_fcfe + pv_tv
    val_per_share = total_equity_val / shares
    tv_share = (pv_tv / total_equity_val) * 100.0

    print("\n--- VALUATION SUMMARY (PEPSICO, INC.) ---")
    print(f"PV of 5-Year FCFE:        ${pv_fcfe:,.2f}M")
    print(f"Terminal Value (TV):      ${tv:,.2f}M  (PV: ${pv_tv:,.2f}M)")
    print(f"Total Equity Value:       ${total_equity_val:,.2f}M")
    print(f"Shares Outstanding:       {shares:,.1f}M")
    print(f"Model Value per Share:    ${val_per_share:.2f}")
    print(f"Observed Market Price:    $143.21 (as of Feb 2025)")
    print(f"Valuation Ratio (M/M):    {(val_per_share / 143.21):.2f}x")
    print(f"Terminal Value Share:     {tv_share:.1f}%")
    print("=" * 85)

    return val_per_share


if __name__ == "__main__":
    run_proforma_pep()
