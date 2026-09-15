"""FIN 43900 Lab 08: Deal Evidence and Valuation Triangulation.

Student Analyst: Oladapo Olaniyan
Teammate: kogbuef@purdue.edu
Target: PepsiCo, Inc. (PEP)

This module:
1. Reconciles synthetic precedent-transaction implied value ($17.40/sh).
2. Runs the PepsiCo Valuation Triangulation Engine across DCF, Trading Comps, and Deal Evidence.
3. Conducts a changed-normalization test (Reported vs. Normalized EBITDA).
4. Evaluates committee action boundaries (Watch-Defer condition & trigger).
"""

from __future__ import annotations

from pathlib import Path
import pandas as pd


def verify_synthetic_precedent() -> float:
    """Reproduce synthetic precedent transaction implied value ($17.40 per share)."""
    # Training case target inputs
    target = {
        "ebitda": 80.0,
        "cash": 50.0,
        "debt": 300.0,
        "diluted_shares": 50.0,
        "precedent_ev_to_ebitda": 14.0,
    }
    
    ev = target["precedent_ev_to_ebitda"] * target["ebitda"]  # 14.0 * 80 = 1120.0
    equity_val = ev + target["cash"] - target["debt"]         # 1120 + 50 - 300 = 870.0
    per_share = equity_val / target["diluted_shares"]          # 870 / 50 = $17.40
    return round(per_share, 4)


def run_pepsico_triangulation() -> dict[str, float]:
    """Run full valuation triangulation for PepsiCo, Inc. (PEP)."""
    # Core Denominators for PepsiCo (FY2024 10-K)
    pep = {
        "reported_ebitda": 16500.0,     # $M reported EBITDA
        "normalized_ebitda": 18311.0,   # $M core normalized EBITDA (excl $1,811M charges)
        "net_income": 9100.0,           # $M net income
        "cash": 8505.0,                 # $M cash & equivalents
        "debt": 44306.0,                # $M total debt
        "diluted_shares": 1378.0,       # M diluted shares
        "market_price": 143.21,         # $ Market closing price (Feb 4, 2025)
    }

    # 1. Method 1: DCF Model (Lab 06 Base Case)
    dcf_base_per_share = 140.73
    dcf_bear_per_share = 101.07
    dcf_bull_per_share = 219.87

    # 2. Method 2: Trading Comparables (Lab 07 Clean Peer Set)
    clean_pe_mult = 20.91        # Median P/E of KO, KDP, MDLZ
    clean_ev_mult = 16.20        # Median EV/EBITDA of KO, KDP, MDLZ
    
    trading_pe_per_share = (clean_pe_mult * pep["net_income"]) / pep["diluted_shares"]
    trading_ev_per_share = (clean_ev_mult * pep["reported_ebitda"] + pep["cash"] - pep["debt"]) / pep["diluted_shares"]

    # 3. Method 3: Precedent Deal Evidence (Sector Transaction Precedent: Mars / Kellanova 16.4x EV/EBITDA)
    deal_ev_mult = 16.40
    deal_ev_per_share = (deal_ev_mult * pep["reported_ebitda"] + pep["cash"] - pep["debt"]) / pep["diluted_shares"]

    # 4. Changed-Normalization Robustness Test: Normalized EBITDA ($18,311M)
    normalized_trading_ev = (clean_ev_mult * pep["normalized_ebitda"] + pep["cash"] - pep["debt"]) / pep["diluted_shares"]
    normalized_deal_ev = (deal_ev_mult * pep["normalized_ebitda"] + pep["cash"] - pep["debt"]) / pep["diluted_shares"]

    return {
        "dcf_base": dcf_base_per_share,
        "dcf_bear": dcf_bear_per_share,
        "dcf_bull": dcf_bull_per_share,
        "trading_pe": round(trading_pe_per_share, 2),
        "trading_ev": round(trading_ev_per_share, 2),
        "deal_ev": round(deal_ev_per_share, 2),
        "norm_trading_ev": round(normalized_trading_ev, 2),
        "norm_deal_ev": round(normalized_deal_ev, 2),
        "norm_shift_trading": round(normalized_trading_ev - trading_ev_per_share, 2),
        "norm_shift_deal": round(normalized_deal_ev - deal_ev_per_share, 2),
        "market_price": pep["market_price"],
    }


def main() -> None:
    # 1. Synthetic Checkpoint Check
    syn_val = verify_synthetic_precedent()
    print("=== SYNTHETIC PRECEDENT TRANSACTION CHECKPOINT ===")
    print(f"Calculated Precedent Per Share: ${syn_val:.4f} (Expected: $17.4000) [{'PASSED' if syn_val == 17.40 else 'FAILED'}]\n")

    # 2. PepsiCo Triangulation Engine
    res = run_pepsico_triangulation()
    print("=== PEPSICO (PEP) VALUATION TRIANGULATION TABLE ===")
    print(f"  Current Market Price (Feb 4, 2025) : ${res['market_price']:.2f}")
    print(f"  Method 1 — FCFF DCF Base Case      : ${res['dcf_base']:.2f} per share (Range: ${res['dcf_bear']:.2f} - ${res['dcf_bull']:.2f})")
    print(f"  Method 2 — Trading Comps P/E       : ${res['trading_pe']:.2f} per share (20.91x clean median)")
    print(f"  Method 3 — Trading Comps EV/EBITDA : ${res['trading_ev']:.2f} per share (16.20x clean median)")
    print(f"  Method 4 — Precedent Deal EV/EBITDA: ${res['deal_ev']:.2f} per share (16.40x Kellanova/Mars)")
    print(f"\n=== CHANGED-NORMALIZATION ROBUSTNESS TEST ===")
    print(f"  Reported EBITDA ($16,500M) EV Comps Value  : ${res['trading_ev']:.2f}/share")
    print(f"  Normalized EBITDA ($18,311M) EV Comps Value: ${res['norm_trading_ev']:.2f}/share")
    print(f"  EBITDA Normalization Shift                  : +${res['norm_shift_trading']:.2f}/share (+12.7%)")
    print(f"  Normalized Precedent Deal Value             : ${res['norm_deal_ev']:.2f}/share")


if __name__ == "__main__":
    main()
