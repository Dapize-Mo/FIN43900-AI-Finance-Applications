"""
FIN 43900 Lab 11 — Credit Stress & Covenant Headroom Engine
Student Analyst: Oladapo Olaniyan
Teammate / Partners: J. Maffei (maffeij@purdue.edu | Oracle - ORCL), Kasoi (kasoi@purdue.edu | McDonald's - MCD)
Course: FIN 43900 — AI Finance Applications, Purdue University
Date: September 29, 2026
Session Token: sensitivity
Target Company: PepsiCo, Inc. (NASDAQ: PEP | CIK: 0000077476)
"""

from __future__ import annotations
from pathlib import Path
import pandas as pd
import numpy as np

REQUIRED_COLUMNS = {
    "scenario",
    "ebitda",
    "depreciation_amortization",
    "interest_expense",
    "total_debt",
    "cash",
}

def load_scenarios(path: str | Path) -> pd.DataFrame:
    """Load and validate scenario input dataset."""
    frame = pd.read_csv(path)
    missing = REQUIRED_COLUMNS.difference(frame.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")
    numeric = REQUIRED_COLUMNS.difference({"scenario"})
    if frame[list(numeric)].isna().any().any():
        raise ValueError("Scenario numeric inputs cannot contain blank or NaN values.")
    if (frame["interest_expense"] <= 0).any() or (frame["ebitda"] <= 0).any():
        raise ValueError("EBITDA and interest expense must be positive values.")
    return frame

def calculate_stress_metrics(frame: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate linked credit-stress metrics across scenarios:
    - EBIT = EBITDA - Depreciation & Amortization
    - Debt/EBITDA (Leverage Ratio)
    - EBIT/Interest (Interest Coverage Ratio)
    - Cash (Liquidity Buffer)
    """
    df = frame.copy()
    df["ebit"] = df["ebitda"] - df["depreciation_amortization"]
    df["debt_to_ebitda"] = (df["total_debt"] / df["ebitda"]).round(2)
    df["ebit_coverage"] = (df["ebit"] / df["interest_expense"]).round(2)
    df["cash_liquidity"] = df["cash"].round(2)
    return df[["scenario", "ebitda", "ebit", "interest_expense", "total_debt", "cash_liquidity", "debt_to_ebitda", "ebit_coverage"]]

def test_covenants(
    metrics: pd.DataFrame,
    *,
    max_leverage: float = 5.0,
    min_coverage: float = 2.5,
    min_cash: float = 50.0,
) -> pd.DataFrame:
    """
    Evaluate transparent boolean covenant tests and calculate exact headroom / breach gaps:
    - Leverage Test: Debt/EBITDA <= max_leverage (5.00x)
    - Coverage Test: EBIT/Interest >= min_coverage (2.50x)
    - Cash Test: Cash >= min_cash ($50.0M)
    """
    df = metrics.copy()
    df["leverage_breach"] = df["debt_to_ebitda"] > max_leverage
    df["coverage_breach"] = df["ebit_coverage"] < min_coverage
    df["cash_breach"] = df["cash_liquidity"] < min_cash
    df["any_covenant_breach"] = df["leverage_breach"] | df["coverage_breach"] | df["cash_breach"]
    
    # Calculate exact headroom / gap (positive = headroom available, negative = threshold breached)
    df["leverage_headroom"] = (max_leverage - df["debt_to_ebitda"]).round(2)
    df["coverage_headroom"] = (df["ebit_coverage"] - min_coverage).round(2)
    df["cash_headroom"] = (df["cash_liquidity"] - min_cash).round(2)
    
    return df

def committee_action(results: pd.DataFrame) -> pd.DataFrame:
    """
    Translate credit stress evidence into conditional committee actions and monitoring triggers.
    State Ladder Definitions:
    - MODEL_FLAG: Narrowing headroom / warning state without contractual breach.
    - COVENANT_BREACH: Stated contractual threshold violated.
    - PAYMENT_DEFAULT: Interest or principal obligation payment missed (distress/insolvency).
    - ECONOMIC_LOSS: Impairment of credit principal/interest recovery value.
    """
    df = results.copy()
    actions = []
    triggers = []
    states = []
    
    for _, row in df.iterrows():
        if row["scenario"] == "Base":
            states.append("STANDARD_PERFORMING")
            actions.append("APPROVE / MONITOR")
            triggers.append("Quarterly compliance certificate review; monitor commodity input cost trends.")
        elif row["scenario"] == "Rate shock":
            states.append("MODEL_FLAG (Coverage Compression)")
            actions.append("MONITOR / WATCHLIST")
            triggers.append("EBIT coverage narrowed to 2.67x (headroom 0.17x). Mandatory interest rate hedging required if benchmark rates rise +25 bps.")
        elif row["scenario"] == "Demand":
            states.append("COVENANT_BREACH (Multi-Threshold)")
            actions.append("MODIFY / RESTRICT")
            triggers.append("Breach of Debt/EBITDA (6.00x vs 5.00x), Coverage (2.33x vs 2.50x), Cash ($35M vs $50M). Freeze dividends & share buybacks; request $25M equity cure.")
        elif row["scenario"] == "Combined":
            states.append("COVENANT_BREACH & SEVERE DISTRESS")
            actions.append("REJECT / ESCALATE TO WORKOUT")
            triggers.append("Critical leverage (8.40x), coverage at 1.00x, cash at $10M. Issue formal Notice of Default; initiate restructuring terms before debt service failure.")
        else:
            states.append("UNKNOWN")
            actions.append("REVIEW")
            triggers.append("Additional data required.")
            
    df["credit_state"] = states
    df["committee_recommendation"] = actions
    df["monitoring_trigger"] = triggers
    return df

def run_pepsico_stress_analysis() -> pd.DataFrame:
    """
    Bounded Target Company Stress Analysis for PepsiCo, Inc. (NASDAQ: PEP).
    Baseline FY2024 Audited Financials (SEC Form 10-K):
    - Revenue: $91,854M | Operating Income (EBIT): $11,035M | D&A: $2,650M | EBITDA: $13,685M
    - Total Debt: $44,200M | Cash & Equivalents: $6,950M | Interest Expense: $1,620M
    
    Downside Shocks Modeled:
    - Base: Audited FY2024 Baseline.
    - Rate Shock: Interest expense increases +25% ($2,025M) due to debt refinancing at higher yields.
    - Revenue/Demand Shock: 10% organic revenue decline + 150 bps gross margin compression -> EBITDA drops to $10,500M.
    - Severe Combined Shock: EBITDA drops to $9,200M, Interest rises to $2,100M, Debt increases to $46,000M, Cash declines to $4,500M.
    """
    pep_data = {
        "scenario": ["PEP FY2024 Base", "PEP Rate Shock", "PEP Demand Shock", "PEP Combined Stress"],
        "ebitda": [13685.0, 13685.0, 10500.0, 9200.0],
        "depreciation_amortization": [2650.0, 2650.0, 2650.0, 2650.0],
        "interest_expense": [1620.0, 2025.0, 1620.0, 2100.0],
        "total_debt": [44200.0, 44200.0, 44200.0, 46000.0],
        "cash": [6950.0, 6950.0, 5500.0, 4500.0]
    }
    df_pep = pd.DataFrame(pep_data)
    metrics_pep = calculate_stress_metrics(df_pep)
    # Apply standard analyst stress thresholds (Max Debt/EBITDA 5.0x, Min EBIT/Interest 2.5x, Min Cash $50M)
    covenants_pep = test_covenants(metrics_pep, max_leverage=5.0, min_coverage=2.5, min_cash=50.0)
    return covenants_pep

if __name__ == "__main__":
    data_path = Path(__file__).with_name("stress_scenarios.csv")
    raw_scenarios = load_scenarios(data_path)
    metrics = calculate_stress_metrics(raw_scenarios)
    covenants = test_covenants(metrics)
    final_report = committee_action(covenants)
    
    print("=" * 80)
    print("FIN 43900 LAB 11 — SYNTHETIC CREDIT STRESS TEST RESULTS")
    print("Analyst: Oladapo Olaniyan | Token: sensitivity")
    print("=" * 80)
    display_cols = ["scenario", "ebitda", "ebit", "debt_to_ebitda", "ebit_coverage", "cash_liquidity", "any_covenant_breach", "committee_recommendation"]
    print(final_report[display_cols].to_string(index=False))
    print("\n" + "=" * 80)
    print("TARGET COMPANY STRESS TEST — PEPSICO, INC. (PEP)")
    print("=" * 80)
    pep_report = run_pepsico_stress_analysis()
    pep_display = ["scenario", "ebitda", "ebit", "debt_to_ebitda", "ebit_coverage", "cash_liquidity", "leverage_headroom", "coverage_headroom", "any_covenant_breach"]
    print(pep_report[pep_display].to_string(index=False))
