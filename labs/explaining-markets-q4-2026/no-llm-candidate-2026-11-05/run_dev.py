"""Development stage ONLY: tune on Q3 events before 2026-08-16. Test periods are never scored here."""
import json, sys, itertools
import numpy as np, pandas as pd
from common import *
a = load_all()
G = E.GROUPS
sets = {"all": sum(G.values(), []), "options+preview": G["options"] + G["preview"], "facts": G["facts"] + G["options"][:0]}
specs = [{"kind": "ridge", "alpha": al} for al in (30, 300, 3000)] + [{"kind": "gbm", "depth": 2, "iters": 150}]
dev_mask = (a.period == "Q3") & (a.dt < DEV_END)
dev = a[dev_mask]
print("dev n", len(dev), dev.dt.min(), dev.dt.max())
res = []
for (sn, cols), spec in itertools.product(sets.items(), specs):
    p = E.walk_forward(a, dev_mask, cols, spec)
    a["_p"] = p
    d, n = score(a[dev_mask], "_p")
    res.append({"features": sn, "spec": spec, "dev_dr2": d, "n": n}); print(sn, spec, round(d, 5), n, flush=True)
a["_p"] = a["ref_gemini25"]; ref, nref = score(a[dev_mask], "_p")
orig = cached_original(); a["_o"] = a.event_id.map(orig)
ov = a[dev_mask & a._o.notna()]
print("ref gemini2.5 (organizer) dev", ref, nref, "| cached original 3.5 overlap n", len(ov))
best = max(res, key=lambda r: r["dev_dr2"])
plan = {"author": "Oladapo Olaniyan", "stage": "frozen after development", "dev_window": "Q3 events < 2026-08-16",
        "chosen": best, "dev_grid": res, "organizer_gemini25_dev_dr2": ref,
        "label_rule": "training target = within-training-window percentile rank of car1; lag 2 days; weekly refit",
        "test_A": "Q3 events >= 2026-08-16 (walk-forward)", "test_B": "Q4 events through 2026-10-27 (walk-forward)",
        "code_sha256": {"em_features.py": sha(HERE/"em_features.py"), "common.py": sha(HERE/"common.py"), "run_dev.py": sha(HERE/"run_dev.py")},
        "feature_columns": sets[best["features"]]}
(HERE/"plan.json").write_text(json.dumps(plan, indent=2, default=str), encoding="utf-8")
print("CHOSEN", best)
