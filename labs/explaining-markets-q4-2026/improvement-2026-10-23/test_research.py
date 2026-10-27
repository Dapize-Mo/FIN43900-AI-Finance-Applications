"""Research validity checks — Oladapo Olaniyan, FIN-43900."""
import copy
from evaluate import load_records,build_inputs,score

def test_model_prompt_excludes_outcomes():
    _,record=load_records()[0]
    sentinel='SECRET_FUTURE_LABEL_998877'
    bad=copy.deepcopy(record)
    bad['event_returns']={'untrusted':sentinel}
    bad['metrics']={'future_label':sentinel}
    bad['baseline_predictions']={'future_prediction':sentinel}
    for method in ('current','outlook'):
        system,user,_=build_inputs(bad,method)
        assert sentinel not in system+user
        assert 'Official event materials' in user or 'Event materials' in user

def test_chronological_holdout_is_disjoint_and_reproducible():
    samples=load_records()
    assert [(s,r['event_id']) for s,r in samples]==[(s,r['event_id']) for s,r in load_records()]
    dev=[r for s,r in samples if s=='development'];hold=[r for s,r in samples if s=='holdout']
    assert len(dev)==32 and len(hold)==64
    assert max(r['event_datetime'] for r in dev)<min(r['event_datetime'] for r in hold)
    assert not {r['event_id'] for r in dev}&{r['event_id'] for r in hold}

def test_frozen_score_does_not_reward_uniform_rescaling():
    records=[r for _,r in load_records()]
    p={(r['event_id'],r['focal_assets'][0]['identifier_value']):i/len(records) for i,r in enumerate(records)}
    shrunk={key:0.25+0.5*value for key,value in p.items()}
    assert abs(score(records,p)['delta_r_squared_imputed']-score(records,shrunk)['delta_r_squared_imputed'])<1e-10


def test_bootstrap_preserves_quarter_targets():
    from evaluate import quarter_targets
    import scoring_frozen as scorer
    _,record=load_records()[0]
    duplicate=dict(record);duplicate['_original_event_id']=record['event_id'];duplicate['event_id']='resampled'
    ticker=record['focal_assets'][0]['identifier_value']
    original=scorer.outcomes_frame([record])
    assert (record['event_id'],ticker) in quarter_targets()
    # Duplicate event identifiers map back to fixed labels, even in a tiny sample.
    result=score([record,duplicate],{(record['event_id'],ticker):0.3,('resampled',ticker):0.7})
    assert result['n_obs']==2
