"""
FIN 43900 — AI Finance Applications
Lab 16: Provenance Gate (Point-in-Time As-Of Filter)

Author: Oladapo Olaniyan (oolaniy@purdue.edu)
Teammate / Learning Partner: J. Maffei (maffeij@purdue.edu | Target Company: Oracle Corp. — ORCL)
Date: October 27, 2026
Session: Week 10, Tuesday Completion Checkout (25 Points)

Standard Library Only:
Builds a point-in-time filter and proves on the known answer what was
historically knowable on the decision date versus what is visible in a naive backtest.
"""

import sys

# ==============================================================================
# EDITABLE INPUTS (Top of Script)
# ==============================================================================

# Default decision date: rows published after this date are unknowable
DEFAULT_DECISION_DATE = "2026-03-31"

# Fictional card-spend index for three retailers (AAA, BBB, CCC)
TRAINING_TABLE = [
    {"row": 1,  "ticker": "AAA", "month_measured": "2026-01", "published_on": "2026-02-10", "index": 101.0},
    {"row": 2,  "ticker": "AAA", "month_measured": "2026-02", "published_on": "2026-03-10", "index": 104.0},
    {"row": 3,  "ticker": "AAA", "month_measured": "2026-03", "published_on": "2026-04-10", "index": 109.0},
    {"row": 4,  "ticker": "AAA", "month_measured": "2026-02", "published_on": "2026-03-25", "index": 103.0},
    {"row": 5,  "ticker": "BBB", "month_measured": "2026-01", "published_on": "2026-02-10", "index": 98.0},
    {"row": 6,  "ticker": "BBB", "month_measured": "2026-02", "published_on": "2026-03-10", "index": 97.0},
    {"row": 7,  "ticker": "BBB", "month_measured": "2026-02", "published_on": "2026-03-10", "index": 97.0},
    {"row": 8,  "ticker": "BBB", "month_measured": "2026-03", "published_on": "2026-04-10", "index": 92.0},
    {"row": 9,  "ticker": "CCC", "month_measured": "2026-01", "published_on": "2026-02-10", "index": 110.0},
    {"row": 10, "ticker": "CCC", "month_measured": "2026-02", "published_on": "2026-04-05", "index": 112.0},
    {"row": 11, "ticker": "",    "month_measured": "2026-02", "published_on": "2026-03-10", "index": 99.0},
    {"row": 12, "ticker": "CCC", "month_measured": "2026-02", "published_on": "2026-03-10", "index": 111.0},
]

MONTH_NAMES = {
    "01": "January",
    "02": "February",
    "03": "March",
    "04": "April",
    "05": "May",
    "06": "June",
    "07": "July",
    "08": "August",
    "09": "September",
    "10": "October",
    "11": "November",
    "12": "December",
}

# ==============================================================================
# POINT-IN-TIME FILTER IMPLEMENTATION
# ==============================================================================

def apply_provenance_filter(data, decision_date=None):
    """
    Applies the four course rules in exact sequence:
      1. Quarantine a row with no ticker.
      2. Remove exact duplicates (same ticker, month, published date, and index).
      3. Remove rows published strictly after the decision date.
      4. Where one ticker and month has multiple publications, keep the latest
         one published on or before the decision date (revision tracking).

    Returns:
      panel: list of surviving row dicts.
      funnel: dict recording removed row numbers per step.
    """
    # -------------------------------------------------------------------------
    # RULE 1: Quarantine rows with no ticker
    # -------------------------------------------------------------------------
    r1_removed = []
    after_r1 = []
    for r in data:
        ticker = r["ticker"].strip() if r["ticker"] else ""
        if not ticker:
            r1_removed.append(r["row"])
        else:
            after_r1.append(r)

    # -------------------------------------------------------------------------
    # RULE 2: Remove exact duplicates
    # -------------------------------------------------------------------------
    r2_removed = []
    after_r2 = []
    seen_exact = set()
    for r in after_r1:
        key = (r["ticker"], r["month_measured"], r["published_on"], r["index"])
        if key in seen_exact:
            r2_removed.append(r["row"])
        else:
            seen_exact.add(key)
            after_r2.append(r)

    # -------------------------------------------------------------------------
    # RULE 3: Remove rows published after the decision date
    # -------------------------------------------------------------------------
    r3_removed = []
    after_r3 = []
    for r in after_r2:
        if decision_date is not None and r["published_on"] > decision_date:
            r3_removed.append(r["row"])
        else:
            after_r3.append(r)

    # -------------------------------------------------------------------------
    # RULE 4: For each (ticker, month), keep the latest published row
    # -------------------------------------------------------------------------
    groups = {}
    for r in after_r3:
        key = (r["ticker"], r["month_measured"])
        if key not in groups:
            groups[key] = []
        groups[key].append(r)

    r4_removed = []
    after_r4 = []
    for key, rows in groups.items():
        if len(rows) == 1:
            after_r4.append(rows[0])
        else:
            # Sort ascending by published_on date, using row number as tie-breaker
            sorted_vintages = sorted(rows, key=lambda x: (x["published_on"], x["row"]))
            latest_vintage = sorted_vintages[-1]
            for older_vintage in sorted_vintages[:-1]:
                r4_removed.append(older_vintage["row"])
            after_r4.append(latest_vintage)

    # Sort final panel by original row ID
    after_r4.sort(key=lambda x: x["row"])

    funnel = {
        "Quarantined: no ticker": r1_removed,
        "Exact duplicate": r2_removed,
        "Published after decision date": r3_removed,
        "Older vintage replaced by a revision": r4_removed,
        "As-of panel": [r["row"] for r in after_r4],
    }
    return after_r4, funnel


def compute_signals(panel, reference_asof_panel=None, is_naive=False):
    """
    Computes percent change from the previous month to the latest knowable month:
      signal = (latest_index / prev_index - 1) * 100

    Labels month by full name and tags revisions where naive uses a post-decision vintage.
    """
    tickers = sorted(list(set(r["ticker"] for r in panel)))
    signals = {}

    # Map as-of latest observations if reference panel provided
    ref_latest = {}
    if reference_asof_panel is not None:
        for t in tickers:
            t_rows = sorted([r for r in reference_asof_panel if r["ticker"] == t],
                            key=lambda x: x["month_measured"])
            if t_rows:
                ref_latest[t] = t_rows[-1]

    for t in tickers:
        t_rows = sorted([r for r in panel if r["ticker"] == t],
                        key=lambda x: x["month_measured"])
        if len(t_rows) < 2:
            signals[t] = {
                "error": "Insufficient history (less than 2 months available)",
                "pct_change": None,
                "display": "N/A",
            }
            continue

        prev_row = t_rows[-2]
        latest_row = t_rows[-1]

        pct_change = ((latest_row["index"] / prev_row["index"]) - 1.0) * 100.0
        m_num = latest_row["month_measured"].split("-")[1]
        m_name = MONTH_NAMES.get(m_num, latest_row["month_measured"])

        # Determine if this observation reflects a revision over what was knowable as-of
        note = m_name
        if is_naive and t in ref_latest:
            ref = ref_latest[t]
            if (latest_row["month_measured"] == ref["month_measured"] and
                    latest_row["row"] != ref["row"]):
                note = f"{m_name}, revised"

        sign = "+" if pct_change > 0 else ""
        signals[t] = {
            "ticker": t,
            "prev_row": prev_row["row"],
            "prev_month": prev_row["month_measured"],
            "prev_index": prev_row["index"],
            "latest_row": latest_row["row"],
            "latest_month": latest_row["month_measured"],
            "latest_index": latest_row["index"],
            "pct_change": pct_change,
            "month_label": note,
            "display": f"{sign}{pct_change:.2f}% ({note})",
        }

    return signals


# ==============================================================================
# REPORTING AND FORMATTING
# ==============================================================================

def print_provenance_report(decision_date=DEFAULT_DECISION_DATE, show_naive=True):
    print("=" * 80)
    print("FIN 43900 LAB 16: PROVENANCE GATE - POINT-IN-TIME AS-OF FILTER")
    print(f"Student: Oladapo Olaniyan | Partner: J. Maffei | Date: October 27, 2026")
    print(f"Active Decision Date: {decision_date}")
    print("=" * 80)

    # 1. As-Of Funnel & Panel
    asof_panel, asof_funnel = apply_provenance_filter(TRAINING_TABLE, decision_date=decision_date)

    print("\n1. THE ROW FUNNEL")
    print("-" * 80)
    print(f"{'Funnel Step':<40} | {'Count':<5} | {'Row Numbers'}")
    print("-" * 80)
    for step, rows in asof_funnel.items():
        if step == "As-of panel":
            continue
        print(f"{step:<40} | {len(rows):<5} | {rows}")
    print("-" * 80)
    print(f"{'As-of panel (surviving rows)':<40} | {len(asof_funnel['As-of panel']):<5} | {asof_funnel['As-of panel']}")
    print("-" * 80)

    print("\n2. AS-OF PANEL (HISTORICALLY KNOWABLE RECORDS)")
    print("-" * 80)
    print(f"{'Row':>3} | {'Ticker':<6} | {'Month':<7} | {'Published':<10} | {'Index':>7} | {'Observation Notes'}")
    print("-" * 80)
    for r in asof_panel:
        note = "Initial release"
        if r["row"] == 4:
            note = "Revision (superseded Row 2 on 2026-03-25)"
        elif r["row"] == 12:
            note = "Initial release (post-date revision Row 10 dropped)"
        print(f"{r['row']:>3} | {r['ticker']:<6} | {r['month_measured']:<7} | {r['published_on']:<10} | {r['index']:>7.2f} | {note}")
    print("-" * 80)

    # 2. Signals
    asof_signals = compute_signals(asof_panel, is_naive=False)

    if show_naive:
        naive_panel, naive_funnel = apply_provenance_filter(TRAINING_TABLE, decision_date=None)
        naive_signals = compute_signals(naive_panel, reference_asof_panel=asof_panel, is_naive=True)

        print("\n3. SIGNAL COMPARISON: AS-OF (KNOWABLE) vs. NAIVE (LOOK-AHEAD LEAK)")
        print("-" * 80)
        print(f"{'Ticker':<6} | {'As-of Signal':<22} | {'Naive Signal':<26} | {'Leak (Naive - As-of)'}")
        print("-" * 80)
        for t in asof_signals:
            asof_disp = asof_signals[t]["display"]
            naive_disp = naive_signals[t]["display"]
            leak = naive_signals[t]["pct_change"] - asof_signals[t]["pct_change"]
            leak_sign = "+" if leak > 0 else ""
            print(f"{t:<6} | {asof_disp:<22} | {naive_disp:<26} | {leak_sign}{leak:.2f} percentage points")
        print("-" * 80)

    return asof_panel, asof_signals


# ==============================================================================
# MAIN ENTRY POINT
# ==============================================================================

if __name__ == "__main__":
    # Allow passing an alternative decision date via command line (e.g., 2026-04-15 for break test)
    active_date = DEFAULT_DECISION_DATE
    if len(sys.argv) > 1:
        if sys.argv[1] in ("--break", "break", "swap"):
            active_date = "2026-04-15"
        else:
            active_date = sys.argv[1]

    print_provenance_report(decision_date=active_date, show_naive=True)
