"""Prepare Oladapo Olaniyan's local FIN-43900 package; never publishes or submits."""
from pathlib import Path
import csv, hashlib, html, json, re, shutil, subprocess, sys, zipfile
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from pypdf import PdfReader, PdfWriter

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'submission'
NAME='Oladapo Olaniyan'
if OUT.exists(): raise FileExistsError('Preserve existing package: '+str(OUT))
OUT.mkdir()
SUPPORT=OUT/'supporting-evidence'; SUPPORT.mkdir()
SOURCE=OUT/'document-sources'; SOURCE.mkdir()

memo='''# PepsiCo - watch / defer initiation
Oladapo Olaniyan | FIN-43900 Project 1 | Buy-side investment committee; no current position
Decision recorded October 17, 2026. Market reference: October 5, 2026. USD; PEP common shares; diluted-proxy valuation. Five-year forecast: FY2026-FY2030. Working investment review horizon: 12-24 months.

## Committee ask
Keep PepsiCo on watch and defer entry. The base DCF value is $117.29 per diluted-proxy share, approximately 6.7% below the recorded $125.65 price. Low/base/high values are $76.12 / $117.29 / $170.22, conditional scenarios rather than probabilities or a single target. Reconsider after a reviewed current-date bridge and verified margin/cash improvement, or a defensible margin of safety. No numerical purchase threshold is claimed as accepted by the analyst.

## Evidence and normalization
The saved FY2025 filing ledger reports revenue $93,925M, operating profit $11,498M, and intangible impairment $1,993M. Adding back the impairment gives normalized EBIT $13,491M. This analytical adjustment does not establish brand recovery or make impairments economically irrelevant. CFO $12,087M less capex $4,415M equals $7,672M; this is not automatically FCFF. Segment capex $4,192M plus corporate $223M reconciles to consolidated $4,415M. Cash-flow working-capital investment and the balance-sheet change differ by $802M; that scope difference remains qualified.

## Forecast, FCFF and bridge
The base forecast assumes revenue growth of 5%, then 3.5%, 3.5%, 3%, and 3%; gross margin 54.2% to 54.5%; SG&A 39.8% to 39.3% of revenue; capex 4.7% of revenue; and a 22% normalized tax rate. These are assumptions, not company facts. FY2030 revenue is about $112,079M, EBIT $17,036M, and FCFF $12,332M. FCFF equals after-tax EBIT plus D&A less capex and operating working-capital investment; financing stays outside FCFF.

Base WACC is 7.66%, with assumed beta 0.65, equity risk premium 5%, debt spread 80bp, and a dated Treasury proxy 5.31%. Terminal growth is 2.5%, terminal incremental ROIC 15%, and terminal reinvestment is NOPAT times growth divided by ROIC. Terminal value is 80.1% of EV. Remaining FY2026 FCFF uses an 82/365 stub, with seasonality unvalidated.

The EV-to-equity bridge is $200,936M EV + $10,251M cash + $465M short-term investments + $2,180M affiliate book-value proxy - $53,214M debt - $172M noncontrolling interest = approximately $160,446M common equity. Dividing by 1,367.891558M diluted-proxy shares gives $117.29. Balance dates are June 13 and share date July 2; a complete October rollforward is not claimed.

<!-- PAGE BREAK -->
## Scenarios and market expectations
| Case | Value/share | WACC | Terminal growth |
|---|---|---|---|
| Low | $76.12 | 8.16% | 1.5% |
| Base | $117.29 | 7.66% | 2.5% |
| High | $170.22 | 7.16% | 3.0% |
| Value Reset Failure | $51.63 | 8.66% | 1.0% |

WACC/g sensitivity spans about $86.17-$166.79 over WACC 6.66%-8.66% and growth 1.5%-3%. Reverse DCF requires approximately 0.85 percentage points more EBIT margin throughout the forecast, holding other inputs fixed, to support $125.65. That is one conditional path rather than a unique market forecast.

## Peer disagreement and downside
The predeclared Coca-Cola and Mondelez lenses use dated annual earnings and qualified balance-sheet proxies. Median EV/EBITDA is about 22.42x and P/E 29.43x. The implied reported-EBITDA and earnings routes produce approximately $215.36 and $177.27 per share; these are qualified comparisons, not additional price targets. Business mix, derivative losses, aged denominators, and investment/claim conventions limit comparability. Do not mechanically average the peer outputs and DCF. No unsupported transaction valuation is used.

Value Reset Failure combines weaker revenue, lower gross margin, higher SG&A, and longer receivable/inventory days. It produces year-two FCFF about $5,937M and modeled cumulative funding draws about $21,208M while maintaining a $4,000M cash floor. This is a modeled funding stress, not a contractual covenant or default forecast.

## Monitoring and reversal conditions
Monitor revenue growth, operating margins, cash conversion, debt, and payouts after future releases. Reconsider entry only when updated evidence supports the valuation and funding path, or when price offers a defensible margin of safety. Structural margin erosion, weak cash conversion, or inadequate downside funding would argue against initiation. The current-date bridge, working-capital scope, peer definitions, and long-run assumptions remain material limitations.

## Validation, AI and sources
The executed ordinary checks report 42 PASS, 0 FAIL, 5 OPEN, and 2 QUALIFIED; the fresh-environment run reproduced principal outputs. A separate ROIC test, 15% to 12%, lowered value from $117.29 to $111.41, a $5.88 / 5.02% decline. These validate named mechanics and model response, not all economic assumptions. No real partner challenge is represented as completed where evidence is absent.

Codex/GPT-6 assisted research, code, calculations, documents, scripts, and transcript comparison. Material uses, independent checks, qualifications, and reported course clarifications are disclosed in Validation-and-AI-Use.pdf. Source dates and locators are in source-register-v3.csv and data/filing-inputs.json; management-outlook-ledger.csv distinguishes guidance from assumptions. The recommendation above is supported by Oladapo's recorded committee position.
'''

research='''# Research evolution - PepsiCo
Oladapo Olaniyan | FIN-43900 Project 1 | Edition B and explanatory record, October 17, 2026

## Preserved Edition A and reported resolution
Brightspace receipt 22599005 records the September 1, 2026, 2:30 PM submission. The receipt-linked attachment contains an Edge error page. Its original bytes are preserved as supporting-evidence/Edition-A-original-submitted.pdf and embedded in this PDF; its page is reproduced at the end. SHA256: f745e7ea27a1445830573029a77d28967a1e4f5e53a9ba9a794079373f35464f.

Oladapo reports that the TA said the copy is acceptable as long as the information is the same. The clarification was documented locally October 17; the earlier conversation's date is unspecified. No written TA approval or recovered report content is claimed.

A separate preexisting draft is preserved unchanged as supporting-evidence/Edition-A-preexisting-draft.md. It contains incomplete numerical text and an attestation whose history is not independently verified here. It is supporting evidence, not relabeled as the original submitted PDF. The comparison below explicitly uses that draft where indicated.

## Edition A supporting draft to Edition B
| Topic | Supporting preexisting draft | Edition B and reason |
|---|---|---|
| Action | States Watch-Defer | Oladapo again states watch/defer in Videos 1 and 3; no action change is claimed |
| Dates and evidence | References FY2024 and September 1 valuation context; several financial numbers are incomplete | FY2025 filing ledger, June/July interim bridge/share dates and October 5 market reference; facts and assumptions separated |
| Engine | Describes an FCFF/enterprise-to-equity valuation contract | Executed five-year linked statements drive FCFF/WACC, with scenario, sensitivity and bridge checks |
| Risk and decision conditions | Calls for margin of safety or volume stabilization | Recorded margin/cash recovery, reviewed current-date bridge, downside funding and price conditions support continued deferral |

This comparison does not assert that the draft matches the submitted PDF's missing report content, repair its damaged numbers, or certify the original tool-use history.

## Consequential development and attribution
Course requirements drove the linked-statement FCFF architecture. AI-assisted code and source review rebuilt earlier lab mechanics, replacing an FCFE/stale-price path rather than renaming it. Unsupported company stress claims from prior work were rejected. Earlier model outputs used mechanical terminal FCFF growth; the correction funds growth with terminal NOPAT times g/ROIC. Base value changed from $130.67 to $117.29 in the preserved working versions. This was a model-design correction, not an invented recollection of a student decision.

## AI-output check: capex
An AI implication of a mismatch between segment and consolidated capital spending was corrected using the saved FY2025 primary-source reconciliation: segment $4.192B plus corporate $0.223B equals consolidated $4.415B. Segment-only spending would understate investment and overstate cash available to investors. The locator was corrected to Note 1, page 68. Independent source arithmetic, rather than another AI answer, supports that disposition.

## Separate test and final interpretation
The frozen ROIC test changed only terminal incremental ROIC from 15% to 12%. More reinvestment at the same growth lowers terminal FCFF and value. Base value fell $117.29 to $111.41 ($5.88 / 5.02%), consistent with the recorded prediction. AI assistance is disclosed under Oladapo's report of the professor's classroom clarification. The model's unchanged action field is a fixed label rather than a tested threshold rule.

Oladapo's recorded recommendation is watch/defer. The recordings support monitoring revenue, margin, cash conversion, debt and payouts, with a reviewed bridge and improved margin/cash evidence or a defensible price margin of safety as reconsideration conditions. They do not establish blanket acceptance of all proposed assumptions or the earlier AI-proposed $93.84 entry threshold.

## Recording clarification and retained limitations
Video 1 shows earlier pages saying guidance is unresolved and completed checks are not run. Those pages predate this clarified evidence package. Exact page snapshots and the unchanged recording are preserved. Current ordinary checks are 42 PASS / 0 FAIL / 5 OPEN / 2 QUALIFIED, and the separate ROIC test has its own frozen record.

The current-date bridge, working-capital difference, peer comparability, stub seasonality and long-run ROIC remain qualified. No actual peer challenge has been invented. Detailed evidence, source locators, reported staff clarification and the complete recording index accompany the repository package. The original error-page attachment follows as a preserved visual page; the byte-identical original file is separately included.
'''

validation='''# Validation and AI use
Oladapo Olaniyan | FIN-43900 Project 1 | October 17, 2026

## Evidence boundary
Market reference: October 5, 2026. Annual accounts: FY2025 ended December 27, 2025. Interim balance: June 13, 2026; point shares: July 2. USD millions and shares millions except per-share values and decimal rates. Source retrieval and accounting definitions are recorded in source-register-v3.csv and data/filing-inputs.json. No complete post-quarter cash/debt/share rollforward or new current market quote is claimed.

## Executed checks
| Area | Evidence / result | Limit |
|---|---|---|
| Ordinary suite | 42 PASS; 0 FAIL; 5 OPEN; 2 QUALIFIED | PASS applies to named checks, not all economics |
| Known answer | Twelve published synthetic metrics reconciled | Mechanical reference case, not company forecast proof |
| Source/definition | Capex 4,192 + 223 = 4,415; filing statement arithmetic and cash distinctions | Working-capital scope difference $802M remains qualified |
| Forecast articulation | Twenty scenario-year rows; statement/cash reconciliation | Simplified frozen accounts and funding assumptions disclosed |
| FCFF / bridge | Financing reconciliation; independent Decimal bridge | Book proxies and stale balance/share dates remain |
| DCF | Boundary rejection, monotonicity, terminal reinvestment, reverse residual | Stub timing and economic assumptions not established |
| Failure / downside | Deliberate copied-cash corruption detected; named downside propagated | Not a default/covenant forecast |
| Clean rerun | Exit 0, no stderr, five principal output hashes match | Historical log paths predate folder move |

Evidence: outputs/final-working-run/checks.csv and repro/cold-20261006T053603935700Z/cold-run-evidence.json. Open and qualified rows remain in the deliverable output. An older static row about a blank locked record predates the dedicated test below; it is not the test's result.

## Locked changed-input record
| Field | Recorded evidence |
|---|---|
| Input and units | Annual terminal incremental ROIC; 15.0% to 12.0% |
| Frozen prediction | Lower ROIC increases reinvestment for fixed growth, lowers terminal FCFF/value; watch/defer expected to remain |
| Precommit | October 15, 2026, 5:22 PM CDT; separately frozen baseline and snapshot hashes |
| Run | Separate experiment copy; exit 0; only the terminal_roic assumption changed |
| Before / after | Reinvestment $2,270.1M to $2,837.6M; terminal FCFF $11,350.3M to $10,782.8M; EV $200,935.6M to $192,886.3M |
| Value / direction | $117.29 to $111.41; decline $5.88 / 5.02% using unrounded values; predicted direction matched |
| Decision effect | Both values below $125.65; fixed draft watch/defer label unchanged; no numeric decision threshold is tested |
| Evidence | repro/locked-change-20261015T1722CDT/locked-test-report.md and frozen-baseline / experiment-run folders |

The prediction and test were AI-assisted. Oladapo reports the professor clarified in class that the posted no-AI wording was a typo and encouraged AI use. The original posted wording remains preserved; no written amendment is invented. This test checks one input's propagation, not that 12% or 15% is the right economic ROIC.

## Material AI uses and dispositions
Exposed assistant identity: Codex / GPT-6. A finer build identifier is unavailable. Material interactions occurred October 6, 15 and 17, 2026. Browser/source retrieval, local Python calculation, ReportLab PDF preparation, and local faster-whisper small.en transcription comparison were used.

| AI-assisted task | Check and disposition |
|---|---|
| Requirements and lab audit | Compared with Brightspace, source files and receipt; use traceable findings; recorded TA resolution supplements old status |
| Source ledger and normalization | Separate filing arithmetic and locators; normalization economics remain qualified |
| Linked forecast / FCFF / WACC code | Known answers, statement/cash identities, bridge and boundaries; computational checks pass, assumption risks retained |
| Terminal reinvestment design | Explicit g/ROIC funding replaces mechanical growth; terminal ROIC remains assumed |
| Forecast/scenario/peer inputs | Labeled assumptions and qualified comparisons; not represented as observed future facts |
| Capex mismatch implication | Corrected against primary arithmetic: $4.192B + $0.223B = $4.415B |
| Changed-input prediction and run | AI assistance disclosed; frozen copy and one-variable comparison retained |
| Memo, research and recording scripts | Prepared with AI; watch/defer position independently expressed by Oladapo in the recordings; no blanket assumption attestation inferred |
| Transcripts and timing | Supplied speech drafts compared with full local recognition; topic times corrected; harmless filler may be condensed, uncertain phrases noted separately |

## Failures, qualifications and recording evidence
The original inherited Python environment could not launch; the recorded clean run used a fresh no-pip environment. SEC direct retrieval returned 403; inspected source text and retrieval failures remain documented. Initial terminal mechanics were corrected; original outputs are preserved. The working-capital difference, current bridge, book/fair-value/lease claims, peer comparability, depreciation convention, stub timing and forecast assumptions remain limitations. No real fresh-eyes partner challenge is asserted without evidence.

Video 1 contains dated working pages; the recorded TA clarification and executed checks supersede their unresolved/not-run wording. The original receipt-linked PDF and supporting draft are preserved with provenance limits. Video 3 speaks to sensitivity, reverse DCF and peers, but sampled frames show summary tables; the manifest does not claim the detailed sections were visually expanded.

Videos measure 2:16.405, 4:08.768 and 4:41.240, within 3/5/5-minute limits. Screen samples show webcam and project evidence. Transcript topic times are approximate navigation markers, not word-level caption timings. ROIC terminology and the 5.02% computation are explained in separate editorial notes, with spoken claims preserved. The comparison is automated and not represented as human word-for-word certification.

Source scripts, immutable test evidence, ordinary output, original logs, recording metadata, reported guidance and clarifications accompany this package. Hosted links and instructional-team access must be completed in the manifest; missing external access is not resolved by preparing these documents.
'''

styles=getSampleStyleSheet()
styles.add(ParagraphStyle(name='Text',fontSize=9,leading=11.8,spaceAfter=6))
styles.add(ParagraphStyle(name='CellText',fontSize=7.8,leading=10))
styles['Heading1'].fontSize=17;styles['Heading1'].leading=20
styles['Heading2'].fontSize=11;styles['Heading2'].leading=14

def pdf(path,text):
    story=[]; lines=text.splitlines();i=0
    def p(t,style='Text'):
        t=html.escape(t)
        t=re.sub(r'\*\*(.*?)\*\*',r'<b>\1</b>',t)
        t=t.replace('`','')
        return Paragraph(t,styles[style])
    while i<len(lines):
        s=lines[i].strip()
        if s=='<!-- PAGE BREAK -->':story.append(PageBreak())
        elif s.startswith('|'):
            rows=[]
            while i<len(lines) and lines[i].startswith('|'):
                cells=[c.strip() for c in lines[i].strip('|').split('|')]
                if not all(re.fullmatch('[-: ]+',c) for c in cells): rows.append(cells)
                i+=1
            n=len(rows[0]); widths=[490/n]*n
            if n==3:widths=[105,178,207]
            if n==2:widths=[118,372]
            t=Table([[p(c,'CellText') for c in row] for row in rows],colWidths=widths,repeatRows=1)
            t.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('BACKGROUND',(0,0),(-1,0),colors.HexColor('#e7eef6')),('GRID',(0,0),(-1,-1),.3,colors.HexColor('#cbd5e1')),('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5)]))
            story.extend([t,Spacer(1,7)]);continue
        elif s.startswith('# '):story.append(p(s[2:],'Heading1'))
        elif s.startswith('## '):story.append(p(s[3:],'Heading2'))
        elif s:story.append(p(s))
        i+=1
    def footer(canvas,doc):
        canvas.setFont('Helvetica',7.5);canvas.drawString(55,25,NAME+' | FIN-43900 Project 1 | AI assistance disclosed');canvas.drawRightString(557,25,str(doc.page))
    SimpleDocTemplate(str(path),pagesize=(612,792),leftMargin=61,rightMargin=61,topMargin=40,bottomMargin=44,author=NAME,title=path.stem).build(story,onFirstPage=footer,onLaterPages=footer)

for name,text in [('Decision-Memo',memo),('Research-Evolution',research),('Validation-and-AI-Use',validation)]:
    (SOURCE/(name+'.md')).write_text(text,encoding='utf-8')
    pdf(OUT/(name+'.pdf'),text)
assert len(PdfReader(OUT/'Decision-Memo.pdf').pages)<=2,'Memo exceeds two pages'

original=ROOT/'recovery/edition-a-20261006/Edition-A-approved-redownload.pdf'
shutil.copy2(original,SUPPORT/'Edition-A-original-submitted.pdf')
shutil.copy2(ROOT/'recovery/edition-a-20261006/edition-a-draft-found-unchanged.md',SUPPORT/'Edition-A-preexisting-draft.md')
writer=PdfWriter()
writer.append(str(OUT/'Research-Evolution.pdf'))
writer.append(str(original))
writer.add_attachment('Edition-A-original-submitted.pdf',original.read_bytes())
temporary=OUT/'Research-Evolution-with-original.pdf'
with temporary.open('wb') as f:writer.write(f)
temporary.replace(OUT/'Research-Evolution.pdf')

for n in range(1,4):
    source=ROOT/f'docs/audio-check/transcript-video-{n}-audio-compared.txt'
    text=source.read_text(encoding='utf-8')
    start=text.index('[00:')
    body=text[start:]
    # Preserve spoken wording and separate notes; harmless filler is not claimed as exact.
    body=re.sub(r'- Exact timestamp alignment needs a word-level audio check before certification as a final verbatim transcript\.',
                '- Topic timestamps were compared with full local audio recognition and remain approximate.',body)
    body=body.replace('- The source audio rendering is not a verified word-level transcript. The major-topic timestamps are approximate and must be checked against playback for exact alignment.',
                      '- Full local audio recognition was compared with the supplied speech rendering. Topic times remain approximate; harmless filler may be condensed.')
    header=f'FIN-43900 PROJECT 1 - VIDEO {n}\nOladapo Olaniyan\nPrepared from the supplied speech draft and full local automated audio comparison. Topic timestamps are approximate; harmless filler may be condensed. Spoken finance slips are retained with separate correction notes. This is not a claim of independent human word-for-word certification.\n\n'
    (OUT/f'transcript-video-{n}.txt').write_text(header+body,encoding='utf-8')

for relative in ['docs/recording-clarifications-20261017.md','docs/staff-guidance-user-reported-v3-20261017.md','docs/audio-check/recording-check-report.md','docs/audio-check/recording-metadata.json']:
    shutil.copy2(ROOT/relative,SUPPORT/Path(relative).name)

# A project-only repository payload excludes the isolated transcription runtime,
# old PDF drafts, caches, and the large original recordings.
payload=OUT/'repository-package';payload.mkdir()
for folder in ['src','data','sources']:
    shutil.copytree(ROOT/folder,payload/folder,ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
shutil.copytree(ROOT/'outputs/final-working-run',payload/'outputs/final-working-run')
for folder in ['locked-change-20261015T1722CDT','cold-20261006T053603935700Z']:
    shutil.copytree(ROOT/'repro'/folder,payload/'repro'/folder,ignore=shutil.ignore_patterns('environment','__pycache__','*.pyc'))
(payload/'docs').mkdir()
for file in [*OUT.glob('*.pdf'),*OUT.glob('transcript-video-*.txt')]:shutil.copy2(file,payload/'docs'/file.name)
shutil.copytree(SUPPORT,payload/'docs/supporting-evidence')
shutil.copytree(SOURCE,payload/'docs/document-sources')
for file in ['assumption-challenges.md','peer-policy.md','recording-clarifications-20261017.md','staff-guidance-user-reported-v3-20261017.md']:
    shutil.copy2(ROOT/'docs'/file,payload/'docs'/file)
for file in ['requirements.txt','source-register-v3.csv']:
    shutil.copy2(ROOT/file,payload/file)
readme='''# PepsiCo valuation - Oladapo Olaniyan
FIN-43900 Project 1. Recorded recommendation: watch/defer initiation.
Market reference October 5, 2026; base $117.29 versus $125.65 price. All economic qualifications remain disclosed.

## View and run
Open outputs/final-working-run/visible-output.html for the preserved executed result.
Python 3.11+; model uses only the standard library, no credentials or network.
From this directory: python src/model.py
Each run creates a new output folder. Run checks are printed by the model; OPEN/QUALIFIED findings remain disclosed.
data/ holds facts and assumptions; src/model.py computes linked statements and FCFF/DCF/peers; src/checks.py supplies checks.
source-register-v3.csv and data/management-outlook-ledger.csv identify source dates, definitions and assumptions.
docs/ holds the PDFs, transcripts, AI disclosure, limitations, and recording clarification.
repro/ retains the separate ROIC experiment and historical cold-run evidence; historical absolute paths may reflect an earlier location.
The isolated local transcription environment and original Zoom recordings are deliberately outside this model package.

## Material limitations
42 PASS, 0 FAIL, 5 OPEN, 2 QUALIFIED is computational evidence, not blanket economic validation.
Bridge/share dates lag valuation date; working-capital scope, peer/claim conventions, seasonality and terminal ROIC remain qualified.
Actual fresh-eyes peer challenge evidence is not supplied. No unsupported personal or no-AI attestation is added.
Hosted repository/video URLs and instructional-team access must be completed in the manifest before submission.
'''
(payload/'README.md').write_text(readme,encoding='utf-8')

with (ROOT/'project1-manifest-working-v5.csv').open(encoding='utf-8-sig',newline='') as f:
    reader=csv.DictReader(f); columns=reader.fieldnames;rows=list(reader)
for row in rows:
    item=row['item']
    if item in ['Research-Evolution.pdf','Validation-and-AI-Use.pdf','Decision memo or deck']:
        row['location_or_url']={'Research-Evolution.pdf':'Research-Evolution.pdf','Validation-and-AI-Use.pdf':'Validation-and-AI-Use.pdf','Decision memo or deck':'Decision-Memo.pdf'}[item]
        row['notes']='Oladapo Olaniyan | Refreshed October 17; qualifications and recorded judgment disclosed. External submission/access pending.'
        row['access_checked']='Local PDF rendered and checked; external submission pending'
    elif item.startswith('Transcript Video '):
        n=int(item[-1]);row['location_or_url']=f'transcript-video-{n}.txt'
        row['title']=f'Oladapo Olaniyan - Video {n} corrected topic transcript'
        row['notes']='Supplied wording compared with full local audio recognition; topic times approximate; finance terminology/corrections separately noted; harmless filler may be condensed.'
        row['access_checked']='Local automated audio comparison; no human verbatim certification claimed'
    elif item=='Repository':
        row['location_or_url']='';row['notes']='Repository payload prepared in repository-package/. Existing course remote is https://github.com/Dapize-Mo/FIN43900-AI-Finance-Applications ; local project was untracked and not present in inspected origin/main tree. Upload/current hosted project/access pending.'
    elif item=='Visible executed output':row['location_or_url']='repository-package/outputs/final-working-run/visible-output.html'
    elif item=='Recording clarification addendum':row['location_or_url']='supporting-evidence/recording-clarifications-20261017.md'
    elif item=='Edition A recovery evidence':row['location_or_url']='supporting-evidence/staff-guidance-user-reported-v3-20261017.md'
    elif item=='Edition A receipt-linked artifact':row['location_or_url']='supporting-evidence/Edition-A-original-submitted.pdf'
    if item.startswith('Video '):row['notes']+=' Hosted share URL remains required.'
    if row['location_or_url'] and (OUT/row['location_or_url']).is_file():
        row['frozen_or_commit_id']='SHA256 '+hashlib.sha256((OUT/row['location_or_url']).read_bytes()).hexdigest()+' (prepared local file; submission receipt pending)'
with (OUT/'submission-manifest.csv').open('w',encoding='utf-8',newline='') as f:
    w=csv.DictWriter(f,fieldnames=columns);w.writeheader();w.writerows(rows)
shutil.copy2(OUT/'submission-manifest.csv',payload/'submission-manifest.csv')
for p in payload.rglob('*'):
    if p.is_file() and p.suffix=='.py':compile(p.read_text(encoding='utf-8-sig'),str(p),'exec')
hashes=[dict(path=p.relative_to(OUT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest(),bytes=p.stat().st_size) for p in OUT.rglob('*') if p.is_file()]
(OUT/'prepared-file-hashes.json').write_text(json.dumps(hashes,indent=2),encoding='utf-8')
with zipfile.ZipFile(OUT/'Oladapo-Olaniyan-Project1-Repository.zip','w',zipfile.ZIP_DEFLATED) as z:
    for p in payload.rglob('*'):
        if p.is_file():z.write(p,p.relative_to(payload))
(OUT/'START-HERE.txt').write_text('''Oladapo Olaniyan - FIN-43900 Project 1
LOCAL PACKAGE PREPARED; external access remains unfinished.

Brightspace attachments:
1. Research-Evolution.pdf
2. Decision-Memo.pdf (two-page maximum)
3. Validation-and-AI-Use.pdf
4. transcript-video-1.txt
5. transcript-video-2.txt
6. transcript-video-3.txt
7. submission-manifest.csv

Repository payload: repository-package/ or Oladapo-Olaniyan-Project1-Repository.zip.
Upload this payload to an accessible GitHub project location and add the exact URL to the manifest.
Upload the three Zoom videos as Unlisted/Public or approved Purdue equivalent; add share URLs and verify instructional-team access.
Enable captions; review finance terms, names and material numbers.
Confirm any assignment filename-prefix and instructor GitHub-access identity before submission.
Actual partner challenge evidence is missing and has not been invented. Other model qualifications remain disclosed.
The transcripts reflect an automated audio comparison; separate notes retain minor speech/recognition uncertainties. They do not certify every filler word.
No recordings need to be redone on the check evidence alone. Original media and historical artifacts remain preserved.
Nothing has been published, pushed or submitted by this preparation script.
''',encoding='utf-8')
print(json.dumps({'folder':str(OUT),'pages':{p.name:len(PdfReader(p).pages) for p in OUT.glob('*.pdf')},'repository_zip_bytes':(OUT/'Oladapo-Olaniyan-Project1-Repository.zip').stat().st_size},indent=2))
