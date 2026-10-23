"""Record verified public publication for Oladapo Olaniyan."""
from pathlib import Path
import csv,json,shutil,zipfile,hashlib
root=Path(__file__).resolve().parents[1]; out=root/'submission'; pkg=out/'repository-package'
commit='502de6a0dd020afe05911652dc7f5a4def5ce316'
base='https://github.com/Dapize-Mo/FIN43900-AI-Finance-Applications'
url=f'{base}/tree/{commit}/projects/project-1'
for path in [root/'project1-manifest-working-v5.csv',out/'submission-manifest.csv']:
    with path.open(encoding='utf-8-sig',newline='') as f:
        reader=csv.DictReader(f); fields=reader.fieldnames; rows=list(reader)
    for row in rows:
        if row['item']=='Repository':
            row.update(location_or_url=url,access_checked='2026-10-18: public README, three PDFs and visible output returned HTTP 200 without sign-in',frozen_or_commit_id=commit,notes='Oladapo Olaniyan | Published public snapshot; subsequent branch metadata updates do not alter this frozen snapshot.')
        if row['item']=='Visible executed output':
            row.update(location_or_url=f'{base}/blob/{commit}/projects/project-1/outputs/final-working-run/visible-output.md',access_checked='2026-10-18: public raw output returned HTTP 200 without sign-in')
    with path.open('w',encoding='utf-8',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=fields); writer.writeheader();writer.writerows(rows)
shutil.copy2(out/'submission-manifest.csv',pkg/'submission-manifest.csv')
(pkg/'.gitattributes').write_text('* -text\n',encoding='utf-8')
(pkg/'.gitignore').write_text('__pycache__/\n*.pyc\n.env\n',encoding='utf-8')
p=pkg/'README.md';s=p.read_text(encoding='utf-8').replace('Repository publication is on the dedicated codex/project-1-submission branch.','The repository is public on the codex/project-1-submission branch. README, PDFs and visible result were checked without sign-in on October 18, 2026. The manifest pins the frozen project snapshot.')
p.write_text(s,encoding='utf-8')
p=out/'START-HERE.txt';s=p.read_text(encoding='utf-8').replace('LOCAL PACKAGE PREPARED; external access remains unfinished.','PACKAGE AND PUBLIC REPOSITORY PREPARED; Brightspace submission remains unfinished.').replace('Upload this payload to an accessible GitHub project location and add the exact URL to the manifest.',f'Published repository snapshot: {url}\nPublic README, three PDFs and visible results checked without sign-in on October 18, 2026.').replace('No repository push or Brightspace submission has been made.','The repository package is published publicly. No Brightspace submission has been made.')
p.write_text(s,encoding='utf-8')
p=out/'PREPARATION-STATUS.md';s=p.read_text(encoding='utf-8').replace('The Git remote is https://github.com/Dapize-Mo/FIN43900-AI-Finance-Applications . Project files were untracked locally and absent from the inspected origin/main tree. The prepared payload has not been pushed; an accessible hosted project URL remains required.',f'The clean package is published publicly on codex/project-1-submission. Frozen snapshot: {url} . The README, three PDFs and visible result returned HTTP 200 without sign-in on October 18, 2026. Existing main-branch coursework was preserved.')
p.write_text(s,encoding='utf-8')
p=out/'package-checks.json';j=json.loads(p.read_text());j['external_access']='Public repository README, three PDFs and visible output checked without sign-in 2026-10-18. Three YouTube videos published Unlisted with captions; independent logged-out video playback unchecked.';j['repository_commit']=commit;p.write_text(json.dumps(j,indent=2),encoding='utf-8')
p=root/'README.md';s=p.read_text(encoding='utf-8');s=s.replace('Repository publication/access and remaining video access checks must still be completed before submission.','The clean repository package is published publicly on codex/project-1-submission; the submission manifest pins its frozen commit. Independent logged-out video playback and Brightspace submission remain pending.').replace('Hosted links/access checks, final transcript wording, and refreshed content-equivalent PDFs remain pending.','The current submission folder contains hosted video links, audio-compared transcripts and refreshed content-equivalent PDFs. Independent logged-out video playback remains pending.')
p.write_text(s,encoding='utf-8')
target=root/'tmp/github-publication/projects/project-1'
for rel in ['README.md','submission-manifest.csv','.gitattributes','.gitignore']:
    shutil.copy2(pkg/rel,target/rel)
with zipfile.ZipFile(out/'Oladapo-Olaniyan-Project1-Repository.zip','w',zipfile.ZIP_DEFLATED) as z:
    for p in pkg.rglob('*'):
        if p.is_file() and '__pycache__' not in p.parts and p.suffix!='.pyc': z.write(p,p.relative_to(pkg))
hashes=[dict(path=p.relative_to(out).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest(),bytes=p.stat().st_size) for p in out.rglob('*') if p.is_file() and p.name!='prepared-file-hashes.json']
(out/'prepared-file-hashes.json').write_text(json.dumps(hashes,indent=2),encoding='utf-8')
print('Updated manifests, README, preparation status, checks, ZIP and hashes with verified public snapshot.')
