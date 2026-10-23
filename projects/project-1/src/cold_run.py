"""Offline clean-environment evidence for Oladapo Olaniyan.
Ordinary reproducibility, never the human locked changed-input test.
"""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,os,shutil,subprocess,sys,venv
ROOT=Path(__file__).resolve().parents[1]
def main():
    run=ROOT/'repro'/datetime.now(timezone.utc).strftime('cold-%Y%m%dT%H%M%S%fZ')
    run.mkdir(parents=True,exist_ok=False)
    package=run/'package'; (package/'src').mkdir(parents=True)
    shutil.copytree(ROOT/'data',package/'data')
    for name in ['model.py','checks.py']: shutil.copy2(ROOT/'src'/name,package/'src'/name)
    environment=run/'environment'
    evidence=dict(analyst='Oladapo Olaniyan',timestamp=datetime.now(timezone.utc).isoformat(),host_python=sys.executable,
                  kind='Ordinary clean run; unchanged inputs; not locked test',copied_package=str(package),
                  first_failure='Inherited course .venv executable inaccessible; recorded before this clean run')
    try:
        venv.EnvBuilder(with_pip=False).create(environment)
        exe=environment/('Scripts/python.exe' if os.name=='nt' else 'bin/python')
        env=os.environ.copy(); env.pop('PYTHONPATH',None); env['PYTHONNOUSERSITE']='1'
        proc=subprocess.run([str(exe),str(package/'src/model.py'),'--output',str(package/'outputs/clean-run')],cwd=package,env=env,text=True,capture_output=True)
        evidence.update(clean_python=str(exe),returncode=proc.returncode,stdout=proc.stdout,stderr=proc.stderr)
        comparisons={}
        for name in ['results.json','forecast-statements.csv','sensitivity.csv','checks.csv','peer-multiples.csv']:
            original=ROOT/'outputs/final-working-run'/name; fresh=package/'outputs/clean-run'/name
            digest=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
            comparisons[name]=dict(reference_sha256=digest(original),cold_sha256=digest(fresh),equal=original.read_bytes()==fresh.read_bytes())
        evidence['comparisons']=comparisons
        evidence['passed']=proc.returncode==0 and all(r['equal'] for r in comparisons.values())
    except Exception as exc:
        evidence.update(passed=False,error=repr(exc))
    (run/'cold-run-evidence.json').write_text(json.dumps(evidence,indent=2),encoding='utf-8')
    print(json.dumps(evidence,indent=2))
    if not evidence['passed']: raise SystemExit(1)
if __name__=='__main__': main()
