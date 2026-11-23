"""
FIN 43900 — AI Finance Applications
Module: Robo Advisor Data Models & Schemas
Author: Oladapo Olaniyan
Date: November 2026

Pydantic schemas and enums based on the multi-agent AI Robo Advisor architecture
(matvix90/ai-robo-advisor) and enhanced for FIN 43900.
"""

from enum import Enum
from typing import Dict, List, Optional
from pydantic import BaseModel, Field


# === Enums ===
class Currency(str, Enum):
    USD = "USD"
    EUR = "EUR"
    GBP = "GBP"
    CAD = "CAD"
    JPY = "JPY"


class StockExchange(str, Enum):
    NYSE = "NYSE"
    NASDAQ = "NASDAQ"
    LSE = "LSE"
    EURONEXT = "EURONEXT"
    TSX = "TSX"


class Benchmarks(str, Enum):
    SPY = "SPY"    # S&P 500 Index ETF
    ACWI = "ACWI"  # MSCI All Country World Index ETF
    VT = "VT"      # Vanguard Total World Stock ETF
    QQQ = "QQQ"    # Invesco QQQ Trust (Nasdaq 100)
    BND = "BND"    # Vanguard Total Bond Market ETF

    @property
    def description(self) -> str:
        descriptions = {
            "SPY": "S&P 500 ETF — 500 leading US large-cap corporations",
            "ACWI": "iShares MSCI ACWI ETF — Global equities across 23 developed & 24 emerging markets",
            "VT": "Vanguard Total World Stock ETF — 9,500+ global stocks across all market caps",
            "QQQ": "Invesco QQQ — Top 100 largest non-financial Nasdaq-listed companies",
            "BND": "Vanguard Total Bond Market ETF — Investment-grade taxable US bonds",
        }
        return descriptions.get(self.value, self.value)


class InvestmentGoal(str, Enum):
    RETIREMENT = "Retirement"
    WEALTH_BUILDING = "Wealth Building"
    INCOME_GENERATION = "Income Generation"
    CAPITAL_PRESERVATION = "Capital Preservation"
    EDUCATION_FUNDING = "Education Funding"
    HOUSE_PURCHASE = "House Purchase"
    EMERGENCY_FUND = "Emergency Fund"


class RiskProfile(str, Enum):
    ULTRA_CONSERVATIVE = "Ultra Conservative"
    CONSERVATIVE = "Conservative"
    MODERATE_CONSERVATIVE = "Moderate Conservative"
    MODERATE = "Moderate"
    MODERATE_AGGRESSIVE = "Moderate Aggressive"
    AGGRESSIVE = "Aggressive"
    ULTRA_AGGRESSIVE = "Ultra Aggressive"


class InvestmentHorizon(str, Enum):
    SHORT_TERM = "Short Term (1-3 years)"
    MEDIUM_TERM = "Medium Term (3-7 years)"
    LONG_TERM = "Long Term (7-15 years)"
    VERY_LONG_TERM = "Very Long Term (15+ years)"


class InvestmentKnowledge(str, Enum):
    NONE = "No knowledge - I'm just starting"
    BASIC = "Basic - I understand stocks and bonds"
    INTERMEDIATE = "Intermediate - I've invested before"
    ADVANCED = "Advanced - I actively manage investments"
    EXPERT = "Expert - I'm a finance professional"


class IncomeLevel(str, Enum):
    UNDER_30K = "Under $30,000"
    FROM_30K_TO_60K = "$30,000 - $60,000"
    FROM_60K_TO_100K = "$60,000 - $100,000"
    FROM_100K_TO_150K = "$100,000 - $150,000"
    FROM_150K_TO_250K = "$150,000 - $250,000"
    OVER_250K = "Over $250,000"


class InvestmentPurpose(str, Enum):
    GROW_WEALTH = "Grow my wealth over time"
    GENERATE_INCOME = "Generate regular income"
    PRESERVE_CAPITAL = "Preserve my capital with minimal risk"
    BALANCE_GROWTH_INCOME = "Balance between growth and income"
    SPECIFIC_GOAL = "Save for a specific goal"


class LiquidityNeed(str, Enum):
    ANYTIME = "I might need it anytime"
    WITHIN_1_YEAR = "Within 1 year"
    FROM_1_TO_3_YEARS = "1-3 years"
    FROM_3_TO_5_YEARS = "3-5 years"
    OVER_5_YEARS = "Not for 5+ years"


class MarketDownturnReaction(str, Enum):
    SELL_ALL = "Sell everything immediately"
    SELL_SOME = "Sell some to reduce risk"
    HOLD = "Hold and wait for recovery"
    BUY_MORE = "Buy more at lower prices"


class InvestmentPriority(str, Enum):
    STABILITY = "Stability and capital preservation"
    INCOME = "Regular income"
    BALANCED = "Balanced approach"
    GROWTH = "Maximum growth potential"


# === User Questionnaire Preferences ===
class PortfolioPreference(BaseModel):
    # Personal info
    age: int = Field(default=35, ge=18, le=100, description="Investor age")
    investment_knowledge: InvestmentKnowledge = Field(
        default=InvestmentKnowledge.INTERMEDIATE,
        description="Level of investment knowledge"
    )
    income_level: IncomeLevel = Field(
        default=IncomeLevel.FROM_60K_TO_100K,
        description="Annual income level"
    )

    # Goals and timeline
    goal: InvestmentGoal = Field(
        default=InvestmentGoal.WEALTH_BUILDING,
        description="Primary investment objective"
    )
    investment_purpose: InvestmentPurpose = Field(
        default=InvestmentPurpose.GROW_WEALTH,
        description="Purpose of investment"
    )
    investment_horizon: InvestmentHorizon = Field(
        default=InvestmentHorizon.LONG_TERM,
        description="Investment time horizon"
    )
    liquidity_need: LiquidityNeed = Field(
        default=LiquidityNeed.FROM_3_TO_5_YEARS,
        description="When funds may be needed"
    )

    # Risk assessment
    risk_profile: RiskProfile = Field(
        default=RiskProfile.MODERATE,
        description="Subjective risk tolerance"
    )
    downturn_reaction: MarketDownturnReaction = Field(
        default=MarketDownturnReaction.HOLD,
        description="Reaction to a 20% market drop"
    )
    investment_priority: InvestmentPriority = Field(
        default=InvestmentPriority.BALANCED,
        description="Core portfolio priority"
    )
    max_loss_tolerance: float = Field(
        default=0.15, ge=0.0, le=1.0,
        description="Maximum tolerable 1-year loss percentage (e.g. 0.15 = 15%)"
    )

    # Financial details
    has_emergency_fund: bool = Field(
        default=True,
        description="Whether investor maintains 3-6 months liquid emergency reserves"
    )
    initial_investment: float = Field(
        default=10000.0, gt=0,
        description="Initial capital deployment in USD"
    )
    recurring_contribution: float = Field(
        default=500.0, ge=0,
        description="Monthly planned recurring contribution in USD"
    )

    # Market preferences
    currency: Currency = Field(default=Currency.USD)
    stock_exchange: StockExchange = Field(default=StockExchange.NYSE)
    benchmark: Benchmarks = Field(default=Benchmarks.SPY)


# === Portfolio Strategy & Holdings ===
class AssetAllocationTarget(BaseModel):
    equities: float = Field(..., ge=0.0, le=1.0, description="Equity sleeve target weight")
    fixed_income: float = Field(..., ge=0.0, le=1.0, description="Fixed income sleeve target weight")
    real_estate_commodities: float = Field(..., ge=0.0, le=1.0, description="Real estate / commodities sleeve target weight")
    cash_equivalents: float = Field(..., ge=0.0, le=1.0, description="Cash / ultra-short treasury sleeve target weight")


class PortfolioHolding(BaseModel):
    symbol: str = Field(..., description="Ticker symbol (e.g. VTI, BND)")
    name: str = Field(..., description="Full ETF name")
    asset_class: str = Field(..., description="Equity, Fixed Income, Real Estate, Cash")
    sub_category: str = Field(..., description="US Large Cap, Emerging Markets, Treasury, etc.")
    weight: float = Field(..., ge=0.0, le=1.0, description="Allocation weight summing to 1.0")
    expense_ratio: float = Field(..., ge=0.0, description="Annual TER percentage (e.g. 0.03 for 3 bps)")


class PortfolioStrategy(BaseModel):
    strategy_name: str
    target_allocation: AssetAllocationTarget
    expected_annual_return: float
    expected_annual_volatility: float
    rationale: str


class Portfolio(BaseModel):
    strategy: PortfolioStrategy
    holdings: List[PortfolioHolding]
    benchmark: Benchmarks


# === Quantitative Performance & Audit Metrics ===
class PerformanceMetrics(BaseModel):
    cagr: float
    annualized_volatility: float
    sharpe_ratio: float
    max_drawdown: float
    alpha: float
    beta: float


class AgentAuditVerdict(BaseModel):
    agent_name: str
    passed: bool
    score: float  # 0.0 to 100.0
    summary: str
    recommendations: List[str] = Field(default_factory=list)


class FullRoboAdvisorReport(BaseModel):
    investor_name: str = "Oladapo Olaniyan"
    preference: PortfolioPreference
    calculated_risk_score: float  # 1 to 100
    portfolio: Portfolio
    portfolio_metrics: PerformanceMetrics
    benchmark_metrics: PerformanceMetrics
    weighted_expense_ratio: float
    diversification_hhi: float
    agent_verdicts: Dict[str, AgentAuditVerdict]
    fiduciary_verdict: str  # "APPROVED" or "REVISION_REQUIRED"
    executive_summary: str
    actionable_advice: List[str]
