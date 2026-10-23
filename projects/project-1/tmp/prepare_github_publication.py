"""Prepare the authorized Project 1 publication for Oladapo Olaniyan."""
from pathlib import Path
import csv, shutil
root=Path(__file__).resolve().parents[1]
out=root/'submission'
pkg=out/'repository-package'
url='https://github.com/Dapize-Mo/FIN43900-AI-Finance-Applications/tree/codex/project-1-submission/projects/project-1'
for p in [root/'project1-manifest-working-v5.csv',out/'submission-manifest.csv']:
    with p.open(encoding='utf-8-sig',newline='') as f:
        r=csv.DictReader(f); fields=r.fieldnames; rows=list(r)
    for row in rows:
        if row['item']=='Repository':
            row.update(location_or_url=url,access_checked='Publication prepared; remote verification pending',notes='Oladapo Olaniyan | Clean Project 1 payload on dedicated course-repository branch. Visible outputs and all three video links included.')
    with p.open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)
shutil.copy2(out/'submission-manifest.csv',pkg/'submission-manifest.csv')
p=pkg/'README.md'
s=p.read_text(encoding='utf-8').replace('Hosted repository/video URLs and instructional-team access must be completed in the manifest before submission.','The submission manifest contains the three Unlisted YouTube links with uploaded English captions. Independent logged-out video playback remains unchecked. Repository publication is on the dedicated codex/project-1-submission branch.')
s+='\n## Submission files\n\n[Research evolution](docs/Research-Evolution.pdf) | [Decision memo](docs/Decision-Memo.pdf) | [Validation and AI use](docs/Validation-and-AI-Use.pdf) | [Manifest](submission-manifest.csv)\n\n[Visible executed result](outputs/final-working-run/visible-output.md) includes the recorded model result without running code. Download the HTML file to view its formatted dashboard.\n'
p.write_text(s,encoding='utf-8')
target=root/'tmp/github-publication/projects/project-1'
shutil.copytree(pkg,target,ignore=shutil.ignore_patterns('__pycache__','*.pyc','.env'),dirs_exist_ok=True)
(target/'.gitignore').write_text('__pycache__/\n*.pyc\n.env\n',encoding='utf-8')
print(f'Prepared {sum(p.is_file() for p in target.rglob("*"))} files at {target}')
