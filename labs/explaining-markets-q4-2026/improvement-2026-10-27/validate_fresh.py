"""Fresh frozen blend validation — Oladapo Olaniyan, FIN-43900."""
from pathlib import Path
import sys,json,gzip,random,hashlib,time,threading,concurrent.futures
import numpy as np
from dotenv import dotenv_values
from openai import OpenAI
HERE=Path(__file__).resolve().parent
PREVIOUS=HERE.parent/'improvement-2026-10-23'
sys.path.insert(0,str(PREVIOUS))
import evaluate as engine
MODEL=engine.MODEL
LOCK=threading.Lock(); RATE=threading.Lock(); NEXT=0.0

def sample():
    all_records=[json.loads(x) for x in gzip.decompress((PREVIOUS/'sources/EARNINGS_RELEASE_2026Q3.jsonl.gz').read_bytes()).decode().splitlines() if x]
    eligible=[r for r in all_records if r.get('metrics',{}).get('earnings_surprise',{}).get('surprise_status')=='ok' and len(r.get('focal_assets',[]))==1 and r.get('disclosure',{}).get('items') and any(v.get('car1') is not None for v in r.get('event_returns',{}).values())]
    eligible.sort(key=lambda r:(r['event_datetime'],r['event_id']))
    prior={x['event_id'] for x in json.loads((PREVIOUS/'evaluation-plan.json').read_text())['records']}
    pool=[r for r in eligible[int(len(eligible)*.65):] if r['event_id'] not in prior]
    return sorted(random.Random(43927).sample(pool,96),key=lambda r:(r['event_datetime'],r['event_id']))

def run(job,cfg):
    global NEXT
    r,method=job
    with RATE:
        delay=max(0,NEXT-time.monotonic())
        if delay:time.sleep(delay)
        NEXT=time.monotonic()+4.2
    system,user,schema=engine.build_inputs(r,method)
    result={'event_id':r['event_id'],'method':method,'input_sha256':hashlib.sha256((MODEL+system+user).encode()).hexdigest()}
    start=time.monotonic()
    with OpenAI(api_key=cfg['GEMINI_API_KEY'],base_url=engine.baseline.GEMINI_BASE_URL,timeout=45,max_retries=0) as client:
        try:
            response=client.chat.completions.parse(model=MODEL,messages=[{'role':'system','content':system},{'role':'user','content':user}],response_format=schema,temperature=0)
            parsed=response.choices[0].message.parsed
            if parsed is None:raise ValueError('No structured forecast')
            result.update(percentile=parsed.predicted_percentile,seconds=round(time.monotonic()-start,3))
        except Exception as exc:result.update(error=type(exc).__name__,status_code=getattr(exc,'status_code',None))
    with LOCK:
        with (HERE/'results/inferences.jsonl').open('a',encoding='utf-8') as f:f.write(json.dumps(result)+'\n')
    return result

def main():
    records=sample()
    plan={'author':'Oladapo Olaniyan','date':'2026-10-27','n':96,'seed':43927,'model':MODEL,'temperature':0,'comparison':'Frozen current prompt versus frozen equal-weight current/outlook blend. No candidate selection on this sample.','gate':'Gain >= 0.01; paired bootstrap 90% lower bound > 0; 95% inference coverage. Failure does not prove blend worse.','candidate_sha256':hashlib.sha256((PREVIOUS/'candidate.py').read_bytes()).hexdigest(),'records':[{'event_id':r['event_id'],'event_datetime':r['event_datetime']} for r in records]}
    planfile=HERE/'fresh-plan.json'
    if planfile.exists():assert json.loads(planfile.read_text())==plan,'Frozen plan changed'
    else:planfile.write_text(json.dumps(plan,indent=2),encoding='utf-8')
    cache=HERE/'results/inferences.jsonl'
    rows=[json.loads(x) for x in cache.read_text().splitlines()] if cache.exists() else []
    done={(x['event_id'],x['method']) for x in rows if 'percentile' in x}
    jobs=[(r,m) for r in records for m in ['current','outlook'] if (r['event_id'],m) not in done]
    cfg=dotenv_values(HERE.parent/'agent/.env')
    print('Fresh records:',len(records),'remaining requests:',len(jobs),'cached:',len(done),flush=True)
    errors=0
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        for i in range(0,len(jobs),8):
            batch=list(pool.map(lambda j:run(j,cfg),jobs[i:i+8]));errors+=sum('error'in x for x in batch)
            print('Completed',min(i+8,len(jobs)),'/',len(jobs),'errors',errors,flush=True)
            if errors>=4:print('Stopped after four errors; cached successes retained.',flush=True);return
    rows=[json.loads(x) for x in cache.read_text().splitlines()]
    vals={(x['event_id'],x['method']):x['percentile'] for x in rows if 'percentile'in x}
    def forecasts(items):
        a={};b={}
        for r in items:
            original=r.get('_original_event_id',r['event_id']);ticker=r['focal_assets'][0]['identifier_value'];key=(r['event_id'],ticker)
            x=vals.get((original,'current'));y=vals.get((original,'outlook'))
            if x is not None:a[key]=x
            if x is not None and y is not None:b[key]=(x+y)/2
        return a,b
    a,b=forecasts(records);current=engine.score(records,a);blend=engine.score(records,b)
    metric='delta_r_squared_imputed';gain=blend[metric]-current[metric]
    rng=random.Random(4392701);gains=[]
    for _ in range(500):
        copies=[]
        for i,r in enumerate(rng.choices(records,k=len(records))):
            copy=dict(r);copy['_original_event_id']=r['event_id'];copy['event_id']=str(i);copies.append(copy)
        a,b=forecasts(copies);gains.append(engine.score(copies,b)[metric]-engine.score(copies,a)[metric])
    interval=[float(np.quantile(gains,.05)),float(np.quantile(gains,.95))]
    success=len(vals)/192
    result={'author':'Oladapo Olaniyan','current':current,'blend':blend,'gain':gain,'paired_bootstrap_90pct':interval,'inference_success_rate':success,'gate_passed':bool(gain>=.01 and interval[0]>0 and success>=.95),'limitations':'Historical model training contamination possible; not proof of live rank change. Fresh sample was frozen before calls and excludes every prior evaluation event.'}
    (HERE/'results/fresh-metrics.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    print(json.dumps(result,indent=2),flush=True)

if __name__=='__main__':main()
