"""Update the local recording manifest for Oladapo Olaniyan."""
from pathlib import Path
import csv
import hashlib
import json

root = Path(__file__).resolve().parents[1]
metadata = json.loads((root/'docs/audio-check/recording-metadata.json').read_text())
source = root/'project1-manifest-working-v4.csv'
target = root/'project1-manifest-working-v5.csv'
if target.exists():
    raise FileExistsError(target)
with source.open(encoding='utf-8-sig',newline='') as f:
    reader=csv.DictReader(f)
    columns=reader.fieldnames
    rows=list(reader)
index={r['item']:r for r in rows}
times={
    1:'00:02 opening/watch-defer; 00:20 Edition B/capex; 01:07 AI/checks; 01:30 ROIC test; 01:57 monitoring',
    2:'00:03 architecture; 00:24 FCFF; 00:59 assumptions; 01:31 results; 02:04 terminal value; 02:26 validation; 03:12 cold run; 03:45 closing',
    3:'00:03 decision; 00:35 scenarios; 01:05 FCFF/forecast; 02:13 downside; 02:50 sensitivity/reverse DCF (spoken); 03:23 peers (spoken); 04:04 committee ask'
}
titles={1:'Research evolution and AI output check',2:'Model architecture, finance and validation',3:'PepsiCo committee recommendation and live output'}
for number,record in enumerate(metadata,1):
    duration=record['video']['duration_seconds']
    minutes=int(duration)//60
    seconds=duration-minutes*60
    measured=f'{minutes:02d}:{seconds:06.3f}'
    v=index[f'Video {number}']
    v.update(location_or_url=record['video']['path'],title=f'Oladapo Olaniyan - {titles[number]}',
             duration_or_as_of=measured,timestamp_index=times[number],
             access_checked='Local file measured and audio processed; sampled frames checked; hosted URL/logged-out access pending',
             frozen_or_commit_id='SHA256 '+record['video']['sha256']+' (local identity; submission freeze pending)',
             notes='Oladapo Olaniyan | Recorded; keep. See docs/recording-clarifications-20261017.md. Topic times approximate; video hosting/access pending.')
    if number==3:
        v['notes']+=' Detailed sensitivity/reverse DCF/peers are narrated; sampled frames show summary tables, not expanded detailed sections.'
    t=index[f'Transcript Video {number}']
    transcript=root/f'docs/audio-check/transcript-video-{number}-audio-compared.txt'
    t.update(location_or_url=transcript.relative_to(root).as_posix(),title=f'Oladapo Olaniyan - Video {number} audio-compared transcript draft',
             duration_or_as_of=measured,timestamp_index=times[number],
             access_checked='Local draft exists; independent automated audio comparison completed; narrow wording review pending',
             frozen_or_commit_id='SHA256 '+hashlib.sha256(transcript.read_bytes()).hexdigest()+' (draft identity; not final freeze)',
             notes='Oladapo Olaniyan | Supplied speech wording retained with separate notes and revised approximate topic times. Final corrected transcript filename/wording pending; do not represent as human-certified verbatim.')
index['Research-Evolution.pdf'].update(
    title='Research evolution - dated-screen clarification recorded',
    notes='Oladapo Olaniyan | Retained PDF needs refresh. Current source docs/research-evolution-v3.md and docs/recording-clarifications-20261017.md record the reported TA resolution and spoken watch/defer judgment. Older screen/PDF unresolved wording is superseded; historical baseline report content is not invented.')
index['Validation-and-AI-Use.pdf']['notes']='Oladapo Olaniyan | Retained PDF needs refresh from docs/validation-and-ai-use-v3.md. Completed separate ROIC test and 42 PASS / 0 FAIL / 5 OPEN / 2 QUALIFIED evidence retained. Recording clarification supplements old screen; final disclosure/PDF equivalence and freeze pending.'
index['Decision memo or deck']['notes']='Oladapo Olaniyan | Retained working memo needs refresh to reflect recorded watch/defer committee ask. Recording does not establish acceptance of all assumptions or proposed $93.84 threshold. See docs/recording-clarifications-20261017.md; final PDF/freeze pending.'
index['Edition A recovery evidence']['notes']='Oladapo Olaniyan | Resolved under student-reported verbal TA clarification: copy acceptable if information is the same. See docs/staff-guidance-user-reported-v3-20261017.md. October 17 is documentation date, not an asserted date of the conversation. Original bytes and receipt evidence preserved.'
index['Edition A receipt-linked artifact']['notes']='Oladapo Olaniyan | Original error-page PDF preserved. Receipt 22599005 verifies submission, not report content. Reported TA resolution documented separately; no written staff message claimed.'
rows.append(dict.fromkeys(columns,''))
rows[-1].update(item='Recording clarification addendum',required='supporting evidence',
    location_or_url='docs/recording-clarifications-20261017.md',title='Oladapo Olaniyan - Recording clarifications and evidence index',
    duration_or_as_of='2026-10-17',access_checked='Local references checked',
    notes='Reconciles Video 1 dated working pages and Video 3 spoken-versus-visible evidence; supplements required PDFs, does not replace them.')
with target.open('w',encoding='utf-8',newline='') as f:
    writer=csv.DictWriter(f,fieldnames=columns);writer.writeheader();writer.writerows(rows)
for row in rows:
    location=row['location_or_url']
    if location and not location.startswith(('http://','https://')):
        p=Path(location)
        if not p.is_absolute(): p=root/p
        if not p.exists(): raise FileNotFoundError(p)
assert len([r for r in rows if r['item'].startswith('Video ')])==3
assert len([r for r in rows if r['item'].startswith('Transcript Video ')])==3
print(f'Created {target}; {len(rows)} rows; all populated local file paths exist; hosted links remain pending.')
