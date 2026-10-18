"""Working evidence packet for Oladapo Olaniyan, FIN-43900 Project 1.
PDF authoring uses ReportLab outside the offline model dependency contract.
Never fabricates human-only evidence. Refuses to replace existing artifacts.
"""
from pathlib import Path
from datetime import datetime,timezone
import csv,hashlib,html,json,re
ROOT=Path(__file__).resolve().parents[1]
NAME='Oladapo Olaniyan'
def write_new(path,text):
    with path.open('x',encoding='utf-8',newline='') as f: f.write(text)
def csv_new(path,rows):
    with path.open('x',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
def ledger(data,a):
    rows=[]
    definitions={'ebit':'GAAP operating profit; before pension/nonoperating interest and tax',
      'da':'Consolidated cash-flow depreciation and amortization; included in operating expenses',
      'impairment':'Intangible asset impairment reported separately in income statement',
      'common_net_income':'Net income attributable to PepsiCo common shareholders',
      'cash':'Cash and cash equivalents; excludes restricted cash and STI',
      'sti':'Reported short-term investments; separate from cash',
      'short_debt':'Short-term debt obligations including current reported debt',
      'long_debt':'Long-term debt obligations excluding short/current debt',
      'affiliates':'Reported investment in noncontrolled affiliates; book nonoperating asset proxy',
      'nci':'Reported noncontrolling interest; book claim proxy',
      'point_shares':'Shares outstanding on cover date; not weighted-average EPS denominator',
      'diluted_shares':'Historical weighted-average diluted EPS shares; not point market-cap count',
      'capex':'Cash-flow capital spending; does not include acquisition consideration',
      'payables_other_current':'Accounts payable and other current liabilities; broad scope, not trade AP only',
      'cfo':'Net cash provided by operating activities; not unlevered FCFF',
      'cfi':'Net cash used/provided in investing activities including more than capex',
      'cff':'Net cash used/provided in financing activities',
      'end_cash_restricted':'Cash, cash equivalents and restricted cash in CF statement',
      'begin_cash_restricted':'Beginning cash, cash equivalents and restricted cash',
      'pension_other':'Other pension and retiree medical benefits income/(expense)',
      'net_interest_other':'Net interest expense and other, negative sign for expense',
      'amortization':'Annual amortization expense, Note4',
      'risk_free':'US10-year daily PAR yield proxy, not spot zero curve',
      'price':'Historical regular-session close, not live quote'}
    def add(field,value,source,period,locator,classification='filing fact',definition=None,units=None,assumption=''):
        rows.append(dict(analyst=NAME,input=field,value=value,units=units or ('shares millions' if 'shares' in field else 'USD millions'),period=period,
           definition=definition or definitions.get(field.split('.')[-1],'Exact reported consolidated line; sign as in ledger'),source_name=source['name'],url=source['url'],
           locator=locator,access_date='2026-10-06',classification=classification,status=source['status'],material_assumption=assumption))
    for group,locator in [('income','Consolidated Statement of Income p57; D&A cash flows p59'),('balance_sheets','Consolidated Balance Sheet p61'),('cash_flows','Consolidated Statement of Cash Flows pp59-60')]:
        for entry in data[group]:
            for k,v in entry.items():
                if k not in ('year','source'):
                    ends={2023:'2023-12-30',2024:'2024-12-28',2025:'2025-12-27'}
                    add(f'{group}.FY{entry["year"]}.{k}',v,data['sources'][entry['source']],f'FY{entry["year"]} ended{ends[entry["year"]]}',locator)
    for k,v in data['interim'].items():
        if k in ('source','point_share_date'): continue
        period=data['interim']['point_share_date'] if k=='point_shares' else '24 weeks ended2026-06-13 / balance2026-06-13'
        if k.startswith('prior_'): period='24 weeks ended2025-06-14'
        add('interim.'+k,v,data['sources']['Q26'],period,'Cover shares; income p2; balance p6')
    add('base_details.amortization',83,data['sources']['K25'],'FY2025 ended2025-12-27','Note4 p75')
    for k in ['segment_capital_spending','corporate_capital_spending','total_capital_spending']:
        add('base_details.'+k,data['base_details'][k],data['sources']['K25'],'FY2025 ended2025-12-27','Note1 Other Segment Information p68, Capital Spending2025 column',definition='Independent segment/corporate/consolidated total cash capital spending reconciliation')
    for k,s in [('price','M26'),('risk_free','R26')]:
        add('market.'+k,data['market'][k],data['sources'][s],'2026-10-05',data['sources'][s]['locator'],'market observation',units='USD per share' if k=='price' else 'decimal rate')
    src=dict(name='AI-proposed model assumptions / primary-source anchors where noted',url='local:data/assumptions.json',status='Unapproved working assumptions, not company facts')
    for k,v in a.items():
        if k in ('analyst','status','scenarios'): continue
        add('assumptions.'+k,v,src,'valuation2026-10-05; forecast2026-2030','data/assumptions.json; docs/assumption-challenges.md','model assumption',
            definition='See assumption-challenges.md for value basis, challenge and evidence that changes decision',units='see definition / decimal rates or USD millions',assumption='Student acceptance pending')
    for case,entry in a['scenarios'].items():
        for k,v in entry.items():
            add(f'scenarios.{case}.{k}',json.dumps(v) if isinstance(v,list) else v,src,'FY2026-FY2030','data/assumptions.json scenario '+case,'model assumption',definition='Causal scenario convention; not realized company fact',units='decimal ratio/growth; days for WC; narrative for story',assumption='Student acceptance pending')
    peers=list(csv.DictReader((ROOT/'data/peer-inputs.csv').open()))
    annual={'ebit','da','common_net_income'}
    for p in peers:
        for k in ['price','point_shares','short_debt','current_long_debt','long_debt','cash','sti','nci','nonoperating_investments','ebit','da','common_net_income']:
            source=dict(name=p['ticker']+' '+('FY2025 SEC10K' if k in annual else 'historical close' if k=='price' else 'Q2 SEC10Q'),
              url=p['annual_url'] if k in annual else p['price_url'] if k=='price' else p['filing_url'],status=p['status'])
            add(f'peers.{p["ticker"]}.{k}',p[k],source,p['financial_period'] if k in annual else p['price_date'] if k=='price' else p['share_date'] if k=='point_shares' else p['balance_date'],p['locator'],
                'qualified peer fact/proxy',definition='Same published basis as policy; investments/NCI book proxies; no fair-value validation',units='USD per share' if k=='price' else 'shares millions' if k=='point_shares' else 'USD millions',assumption='STI0 MDLZ means no separately reported line, not proven no investments; bridge review pending')
    return rows
def pdf_from_md(path,text,title,memo=False):
    from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Table,TableStyle,PageBreak
    from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
    from reportlab.lib import colors
    from reportlab.lib.enums import TA_LEFT
    styles=getSampleStyleSheet()
    styles.add(ParagraphStyle(name='BodySmall',fontName='Helvetica',fontSize=9.1 if memo else 9,leading=12,spaceAfter=7))
    styles.add(ParagraphStyle(name='Cell',fontName='Helvetica',fontSize=7.4,leading=9.5))
    styles['Heading1'].fontSize=16; styles['Heading1'].leading=19
    styles['Heading2'].fontSize=11.5; styles['Heading2'].leading=14
    def para(t,style='BodySmall'):
        t=html.escape(t).replace('**','').replace('`','')
        return Paragraph(t,styles[style])
    story=[]; lines=text.splitlines();i=0
    while i<len(lines):
        line=lines[i]
        if line=='<!-- PAGE BREAK -->': story.append(PageBreak());i+=1;continue
        if line.startswith('|'):
            tablelines=[]
            while i<len(lines) and lines[i].startswith('|'):
                parts=[x.strip() for x in lines[i].strip('|').split('|')]
                if not all(re.fullmatch(r'[-: ]+',x or ' ') for x in parts): tablelines.append(parts)
                i+=1
            columns=len(tablelines[0]); widths=([80,68,76,76,76,82] if columns==6 else [468/columns]*columns)
            if sum(widths)>468: widths=[468/columns]*columns
            t=Table([[para(x,'Cell') for x in row] for row in tablelines],colWidths=widths,repeatRows=1,hAlign='LEFT')
            t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#e6eef4')),('VALIGN',(0,0),(-1,-1),'TOP'),('GRID',(0,0),(-1,-1),.3,colors.HexColor('#bcc8d0')),('LEFTPADDING',(0,0),(-1,-1),5),('RIGHTPADDING',(0,0),(-1,-1),5),('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5)]))
            story.extend([t,Spacer(1,8)]);continue
        if line.startswith('# '): story.append(para(line[2:],'Heading1'))
        elif line.startswith('## '): story.append(para(line[3:],'Heading2'))
        elif line.strip(): story.append(para(line))
        else: story.append(Spacer(1,3))
        i+=1
    def footer(c,doc):
        c.setFont('Helvetica',8); c.setFillColor(colors.HexColor('#4a5965'))
        c.drawString(54,28,NAME+' | FIN-43900 Project1 | WORKING / AI-ASSISTED')
        c.drawRightString(558,28,str(doc.page))
    if path.exists(): raise FileExistsError(path)
    SimpleDocTemplate(str(path),pagesize=(612,792),rightMargin=72,leftMargin=72,topMargin=44,bottomMargin=48,title=title,author=NAME).build(story,onFirstPage=footer,onLaterPages=footer)
def main():
    data=json.loads((ROOT/'data/filing-inputs.json').read_text());a=json.loads((ROOT/'data/assumptions.json').read_text())
    r=json.loads((ROOT/'outputs/review-run/results.json').read_text()); b=r['scenarios']['base'];p=r['peer_comparison']
    forecast=list(csv.DictReader((ROOT/'outputs/review-run/forecast-statements.csv').open()))
    downside=[x for x in forecast if x['scenario']=='value_reset_failure']
    draw=sum(float(x['debt_draw']) for x in downside)
    base=[x for x in forecast if x['scenario']=='base']
    sens=list(csv.DictReader((ROOT/'outputs/review-run/sensitivity.csv').open()))
    memo=f'''# PepsiCo: watch/defer pending evidence closure

Oladapo Olaniyan | Buy-side investment committee, no current PEP position | Working AI-assisted memo2026-10-06. Student recommendation/approval: [blank]. Horizon12-24months; forecastFY2026-2030. USD; PEP common shares. MarketdateOctober5,2026; price${data['market']['price']:.2f}. BridgeJune13/sharesJuly2, not an October balance sheet.

## Decision and strongest evidence

AI draft committee ask: retain PEP on a watchlist and defer initiation. Base value${b['value_per_diluted_share']:.2f} is {(1-b['value_per_diluted_share']/data['market']['price']):.1%} below the dated close, with conditional low/base/high values${r['scenarios']['low']['value_per_diluted_share']:.2f}/${b['value_per_diluted_share']:.2f}/${r['scenarios']['high']['value_per_diluted_share']:.2f}. This is a scenario range, not a confidence interval or approved target. No scenario probability or averaged DCF/comps target is assigned. Senior sector analysts retain ownership of the view; this evidence stack supports their review.

FY2025 SEC revenue93,925, operating profit11,498 and intangible impairment1,993 support a13,491 normalized EBIT base (14.36% margin). Removal is an analytical normalization, not evidence that damaged brands recovered. CFO12,087 less cash capex4,415 is7,672; the normalized operating FCFF proxy8,346.98 differs for stated tax/nonoperating/WC reasons. The802 difference between cash-flow and balance-sheet WC change remains unresolved.

## Forecast and valuation mechanics

FY2026 reported growth5% anchors to management4-6% outlook; later3.5/3.5/3/3% is assumed. Base gross margin54.2->54.5%, SG&A39.8->39.3%, capex4.7% of sales, normalized tax22%. Base FY2030 revenue{float(base[-1]['revenue']):,.0f}, EBIT{float(base[-1]['ebit']):,.0f}, FCFF{float(base[-1]['fcff']):,.0f} USDm. Five-year IS/BS/CF articulate; cash funding is explicit, not silent plug.

WACC{b['wacc']:.2%}: observed Treasury5.31% plus assumed beta0.65, ERP5%, debt spread80bp; equity/debt weights use basicpoint marketcap/bookdebtproxy. Remaining2026 FCFF is prorated82/365, an unvalidated seasonality assumption. Terminal g2.5%, assumed incremental ROIC15% and g/ROIC16.67% reinvestment. Terminal PV is{b['terminal_value_share']:.1%} of EV: long-run economics dominate. DCF EV{b['enterprise_value']:,.0f} + cash10,251 + STI465 + affiliatebook2,180 - debt53,214 - NCI172 = common equity{b['common_equity_value']:,.0f} USDm; divide1,367.891558 million dilutedproxy shares. Claims/fair-value/current-date rollforward remain qualified.

<!-- PAGE BREAK -->
## Scenarios, market expectations and method disagreement

| Case | Value/share | WACC | g | Terminal share | Driver |
|---|---|---|---|---|---|
| Low | ${r['scenarios']['low']['value_per_diluted_share']:.2f} | 8.16% | 1.5% | 77.7% | weak demand/costs/WC |
| Base | ${b['value_per_diluted_share']:.2f} | 7.66% | 2.5% | 80.1% | modest productivity |
| High | ${r['scenarios']['high']['value_per_diluted_share']:.2f} | 7.16% | 3.0% | 82.8% | volume/mix recovery |
| Value Reset Failure | ${r['scenarios']['value_reset_failure']['value_per_diluted_share']:.2f} | 8.66% | 1.0% | 77.2% | price cuts/slow overhead |

Ordinary sensitivity spans${min(float(x['per_share']) for x in sens):.2f}-${max(float(x['per_share']) for x in sens):.2f} across WACC6.66-8.66% and g1.5-3%. This is parameter stress, not a causal scenario. Reverse DCF requires roughly{r['reverse_dcf']['uniform_ebit_margin_shift']*100:.2f} percentage points more EBIT margin in every forecast year (lower SG&A), holding other drivers fixed, to explain125.65. It is one conditional market-implied path, not the market's uniquely identified belief.

Predeclared KO/MDLZ sector lenses use Oct5 closes, FY25 GAAP EBIT+D&A/common NI and Q2 bridges. EV/EBITDA median{p['median_ev_ebitda']:.2f}x implies PEP${p['reported_ev_route']:.2f} on reported EBITDA, versus${p['normalized_ev_route']:.2f} on separately normalized EBITDA; P/E median{p['median_pe']:.2f}x implies${p['reported_pe_route']:.2f}. These qualified comparisons exceed DCF because franchise/snack economics differ, MDLZ earnings include derivative mark-to-market losses, and book-investment/claim proxies and old denominators distort comparability. They do not justify averaging into a target. No defensible transaction valuation is claimed.

## Downside, monitoring and committee conditions

Value Reset Failure assumes2027 revenue-3%, gross margin51.5%, SG&A41.5% and10 extra days for both receivables/inventory. Modeled year2 FCFF{float(downside[1]['fcff']):,.0f} USDm; cumulative funding draw{draw:,.0f} USDm while maintaining cashfloor4,000. This links operating weakness to cash, debt and value; it is not an actual covenant/default statement. Persistent deterioration would support do-not-initiate and payout/funding review, rather than relying on a reassuring base case.

AI-proposed entry reconsideration: a20% discount to reviewed basevalue (about${b['value_per_diluted_share']*.8:.2f}) plus verified margin/cash recovery and credible downside funding. Monitor organic volume/pricing, North American margin, inventory/receivable days, cash conversion and debt/payouts after each release. Reversal: structural margin erosion or unavailable funding invalidates initiation; stronger verified economics/current bridge can support reconsideration. Threshold/horizon/risk budget and final committee ask require student judgment, not a claimed personal view.

42 ordinary checks passed, zero failed; clean fresh-environment outputs match five financial artifacts byte-for-byte. Two qualified/five open records remain. See Validation-and-AI-Use-working.pdf and source-register-v2.csv. Human locked prediction/run, real partner challenge and EditionA recovery/staff guidance are incomplete; recordings/transcripts/access/freeze not complete. No submission-ready attestation is made.
'''
    write_new(ROOT/'docs/decision-memo-working.md',memo)
    csv_new(ROOT/'source-register-v2.csv',ledger(data,a))
    cols=['item','required','location_or_url','title','duration_or_as_of','timestamp_index','access_checked','frozen_or_commit_id','notes']
    rows=[]
    entries=[('Research-Evolution.pdf','yes','docs/Research-Evolution-working.pdf','Working B / Edition A recovery hold','2026-10-06','Edition A unavailable; staff guidance needed'),
      ('Repository','yes','','PEP Project1 - Oladapo Olaniyan','','Local code runs; no hosted URL/access confirmation; original README retained; RUNME supplements'),
      ('Visible executed output','yes','outputs/review-run/visible-output.html','Executed working FCFF evidence','Market2026-10-05','Local readable output; not a public deployment'),
      ('Decision memo or deck','yes','docs/Decision-Memo-working.pdf','PEP watch/defer - working memo','2 pages','Student judgment pending'),
      ('Validation-and-AI-Use.pdf','yes','docs/Validation-and-AI-Use-working.pdf','Working checks / AI record','2026-10-06','Locked record blank; final source equivalence/freeze pending'),
      ('Video 1','yes','','Research evolution and AI output check','<=3:00','Not recorded; URL/title/measured duration/index pending'),
      ('Transcript Video 1','yes','','Corrected actual transcript','','Not created; must follow real recording'),
      ('Video 2','yes','','Architecture / finance / clean run','<=5:00','Not recorded; URL/title/measured duration/index pending'),
      ('Transcript Video 2','yes','','Corrected actual transcript','','Not created; must follow real recording'),
      ('Video 3','yes','','Committee decision with live product demo','<=5:00','Not recorded; URL/title/measured duration/index pending'),
      ('Transcript Video 3','yes','','Corrected actual transcript','','Not created; must follow real recording'),
      ('Optional deployed output','no','','','','Not requested; no deployment')]
    for item,required,loc,title,asof,notes in entries:
        row={k:'' for k in cols};row.update(item=item,required=required,location_or_url=loc,title=title,duration_or_as_of=asof,access_checked='pending',notes=NAME+' | WORKING | '+notes);rows.append(row)
    csv_new(ROOT/'project1-manifest-working.csv',rows)
    pdf_from_md(ROOT/'docs/Decision-Memo-working.pdf',memo,'PEP Working Decision Memo - '+NAME,True)
    for stem,md in [('Research-Evolution-working','research-evolution-v2'),('Validation-and-AI-Use-working','validation-and-ai-use-v2')]:
        pdf_from_md(ROOT/'docs'/f'{stem}.pdf',(ROOT/'docs'/f'{md}.md').read_text(encoding='utf-8'),stem+' - '+NAME)
    from pypdf import PdfReader
    qa=[]
    for path in sorted((ROOT/'docs').glob('*working.pdf')):
        reader=PdfReader(path);text='\n'.join(page.extract_text() for page in reader.pages)
        qa.append(dict(analyst=NAME,file=str(path.resolve()),pages=len(reader.pages),name_present=NAME in text,characters=len(text),sha256=hashlib.sha256(path.read_bytes()).hexdigest()))
    if next(x['pages'] for x in qa if 'Decision-Memo' in x['file'])>2: raise RuntimeError('Memo exceeds two pages')
    write_new(ROOT/'outputs/pdf-text-checks.json',json.dumps(qa,indent=2))
    print(json.dumps(qa,indent=2))
if __name__=='__main__':main()
