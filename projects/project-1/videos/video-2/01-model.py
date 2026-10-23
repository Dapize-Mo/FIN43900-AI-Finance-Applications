"""Offline linked FCFF valuation for Oladapo Olaniyan, FIN-43900 Project 1.
AI-assisted working model; all judgment/assumption acceptance remains with analyst.
No locked changed-input prediction/test is implemented or executed here.
"""
from __future__ import annotations
from pathlib import Path
import sys
from datetime import date, datetime, timezone
import argparse, csv, html, json, math, statistics, hashlib

# This presentation copy lives in videos/video-2; the working project root is
# three levels above it and contains data/ and src/.
ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / 'src'
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))
ASSETS = ('cash','sti','receivables','inventory','prepaid','ppe','amortizable_intangibles','goodwill','indefinite_intangibles','affiliates','deferred_tax_assets','other_assets')
LIABILITIES = ('short_debt','payables_other_current','long_debt','deferred_tax_liabilities','other_liabilities')

def load():
    return (json.loads((ROOT/'data/filing-inputs.json').read_text()),
            json.loads((ROOT/'data/assumptions.json').read_text()))

def nwc(bs):
    return bs['receivables']+bs['inventory']+bs['prepaid']-bs['payables_other_current']

def totals(bs):
    assets=sum(bs[k] for k in ASSETS)
    liabilities=sum(bs[k] for k in LIABILITIES)
    return assets, liabilities, assets-liabilities-bs['common_equity']-bs['nci']

def bridge(data, assumptions):
    q=data['interim']
    # Point shares plus incremental dilution proxy; never EPS period-average shares as market cap.
    point=q['point_shares']
    return dict(cash=q['cash'],sti=q['sti'],debt=q['short_debt']+q['long_debt'],
                nci=q['nci'],nonoperating_assets=q['affiliates'],
                point_shares=point,diluted_shares=point+assumptions['dilution_increment'],
                price=data['market']['price'],balance_date='2026-06-13',share_date=q['point_share_date'])

def wacc_inputs(data,a):
    b=bridge(data,a)
    equity=b['price']*b['point_shares']
    debt=b['debt'] # book proxy for market debt; flag rather than call market value
    rf=data['market']['risk_free']
    ke=rf+a['beta']*a['equity_risk_premium']
    kd=rf+a['debt_spread']
    w=ke*equity/(equity+debt)+kd*(1-a['tax_rate'])*debt/(equity+debt)
    return dict(risk_free=rf,beta=a['beta'],erp=a['equity_risk_premium'],cost_equity=ke,
                cost_debt=kd,equity_weight=equity/(equity+debt),wacc=w)

def forecast(data,a,scenario):
    hist=data['income'][-1]
    opening=data['balance_sheets'][-1].copy()
    rev_prior=hist['revenue']
    s=a['scenarios'][scenario]
    depreciation_rate=(hist['da']-data['base_details']['amortization'])/opening['ppe']
    amort_ratio=data['base_details']['amortization']/hist['revenue']
    receivable_ratio=opening['receivables']/hist['revenue']
    inventory_ratio=opening['inventory']/hist['cogs']
    prepaid_ratio=opening['prepaid']/hist['revenue']
    payable_ratio=opening['payables_other_current']/hist['revenue']
    rows=[]
    for i,year in enumerate(range(2026,2031)):
        revenue=rev_prior*(1+s['growth'][i])
        gross_profit=revenue*s['gross_margin'][i]
        cogs=revenue-gross_profit
        sga=revenue*s['sga_ratio'][i]
        # D&A is already embedded in COGS/SG&A; do not subtract twice from EBIT.
        depreciation=opening['ppe']*depreciation_rate
        amortization=min(opening['amortizable_intangibles'],revenue*amort_ratio)
        da=depreciation+amortization
        ebit=gross_profit-sga
        financing_rate=wacc_inputs(data,a)['cost_debt']+max(0,s['wacc_shift'])
        interest_expense=(opening['short_debt']+opening['long_debt'])*financing_rate
        interest_income=opening['cash']*data['market']['risk_free']
        pension_other=-133.0 # conservative continuation; no valuation of nonservice pension income
        pretax=ebit-interest_expense+interest_income+pension_other
        tax=max(pretax,0)*a['tax_rate']
        ni=pretax-tax
        nci_income=max(ni,0)*hist['nci_income']/hist['net_income']
        common_ni=ni-nci_income
        closing=opening.copy()
        extra=s['working_capital_extra_days']/365
        closing.update(receivables=revenue*(receivable_ratio+extra),
                       inventory=cogs*(inventory_ratio+extra),prepaid=revenue*prepaid_ratio,
                       payables_other_current=revenue*payable_ratio)
        delta_nwc=nwc(closing)-nwc(opening)
        capex=revenue*s['capex_ratio']
        closing['ppe']=opening['ppe']+capex-depreciation
        closing['amortizable_intangibles']=opening['amortizable_intangibles']-amortization
        nopat=ebit*(1-a['tax_rate'])
        fcff=nopat+da-capex-delta_nwc
        cfo=ni+da-delta_nwc
        cfi=-capex
        dividends=a['dividends_2026']*(1+a['dividend_growth'])**i
        buybacks=a['annual_buybacks']
        nci_distribution=nci_income
        repayment=min(a['annual_debt_repayment'],opening['long_debt'])
        cash_before_funding=opening['cash']+cfo+cfi-dividends-buybacks-nci_distribution-repayment
        draw=max(0,a['min_cash']-cash_before_funding)
        closing['cash']=cash_before_funding+draw
        closing['short_debt']=opening['short_debt']+draw
        closing['long_debt']=opening['long_debt']-repayment
        closing['common_equity']=opening['common_equity']+common_ni-dividends-buybacks
        closing['nci']=opening['nci']+nci_income-nci_distribution
        cff=draw-repayment-dividends-buybacks-nci_distribution
        assets,liabilities,gap=totals(closing)
        row=dict(scenario=scenario,year=year,revenue=revenue,cogs=cogs,gross_profit=gross_profit,
                 sga=sga,ebit=ebit,depreciation=depreciation,amortization=amortization,da=da,
                 interest_expense=interest_expense,interest_income=interest_income,pension_other=pension_other,
                 pretax=pretax,tax=tax,net_income=ni,nci_income=nci_income,common_net_income=common_ni,
                 nopat=nopat,capex=capex,opening_nwc=nwc(opening),nwc=nwc(closing),delta_nwc=delta_nwc,
                 fcff=fcff,cfo=cfo,cfi=cfi,cff=cff,dividends=dividends,buybacks=buybacks,
                 nci_distribution=nci_distribution,debt_repayment=repayment,debt_draw=draw,
                 beginning_cash=opening['cash'],cash_change=cfo+cfi+cff,
                 assets=assets,liabilities=liabilities,balance_gap=gap,ebit_coverage=ebit/interest_expense,
                 debt_ebitda=(closing['short_debt']+closing['long_debt'])/(ebit+da),**{k:closing[k] for k in ASSETS+LIABILITIES+('common_equity','nci')})
        rows.append(row)
        opening=closing
        rev_prior=revenue
    return rows

def dcf(cashflows,wacc,g,b,times=None,terminal_fcff=None):
    if not (math.isfinite(wacc) and math.isfinite(g) and wacc>g and wacc>0 and g>-1):
        raise ValueError('DCF requires finite WACC>g, WACC>0 and g>-100percent')
    if len(cashflows)!=5 or b['diluted_shares']<=0 or not all(math.isfinite(v) for v in cashflows):
        raise ValueError('DCF requires five finite cashflows and positive diluted shares')
    times=times or [1,2,3,4,5]
    pv_explicit=sum(cf/(1+wacc)**t for cf,t in zip(cashflows,times))
    terminal_fcff=cashflows[-1]*(1+g) if terminal_fcff is None else terminal_fcff
    if not math.isfinite(terminal_fcff):
        raise ValueError('Terminal FCFF must be finite')
    tv=terminal_fcff/(wacc-g)
    pv_tv=tv/(1+wacc)**times[-1]
    ev=pv_explicit+pv_tv
    equity=ev+b['cash']+b.get('sti',0)+b.get('nonoperating_assets',0)-b['debt']-b.get('nci',0)
    return dict(pv_explicit_fcff=pv_explicit,terminal_value_year_5=tv,pv_terminal_value=pv_tv,
                enterprise_value=ev,common_equity_value=equity,value_per_diluted_share=equity/b['diluted_shares'],
                terminal_value_share=pv_tv/ev if ev else None)

def valuation(data,a,rows,wacc=None,g=None):
    s=a['scenarios'][rows[0]['scenario']]
    wacc=wacc if wacc is not None else wacc_inputs(data,a)['wacc']+s['wacc_shift']
    g=g if g is not None else s['terminal_growth']
    stub=(date.fromisoformat(a['fiscal_2026_end'])-date.fromisoformat(a['valuation_date'])).days/365
    # First remaining-year cashflow is a uniform-accrual estimate, not the full expired fiscal year.
    times=[stub+i for i in range(5)]
    flows=[r['fcff'] for r in rows]
    flows[0]*=stub
    roic=a['terminal_roic']
    if not (0<=g<roic):
        raise ValueError('Terminal reinvestment requires 0<=g<terminal ROIC')
    terminal_nopat=rows[-1]['nopat']*(1+g)
    terminal_reinvestment=terminal_nopat*g/roic
    terminal_fcff=terminal_nopat-terminal_reinvestment
    result=dcf(flows,wacc,g,bridge(data,a),times,terminal_fcff)
    result.update(wacc=wacc,terminal_growth=g,remaining_2026_fraction=stub,discount_times=times,
                  discounted_cashflows=flows,stub_policy='uniform annual FCFF pro-rata; seasonality unvalidated',
                  terminal_roic=roic,terminal_nopat=terminal_nopat,terminal_reinvestment=terminal_reinvestment,
                  terminal_fcff=terminal_fcff,
                  terminal_policy='FY2031 NOPAT=FY2030 NOPAT*(1+g); net reinvestment=NOPAT*g/ROIC; FCFF=NOPAT-net reinvestment. ROIC is an unapproved assumption.')
    return result

def reverse_margin(data,a):
    # Ordinary market-implied analysis; not the human locked test.
    from copy import deepcopy
    b=bridge(data,a)
    target=b['price']*b['diluted_shares']
    def value(shift):
        x=deepcopy(a)
        x['scenarios']['base']['sga_ratio']=[v-shift for v in a['scenarios']['base']['sga_ratio']]
        return valuation(data,x,forecast(data,x,'base'))['common_equity_value']
    low,high=-0.06,0.06
    if not value(low)<=target<=value(high):
        return dict(status='unbracketed',target_equity=target,lower_equity=value(low),upper_equity=value(high))
    for _ in range(100):
        mid=(low+high)/2
        if value(mid)<target: low=mid
        else: high=mid
    return dict(status='solved',uniform_ebit_margin_shift=mid,target_equity=target,
                solved_equity=value(mid),residual=value(mid)-target,
                interpretation='Uniform reduction in SG&A ratio, holding revenue, gross margin, WACC and g fixed; a conditional price-implied margin path, not a prediction')

def peers(data,a):
    results=[]
    with (ROOT/'data/peer-inputs.csv').open(newline='',encoding='utf-8') as f:
        for row in csv.DictReader(f):
            fields=['price','point_shares','short_debt','current_long_debt','long_debt','cash','sti','nci','nonoperating_investments','ebit','da','common_net_income']
            v={k:float(row[k]) for k in fields}
            equity=v['price']*v['point_shares']
            debt=v['short_debt']+v['current_long_debt']+v['long_debt']
            ev=equity+debt+v['nci']-v['cash']-v['sti']-v['nonoperating_investments']
            results.append(dict(ticker=row['ticker'],classification=row['classification'],price_date=row['price_date'],
                           market_equity=equity,debt=debt,enterprise_value=ev,ebitda=v['ebit']+v['da'],
                           common_net_income=v['common_net_income'],ev_ebitda=ev/(v['ebit']+v['da']),
                           pe=equity/v['common_net_income'],status=row['status']))
    ev_multiple=statistics.median(r['ev_ebitda'] for r in results)
    pe_multiple=statistics.median(r['pe'] for r in results)
    h=data['income'][-1]
    b=bridge(data,a)
    adjustment=b['cash']+b['sti']+b['nonoperating_assets']-b['debt']-b['nci']
    reported_ebitda=h['ebit']+h['da']
    normalized_ebitda=reported_ebitda+h['impairment']
    return dict(peers=results,count=len(results),median_ev_ebitda=ev_multiple,median_pe=pe_multiple,
                reported_ev_route=(reported_ebitda*ev_multiple+adjustment)/b['diluted_shares'],
                normalized_ev_route=(normalized_ebitda*ev_multiple+adjustment)/b['diluted_shares'],
                reported_pe_route=h['common_net_income']*pe_multiple/b['diluted_shares'],
                caution='Two qualified sector lenses, book investment/NCI proxies, aged share/debt data and FY2025 denominators. Indicative comparison, not approved target or complete peer validation.')

def historical_reconciliation(data,a):
    h=data['income'][-1]; cf=data['cash_flows'][-1]
    normalized_ebit=h['ebit']+h['impairment']
    bs_delta=nwc(data['balance_sheets'][-1])-nwc(data['balance_sheets'][-2])
    cf_delta=-sum(cf[k] for k in ('cash_receivables','cash_inventory','cash_prepaid','cash_payables'))
    economic_fcff=normalized_ebit*(1-a['tax_rate'])+h['da']-cf['capex']-cf_delta
    # Reconcile EBITDA-style operating conversion against reported CFO, not claim CFO-capex is FCFF.
    simple_reported_fcff=h['ebit']*(1-a['tax_rate'])+h['da']-cf['capex']-cf_delta
    aftertax_nonop=(h['pension_other']+h['net_interest_other'])*(1-a['tax_rate'])
    tax_normalization=h['pretax']*a['tax_rate']-h['tax']
    other_cfo_adjustments=cf['cfo']-(h['net_income']+h['da']-cf_delta)
    return dict(reported_ebit=h['ebit'],impairment_addback=h['impairment'],normalized_ebit=normalized_ebit,
                normalized_margin=normalized_ebit/h['revenue'],tax_assumption=a['tax_rate'],cash_capex=cf['capex'],
                bs_delta_nwc=bs_delta,cash_flow_delta_nwc=cf_delta,nwc_definition_difference=cf_delta-bs_delta,
                normalized_operating_fcff=economic_fcff,simple_reported_operating_fcff=simple_reported_fcff,
                reported_cfo_less_capex=cf['cfo']-cf['capex'],other_cfo_adjustments=other_cfo_adjustments,
                cfo_to_fcff_reconciliation=simple_reported_fcff+aftertax_nonop+tax_normalization+other_cfo_adjustments,
                explanation='Normalized FCFF is an operating proxy, not reported cash flow. Other CFO adjustments include impairments, leases, SBC, tax/pension/restructuring timing and other items; not all recur or add economic value. Balance delta excludes cash/debt and uses broad AP line; cash-flow delta excludes acquisition/FX effects. Do not double-count impairment addback with CFO adjustments.')

def csv_write(path,rows):
    if not rows: return
    with path.open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--output',type=Path,default=None,help='New empty output directory; existing work is never overwritten')
    args=parser.parse_args()
    out=args.output or ROOT/'outputs'/datetime.now(timezone.utc).strftime('run-%Y%m%dT%H%M%S%fZ')
    out.mkdir(parents=True,exist_ok=False)
    data,a=load()
    scenarios={name:forecast(data,a,name) for name in a['scenarios']}
    valuations={name:valuation(data,a,rows) for name,rows in scenarios.items()}
    from checks import run_checks
    checks=run_checks(data,a,scenarios,valuations)
    sensitivity=[]
    base_w=wacc_inputs(data,a)['wacc']
    for w in [base_w-.01,base_w-.005,base_w,base_w+.005,base_w+.01]:
        for g in [.015,.02,.025,.03]:
            v=valuation(data,a,scenarios['base'],w,g)
            sensitivity.append(dict(wacc=w,terminal_growth=g,per_share=v['value_per_diluted_share'],terminal_share=v['terminal_value_share']))
    result=dict(analyst=data['analyst'],as_of=data['market']['date'],status='WORKING / NOT SUBMISSION READY',
                assumption_status=a['status'],finance_action_draft='watch/defer pending analyst review and source/convention closure',
                bridge=bridge(data,a),wacc=wacc_inputs(data,a),normalization=historical_reconciliation(data,a),
                scenarios=valuations,peer_comparison=peers(data,a),reverse_dcf=reverse_margin(data,a),checks=checks,
                material_limitations=['Human locked prediction/run blank and unexecuted','Edition A recovery unresolved',
                                     'Bridge and point shares dated June/July2026; post-quarter changes unverified',
                                     'AI-proposed beta/ERP/spread, forecasts and action thresholds need student review',
                                     'Stub FCFF seasonality and 15percent terminal ROIC assumption unvalidated',
                                     'Peer fair-value/lease/tax-claim conventions not fully validated'])
    (out/'results.json').write_text(json.dumps(result,indent=2,allow_nan=False),encoding='utf-8')
    csv_write(out/'forecast-statements.csv',[r for rows in scenarios.values() for r in rows])
    csv_write(out/'sensitivity.csv',sensitivity)
    csv_write(out/'checks.csv',checks)
    csv_write(out/'peer-multiples.csv',result['peer_comparison']['peers'])
    inputs={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted((ROOT/'data').glob('*'))}
    source_files=list((ROOT/'src').glob('*.py'))
    inputs.update({str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in source_files})
    (out/'input-hashes.json').write_text(json.dumps(inputs,indent=2),encoding='utf-8')
    lines=['# PEP executed working output','',f'Analyst: {data["analyst"]}. Market date: {data["market"]["date"]}. USD millions unless per share.','',
           '**Working analysis: assumptions and convention risks remain; this is not the analyst\'s final judgment.**','',
           '| Case | EV $M | Equity $M | $/diluted share | PV terminal / EV | WACC | g |','|---|---:|---:|---:|---:|---:|---:|']
    for name,v in valuations.items():
        lines.append(f'|{name}|{v["enterprise_value"]:,.1f}|{v["common_equity_value"]:,.1f}|{v["value_per_diluted_share"]:.2f}|{v["terminal_value_share"]:.1%}|{v["wacc"]:.2%}|{v["terminal_growth"]:.1%}|')
    lines.extend(['','## Base five-year statements (USD millions)','',
                  '| Year | Revenue | EBIT | Common NI | CFO | Capex | FCFF | Cash | Debt | BS gap |',
                  '|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|']+
                  [f'|{r["year"]}|{r["revenue"]:,.1f}|{r["ebit"]:,.1f}|{r["common_net_income"]:,.1f}|{r["cfo"]:,.1f}|{r["capex"]:,.1f}|{r["fcff"]:,.1f}|{r["cash"]:,.1f}|{r["short_debt"]+r["long_debt"]:,.1f}|{r["balance_gap"]:.4f}|' for r in scenarios['base']])
    lines.extend(['','## Material forecast assumptions','',json.dumps(a,indent=2),
                  '',f'Observed PEP close: ${data["market"]["price"]:.2f}. Bridge: '+json.dumps(result['bridge']),
                  '',f'Known normalization: {json.dumps(result["normalization"],indent=2)}',
                  '',f'Conditional reverse DCF: {json.dumps(result["reverse_dcf"],indent=2)}',
                  '',f'Qualified peer comparison: {json.dumps(result["peer_comparison"],indent=2)}','',
                  'The downside named Value Reset Failure is an ordinary AI-assisted scenario; it is not the locked changed-input evidence. No locked test is run by this program.',
                  '', '## Validation results','']+[f'- {c["status"]}: {c["check"]}: {c["detail"]}' for c in checks]+['','## Remaining limitations','']+['- '+s for s in result['material_limitations']])
    text='\n'.join(lines)+'\n'
    (out/'visible-output.md').write_text(text,encoding='utf-8')
    table=''.join('<tr><td>'+html.escape(name)+'</td>'+''.join(f'<td>{v[k]:,.2f}</td>' for k in ('enterprise_value','common_equity_value','value_per_diluted_share'))+f'<td>{v["terminal_value_share"]:.1%}</td></tr>' for name,v in valuations.items())
    forecast_table=''.join('<tr>'+''.join(f'<td>{r[k]:,.1f}</td>' for k in ('year','revenue','ebit','common_net_income','cfo','capex','fcff','cash'))+'</tr>' for r in scenarios['base'])
    sensitivity_table=''.join(f'<tr><td>{r["wacc"]:.2%}</td><td>{r["terminal_growth"]:.1%}</td><td>${r["per_share"]:.2f}</td><td>{r["terminal_share"]:.1%}</td></tr>' for r in sensitivity)
    html_text=f'''<!doctype html><html lang="en"><meta charset="utf-8"><title>PEP | Oladapo Olaniyan | Working valuation</title><style>body{{font:16px system-ui;max-width:1100px;margin:40px auto;padding:20px;color:#17283b;background:#f5f7fa}}h1{{color:#004d71}}table{{border-collapse:collapse;background:white;width:100%}}td,th{{padding:14px;text-align:right;border-bottom:1px solid #ddd}}td:first-child,th:first-child{{text-align:left}}.status{{background:#fff0ca;padding:18px}}pre{{white-space:pre-wrap;overflow-wrap:anywhere;font-size:13px}}details{{margin:20px 0}}a{{color:#005c87}}</style><h1>PepsiCo committee decision workspace</h1><p>Oladapo Olaniyan | FIN-43900 Project 1 | Market date {data['market']['date']}</p><p class="status">Executed working analysis. Draft action: watch/defer until evidence and analyst judgment are complete. Price ${data['market']['price']:.2f}. All forecast values are assumptions, not company facts.</p><table><tr><th>Case</th><th>EV $M</th><th>Common equity $M</th><th>$/diluted share</th><th>Terminal share</th></tr>{table}</table><h2>Base five-year statements - USD millions</h2><table><tr><th>Year</th><th>Sales</th><th>EBIT</th><th>Common NI</th><th>CFO</th><th>Capex</th><th>FCFF</th><th>Cash</th></tr>{forecast_table}</table><p>Open <a href="forecast-statements.csv">full statements</a>, <a href="sensitivity.csv">WACC/g sensitivity</a>, <a href="checks.csv">check evidence</a>, or <a href="results.json">full results</a>.</p><details open><summary>Finance logic and input assumptions</summary><pre>{html.escape(json.dumps(dict(wacc=result['wacc'],bridge=result['bridge'],normalization=result['normalization'],assumptions=a),indent=2))}</pre></details><details><summary>WACC / terminal growth sensitivity - USD per diluted share</summary><table><tr><th>WACC</th><th>g</th><th>Value/share</th><th>Terminal share</th></tr>{sensitivity_table}</table></details><details><summary>Reverse DCF and peer comparison</summary><pre>{html.escape(json.dumps(dict(reverse=result['reverse_dcf'],peers=result['peer_comparison']),indent=2))}</pre></details><details open><summary>Checks and unresolved evidence</summary><pre>{html.escape(json.dumps(dict(checks=checks,limitations=result['material_limitations']),indent=2))}</pre></details></html>'''
    (out/'visible-output.html').write_text(html_text,encoding='utf-8')
    print(f'Analyst: {data["analyst"]}\nOutput: {out.resolve()}')
    for name,v in valuations.items(): print(f'{name}: ${v["value_per_diluted_share"]:.2f}/share; TV share {v["terminal_value_share"]:.1%}')
    print('Checks:',{s:sum(c['status']==s for c in checks) for s in ('PASS','FAIL','OPEN','QUALIFIED')})
    if any(c['status']=='FAIL' for c in checks): raise SystemExit(1)

if __name__=='__main__':
    main()
