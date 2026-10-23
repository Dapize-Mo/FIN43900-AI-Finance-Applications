"""Final rendering correction/check record for Oladapo Olaniyan."""
from pathlib import Path
import csv,hashlib,json
import render_review as r
import build_packet as b
from pypdf import PdfReader
ROOT=r.ROOT; OUT=r.OUT
parts=[r.dashboard()]
for relative in ['docs/continuation-audit.md','docs/assumption-challenges.md','docs/peer-policy.md','docs/video-preparation.md','RUNME.md','docs/completion-report.md']:
    parts.extend(['<!-- PAGE BREAK -->',r.clean((ROOT/relative).read_text(encoding='utf-8'))])
notes='\n\n'.join(parts)
b.write_new(OUT/'Supporting-Notes-review-v2.md',notes)
b.pdf_from_md(OUT/'Supporting-Notes-review-v2.pdf',notes,'Project 1 Supporting Review - Oladapo Olaniyan')
expected='F745E7EA27A1445830573029A77D28967A1E4F5E53A9BA9A794079373F35464F'
text=''.join(page.extract_text() for page in PdfReader(OUT/'Supporting-Notes-review-v2.pdf').pages)
assert expected in text,'Preserved Edition A hash must remain intact in rendered output'
record=json.loads((OUT/'render-review-record.json').read_text())
record.update(supporting_notes_current='Supporting-Notes-review-v2.pdf',supporting_hash_text_intact=True,
    dashboard_visual='Main view inspected in browser; case labels and years corrected without financial changes',
    formatting_failure='Initial prose spacing broke one unseparated hash; protected hash regex corrected; initial review copy preserved',
    source_hashes_still_match=all(hashlib.sha256(Path(row['source']).read_bytes()).hexdigest()==row['source_sha256'] for row in record['files']),
    main_pdf_visual='All six main-PDF pages inspected; no clipping/overlap; memo two pages',
    supporting_pdf_visual='Initial12 pages inspected; corrected hash version pending final inspection')
b.write_new(OUT/'render-review-record-final.json',json.dumps(record,indent=2))
print(json.dumps(record,indent=2))
