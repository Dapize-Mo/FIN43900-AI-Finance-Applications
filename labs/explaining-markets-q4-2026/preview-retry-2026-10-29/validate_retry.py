"""Frozen targeted prompt validation - Oladapo Olaniyan, FIN-43900."""
from pathlib import Path
import sys,json,gzip,random,hashlib,time,os
import numpy as np
from dotenv import dotenv_values
from openai import OpenAI
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'improvement-2026-10-23'))
import evaluate as engine
CANDIDATE_SYSTEM=engine.baseline.SYSTEM_PROMPT
MODEL='gemini-3.5-flash-lite'
def records_and_plan():
 records=[json.loads(x) for x in gzip.decompress((HERE/'2026Q4.jsonl.gz').read_bytes()).decode().splitlines() if x]
 eligible=[r for r in records if r.get('metrics',{}).get('earnings_surprise',{}).get('surprise_status')=='ok' and len(r.get('focal_assets',[]))==1 and r.get('disclosure',{}).get('items') and any(v.get('car1') is not None for v in r.get('event_returns',{}).values())]
 eligible.sort(key=lambda r:(r['event_datetime'],r['event_id']))
 chosen=sorted(random.Random(4392911).sample(eligible,32),key=lambda r:(r['event_datetime'],r['event_id']))
 plan={'author':'Oladapo Olaniyan','date':'2026-10-29','model':MODEL,'temperature':0,'n':32,'seed':4392911,'quarter':'2026Q4','candidate_sha256':hashlib.sha256((CANDIDATE_SYSTEM+' preview cap 16000').encode()).hexdigest(),'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'records':[{'event_id':r['event_id'],'event_datetime':r['event_datetime']} for r in chosen],'gate':'Candidate gain >=0.01, paired bootstrap 90% lower bound >0, paired coverage >=95%; otherwise retain original. No tuning or re-selection after evaluation.','limitations':['Exploratory Q4 sample comes from the same period used in the live audit; it is not an untouched confirmation set.','Historical model training contamination cannot be excluded.','Uniform calibration alone cannot improve OLS delta R squared.','Retry test uses the same previously examined Q4 sample and cached forecasts; exploratory, not independent confirmation. One bounded SDK retry; no production changes.']}
 p=HERE/'validation-plan.json'
 if p.exists():assert json.loads(p.read_text())==plan,'Frozen plan changed'
 else:p.write_text(json.dumps(plan,indent=2),encoding='utf-8')
 return records,chosen,plan

def main():
 all_records,chosen,plan=records_and_plan()
 if '--prepare' in sys.argv:
  print(json.dumps({'frozen_n':len(chosen),'candidate_sha256':plan['candidate_sha256'],'quarters':sorted(set(r['event_datetime'][:7] for r in chosen))}));return
 cfg=dotenv_values(HERE.parent/'agent/.env'); cache=HERE/'inferences.jsonl'
 rows=[json.loads(x) for x in cache.read_text().splitlines()] if cache.exists() else []
 done={(x['event_id'],x['method']) for x in rows if 'percentile'in x}
 errors=0;last_start=0
 with OpenAI(api_key=cfg['GEMINI_API_KEY'],base_url=engine.baseline.GEMINI_BASE_URL,timeout=45,max_retries=1) as client:
  for i,r in enumerate(chosen):
   for method in ['original','evidence']:
    if (r['event_id'],method) in done:continue
    old_limit=engine.baseline.PREVIEW_MAX_CHARS
    try:
     if method=='evidence':engine.baseline.PREVIEW_MAX_CHARS=16000
     system,user,schema=engine.build_inputs(r,'current')
    finally:engine.baseline.PREVIEW_MAX_CHARS=old_limit
    time.sleep(max(0,4.2-(time.monotonic()-last_start)));last_start=time.monotonic();start=last_start
    result={'event_id':r['event_id'],'method':method,'model':MODEL,'input_sha256':hashlib.sha256((system+user).encode()).hexdigest()}
    try:
     response=client.chat.completions.parse(model=MODEL,messages=[{'role':'system','content':system},{'role':'user','content':user}],response_format=schema,temperature=0)
     parsed=response.choices[0].message.parsed
     if parsed is None:raise ValueError('Missing structured forecast')
     result.update(percentile=parsed.predicted_percentile,seconds=round(time.monotonic()-start,3))
    except Exception as e:
     errors+=1;result.update(error=type(e).__name__,status_code=getattr(e,'status_code',None))
    with cache.open('a',encoding='utf-8') as f:f.write(json.dumps(result)+'\n')
    if result.get('status_code') in [401,403,429] or errors>=4:
     print('Stopped for provider error; successes retained:',json.dumps({k:result[k] for k in ('method','error','status_code') if k in result}),flush=True);return
   if (i+1)%8==0:print('Completed event pairs',i+1,'/32; errors',errors,flush=True)
 rows=[json.loads(x) for x in cache.read_text().splitlines()]
 values={(x['event_id'],x['method']):x['percentile'] for x in rows if 'percentile'in x}
 paired=[r for r in chosen if all((r['event_id'],m) in values for m in ['original','evidence'])]
 frame=engine.scorer.add_percentiles(engine.scorer.outcomes_frame(all_records))
 labels={(r.event_id,r.identifier_value):(r.y,r.surprise_pct) for r in frame.itertuples()}
 keys=[(r['event_id'],r['focal_assets'][0]['identifier_value']) for r in paired]
 y=np.array([labels[k][0] for k in keys]);s=np.array([labels[k][1] for k in keys]);b=np.array([values[(r['event_id'],'original')] for r in paired]);c=np.array([values[(r['event_id'],'evidence')] for r in paired])
 def score(pred):
  f=engine.scorer.outcomes_frame(paired);f['y']=y;f['surprise_pct']=s;f['candidate']=pred
  out=engine.scorer.score_submission(f,'candidate')
  return {k:v.item() if hasattr(v,'item') else v for k,v in out.items()}
 bm,cm=score(b),score(c)
 def delta(yy,ss,pp):
  def rs(x):
   fit=x@np.linalg.lstsq(x,yy,rcond=None)[0];return 1-np.sum((yy-fit)**2)/np.sum((yy-yy.mean())**2)
  x=np.column_stack([np.ones(len(yy)),ss]);return rs(np.column_stack([x,pp]))-rs(x)
 assert np.isclose(delta(y,s,b),bm['delta_r_squared_imputed'])
 assert np.isclose(delta(y,s,c),cm['delta_r_squared_imputed'])
 rng=np.random.default_rng(4392912);g=[]
 for _ in range(2000):
  i=rng.integers(0,len(y),len(y));g.append(delta(y[i],s[i],c[i])-delta(y[i],s[i],b[i]))
 interval=np.quantile(g,[.05,.95]).tolist();gain=cm['delta_r_squared_imputed']-bm['delta_r_squared_imputed'];coverage=len(paired)/32
 result={'author':'Oladapo Olaniyan','n':len(paired),'original':bm,'evidence':cm,'gain':gain,'paired_bootstrap_90pct':interval,'coverage':coverage,'gate_passed':bool(gain>=.01 and interval[0]>0 and coverage>=.95),'inference_errors':errors,'limitations':plan['limitations']}
 (HERE/'validation-results.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
 print(json.dumps(result,indent=2),flush=True)
if __name__=='__main__':main()
