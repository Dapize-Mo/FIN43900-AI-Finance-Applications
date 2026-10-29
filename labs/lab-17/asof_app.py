"""
FIN 43900 Lab 17: Point-in-Time Audit (Streamlit Rates App)
Student Author: Oladapo Olaniyan (oolaniy@purdue.edu)
Course: FIN 43900 - AI Finance Applications, Fall 2026
Instructor: Prof. Cinder Zhang, Daniels School of Business, Purdue University

A Streamlit application that works like a FRED page for interest rates,
pulling live data from FRED (today's vintage) and ALFRED (vintage as of a specific date).
Evaluates point-in-time data availability, publication lag, and historical revisions.
"""

import io
import urllib.request
import urllib.error
import datetime
import pandas as pd
import numpy as np
import altair as alt
import streamlit as st

# Set page config
st.set_page_config(
    page_title="FRED/ALFRED Point-in-Time Rates App",
    page_icon="📈",
    layout="wide",
)

# Title & Mandated Disclaimer
st.title("Point-in-Time Interest Rates & Macroeconomic Audit")
st.markdown(
    "*data from FRED and ALFRED, Federal Reserve Bank of St. Louis, downloaded today; "
    "built with AI help, a learning demonstration, not investment advice.*"
)

# -----------------------------------------------------------------------------
# Cached Download Functions
# -----------------------------------------------------------------------------

@st.cache_data(ttl=3600, show_spinner=False)
def download_fred_series(series_id: str) -> pd.DataFrame:
    """
    Downloads today's values for a given series from FRED public CSV.
    URL: https://fred.stlouisfed.org/graph/fredgraph.csv?id=SERIES
    Replaces '.' with NaN, drops missing values, and parses dates.
    """
    url = f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={series_id}"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            content = resp.read().decode("utf-8")
    except urllib.error.HTTPError as e:
        raise ValueError(f"Series ID '{series_id}' not found on FRED (HTTP {e.code}: {e.reason}).") from e
    except urllib.error.URLError as e:
        raise ConnectionError(f"Network error accessing FRED for '{series_id}': {e.reason}") from e
    
    # Check if FRED returned an HTML error page instead of CSV
    if "<!DOCTYPE" in content or "<html" in content.lower():
        raise ValueError(f"FRED returned an invalid response for series ID '{series_id}'. Please check if the ID is valid.")
    
    df = pd.read_csv(io.StringIO(content))
    if df.empty or len(df.columns) < 2:
        raise ValueError(f"No valid data columns found for series ID '{series_id}'.")
    
    val_col = df.columns[1]
    df[val_col] = pd.to_numeric(df[val_col].astype(str).str.strip().replace(".", np.nan), errors="coerce")
    df["observation_date"] = pd.to_datetime(df["observation_date"])
    df = df.dropna(subset=[val_col]).rename(columns={val_col: "today_value"}).sort_values("observation_date").reset_index(drop=True)
    return df


@st.cache_data(ttl=3600, show_spinner=False)
def download_alfred_series(series_id: str, vintage_date: str) -> pd.DataFrame:
    """
    Downloads the values as known on vintage_date from ALFRED public CSV.
    URL: https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=SERIES&vintage_date=YYYY-MM-DD
    Replaces '.' with NaN, drops missing values, and parses dates.
    """
    url = f"https://alfred.stlouisfed.org/graph/alfredgraph.csv?id={series_id}&vintage_date={vintage_date}"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            content = resp.read().decode("utf-8")
    except urllib.error.HTTPError as e:
        raise ValueError(f"Series ID '{series_id}' with vintage '{vintage_date}' not found on ALFRED (HTTP {e.code}: {e.reason}).") from e
    except urllib.error.URLError as e:
        raise ConnectionError(f"Network error accessing ALFRED for '{series_id}': {e.reason}") from e
        
    if "<!DOCTYPE" in content or "<html" in content.lower():
        raise ValueError(f"ALFRED returned an invalid response for series ID '{series_id}' with vintage '{vintage_date}'.")
        
    df = pd.read_csv(io.StringIO(content))
    if df.empty or len(df.columns) < 2:
        raise ValueError(f"No valid data columns found in ALFRED for series ID '{series_id}'.")
        
    val_col = df.columns[1]
    df[val_col] = pd.to_numeric(df[val_col].astype(str).str.strip().replace(".", np.nan), errors="coerce")
    df["observation_date"] = pd.to_datetime(df["observation_date"])
    df = df.dropna(subset=[val_col]).rename(columns={val_col: "vintage_value"}).sort_values("observation_date").reset_index(drop=True)
    return df


# -----------------------------------------------------------------------------
# Sidebar Configuration
# -----------------------------------------------------------------------------

st.sidebar.header("Data Selection & Controls")

DEFAULT_SERIES = {
    "BAA": "Moody's Baa corporate bond yield",
    "FEDFUNDS": "federal funds rate",
    "DGS10": "10-year Treasury yield",
    "MORTGAGE30US": "30-year mortgage rate",
}

# Multiselect with ID and name
selected_default_keys = st.sidebar.multiselect(
    "Select Default Interest Rate Series:",
    options=list(DEFAULT_SERIES.keys()),
    default=list(DEFAULT_SERIES.keys()),
    format_func=lambda x: f"{x} ({DEFAULT_SERIES[x]})"
)

# Text box to add any other FRED series ID
custom_series_input = st.sidebar.text_input(
    "Add other FRED series ID (e.g. CPIAUCSL, PAYEMS, UNRATE, T10Y2Y):",
    value=""
)

# Parse additional series
all_series = list(selected_default_keys)
if custom_series_input.strip():
    custom_ids = [s.strip().upper() for s in custom_series_input.split(",") if s.strip()]
    for cid in custom_ids:
        if cid not in all_series:
            all_series.append(cid)

# Start date input (default: 1 January 2020)
start_date = st.sidebar.date_input(
    "Start Date:",
    value=datetime.date(2020, 1, 1),
    min_value=datetime.date(1950, 1, 1),
    max_value=datetime.date(2030, 12, 31)
)

# "As known on" date input (default: today)
vintage_date = st.sidebar.date_input(
    "'As known on' Date (Vintage):",
    value=datetime.date.today(),
    min_value=datetime.date(1950, 1, 1),
    max_value=datetime.date(2030, 12, 31)
)

vintage_date_str = vintage_date.strftime("%Y-%m-%d")
start_date_ts = pd.to_datetime(start_date)

st.sidebar.markdown("---")
st.sidebar.markdown(f"**Audit Vintage:** `{vintage_date_str}`")
st.sidebar.markdown(f"**Series Count:** `{len(all_series)}`")

# -----------------------------------------------------------------------------
# Main Application Flow
# -----------------------------------------------------------------------------

if not all_series:
    st.warning("Please select at least one series from the sidebar.")
    st.stop()

table_rows = []
series_data_cache = {}

# Process each series independently so unknown IDs don't crash the page
for sid in all_series:
    try:
        # Download both today and vintage data
        df_today = download_fred_series(sid)
        df_vintage = download_alfred_series(sid, vintage_date_str)
        
        if df_today.empty or df_vintage.empty:
            st.error(f"⚠️ Series `{sid}` returned an empty dataset from FRED/ALFRED.")
            continue
            
        # Filter today's data for the chart from start_date
        df_today_chart = df_today[df_today["observation_date"] >= start_date_ts].copy()
        
        # Last date measured and value as known on vintage date
        last_vintage_row = df_vintage.iloc[-1]
        last_vintage_date = last_vintage_row["observation_date"]
        last_vintage_val = last_vintage_row["vintage_value"]
        
        # Last date measured and value today
        last_today_row = df_today.iloc[-1]
        last_today_date = last_today_row["observation_date"]
        last_today_val = last_today_row["today_value"]
        
        # Values today after the last date known then (late count)
        late_count = len(df_today[df_today["observation_date"] > last_vintage_date])
        
        # Values on same dates revised since (revised count)
        merged = pd.merge(df_vintage, df_today, on="observation_date", how="inner")
        # Floating point difference threshold
        revised_mask = np.abs(merged["vintage_value"] - merged["today_value"]) > 1e-5
        revised_count = int(revised_mask.sum())
        
        # Save metrics for summary table
        table_rows.append({
            "Series ID": sid,
            "FRED Page": f"https://fred.stlouisfed.org/series/{sid}",
            "Last Date Known Then": last_vintage_date.strftime("%Y-%m-%d"),
            "Value Known Then": f"{last_vintage_val:,.4f}".rstrip("0").rstrip("."),
            "Last Date Measured Today": last_today_date.strftime("%Y-%m-%d"),
            "Value Today": f"{last_today_val:,.4f}".rstrip("0").rstrip("."),
            "Late Values Today (After Known Date)": late_count,
            "Revised Values Since (Same Dates)": revised_count,
        })
        
        # Filter vintage data for the chart from start_date
        df_vintage_chart = df_vintage[df_vintage["observation_date"] >= start_date_ts].copy()

        series_data_cache[sid] = {
            "df_today_chart": df_today_chart,
            "df_vintage_chart": df_vintage_chart,
            "last_vintage_date": last_vintage_date,
            "last_vintage_val": last_vintage_val,
            "last_today_date": last_today_date,
            "last_today_val": last_today_val,
            "late_count": late_count,
            "revised_count": revised_count,
        }
        
    except Exception as e:
        st.error(f"❌ Error processing series `{sid}`: {str(e)}")

# -----------------------------------------------------------------------------
# Section 1: Charts
# -----------------------------------------------------------------------------

st.subheader("1. Series Charts & Point-in-Time Horizons")

if series_data_cache:
    for sid, sdata in series_data_cache.items():
        chart_df = sdata["df_today_chart"].copy()
        v_chart_df = sdata["df_vintage_chart"].copy()
        friendly_name = DEFAULT_SERIES.get(sid, sid)
        
        with st.container(border=True):
            # Header Row
            top_left, top_right = st.columns([4, 1])
            with top_left:
                st.markdown(f"#### **{sid}** — <span style='font-weight:400; color:#94A3B8;'>{friendly_name}</span>", unsafe_allow_html=True)
            with top_right:
                st.markdown(f"<div style='text-align:right;'><a href='https://fred.stlouisfed.org/series/{sid}' target='_blank' style='text-decoration:none;'>🔗 Open on FRED ↗</a></div>", unsafe_allow_html=True)
            
            # Executive KPI Cards
            c1, c2, c3, c4, c5 = st.columns(5)
            with c1:
                st.metric("📅 Last Known Then", sdata["last_vintage_date"].strftime("%Y-%m-%d"))
            with c2:
                st.metric("🔢 Value Known Then", f"{sdata['last_vintage_val']:,.4f}".rstrip("0").rstrip("."))
            with c3:
                st.metric("📈 Value Today", f"{sdata['last_today_val']:,.4f}".rstrip("0").rstrip("."))
            with c4:
                st.metric("⏳ Late Obs (Lag)", sdata["late_count"])
            with c5:
                rev_label = f"{sdata['revised_count']}" if sdata["revised_count"] == 0 else f"{sdata['revised_count']} ⚠️"
                st.metric("🔄 Revised Since", rev_label)
            
            if not chart_df.empty:
                # Legend and display mode indicator
                st.markdown(
                    f"<div style='font-size:0.85rem; color:#94A3B8; margin-bottom:8px;'>"
                    f"<span style='color:#38BDF8; font-weight:600;'>━ Today's Values (FRED)</span> &nbsp;&nbsp;|&nbsp;&nbsp; "
                    f"<span style='color:#F59E0B; font-weight:600;'>┅ Known on {vintage_date_str} (ALFRED)</span> &nbsp;&nbsp;|&nbsp;&nbsp; "
                    f"<span style='color:#EF4444; font-weight:600;'>┆ Cutoff Horizon ({sdata['last_vintage_date'].strftime('%Y-%m-%d')})</span>"
                    f"</div>",
                    unsafe_allow_html=True
                )
                
                # 1. Subtle Gradient Area under Today's Series
                area_chart = (
                    alt.Chart(chart_df)
                    .mark_area(
                        color=alt.Gradient(
                            gradient="linear",
                            stops=[
                                alt.GradientStop(color="rgba(56, 189, 248, 0.22)", offset=0),
                                alt.GradientStop(color="rgba(56, 189, 248, 0.01)", offset=1),
                            ],
                            x1=1, x2=1, y1=1, y2=0
                        )
                    )
                    .encode(x="observation_date:T", y="today_value:Q")
                )
                
                # 2. Main Today's Line
                today_line = (
                    alt.Chart(chart_df)
                    .mark_line(color="#38BDF8", strokeWidth=2.4)
                    .encode(
                        x=alt.X(
                            "observation_date:T",
                            title="Observation Date",
                            axis=alt.Axis(format="%b %Y", grid=True, gridColor="rgba(148, 163, 184, 0.12)", labelFontSize=11)
                        ),
                        y=alt.Y(
                            "today_value:Q",
                            title=f"{sid} Rate / Value",
                            scale=alt.Scale(zero=False),
                            axis=alt.Axis(grid=True, gridColor="rgba(148, 163, 184, 0.12)", labelFontSize=11)
                        ),
                        tooltip=[
                            alt.Tooltip("observation_date:T", title="Observation Date", format="%B %d, %Y"),
                            alt.Tooltip("today_value:Q", title="Value Today", format=",.4f")
                        ]
                    )
                )
                
                chart_layers = [area_chart, today_line]
                
                # 3. Vintage Overlay Line (if observations exist)
                if not v_chart_df.empty:
                    vintage_line = (
                        alt.Chart(v_chart_df)
                        .mark_line(color="#F59E0B", strokeDash=[5, 4], strokeWidth=2.2)
                        .encode(
                            x="observation_date:T",
                            y="vintage_value:Q",
                            tooltip=[
                                alt.Tooltip("observation_date:T", title="Observation Date", format="%B %d, %Y"),
                                alt.Tooltip("vintage_value:Q", title=f"Known on {vintage_date_str}", format=",.4f")
                            ]
                        )
                    )
                    chart_layers.append(vintage_line)
                
                # 4. Vertical Rule and Marker Dot at Point-in-Time Cutoff
                cutoff_ts = pd.to_datetime(sdata["last_vintage_date"])
                cutoff_data = pd.DataFrame({
                    "cutoff": [cutoff_ts],
                    "val": [sdata["last_vintage_val"]],
                    "label": [f"Known Cutoff: {cutoff_ts.strftime('%Y-%m-%d')} (Val: {sdata['last_vintage_val']})"]
                })
                
                cutoff_rule = (
                    alt.Chart(cutoff_data)
                    .mark_rule(color="#EF4444", strokeDash=[4, 3], strokeWidth=2.0)
                    .encode(x="cutoff:T")
                )
                cutoff_dot = (
                    alt.Chart(cutoff_data)
                    .mark_circle(size=85, color="#EF4444")
                    .encode(
                        x="cutoff:T",
                        y="val:Q",
                        tooltip=[
                            alt.Tooltip("cutoff:T", title="Cutoff Horizon Date", format="%B %d, %Y"),
                            alt.Tooltip("val:Q", title="Value Known Then", format=",.4f")
                        ]
                    )
                )
                chart_layers.extend([cutoff_rule, cutoff_dot])
                
                # Combine all chart layers
                composite_chart = (
                    alt.layer(*chart_layers)
                    .properties(height=330)
                    .interactive()
                )
                st.altair_chart(composite_chart, use_container_width=True)
                
                # 5. Mandated Subtext Caption
                st.caption(
                    f"ℹ️ **Point-in-Time Knowledge Cutoff:** On **{vintage_date_str}**, the latest observation known was "
                    f"**{sdata['last_vintage_date'].strftime('%Y-%m-%d')}** (value: **{sdata['last_vintage_val']}**). "
                    f"Today's series extends to **{sdata['last_today_date'].strftime('%Y-%m-%d')}** (value: **{sdata['last_today_val']}**)."
                )
            else:
                st.info(f"No observations found for {sid} after start date {start_date}.")
        st.markdown("---")

# -----------------------------------------------------------------------------
# Section 2: Audit Summary Table
# -----------------------------------------------------------------------------

st.subheader("2. Point-in-Time Audit & Revision Ledger")

if table_rows:
    display_df = pd.DataFrame(table_rows)
    
    # Render with Streamlit data table using LinkColumn
    st.dataframe(
        display_df,
        column_config={
            "FRED Page": st.column_config.LinkColumn("FRED Source", display_text="Open on FRED"),
            "Late Values Today (After Known Date)": st.column_config.NumberColumn(
                "Late Values (Lag)",
                help="How many values today's data has after the last date known on the vintage date"
            ),
            "Revised Values Since (Same Dates)": st.column_config.NumberColumn(
                "Revised Values",
                help="How many historical values on identical observation dates have changed between vintage and today"
            ),
        },
        use_container_width=True,
        hide_index=True,
    )
    
    # Also render clean markdown table for easy copy-paste / reading
    st.markdown("#### Tabular Summary (Markdown View)")
    md_header = "| Series ID | FRED Link | Last Date Known Then | Value Known Then | Last Date Measured Today | Value Today | Late Count | Revised Count |\n"
    md_header += "| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |\n"
    for r in table_rows:
        md_header += f"| **{r['Series ID']}** | [{r['Series ID']}]({r['FRED Page']}) | {r['Last Date Known Then']} | {r['Value Known Then']} | {r['Last Date Measured Today']} | {r['Value Today']} | {r['Late Values Today (After Known Date)']} | {r['Revised Values Since (Same Dates)']} |\n"
    st.markdown(md_header)
else:
    st.warning("No series successfully processed to display in the audit ledger.")

# -----------------------------------------------------------------------------
# Footer
# -----------------------------------------------------------------------------

st.markdown("---")
st.markdown(
    "**Course:** FIN 43900 — AI Finance Applications | **Student:** Oladapo Olaniyan (`oolaniy@purdue.edu`) | "
    "**Institution:** Mitchell E. Daniels, Jr. School of Business, Purdue University"
)
