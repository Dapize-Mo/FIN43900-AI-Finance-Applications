"""FIN 43900 Lab 09 — Credit Evidence and Screening Model.

Student Analyst: Oladapo Olaniyan
Teammate / Partner: kogbuef@purdue.edu
Course: FIN 43900 — AI Finance Applications, Purdue University

This model loads synthetic borrower data, computes credit ratios using documented conventions,
reconciles injected definition conflicts, executes screening policies, and calculates
confusion matrix error metrics (False Positives / Opportunity Cost vs False Negatives / Loss Cost).
"""

from __future__ import annotations

from pathlib import Path
import numpy as np
import pandas as pd


REQUIRED_COLUMNS = {
    "borrower",
    "ebitda",
    "depreciation_amortization",
    "interest_expense",
    "total_debt",
    "current_assets",
    "current_liabilities",
    "cfo",
    "capital_expenditures",
    "adverse_outcome_next_12m",
}


def load_cases(path: str | Path) -> pd.DataFrame:
    """Load borrower case ledger and validate schema integrity."""
    cases = pd.read_csv(path)
    missing = REQUIRED_COLUMNS.difference(cases.columns)
    if missing:
        raise ValueError(f"Required credit fields missing: {sorted(missing)}")
    if cases["borrower"].duplicated().any():
        raise ValueError("Borrower identifiers must be unique")
    return cases


def compute_ratios(cases: pd.DataFrame) -> pd.DataFrame:
    """Compute financial ratios using documented credit conventions.
    
    Conventions:
    1. Gross Leverage = total_debt / ebitda (invalid if ebitda <= 0)
    2. EBIT Interest Coverage = (ebitda - depreciation_amortization) / interest_expense
    3. EBITDA Interest Coverage = ebitda / interest_expense (for conflict reconciliation)
    4. Current Ratio = current_assets / current_liabilities
    5. FCF / Debt = (cfo - capital_expenditures) / total_debt
    """
    df = cases.copy()
    
    # EBIT calculation
    df["ebit"] = df["ebitda"] - df["depreciation_amortization"]
    
    # 1. Gross Leverage (Debt / EBITDA)
    df["leverage"] = np.where(df["ebitda"] > 0, df["total_debt"] / df["ebitda"], np.nan)
    
    # 2. EBIT Interest Coverage
    df["ebit_coverage"] = np.where(df["interest_expense"] > 0, df["ebit"] / df["interest_expense"], np.nan)
    
    # 3. EBITDA Interest Coverage (Injected Conflict)
    df["ebitda_coverage"] = np.where(df["interest_expense"] > 0, df["ebitda"] / df["interest_expense"], np.nan)
    
    # 4. Current Ratio (Liquidity)
    df["current_ratio"] = np.where(df["current_liabilities"] > 0, df["current_assets"] / df["current_liabilities"], np.nan)
    
    # 5. FCF / Debt Yield
    df["fcf_to_debt"] = np.where(df["total_debt"] > 0, (df["cfo"] - df["capital_expenditures"]) / df["total_debt"], np.nan)
    
    return df


def apply_credit_screen(ratios_df: pd.DataFrame, policy: dict) -> pd.DataFrame:
    """Apply policy rules and return screen decision and factor reasons.
    
    Policy format dictionary keys:
    - max_leverage: float (e.g. 4.5)
    - min_ebit_coverage: float (e.g. 3.0)
    - min_current_ratio: float (e.g. 1.0)
    - min_fcf_to_debt: float (e.g. 0.05)
    """
    df = ratios_df.copy()
    decisions = []
    reasons_list = []
    
    for idx, row in df.iterrows():
        reasons = []
        
        # Check invalid EBITDA
        if pd.isna(row["leverage"]):
            reasons.append("Invalid/Negative EBITDA")
        elif row["leverage"] > policy["max_leverage"]:
            reasons.append(f"High Leverage ({row['leverage']:.2f}x > {policy['max_leverage']}x)")
            
        # Check coverage
        if pd.isna(row["ebit_coverage"]) or row["ebit_coverage"] < policy["min_ebit_coverage"]:
            reasons.append(f"Low EBIT Coverage ({row['ebit_coverage']:.2f}x < {policy['min_ebit_coverage']}x)")
            
        # Check current ratio
        if pd.isna(row["current_ratio"]) or row["current_ratio"] < policy["min_current_ratio"]:
            reasons.append(f"Low Liquidity ({row['current_ratio']:.2f}x < {policy['min_current_ratio']}x)")
            
        # Check FCF to Debt
        if pd.isna(row["fcf_to_debt"]) or row["fcf_to_debt"] < policy["min_fcf_to_debt"]:
            reasons.append(f"Weak FCF/Debt ({row['fcf_to_debt']*100:.2f}% < {policy['min_fcf_to_debt']*100:.1f}%)")
            
        # Determine decision
        if len(reasons) == 0:
            decisions.append("approve")
            reasons_list.append("Passes all baseline credit metrics")
        elif len(reasons) == 1 and ("Low Liquidity" in reasons[0] or "Weak FCF" in reasons[0]):
            decisions.append("review")
            reasons_list.append("; ".join(reasons))
        else:
            decisions.append("reject")
            reasons_list.append("; ".join(reasons))
            
    df["decision"] = decisions
    df["reason_codes"] = reasons_list
    return df


def evaluate_decisions(screen_df: pd.DataFrame, label_column: str = "adverse_outcome_next_12m") -> dict[str, int]:
    """Map review/reject to positive risk flag (1) and approve to negative (0).
    
    Labels:
    - Actual = 1 (Adverse Outcome / Default)
    - Actual = 0 (No Default / Safe)
    - Predicted = 1 (Review or Reject flag)
    - Predicted = 0 (Approve flag)
    
    Metrics:
    - TP: Actual 1, Pred 1 (Correctly Flagged Risk)
    - TN: Actual 0, Pred 0 (Correctly Approved Safe Borrower)
    - FP: Actual 0, Pred 1 (Safe Borrower Rejected -> Opportunity Cost)
    - FN: Actual 1, Pred 0 (Unsafe Borrower Approved -> Credit Loss Cost)
    """
    df = screen_df.copy()
    df["pred_risk"] = np.where(df["decision"].isin(["review", "reject"]), 1, 0)
    df["actual_risk"] = df[label_column]
    
    tp = int(((df["actual_risk"] == 1) & (df["pred_risk"] == 1)).sum())
    tn = int(((df["actual_risk"] == 0) & (df["pred_risk"] == 0)).sum())
    fp = int(((df["actual_risk"] == 0) & (df["pred_risk"] == 1)).sum())
    fn = int(((df["actual_risk"] == 1) & (df["pred_risk"] == 0)).sum())
    
    return {"TP": tp, "TN": tn, "FP": fp, "FN": fn}


def main() -> None:
    print("=" * 75)
    print("FIN 43900 Lab 09 — Credit Evidence & Ratio Screening Model")
    print("Analyst: Oladapo Olaniyan")
    print("=" * 75)
    
    # 1. Load Data
    data_path = Path(__file__).resolve().parent / "credit_cases.csv"
    cases = load_cases(data_path)
    
    # 2. Compute Ratios
    ratios = compute_ratios(cases)
    
    # Verify Borrower A Known Answers
    borrower_a = ratios[ratios["borrower"] == "A"].iloc[0]
    print("\n--- 1. BORROWER A KNOWN ANSWERS VERIFICATION ---")
    print(f"Leverage (Debt/EBITDA):       {borrower_a['leverage']:.4f}x (Expected: 4.0000x)")
    print(f"EBIT Interest Coverage:       {borrower_a['ebit_coverage']:.4f}x (Expected: 5.0000x)")
    print(f"EBITDA Interest Coverage:     {borrower_a['ebitda_coverage']:.4f}x (Conflict Check: 6.2500x)")
    print(f"Current Ratio (Liquidity):    {borrower_a['current_ratio']:.4f}x (Expected: 1.2500x)")
    print(f"FCF / Debt Yield:            {borrower_a['fcf_to_debt']*100:.4f}% (Expected: 8.3333%)")
    
    # Display full ratio ledger
    print("\n--- 2. ALL BORROWERS RATIO SUMMARY ---")
    cols_to_print = ["borrower", "ebitda", "total_debt", "leverage", "ebit_coverage", "current_ratio", "fcf_to_debt", "adverse_outcome_next_12m"]
    print(ratios[cols_to_print].to_string(index=False))
    
    # 3. Apply Baseline Credit Policy
    baseline_policy = {
        "max_leverage": 4.5,
        "min_ebit_coverage": 3.0,
        "min_current_ratio": 1.0,
        "min_fcf_to_debt": 0.05,
    }
    screen_results = apply_credit_screen(ratios, baseline_policy)
    
    print("\n--- 3. BASELINE CREDIT SCREENING DECISIONS ---")
    print(screen_results[["borrower", "decision", "adverse_outcome_next_12m", "reason_codes"]].to_string(index=False))
    
    # 4. Evaluate Confusion Matrix & Error Costs
    metrics = evaluate_decisions(screen_results)
    print("\n--- 4. BASELINE CONFUSION MATRIX & EVALUATION ---")
    print(f"True Positives  (TP - Correct Risk Flags):  {metrics['TP']}")
    print(f"True Negatives  (TN - Correct Approvals):   {metrics['TN']}")
    print(f"False Positives (FP - Opportunity Cost):   {metrics['FP']}")
    print(f"False Negatives (FN - Severe Loss Cost):   {metrics['FN']}")
    
    # 5. Sensitivity Analysis: Attack One Rule (Relaxing FCF/Debt to 1%)
    relaxed_policy = baseline_policy.copy()
    relaxed_policy["min_fcf_to_debt"] = 0.01  # Relax threshold from 5% to 1%
    relaxed_screen = apply_credit_screen(ratios, relaxed_policy)
    relaxed_metrics = evaluate_decisions(relaxed_screen)
    
    print("\n--- 5. SENSITIVITY TEST: RELAXING FCF/DEBT RULE TO 1.0% ---")
    print(relaxed_screen[["borrower", "decision", "adverse_outcome_next_12m", "reason_codes"]].to_string(index=False))
    print(f"Relaxed Policy Error Metrics: TP={relaxed_metrics['TP']}, TN={relaxed_metrics['TN']}, FP={relaxed_metrics['FP']}, FN={relaxed_metrics['FN']}")
    if relaxed_metrics["FN"] > metrics["FN"]:
        print("ALERT: Relaxing FCF/Debt created a False Negative (Unsafe borrower passed!). FCF screen is vital for cash-drain cases like Borrower D.")


if __name__ == "__main__":
    main()
