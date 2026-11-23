"""
FIN 43900 — AI Finance Applications
Module: Robo Advisor Terminal CLI Application
Author: Oladapo Olaniyan
Date: November 2026

Replicates the terminal CLI workflow demonstrated by Dr. Z in the YouTube video,
with automatic session saving and progress restoration.
"""

import sys
import os

from models import (
    Benchmarks,
    Currency,
    IncomeLevel,
    InvestmentGoal,
    InvestmentHorizon,
    InvestmentKnowledge,
    InvestmentPriority,
    InvestmentPurpose,
    LiquidityNeed,
    MarketDownturnReaction,
    PortfolioPreference,
    RiskProfile,
    StockExchange,
)
from robo_engine import run_robo_advisor_pipeline
from storage import load_profile, save_profile, save_report_json


def prompt_choice(prompt: str, choices: list, default_idx: int = 0) -> any:
    print(f"\n{prompt}")
    for idx, c in enumerate(choices):
        val_str = c.value if hasattr(c, "value") else str(c)
        prefix = "--> " if idx == default_idx else "    "
        print(f"{prefix}[{idx + 1}] {val_str}")
    
    while True:
        resp = input(f"Select option (1-{len(choices)}) [default: {default_idx + 1}]: ").strip()
        if not resp:
            return choices[default_idx]
        try:
            val = int(resp) - 1
            if 0 <= val < len(choices):
                return choices[val]
        except ValueError:
            pass
        print(f"Invalid selection. Please enter a number between 1 and {len(choices)}.")


def run_cli():
    print("=" * 78)
    print("      FIN 43900 — AI ROBO ADVISOR (MULTI-AGENT DECISION SYSTEM)      ")
    print("               Student & Coverage: Oladapo Olaniyan                  ")
    print("=" * 78)

    # Check for saved profile
    saved = load_profile()
    if saved:
        print(f"\n[Found previous session progress: Age {saved.age}, Goal '{saved.goal.value}']")
        reuse = input("Would you like to resume from your saved profile? (y/n) [default: y]: ").strip().lower()
        if reuse != "n":
            pref = saved
            print("\n>> Loaded saved profile successfully!")
        else:
            pref = None
    else:
        pref = None

    if pref is None:
        print("\n--- SECTION 1: Personal & Financial Profile ---")
        age_in = input("What is your age? [default: 35]: ").strip()
        age = int(age_in) if age_in.isdigit() else 35

        knowledge = prompt_choice("What is your level of investment knowledge?", list(InvestmentKnowledge), 2)
        income = prompt_choice("What is your annual income level?", list(IncomeLevel), 2)

        print("\n--- SECTION 2: Investment Goals & Horizon ---")
        goal = prompt_choice("What is your primary investment goal?", list(InvestmentGoal), 1)
        purpose = prompt_choice("What is your investment purpose?", list(InvestmentPurpose), 0)
        horizon = prompt_choice("What is your investment time horizon?", list(InvestmentHorizon), 2)
        liquidity = prompt_choice("When might you need to access these funds?", list(LiquidityNeed), 3)

        print("\n--- SECTION 3: Risk Assessment ---")
        risk_profile = prompt_choice("How would you describe your subjective risk profile?", list(RiskProfile), 3)
        reaction = prompt_choice("Imagine your portfolio drops 20% in a broad market decline. What do you do?", list(MarketDownturnReaction), 2)
        priority = prompt_choice("What matters most to you in this portfolio?", list(InvestmentPriority), 2)

        loss_in = input("Maximum percentage loss you would tolerate in a 1-year period (e.g. 15 for 15%) [default: 15]: ").strip()
        try:
            max_loss = float(loss_in) / 100.0 if loss_in else 0.15
        except ValueError:
            max_loss = 0.15

        ef_in = input("Do you maintain a 3-6 month liquid emergency fund? (y/n) [default: y]: ").strip().lower()
        has_ef = ef_in != "n"

        print("\n--- SECTION 4: Capital Deployment & Benchmark ---")
        init_in = input("What is your initial investment amount ($)? [default: 10000]: ").strip()
        try:
            initial_cap = float(init_in) if init_in else 10000.0
        except ValueError:
            initial_cap = 10000.0

        rec_in = input("Monthly planned recurring contribution ($)? [default: 500]: ").strip()
        try:
            recurring = float(rec_in) if rec_in else 500.0
        except ValueError:
            recurring = 500.0

        benchmark = prompt_choice("Select your performance benchmark ETF:", list(Benchmarks), 0)

        pref = PortfolioPreference(
            age=age,
            investment_knowledge=knowledge,
            income_level=income,
            goal=goal,
            investment_purpose=purpose,
            investment_horizon=horizon,
            liquidity_need=liquidity,
            risk_profile=risk_profile,
            downturn_reaction=reaction,
            investment_priority=priority,
            max_loss_tolerance=max_loss,
            has_emergency_fund=has_ef,
            initial_investment=initial_cap,
            recurring_contribution=recurring,
            currency=Currency.USD,
            stock_exchange=StockExchange.NYSE,
            benchmark=benchmark
        )

        # Save profile for resumption
        saved_path = save_profile(pref)
        print(f"\n>> Profile saved to {saved_path} (Auto-recovery active)")

    print("\n" + "=" * 78)
    print(">> RUNNING AI ROBO ADVISOR MULTI-AGENT PIPELINE...")
    print("   [1] Risk Scoring Engine")
    print("   [2] Strategy Formulation Agent")
    print("   [3] ETF Portfolio Construction Agent")
    print("   [4] Multi-Agent Audit (Fees, Diversification, Alignment, Performance)")
    print("   [5] Fiduciary Orchestration Synthesis")
    print("=" * 78)

    report = run_robo_advisor_pipeline(pref)
    save_report_json(report)

    # Display Report
    print(f"\n{'='*78}")
    print(f"INVESTOR NAME: {report.investor_name}")
    print(f"STRATEGY:      {report.portfolio.strategy.strategy_name}")
    print(f"RISK SCORE:    {report.calculated_risk_score}/100")
    print(f"FIDUCIARY DISPOSITION: [{report.fiduciary_verdict}]")
    print(f"{'='*78}\n")

    print("--- CONSTRUCTED ETF PORTFOLIO HOLDINGS ---")
    print(f"{'Symbol':<8} {'Asset Class':<15} {'Weight':<10} {'TER':<8} {'Name'}")
    print("-" * 78)
    for h in report.portfolio.holdings:
        print(f"{h.symbol:<8} {h.asset_class:<15} {h.weight*100:>5.1f}%    {h.expense_ratio:>4.2f}%   {h.name}")
    print("-" * 78)
    print(f"Weighted Expense Ratio: {report.weighted_expense_ratio:.3f}% ({report.weighted_expense_ratio*100:.1f} bps)")
    print(f"HHI Concentration:      {report.diversification_hhi:.4f}")

    print("\n--- HISTORICAL BACKTEST METRICS (2-YEAR DAILY) ---")
    print(f"{'Metric':<25} {'Portfolio':<15} {'Benchmark (' + pref.benchmark.value + ')'}")
    print("-" * 78)
    pm = report.portfolio_metrics
    bm = report.benchmark_metrics
    print(f"{'CAGR (Annual Return)':<25} {pm.cagr*100:>6.2f}%         {bm.cagr*100:>6.2f}%")
    print(f"{'Annualized Volatility':<25} {pm.annualized_volatility*100:>6.2f}%         {bm.annualized_volatility*100:>6.2f}%")
    print(f"{'Sharpe Ratio (Rf=4%)':<25} {pm.sharpe_ratio:>6.2f}          {bm.sharpe_ratio:>6.2f}")
    print(f"{'Max Drawdown':<25} {pm.max_drawdown*100:>6.2f}%         {bm.max_drawdown*100:>6.2f}%")
    print(f"{'Alpha (Annualized)':<25} {pm.alpha*100:>6.2f}%         {'0.00%':>6}")
    print(f"{'Beta vs Benchmark':<25} {pm.beta:>6.2f}          {'1.00':>6}")

    print("\n--- MULTI-AGENT AUDIT VERDICTS ---")
    for key, v in report.agent_verdicts.items():
        status_tag = "[PASS]" if v.passed else "[FLAG]"
        print(f"\n{status_tag} {v.agent_name} (Score: {v.score}/100)")
        print(f"  Summary: {v.summary}")
        for r in v.recommendations:
            print(f"  * Recommendation: {r}")

    print("\n" + "=" * 78)
    print("EXECUTIVE SUMMARY:")
    print(report.executive_summary)
    print("=" * 78)


if __name__ == "__main__":
    run_cli()
