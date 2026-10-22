"""FIN 43900 Lab 15 -- Portfolio Stability Decision Streamlit Application
Interactive web interface finding the lowest-risk portfolio mix meeting mandate
objectives and reserve rules, evaluating estimation risk and portfolio stability.

Author: Oladapo Olaniyan (oolaniy@purdue.edu)
Course: FIN 43900 -- AI Finance Applications, Purdue University
Session: Session 15 (Week 9)
"""

import copy
import streamlit as st
import pandas as pd

# Import calculation engine and Meridian defaults directly from portfolio.py (reusing math)
from portfolio import (
    SLEEVES as MERIDIAN_SLEEVES,
    CORRELATION as MERIDIAN_CORRELATION,
    OBJECTIVE_RETURN as DEFAULT_OBJECTIVE,
    RESERVE_MINIMUM as DEFAULT_RESERVE_MIN,
    build_covariance,
    search_lowest_risk_mix,
    estimate_from_prices,
    format_weights,
)

# ------------------------------------------------------------------------------
# PAGE CONFIGURATION
# ------------------------------------------------------------------------------
st.set_page_config(
    page_title="Portfolio Stability Decision | FIN 43900",
    page_icon="⚖️",
    layout="wide",
)

st.title("Lab 15 — Portfolio Stability Decision")
st.caption("built with AI help, a learning demonstration, not investment advice.")
st.markdown("**Author:** Oladapo Olaniyan (`oolaniy@purdue.edu`) | **Course:** FIN 43900 AI Finance Applications, Purdue University")

# ------------------------------------------------------------------------------
# SIDEBAR CONTROLS
# ------------------------------------------------------------------------------
st.sidebar.header("Mandate & Data Controls")

objective_input = st.sidebar.number_input(
    "Target Objective Return (%)",
    min_value=0.0,
    max_value=30.0,
    value=float(DEFAULT_OBJECTIVE * 100.0),
    step=0.1,
    help="Target annualized portfolio return required by the mandate (e.g. CPI + 4.0% = 6.5%).",
)
objective_decimal = objective_input / 100.0

reserve_min_input = st.sidebar.number_input(
    "Minimum Reserve-Eligible Weight (%)",
    min_value=0.0,
    max_value=100.0,
    value=float(DEFAULT_RESERVE_MIN * 100.0),
    step=0.5,
    help="Mandatory minimum weight in daily-liquid sovereign cash/bills/Treasuries (e.g. 3.0% = 12 months payout).",
)
reserve_min_decimal = reserve_min_input / 100.0

uploaded_file = st.sidebar.file_uploader(
    "Upload prices.csv",
    type=["csv"],
    help="CSV file of monthly adjusted close prices (Date first, oldest first, one column per ticker).",
)

last_36_switch = st.sidebar.checkbox(
    "Last 36 Months Only",
    value=False,
    help="Estimate parameters using only the most recent 36 monthly observations instead of full history.",
)

# ------------------------------------------------------------------------------
# LOAD ASSET UNIVERSE & PARAMETERS
# ------------------------------------------------------------------------------
if uploaded_file is not None:
    try:
        tickers, raw_sleeves, corr_matrix, n_obs = estimate_from_prices(uploaded_file, last_36=last_36_switch)
        data_source_label = f"Uploaded CSV ({'Last 36 Months' if last_36_switch else 'All Months'}, N={n_obs})"
        base_sleeves = copy.deepcopy(raw_sleeves)
        base_corr = copy.deepcopy(corr_matrix)
    except Exception as e:
        st.sidebar.error(f"Error parsing uploaded prices CSV: {e}")
        base_sleeves = copy.deepcopy(MERIDIAN_SLEEVES)
        base_corr = copy.deepcopy(MERIDIAN_CORRELATION)
        data_source_label = "Meridian Foundation Training Values (Fallback)"
else:
    base_sleeves = copy.deepcopy(MERIDIAN_SLEEVES)
    base_corr = copy.deepcopy(MERIDIAN_CORRELATION)
    data_source_label = "Meridian Foundation Training Values (Course Authored)"

# Compute "As-Loaded" Baseline Mix (Unedited baseline)
base_cov = build_covariance(base_sleeves, base_corr)
base_mix = search_lowest_risk_mix(
    base_sleeves,
    base_cov,
    objective=objective_decimal,
    reserve_min=reserve_min_decimal,
    step=5,
)

st.info(f"**Active Data Source:** {data_source_label} | **Decision Hurdle:** >= {objective_input:.2f}% | **Reserve Floor:** >= {reserve_min_input:.1f}%")

# ------------------------------------------------------------------------------
# EDITABLE INPUTS PANEL
# ------------------------------------------------------------------------------
st.subheader("Asset Sleeve Inputs (Editable Estimates & Eligibility)")
st.markdown("Modify any expected return estimate below or toggle reserve eligibility to test allocation stability against estimation shocks:")

cols = st.columns(len(base_sleeves))
edited_sleeves = []

for idx, (col, s) in enumerate(zip(cols, base_sleeves)):
    with col:
        st.markdown(f"**{s['name']}**")
        default_ret_pct = float(round(s["return"] * 100.0, 2))
        vol_pct = float(round(s["volatility"] * 100.0, 2))
        
        # Expected return editable box
        new_ret_pct = st.number_input(
            f"Exp Return (%)",
            value=default_ret_pct,
            step=0.1,
            key=f"ret_{idx}_{s['name']}",
            help=f"Annualized expected return for {s['name']}.",
        )
        
        # Reserve eligible toggle box
        is_reserve = st.checkbox(
            "Reserve Eligible",
            value=bool(s["reserve_eligible"]),
            key=f"res_{idx}_{s['name']}",
            help="Eligible to satisfy mandatory sovereign liquidity reserve rule.",
        )
        
        st.caption(f"Volatility: `{vol_pct:.2f}%`")
        
        edited_sleeves.append({
            "name": s["name"],
            "return": new_ret_pct / 100.0,
            "volatility": s["volatility"],
            "reserve_eligible": is_reserve,
        })

# ------------------------------------------------------------------------------
# OPTIMIZE CURRENT / STRESSED MIX
# ------------------------------------------------------------------------------
curr_cov = build_covariance(edited_sleeves, base_corr)
curr_mix = search_lowest_risk_mix(
    edited_sleeves,
    curr_cov,
    objective=objective_decimal,
    reserve_min=reserve_min_decimal,
    step=5,
)

# ------------------------------------------------------------------------------
# SIDE-BY-SIDE ALLOCATION COMPARISON
# ------------------------------------------------------------------------------
st.write("---")
st.subheader("Decision Comparison: As-Loaded Baseline vs. Current / Stressed Mix")

col_base, col_curr = st.columns(2)

# Left Column: As-Loaded Baseline
with col_base:
    st.markdown("### 📌 As-Loaded Baseline")
    if base_mix is not None:
        w_base_pct = [round(w * 100.0, 2) for w in base_mix["weights"]]
        w_base_str = " / ".join(f"{w:.0f}" for w in w_base_pct)
        st.success(f"**Optimal Weights:** `{w_base_str}`")
        
        m_col1, m_col2, m_col3 = st.columns(3)
        m_col1.metric("Expected Return", f"{base_mix['return']*100:.2f}%")
        m_col2.metric("Portfolio Volatility", f"{base_mix['volatility']*100:.2f}%")
        m_col3.metric("Reserve-Eligible", f"{base_mix['reserve']*100:.1f}%")
        
        df_base = pd.DataFrame({
            "Asset Sleeve": [s["name"] for s in base_sleeves],
            "Weight (%)": [f"{w:.1f}%" for w in w_base_pct],
            "Reserve Eligible": ["Yes" if s["reserve_eligible"] else "No" for s in base_sleeves],
        })
        st.dataframe(df_base, hide_index=True, use_container_width=True)
    else:
        st.error("**No mix meets the objective** under baseline inputs.")

# Right Column: Current / Stressed Mix
with col_curr:
    st.markdown("### ⚡ Current / Stressed Mix")
    if curr_mix is not None:
        w_curr_pct = [round(w * 100.0, 2) for w in curr_mix["weights"]]
        w_curr_str = " / ".join(f"{w:.0f}" for w in w_curr_pct)
        st.success(f"**Optimal Weights:** `{w_curr_str}`")
        
        m_col1, m_col2, m_col3 = st.columns(3)
        m_col1.metric("Expected Return", f"{curr_mix['return']*100:.2f}%")
        m_col2.metric("Portfolio Volatility", f"{curr_mix['volatility']*100:.2f}%")
        m_col3.metric("Reserve-Eligible", f"{curr_mix['reserve']*100:.1f}%")
        
        df_curr = pd.DataFrame({
            "Asset Sleeve": [s["name"] for s in edited_sleeves],
            "Weight (%)": [f"{w:.1f}%" for w in w_curr_pct],
            "Reserve Eligible": ["Yes" if s["reserve_eligible"] else "No" for s in edited_sleeves],
        })
        st.dataframe(df_curr, hide_index=True, use_container_width=True)
    else:
        st.error("**No mix meets the objective** under current inputs.")

# ------------------------------------------------------------------------------
# STABILITY ANALYSIS & LARGEST WEIGHT CHANGE
# ------------------------------------------------------------------------------
st.write("---")
if base_mix is not None and curr_mix is not None:
    weight_changes = [abs(c - b) for c, b in zip(w_curr_pct, w_base_pct)]
    max_change_pts = max(weight_changes)
    
    st.subheader("Stability Diagnosis: Maximum Weight Shift")
    st.metric(
        label="Largest Weight Change Across Asset Sleeves",
        value=f"{max_change_pts:.0f} points",
        delta=f"{max_change_pts:.0f} pts shift",
        delta_color="inverse" if max_change_pts >= 20.0 else "normal",
    )
    
    # Detailed change table
    change_rows = []
    for s_base, s_curr, wb, wc in zip(base_sleeves, edited_sleeves, w_base_pct, w_curr_pct):
        diff = wc - wb
        change_rows.append({
            "Asset Sleeve": s_base["name"],
            "Baseline Weight": f"{wb:.1f}%",
            "Current Weight": f"{wc:.1f}%",
            "Absolute Shift (pts)": f"{abs(diff):.1f}",
            "Direction": "Unchanged" if abs(diff) < 1e-6 else ("+ Allocation" if diff > 0 else "- Allocation"),
        })
    st.table(pd.DataFrame(change_rows))

    if max_change_pts >= 20.0:
        st.warning(
            f"⚠️ **Estimation Risk Warning:** A minor adjustment in estimates caused a **{max_change_pts:.0f}-point shift** in portfolio capital. "
            "Because quadratic optimizers are 'error maximizers' that heavily overweight over-estimated assets and underweight under-estimated ones, "
            "this mix must be classified as **PILOT or REJECT**, never blindly adopted."
        )
    else:
        st.success("✅ **Stable Allocation:** Weight adjustments remain within acceptable parameter sensitivity boundaries.")

elif base_mix is None and curr_mix is None:
    st.warning("Neither baseline nor current inputs permit a feasible allocation clearing the objective and reserve floor.")
else:
    st.warning("One of the runs failed to produce a feasible mix. Review objective return or reserve requirements.")

# ------------------------------------------------------------------------------
# KNOWN-ANSWER AUDIT & BENCHMARKS EXPANDER
# ------------------------------------------------------------------------------
with st.expander("🔍 Course Known-Answer Verification Anchors (Lab 15 Rubric)"):
    st.markdown("""
    | Configuration / Run | Expected Allocation (Bills / 10y / IG / Eq) | Return | Volatility | Largest Shift |
    | :--- | :---: | :---: | :---: | :---: |
    | **Meridian As Loaded** | `0 / 20 / 25 / 55` | **6.51%** | **9.44%** | Baseline |
    | **Equity Return 8.0% → 7.0%** | `0 / 10 / 10 / 80` | **6.53%** | **12.94%** | **25 points** |
    | **Engine Link Probe (IG-Eq Corr = 0.50)** | `0 / 40 / 0 / 60` | **6.52%** | **9.73%** | Engine Link Proven |
    """)
    st.caption("Engine link verified: calculations execute directly against `portfolio.py` with zero copied math.")
