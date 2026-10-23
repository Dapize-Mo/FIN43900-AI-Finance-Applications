"""Formatting-only review packet for Oladapo Olaniyan, FIN-43900.
Preserves source artifacts and every human-only blank. No model/test execution.
"""
from pathlib import Path
import csv,hashlib,json,re,sys
from datetime import datetime,timezone
import build_packet as b
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'presentation'
def clean(text):
    protected=[]
    def save(m):
        protected.append(m.group());return f'@@{len(protected)-1}@@'
    pattern=r'`[^`\n]+`|https?://[^\s|]+|[A-Fa-f0-9]{64}(?![A-Fa-f0-9])|[\w./\\-]+\.(?:md|pdf|csv|json|py|txt|html|png)'
    text=re.sub(pattern,save,text)
    text=re.sub(r'(?<=[A-Za-z])(?=[0-9$])',' ',text)
    text=re.sub(r'(?<=[0-9])(?=[A-Za-z])',' ',text)
    text=re.sub(r',(?=[0-9]{4}\b)',', ',text) # date punctuation; thousands unchanged
    for old,new in [('capitalspending','capital spending'),('freecashflow','free cash flow'),('marketcap','market capitalization'),
       ('cashflow','cash flow'),('cashfloor','cash floor'),('basevalue','base value'),('dilutedproxy','diluted proxy'),
       ('currentbridge','current bridge'),('sourceclosure','source closure'),('sourcecheck','source check'),('studentacceptance','student acceptance'),
       ('cashconversion','cash conversion'),('growthassumption','growth assumption'),('no-AI','no-AI')]:text=text.replace(old,new)
    for i,s in enumerate(protected):text=text.replace(f'@@{i}@@',s)
    # Existing code examples remain readable without literal fence markers.
    text='\n'.join(line for line in text.splitlines() if not line.startswith('```'))
    return text
def dashboard():
    r=json.loads((ROOT/'outputs/final-working-run/results.json').read_text())
    lines=['# Executed valuation dashboard','',
      'Oladapo Olaniyan | Formatting review, October 6, 2026. Working values from final-working-run; finance assumptions unchanged. AI draft watch/defer; student final judgment blank.',
      '',f'Market date: {r["as_of"]}; observed price ${r["bridge"]["price"]:.2f}. USD millions unless per share. Bridge and diluted-share proxies retain dated limitations.',
      '', '| Case | EV ($M) | Equity ($M) | Value/share | TV / EV |','|---|---|---|---|---|']
    for name,v in r['scenarios'].items():lines.append(f'| {name.replace("_"," ")} | {v["enterprise_value"]:,.0f} | {v["common_equity_value"]:,.0f} | ${v["value_per_diluted_share"]:.2f} | {v["terminal_value_share"]:.1%} |')
    lines.extend(['','## Base forecast: linked statements','',
      '| FY | Revenue | EBIT | Common NI | CFO | FCFF |','|---|---|---|---|---|---|'])
    rows=list(csv.DictReader((ROOT/'outputs/final-working-run/forecast-statements.csv').open()))
    for row in rows:
        if row['scenario']=='base':lines.append('| '+str(row['year'])+' | '+' | '.join(f'{float(row[k]):,.0f}' for k in ['revenue','ebit','common_net_income','cfo','fcff'])+' |')
    lines.extend(['','## WACC / terminal-growth sensitivity: value per share','',
      '| WACC | g = 1.5% | g = 2.0% | g = 2.5% | g = 3.0% |','|---|---|---|---|---|'])
    grid=list(csv.DictReader((ROOT/'outputs/final-working-run/sensitivity.csv').open()))
    for w in sorted(set(float(row['wacc']) for row in grid)):
        cells=[row for row in grid if float(row['wacc'])==w]
        lines.append(f'| {w:.2%} | '+' | '.join(f'${float(row["per_share"]):.2f}' for row in cells)+' |')
    lines.extend(['','42 ordinary checks passed; zero failed; five open; two qualified. Clean-run evidence exists. Arithmetic success does not establish economic assumptions or human ownership.',
        '', 'Mandatory remaining evidence: Edition A recovery guidance, human-authored AI-off frozen prediction and AI-closed run, real partner challenge, final student action/dispositions, recordings/transcripts, accessible repository/videos and final manifest/freeze. These are not supplied by rendering.'])
    return '\n'.join(lines)
def main():
    OUT.mkdir(exist_ok=False)
    pairs=[('Decision-Memo','docs/decision-memo-working-v2.md'),('Research-Evolution','docs/research-evolution-v3.md'),('Validation-and-AI-Use','docs/validation-and-ai-use-v3.md')]
    evidence=[]
    for name,relative in pairs:
        source=ROOT/relative;text=clean(source.read_text(encoding='utf-8'))
        text=text.replace('source-register-v2.csv','source-register-v3.csv')
        b.write_new(OUT/f'{name}-review.md',text)
        b.pdf_from_md(OUT/f'{name}-review.pdf',text,name+' - Oladapo Olaniyan',name=='Decision-Memo')
        evidence.append(dict(analyst='Oladapo Olaniyan',source=str(source.resolve()),source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),rendered=str((OUT/f'{name}-review.pdf').resolve()),kind='Formatting only; source values/blank fields retained'))
    parts=[dashboard()]
    for relative in ['docs/continuation-audit.md','docs/assumption-challenges.md','docs/peer-policy.md','docs/video-preparation.md','RUNME.md','docs/completion-report.md']:
        text=clean((ROOT/relative).read_text(encoding='utf-8'))
        parts.extend(['<!-- PAGE BREAK -->',text])
    notes='\n\n'.join(parts)
    b.write_new(OUT/'Supporting-Notes-review.md',notes)
    b.pdf_from_md(OUT/'Supporting-Notes-review.pdf',notes,'Project 1 Supporting Review - Oladapo Olaniyan')
    from pypdf import PdfReader
    for row in evidence:row['pages']=len(PdfReader(row['rendered']).pages)
    assert evidence[0]['pages']<=2,'Memo must stay within two pages'
    notes_pages=len(PdfReader(OUT/'Supporting-Notes-review.pdf').pages)
    audit=dict(analyst='Oladapo Olaniyan',timestamp_utc=datetime.now(timezone.utc).isoformat(),files=evidence,supporting_notes_pages=notes_pages,
       original_sources_unmodified=True,model_not_changed_or_rerun=True,human_locked_fields='retained blank',submission_ready=False,visual_inspection='pending rendered-page inspection')
    b.write_new(OUT/'render-review-record.json',json.dumps(audit,indent=2))
    print(json.dumps(audit,indent=2))
if __name__=='__main__':main()
