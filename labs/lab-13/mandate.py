"""Editable mandate checker for FIN 43900 Lab 13.

Student: Oladapo Olaniyan
Case: fictional Meridian Foundation Reserve
Uses only Python's standard library. This is a rule checker, not an optimizer.
"""
from collections import defaultdict
from copy import deepcopy
import sys

RESERVE_VALUE_MILLIONS = 100.0
QUARTERLY_PAYOUT_MILLIONS = 0.75
PAYOUT_QUARTERS = 4
LIQUIDITY_DAYS = 5
LIQUIDITY_MINIMUM_PCT = 90.0
ISSUER_LIMIT_PCT = 8.0
ALLOCATION_TARGET_PCT = 100.0

# Edit these case inputs to explore different candidates. issuer_exempt reflects
# the prompt's exemptions for cash, U.S. Treasuries, and diversified funds.
HOLDINGS = {
    "Cash": {"issuer": None, "days": 0, "reserve_eligible": True, "issuer_exempt": True},
    "Treasury bills": {"issuer": "U.S. Treasury", "days": 1, "reserve_eligible": True, "issuer_exempt": True},
    "Treasury 10-year note": {"issuer": "U.S. Treasury", "days": 1, "reserve_eligible": True, "issuer_exempt": True},
    "Global equity index fund": {"issuer": "Diversified fund", "days": 2, "reserve_eligible": False, "issuer_exempt": True},
    "Investment-grade bond fund": {"issuer": "Diversified fund", "days": 3, "reserve_eligible": False, "issuer_exempt": True},
    "Private real estate fund": {"issuer": "Diversified fund", "days": 90, "reserve_eligible": False, "issuer_exempt": True},
    "Acme Corp bonds": {"issuer": "Acme Corp", "days": 4, "reserve_eligible": False, "issuer_exempt": False},
    "Acme Corp stock": {"issuer": "Acme Corp", "days": 1, "reserve_eligible": False, "issuer_exempt": False},
}

CANDIDATES = {
    "A": {"Cash": 2, "Treasury bills": 2, "Treasury 10-year note": 10,
          "Global equity index fund": 60, "Investment-grade bond fund": 26,
          "Private real estate fund": 0, "Acme Corp bonds": 0, "Acme Corp stock": 0},
    "B": {"Cash": 1, "Treasury bills": 0, "Treasury 10-year note": 0,
          "Global equity index fund": 55, "Investment-grade bond fund": 20,
          "Private real estate fund": 15, "Acme Corp bonds": 5, "Acme Corp stock": 4},
    "C": {"Cash": 1, "Treasury bills": 1, "Treasury 10-year note": 0,
          "Global equity index fund": 70, "Investment-grade bond fund": 20,
          "Private real estate fund": 0, "Acme Corp bonds": 0, "Acme Corp stock": 8},
    "D": {"Cash": 4, "Treasury bills": 0, "Treasury 10-year note": 0,
          "Global equity index fund": 96, "Investment-grade bond fund": 0,
          "Private real estate fund": 0, "Acme Corp bonds": 0, "Acme Corp stock": 0},
}


def check_candidate(weights):
    """Compute metrics and pass/fail flags solely from holding metadata and weights."""
    complete_weights = {name: float(weights.get(name, 0.0)) for name in HOLDINGS}
    total = sum(complete_weights.values())
    minimum = min(complete_weights.values())
    reserve = sum(complete_weights[name] for name, h in HOLDINGS.items() if h["reserve_eligible"])
    liquid = sum(complete_weights[name] for name, h in HOLDINGS.items() if h["days"] <= LIQUIDITY_DAYS)
    issuer_weights = defaultdict(float)
    for name, h in HOLDINGS.items():
        if h["issuer"] and not h["issuer_exempt"]:
            issuer_weights[h["issuer"]] += complete_weights[name]
    largest_issuer = max(issuer_weights.values(), default=0.0)
    reserve_minimum = PAYOUT_QUARTERS * QUARTERLY_PAYOUT_MILLIONS / RESERVE_VALUE_MILLIONS * 100.0
    checks = {
        "allocation": abs(total - ALLOCATION_TARGET_PCT) < 1e-9,
        "long_only": minimum >= 0.0,
        "reserve_floor": reserve >= reserve_minimum,
        "liquidity": liquid >= LIQUIDITY_MINIMUM_PCT,
        "issuer_cap": largest_issuer <= ISSUER_LIMIT_PCT,
    }
    return {"total": total, "minimum": minimum, "reserve": reserve,
            "reserve_minimum": reserve_minimum, "liquid": liquid,
            "largest_issuer": largest_issuer, "checks": checks}


def print_candidate(label, weights):
    result = check_candidate(weights)
    print(f"Candidate {label}")
    print(f"  Allocation: {result['total']:.1f}% ({'pass' if result['checks']['allocation'] else 'FAIL'})")
    print(f"  Lowest holding weight: {result['minimum']:.1f}% ({'pass' if result['checks']['long_only'] else 'FAIL'})")
    print(f"  Reserve eligible: {result['reserve']:.1f}% / {result['reserve_minimum']:.1f}% minimum ({'pass' if result['checks']['reserve_floor'] else 'FAIL'})")
    print(f"  Redeemable within {LIQUIDITY_DAYS} business days: {result['liquid']:.1f}% / {LIQUIDITY_MINIMUM_PCT:.1f}% minimum ({'pass' if result['checks']['liquidity'] else 'FAIL'})")
    print(f"  Largest non-exempt single-company weight: {result['largest_issuer']:.1f}% / {ISSUER_LIMIT_PCT:.1f}% maximum ({'pass' if result['checks']['issuer_cap'] else 'FAIL'})")
    failures = sum(not passed for passed in result["checks"].values())
    print(f"  Calendar-year loss: requires CIO clarification")
    print(f"  Verdict: {'passes every checkable rule' if failures == 0 else f'fails {failures} rule(s)'}")
    return result


def main():
    reserve_minimum = PAYOUT_QUARTERS * QUARTERLY_PAYOUT_MILLIONS / RESERVE_VALUE_MILLIONS * 100.0
    print(f"Reserve floor: {PAYOUT_QUARTERS} x ${QUARTERLY_PAYOUT_MILLIONS:.2f}m / ${RESERVE_VALUE_MILLIONS:.1f}m = {reserve_minimum:.1f}%")
    if "--negative-probe" in sys.argv:
        probe = deepcopy(CANDIDATES["A"])
        probe["Cash"] = -2
        probe["Global equity index fund"] += 4
        print_candidate("A negative-weight probe", probe)
        print("Original Candidate A inputs restored (temporary probe copy was used).")
        return
    for name, weights in CANDIDATES.items():
        print_candidate(name, weights)
        print()


if __name__ == "__main__":
    main()
    main()



