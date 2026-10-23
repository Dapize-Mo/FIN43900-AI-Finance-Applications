"""Save verified corrected submission evidence for Oladapo Olaniyan."""
from pathlib import Path
import hashlib,json
root=Path(__file__).resolve().parents[1]
out=root/'submission/corrected-20261018'
names=['Research-Evolution.pdf','Decision-Memo.pdf','Validation-and-AI-Use.pdf','transcript-video-1.txt','transcript-video-2.txt','transcript-video-3.txt','submission-manifest.csv']
record=dict(analyst='Oladapo Olaniyan',assignment='Project 1 — Corporate Finance Application — Single Assignment',submission_id='23393677',supersedes='23393007',displayed_submission_date='Oct 18, 2026 10:24 AM',timezone='America/Indianapolis',status='File submission successful',files=[dict(name=n,bytes=(out/n).stat().st_size,sha256=hashlib.sha256((out/n).read_bytes()).hexdigest()) for n in names],correction='Credits confirmed Kenechukwu Ogbuefi Lab 10 SG&A challenge; original recordings and financial outputs preserved')
(out/'submission-receipt.json').write_text(json.dumps(record,indent=2),encoding='utf-8')
summary='Oladapo Olaniyan | FIN-43900 Project 1\nCorrected final submission successful: 23393677, October 18, 2026 at 10:24 AM (America/Indianapolis).\nThis seven-file bundle supersedes 23393007. The peer-review evidence is credited; financial outputs and recordings are preserved.\nSee submission-receipt.json and brightspace-submission-23393677.png.\n'
(out/'FINAL-SUBMISSION-STATUS.txt').write_text(summary,encoding='utf-8')
(root/'submission/CURRENT-SUBMISSION.txt').write_text(summary+'Current files and receipt: corrected-20261018/\nEarlier files remain preserved as historical versions.\n',encoding='utf-8')
for rel in ['START-HERE.txt','PREPARATION-STATUS.md']:
    p=out/rel;s=p.read_text(encoding='utf-8')
    if 'CORRECTED FINAL RECEIPT 23393677' not in s:s='CORRECTED FINAL RECEIPT 23393677 | October 18, 2026 10:24 AM | Seven files submitted successfully.\nSee FINAL-SUBMISSION-STATUS.txt. Earlier receipt references below are preserved history.\n\n'+s
    p.write_text(s,encoding='utf-8')
p=out/'package-checks.json';j=json.loads(p.read_text());j['brightspace_submission_id']='23393677';j['corrected_submission']='Seven files confirmed, October 18, 2026 10:24 AM; confirmed Lab 10 peer evidence included';p.write_text(json.dumps(j,indent=2),encoding='utf-8')
hashes=[dict(path=p.relative_to(out).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest(),bytes=p.stat().st_size) for p in out.rglob('*') if p.is_file() and p.name!='prepared-file-hashes.json']
(out/'prepared-file-hashes.json').write_text(json.dumps(hashes,indent=2),encoding='utf-8')
assert all((out/f['name']).stat().st_size==f['bytes'] for f in record['files'])
print('Saved corrected receipt 23393677, seven submitted-file hashes and current-package pointer.')
