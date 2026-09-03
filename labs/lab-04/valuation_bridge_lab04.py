"""FIN 43900 Lab 04 — Evidence Ledger & Enterprise-to-Equity Bridge Validation Script.

Target Company: PepsiCo, Inc. (PEP)
Filing: SEC Form 10-K for Fiscal Year Ended December 28, 2024 (CIK: 0000077476)
"""

from pathlib import Path
import pandas as pd

def run_lab04_valuation():
    csv_path = Path(__file__).resolve().parent / "pep_evidence_ledger_lab04.csv"
    df = pd.read_csv(csv_path)
    values = df.set_index("item")["value"].astype(float).to_dict()

    revenue = values["Revenue"]
    ebit_reported = values["EBIT or operating income"]
    tax_rate = values["Tax evidence"]
    dna = values["Depreciation and amortization"]
    capex = values["Capital expenditures"]
    nwc = values["Operating working capital"]
    cash = values["Cash and non-operating assets"]
    debt = values["Debt and debt-like claims"]
    shares = values["Diluted common shares"]
    ebit_core = values["Normalized Core EBIT"]

    # 1. Reported GAAP Unlevered FCFF Base
    nopat_reported = ebit_reported * (1 - tax_rate)
    fcff_base_reported = nopat_reported + dna - capex

    # 2. Normalized Core Unlevered FCFF Base
    nopat_core = ebit_core * (1 - tax_rate)
    fcff_base_core = nopat_core + dna - capex

    # 3. Balance Sheet Bridge Claims
    net_debt = debt - cash

    print("=" * 75)
    print("PEPSICO (PEP) — LAB 04 EVIDENCE LEDGER & BRIDGE AUDIT")
    print("=" * 75)
    print(f"Reported Revenue (GAAP):          ${revenue:,.2f}M")
    print(f"Reported EBIT (GAAP):             ${ebit_reported:,.2f}M  (Margin: {ebit_reported/revenue*100:.2f}%)")
    print(f"Normalized Core EBIT:             ${ebit_core:,.2f}M  (Margin: {ebit_core/revenue*100:.2f}%)")
    print(f"Effective Tax Rate:               {tax_rate*100:.2f}%")
    print(f"Depreciation & Amortization:      ${dna:,.2f}M")
    print(f"Capital Expenditures (CapEx):     ${capex:,.2f}M")
    print(f"Diluted Common Shares:            {shares:,.1f}M")
    print("-" * 75)
    print(f"Reported NOPAT:                   ${nopat_reported:,.2f}M")
    print(f"Reported Base FCFF (excl dNWC):   ${fcff_base_reported:,.2f}M")
    print(f"Normalized Core NOPAT:            ${nopat_core:,.2f}M")
    print(f"Normalized Core FCFF (excl dNWC): ${fcff_base_core:,.2f}M")
    print("-" * 75)
    print("ENTERPRISE-TO-EQUITY BRIDGE CLAIMS:")
    print(f"  (+) Non-Operating Cash:         ${cash:,.2f}M")
    print(f"  (-) Total Debt Obligations:     ${debt:,.2f}M")
    print(f"  (=) Net Debt Claim:             ${net_debt:,.2f}M")
    print("=" * 75)

    # Bridge testing at plausible EV range ($250B - $290B)
    print("\nVALUATION BRIDGE SENSITIVITY (USD millions except per-share price):")
    print(f"{'Enterprise Value':<20}{'Net Debt':<15}{'Equity Value':<15}{'Diluted Shares':<18}{'Per Share Value':<15}")
    print("-" * 83)
    for ev in [250000.0, 270000.0, 290000.0]:
        eq_val = ev - net_debt
        per_share = eq_val / shares
        print(f"${ev:,.0f}M{'':<6}${net_debt:,.0f}M{'':<4}${eq_val:,.0f}M{'':<4}{shares:,.0f}M{'':<9}${per_share:.2f}")
    print("=" * 75)

if __name__ == "__main__":
    run_lab04_valuation()
