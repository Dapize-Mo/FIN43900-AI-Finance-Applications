"""Preregistered historical comparison — Oladapo Olaniyan, FIN-43900.
No POST to competition APIs. Model inputs exclude outcomes and baseline predictions.
"""
from pathlib import Path
import sys,json,gzip,hashlib,random,os,time,concurrent.futures,threading
from functools import lru_cache
import numpy as np
import pandas as pd
from dotenv import dotenv_values
from openai import OpenAI

HERE=Path(__file__).resolve().parent
AGENT=HERE.parent/'agent'
sys.path.insert(0,str(AGENT));sys.path.insert(0,str(AGENT/'src'));sys.path.insert(0,str(HERE/'sources'))
import predict as baseline
import scoring_frozen as scorer
from candidate import SYSTEM,EvidencePrediction
MODEL='gemini-3.5-flash-lite'
LOCK=threading.Lock()
RATE_LOCK=threading.Lock()
NEXT_REQUEST=0.0

def load_records():
    records=[json.loads(x) for x in gzip.decompress((HERE/'sources/EARNINGS_RELEASE_2026Q3.jsonl.gz').read_bytes()).decode().splitlines() if x]
    records=[r for r in records if r.get('metrics',{}).get('earnings_surprise',{}).get('surprise_status')=='ok' and len(r.get('focal_assets',[]))==1 and r.get('disclosure',{}).get('items') and any(v.get('car1') is not None for v in r.get('event_returns',{}).values())]
    records=sorted(records,key=lambda r:(r['event_datetime'],r['event_id']))
    boundary=int(len(records)*0.65)
    rng=random.Random(43923)
    dev=sorted(rng.sample(records[:boundary],32),key=lambda r:r['event_datetime'])
    holdout=sorted(rng.sample(records[boundary:],64),key=lambda r:r['event_datetime'])
    return [('development',r) for r in dev]+[('holdout',r) for r in holdout]

def build_inputs(record,method):
    # Explicitly select only the official disclosure bundle: never serialize record.
    materials=baseline.format_materials(record['disclosure'])
    ticker=record['focal_assets'][0]['identifier_value']
    if method=='current':
        user=(f"Event type: {record['event_type']}\nTicker: {ticker}\n\nEvent materials:\n{materials}\n\n"
          "Weigh, in roughly this order:\n"
          "  1. Quantitative surprise vs expectations — revenue, EPS, segment metrics.\n"
          "  2. Guidance / outlook — raises, holds, cuts vs the prior trajectory.\n"
          "  3. Strategic shifts — product launches, M&A, capital allocation, leadership.\n"
          "  4. Tone and confidence in management commentary (small weight).\n"
          "  5. Risks called out — regulatory, supply chain, demand, competition.\n\n"
          f"Predict the next-day unexpected-return percentile for {ticker}.")
        return baseline.SYSTEM_PROMPT,user,baseline.Prediction
    return SYSTEM,f"Event type: {record['event_type']}\nTicker: {ticker}\nOfficial event materials:\n{materials}",EvidencePrediction

def run_one(job,cfg):
    global NEXT_REQUEST
    with RATE_LOCK:
        wait=max(0,NEXT_REQUEST-time.monotonic())
        if wait:time.sleep(wait)
        NEXT_REQUEST=time.monotonic()+4.2
    split,record,method=job
    system,user,schema=build_inputs(record,method)
    digest=hashlib.sha256((MODEL+system+user).encode()).hexdigest()
    start=time.monotonic()
    client=OpenAI(api_key=cfg['GEMINI_API_KEY'],base_url=baseline.GEMINI_BASE_URL,timeout=45,max_retries=0)
    try:
        response=client.chat.completions.parse(model=MODEL,messages=[{'role':'system','content':system},{'role':'user','content':user}],response_format=schema,temperature=0)
        value=response.choices[0].message.parsed
        if value is None: raise ValueError('No parsed response')
        result={'split':split,'event_id':record['event_id'],'method':method,'model':MODEL,'input_sha256':digest,'percentile':value.predicted_percentile,'seconds':round(time.monotonic()-start,3),'evidence':getattr(value,'evidence',[])}
    except Exception as exc:
        result={'split':split,'event_id':record['event_id'],'method':method,'input_sha256':digest,'error':type(exc).__name__,'status_code':getattr(exc,'status_code',None)}
    finally: client.close()
    with LOCK:
        with (HERE/'results/inferences.jsonl').open('a',encoding='utf-8') as f:f.write(json.dumps(result)+'\n')
    return result

@lru_cache(maxsize=1)
def quarter_targets():
    records=[json.loads(x) for x in gzip.decompress((HERE/'sources/EARNINGS_RELEASE_2026Q3.jsonl.gz').read_bytes()).decode().splitlines() if x]
    frame=scorer.add_percentiles(scorer.outcomes_frame(records))
    return {(r.event_id,r.identifier_value):(r.y,r.surprise_pct) for r in frame.itertuples()}

def score(records,values):
    frame=scorer.outcomes_frame(records)
    targets=quarter_targets()
    originals={r['event_id']:r.get('_original_event_id',r['event_id']) for r in records}
    labels=[targets[(originals[r.event_id],r.identifier_value)] for r in frame.itertuples()]
    frame['y']=[x[0] for x in labels]
    frame['surprise_pct']=[x[1] for x in labels]
    frame['candidate']=[values.get((r.event_id,r.identifier_value),float('nan')) for r in frame.itertuples()]
    s=scorer.score_submission(frame,'candidate')
    return {k:(int(v) if isinstance(v,np.integer) else float(v) if isinstance(v,np.floating) else v) for k,v in s.items()}

def evaluate():
    selected=load_records();cfg=dotenv_values(AGENT/'.env')
    plan={'author':'Oladapo Olaniyan','date':'2026-10-23','model':MODEL,'development_n':32,'holdout_n':64,'seed':43923,'selection_rule':'Choose candidate or 50/50 blend using development delta R2 only. Holdout is evaluated once after selection.','deployment_gate':'Holdout delta R2 gain at least 0.01 and paired-bootstrap 90% lower bound greater than zero, with at least 95% inference success.','records':[{'split':s,'event_id':r['event_id'],'event_datetime':r['event_datetime'],'knowledge_cutoff':r.get('knowledge_cutoff')} for s,r in selected],'candidate_sha256':hashlib.sha256((HERE/'candidate.py').read_bytes()).hexdigest(),'limitations':'Historical LLM training contamination cannot be excluded. Holdout events precede current work. Validation cannot establish live competitiveness.'}
    manifest=HERE/'evaluation-plan.json'
    if manifest.exists():
        old=json.loads(manifest.read_text())
        assert old['candidate_sha256']==plan['candidate_sha256'],'Candidate changed after preregistration'
    else:manifest.write_text(json.dumps(plan,indent=2),encoding='utf-8')
    cached=[]
    cache=HERE/'results/inferences.jsonl'
    if cache.exists():cached=[json.loads(x) for x in cache.read_text(encoding='utf-8').splitlines()]
    done={(r['event_id'],r['method']) for r in cached if 'percentile' in r}
    jobs=[(s,r,m) for s,r in selected for m in ['current','outlook'] if (r['event_id'],m) not in done]
    print('Planned calls:',len(jobs),'cache successes:',len(done),flush=True)
    completed=0;failures=0
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        # Process bounded chunks to stop promptly on provider quota/auth failure.
        for start in range(0,len(jobs),8):
            outcomes=list(pool.map(lambda j:run_one(j,cfg),jobs[start:start+8]))
            completed+=len(outcomes);failures+=sum('error' in r for r in outcomes)
            print('Completed',completed,'/',len(jobs),'failures',failures,flush=True)
            if failures>=4:print('Stopped after four errors; cached successes retained.',flush=True);return
    rows=[json.loads(x) for x in cache.read_text(encoding='utf-8').splitlines()]
    values={(x['event_id'],x['method']):x['percentile'] for x in rows if 'percentile'in x}
    metrics={}
    for split in ('development','holdout'):
        records=[r for s,r in selected if s==split]
        methods={}
        for method in ('current','outlook','blend'):
            p={}
            for r in records:
                key=(r['event_id'],r['focal_assets'][0]['identifier_value'])
                a=values.get((r['event_id'],'current'));b=values.get((r['event_id'],'outlook'))
                value=a if method=='current' else b if method=='outlook' else (a+b)/2 if a is not None and b is not None else None
                if value is not None:p[key]=value
            methods[method]=score(records,p)
        metrics[split]=methods
    metric='delta_r_squared_imputed'
    chosen=max(('outlook','blend'),key=lambda m:metrics['development'][m].get(metric,-1))
    hold=[r for split,r in selected if split=='holdout']
    current=metrics['holdout']['current'][metric]
    gain=metrics['holdout'][chosen][metric]-current
    # Paired event bootstrap, frozen seed; no model selection on holdout.
    rng=random.Random(4392301); gains=[]
    for iteration in range(500):
        sampled=rng.choices(hold,k=len(hold)); copies=[]; a={};b={}
        for i,r in enumerate(sampled):
            copy=dict(r); copy['_original_event_id']=r['event_id']; copy['event_id']=str(i); copies.append(copy)
            ticker=r['focal_assets'][0]['identifier_value']
            first=values.get((r['event_id'],'current'));second=values.get((r['event_id'],'outlook'))
            if first is not None:a[(str(i),ticker)]=first
            forecast=second if chosen=='outlook' else (first+second)/2 if first is not None and second is not None else None
            if forecast is not None:b[(str(i),ticker)]=forecast
        sa=score(copies,a).get(metric);sb=score(copies,b).get(metric)
        if sa is not None and sb is not None:gains.append(sb-sa)
    interval=[float(np.quantile(gains,0.05)),float(np.quantile(gains,0.95))]
    success=len(values)/(len(selected)*2)
    metrics['decision']={'chosen_on_development':chosen,'holdout_gain':gain,'paired_bootstrap_90pct':interval,'inference_success_rate':success,'deployment_gate_passed':bool(gain>=0.01 and interval[0]>0 and success>=0.95)}
    print(json.dumps(metrics,indent=2),flush=True)
    (HERE/'results/metrics.json').write_text(json.dumps(metrics,indent=2,default=str),encoding='utf-8')

if __name__=='__main__':evaluate()
