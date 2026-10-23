"""Corrected working packet and closure audit for Oladapo Olaniyan.
Preserves superseded drafts. No locked prediction or test functionality.
"""
from pathlib import Path
import csv,hashlib,json,re
from datetime import datetime,timezone
import build_packet as b
ROOT=Path(__file__).resolve().parents[1]
def main():
    data=json.loads((ROOT/'data/filing-inputs.json').read_text(encoding='utf-8'))
    assumptions=json.loads((ROOT/'data/assumptions.json').read_text(encoding='utf-8'))
    memo=(ROOT/'docs/decision-memo-working.md').read_text(encoding='utf-8').replace('Note15','Note1').replace('Validation-and-AI-Use-working.pdf','Validation-and-AI-Use-working-v2.pdf').replace('source-register-v2.csv','source-register-v3.csv')
    for old,new in [('memo2026','memo 2026'),('Horizon12','Horizon 12'),('forecastFY','forecast FY'),('MarketdateOctober','Market date October'),('BridgeJune13/sharesJuly2','Bridge June 13 / shares July 2'),('cashflow','cash flow'),('basevalue','base value'),('USDm','USD million'),('dilutedproxy','diluted proxy'),('basicpoint','basic point'),('bookdebtproxy','book debt proxy'),('cashfloor','cash floor'),('affiliatebook','affiliate book '),('spending4','spending 4'),('Assumes2027','Assumes 2027')]:memo=memo.replace(old,new)
    # Readability edits only on prose; paths, URLs, hashes and calculations untouched.
    labels=['revenue','profit','impairment','CFO','capex','proxy','margin','SG&A','WACC','Treasury','beta','ERP','spread','FCFF','NOPAT','ROIC','EV','cash','STI','debt','NCI','equity','divide','median','g','year','price','growth']
    for label in labels:memo=re.sub(r'\b'+re.escape(label)+r'(?=[\d$])',label+' ',memo)
    memo=memo.replace('same', 'same')
    b.write_new(ROOT/'docs/decision-memo-working-v2.md',memo)
    validation=(ROOT/'docs/validation-and-ai-use-v2.md').read_text(encoding='utf-8').replace('outputs/verified-run','outputs/final-working-run')
    validation+='\n\n## Final continuation run and draft correction\n\nAnalyst: Oladapo Olaniyan. Final working model produced42 PASS,0 FAIL,5 OPEN,2 QUALIFIED. Fresh no-pip environment run `repro/cold-20261006T053603935700Z/cold-run-evidence.json` exited0 with no stderr and exact SHA256 matches for results.json, statements, sensitivity, checks and peer multiples. This is executed reproducibility evidence; it does not validate the economic assumptions or satisfy the locked test.\n\nFinal primary recheck corrected the capital-spending locator from Note15 to Note1 p68 and distinguishes segment4,192 plus corporate223 from total4,415. Independent note inputs now feed an executable equality check against the CF line. Earlier working PDFs remain superseded; corrected-v2 PDFs and source-register-v3 are current. Packet UTF-8 loading failure and Poppler wrapper path failure were retained; direct bundled Poppler executable rendered the drafts. A localhost/browser preview attempt failed to attach and sandbox socket access was blocked; no successful browser interaction is claimed. Static HTML contains visible inputs/outputs, and PDF layout/text evidence is separately recorded.\n'
    b.write_new(ROOT/'docs/validation-and-ai-use-v3.md',validation)
    research=(ROOT/'docs/research-evolution-v2.md').read_text(encoding='utf-8').replace('Verified-run','Final-working-run').replace('Source-register-v2','Source-register-v3')
    research+='\n\nSource correction within this AI-assisted continuation: the4,415 capital-spending total is Note1 (including corporate), not Note15. Segment subtotal4,192 + corporate223 is now a separate executable primary-source reconciliation. Earlier drafts are superseded and preserved; no student judgment is asserted.\n'
    b.write_new(ROOT/'docs/research-evolution-v3.md',research)
    b.csv_new(ROOT/'source-register-v3.csv',b.ledger(data,assumptions))
    rows=list(csv.DictReader((ROOT/'project1-manifest-working.csv').open(encoding='utf-8')))
    for row in rows:
        row['location_or_url']=row['location_or_url'].replace('-working.pdf','-working-v2.pdf').replace('outputs/review-run','outputs/final-working-run')
        if row['item'] in ('Research-Evolution.pdf','Decision memo or deck','Validation-and-AI-Use.pdf'):row['access_checked']='Local text/page/layout checked; external access/freeze pending'
    b.csv_new(ROOT/'project1-manifest-working-v2.csv',rows)
    for stem,text in [('Decision-Memo',memo),('Research-Evolution',research),('Validation-and-AI-Use',validation)]:
        b.pdf_from_md(ROOT/'docs'/f'{stem}-working-v2.pdf',text,stem+' - Oladapo Olaniyan',stem=='Decision-Memo')
    from pypdf import PdfReader
    checks=[]
    for path in sorted((ROOT/'docs').glob('*working-v2.pdf')):
        reader=PdfReader(path);text='\n'.join(p.extract_text() for p in reader.pages)
        checks.append(dict(analyst='Oladapo Olaniyan',file=str(path.resolve()),pages=len(reader.pages),name_present='Oladapo Olaniyan' in text,
                           corrected_note1='Note1' in text,sha256=hashlib.sha256(path.read_bytes()).hexdigest()))
    if next(x['pages'] for x in checks if 'Decision-Memo' in x['file'])>2:raise RuntimeError('Memo exceeds2 pages')
    b.write_new(ROOT/'outputs/pdf-text-checks-v2.json',json.dumps(checks,indent=2))
    print(json.dumps(checks,indent=2))
if __name__=='__main__':main()
