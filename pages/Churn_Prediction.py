"""
pages/Churn_Prediction.py
=========================
Customer Churn Prediction Dashboard — Shalina Distribution Intelligence
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import sys, os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fabric_connector import load_data as _load_data
from src.churn_model import train, active_at_risk, RISK_COLORS, RISK_LABELS

# Page config is set by app.py — do not call set_page_config here

# ── SIDEBAR NAVIGATION ──────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div style="padding:20px 8px 10px 8px;">'
        '<div style="font-family:Inter,sans-serif;font-size:10px;font-weight:700;'
        'color:rgba(100,180,220,0.7);text-transform:uppercase;letter-spacing:2px;'
        'margin-bottom:20px;">Navigation</div></div>', unsafe_allow_html=True)
    st.page_link('app.py',                    label='Dashboard')
    st.page_link('pages/Command_Center.py',   label='Command Center')
    st.page_link('pages/RFM_Analysis.py',     label='RFM Analysis')
    st.page_link('pages/Churn_Prediction.py',  label='Churn Prediction')
    st.page_link('pages/Revenue_Forecast.py', label='Revenue Forecast')
    st.page_link('pages/Upload_Data.py',      label='Upload Data')
    st.markdown('<div style="margin-top:16px;padding:0 8px;">'
        '<div style="height:1px;background:linear-gradient(90deg,transparent,'
        'rgba(33,150,196,0.35),transparent);"></div></div>',
        unsafe_allow_html=True)
    import streamlit.components.v1 as _sc2
    _sc2.html('<script>(function(){'
        'function r(){var n=window.parent.document.querySelector("[data-testid=\\"stSidebarNav\\"]");'
        'if(n){n.remove();}else{setTimeout(r,200);}}'
        'r();setTimeout(r,800);setTimeout(r,2500);'
        '})();</script>', height=0)


# ── SHARED CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500&display=swap');
* { box-sizing: border-box; }
.stApp {
    font-family: 'Inter', sans-serif; color: #E2E8F0;
    background: #0d1526; min-height: 100vh;
}
.stApp::before {
    content: ''; position: fixed; inset: 0;
    background:
        radial-gradient(ellipse 80% 50% at 10% 0%,  rgba(20,100,220,0.22) 0%, transparent 60%),
        radial-gradient(ellipse 50% 40% at 90% 10%,  rgba(100,30,200,0.18) 0%, transparent 55%),
        radial-gradient(ellipse 60% 60% at 50% 100%, rgba(15,60,160,0.20) 0%, transparent 60%);
    pointer-events: none; z-index: 0;
}
.main .block-container {
    background: transparent; padding-top: 1.5rem;
    padding-left: 1.5rem; padding-right: 1.5rem;
    max-width: 1500px; position: relative; z-index: 1;
}
section[data-testid="stSidebar"] {
    background: rgba(8,13,26,0.95) !important;
    border-right: 1px solid rgba(255,255,255,0.06) !important;
}
section[data-testid="stSidebar"] * { color:#94A3B8 !important; font-family:'Inter',sans-serif !important; }
[data-testid="stDecoration"],
#MainMenu,footer { display:none !important; }
[data-testid="stToolbar"] { display:flex !important; background:transparent !important; }
header[data-testid="stHeader"] { background:transparent !important; }
[data-testid="collapsedControl"],[data-testid="stSidebarCollapseButton"],button[kind="header"] {
    display:flex !important;
    visibility:visible !important;
    opacity:1 !important;
    z-index:999999 !important;
}
[data-testid="stSidebarCollapseButton"] *,
[data-testid="collapsedControl"] *,
[data-testid="stExpandSidebarButton"] * { font-size:0 !important; }
[data-testid="stSidebarCollapseButton"]::before {
    content:"‹";
    color:#94A3B8;
    font-size:26px;
    line-height:1;
}
[data-testid="collapsedControl"]::before,
[data-testid="stExpandSidebarButton"]::before {
    content:"›";
    color:#94A3B8;
    font-size:26px;
    line-height:1;
}
[data-testid="stExpandSidebarButton"] {
    display:flex !important;
    visibility:visible !important;
    opacity:1 !important;
    position:fixed !important;
    top:16px !important;
    left:16px !important;
    width:34px !important;
    height:34px !important;
    min-width:34px !important;
    z-index:999999 !important;
    align-items:center !important;
    justify-content:center !important;
    background:rgba(8,13,26,0.82) !important;
    border:1px solid rgba(255,255,255,0.12) !important;
    border-radius:8px !important;
}

.page-header {
    padding: 20px 0 16px 0;
    border-bottom: 1px solid rgba(255,255,255,0.06);
    margin-bottom: 24px;
}
.page-eyebrow {
    font-size: 10px; font-weight: 600; letter-spacing: 3px;
    text-transform: uppercase; color: #475569; margin-bottom: 6px;
}
.page-title {
    font-size: 24px; font-weight: 800; color: #F1F5F9;
    letter-spacing: -0.5px;
}
.page-title span { color: #A855F7; }

.kpi-row { display:grid; grid-template-columns:repeat(4,1fr); gap:12px; margin-bottom:24px; }
.kpi-card {
    border-radius: 12px; padding: 20px 20px 16px 20px;
    position: relative; overflow: hidden; min-height: 110px;
    border: 1px solid rgba(255,255,255,0.08);
    transition: transform 0.2s ease;
}
.kpi-card:hover { transform: translateY(-2px); }
.kpi-card.mc-purple { background:linear-gradient(135deg,#0f0a1a 0%,#3b1f6e 100%); box-shadow:0 4px 24px rgba(139,92,246,0.15),inset 0 1px 0 rgba(139,92,246,0.2); border-color:rgba(139,92,246,0.25); }
.kpi-card.mc-red    { background:linear-gradient(135deg,#1a0505 0%,#5c1010 100%); box-shadow:0 4px 24px rgba(239,68,68,0.15),inset 0 1px 0 rgba(239,68,68,0.2);   border-color:rgba(239,68,68,0.25); }
.kpi-card.mc-amber  { background:linear-gradient(135deg,#1a1400 0%,#5c4500 100%); box-shadow:0 4px 24px rgba(245,158,11,0.15),inset 0 1px 0 rgba(245,158,11,0.2); border-color:rgba(245,158,11,0.25); }
.kpi-card.mc-green  { background:linear-gradient(135deg,#051a0f 0%,#0d5c2a 100%); box-shadow:0 4px 24px rgba(34,197,94,0.15),inset 0 1px 0 rgba(34,197,94,0.2);  border-color:rgba(34,197,94,0.25); }
.kpi-card.mc-blue   { background:linear-gradient(135deg,#0f172a 0%,#1e3a5f 100%); box-shadow:0 4px 24px rgba(59,130,246,0.15),inset 0 1px 0 rgba(59,130,246,0.2); border-color:rgba(59,130,246,0.25); }
.kpi-accent-line { height:2px; width:40px; border-radius:1px; margin-bottom:12px; }
.kpi-label { font-size:10px; font-weight:600; letter-spacing:1.5px; text-transform:uppercase; color:#64748B; margin-bottom:6px; }
.kpi-value { font-size:32px; font-weight:800; color:#F8FAFC; line-height:1; letter-spacing:-1px; }
.kpi-delta { font-size:11px; color:#475569; margin-top:6px; }

.section-title {
    font-size:11px; font-weight:700; letter-spacing:2px;
    text-transform:uppercase; color:#475569;
    margin-top:24px; margin-bottom:12px;
    display:flex; align-items:center; gap:10px;
}
.section-title::after {
    content:''; flex:1; height:1px;
    background:linear-gradient(90deg,rgba(255,255,255,0.08),transparent);
}

.risk-badge {
    display:inline-block; padding:3px 10px; border-radius:4px;
    font-size:10px; font-weight:700; letter-spacing:0.5px; text-transform:uppercase;
}
.risk-high   { background:rgba(239,68,68,0.12);  color:#FCA5A5; border:1px solid rgba(239,68,68,0.3); }
.risk-medium { background:rgba(245,158,11,0.12); color:#FCD34D; border:1px solid rgba(245,158,11,0.3); }
.risk-low    { background:rgba(34,197,94,0.12);  color:#86EFAC; border:1px solid rgba(34,197,94,0.3); }

.insight-card {
    background:rgba(255,255,255,0.025); border-radius:12px;
    padding:16px 20px; border:1px solid rgba(255,255,255,0.07);
    margin-bottom:10px;
}
.insight-title  { font-size:14px; font-weight:700; color:#F1F5F9; margin-bottom:4px; }
.insight-detail { font-size:12px; color:#64748B; line-height:1.6; }

.model-badge {
    display:inline-flex; align-items:center; gap:6px;
    background:rgba(139,92,246,0.1); border:1px solid rgba(139,92,246,0.3);
    border-radius:6px; padding:4px 12px;
    font-size:10px; font-weight:700; letter-spacing:1px;
    text-transform:uppercase; color:#C4B5FD; margin-bottom:20px;
}

[data-baseweb="select"] > div {
    background:rgba(255,255,255,0.04) !important;
    border:1px solid rgba(255,255,255,0.08) !important;
    border-radius:8px !important; color:#E2E8F0 !important;
}
[data-baseweb="select"] svg { fill:#475569 !important; }
[data-baseweb="popover"] { background:#0f172a !important; border:1px solid rgba(255,255,255,0.1) !important; }
[role="option"] { background:#0f172a !important; color:#E2E8F0 !important; }
[role="option"]:hover { background:rgba(139,92,246,0.15) !important; }
.stSelectbox label { color:#475569 !important; font-size:10px !important; font-weight:700 !important; text-transform:uppercase; letter-spacing:1px; }
[data-testid="stDataFrame"] { border-radius:10px !important; border:1px solid rgba(255,255,255,0.07) !important; }
.stDownloadButton > button { background:rgba(139,92,246,0.15) !important; color:#C4B5FD !important; border:1px solid rgba(139,92,246,0.3) !important; border-radius:8px !important; font-weight:600 !important; }
</style>
""", unsafe_allow_html=True)

# ── PAGE HEADER ───────────────────────────────────────────────────────────────
st.markdown("""
<div class="page-header">
    <div class="page-eyebrow">Shalina Healthcare &nbsp;&middot;&nbsp; Predictive Analytics</div>
    <div class="page-title">Customer <span>Churn</span> Prediction</div>
</div>
""", unsafe_allow_html=True)

# ── LOAD DATA ─────────────────────────────────────────────────────────────────
@st.cache_data(show_spinner=False)
def load():
    df, _, _ = _load_data()
    return df

df_all = load()
if df_all is None:
    st.error("No data available. Please check your data source.")
    st.stop()

# ── TRAIN MODEL (cached — only trains once per session) ──────────────────────
@st.cache_data(show_spinner=False)
def run_model(data_hash: int, _df: pd.DataFrame):
    return train(_df)

with st.spinner("Training churn model — this takes about 20 seconds on first load..."):
    _hash = hash(str(len(df_all)))
    model, scored_df, metrics = run_model(_hash, df_all)

_model_label = metrics.get("model_type", "XGBoost")
st.markdown(f"""
<div class="model-badge">
    <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor"
         stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/>
    </svg>
    {_model_label} &nbsp;&middot;&nbsp; 500 Trees &nbsp;&middot;&nbsp; scale_pos_weight
</div>
""", unsafe_allow_html=True)

# ── FILTERS ───────────────────────────────────────────────────────────────────
col_f1, col_f2, col_f3 = st.columns([1, 1, 4])
with col_f1:
    country_sel = st.selectbox("Country", ["All", "Nigeria", "Angola"])
with col_f2:
    risk_sel = st.selectbox("Risk Tier", ["All"] + RISK_LABELS)

# Apply filters
view = scored_df.copy()
if country_sel != "All":
    view = view[view["country"] == country_sel]
if risk_sel != "All":
    view = view[view["risk_tier"] == risk_sel]

active_view = active_at_risk(view)
total_view  = scored_df[scored_df["country"] == country_sel] if country_sel != "All" else scored_df

# Country-specific bounds for map
map_center = {"lat": 9.0, "lon": 8.0}  if country_sel == "Nigeria" else \
             {"lat":-11.0, "lon":17.5} if country_sel == "Angola"  else \
             {"lat":  1.5, "lon":12.0}
map_zoom   = 5 if country_sel != "All" else 3

# ── KPI CARDS ─────────────────────────────────────────────────────────────────
total_active  = len(scored_df[scored_df["ytd_value"] > 0])
high_risk_n   = len(active_at_risk(total_view if country_sel != "All" else scored_df)
                    [active_at_risk(total_view if country_sel != "All" else scored_df)["risk_tier"] == "High Risk"])
med_risk_n    = len(active_at_risk(total_view if country_sel != "All" else scored_df)
                    [active_at_risk(total_view if country_sel != "All" else scored_df)["risk_tier"] == "Medium Risk"])
rev_at_risk   = active_at_risk(total_view if country_sel != "All" else scored_df) \
                    [active_at_risk(total_view if country_sel != "All" else scored_df)["risk_tier"] == "High Risk"]["ytd_value"].sum()

st.markdown(f"""
<div class="kpi-row">
    <div class="kpi-card mc-purple">
        <div class="kpi-accent-line" style="background:linear-gradient(90deg,#8B5CF6,#A78BFA);"></div>
        <div class="kpi-label">Model AUC Score</div>
        <div class="kpi-value">{metrics['auc']}</div>
        <div class="kpi-delta">CV AUC {metrics['cv_auc_mean']} &plusmn; {metrics['cv_auc_std']}</div>
    </div>
    <div class="kpi-card mc-red">
        <div class="kpi-accent-line" style="background:linear-gradient(90deg,#EF4444,#F87171);"></div>
        <div class="kpi-label">High Risk Active Outlets</div>
        <div class="kpi-value">{high_risk_n:,}</div>
        <div class="kpi-delta">Churn probability &gt; 65%</div>
    </div>
    <div class="kpi-card mc-amber">
        <div class="kpi-accent-line" style="background:linear-gradient(90deg,#F59E0B,#FCD34D);"></div>
        <div class="kpi-label">Medium Risk Outlets</div>
        <div class="kpi-value">{med_risk_n:,}</div>
        <div class="kpi-delta">Churn probability 35&ndash;65%</div>
    </div>
    <div class="kpi-card mc-green">
        <div class="kpi-accent-line" style="background:linear-gradient(90deg,#22C55E,#4ADE80);"></div>
        <div class="kpi-label">Revenue at Risk</div>
        <div class="kpi-value">&#8358;{rev_at_risk/1000:,.0f}M</div>
        <div class="kpi-delta">YTD from high-risk active outlets</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── TWO COLUMN : Feature Importance + Risk Distribution ──────────────────────
c1, c2 = st.columns(2)

with c1:
    st.markdown('<div class="section-title">Feature Importance</div>', unsafe_allow_html=True)
    fi_df = pd.DataFrame(metrics["feat_imp"], columns=["Feature", "Importance"])
    fi_df["Importance_pct"] = (fi_df["Importance"] / fi_df["Importance"].sum() * 100).round(1)

    fig_fi = px.bar(
        fi_df, x="Importance_pct", y="Feature", orientation="h",
        color="Importance_pct",
        color_continuous_scale=[[0,"rgba(139,92,246,0.3)"], [1,"rgba(139,92,246,1)"]],
        text=fi_df["Importance_pct"].apply(lambda x: f"{x:.1f}%"),
    )
    fig_fi.update_traces(textposition="outside", textfont=dict(color="#94A3B8", size=10))
    fig_fi.update_coloraxes(showscale=False)
    fig_fi.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(255,255,255,0.02)",
        font=dict(color="#64748B", size=11), height=340,
        xaxis=dict(gridcolor="rgba(255,255,255,0.04)", showticklabels=False, title=""),
        yaxis=dict(gridcolor="rgba(255,255,255,0.04)", title=""),
        margin=dict(l=0, r=60, t=10, b=0),
    )
    st.plotly_chart(fig_fi, use_container_width=True)

with c2:
    st.markdown('<div class="section-title">Risk Tier Distribution (Active Outlets)</div>', unsafe_allow_html=True)
    _active_filtered = active_at_risk(total_view if country_sel != "All" else scored_df)
    risk_counts = _active_filtered["risk_tier"].value_counts().reset_index()
    risk_counts.columns = ["Tier", "Count"]

    fig_risk = px.pie(
        risk_counts, values="Count", names="Tier",
        color="Tier", color_discrete_map=RISK_COLORS, hole=0.55,
    )
    fig_risk.update_traces(
        textinfo="percent+label",
        textfont=dict(color="#E2E8F0", size=11),
    )
    fig_risk.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        legend=dict(font=dict(color="#94A3B8")),
        font=dict(color="#94A3B8"), height=340,
        margin=dict(l=0, r=0, t=10, b=0),
        annotations=[dict(
            text=f"{len(_active_filtered):,}<br><span style='font-size:10px'>Active</span>",
            x=0.5, y=0.5, font_size=18, font_color="#F1F5F9",
            showarrow=False,
        )]
    )
    st.plotly_chart(fig_risk, use_container_width=True)

# ── MODEL QUALITY ─────────────────────────────────────────────────────────────
st.markdown('<div class="section-title">Model Performance</div>', unsafe_allow_html=True)

mq1, mq2, mq3, mq4, mq5 = st.columns(5)
_metrics_items = [
    (mq1, "Accuracy",  f"{metrics['accuracy']*100:.1f}%",  "Overall correct predictions"),
    (mq2, "Precision", f"{metrics['precision_churn']*100:.1f}%", "Of flagged churners, actually churned"),
    (mq3, "Recall",    f"{metrics['recall_churn']*100:.1f}%",    "Of actual churners, correctly flagged"),
    (mq4, "F1 Score",  f"{metrics['f1_churn']:.3f}",             "Precision-Recall balance"),
    (mq5, "Base Churn Rate", f"{metrics['churn_rate_pct']}%",    f"{metrics['total_churned']:,} of {metrics['total_outlets']:,} outlets"),
]
for col, label, val, detail in _metrics_items:
    with col:
        st.markdown(f"""
        <div style="background:rgba(255,255,255,0.025);border:1px solid rgba(255,255,255,0.07);
             border-radius:10px;padding:14px 16px;text-align:center;">
            <div style="font-size:9px;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;
                 color:#475569;margin-bottom:6px;">{label}</div>
            <div style="font-size:22px;font-weight:800;color:#F1F5F9;letter-spacing:-0.5px;">
                {val}</div>
            <div style="font-size:10px;color:#64748B;margin-top:4px;line-height:1.4;">{detail}</div>
        </div>""", unsafe_allow_html=True)

# ── CHURN RISK MAP ────────────────────────────────────────────────────────────
st.markdown('<div class="section-title">Churn Risk Map &mdash; Active Outlets</div>',
            unsafe_allow_html=True)

# Validate coordinates before mapping
_BOUNDS = {
    "Nigeria": (2.5, 15.0, 2.5, 15.5),
    "Angola":  (-19.0, -3.5, 10.5, 25.5),
}

def _valid_coords(df, country_filter):
    mask = (
        df["latitude"].notna()  & df["longitude"].notna() &
        (df["latitude"]  != 0)  & (df["longitude"]  != 0) &
        (df["latitude"].abs()  > 0.01) &
        (df["longitude"].abs() > 0.01)
    )
    if country_filter != "All" and country_filter in _BOUNDS:
        lat_min, lat_max, lon_min, lon_max = _BOUNDS[country_filter]
        mask &= df["latitude"].between(lat_min, lat_max)
        mask &= df["longitude"].between(lon_min, lon_max)
    return df[mask]

map_active = _valid_coords(
    active_at_risk(total_view if country_sel != "All" else scored_df),
    country_sel
)
if risk_sel != "All":
    map_active = map_active[map_active["risk_tier"] == risk_sel]

map_sample = map_active.sample(min(6000, len(map_active)), random_state=42) \
             if len(map_active) > 6000 else map_active

if len(map_sample) > 0:
    map_sample = map_sample.copy()
    map_sample["churn_pct"] = (map_sample["churn_prob"] * 100).round(1)
    map_sample["_sz"] = (map_sample["churn_prob"] * 14 + 3).clip(3, 17)

    fig_map = px.scatter_mapbox(
        map_sample,
        lat="latitude", lon="longitude",
        color="risk_tier",
        color_discrete_map=RISK_COLORS,
        size="_sz", size_max=17,
        zoom=map_zoom, height=500,
        hover_name="Shop Name",
        hover_data={
            "churn_pct":      ":.1f",
            "risk_tier":      True,
            "ytd_value":      ":,.1f",
            "Retailer Subtype": True,
            "latitude":  False,
            "longitude": False,
            "_sz":       False,
        },
        labels={"churn_pct": "Churn Prob (%)", "ytd_value": "YTD Revenue (K)"},
        center=map_center,
        category_orders={"risk_tier": RISK_LABELS},
    )
    fig_map.update_layout(
        mapbox_style="carto-darkmatter",
        paper_bgcolor="rgba(0,0,0,0)",
        legend=dict(
            font=dict(color="#94A3B8", size=11),
            bgcolor="rgba(8,13,26,0.85)",
            bordercolor="rgba(255,255,255,0.08)",
            borderwidth=1,
            title=dict(text="Churn Risk", font=dict(color="#94A3B8")),
        ),
        margin=dict(l=0, r=0, t=0, b=0),
    )
    st.plotly_chart(fig_map, use_container_width=True)
else:
    st.markdown(
        '<div style="background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.07);'
        'border-radius:10px;padding:20px;text-align:center;color:#64748B;font-size:13px;">'
        'No outlets with valid GPS coordinates match the current filters.</div>',
        unsafe_allow_html=True
    )

# ── TOP AT-RISK TABLE ─────────────────────────────────────────────────────────
st.markdown('<div class="section-title">Top At-Risk Active Outlets</div>', unsafe_allow_html=True)

_display = active_at_risk(total_view if country_sel != "All" else scored_df).copy()
if risk_sel != "All":
    _display = _display[_display["risk_tier"] == risk_sel]

_display = _display.head(100)[[
    "Shop Name", "country", "Retailer Subtype",
    "ytd_value", "churn_prob", "risk_tier",
    "neighbor_churn_rate", "ytd_pct_country",
]].rename(columns={
    "Shop Name":            "Outlet",
    "country":              "Country",
    "Retailer Subtype":     "Type",
    "ytd_value":            "YTD Revenue (K)",
    "churn_prob":           "Churn Probability",
    "risk_tier":            "Risk Tier",
    "neighbor_churn_rate":  "Neighbourhood Churn Rate",
    "ytd_pct_country":      "Percentile in Country",
}).reset_index(drop=True)

_display.index += 1
_display["YTD Revenue (K)"]          = _display["YTD Revenue (K)"].apply(lambda x: f"\u20a6{x:,.1f}K")
_display["Churn Probability"]        = _display["Churn Probability"].apply(lambda x: f"{x*100:.1f}%")
_display["Neighbourhood Churn Rate"] = _display["Neighbourhood Churn Rate"].apply(lambda x: f"{x*100:.0f}%")
_display["Percentile in Country"]    = _display["Percentile in Country"].apply(lambda x: f"{x*100:.0f}th")

st.dataframe(_display, use_container_width=True)

# ── PRE-CHURN ALERTS ──────────────────────────────────────────────────────────
# Active outlets with a negative 3-month sales trend — these are NOT yet
# flagged as High Risk by the model but are visibly declining.
_pre_churn = scored_df[
    (scored_df["ytd_value"] > 0) &
    (scored_df["ytd_3m_trend"] < 0) &
    (~scored_df["risk_tier"].isin(["High Risk"]))
].copy()
if country_sel != "All":
    _pre_churn = _pre_churn[_pre_churn["country"] == country_sel]

if len(_pre_churn) > 0:
    st.markdown('<div class="section-title">Pre-Churn Alerts — Active but Declining</div>',
                unsafe_allow_html=True)
    st.markdown(f"""
    <div style="background:rgba(249,115,22,0.07);border:1px solid rgba(249,115,22,0.25);
         border-radius:12px;padding:14px 20px;margin-bottom:14px;display:flex;align-items:center;gap:14px;">
        <div style="font-size:24px;">⚠️</div>
        <div>
            <div style="font-size:13px;font-weight:700;color:#FDBA74;margin-bottom:3px;">
                {len(_pre_churn):,} outlets are currently active but have a declining 3-month revenue trend</div>
            <div style="font-size:11px;color:#64748B;">
                These outlets are not yet High Risk but are showing early churn signals.
                Early intervention now is cheaper than retention later.
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    _pc_display = _pre_churn.sort_values("ytd_3m_trend").head(50)[[
        "Shop Name", "country", "Retailer Subtype", "ytd_value",
        "ytd_3m_trend", "risk_tier", "churn_prob",
    ]].rename(columns={
        "Shop Name":        "Outlet",
        "country":          "Country",
        "Retailer Subtype": "Type",
        "ytd_value":        "YTD Revenue (K)",
        "ytd_3m_trend":     "3M Sales Slope",
        "risk_tier":        "Current Risk",
        "churn_prob":       "Churn Prob",
    }).reset_index(drop=True)
    _pc_display.index += 1
    _pc_display["YTD Revenue (K)"] = _pc_display["YTD Revenue (K)"].apply(lambda x: f"₦{x:,.1f}K")
    _pc_display["3M Sales Slope"]  = _pc_display["3M Sales Slope"].apply(lambda x: f"{x:+.1f}")
    _pc_display["Churn Prob"]      = _pc_display["Churn Prob"].apply(lambda x: f"{x*100:.1f}%")
    st.dataframe(_pc_display, use_container_width=True)

# ── EXPORT BUTTONS ────────────────────────────────────────────────────────────
st.markdown('<div class="section-title">Export</div>', unsafe_allow_html=True)

_export_df = active_at_risk(total_view if country_sel != "All" else scored_df)[[
    "Shop Name", "country", "Retailer Subtype",
    "ytd_value", "churn_prob", "risk_tier",
    "neighbor_churn_rate", "ytd_pct_country",
]]

exp_col1, exp_col2, exp_col3 = st.columns([1, 1, 4])

with exp_col1:
    csv_export = _export_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        "⬇ Download CSV",
        csv_export,
        f"churn_risk_{country_sel.lower()}.csv",
        "text/csv",
        use_container_width=True,
    )

with exp_col2:
    import io
    _xl_buf = io.BytesIO()
    with pd.ExcelWriter(_xl_buf, engine="openpyxl") as _xw:
        _export_df.to_excel(_xw, index=False, sheet_name="At-Risk Outlets")
        if len(_pre_churn) > 0:
            _pre_churn[[
                "Shop Name", "country", "Retailer Subtype",
                "ytd_value", "ytd_3m_trend", "risk_tier", "churn_prob",
            ]].to_excel(_xw, index=False, sheet_name="Pre-Churn Alerts")
    _xl_buf.seek(0)
    st.download_button(
        "⬇ Download Excel",
        _xl_buf,
        f"churn_risk_{country_sel.lower()}.xlsx",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True,
    )

# ── WRITE-BACK TO FABRIC ──────────────────────────────────────────────────────
st.markdown('<div class="section-title">Fabric Write-Back</div>', unsafe_allow_html=True)
st.markdown("""
<div style="background:rgba(59,130,246,0.06);border:1px solid rgba(59,130,246,0.2);
     border-radius:12px;padding:14px 20px;margin-bottom:12px;">
    <div style="font-size:12px;color:#93C5FD;font-weight:600;margin-bottom:4px;">
        Save predictions back to your Fabric warehouse</div>
    <div style="font-size:11px;color:#64748B;line-height:1.6;">
        This creates a <code style="color:#93C5FD">ChurnPredictions</code> table in your Fabric warehouse
        so these scores are available in Power BI and other tools.
        Requires FABRIC_SQL_ENDPOINT to be configured.
    </div>
</div>
""", unsafe_allow_html=True)

if st.button("Push Churn Predictions to Fabric", use_container_width=False,
             key="btn_write_back_churn"):
    with st.spinner("Writing predictions to Fabric warehouse..."):
        from fabric_connector import write_churn_predictions
        result = write_churn_predictions(scored_df)
    if result["success"]:
        st.success(f"✅ {result['rows_written']:,} outlet predictions written to "
                   f"[dbo].[ChurnPredictions] in Fabric.")
    else:
        st.error(f"❌ Write-back failed: {result['error']}")

# ── STRATEGIC INSIGHTS ────────────────────────────────────────────────────────
st.markdown('<div class="section-title">Retention Strategy</div>', unsafe_allow_html=True)

_all_active   = active_at_risk(scored_df)
_hr_outlets   = _all_active[_all_active["risk_tier"] == "High Risk"]
_hr_primary   = _hr_outlets[_hr_outlets["is_primary"] == 1]
_hr_secondary = _hr_outlets[_hr_outlets["is_primary"] == 0]
_hr_rev       = _hr_outlets["ytd_value"].sum()
_hr_rev_prim  = _hr_primary["ytd_value"].sum()
_top_zone     = (
    _hr_outlets["geo_cluster"].value_counts().idxmax()
    if len(_hr_outlets) > 0 else "N/A"
)
_zone_count   = (
    int(_hr_outlets["geo_cluster"].value_counts().max())
    if len(_hr_outlets) > 0 else 0
)

st.markdown(f"""
<div class="insight-card">
    <span style="display:inline-block;padding:3px 10px;border-radius:4px;font-size:10px;
         font-weight:700;letter-spacing:0.5px;text-transform:uppercase;margin-bottom:8px;
         background:rgba(239,68,68,0.12);color:#FCA5A5;border:1px solid rgba(239,68,68,0.3);">
        Immediate Action</span>
    <div class="insight-title">
        {len(_hr_primary):,} High-Risk Primary Outlets Need Urgent Attention</div>
    <div class="insight-detail">
        These are primary trade channels currently active but showing strong churn signals.
        Combined YTD revenue at stake:
        <strong style="color:#FFFFFF">&#8358;{_hr_rev_prim/1000:,.0f}M</strong>.
        Assign dedicated field reps for personal engagement visits within the next 30 days.
    </div>
</div>
<div class="insight-card">
    <span style="display:inline-block;padding:3px 10px;border-radius:4px;font-size:10px;
         font-weight:700;letter-spacing:0.5px;text-transform:uppercase;margin-bottom:8px;
         background:rgba(245,158,11,0.12);color:#FCD34D;border:1px solid rgba(245,158,11,0.3);">
        Geographic Focus</span>
    <div class="insight-title">
        Cluster Zone {_top_zone} Has the Highest Concentration of At-Risk Outlets</div>
    <div class="insight-detail">
        {_zone_count:,} high-risk outlets cluster in a single geographic zone &mdash;
        indicating a localised distribution or relationship breakdown. A targeted area
        blitz by regional sales would be more efficient than scattered individual visits.
    </div>
</div>
<div class="insight-card">
    <span style="display:inline-block;padding:3px 10px;border-radius:4px;font-size:10px;
         font-weight:700;letter-spacing:0.5px;text-transform:uppercase;margin-bottom:8px;
         background:rgba(59,130,246,0.12);color:#93C5FD;border:1px solid rgba(59,130,246,0.3);">
        Revenue Protection</span>
    <div class="insight-title">
        &#8358;{_hr_rev/1000:,.0f}M YTD Revenue at Risk Across {len(_hr_outlets):,} Outlets</div>
    <div class="insight-detail">
        If all high-risk active outlets churn, this is the revenue exposure.
        Even retaining 50% of at-risk outlets would protect
        <strong style="color:#FFFFFF">&#8358;{_hr_rev/2000:,.0f}M</strong>.
        Prioritise by current YTD value &mdash; use the export above sorted by revenue.
    </div>
</div>
""", unsafe_allow_html=True)
