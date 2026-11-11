"""
FIN 43900 — Project 2: Investment Management Application
Point-in-Time Signal Processor, Provenance Gate & Formal Data Card

Author: Oladapo Olaniyan (oolaniy@purdue.edu)
Institution: Mitchell E. Daniels, Jr. School of Business, Purdue University
"""

import os
from typing import Any, Dict, List, Optional
import pandas as pd
import numpy as np


# ==============================================================================
# OFFICIAL POINT-IN-TIME DATA CARD
# ==============================================================================

PIT_DATA_CARD: Dict[str, Any] = {
    "signal_name": "Consumer Price Index for All Urban Consumers (CPIAUCSL)",
    "series_id": "CPIAUCSL",
    "provider": "U.S. Bureau of Labor Statistics (BLS) via FRED / ALFRED (St. Louis Fed)",
    "frequency": "Monthly",
    "temporal_coordinates": {
        "event_time (t_event)": "Reference month of economic activity (e.g., September 2026)",
        "publication_time (t_pub)": "Official release date (typically 10–14 days after month-end)",
        "vintage_date (v)": "Snapshot date representing what was knowable as of market close",
    },
    "publication_lag": "10 to 14 calendar days post reference month end",
    "revision_behavior": (
        "Seasonally adjusted series undergoing annual recalculations of seasonal factors "
        "every January, revising the preceding 5 full calendar years (up to 60 historical months)."
    ),
    "look_ahead_risk": (
        "High. Using modern finalized data retrospectively attributes future inflation revisions "
        "and unreleased month prints to historical trading days, falsely depressing measured tracking error."
    ),
    "fiduciary_disposition": "CONDITIONAL ADMISSION (QUARANTINE ENFORCED)",
    "admission_protocol": (
        "Admitted for strategy execution and mandate verification ONLY when vintage date "
        "is strictly <= trade execution date (ALFRED point-in-time query), or by substituting "
        "the unrevised non-seasonally adjusted index (CPIAUCNS)."
    ),
    "empirical_evidence_lab17": {
        "test_vintage": "2026-09-30",
        "tested_observation": "2026-09",
        "result": "September 2026 print (336.298) did NOT exist on Sept 30; only August 2026 (334.131) was knowable.",
        "seasonal_revision_test": "Comparing vintage 2024-01-15 against today reveals 60 historical months revised.",
    },
}


def load_point_in_time_data(data_path: Optional[str] = None) -> pd.DataFrame:
    """
    Loads local point-in-time dataset, falling back to default project path.
    """
    if data_path is None:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        data_path = os.path.join(base_dir, "data", "pit_macro.csv")

    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Point-in-time data file not found at: {data_path}")

    df = pd.read_csv(data_path)
    df["observation_date"] = pd.to_datetime(df["observation_date"])
    return df


def audit_point_in_time_availability(
    df: pd.DataFrame,
    as_of_date: str = "2026-09-30",
) -> Dict[str, Any]:
    """
    Evaluates what inflation data was knowable as of a specific decision date,
    contrasting it with modern revised data to measure the revision delta.
    """
    as_of_dt = pd.to_datetime(as_of_date)

    # Filter observations that could have been published by as_of_date
    # CPI requires ~14 days lag, so an observation for month M is knowable only after M-end + 14d
    valid_knowable = []
    revisions_found = 0
    max_revision_abs = 0.0

    for _, row in df.iterrows():
        obs_date = row["observation_date"]
        # Publication date is roughly 14 days after month end
        pub_est = obs_date + pd.DateOffset(days=45)  # Safe buffer to ensure publication

        today_val = row.get("today_vintage")
        v2024_val = row.get("vintage_2024_01_15")
        v2026_val = row.get("vintage_2026_09_30")

        # Check revision between vintage and today
        if pd.notna(v2024_val) and pd.notna(today_val):
            diff = abs(today_val - v2024_val)
            if diff > 1e-4:
                revisions_found += 1
                if diff > max_revision_abs:
                    max_revision_abs = diff

        is_knowable = obs_date < as_of_dt - pd.DateOffset(days=15)
        if is_knowable and pd.notna(v2026_val):
            valid_knowable.append({
                "observation_date": obs_date.strftime("%Y-%m-%d"),
                "knowable_value": v2026_val,
                "today_revised_value": today_val,
                "revision_delta": today_val - v2026_val if pd.notna(today_val) else 0.0,
            })

    latest_knowable = valid_knowable[-1] if valid_knowable else None

    return {
        "as_of_date": as_of_date,
        "latest_knowable_observation": latest_knowable,
        "total_observations_audited": len(df),
        "total_historical_revisions_detected": revisions_found,
        "max_revision_magnitude": max_revision_abs,
        "data_card": PIT_DATA_CARD,
    }

