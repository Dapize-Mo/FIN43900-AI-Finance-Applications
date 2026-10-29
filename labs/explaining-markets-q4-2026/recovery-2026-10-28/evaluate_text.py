"""Frozen local-only text experiment — Oladapo Olaniyan, FIN-43900."""
from pathlib import Path
import sys,json,gzip,hashlib
import numpy as np
HERE=Path(__file__).resolve().parent;OLD=HERE.parent/'improvement-2026-10-23'
sys.path.insert(0,str(OLD));import evaluate as engine
from text_model import RidgeTextModel
all_records=[json.loads(x) for x in gzip.decompress((OLD/'sources/EARNINGS_RELEASE_2026Q3.jsonl.gz').read_bytes()).decode().splitlines() if x]
records=[r for r in all_records if r.get('metrics',{}).get('earnings_surprise',{}).get('surprise_status')=='ok' and len(r.get('focal_assets',[]))==1 and r.get('disclosure',{}).get('items') and any(v.get('car1') is not None for v in r.get('event_returns',{}).values())]
records.sort(key=lambda r:(r['event_datetime'],r['event_id']))
prior={r['event_id'] for r in json.loads((OLD/'evaluation-plan.json').read_text())['records']}
prior|={r['event_id'] for r in json.loads((HERE.parent/'improvement-2026-10-27/fresh-plan.json').read_text())['records']}
a=int(len(records)*.5);b=int(len(records)*.65)
train=records[:a];dev=records[a:b];hold=[r for r in records[b:] if r['event_id'] not in prior]
plan={'author':'Oladapo Olaniyan','date':'2026-10-28','method':'Hashed unigram/bigram TFIDF ridge regression; official disclosure only; target quarter percentile.','alphas':[.1,1.,10.],'select_on':'development delta R squared only','train_n':len(train),'development_n':len(dev),'holdout_n':len(hold),'prior_evaluation_events_excluded_from_holdout':len(prior),'candidate_sha256':hashlib.sha256((HERE/'text_model.py').read_bytes()).hexdigest(),'holdout_ids':[r['event_id'] for r in hold],'deployment_gate':'Not automatically deployable: compare independent organizer Gemini reference; must establish evidence against actual deployed agent before production use.'}
assert not (HERE/'text-plan.json').exists(),'Do not reuse holdout for tuning'
(HERE/'text-plan.json').write_text(json.dumps(plan,indent=2),encoding='utf-8')
# Extraction explicitly selects disclosure; targets never appear in documents.
def docs(items):return [engine.baseline.format_materials(r['disclosure']) for r in items]
targets=engine.quarter_targets()
def labels(items):return [targets[(r['event_id'],r['focal_assets'][0]['identifier_value'])][0] for r in items]
def score(items,pred):return engine.score(items,{(r['event_id'],r['focal_assets'][0]['identifier_value']):float(v) for r,v in zip(items,pred)})
# Mathematical sanity check, independent synthetic target values.
sanity=RidgeTextModel(alpha=.1).fit(['strong growth raised guidance']*8+['weak decline cut guidance']*8,[.8]*8+[.2]*8)
v=sanity.predict(['strong growth raised guidance','weak decline cut guidance'])
assert v[0]>.7 and v[1]<.3
metric='delta_r_squared_imputed';development={}
for alpha in plan['alphas']:
 model=RidgeTextModel(alpha=alpha).fit(docs(train),labels(train))
 development[str(alpha)]=score(dev,model.predict(docs(dev)))
chosen=max(plan['alphas'],key=lambda x:development[str(x)][metric])
model=RidgeTextModel(alpha=chosen).fit(docs(train+dev),labels(train+dev))
hold_predictions=model.predict(docs(hold));candidate=score(hold,hold_predictions)
reference=[];available=[]
for i,r in enumerate(hold):
 ticker=r['focal_assets'][0]['identifier_value'];value=r.get('baseline_predictions',{}).get('gemini/ea-explain-contemp-summary',{}).get(ticker)
 if value is not None:available.append(i);reference.append(value)
ref_records=[hold[i] for i in available]
ref=score(ref_records,reference);same=score(ref_records,hold_predictions[available])
result={'author':'Oladapo Olaniyan','chosen_alpha':chosen,'development':development,'holdout':candidate,'organizer_reference_gemini':ref,'candidate_on_same_reference_sample':same,'difference_vs_reference':same[metric]-ref[metric],'holdout_n':len(hold),'limitations':'Reference is archived organizer Gemini 2.5 Flash-Lite, not our live Gemini 3.5 prompt blend. A higher score cannot prove a live improvement. No model requests or production changes.'}
(HERE/'text-results.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
np.savez_compressed(HERE/'text-model-research.npz',idf=model.idf,weights=model.weights,mean=model.mean,alpha=chosen)
print(json.dumps({'train':len(train),'development':len(dev),'holdout':len(hold),'chosen_alpha':chosen,'candidate_delta_r2':candidate[metric],'reference_delta_r2':ref[metric],'difference':result['difference_vs_reference']},indent=2))
