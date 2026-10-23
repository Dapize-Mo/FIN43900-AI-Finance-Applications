"""AI-assisted reading and video preparation for Oladapo Olaniyan.

Reads executed outputs only. Preserves originals and refuses to overwrite outputs.
Does not author, design or execute the human-only changed-input prediction/test.
"""
from pathlib import Path
from datetime import datetime, timezone
import csv, hashlib, html, json
from collections import Counter

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.graphics.shapes import Drawing, Rect, Line, String
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'presentation'
NAME = 'Oladapo Olaniyan'
INPUTS = [ROOT / 'outputs/final-working-run/results.json',
          ROOT / 'outputs/final-working-run/forecast-statements.csv',
          ROOT / 'outputs/final-working-run/checks.csv',
          ROOT / 'data/assumptions.json', ROOT / 'data/filing-inputs.json']
hashes = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in INPUTS}
r = json.loads(INPUTS[0].read_text())
with INPUTS[1].open(newline='') as f:
    forecast = [x for x in csv.DictReader(f) if x['scenario'] == 'base']
price = r['bridge']['price']
styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name='GuideBody', fontName='Helvetica', fontSize=10.3,
                          leading=14.6, spaceAfter=8, textColor=colors.HexColor('#243747')))
styles.add(ParagraphStyle(name='GuideSmall', parent=styles['GuideBody'], fontSize=8.5, leading=11.5, spaceAfter=6))
styles.add(ParagraphStyle(name='GuideCell', parent=styles['GuideBody'], fontSize=8.9, leading=12, spaceAfter=0))
styles.add(ParagraphStyle(name='GuideHeadCell', parent=styles['GuideCell'], textColor=colors.white, fontName='Helvetica-Bold'))
styles['Heading1'].fontName = 'Helvetica-Bold'
styles['Heading1'].fontSize = 22
styles['Heading1'].leading = 26
styles['Heading1'].textColor = colors.HexColor('#12364a')
styles['Heading2'].fontSize = 12.5
styles['Heading2'].leading = 16
styles['Heading2'].textColor = colors.HexColor('#087b83')
story = []
md = []

def p(text, style='GuideBody'):
    story.append(Paragraph(html.escape(text), styles[style]))
    md.append(text + '\n')

def title(kicker, text, sub):
    if story:
        story.append(PageBreak())
        md.append('\n---\n')
    p(kicker.upper(), 'GuideSmall')
    story.append(Paragraph(html.escape(text), styles['Heading1']))
    md.append('# ' + text + '\n')
    p(sub)

def h(text):
    story.append(Paragraph(html.escape(text), styles['Heading2']))
    md.append('## ' + text + '\n')

def table(head, rows, widths):
    values = [[Paragraph(html.escape(str(x)), styles['GuideHeadCell']) for x in head]]
    values += [[Paragraph(html.escape(str(x)), styles['GuideCell']) for x in row] for row in rows]
    t = Table(values, colWidths=widths, repeatRows=1, hAlign='LEFT')
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#12364a')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor('#f0f5f7'), colors.white]),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LINEBELOW', (0, 0), (-1, -1), .3, colors.HexColor('#ccd9df')),
        ('LEFTPADDING', (0, 0), (-1, -1), 7), ('RIGHTPADDING', (0, 0), (-1, -1), 7),
        ('TOPPADDING', (0, 0), (-1, -1), 7), ('BOTTOMPADDING', (0, 0), (-1, -1), 7)]))
    story.extend([t, Spacer(1, 10)])
    md.append('| ' + ' | '.join(head) + ' |\n| ' + ' | '.join(['---'] * len(head)) + ' |\n')
    for row in rows:
        md.append('| ' + ' | '.join(str(x) for x in row) + ' |\n')

def link(label, url, description):
    story.append(Paragraph('<b>' + html.escape(label) + '</b> - ' + html.escape(description) +
                           '<br/><link href="' + html.escape(url, quote=True) + '" color="#087b83">Open source</link>', styles['GuideSmall']))
    md.append(f'[{label}]({url}) - {description}\n')

title('Read first / 1', 'PepsiCo: make your own recommendation',
      NAME + ' | FIN-43900 Project 1 | AI-assisted study guide | October 6, 2026')
p('Your current chosen action is BUY. The purpose of this guide is to help you decide whether the evidence supports it and explain your reasoning. It is a study aid, not your final two-page memo or a completed personal attestation.')
h('The company and the decision')
p('The fund has no current PEP position. Its choices are initiate, watch/defer, or do not initiate. PepsiCo and Coca-Cola are separate companies: Coke and Sprite belong to Coca-Cola; Pepsi and Starry belong to PepsiCo. PepsiCo also sells convenient foods. Competition extends beyond these two companies. [1, 2]')
h('Business quality and purchase price are different questions')
p('A business can grow and still be expensive. Valuation asks whether the cash it can generate is worth more than the price being paid, given risk. Positive growth alone does not establish an attractive entry price.')
case_rows = []
for key, label in [('low','Low'),('base','Base'),('high','High'),('value_reset_failure','Value Reset Failure')]:
    value = r['scenarios'][key]['value_per_diluted_share']
    case_rows.append([label, f'${value:.2f}', f'{(value / price - 1) * 100:+.1f}%'])
table(['Executed case', 'Model value/share', 'Value vs. $125.65'], case_rows, [190, 135, 179])
p('The comparison is a model-value gap, not a promised stock return; it excludes dividends, time and probabilities. These are conditional scenario values, not a confidence interval. Prices/values are USD per diluted-proxy share. The price observation is October 5; balance-sheet claims are dated June 13 and point shares July 2.')
d = Drawing(504, 92)
scale = 2.18
for i, (key, label) in enumerate([('low','Low'),('base','Base'),('high','High')]):
    y = 69 - i * 25
    value = r['scenarios'][key]['value_per_diluted_share']
    d.add(String(0, y + 4, label, fontName='Helvetica', fontSize=9, fillColor=colors.HexColor('#243747')))
    d.add(Rect(55, y, value * scale, 15, fillColor=colors.HexColor('#087b83'), strokeColor=None))
    d.add(String(50 + value * scale, y + 4, f'${value:.2f}', fontName='Helvetica-Bold', fontSize=9,
                 fillColor=colors.white, textAnchor='end'))
d.add(Line(55 + price * scale, 10, 55 + price * scale, 89, strokeColor=colors.HexColor('#c76b22'), strokeWidth=1.5))
d.add(String(55 + price * scale + 4, 87, 'Dated price $125.65', fontName='Helvetica', fontSize=8, fillColor=colors.HexColor('#a45215')))
story.append(d)

title('Understand the engine / 2', 'How the forecast becomes a value', 'Read this before rehearsing the code or committee video.')
table(['Statement', 'What it does', 'How it connects'], [
    ['Income statement', 'Sales less costs produces operating profit and net income.', 'Sales, margins, depreciation and interest flow from drivers/schedules.'],
    ['Balance sheet', 'Tracks assets, debt, operating liabilities and equity.', 'Capital spending/depreciation roll assets; retained earnings and payouts roll equity.'],
    ['Cash flow', 'Shows operating, investing and financing cash movements.', 'Opening cash plus cash change must equal closing balance-sheet cash.']
], [105, 193, 206])
h('Five-year base forecast - executed, not company guidance')
table(['Fiscal year', 'Revenue', 'EBIT', 'FCFF'], [[x['year'], f"{float(x['revenue']):,.0f}", f"{float(x['ebit']):,.0f}", f"{float(x['fcff']):,.0f}"] for x in forecast], [105, 133, 133, 133])
p('Figures above are USD millions. Simplified accounts can balance mathematically while the forecast economics remain uncertain; frozen accounts and financing assumptions are disclosed.')
h('FCFF: cash available to all capital providers')
p('FCFF = EBIT x (1 - tax rate) + depreciation/amortization - capital spending - increase in operating working capital. EBIT is operating profit. NOPAT is EBIT after operating tax. More receivables or inventory generally ties up cash. Borrowing and dividends are financing items, outside FCFF.')
h('DCF and the enterprise-to-equity bridge')
p('Discount forecast FCFF and continuing value at WACC. Then add qualifying cash/investments and subtract debt and other claims to reach common equity value. Divide by the stated diluted-share proxy. The dates and definitions of every bridge item matter.')
b = r['bridge']; base = r['scenarios']['base']
p(f"Executed bridge (USD billions, rounded): enterprise value {base['enterprise_value']/1000:.2f} + cash/STI {(b['cash']+b['sti'])/1000:.2f} + affiliate book proxy {b['nonoperating_assets']/1000:.2f} - debt {b['debt']/1000:.2f} - NCI {b['nci']/1000:.2f} = common equity {base['common_equity_value']/1000:.2f}. Dividing by {b['diluted_shares']:,.2f} million proxy shares yields ${base['value_per_diluted_share']:.2f}.")

title('Read the evidence / 3', 'What supports buying - and what challenges it', 'Keep facts, management expectations and your own forecast separate.')
table(['Evidence', 'What it supports', 'What it does not prove'], [
    ['Q2 2026 reported revenue +6.4%; organic revenue +2.4%. [3]', 'Growth is present; acquisitions and FX explain part of reported growth.', 'That all growth is recurring, or that the stock is cheap.'],
    ['Q2 core EPS +4%; core operating margin down 40 basis points. [3]', 'Underlying earnings grew, with pressure on profitability.', 'Broad improvement in every business or margin.'],
    ['Management FY2026 outlook: organic growth 2-4%; core constant-currency EPS growth 4-6%. [3]', 'A disclosed starting point for near-term expectations.', 'Guaranteed results or five-year guidance.'],
    ['Strong brand portfolio and distribution described by the company. [1]', 'A business thesis worth testing against volumes, pricing and cash.', 'A company-wide duopoly or permanent pricing power.'],
    ['Qualified peer multiples imply values above DCF.', 'A reason to investigate valuation-method disagreement.', 'Permission to average methods or choose only the highest result.']
], [171, 165, 168])
h('Four assumptions that can change the answer')
table(['Working convention', 'Why it matters'], [
    [f"WACC {base['wacc']*100:.2f}%", 'Higher required returns lower DCF value. Beta, equity risk premium and debt spread remain assumptions.'],
    ['Terminal growth 2.5%; incremental ROIC 15%', 'Continuing growth requires reinvestment. Both long-run inputs need economic support.'],
    [f"Terminal PV {base['terminal_value_share']*100:.1f}% of enterprise value", 'Most base value lies beyond the explicit five years, making long-run economics consequential.'],
    ['FY2025 EBIT 11,498 + impairment 1,993 = normalized 13,491', 'The add-back removes an accounting charge, but does not restore damaged brand economics. USD millions.']
], [186, 318])
p('Remaining qualifications include an $802 million working-capital definition difference, dated debt/cash/share inputs, book investment/NCI proxies, dilution and financing assumptions, and only two qualified peers. Recorded tests: 42 PASS, 0 FAIL, 5 OPEN, 2 QUALIFIED; these do not certify the assumptions.')
p('Q3 results are scheduled for October 8. As of this October 6 guide they are not released. Consider that release before finalizing; no future results have been inferred. [4]', 'GuideSmall')

title('Your judgment / 4', 'Build a recommendation you can defend', 'This worksheet is for ordinary committee reasoning. It is not the locked changed-input prediction.')
p('Start by reconciling your chosen BUY action with the base value being below the dated market price. You may disagree with the working model, but show evidence for that disagreement. Do not adjust assumptions solely to obtain a buy result.')
table(['Committee action', 'What your evidence must establish'], [
    ['Initiate / BUY', 'Why value, price and downside exposure justify starting a position; specify size/conditions yourself.'],
    ['Watch/defer', 'What price or verified operating evidence would make initiation justified, and when to reassess.'],
    ['Do not initiate', 'Which structural or cash/funding risk defeats the thesis, and what would reverse that view.']
], [139, 365])
for head, prompt in [
    ('1. My action and scope', 'Initiate, watch/defer or do not initiate? Horizon and proposed allocation, if any?'),
    ('2. Strongest evidence', 'Which dated facts support my action? Which figures are only management or model expectations?'),
    ('3. Price, value and the counterargument', 'Why does my action follow from the range and price? What is the strongest case against it?'),
    ('4. Conditions and reversal', 'What would invalidate my view? What will I monitor, over what window, and who owns that review?')]:
    h(head);p(prompt);p('My response: ______________________________________________________________', 'GuideSmall')
p('A final recommendation needs a range, dated evidence, conditions, reversal/monitoring triggers and a clear committee ask. Your proposed allocation and monitoring thresholds are still blank. This guide supplies no personal experience or completed partner challenge.')
p('Separate mandatory task: write/freeze the human-only prediction independently with AI off before its test is designed or run; execute that test with AI closed. No input, prediction or test is proposed here. Ordinary model checks cannot replace it.', 'GuideSmall')

title('Video preparation / 5', 'Videos 1 and 2: demonstrate ownership', 'These are planning budgets, not recorded timestamps. The shared course instructions set the hard limits. [5, 6]')
h('Video 1 - research evolution and an AI-output check | maximum 3:00')
table(['Planned time', 'Show', 'Explain in your own words'], [
    ['0:00-0:25', 'Target and current research position.', 'The committee question and what changed in your thinking.'],
    ['0:25-1:05', 'Approved error-page Edition A and recovery record; current B.', 'You report permission to use the unchanged error PDF. Actual A report content is unavailable; do not invent an A-to-B comparison.'],
    ['1:05-2:15', 'The documented AI capital-spending source claim and primary evidence.', 'Note 1 p68: segment 4,192 + corporate 223 = total 4,415. Explain the correction from the earlier wrong locator/segment-total claim.'],
    ['2:15-2:50', 'Your own disposition and research decision.', 'What you accepted, qualified, corrected or rejected, and why the evidence was sufficient.']
], [79, 210, 215])
p('Open: presentation/Research-Evolution-review.pdf; sources/pep-capex-reconciliation.md; docs/validation-and-ai-use-v3.md; docs/staff-guidance-user-reported-v2-20261006.md. Read the record before claiming an AI mistake or personal discovery.', 'GuideSmall')
h('Video 2 - code, finance and validation | maximum 5:00')
table(['Planned time', 'Show', 'Explain'], [
    ['0:00-0:35', 'Repository and RUNME.md.', 'Where sources, assumptions, model, checks and output live.'],
    ['0:35-2:30', 'data inputs -> src/model.py -> statements/FCFF/DCF.', 'One connected calculation, financing outside FCFF, and the equity bridge.'],
    ['2:30-3:45', 'src/checks.py and recorded checks.csv.', 'The ordinary cash-articulation corruption check and known-answer check; their actual evidence and limits.'],
    ['3:45-4:45', 'Cold-run evidence and visible output.', 'Fresh-environment results match the output; show how a clean user reproduces it and one unresolved risk.']
], [79, 210, 215])
p('Cold-run evidence: repro/cold-20261006T053603935700Z/cold-run-evidence.json. Ordinary reproduction command from project folder: python src/model.py. It creates a new output folder. This command is not the human locked test.', 'GuideSmall')

title('Committee defense / 6', 'Video 3: defend the decision with the product', 'Maximum 5:00. The live product demonstration is the main delivery; a slide-only or README-only tour is insufficient. [5, 6]')
table(['Planned time', 'On screen', 'Your purpose'], [
    ['0:00-0:30', 'Dashboard and memo.', 'State your chosen action, horizon and range; explain who decides.'],
    ['0:30-1:25', 'Price, low/base/high values and evidence dates.', 'Reconcile the recommendation with the below-price base case.'],
    ['1:25-2:20', 'Scenario output and named downside.', 'Trace operating weakness through cash, borrowing and value; state the effect on your action.'],
    ['2:20-3:20', 'WACC/g sensitivity, terminal share and reverse DCF.', 'Explain why long-run assumptions matter. Reverse DCF is one conditional price-implied path, not a unique market belief.'],
    ['3:20-4:15', 'Peer comparisons and limitations.', 'Explain method disagreement and what you have qualified.'],
    ['4:15-4:45', 'Your conditions and committee ask.', 'State monitoring, reversal trigger and the action you want approved.']
], [79, 210, 215])
h('Open the visible product')
p('Open presentation/Dashboard-review.html in your browser. Keep the memo and the executed CSVs available. This display copy formats case labels and years; its financial results are unchanged. For model inputs and complete output, use outputs/final-working-run/.')
h('Questions to rehearse aloud')
for question in [
    'Why BUY when your base model value is below the dated market price?',
    'Which evidence supports your most consequential assumption, and what challenges it?',
    'Why is terminal value about 80% of enterprise value?',
    'Why do peer multiples imply more value than the DCF, and which comparison is most qualified?',
    'What does Value Reset Failure mean for cash/funding and your committee action?']:
    p('- ' + question)
p('Use your own answers. Keep any uncompleted conditions visibly unfinished until you decide them. Do not present the current watch/defer AI draft memo as an already-finished BUY memo; align it with your defended judgment before recording the final version.', 'GuideSmall')

title('Recording workflow / 7', 'Make three clear recordings', 'Screen + your voice + a small webcam view. Clear evidence and audio matter more than production polish. [6]')
h('An optional Windows route: Clipchamp')
p('If Clipchamp is available, open a video project and use Record & create, then the screen-and-camera option. Choose the microphone and camera, and allow the permissions you intend to use. Select the window/screen containing your evidence. Make a short practice recording; replay it to check audio, text size and webcam placement. Microsoft documents these controls. [7]')
p('Record the three videos separately. Keep the webcam away from figures and code. Close unrelated windows and notifications. Export local video files and verify each final duration and the opening/ending audio. Leave time under each cap; the outline targets 2:50 / 4:45 / 4:45.')
h('YouTube and corrected transcripts')
p('The course allows separate Unlisted or Public links, never Private, or an approved Purdue-hosted equivalent. Unlisted YouTube videos can be watched without a Google account by anyone with the link, and that link can be reshared. Set visibility deliberately when you choose to upload. No upload is performed here. [6, 8]')
p('After recording, start with actual platform captions/transcript. Correct finance terms, PEP/KO/MDLZ, your name, speaker attribution, and material numbers against the final evidence. YouTube Studio permits caption editing. Save a corrected plain-text transcript for each video; captions alone do not replace those files. [6, 9]')
h('Suggested local filenames - create only after real recording')
table(['Video', 'Working recording name', 'Required transcript'], [
    ['1', 'Oladapo_Olaniyan_P1_Video1_Research.mp4', 'docs/transcript-video-1.txt'],
    ['2', 'Oladapo_Olaniyan_P1_Video2_Model.mp4', 'docs/transcript-video-2.txt'],
    ['3', 'Oladapo_Olaniyan_P1_Video3_Committee.mp4', 'docs/transcript-video-3.txt']
], [44, 258, 202])
p('Confirm the official submission filename prefix before final naming. Record actual titles, measured durations, URLs and timestamp indices in the manifest. Test all links logged out and keep access through the grade-appeal window. Freeze mutually consistent videos, transcripts, memo, output and validation records. [6]')
p('I can help with cue cards, rehearsal questions, factual checks and transcript corrections from actual recordings. You supply your voice, face, judgment and real evidence. There are no recordings, measured durations or completed transcripts in this guide.', 'GuideSmall')

title('Evidence and next steps / 8', 'Sources, boundaries and completion', 'Primary sources and local executed output; accessed or rechecked October 6, 2026.')
link('[1] PepsiCo FY2025 SEC Form 10-K', 'https://www.sec.gov/Archives/edgar/data/77476/000007747626000007/pep-20251227.htm',
     'Year ended December 27, 2025. Item 1 brands/competition pp5-7; income p57; cash flow pp59-60; Note 1 capital spending p68. Filing facts; USD millions where shown.')
link('[2] Coca-Cola FY2025 SEC Form 10-K', 'https://investors.coca-colacompany.com/filings-reports/all-sec-filings/content/0001628280-26-010047/ko-20251231.htm',
     'Year ended December 31, 2025. Item 1 business/brands: Coke and Sprite ownership; ownership is distinct from distribution.')
link('[3] PepsiCo Q2 2026 earnings release', 'https://www.sec.gov/Archives/edgar/data/77476/000007747626000037/q220268-kxexhibit991.htm',
     '12 weeks ended June 13, 2026. Results/discussion pp1-2; guidance p5; growth in percent, margin changes in basis points. Organic/core measures are non-GAAP; guidance is expectation.')
link('[4] PepsiCo Q3 reporting schedule', 'https://www.pepsico.com/en/newsroom/press-releases/2026/pepsico-announces-timing-and-availability-of-third-quarter-2026-financial-results',
     'Announces October 8 release for the quarter ending September 5. Schedule only; no Q3 results claimed.')
link('[5] Live Brightspace Project 1', 'https://purdue.brightspace.com/d2l/lms/dropbox/user/folder_submit_files.d2l?db=1581848&grpid=0&isprv=0&bp=0&ou=1636012',
     'Read live October 6. Individual 300 points; due October 19 at 11:59 PM Eastern. Controls assignment requirements and deadlines.')
link('[6] Shared course submission architecture', 'https://github.com/CinderZhang/FIN43900-Fall2026/blob/main/PROJECT-SUBMISSION-ARCHITECTURE.md',
     'Local fetched course copy, sections 4-7 and video/access rules. Video purposes, 3/5/5 limits, webcam, corrected transcript and access requirements.')
link('[7] Microsoft Clipchamp recording controls', 'https://support.microsoft.com/en-us/clipchamp/how-to-enable-and-change-camera-and-microphone-settings-in-the-clipchamp-windows-app',
     'Record & create and camera/microphone controls; optional recording route, not a claim that it is installed or tested on this device.')
link('[8] YouTube privacy settings', 'https://support.google.com/youtube/answer/157177?hl=en', 'Unlisted versus Private/Public and link access. No upload/access check performed.')
link('[9] YouTube caption editing', 'https://support.google.com/youtube/answer/2734705?hl=en', 'Editing captions after actual recording; does not establish a completed transcript.')
h('Local evidence and what remains')
p('Model figures: outputs/final-working-run/results.json and forecast-statements.csv, as-of October 5; checks.csv records executed computational tests. data/assumptions.json separates unapproved assumptions. source-register-v3.csv and data/management-outlook-ledger.csv retain input definitions, periods, units, locators and qualifications.', 'GuideSmall')
p('Current permission: docs/staff-guidance-user-reported-v2-20261006.md records your permission report for the original error-page Edition A PDF. Use manifest v4; earlier permission-uncertainty statements are historical. The report contents are still unavailable. No recovered draft is silently substituted.', 'GuideSmall')
p('Finish: defend/align your recommendation and conditions; close or explicitly qualify financial gaps; supply a real fresh-eyes challenge; complete the human-only task separately; record videos/correct transcripts; verify repository/link access and filename prefix; freeze the consistent bundle. This guide does not make the project submission-ready.', 'GuideSmall')

pdf = OUT / 'PEP-Recommendation-and-Video-Guide-v3.pdf'
markdown = OUT / 'PEP-Recommendation-and-Video-Guide-v3.md'
review = OUT / 'reading-guide-review-v3.json'
for path in [pdf, markdown, review]:
    if path.exists():
        raise FileExistsError(path)
with markdown.open('x', encoding='utf-8') as f:
    f.write('# ' + NAME + ' - Project 1 reading and video guide\n\n' + '\n'.join(md))

def footer(c, doc):
    c.setStrokeColor(colors.HexColor('#ccd9df')); c.line(48, 39, 564, 39)
    c.setFont('Helvetica', 7.4); c.setFillColor(colors.HexColor('#52616b'))
    c.drawString(48, 27, NAME + ' | AI-assisted study guide | Model as-of Oct 5, 2026')
    c.drawRightString(564, 27, f'{doc.page}')

SimpleDocTemplate(str(pdf), pagesize=(612, 792), leftMargin=48, rightMargin=48,
                  topMargin=42, bottomMargin=51, title='PEP Recommendation and Video Guide - '+NAME,
                  author=NAME).build(story, onFirstPage=footer, onLaterPages=footer)
reader = PdfReader(pdf)
pages = [x.extract_text() or '' for x in reader.pages]
assert len(pages) == 8, f'Expected 8 pages, got {len(pages)}'
assert all(NAME in x for x in pages)
for phrase in ['$117.29', '$125.65', '42 PASS', '3:00', '5:00', 'October 19', 'AI closed']:
    assert phrase in '\n'.join(pages), phrase
assert all(hashlib.sha256(p.read_bytes()).hexdigest() == hashes[str(p.relative_to(ROOT))] for p in INPUTS)
record = {'student': NAME, 'created_utc': datetime.now(timezone.utc).isoformat(),
          'guide_pages': len(pages), 'input_hashes': hashes, 'inputs_unchanged': True,
          'finance_model_rerun': False, 'visual_review': 'Pending rendered-page review',
          'preserved_first_failure': 'Initial nine-page PDF/Markdown retained; worksheet note spilled onto its own page. Worksheet reorganized to keep eight pages; no financial model values changed.',
          'preserved_visual_issue': 'v2 price-reference line intersected an outside bar-value label. v3 places value labels inside the bars; v2 retained.',
          'worksheet': 'Blank ordinary committee reasoning; no locked prediction or test supplied',
          'video_status': 'Outlines only; no recordings, transcripts, actual timestamps or uploads',
          'authoring': 'AI-assisted guide, source research and layout; student owns recommendation',
          'created': [str(pdf), str(markdown), str(review), str(Path(__file__))]}
with review.open('x', encoding='utf-8') as f:
    json.dump(record, f, indent=2)
print(json.dumps({'pages':len(pages), 'inputs_unchanged':True, 'pdf':str(pdf)}))
