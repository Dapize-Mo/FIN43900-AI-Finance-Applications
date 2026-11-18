"""Frozen out-of-sample evaluation -- Oladapo Olaniyan. Refuses to run if frozen code/plan changed."""
import json, warnings
import numpy as np, pandas as pd
warnings.filterwarnings("ignore")
from common import *
plan = json.loads((HERE/"plan.json").read_text())
for f in ("em_features.py", "common.py", "run_dev.py"):
    assert sha(HERE/f) == plan["code_sha256"][f], f"{f} changed after freeze"
a = load_all(); cols = plan["feature_columns"]; spec = plan["chosen"]["spec"]
cache = cached_original()
for l in (LAB/"preview-retry-2026-10-29/inferences.jsonl").read_text(encoding="utf-8").splitlines():
    r = json.loads(l)
    if r.get("method") == "original" and "percentile" in r: cache[r["event_id"]] = r["percentile"]
a["orig35"] = a.event_id.map(cache)
masks = {"A_Q3_late (walk-forward)": (a.period == "Q3") & (a.dt >= DEV_END), "B_Q4_to_Oct27 (walk-forward)": a.period == "Q4"}
rng = np.random.default_rng(20261105)
def boot(d, cols_pred, B=2000, cluster=None):
    """paired bootstrap of delta R^2 for each column and their difference; labels fixed (quarter-wide)."""
    n = len(d); y, s = d.y.to_numpy(), d.surprise_pct.to_numpy(); P = {c: d[c].to_numpy() for c in cols_pred}
    groups = d.dt.dt.date.astype(str).to_numpy() if cluster else None
    out = {c: [] for c in cols_pred}; diff = []
    ug = np.unique(groups) if cluster else None
    idxs = {g: np.where(groups == g)[0] for g in ug} if cluster else None
    for _ in range(B):
        if cluster: ix = np.concatenate([idxs[g] for g in rng.choice(ug, len(ug))])
        else: ix = rng.integers(0, n, n)
        v = [dr2_fast(y[ix], s[ix], P[c][ix]) for c in cols_pred]
        for c, x in zip(cols_pred, v): out[c].append(x)
        if len(v) == 2: diff.append(v[0] - v[1])
    q = lambda z: [float(np.percentile(z, 5)), float(np.percentile(z, 95))]
    return {c: q(out[c]) for c in cols_pred}, (q(diff) if diff else None)
report = {"plan_sha256": sha(HERE/"plan.json"), "chosen": plan["chosen"], "tests": {}}
for name, m in masks.items():
    a["cand"] = np.clip(E.walk_forward(a, m, cols, spec), 0, 1)
    # exploratory (post-freeze, NOT selection): richer feature sets
    a["expl_all"] = np.clip(E.walk_forward(a, m, sum(E.GROUPS.values(), []), spec), 0, 1)
    a["expl_opt_prev_ridge300"] = np.clip(E.walk_forward(a, m, E.GROUPS["options"] + E.GROUPS["preview"], {"kind": "ridge", "alpha": 300}), 0, 1)
    d = a[m & a.cand.notna() & a.surprise_pct.notna() & a.y.notna()].copy()
    t = {"n_events": int(m.sum()), "n_scored_candidate": int(len(d)), "coverage": float(len(d) / (m & a.surprise_pct.notna() & a.y.notna()).sum()), "date_range": [str(d.dt.min()), str(d.dt.max())]}
    for c in ("cand", "expl_all", "expl_opt_prev_ridge300", "ref_gemini25"):
        dd = d.dropna(subset=[c]); v, n = score(dd, c); t[c] = {"dr2": v, "n": n}
    d2 = d.copy(); d2["cand"] = d2["cand"]
    db = d.dropna(subset=["ref_gemini25"]); t["n_common_with_ref"] = int(len(db)); ci_e, diff_e = boot(db, ["cand", "ref_gemini25"]); ci_c, diff_c = boot(db, ["cand", "ref_gemini25"], cluster=True)
    t["cand_ci90_event"] = ci_e["cand"]; t["cand_ci90_dayclustered"] = ci_c["cand"]
    t["ref_ci90_event"] = ci_e["ref_gemini25"]
    t["cand_minus_ref_ci90_event"] = diff_e; t["cand_minus_ref_ci90_dayclustered"] = diff_c
    t["cand_on_common_with_ref"] = score(db, "cand")[0]; t["ref_on_common"] = score(db, "ref_gemini25")[0]; t["cand_minus_ref"] = t["cand_on_common_with_ref"] - t["ref_on_common"]
    ov = d.dropna(subset=["orig35"])
    if len(ov) >= 20:
        v1, n1 = score(ov, "cand"); v2, n2 = score(ov, "orig35"); ci, df_ = boot(ov, ["cand", "orig35"])
        t["overlap_with_cached_original35"] = {"n": int(len(ov)), "cand": v1, "original35_t0": v2, "cand_minus_orig": v1 - v2, "diff_ci90": df_, "cand_ci90": ci["cand"], "orig_ci90": ci["orig35"]}
    report["tests"][name] = t
    print(name, json.dumps({k: v for k, v in t.items()}, default=str, indent=1)[:2500], flush=True)
(HERE/"test-results.json").write_text(json.dumps(report, indent=2, default=str), encoding="utf-8")
