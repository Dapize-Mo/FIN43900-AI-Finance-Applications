"""Correct omitted, student-confirmed Lab 10 peer evidence; Oladapo Olaniyan."""
from pathlib import Path
import csv,json,hashlib,shutil,re,html,zipfile
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from pypdf import PdfReader,PdfWriter
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'submission';OUT=BASE/'corrected-20261018';NAME='Oladapo Olaniyan'
backup=BASE/'superseded-before-peer-review-correction-20261018'
backup.mkdir(exist_ok=True)
for name in ['Research-Evolution.pdf','Decision-Memo.pdf','Validation-and-AI-Use.pdf','submission-manifest.csv','Oladapo-Olaniyan-Project1-Repository.zip','prepared-file-hashes.json']:
    if not (backup/name).exists():shutil.copy2(BASE/name,backup/name)
if not (backup/'document-sources').exists():shutil.copytree(BASE/'document-sources',backup/'document-sources')
OUT.mkdir(exist_ok=True)
for folder in ['document-sources','supporting-evidence','repository-package']:
    if not (OUT/folder).exists():shutil.copytree(BASE/folder,OUT/folder)
for name in ['START-HERE.txt','PREPARATION-STATUS.md','package-checks.json','youtube-upload-status.json','submission-manifest.csv','transcript-video-1.txt','transcript-video-2.txt','transcript-video-3.txt']:
    if not (OUT/name).exists():shutil.copy2(BASE/name,OUT/name)
pkg=OUT/'repository-package'
lab=ROOT.parents[1]/'labs/lab-10/lab-10-checkout.md'
assert lab.exists(),lab
source=lab.read_text(encoding='utf-8')
excerpt=source.split('## E — Fresh Eyes (Partner Review & Attack)')[1].split('### 2. Student Attack')[0]
excerpt=excerpt.replace(' (`kogbuef@purdue.edu`)','')
record=f'''# Credited Lab 10 peer challenge - correction addendum
Oladapo Olaniyan | FIN-43900 Project 1 | October 18, 2026

## Provenance and correction
The earlier final package incorrectly described real peer-challenge evidence as missing. Lab 10 already documents a named review; Oladapo confirmed on October 18, 2026 that this discussion happened. The event is dated only September 2026 / Thursday Merit Checkout in the source; no precise day is invented. Reviewer: Kenechukwu Ogbuefi. Source: labs/lab-10/lab-10-checkout.md, section E, Partner Review & Attack. Source SHA256: {hashlib.sha256(lab.read_bytes()).hexdigest()}.

## Preserved recorded exchange
{excerpt.strip()}

## Current project disposition
The challenge asks whether cost-efficiency gains are defensible when history worsened. That concern remains relevant. The current base case assumes SG&A at 39.8% to 39.3% of REVENUE over FY2026-FY2030. The older 74%-72% ratios were a share of GROSS PROFIT; they are not directly comparable and were not copied into the current model.

The earlier defense's numerical normalization and productivity claims are recorded historical wording, not newly verified evidence. The project does not rely on them to establish that the forecast improvement will occur. The current response qualifies the assumed improvement, tests adverse margins and overhead in the named Value Reset Failure case, and retains watch/defer with monitoring of margins and cash conversion. These current model features were already present; no claim is made that a newly discovered document caused an earlier model change.

## Evidence that would change the assumption
Review subsequent filing-based SG&A/revenue, segment volume, pricing/mix, margin and productivity evidence. Sustained overhead pressure or promotional spending without volume recovery would weaken the efficiency assumption and support continued deferral or a lower scenario. Improvement needs comparable definitions and a current bridge. This credited review addresses the documentation gap; it does not validate every forecast input or remove the other disclosed limitations.
'''
(OUT/'supporting-evidence/peer-challenge-correction-20261018.md').write_text(record,encoding='utf-8')
for folder in [pkg/'docs',ROOT/'docs']:
    (folder/'peer-challenge-correction-20261018.md').write_text(record,encoding='utf-8')
for p in [ROOT/'docs/assumption-challenges.md',pkg/'docs/assumption-challenges.md']:
    s=p.read_text(encoding='utf-8')
    s=s.replace('Real partner/fresh-eyes challenge: **[blank - student must supply actual person, date, challenge and response; no invented meeting]**.','Credited peer challenge: Kenechukwu Ogbuefi, Lab 10 (September 2026; exact day unspecified), challenged assumed SG&A improvement despite worsening historical ratios. Oladapo confirmed the discussion on October 18. See peer-challenge-correction-20261018.md for the original exchange, current model response and definition differences. The initial missing-evidence label was a packaging omission.')
    p.write_text(s,encoding='utf-8')
replacements={
 'Decision-Memo':('No real partner challenge is represented as completed where evidence is absent.','Lab 10 records Kenechukwu Ogbuefi challenging assumed SG&A improvement; Oladapo confirmed the review October 18. The current response retains efficiency assumptions as qualified and stresses adverse overhead; see the credited peer-challenge addendum.'),
 'Research-Evolution':('No actual peer challenge has been invented.','Lab 10 credits Kenechukwu Ogbuefi with challenging SG&A efficiency gains despite worsening history; Oladapo confirmed the discussion October 18. Earlier omission of this evidence is corrected in peer-challenge-correction-20261018.md. Old ratios use gross profit; current SG&A ratios use revenue. The current disposition qualifies efficiency gains and retains adverse-margin stress; no historical causation is invented.'),
 'Validation-and-AI-Use':('No real fresh-eyes partner challenge is asserted without evidence.','The earlier missing-peer-evidence label is corrected: Lab 10 names Kenechukwu Ogbuefi challenging SG&A improvement; Oladapo confirmed the discussion October 18. The original exchange and current response are in peer-challenge-correction-20261018.md. Historical gross-profit ratios are distinguished from current revenue ratios; the old defense is not treated as verified financial evidence.')}
builder=(ROOT/'src/prepare_submission.py').read_text(encoding='utf-8')
exec(builder[builder.index('styles=getSampleStyleSheet()'):builder.index('for name,text in')],globals())
for name,(old,new) in replacements.items():
    p=OUT/'document-sources'/f'{name}.md';s=(backup/'document-sources'/f'{name}.md').read_text(encoding='utf-8');assert old in s;s=s.replace(old,new)
    if name=='Validation-and-AI-Use':
        s=s.replace('Hosted links and instructional-team access must be completed in the manifest; missing external access is not resolved by preparing these documents.','The manifest records the public repository and all three Unlisted video links. Anonymous video player access and public repository access passed October 18; receipt 23393007 confirms the first submission. This correction preserves that earlier submission and updates the credited peer-review record.')
        s=s.replace('October 6, 15 and 17, 2026.','October 6, 15, 17 and 18, 2026.')
    p.write_text(s,encoding='utf-8')
    rendered=ROOT/'tmp'/f'{name}-peer-corrected.pdf';pdf(rendered,s)
    shutil.copy2(rendered,OUT/f'{name}.pdf')
    if name=='Research-Evolution':
        original=OUT/'supporting-evidence/Edition-A-original-submitted.pdf'
        writer=PdfWriter();writer.append(str(OUT/f'{name}.pdf'));writer.append(str(original));writer.add_attachment(original.name,original.read_bytes())
        with (OUT/'Research-Evolution-corrected-temp.pdf').open('wb') as f:writer.write(f)
        (OUT/'Research-Evolution-corrected-temp.pdf').replace(OUT/f'{name}.pdf')
    shutil.copy2(p,pkg/'docs/document-sources'/p.name)
    shutil.copy2(OUT/f'{name}.pdf',pkg/'docs'/f'{name}.pdf')
assert len(PdfReader(OUT/'Decision-Memo.pdf').pages)<=2
for p in [pkg/'README.md',ROOT/'README.md',OUT/'START-HERE.txt',OUT/'PREPARATION-STATUS.md']:
    s=p.read_text(encoding='utf-8')
    s=s.replace('Actual fresh-eyes peer challenge evidence is not supplied.','Lab 10 peer review by Kenechukwu Ogbuefi is documented and student-confirmed; see docs/peer-challenge-correction-20261018.md.')
    s=s.replace('Actual partner challenge evidence is missing and has not been invented.','The earlier missing-peer-evidence label was a packaging omission: Lab 10 records Kenechukwu Ogbuefi\'s challenge and Oladapo confirmed it October 18. The correction is documented in supporting-evidence/peer-challenge-correction-20261018.md.')
    s=s.replace('Actual fresh-eyes peer-challenge evidence is absent and has not been invented.','Credited Lab 10 peer challenge evidence is now documented in the October 18 correction addendum; Oladapo confirmed the discussion.')
    p.write_text(s,encoding='utf-8')
for p in [ROOT/'project1-manifest-working-v5.csv',OUT/'submission-manifest.csv']:
    with p.open(encoding='utf-8-sig',newline='') as f:
        r=csv.DictReader(f);fields=r.fieldnames;rows=list(r)
    for row in rows:
        if row['item'] in ['Research-Evolution.pdf','Decision memo or deck','Validation-and-AI-Use.pdf']:
            filename={'Decision memo or deck':'Decision-Memo.pdf'}.get(row['item'],row['item'])
            row.update(frozen_or_commit_id='SHA256 '+hashlib.sha256((OUT/filename).read_bytes()).hexdigest(),duration_or_as_of='Corrected 2026-10-18',access_checked='Corrected peer-credit PDF; rendering and revised submission verification pending',notes='Oladapo Olaniyan | Corrected omitted Lab 10 peer challenge credited to Kenechukwu Ogbuefi; discussion confirmed October 18. Financial outputs unchanged.')
    if not any(r['item']=='Credited peer challenge correction' for r in rows):
        row={k:'' for k in fields};row.update(item='Credited peer challenge correction',required='supporting evidence',location_or_url='supporting-evidence/peer-challenge-correction-20261018.md',title='Oladapo Olaniyan - Credited Lab 10 peer review',duration_or_as_of='Review September 2026; confirmed October 18',access_checked='Source Lab 10 and direct student confirmation',notes='Kenechukwu Ogbuefi questioned SG&A efficiency gains; old and current percentage definitions distinguished.');rows.append(row)
    with p.open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)
shutil.copy2(OUT/'submission-manifest.csv',pkg/'submission-manifest.csv')
checkout=ROOT/'tmp/github-publication/projects/project-1'
for rel in ['README.md','submission-manifest.csv','docs/assumption-challenges.md','docs/peer-challenge-correction-20261018.md']+[f'docs/{n}.pdf' for n in replacements]+[f'docs/document-sources/{n}.md' for n in replacements]:
    shutil.copy2(pkg/rel,checkout/rel)
with zipfile.ZipFile(OUT/'Oladapo-Olaniyan-Project1-Repository-corrected-20261018.zip','w',zipfile.ZIP_DEFLATED) as z:
    for p in pkg.rglob('*'):
        if p.is_file() and '__pycache__' not in p.parts and p.suffix!='.pyc': z.write(p,p.relative_to(pkg))
hashes=[dict(path=p.relative_to(OUT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest(),bytes=p.stat().st_size) for p in OUT.rglob('*') if p.is_file() and p.name!='prepared-file-hashes.json']
(OUT/'prepared-file-hashes.json').write_text(json.dumps(hashes,indent=2),encoding='utf-8')
print(json.dumps({'pdf_pages':{n:len(PdfReader(OUT/f'{n}.pdf').pages) for n in replacements},'backup':str(backup),'peer_challenge':'Lab 10 source plus direct student confirmation'},indent=2))
