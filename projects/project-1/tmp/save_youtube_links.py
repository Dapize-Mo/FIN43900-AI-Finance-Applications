"""Save only observed upload states for Oladapo Olaniyan; no publication action."""
from pathlib import Path
import csv,json,shutil,hashlib,zipfile
root=Path(__file__).resolve().parents[1]
out=root/'submission'
videos=[
 {'number':1,'id':'wvQGeS27rS4','title':'FIN 43900 Project 1 - Video 1: Research Evolution & AI Use - Oladapo Olaniyan','visibility':'Unlisted','published':True,'captions':'English (United States) by you saved','checks':'No issues found'},
 {'number':2,'id':'kUG0_Xe46so','title':'FIN 43900 Project 1 - Video 2: Model & Validation - Oladapo Olaniyan','visibility':'Unlisted','published':True,'captions':'English (United States) by you saved','checks':'No issues found'},
 {'number':3,'id':'GFaCDIIHAgg','title':'FIN 43900 Project 1 - Video 3: PepsiCo Committee Recommendation - Oladapo Olaniyan','visibility':'Unlisted','published':True,'captions':'English (United States) by you saved','checks':'No issues found'}]
(out/'youtube-upload-status.json').write_text(json.dumps(dict(analyst='Oladapo Olaniyan',videos=videos,logged_out_access='2026-10-18: fresh anonymous requests returned playabilityStatus OK and 15 adaptive stream formats for each correct video ID; no account cookies used. Privacy-enhanced direct embed encountered referrer error 153; anonymous watch-page player access passed.'),indent=2),encoding='utf-8')
for path in [root/'project1-manifest-working-v5.csv',out/'submission-manifest.csv']:
 with path.open(encoding='utf-8-sig',newline='') as f:
  reader=csv.DictReader(f);fields=reader.fieldnames;rows=list(reader)
 for row in rows:
  for video in videos:
   if row['item']==f'Video {video["number"]}':
    row['location_or_url']='https://youtu.be/'+video['id']
    row['title']=video['title']
    row['access_checked']=f'2026-10-18: anonymous player status OK, 15 stream formats; {video["visibility"]}; captions: {video["captions"]}'
    row['notes']=f'Oladapo Olaniyan | Provider YouTube; stable ID {video["id"]}; checks: {video["checks"]}. '+('Published as Unlisted with captions and topic index.' if video['published'] else 'Upload complete but browser interrupted before final caption/visibility settings; do not submit as accessible until confirmed.')
    if video['number']==3:row['notes']+=' Sensitivity/reverse DCF/peers are spoken; sampled screens show summary tables.'
  if row['item'] in ['Research-Evolution.pdf','Validation-and-AI-Use.pdf','Decision memo or deck'] and path.parent==out:
   row['duration_or_as_of']='Prepared 2026-10-17'
 with path.open('w',encoding='utf-8',newline='') as f:
  writer=csv.DictWriter(f,fieldnames=fields);writer.writeheader();writer.writerows(rows)
shutil.copy2(out/'submission-manifest.csv',out/'repository-package/submission-manifest.csv')
for file in out.glob('captions-video-*.srt'):shutil.copy2(file,out/'repository-package/docs'/file.name)
shutil.copy2(out/'youtube-upload-status.json',out/'repository-package/docs/youtube-upload-status.json')
with zipfile.ZipFile(out/'Oladapo-Olaniyan-Project1-Repository.zip','w',zipfile.ZIP_DEFLATED) as z:
 for p in (out/'repository-package').rglob('*'):
  if p.is_file():z.write(p,p.relative_to(out/'repository-package'))
hashes=[dict(path=p.relative_to(out).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest(),bytes=p.stat().st_size) for p in out.rglob('*') if p.is_file() and p.name!='prepared-file-hashes.json']
(out/'prepared-file-hashes.json').write_text(json.dumps(hashes,indent=2),encoding='utf-8')
print('Saved three published Unlisted links; updated working/submission manifests, archive, captions, and hashes.')
