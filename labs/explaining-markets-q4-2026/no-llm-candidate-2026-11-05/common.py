"""Shared evaluation harness -- Oladapo Olaniyan, FIN-43900. Uses the pinned official scorer."""
import sys, json, gzip, hashlib
from pathlib import Path
import numpy as np, pandas as pd
HERE = Path(__file__).resolve().parent; LAB = HERE.parent
sys.path.insert(0, str(LAB / "improvement-2026-10-23" / "sources")); sys.path.insert(0, str(HERE))
import scoring_frozen as scorer
import em_features as E
PATHS = {"Q2": LAB/"forecast-audit-2026-10-28/2026Q2.jsonl.gz",
         "Q3": LAB/"improvement-2026-10-23/sources/EARNINGS_RELEASE_2026Q3.jsonl.gz",
         "Q4": LAB/"forecast-audit-2026-10-28/2026Q4.jsonl.gz"}
DEV_END = pd.Timestamp("2026-08-16", tz="UTC")   # dev: Q3 before this date; test A: Q3 on/after

def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def load_all():
    frames, labels = [], {}
    for tag, p in PATHS.items():
        df, _ = E.build_frame(p, tag); frames.append(df)
        allrecs = [json.loads(l) for l in gzip.open(p, "rt")]
        lab = scorer.add_percentiles(scorer.outcomes_frame(allrecs))   # quarter-wide official labels
        for r in lab.itertuples(): labels[(r.event_id, r.identifier_value)] = (r.y, r.surprise_pct)
    a = pd.concat(frames, ignore_index=True).sort_values(["dt", "event_id"]).reset_index(drop=True)
    a["y"] = [labels.get((e, t), (np.nan, np.nan))[0] for e, t in zip(a.event_id, a.ticker)]
    a["surprise_pct"] = [labels.get((e, t), (np.nan, np.nan))[1] for e, t in zip(a.event_id, a.ticker)]
    return a

def score(df, col):
    """Official contest metric (delta R^2, imputed family) over the rows of df."""
    s = scorer.score_submission(df[["y", "surprise_pct", col]].copy(), col)
    return s["delta_r_squared_imputed"], s["n_obs"]

def dr2_fast(y, s, p):
    """Closed-form delta R^2 identical to the scorer's two-regressor OLS (for bootstrap)."""
    y, s, p = map(np.asarray, (y, s, p)); n = len(y)
    X = np.column_stack([np.ones(n), s, p]); X0 = X[:, :2]
    def r2(M):
        b = np.linalg.lstsq(M, y, rcond=None)[0]; res = y - M @ b
        return 1 - (res @ res) / ((y - y.mean()) @ (y - y.mean()))
    return r2(X) - r2(X0)

def cached_original():
    out = {}
    for rel, key in [("improvement-2026-10-23/results/inferences.jsonl", "current"),
                     ("improvement-2026-10-27/results/inferences.jsonl", "current")]:
        for l in (LAB/rel).read_text(encoding="utf-8").splitlines():
            r = json.loads(l)
            if r.get("method") == key and "percentile" in r: out[r["event_id"]] = r["percentile"]
    return out
