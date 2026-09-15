"""FIN 43900 Lab 07: Comparable-Company Policy and Implied Range.

Student Analyst: Oladapo Olaniyan
Teammate: kogbuef@purdue.edu
Target: PepsiCo, Inc. (PEP)

This module:
1. Reconciles synthetic known answers for Week 4 starter case.
2. Computes peer multiples, medians, enterprise-to-equity bridges.
3. Applies student peer policy to PepsiCo (PEP) and real market peers (KO, KDP, MDLZ, KHC).
4. Conducts borderline peer inclusion/qualification robustness test.
"""

from __future__ import annotations

from pathlib import Path
import pandas as pd


def load_cases(folder: Path) -> tuple[pd.DataFrame, dict[str, float], dict[str, float]]:
    peers = pd.read_csv(folder / "peer_case.csv")
    target_table = pd.read_csv(folder / "target_case.csv")
    expected_table = pd.read_csv(folder / "expected_output.csv")
    target = target_table.set_index("metric")["value"].astype(float).to_dict()
    expected = expected_table.set_index("output")["expected_value"].astype(float).to_dict()
    return peers, target, expected


def calculate_peer_multiples(peers: pd.DataFrame) -> pd.DataFrame:
    """Calculate consistent enterprise (EV/EBITDA) and equity (P/E) multiples."""
    df = peers.copy()
    df["ev_to_ebitda"] = df["enterprise_value"] / df["ebitda"]
    df["price_to_earnings"] = df["equity_value"] / df["net_income"]
    return df


def implied_target_values(
    peer_multiples: pd.DataFrame, target: dict[str, float]
) -> dict[str, float]:
    """Calculate median trading and precedent implied per-share values."""
    med_ev_ebitda = float(peer_multiples["ev_to_ebitda"].median())
    med_pe = float(peer_multiples["price_to_earnings"].median())

    # EV/EBITDA is Enterprise Multiple -> Needs Bridge (EV -> Equity Value -> Per Share)
    trading_ev = med_ev_ebitda * target["ebitda"]
    trading_eq_from_ev = trading_ev + target["cash"] - target["debt"]
    trading_ev_per_share = trading_eq_from_ev / target["diluted_shares"]

    # P/E is Equity Multiple -> Direct to Equity Value (NO BRIDGE)
    trading_eq_from_pe = med_pe * target["net_income"]
    trading_pe_per_share = trading_eq_from_pe / target["diluted_shares"]

    # Precedent Transaction (EV Multiple) -> Needs Bridge
    precedent_ev_mult = target.get("precedent_ev_to_ebitda", 14.0)
    precedent_ev = precedent_ev_mult * target["ebitda"]
    precedent_eq = precedent_ev + target["cash"] - target["debt"]
    precedent_per_share = precedent_eq / target["diluted_shares"]

    return {
        "median_ev_to_ebitda": med_ev_ebitda,
        "median_price_to_earnings": med_pe,
        "trading_ev_to_ebitda_per_share": round(trading_ev_per_share, 4),
        "trading_price_to_earnings_per_share": round(trading_pe_per_share, 4),
        "precedent_transaction_per_share": round(precedent_per_share, 4),
    }


def run_pepsico_peer_model() -> dict[str, float]:
    """Run real-world peer valuation for PepsiCo, Inc. (PEP)."""
    # Sourced SEC & Market Data for PepsiCo (FY2024 / Q1 2025)
    pep_target = {
        "ebitda": 16500.0,  # $M reported EBITDA
        "net_income": 9100.0,  # $M net income attributable to PEP
        "cash": 8505.0,  # $M cash and cash equivalents
        "debt": 44306.0,  # $M total debt
        "diluted_shares": 1378.0,  # M diluted shares
        "current_market_price": 143.21,
    }

    # Verified Real Peer Set (SEC Form 10-K & Market Cap as of Feb 2025)
    real_peers = pd.DataFrame([
        {
            "company": "The Coca-Cola Company (KO)",
            "ticker": "KO",
            "enterprise_value": 310000.0,
            "ebitda": 14500.0,
            "equity_value": 285000.0,
            "net_income": 10700.0,
            "status": "Core Included",
        },
        {
            "company": "Keurig Dr Pepper Inc. (KDP)",
            "ticker": "KDP",
            "enterprise_value": 58500.0,
            "ebitda": 4100.0,
            "equity_value": 44000.0,
            "net_income": 2250.0,
            "status": "Core Included",
        },
        {
            "company": "Mondelez International, Inc. (MDLZ)",
            "ticker": "MDLZ",
            "enterprise_value": 115000.0,
            "ebitda": 7100.0,
            "equity_value": 92000.0,
            "net_income": 4400.0,
            "status": "Core Included",
        },
        {
            "company": "The Kraft Heinz Company (KHC)",
            "ticker": "KHC",
            "enterprise_value": 56000.0,
            "ebitda": 6400.0,
            "equity_value": 41000.0,
            "net_income": 2850.0,
            "status": "Borderline Peer",
        },
    ])

    # Compute Multiples for All 4 Peers
    peer_mults_full = calculate_peer_multiples(real_peers)
    
    # 1. Full Peer Set Valuations
    med_ev_full = float(peer_mults_full["ev_to_ebitda"].median())
    med_pe_full = float(peer_mults_full["price_to_earnings"].median())

    ev_val_full = (med_ev_full * pep_target["ebitda"] + pep_target["cash"] - pep_target["debt"]) / pep_target["diluted_shares"]
    pe_val_full = (med_pe_full * pep_target["net_income"]) / pep_target["diluted_shares"]

    # 2. Borderline Test: Remove Kraft Heinz (KHC) due to lower organic growth and debt load
    peer_mults_clean = peer_mults_full[peer_mults_full["ticker"] != "KHC"]
    med_ev_clean = float(peer_mults_clean["ev_to_ebitda"].median())
    med_pe_clean = float(peer_mults_clean["price_to_earnings"].median())

    ev_val_clean = (med_ev_clean * pep_target["ebitda"] + pep_target["cash"] - pep_target["debt"]) / pep_target["diluted_shares"]
    pe_val_clean = (med_pe_clean * pep_target["net_income"]) / pep_target["diluted_shares"]

    return {
        "full_med_ev_ebitda": round(med_ev_full, 2),
        "full_med_pe": round(med_pe_full, 2),
        "full_implied_ev_per_share": round(ev_val_full, 2),
        "full_implied_pe_per_share": round(pe_val_full, 2),
        "clean_med_ev_ebitda": round(med_ev_clean, 2),
        "clean_med_pe": round(med_pe_clean, 2),
        "clean_implied_ev_per_share": round(ev_val_clean, 2),
        "clean_implied_pe_per_share": round(pe_val_clean, 2),
        "khc_ev_impact": round(ev_val_clean - ev_val_full, 2),
        "khc_pe_impact": round(pe_val_clean - pe_val_full, 2),
    }


def main() -> None:
    # 1. Reconcile Synthetic Known Answers
    starter_folder = Path(__file__).resolve().parent.parent.parent / "FIN43900-Fall2026-main" / "lessons" / "week-04" / "starter"
    if starter_folder.exists():
        peers, target, expected = load_cases(starter_folder)
        peer_mults = calculate_peer_multiples(peers)
        results = implied_target_values(peer_mults, target)

        print("=== SYNTHETIC CASE CHECKPOINT RECONCILIATION ===")
        all_passed = True
        for key, exp_val in expected.items():
            calc_val = results[key]
            diff = abs(calc_val - exp_val)
            status = "PASSED" if diff < 1e-3 else "FAILED"
            if status == "FAILED":
                all_passed = False
            print(f"  {key:<35}: Calc={calc_val:<8.4f} Exp={exp_val:<8.4f} [{status}]")

        print(f"\nSynthetic Checkpoints Overall Status: {'ALL PASSED' if all_passed else 'CHECK FAILED'}\n")

    # 2. PepsiCo Real Peer Model
    print("=== PEPSICO (PEP) REAL PEER VALUATION & BORDERLINE TEST ===")
    pep_res = run_pepsico_peer_model()
    print(f"Full Peer Set (4 Peers):")
    print(f"  Median EV/EBITDA  : {pep_res['full_med_ev_ebitda']}x -> Implied Value = ${pep_res['full_implied_ev_per_share']}/share")
    print(f"  Median P/E        : {pep_res['full_med_pe']}x -> Implied Value = ${pep_res['full_implied_pe_per_share']}/share")
    print(f"\nClean Peer Set (Excluding Borderline Peer KHC):")
    print(f"  Median EV/EBITDA  : {pep_res['clean_med_ev_ebitda']}x -> Implied Value = ${pep_res['clean_implied_ev_per_share']}/share")
    print(f"  Median P/E        : {pep_res['clean_med_pe']}x -> Implied Value = ${pep_res['clean_implied_pe_per_share']}/share")
    print(f"\nBorderline Peer Removal Impact (Qualifying KHC):")
    print(f"  EV/EBITDA Implied Shift : +${pep_res['khc_ev_impact']}/share")
    print(f"  P/E Implied Shift       : +${pep_res['khc_pe_impact']}/share")


if __name__ == "__main__":
    main()
