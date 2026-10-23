# PEP executed working output

Analyst: Oladapo Olaniyan. Market date: 2026-10-05. USD millions unless per share.

**Working analysis: assumptions and convention risks remain; this is not the analyst's final judgment.**

| Case | EV $M | Equity $M | $/diluted share | PV terminal / EV | WACC | g |
|---|---:|---:|---:|---:|---:|---:|
|low|144,615.6|104,125.6|76.12|77.7%|8.16%|1.5%|
|base|200,935.6|160,445.6|117.29|80.1%|7.66%|2.5%|
|high|273,327.4|232,837.4|170.22|82.8%|7.16%|3.0%|
|value_reset_failure|111,116.2|70,626.2|51.63|77.2%|8.66%|1.0%|

## Base five-year statements (USD millions)

| Year | Revenue | EBIT | Common NI | CFO | Capex | FCFF | Cash | Debt | BS gap |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
|2026|98,621.2|14,201.5|8,949.1|12,845.1|4,635.2|10,278.2|8,409.1|49,182.0|0.0000|
|2027|102,073.0|14,902.7|9,461.6|13,428.6|4,797.4|10,730.5|7,840.2|49,182.0|-0.0000|
|2028|105,645.5|15,635.5|10,006.0|14,122.0|4,965.3|11,279.6|7,548.9|49,182.0|0.0000|
|2029|108,814.9|16,322.2|10,526.1|14,749.7|5,114.3|11,770.4|7,481.5|49,182.0|0.0000|
|2030|112,079.4|17,036.1|11,076.4|15,461.9|5,267.7|12,331.9|7,710.2|49,182.0|-0.0000|

## Material forecast assumptions

{
  "analyst": "Oladapo Olaniyan",
  "status": "AI-proposed working assumptions; student acceptance pending; never company facts",
  "valuation_date": "2026-10-05",
  "fiscal_2026_end": "2026-12-26",
  "tax_rate": 0.22,
  "beta": 0.65,
  "equity_risk_premium": 0.05,
  "debt_spread": 0.008,
  "terminal_roic": 0.15,
  "min_cash": 4000,
  "annual_debt_repayment": 0,
  "annual_buybacks": 1000,
  "dividends_2026": 7900,
  "dividend_growth": 0.03,
  "dilution_increment": 3,
  "affiliates_book_proxy": true,
  "scenarios": {
    "low": {
      "growth": [
        0.04,
        0.015,
        0.02,
        0.02,
        0.02
      ],
      "gross_margin": [
        0.535,
        0.532,
        0.532,
        0.535,
        0.537
      ],
      "sga_ratio": [
        0.4,
        0.405,
        0.402,
        0.4,
        0.398
      ],
      "capex_ratio": 0.049,
      "working_capital_extra_days": 5,
      "wacc_shift": 0.005,
      "terminal_growth": 0.015,
      "causal_story": "Consumer value reset fails to restore North American volume; pricing/mix and input costs compress gross margins; slower sell-through ties up inventory and receivables; debt funding persists."
    },
    "base": {
      "growth": [
        0.05,
        0.035,
        0.035,
        0.03,
        0.03
      ],
      "gross_margin": [
        0.542,
        0.544,
        0.545,
        0.545,
        0.545
      ],
      "sga_ratio": [
        0.398,
        0.398,
        0.397,
        0.395,
        0.393
      ],
      "capex_ratio": 0.047,
      "working_capital_extra_days": 0,
      "wacc_shift": 0,
      "terminal_growth": 0.025,
      "causal_story": "FY2026 reported sales follow midpoint management4-6percent guidance; international strength offsets North American weakness; modest productivity lowers SG&A intensity while reinvestment remains below5percent of sales."
    },
    "high": {
      "growth": [
        0.06,
        0.05,
        0.045,
        0.04,
        0.035
      ],
      "gross_margin": [
        0.55,
        0.553,
        0.555,
        0.555,
        0.555
      ],
      "sga_ratio": [
        0.394,
        0.392,
        0.39,
        0.389,
        0.388
      ],
      "capex_ratio": 0.047,
      "working_capital_extra_days": -2,
      "wacc_shift": -0.005,
      "terminal_growth": 0.03,
      "causal_story": "Value offerings rebuild volume; stronger international mix and productivity improve gross profit and fixed-cost absorption; faster collections reduce working capital."
    },
    "value_reset_failure": {
      "growth": [
        0.04,
        -0.03,
        0,
        0.01,
        0.02
      ],
      "gross_margin": [
        0.535,
        0.515,
        0.52,
        0.525,
        0.53
      ],
      "sga_ratio": [
        0.4,
        0.415,
        0.41,
        0.405,
        0.4
      ],
      "capex_ratio": 0.049,
      "working_capital_extra_days": 10,
      "wacc_shift": 0.01,
      "terminal_growth": 0.01,
      "causal_story": "Named downside: Value Reset Failure. Demand deterioration and price cuts reduce revenue, commodity/distribution costs compress gross margin, overhead adjusts slowly, collections/inventory worsen. Cash falls, modeled funding rises and value declines. This is a separate AI-assisted scenario, not the locked human changed-input test."
    }
  }
}

Observed PEP close: $125.65. Bridge: {"cash": 10251, "sti": 465, "debt": 53214, "nci": 172, "nonoperating_assets": 2180, "point_shares": 1364.891558, "diluted_shares": 1367.891558, "price": 125.65, "balance_date": "2026-06-13", "share_date": "2026-07-02"}

Known normalization: {
  "reported_ebit": 11498,
  "impairment_addback": 1993,
  "normalized_ebit": 13491,
  "normalized_margin": 0.143635879691243,
  "tax_assumption": 0.22,
  "cash_capex": 4415,
  "bs_delta_nwc": 410,
  "cash_flow_delta_nwc": 1212,
  "nwc_definition_difference": 802,
  "normalized_operating_fcff": 8346.98,
  "simple_reported_operating_fcff": 6792.4400000000005,
  "reported_cfo_less_capex": 7672,
  "other_cfo_adjustments": 1553,
  "cfo_to_fcff_reconciliation": 7672.0,
  "explanation": "Normalized FCFF is an operating proxy, not reported cash flow. Other CFO adjustments include impairments, leases, SBC, tax/pension/restructuring timing and other items; not all recur or add economic value. Balance delta excludes cash/debt and uses broad AP line; cash-flow delta excludes acquisition/FX effects. Do not double-count impairment addback with CFO adjustments."
}

Conditional reverse DCF: {
  "status": "solved",
  "uniform_ebit_margin_shift": 0.00846876991924736,
  "target_equity": 171875.5742627,
  "solved_equity": 171875.5742627,
  "residual": 0.0,
  "interpretation": "Uniform reduction in SG&A ratio, holding revenue, gross margin, WACC and g fixed; a conditional price-implied margin path, not a prediction"
}

Qualified peer comparison: {
  "peers": [
    {
      "ticker": "KO",
      "classification": "beverage lens",
      "price_date": "2026-10-05",
      "market_equity": 372213.53501193004,
      "debt": 43543.0,
      "enterprise_value": 380768.53501193004,
      "ebitda": 14812.0,
      "common_net_income": 13107.0,
      "ev_ebitda": 25.706760397780855,
      "pe": 28.398072404969103,
      "status": "qualified book investment/NCI proxies; close differs by0.01 at other provider"
    },
    {
      "ticker": "MDLZ",
      "classification": "snack lens",
      "price_date": "2026-10-05",
      "market_equity": 74651.25825393,
      "debt": 21450.0,
      "enterprise_value": 93819.25825393,
      "ebitda": 4906.0,
      "common_net_income": 2451.0,
      "ev_ebitda": 19.123371026076235,
      "pe": 30.457469707845778,
      "status": "qualified annual earnings hit by1341 derivative mark-to-market losses; no reported separate STI line assumed0"
    }
  ],
  "count": 2,
  "median_ev_ebitda": 22.415065711928545,
  "median_pe": 29.42777105640744,
  "reported_ev_route": 215.36269860334923,
  "normalized_ev_route": 248.02115438707412,
  "reported_pe_route": 177.26904745236925,
  "caution": "Two qualified sector lenses, book investment/NCI proxies, aged share/debt data and FY2025 denominators. Indicative comparison, not approved target or complete peer validation."
}

The downside named Value Reset Failure is an ordinary AI-assisted scenario; it is not the locked changed-input evidence. No locked test is run by this program.

## Validation results

- PASS: FY2023 filing income articulation: Reported statement lines reconcile exactly in USD millions
- PASS: FY2024 filing income articulation: Reported statement lines reconcile exactly in USD millions
- PASS: FY2025 filing income articulation: Reported statement lines reconcile exactly in USD millions
- PASS: FY2024 source balance: Assets 99467; liabilities 81296; gap 0
- PASS: FY2025 source balance: Assets 107399; liabilities 86852; gap 0
- PASS: FY2023 source cash-flow articulation: Cash+restricted ending 9761; net movement 4661
- PASS: FY2024 source cash-flow articulation: Cash+restricted ending 8553; net movement -1208
- PASS: FY2025 source cash-flow articulation: Cash+restricted ending 9204; net movement 651
- PASS: FY2025 cash vs restricted definition: Cash-flow9204 minus balance cash9159 =45 restricted; excluded from bridge
- PASS: low linked statements: Max balance gap 1.09e-11; cash articulation gap 9.09e-13
- PASS: low PP&E/intangible rollforward: Depreciation amortization separated; no negative asset balances
- PASS: low FCFF financing reconciliation: FCFF=CFO-capex+after-tax financing/nonoperating adjustment under positive pretax income; excludes draws and shareholder payouts
- PASS: low finite five years: FY2026-FY2030; all numeric outputs finite
- PASS: base linked statements: Max balance gap 1.46e-11; cash articulation gap 9.09e-13
- PASS: base PP&E/intangible rollforward: Depreciation amortization separated; no negative asset balances
- PASS: base FCFF financing reconciliation: FCFF=CFO-capex+after-tax financing/nonoperating adjustment under positive pretax income; excludes draws and shareholder payouts
- PASS: base finite five years: FY2026-FY2030; all numeric outputs finite
- PASS: high linked statements: Max balance gap 1.46e-11; cash articulation gap 3.64e-12
- PASS: high PP&E/intangible rollforward: Depreciation amortization separated; no negative asset balances
- PASS: high FCFF financing reconciliation: FCFF=CFO-capex+after-tax financing/nonoperating adjustment under positive pretax income; excludes draws and shareholder payouts
- PASS: high finite five years: FY2026-FY2030; all numeric outputs finite
- PASS: value_reset_failure linked statements: Max balance gap 7.28e-12; cash articulation gap 4.55e-13
- PASS: value_reset_failure PP&E/intangible rollforward: Depreciation amortization separated; no negative asset balances
- PASS: value_reset_failure FCFF financing reconciliation: FCFF=CFO-capex+after-tax financing/nonoperating adjustment under positive pretax income; excludes draws and shareholder payouts
- PASS: value_reset_failure finite five years: FY2026-FY2030; all numeric outputs finite
- PASS: low independent bridge: Decimal EV + cash + STI + affiliate book proxy - debt - NCI; per share difference 0
- PASS: base independent bridge: Decimal EV + cash + STI + affiliate book proxy - debt - NCI; per share difference 1.42e-14
- PASS: high independent bridge: Decimal EV + cash + STI + affiliate book proxy - debt - NCI; per share difference 2.84e-14
- PASS: value_reset_failure independent bridge: Decimal EV + cash + STI + affiliate book proxy - debt - NCI; per share difference 0
- PASS: DCF WACC monotonicity: Holding ordinary base FCFF fixed: +/-50bp WACC produces correct EV direction; not the locked test
- PASS: DCF g monotonicity: Holding ordinary base FCFF fixed: +/-50bp g gives correct EV direction
- PASS: DCF invalid boundary rejection: g>=WACC, nonfinite WACC and g=-100percent all raise ValueError
- PASS: Zero operating value boundary: EV0; equity equals bridge adjustments; terminal share undefined rather than division by0
- PASS: Market-date first flow: Only remaining2026 FCFF discounted; no full expired-year flow valued. Uniform accrual assumption is QUALIFIED separately.
- PASS: Published known-answer fixture integrity: Packaged fixtures checked against hashes of audited professor starter; independent of other lab folders
- PASS: Lab05 synthetic known-answer 12 metrics: Max absolute difference 4.7098774e-07; failures []; unchanged distributed fixture packaged under data/
- PASS: CFO-to-operating-FCFF algebra: Includes after-tax nonoperating effect, tax normalization and separately disclosed CFO adjustments; not a claim those adjustments all recur
- QUALIFIED: Working-capital source definition: Cash-flow delta 1212 vs balance delta 410; difference 802 preserved. Acquisition/FX/line-scope component breakdown still pending.
- QUALIFIED: Peer same numerator denominator basis: Common market date; FY2025 GAAP EBIT+D&A and common NI; EV and equity separated. Fair-value and interim rollforward gaps remain.
- PASS: Named downside causal propagation: Year2 FCFF 5936.85 vs base 10730.54; debt draw 21207.58; not a contractual covenant/default test
- PASS: Terminal growth funds reinvestment: Each case funds g/ROIC net reinvestment; terminal ROIC judgment is not validated by this arithmetic
- PASS: Reverse DCF numerical solution: Price-implied SG&A margin shift solves market-equity target; conditional analysis, not a forecast or locked test
- PASS: Cash-ledger corruption detected: Synthetic +100 USDm closing-cash corruption triggers articulation gap; no source or forecast input changed
- PASS: Primary capex source reconciliation: CF capital spending4415 equals Note1 Other Segment Information: segment4192 + corporate223 = total4415. Earlier Note15/segment-total locator corrected, not AI agreement.
- OPEN: Independent valuation source/definition closure: Annual statement arithmetic passes, but post-quarter bridge, dilution, pension/tax claims and affiliate fair values require analyst review.
- OPEN: Stub seasonality and terminal ROIC judgment: Uniform stub cashflow seasonality and terminal ROIC15percent require evidence/analyst acceptance; reinvestment arithmetic is tested separately.
- OPEN: Peer policy judgment: AI-drafted updated policy and candidate disposition require analyst acceptance; no historical human-only attestation adopted.
- OPEN: Human locked changed-input record: All fields remain blank; prediction neither proposed nor authored; test neither designed nor executed.
- OPEN: Edition A recovery: Hash preserved; report content unavailable; staff guidance not requested or invented.

## Remaining limitations

- Human locked prediction/run blank and unexecuted
- Edition A recovery unresolved
- Bridge and point shares dated June/July2026; post-quarter changes unverified
- AI-proposed beta/ERP/spread, forecasts and action thresholds need student review
- Stub FCFF seasonality and 15percent terminal ROIC assumption unvalidated
- Peer fair-value/lease/tax-claim conventions not fully validated
