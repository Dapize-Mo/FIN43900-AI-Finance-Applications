"""Join live forecasts (portal, Oct 28-Nov 6) to the refreshed official archive - Oladapo Olaniyan."""
import sys, json, gzip, warnings
from pathlib import Path
import numpy as np, pandas as pd
warnings.filterwarnings("ignore")
HERE = Path(__file__).resolve().parent; LAB = HERE.parent
sys.path.insert(0, str(LAB/"improvement-2026-10-23"/"sources")); sys.path.insert(0, str(LAB/"no-llm-candidate-2026-11-05"))
import scoring_frozen as scorer, em_features as E
def load():
    recs = [json.loads(l) for l in gzip.open(HERE/"2026Q4.jsonl.gz", "rt")]
    lab = scorer.add_percentiles(scorer.outcomes_frame(recs))
    L = {(r.event_id, r.identifier_value): (r.y, r.surprise_pct) for r in lab.itertuples()}
    df, _ = E.build_frame(HERE/"2026Q4.jsonl.gz", "Q4")
    df["y"] = [L.get((e, t), (np.nan,)*2)[0] for e, t in zip(df.event_id, df.ticker)]
    df["sp"] = [L.get((e, t), (np.nan,)*2)[1] for e, t in zip(df.event_id, df.ticker)]
    P = {}
    for f in ("preds_a.txt", "preds_b.txt", "preds_c.txt"):
        for tok in (HERE/f).read_text().split():
            k, v = tok.split("="); P[k] = int(v)/100
    late = df.dt >= pd.Timestamp("2026-10-28", tz="UTC")
    df["pred"] = np.where(late, df.ticker.map(P), np.nan)
    df["day"] = df.dt.dt.tz_convert("America/New_York").dt.strftime("%m-%d")
    return df, recs
def dr2(d, cols):
    """delta R^2 of adding `cols` to the surprise-only fit (same OLS as the scorer for one column)."""
    y = d.y.to_numpy(); n = len(y)
    def r2(M):
        b = np.linalg.lstsq(M, y, rcond=None)[0]; r = y - M @ b; return 1 - r @ r / ((y - y.mean()) @ (y - y.mean()))
    X0 = np.column_stack([np.ones(n), d.sp]); X = np.column_stack([X0] + [d[c] for c in cols])
    return r2(X) - r2(X0)
