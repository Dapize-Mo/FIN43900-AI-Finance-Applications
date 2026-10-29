"""Hosted configuration check — Oladapo Olaniyan; no provider requests."""
from pathlib import Path
import sys,json,modal
sys.path.insert(0,str(Path(__file__).resolve().parent.parent/'agent'))
from modal_app import image
app=modal.App('fin439-recovery-mode-check')
@app.function(image=image,timeout=60,serialized=True)
def check():
    import os
    from unittest.mock import patch
    import predict
    assert os.environ.get('EM_STRATEGY')=='original'
    with patch.object(predict,'_ask_current',return_value=.72) as current, patch.object(predict,'_ask_outlook',side_effect=AssertionError('Unexpected outlook request')) as outlook:
        value=predict._ask_llm(summary={},ticker='SYNTH',event_type='SYNTHETIC_CHECK')
        assert value==.72 and current.call_count==1 and outlook.call_count==0
    return {'mode':os.environ['EM_STRATEGY'],'selection_passed':True,'actual_model_calls':0,'author':'Oladapo Olaniyan'}
if __name__=='__main__':
    with app.run():result=check.remote()
    (Path(__file__).parent/'mode-check.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    print(json.dumps(result))
