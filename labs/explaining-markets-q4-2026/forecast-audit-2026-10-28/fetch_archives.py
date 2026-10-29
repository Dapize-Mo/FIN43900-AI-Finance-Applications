"""Read official archives through existing Modal hosting - Oladapo Olaniyan."""
from pathlib import Path
import sys,json,hashlib,gzip,modal,httpx
from dotenv import dotenv_values
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'agent'))
from modal_app import image
app=modal.App('fin439-archive-audit')
@app.function(image=image,timeout=90,serialized=True)
def fetch(url):
 import urllib.request
 with urllib.request.urlopen(url,timeout=60) as response:return response.read()
if __name__=='__main__':
 cfg=dotenv_values(HERE.parent/'agent/.env')
 manifest=httpx.get('https://api.explainingmarkets.ai/v1/archive',headers={'X-API-Key':cfg['EM_API_KEY']},timeout=30);manifest.raise_for_status()
 sources=[]
 with app.run():
  for quarter in ['2026Q2','2026Q4']:
   item=next(x for x in manifest.json()['files'] if x['quarter']==quarter and x['event_type']=='EARNINGS_RELEASE')
   p=HERE/(quarter+'.jsonl.gz')
   data=fetch.remote(item['url'])
   records=[json.loads(x) for x in gzip.decompress(data).decode().splitlines() if x]
   if not p.exists():p.write_bytes(data)
   else:assert p.read_bytes()==data
   sources.append({'author':'Oladapo Olaniyan','quarter':quarter,'records':len(records),'sha256':hashlib.sha256(data).hexdigest(),'source':'https://api.explainingmarkets.ai/v1/archive','access_date':'2026-10-28','built_at':item.get('built_at')})
   print(quarter,'records',len(records),flush=True)
 (HERE/'sources-verified.json').write_text(json.dumps(sources,indent=2),encoding='utf-8')
