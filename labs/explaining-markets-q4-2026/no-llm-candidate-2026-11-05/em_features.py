"""No-generative-AI candidate: deterministic features + ridge/GBM, walk-forward.
Author: Oladapo Olaniyan, FIN-43900. Uses ONLY the official event bundle
(earnings-call-facts, earnings-preview, option-implied-stats) -- never outcomes,
earnings-surprise metrics, baseline predictions, or any LLM."""
import re, json, gzip, math
import numpy as np, pandas as pd

POS = r"\b(raised|raising|raise|above|exceed\w*|beat|beating|record|strong\w*|accelerat\w*|expan\w*|outperform\w*|momentum|ahead of|upgrade\w*|robust|improv\w*)\b"
NEG = r"\b(lowered|cut|cuts|reduc\w*|below|miss\w*|declin\w*|decreas\w*|weak\w*|headwind\w*|pressure\w*|soft\w*|slowdown|uncertain\w*|impair\w*|loss\w*|delay\w*|challeng\w*|tariff\w*|dilut\w*|shortfall|lower)\b"
GUIDE = r"(guidance|outlook|expects?|forecast|anticipat\w*|full[- ]year|fiscal 20\d\d)"
REAFF = r"\b(reaffirm\w*|maintain\w*|reiterat\w*|unchanged|in line with prior)\b"
VS_EXP_UP = r"(exceed\w*|above|beat|ahead of|surpass\w*)[^.]{0,40}(consensus|expectations|estimates|analyst|guidance)"
VS_EXP_DN = r"(below|miss\w*|short of|under)[^.]{0,40}(consensus|expectations|estimates|analyst|guidance)"
PREV_POS = r"\b(beat|beats|upgrade\w*|raised|accelerat\w*|strong\w*|upside|tailwind\w*|positive revision\w*)\b"
PREV_NEG = r"\b(miss|misses|downgrade\w*|cut|cuts|weak\w*|downside|headwind\w*|risk\w*|negative revision\w*|elevated expectations|priced in|high bar)\b"
NUM = r"(\d+(?:\.\d+)?)"

def _items(bundle):
    d = {}
    for i in (bundle or {}).get("items", []):
        d[i.get("id")] = i.get("content")
    return d

def _signed_pct(text):
    m = re.search(r"(revenue|sales)[^.%]{0,80}?\b(up|rose|grew|increased?|growth of|climbed|surged|jumped)\b[^.%]{0,40}?" + NUM + r"%", text, re.I)
    if m: return float(m.group(3))
    m = re.search(r"(revenue|sales)[^.%]{0,80}?\b(down|fell|declined?|decreased?|dropped)\b[^.%]{0,40}?" + NUM + r"%", text, re.I)
    if m: return -float(m.group(3))
    return None

def _money(s):
    m = re.search(r"\$?\s*" + NUM + r"\s*([KMBT])\b", s)
    if not m: return None
    return float(m.group(1)) * {"K": 1e3, "M": 1e6, "B": 1e9, "T": 1e12}[m.group(2)]

def features(bundle):
    it = _items(bundle)
    f = {}
    facts = it.get("earnings-call-facts") or []
    facts = [x for x in facts if isinstance(x, str)]
    ftxt = " ".join(facts)
    n = max(len(facts), 1)
    f["n_facts"] = len(facts); f["log_len_facts"] = math.log1p(len(ftxt))
    f["f_pos"] = len(re.findall(POS, ftxt, re.I)) / n
    f["f_neg"] = len(re.findall(NEG, ftxt, re.I)) / n
    f["f_net"] = f["f_pos"] - f["f_neg"]
    gs = [x for x in facts if re.search(GUIDE, x, re.I)]
    gtxt = " ".join(gs)
    f["g_pos"] = len(re.findall(POS, gtxt, re.I)); f["g_neg"] = len(re.findall(NEG, gtxt, re.I))
    f["g_net"] = f["g_pos"] - f["g_neg"]; f["g_reaff"] = len(re.findall(REAFF, gtxt, re.I)); f["g_n"] = len(gs)
    f["vs_up"] = len(re.findall(VS_EXP_UP, ftxt, re.I)); f["vs_dn"] = len(re.findall(VS_EXP_DN, ftxt, re.I))
    f["vs_net"] = f["vs_up"] - f["vs_dn"]
    g = _signed_pct(ftxt)
    f["rev_growth_avail"] = float(g is not None)
    f["rev_growth"] = float(np.clip(g, -60, 100)) / 100 if g is not None else 0.0
    # first-fact sentiment (headline) 
    h = facts[0] if facts else ""
    f["h_net"] = len(re.findall(POS, h, re.I)) - len(re.findall(NEG, h, re.I))
    # options
    o = it.get("option-implied-stats")
    iv = mv = sk = None
    if isinstance(o, dict):
        def val(k):
            b = o.get(k)
            return b["value"] if isinstance(b, dict) and b.get("status") == "ok" and isinstance(b.get("value"), (int, float)) else None
        iv, mv, sk = val("implied_earnings_volatility"), val("implied_absolute_earnings_move"), val("skew_25_delta")
    f["opt_avail"] = float(iv is not None)
    f["log_iv"] = math.log(iv) if iv and iv > 0 else 0.0
    f["log_move"] = math.log(mv) if mv and mv > 0 else 0.0
    f["skew_avail"] = float(sk is not None); f["skew"] = float(np.clip(sk, -0.3, 0.3)) if sk is not None else 0.0
    # preview
    p = it.get("earnings-preview")
    p = p if isinstance(p, str) else ""
    f["prev_avail"] = float(bool(p.strip()))
    f["log_len_prev"] = math.log1p(len(p))
    pn = max(len(p) / 1000, 1)
    f["p_pos"] = len(re.findall(PREV_POS, p, re.I)) / pn; f["p_neg"] = len(re.findall(PREV_NEG, p, re.I)) / pn
    f["p_net"] = f["p_pos"] - f["p_neg"]
    price = None
    m = re.search(r"(?:last price|price|stock|shares)\W{0,6}(?:~|≈)?\$\s*" + NUM, p, re.I)
    if m: price = float(m.group(1))
    m = re.search(r"52[- ]?w(?:ee)?k(?: range)?\W{0,8}\$?\s*" + NUM + r"\s*(?:[–\-—]|to)\s*\$?\s*" + NUM, p, re.I)
    pos52 = None
    if m and price is not None and float(m.group(2)) > float(m.group(1)):
        lo, hi = float(m.group(1)), float(m.group(2)); pos52 = (price - lo) / (hi - lo)
    f["pos52_avail"] = float(pos52 is not None); f["pos52"] = float(np.clip(pos52, -0.2, 1.2)) if pos52 is not None else 0.5
    m = re.search(r"(?:market cap|mkt cap|mcap)\W{0,8}(?:~|≈)?\$?\s*" + NUM + r"\s*([MBT])\b", p, re.I)
    mc = float(m.group(1)) * {"M": 1e6, "B": 1e9, "T": 1e12}[m.group(2).upper()] if m else None
    f["log_mcap"] = math.log(mc) if mc else 0.0; f["mcap_avail"] = float(mc is not None)
    m = re.search(r"beta\W{0,8}" + NUM, p, re.I)
    f["beta_avail"] = float(m is not None); f["beta"] = float(np.clip(float(m.group(1)), 0, 4)) if m else 1.0
    m = re.search(r"([+\-−–]?" + NUM + r")%\s*YTD|YTD\W{0,12}([+\-−–]?" + NUM + r")%|(down|up)\s*~?" + NUM + r"%\s*(?:YTD|year[- ]to[- ]date)", p, re.I)
    ytd = None
    if m:
        fix = lambda z: float(z.replace("−", "-").replace("–", "-"))
        if m.group(1) is not None: ytd = fix(m.group(1))
        elif m.group(3) is not None: ytd = fix(m.group(3))
        else: ytd = float(m.group(6)) * (-1 if m.group(5).lower() == "down" else 1)
    f["ytd_avail"] = float(ytd is not None); f["ytd"] = float(np.clip(ytd, -80, 150)) / 100 if ytd is not None else 0.0
    # consensus implied revenue growth from first consensus revenue row
    cg = None
    for line in p.splitlines():
        if re.search(r"\|\s*(net )?(revenue|sales)", line, re.I) and "%" in line:
            pc = re.findall(r"([+\-−–]?" + NUM + r")%", line)
            if pc: cg = float(pc[-1][0].replace("−", "-").replace("–", "-")); break
    f["cons_g_avail"] = float(cg is not None); f["cons_g"] = float(np.clip(cg, -60, 100)) / 100 if cg is not None else 0.0
    f["growth_vs_cons"] = f["rev_growth"] - f["cons_g"] if (g is not None and cg is not None) else 0.0
    # interactions: direction signal scaled by expected volatility
    f["net_x_iv"] = f["f_net"] * math.exp(f["log_iv"]) if f["opt_avail"] else 0.0
    f["skew_x_iv"] = f["skew"] * math.exp(f["log_iv"]) if f["opt_avail"] else 0.0
    return f

GROUPS = {
  "options": ["opt_avail","log_iv","log_move","skew_avail","skew","net_x_iv","skew_x_iv"],
  "facts": ["n_facts","log_len_facts","f_pos","f_neg","f_net","g_pos","g_neg","g_net","g_reaff","g_n","vs_up","vs_dn","vs_net","rev_growth_avail","rev_growth","h_net"],
  "preview": ["prev_avail","log_len_prev","p_pos","p_neg","p_net","pos52_avail","pos52","mcap_avail","log_mcap","beta_avail","beta","ytd_avail","ytd","cons_g_avail","cons_g","growth_vs_cons"],
}

def load(path):
    rows = [json.loads(l) for l in gzip.open(path, "rt")]
    return [r for r in rows if len(r.get("focal_assets", [])) == 1 and r.get("disclosure", {}).get("items")]

def build_frame(path, quarter_tag):
    """One row per event with features (bundle only), car1, event time, cutoff."""
    recs = load(path)
    out = []
    for r in recs:
        t = r["focal_assets"][0]["identifier_value"]
        car1 = (r.get("event_returns", {}).get(t) or {}).get("car1")
        row = features(r["disclosure"])
        row.update(event_id=r["event_id"], ticker=t, period=quarter_tag, dt=pd.Timestamp(r["event_datetime"]),
                   cutoff=pd.Timestamp(r["knowledge_cutoff"]), car1=car1,
                   ref_gemini25=((r.get("baseline_predictions") or {}).get("gemini/ea-explain-contemp-summary") or {}).get(t))
        out.append(row)
    return pd.DataFrame(out).sort_values(["dt", "event_id"]).reset_index(drop=True), recs

def rank01(x):
    x = np.asarray(x, float); n = len(x)
    if n < 2: return np.full(n, 0.5)
    return pd.Series(x).rank(method="average").to_numpy().__sub__(1) / (n - 1)

class Ridge:
    def __init__(self, alpha): self.alpha = alpha
    def fit(self, X, y):
        self.mu = X.mean(0); self.sd = X.std(0) + 1e-9
        Z = np.clip((X - self.mu) / self.sd, -4, 4); self.ym = y.mean()
        A = Z.T @ Z + self.alpha * np.eye(Z.shape[1]); self.w = np.linalg.solve(A, Z.T @ (y - self.ym)); return self
    def predict(self, X):
        return self.ym + np.clip((X - self.mu) / self.sd, -4, 4) @ self.w

def make_model(spec):
    if spec["kind"] == "ridge": return Ridge(spec["alpha"])
    from sklearn.ensemble import HistGradientBoostingRegressor
    class G:
        def fit(s, X, y):
            s.m = HistGradientBoostingRegressor(max_depth=spec["depth"], max_iter=spec["iters"], learning_rate=0.04,
                      min_samples_leaf=40, l2_regularization=5.0, random_state=0).fit(X, y); return s
        def predict(s, X): return s.m.predict(X)
    return G()

def walk_forward(df, test_mask, cols, spec, lag_days=2):
    """Predict each test event with a model fit only on events whose outcome was realized
    (event time + lag) before the FIRST knowledge cutoff of the test week. Training target =
    percentile rank of car1 among the training events themselves (no future distribution)."""
    pred = pd.Series(np.nan, index=df.index)
    t = df[test_mask]
    wk = t["cutoff"].dt.tz_convert("UTC").dt.to_period("W")
    for w, g in t.groupby(wk):
        start = g["cutoff"].min()
        tr = df[(df["dt"] + pd.Timedelta(days=lag_days) <= start) & df["car1"].notna()]
        if len(tr) < 200: continue
        y = rank01(tr["car1"].to_numpy())
        m = make_model(spec).fit(tr[cols].to_numpy(float), y)
        p = np.asarray(m.predict(g[cols].to_numpy(float)))
        pred.loc[g.index] = p
    return pred

def to_percentile_unit(p):  # map raw model output to [0,1] by clipping (score is affine-invariant anyway)
    return np.clip(p, 0, 1)
