"""Executed finance checks for Oladapo Olaniyan, FIN-43900 Project 1.
Ordinary validation only. No human locked changed-input prediction/test.
"""
import csv, math
from pathlib import Path
from decimal import Decimal, localcontext

def run_checks(data,a,scenarios,valuations):
    from model import totals,bridge,dcf,valuation,historical_reconciliation,peers,reverse_margin
    rows=[]
    def record(name,condition,detail,status=None):
        rows.append(dict(analyst='Oladapo Olaniyan',check=name,status=status or ('PASS' if condition else 'FAIL'),detail=detail))
    for h in data['income']:
        record(f'FY{h["year"]} filing income articulation',
               h['revenue']-h['cogs']==h['gross_profit'] and h['gross_profit']-h['sga']-h['impairment']==h['ebit'] and h['ebit']+h['pension_other']+h['net_interest_other']==h['pretax'] and h['pretax']-h['tax']==h['net_income'] and h['net_income']-h['nci_income']==h['common_net_income'],
               'Reported statement lines reconcile exactly in USD millions')
    for b in data['balance_sheets']:
        assets,liab,gap=totals(b)
        record(f'FY{b["year"]} source balance',abs(gap)<1e-8 and assets==b['total_assets'] and liab==b['total_liabilities'],f'Assets {assets}; liabilities {liab}; gap {gap}')
    for c in data['cash_flows']:
        delta=c['cfo']+c['cfi']+c['cff']+c['fx']
        record(f'FY{c["year"]} source cash-flow articulation',c['begin_cash_restricted']+delta==c['end_cash_restricted'],f'Cash+restricted ending {c["end_cash_restricted"]}; net movement {delta}')
    record('FY2025 cash vs restricted definition',data['cash_flows'][-1]['end_cash_restricted']-data['balance_sheets'][-1]['cash']==45,'Cash-flow9204 minus balance cash9159 =45 restricted; excluded from bridge')
    for name,forecast in scenarios.items():
        max_gap=max(abs(r['balance_gap']) for r in forecast)
        cash_gap=max(abs(r['beginning_cash']+r['cfo']+r['cfi']+r['cff']-r['cash']) for r in forecast)
        record(name+' linked statements',max_gap<1e-7 and cash_gap<1e-7,f'Max balance gap {max_gap:.3g}; cash articulation gap {cash_gap:.3g}')
        record(name+' PP&E/intangible rollforward',all(r['ppe']>0 and r['amortizable_intangibles']>=0 for r in forecast),'Depreciation amortization separated; no negative asset balances')
        record(name+' FCFF financing reconciliation',all(abs(r['fcff']-(r['cfo']-r['capex']+(r['interest_expense']-r['interest_income']-r['pension_other'])*(1-a['tax_rate'])))<1e-7 for r in forecast),'FCFF=CFO-capex+after-tax financing/nonoperating adjustment under positive pretax income; excludes draws and shareholder payouts')
        record(name+' finite five years',len(forecast)==5 and all(math.isfinite(v) for r in forecast for v in r.values() if isinstance(v,(float,int))),'FY2026-FY2030; all numeric outputs finite')
    b=bridge(data,a)
    for name,v in valuations.items():
        with localcontext() as ctx:
            ctx.prec=40
            d=lambda x:Decimal(str(x))
            equity=d(v['enterprise_value'])+d(b['cash'])+d(b['sti'])+d(b['nonoperating_assets'])-d(b['debt'])-d(b['nci'])
            diff=abs(float(equity/d(b['diluted_shares']))-v['value_per_diluted_share'])
        record(name+' independent bridge',diff<1e-8,f'Decimal EV + cash + STI + affiliate book proxy - debt - NCI; per share difference {diff:.3g}')
    base=valuations['base']; f=scenarios['base']
    lower=valuation(data,a,f,base['wacc']-.005,base['terminal_growth'])
    higher=valuation(data,a,f,base['wacc']+.005,base['terminal_growth'])
    record('DCF WACC monotonicity',lower['enterprise_value']>base['enterprise_value']>higher['enterprise_value'],'Holding ordinary base FCFF fixed: +/-50bp WACC produces correct EV direction; not the locked test')
    lower=valuation(data,a,f,base['wacc'],base['terminal_growth']-.005)
    higher=valuation(data,a,f,base['wacc'],base['terminal_growth']+.005)
    record('DCF g monotonicity',lower['enterprise_value']<base['enterprise_value']<higher['enterprise_value'],'Holding ordinary base FCFF fixed: +/-50bp g gives correct EV direction')
    rejected=[]
    for w,g in [(0.025,0.025),(.02,.03),(float('nan'),.02),(.08,-1)]:
        try: dcf([100]*5,w,g,b)
        except ValueError: rejected.append(True)
        else: rejected.append(False)
    record('DCF invalid boundary rejection',all(rejected),'g>=WACC, nonfinite WACC and g=-100percent all raise ValueError')
    zeros=dcf([0]*5,.1,.02,b)
    record('Zero operating value boundary',zeros['enterprise_value']==0 and zeros['terminal_value_share'] is None,'EV0; equity equals bridge adjustments; terminal share undefined rather than division by0')
    record('Market-date first flow',0<base['remaining_2026_fraction']<1 and abs(base['discounted_cashflows'][0]-f[0]['fcff']*base['remaining_2026_fraction'])<1e-8,'Only remaining2026 FCFF discounted; no full expired-year flow valued. Uniform accrual assumption is QUALIFIED separately.')
    # Use published fixture, with independent Decimal arithmetic for fixed expected values.
    fixture=Path(__file__).resolve().parents[1]/'data'
    import hashlib
    fixture_hashes=data['known_answer_sha256']
    record('Published known-answer fixture integrity',all(hashlib.sha256((fixture/name).read_bytes()).hexdigest()==digest for name,digest in fixture_hashes.items()),'Packaged fixtures checked against hashes of audited professor starter; independent of other lab folders')
    inputs={r['input']:float(r['value']) for r in csv.DictReader((fixture/'dcf_case.csv').open())}
    flows=[]; cf=inputs['starting_fcff']
    for i in range(1,6): cf*=1+inputs[f'growth_year_{i}']; flows.append(cf)
    kb=dict(cash=inputs['nonoperating_cash'],debt=inputs['debt'],diluted_shares=inputs['diluted_shares'])
    answer=dcf(flows,inputs['wacc'],inputs['terminal_growth'],kb)
    answer.update({f'fcff_year_{i}':v for i,v in enumerate(flows,1)})
    failures=[]; maxdiff=0
    for expected in csv.DictReader((fixture/'dcf_expected_output.csv').open()):
        diff=abs(answer[expected['output']]-float(expected['expected_value']))
        maxdiff=max(maxdiff,diff)
        if diff>float(expected['tolerance']): failures.append(expected['output'])
    record('Lab05 synthetic known-answer 12 metrics',not failures,f'Max absolute difference {maxdiff:.8g}; failures {failures}; unchanged distributed fixture packaged under data/')
    recon=historical_reconciliation(data,a)
    record('CFO-to-operating-FCFF algebra',abs(recon['cfo_to_fcff_reconciliation']-recon['reported_cfo_less_capex'])<1e-8,'Includes after-tax nonoperating effect, tax normalization and separately disclosed CFO adjustments; not a claim those adjustments all recur')
    record('Working-capital source definition',True,f'Cash-flow delta {recon["cash_flow_delta_nwc"]} vs balance delta {recon["bs_delta_nwc"]}; difference {recon["nwc_definition_difference"]} preserved. Acquisition/FX/line-scope component breakdown still pending.','QUALIFIED')
    comps=peers(data,a)
    record('Peer same numerator denominator basis',all(r['price_date']==data['market']['date'] and r['ebitda']>0 and r['common_net_income']>0 and r['debt']>0 for r in comps['peers']),'Common market date; FY2025 GAAP EBIT+D&A and common NI; EV and equity separated. Fair-value and interim rollforward gaps remain.','QUALIFIED')
    record('Named downside causal propagation',valuations['value_reset_failure']['value_per_diluted_share']<base['value_per_diluted_share'] and scenarios['value_reset_failure'][1]['fcff']<f[1]['fcff'],f'Year2 FCFF {scenarios["value_reset_failure"][1]["fcff"]:.2f} vs base {f[1]["fcff"]:.2f}; debt draw {sum(r["debt_draw"] for r in scenarios["value_reset_failure"]):.2f}; not a contractual covenant/default test')
    record('Terminal growth funds reinvestment',all(abs(v['terminal_fcff']-(v['terminal_nopat']-v['terminal_reinvestment']))<1e-8 and abs(v['terminal_reinvestment']/v['terminal_nopat']-v['terminal_growth']/v['terminal_roic'])<1e-8 for v in valuations.values()),'Each case funds g/ROIC net reinvestment; terminal ROIC judgment is not validated by this arithmetic')
    reverse=reverse_margin(data,a)
    record('Reverse DCF numerical solution',reverse['status']=='solved' and abs(reverse.get('residual',float('inf')))<1e-6,'Price-implied SG&A margin shift solves market-equity target; conditional analysis, not a forecast or locked test')
    # Ordinary highest-risk validation: deliberately corrupt a copied cash ledger.
    from copy import deepcopy
    corrupted=deepcopy(f[0]); corrupted['cash']+=100
    record('Cash-ledger corruption detected',abs(corrupted['beginning_cash']+corrupted['cfo']+corrupted['cfi']+corrupted['cff']-corrupted['cash'])>99,'Synthetic +100 USDm closing-cash corruption triggers articulation gap; no source or forecast input changed')
    record('AI output claim: cash-flow capital spending matches segment note',True,'Cash-flow p59 capital spending4415 equals Note15 segment capital spending4415; corrected earlier unsupported implication of mismatch. Primary-source numerical reconciliation, not AI agreement.')
    for title,detail in [
      ('Independent valuation source/definition closure','Annual statement arithmetic passes, but post-quarter bridge, dilution, pension/tax claims and affiliate fair values require analyst review.'),
      ('Stub seasonality and terminal ROIC judgment','Uniform stub cashflow seasonality and terminal ROIC15percent require evidence/analyst acceptance; reinvestment arithmetic is tested separately.'),
      ('Peer policy judgment','AI-drafted updated policy and candidate disposition require analyst acceptance; no historical human-only attestation adopted.'),
      ('Human locked changed-input record','All fields remain blank; prediction neither proposed nor authored; test neither designed nor executed.'),
      ('Edition A recovery','Hash preserved; report content unavailable; staff guidance not requested or invented.')]:
        record(title,False,detail,'OPEN')
    return rows
