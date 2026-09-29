"""
Execution wrapper script for Lab 11 Credit Stress Model
Student Analyst: Oladapo Olaniyan
"""
import sys
from pathlib import Path

# Add current directory to path
sys.path.append(str(Path(__file__).parent))

from credit_stress_lab11 import load_scenarios, calculate_stress_metrics, test_covenants, committee_action, run_pepsico_stress_analysis

def main():
    data_path = Path(__file__).parent / "stress_scenarios.csv"
    raw_scenarios = load_scenarios(data_path)
    metrics = calculate_stress_metrics(raw_scenarios)
    covenants = test_covenants(metrics)
    final_report = committee_action(covenants)
    
    print("\n--- SYNTHETIC CREDIT STRESS TEST MATRIX ---")
    print(final_report.to_string(index=False))
    
    print("\n--- PEPSICO (PEP) BOUNDED STRESS TEST MATRIX ---")
    pep_report = run_pepsico_stress_analysis()
    print(pep_report.to_string(index=False))

if __name__ == "__main__":
    main()
