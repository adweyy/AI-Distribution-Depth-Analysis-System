import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import os

st.set_page_config(
    layout="wide",
    page_title="Shalina | Distribution Intelligence",
    initial_sidebar_state="expanded"
)

# ── SESSION STATE INIT ────────────────────────────────────────────
if "country"         not in st.session_state: st.session_state.country         = "Nigeria"
if "nav_page"        not in st.session_state: st.session_state.nav_page        = "Dashboard"
if "selected_outlet" not in st.session_state: st.session_state.selected_outlet = None

# ── SIDEBAR PART 1 : Navigation links ────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="padding:20px 8px 10px 8px;">
        <div style="font-family:'Inter',sans-serif;font-size:10px;font-weight:700;
             color:rgba(100,180,220,0.7);text-transform:uppercase;letter-spacing:2px;margin-bottom:20px;">
            Navigation
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.page_link("app.py",                    label="Dashboard")
    st.page_link("pages/Command_Center.py",   label="Command Center")
    st.page_link("pages/RFM_Analysis.py",     label="RFM Analysis")
    st.page_link("pages/Churn_Prediction.py",  label="Churn Prediction")
    st.page_link("pages/Revenue_Forecast.py",  label="Revenue Forecast")
    st.page_link("pages/Upload_Data.py",       label="Upload Data")

    st.markdown("""
    <div style="margin-top:16px;padding:0 8px;">
        <div style="height:1px;background:linear-gradient(90deg,transparent,
             rgba(33,150,196,0.35),transparent);"></div>
    </div>""", unsafe_allow_html=True)

    st.markdown("""
    <div style='margin-top:16px;padding:0 8px;font-family:Inter,sans-serif;font-size:10px;
         font-weight:700;color:rgba(100,180,220,0.7);text-transform:uppercase;letter-spacing:2px;'>
         Data
    </div>""", unsafe_allow_html=True)

    if st.button("Refresh Data", use_container_width=True, key="refresh_data"):
        st.cache_data.clear()
        st.rerun()

    import streamlit.components.v1 as _sc
    _sc.html("""<script>(function(){
        function r(){var n=window.parent.document.querySelector('[data-testid="stSidebarNav"]');
        if(n){n.remove();}else{setTimeout(r,200);}}
        r();setTimeout(r,800);setTimeout(r,2500);
    })();</script>""", height=0)

# ── GLOBAL CSS ────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500&display=swap');
* { box-sizing: border-box; }

.stApp {
    font-family: 'Inter', sans-serif;
    color: #E2E8F0;
    background: #0d1526;
    min-height: 100vh;
    position: relative;
}
.stApp::before {
    content: '';
    position: fixed; inset: 0;
    background:
        radial-gradient(ellipse 80% 50% at 10% 0%,  rgba(20,100,220,0.22) 0%, transparent 60%),
        radial-gradient(ellipse 50% 40% at 90% 10%,  rgba(100,30,200,0.18) 0%, transparent 55%),
        radial-gradient(ellipse 60% 60% at 50% 100%, rgba(15,60,160,0.20) 0%, transparent 60%);
    pointer-events: none; z-index: 0;
}
.main .block-container {
    background: transparent;
    padding-top: 0rem; padding-left: 1.5rem; padding-right: 1.5rem;
    max-width: 1500px; position: relative; z-index: 1;
}
section[data-testid="stSidebar"] {
    background: rgba(8,13,26,0.95) !important;
    border-right: 1px solid rgba(255,255,255,0.06) !important;
}
section[data-testid="stSidebar"] * { color: #94A3B8 !important; font-family: 'Inter', sans-serif !important; }
section[data-testid="stSidebar"] a:hover { color: #fff !important; background: rgba(255,255,255,0.06) !important; border-radius: 8px !important; }
[data-testid="stSidebarNav"],[data-testid="stSidebarNavItems"],section[data-testid="stSidebar"] nav { display:none !important; }
[data-testid="stDecoration"],#MainMenu,footer { display:none !important; }
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

.mc-topbar { display:flex; align-items:center; justify-content:space-between; padding:14px 0 10px 0; border-bottom:1px solid rgba(255,255,255,0.06); margin-bottom:16px; }
.mc-eyebrow { font-size:10px; font-weight:600; letter-spacing:3px; text-transform:uppercase; color:#475569; margin-bottom:4px; }
.mc-title   { font-size:22px; font-weight:800; color:#F1F5F9; letter-spacing:-0.5px; line-height:1.1; }
.mc-title span { color:#3B82F6; }
.mc-status-group { display:flex; gap:16px; align-items:center; }
.mc-status-pill { display:flex; align-items:center; gap:7px; background:rgba(255,255,255,0.04); border:1px solid rgba(255,255,255,0.08); border-radius:20px; padding:5px 12px; font-size:10px; font-weight:700; letter-spacing:1.5px; text-transform:uppercase; color:#94A3B8; }
.mc-status-dot { width:7px; height:7px; border-radius:50%; background:#22C55E; box-shadow:0 0 8px rgba(34,197,94,0.8),0 0 16px rgba(34,197,94,0.4); animation:statusPulse 2s ease-in-out infinite; }
.mc-status-dot.amber { background:#F59E0B; box-shadow:0 0 8px rgba(245,158,11,0.8),0 0 16px rgba(245,158,11,0.4); }
@keyframes statusPulse { 0%,100%{opacity:1;} 50%{opacity:0.4;} }

.kpi-row { display:grid; grid-template-columns:repeat(4,1fr); gap:12px; margin-bottom:20px; }
.kpi-card { border-radius:12px; padding:20px 20px 16px 20px; position:relative; overflow:hidden; min-height:120px; border:1px solid rgba(255,255,255,0.08); transition:transform 0.2s ease,box-shadow 0.2s ease; cursor:default; }
.kpi-card:hover { transform:translateY(-3px); }
.kpi-card::before { content:''; position:absolute; top:-60px; right:-60px; width:180px; height:180px; border-radius:50%; background:rgba(255,255,255,0.04); pointer-events:none; }
.kpi-card.mc-blue   { background:linear-gradient(135deg,#0f172a 0%,#1e3a5f 100%); box-shadow:0 4px 24px rgba(59,130,246,0.15),inset 0 1px 0 rgba(59,130,246,0.2);   border-color:rgba(59,130,246,0.25); }
.kpi-card.mc-orange { background:linear-gradient(135deg,#1a0f00 0%,#5c2400 100%); box-shadow:0 4px 24px rgba(249,115,22,0.15),inset 0 1px 0 rgba(249,115,22,0.2);  border-color:rgba(249,115,22,0.25); }
.kpi-card.mc-purple { background:linear-gradient(135deg,#0f0a1a 0%,#3b1f6e 100%); box-shadow:0 4px 24px rgba(139,92,246,0.15),inset 0 1px 0 rgba(139,92,246,0.2);  border-color:rgba(139,92,246,0.25); }
.kpi-card.mc-amber  { background:linear-gradient(135deg,#1a1400 0%,#5c4500 100%); box-shadow:0 4px 24px rgba(245,158,11,0.15),inset 0 1px 0 rgba(245,158,11,0.2);  border-color:rgba(245,158,11,0.25); }
.kpi-card.mc-red    { background:linear-gradient(135deg,#1a0505 0%,#5c1010 100%); box-shadow:0 4px 24px rgba(239,68,68,0.15),inset 0 1px 0 rgba(239,68,68,0.2);    border-color:rgba(239,68,68,0.25); }
.kpi-card.mc-green  { background:linear-gradient(135deg,#051a0f 0%,#0d5c2a 100%); box-shadow:0 4px 24px rgba(34,197,94,0.15),inset 0 1px 0 rgba(34,197,94,0.2);   border-color:rgba(34,197,94,0.25); }
.kpi-accent-line { height:2px; width:40px; border-radius:1px; margin-bottom:12px; }
.kpi-label { font-size:10px; font-weight:600; letter-spacing:1.5px; text-transform:uppercase; color:#64748B; margin-bottom:6px; }
.kpi-value { font-size:36px; font-weight:800; color:#F8FAFC; line-height:1; letter-spacing:-1px; }
.kpi-delta { font-size:11px; color:#475569; margin-top:6px; }

.section-title { font-size:11px; font-weight:700; letter-spacing:2px; text-transform:uppercase; color:#475569; margin-top:24px; margin-bottom:12px; display:flex; align-items:center; gap:10px; }
.section-title::after { content:''; flex:1; height:1px; background:linear-gradient(90deg,rgba(255,255,255,0.08),transparent); }

.insight-card { background:rgba(255,255,255,0.025); border-radius:12px; padding:16px 20px; border:1px solid rgba(255,255,255,0.07); margin-bottom:10px; transition:border-color 0.2s,background 0.2s; }
.insight-card:hover { background:rgba(255,255,255,0.04); border-color:rgba(255,255,255,0.12); }
.insight-title  { font-size:14px; font-weight:700; color:#F1F5F9; margin-bottom:4px; }
.insight-detail { font-size:12px; color:#64748B; line-height:1.6; }

.badge { display:inline-block; padding:3px 10px; border-radius:4px; font-size:10px; font-weight:700; margin-bottom:8px; letter-spacing:0.5px; text-transform:uppercase; }
.badge-dead  { background:rgba(239,68,68,0.12);  color:#FCA5A5; border:1px solid rgba(239,68,68,0.3); }
.badge-under { background:rgba(249,115,22,0.12); color:#FDBA74; border:1px solid rgba(249,115,22,0.3); }
.badge-low   { background:rgba(59,130,246,0.12); color:#93C5FD; border:1px solid rgba(59,130,246,0.3); }
.badge-high  { background:rgba(139,92,246,0.12); color:#C4B5FD; border:1px solid rgba(139,92,246,0.3); }

.odc-wrap { background:linear-gradient(135deg,rgba(15,25,50,0.95),rgba(20,35,70,0.9)); border:1px solid rgba(59,130,246,0.3); border-radius:14px; padding:20px 24px 16px 24px; margin-bottom:20px; box-shadow:0 8px 40px rgba(59,130,246,0.12),inset 0 1px 0 rgba(255,255,255,0.06); position:relative; overflow:hidden; }
.odc-wrap::before { content:''; position:absolute; top:-80px; right:-80px; width:240px; height:240px; border-radius:50%; background:radial-gradient(circle,rgba(59,130,246,0.08) 0%,transparent 70%); pointer-events:none; }
.odc-eyebrow { font-size:9px; font-weight:700; letter-spacing:2.5px; text-transform:uppercase; color:#3B82F6; margin-bottom:6px; }
.odc-name    { font-size:20px; font-weight:800; color:#F1F5F9; letter-spacing:-0.4px; line-height:1.1; }
.odc-meta    { display:flex; gap:8px; align-items:center; margin-top:8px; margin-bottom:16px; padding-bottom:16px; border-bottom:1px solid rgba(255,255,255,0.06); flex-wrap:wrap; }
.odc-stats   { display:flex; align-items:center; gap:0; margin-bottom:4px; }
.odc-stat    { flex:1; padding:0 20px; }
.odc-stat:first-child { padding-left:0; }
.odc-divider { width:1px; height:40px; background:rgba(255,255,255,0.07); flex-shrink:0; }
.odc-stat-label { font-size:9px; font-weight:700; letter-spacing:1.5px; text-transform:uppercase; color:#475569; margin-bottom:6px; }
.odc-stat-value { font-size:22px; font-weight:800; letter-spacing:-0.5px; line-height:1; }

section[data-testid="stSidebar"] .stTextInput input {
    background: #0d1f3c !important;
    border: 1px solid rgba(59,130,246,0.35) !important;
    border-radius: 8px !important;
    color: #E2E8F0 !important;
    font-size: 12px !important;
    caret-color: #60A5FA !important;
    box-shadow: inset 0 1px 4px rgba(0,0,0,0.4) !important;
}
section[data-testid="stSidebar"] .stTextInput input:focus {
    border-color: rgba(59,130,246,0.7) !important;
    box-shadow: inset 0 1px 4px rgba(0,0,0,0.4), 0 0 0 2px rgba(59,130,246,0.15) !important;
    outline: none !important;
}
section[data-testid="stSidebar"] .stTextInput input::placeholder {
    color: #4A6080 !important;
    font-style: italic;
}
section[data-testid="stSidebar"] .stTextInput > div,
section[data-testid="stSidebar"] .stTextInput > div > div { background:transparent !important; }
section[data-testid="stSidebar"] .stSelectbox [data-baseweb="select"] > div { background:rgba(255,255,255,0.04) !important; border:1px solid rgba(255,255,255,0.08) !important; border-radius:8px !important; }

div[data-testid="stHorizontalBlock"] div[data-testid="column"] .stButton > button { background:rgba(255,255,255,0.04) !important; color:#94A3B8 !important; border:1px solid rgba(255,255,255,0.08) !important; border-radius:8px !important; font-weight:600 !important; font-size:13px !important; width:100% !important; transition:all 0.2s ease !important; }
div[data-testid="stHorizontalBlock"] div[data-testid="column"] .stButton > button:hover { background:rgba(59,130,246,0.15) !important; border-color:rgba(59,130,246,0.4) !important; color:#E2E8F0 !important; }

.stSelectbox label { color:#475569 !important; font-size:10px !important; font-weight:700 !important; text-transform:uppercase; letter-spacing:1px; }
[data-baseweb="select"] > div { background:rgba(255,255,255,0.04) !important; border:1px solid rgba(255,255,255,0.08) !important; border-radius:8px !important; color:#E2E8F0 !important; }
[data-baseweb="select"] svg { fill:#475569 !important; }
[data-baseweb="popover"] { background:#0f172a !important; border:1px solid rgba(255,255,255,0.1) !important; }
[role="option"] { background:#0f172a !important; color:#E2E8F0 !important; }
[role="option"]:hover { background:rgba(59,130,246,0.15) !important; }

[data-testid="stImageContainer"] button,[data-testid="StyledFullScreenButton"] { display:none !important; }
[data-testid="stDataFrame"] { border-radius:10px !important; border:1px solid rgba(255,255,255,0.07) !important; }
.stDownloadButton > button { background:rgba(59,130,246,0.15) !important; color:#93C5FD !important; border:1px solid rgba(59,130,246,0.3) !important; border-radius:8px !important; font-weight:600 !important; }
.stDownloadButton > button:hover { background:rgba(59,130,246,0.25) !important; }

.ds-banner { background:transparent; border:1px solid rgba(255,255,255,0.06); border-radius:10px; padding:10px 16px; margin-bottom:14px; display:flex; align-items:center; gap:14px; }

.shalina-reveal { opacity:0; transform:translateY(40px) scale(0.98); transition:opacity 0.7s cubic-bezier(.16,1,.3,1),transform 0.7s cubic-bezier(.16,1,.3,1); will-change:opacity,transform; }
.shalina-reveal.visible { opacity:1; transform:translateY(0) scale(1); }
.shalina-reveal:nth-child(2){transition-delay:0.08s;} .shalina-reveal:nth-child(3){transition-delay:0.16s;} .shalina-reveal:nth-child(4){transition-delay:0.24s;}
</style>
""", unsafe_allow_html=True)

# ── LOAD DATA ─────────────────────────────────────────────────────
import sys, os as _os
sys.path.insert(0, _os.path.dirname(__file__))
from fabric_connector import load_data as _load_data

df_all, data_source, data_status = _load_data()

if df_all is None:
    st.markdown(
        '<div style="background:rgba(200,50,50,0.2);border:1px solid rgba(255,80,80,0.4);'
        'border-radius:12px;padding:16px 20px;color:#FFAAAA;font-weight:600;font-size:13px;">'
        'No data available. Please add shalina_combined_data.csv or configure Fabric credentials in .env'
        '</div>', unsafe_allow_html=True
    )
    st.stop()

# ── HELPERS ───────────────────────────────────────────────────────
def get_stats(df):
    nonzero = df[df['YTD Retailing Value'] > 0]['YTD Retailing Value']
    p25  = nonzero.quantile(0.25) if len(nonzero) else 0
    mean = nonzero.mean()         if len(nonzero) else 0
    p75  = nonzero.quantile(0.75) if len(nonzero) else 0
    return p25, mean, p75

def gps_quality(df, country):
    """Return (valid_count, total_count, pct_valid) for a country dataframe."""
    _bounds_map = {
        "Nigeria": dict(lat_min=2.5, lat_max=15.0, lon_min=2.5,  lon_max=15.5),
        "Angola":  dict(lat_min=-19.0,lat_max=-3.5,lon_min=10.5, lon_max=25.5),
    }
    b = _bounds_map.get(country, dict(lat_min=-90,lat_max=90,lon_min=-180,lon_max=180))
    valid = df[
        df['latitude'].notna()  & df['longitude'].notna() &
        (df['latitude']  != 0)  & (df['longitude']  != 0) &
        (df['latitude'].abs()  > 0.01) &
        (df['longitude'].abs() > 0.01) &
        df['latitude'].between(b['lat_min'],  b['lat_max']) &
        df['longitude'].between(b['lon_min'], b['lon_max'])
    ]
    total = max(len(df), 1)
    return len(valid), len(df), round(len(valid) / total * 100, 1)

def delta_html(value, low, high, reverse=False, prefix="", suffix="",
               label_lo="low", label_mid="moderate", label_hi="strong"):
    if reverse:
        if value > high:   color, arrow, lbl = "#EF4444", "&#8593;", label_hi
        elif value > low:  color, arrow, lbl = "#F59E0B", "&#8593;", label_mid
        else:              color, arrow, lbl = "#22C55E", "&#8595;", label_lo
    else:
        if value >= high:  color, arrow, lbl = "#22C55E", "&#8593;", label_hi
        elif value >= low: color, arrow, lbl = "#F59E0B", "&#8594;", label_mid
        else:              color, arrow, lbl = "#EF4444", "&#8595;", label_lo
    return (f'<span style="color:{color};font-weight:700;">{arrow} '
            f'{prefix}{value:.1f}{suffix}</span>'
            f'<span style="color:{color};opacity:0.75;"> &mdash; {lbl}</span>')

color_map = {
    'Dead Whitespace': '#EF4444',
    'Underperforming': '#F97316',
    'Low Performer':   '#EAB308',
    'Active':          '#22C55E',
    'High Performer':  '#A855F7'
}
chart_layout = dict(
    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(255,255,255,0.02)",
    font=dict(color="#64748B", size=11), height=380,
    xaxis=dict(gridcolor="rgba(255,255,255,0.04)", linecolor="rgba(255,255,255,0.06)", color="#64748B"),
    yaxis=dict(gridcolor="rgba(255,255,255,0.04)", linecolor="rgba(255,255,255,0.06)", color="#64748B"),
    margin=dict(l=0, r=0, t=20, b=0),
    legend=dict(font=dict(color="#94A3B8"), bgcolor="rgba(8,13,26,0.8)",
                bordercolor="rgba(255,255,255,0.08)", borderwidth=1)
)

# ── SIDEBAR PART 2 : Outlet Search ────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="margin-top:20px;padding:0 8px;">
        <div style="height:1px;background:linear-gradient(90deg,transparent,rgba(33,150,196,0.35),transparent);"></div>
    </div>""", unsafe_allow_html=True)
    st.markdown("""
    <div style='margin-top:16px;padding:0 8px;font-family:Inter,sans-serif;font-size:10px;
         font-weight:700;color:rgba(100,180,220,0.7);text-transform:uppercase;
         letter-spacing:2px;margin-bottom:8px;'>Outlet Search</div>
    """, unsafe_allow_html=True)

    search_q   = st.text_input("", placeholder="Type a shop name...",
                               key="outlet_search_input", label_visibility="collapsed")
    _s_country = st.session_state.get("country", "Nigeria")
    _s_df      = df_all[df_all['country'] == _s_country]

    if search_q and len(search_q) >= 2:
        _matches = _s_df[_s_df['Shop Name'].str.contains(search_q, case=False, na=False)]
        if len(_matches) > 0:
            _names  = _matches['Shop Name'].tolist()[:20]
            _chosen = st.selectbox("", _names, key="outlet_pick", label_visibility="collapsed")
            if st.button("View Details", key="btn_view_outlet", use_container_width=True):
                st.session_state.selected_outlet = _chosen
                st.rerun()
        else:
            st.markdown(
                "<div style='color:#64748B;font-size:11px;padding:4px 0 0 2px;'>No outlets found.</div>",
                unsafe_allow_html=True
            )

    if st.session_state.selected_outlet:
        if st.button("Clear Drill-down", key="btn_clear_outlet", use_container_width=True):
            st.session_state.selected_outlet = None
            st.rerun()

# ── TOP BAR ───────────────────────────────────────────────────────
sync_label = "DATA SYNC: STABLE" if data_status in ("live","hybrid") else "DATA SYNC: CSV"

import base64 as _b64
_logo_file = next(
    (f for f in ['shalina_healthcare_logo.jfif','shalina_healthcare_logo.png','shalina_logo.png']
     if _os.path.exists(f)), None
)
if _logo_file:
    _logo_ext  = 'jpeg' if _logo_file.endswith('.jfif') else 'png'
    _logo_b64  = _b64.b64encode(open(_logo_file,'rb').read()).decode()
    _logo_mime = f'image/{_logo_ext}'
else:
    _logo_mime = 'image/png'
    _logo_b64  = ("iVBORw0KGgoAAAANSUhEUgAAAjAAAACMCAYAAABRTFQrAAAABmJLR0QA"
                  "/wD/AP+gvaeTAAAADUlEQVQI12NgYGD4DwABBAEBhc9HaQAAAABJRU5ErkJggg==")

logo_col, title_col = st.columns([1, 11])
with logo_col:
    st.markdown(
        f'<img src="data:{_logo_mime};base64,{_logo_b64}" style="width:180px;margin-top:4px;" />',
        unsafe_allow_html=True
    )
with title_col:
    _dot_cls = "amber" if data_status == "csv" else ""
    st.markdown(f"""
    <div class="mc-topbar">
        <div>
            <div class="mc-eyebrow">Shalina Healthcare &nbsp;&middot;&nbsp; Distribution Intelligence Platform</div>
            <div class="mc-title">AI Distribution <span>Depth</span> Analysis System</div>
        </div>
        <div class="mc-status-group">
            <div class="mc-status-pill"><div class="mc-status-dot"></div>SYS: ONLINE</div>
            <div class="mc-status-pill"><div class="mc-status-dot {_dot_cls}"></div>{sync_label}</div>
        </div>
    </div>""", unsafe_allow_html=True)

# ── DATA SOURCE BANNER ────────────────────────────────────────────
is_live   = data_status == "live"
is_hybrid = data_status == "hybrid"
dot_color = "#4CAF50" if is_live else ("#6EC6F5" if is_hybrid else "#F9A825")
dot_glow  = ("rgba(76,175,80,0.6)"    if is_live  else
             ("rgba(110,198,245,0.6)" if is_hybrid else "rgba(249,168,37,0.6)"))
status_label = data_source  # always use actual label from fabric_connector
status_sub = (
    "Live data — both countries pulling from Microsoft Fabric" if is_live else
    ("Hybrid mode — one country live, one using CSV fallback" if is_hybrid else
     "Fabric unreachable — using CSV fallback for both countries")
)

st.markdown(f"""
<style>
@keyframes pulse {{
  0%   {{ box-shadow:0 0 0 0 {dot_glow},0 0 8px {dot_color};opacity:1; }}
  50%  {{ box-shadow:0 0 0 8px transparent,0 0 16px {dot_color};opacity:0.7; }}
  100% {{ box-shadow:0 0 0 0 {dot_glow},0 0 8px {dot_color};opacity:1; }}
}}
@keyframes ripple {{
  0%   {{ transform:scale(1);opacity:0.6; }}
  100% {{ transform:scale(2.5);opacity:0; }}
}}
</style>
<div class="ds-banner" style="border-radius:12px;padding:12px 20px;backdrop-filter:blur(10px);">
    <div style="position:relative;width:14px;height:14px;flex-shrink:0;">
        <div style="position:absolute;top:0;left:0;width:14px;height:14px;border-radius:50%;
             background:{dot_color};animation:ripple 2s ease-out infinite;z-index:1;"></div>
        <div style="width:14px;height:14px;border-radius:50%;background:{dot_color};
             animation:pulse 2s ease-in-out infinite;position:relative;z-index:2;"></div>
    </div>
    <div style="flex:1;">
        <div style="font-family:'Inter',sans-serif;font-size:13px;font-weight:700;color:#FFFFFF;">{status_label}</div>
        <div style="font-size:11px;color:#90B8D0;margin-top:2px;">{status_sub}</div>
    </div>
    <div style="display:flex;flex-direction:column;gap:5px;align-items:flex-end;">
        <div style="display:flex;align-items:center;gap:6px;font-size:10px;color:#90B8D0;font-weight:600;text-transform:uppercase;letter-spacing:0.8px;">
            <div style="width:8px;height:8px;border-radius:50%;background:#4CAF50;box-shadow:0 0 6px rgba(76,175,80,0.7);"></div>Live &mdash; Microsoft Fabric
        </div>
        <div style="display:flex;align-items:center;gap:6px;font-size:10px;color:#90B8D0;font-weight:600;text-transform:uppercase;letter-spacing:0.8px;">
            <div style="width:8px;height:8px;border-radius:50%;background:#6EC6F5;box-shadow:0 0 6px rgba(110,198,245,0.7);"></div>Hybrid &mdash; CSV + Fabric
        </div>
        <div style="display:flex;align-items:center;gap:6px;font-size:10px;color:#90B8D0;font-weight:600;text-transform:uppercase;letter-spacing:0.8px;">
            <div style="width:8px;height:8px;border-radius:50%;background:#F9A825;box-shadow:0 0 6px rgba(249,168,37,0.7);"></div>CSV Fallback
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── COUNTRY SWITCHER ──────────────────────────────────────────────
st.markdown(
    "<div style='margin:12px 0 6px 0;font-family:Inter,sans-serif;font-size:10px;font-weight:700;"
    "color:#90C8E8;text-transform:uppercase;letter-spacing:1.5px;'>Select Country</div>",
    unsafe_allow_html=True
)
cc1, cc2, cc3 = st.columns([1, 1, 8])
with cc1:
    if st.button("Nigeria", use_container_width=True, key="btn_ng"):
        st.session_state.country = "Nigeria"
        st.session_state.selected_outlet = None
with cc2:
    if st.button("Angola", use_container_width=True, key="btn_ao"):
        st.session_state.country = "Angola"
        st.session_state.selected_outlet = None

country    = st.session_state.country
df_country = df_all[df_all['country'] == country].copy()
p25, mean_val, p75 = get_stats(df_country)

accent = "#3B82F6" if country == "Nigeria" else "#8B5CF6"
st.markdown(
    f"<div style='height:2px;background:linear-gradient(90deg,{accent},transparent);margin-bottom:16px;'></div>",
    unsafe_allow_html=True
)

# ── NAVBAR ────────────────────────────────────────────────────────
n1, n2, n3, n4 = st.columns(4)
with n1:
    if st.button("Dashboard",            use_container_width=True, key="nav_dash"):
        st.session_state.nav_page = "Dashboard"
with n2:
    if st.button("Outlet Performance",   use_container_width=True, key="nav_perf"):
        st.session_state.nav_page = "Outlet Performance"
with n3:
    if st.button("Whitespace Detection", use_container_width=True, key="nav_white"):
        st.session_state.nav_page = "Whitespace Detection"
with n4:
    if st.button("Expansion Strategy",   use_container_width=True, key="nav_expand"):
        st.session_state.nav_page = "Expansion Strategy"

st.markdown(
    f'<div id="shalina-active-page" data-page="{st.session_state.nav_page}" style="display:none;"></div>',
    unsafe_allow_html=True
)

# ── JS : FX + SVG ICONS + ACTIVE NAV ─────────────────────────────
import streamlit.components.v1 as _fx_c
_fx_c.html("""<script>
(function(){
    const doc = window.parent.document;

    // No icons on main navbar buttons — icons are sidebar-only

    const SIDEBAR_ICONS = {
        'Dashboard':
            '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg>',
        'RFM Analysis':
            '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg>',
        'Churn Prediction':
            '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>',
        'Upload Data':
            '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="16 16 12 12 8 16"/><line x1="12" y1="12" x2="12" y2="21"/><path d="M20.39 18.39A5 5 0 0 0 18 9h-1.26A8 8 0 1 0 3 16.3"/></svg>',
    };

    // ── Sidebar icon injection ───────────────────────────────────
    function addSidebarIcons() {
        const sidebar = doc.querySelector('[data-testid="stSidebar"]');
        if (!sidebar) return;

        // Target both st.page_link anchors AND plain sidebar buttons
        // st.page_link renders as <a data-testid="stPageLink"> containing a <span> with text
        sidebar.querySelectorAll('a[data-testid="stPageLink"]').forEach(link => {
            if (link.dataset.siconDone) return;

            // Find the deepest text span — Streamlit nests several spans
            const allSpans = link.querySelectorAll('span');
            let textSpan = null;
            for (const sp of allSpans) {
                const t = sp.textContent.trim();
                if (SIDEBAR_ICONS[t]) { textSpan = sp; break; }
            }
            if (!textSpan) return;

            const label = textSpan.textContent.trim();
            const svg   = SIDEBAR_ICONS[label];
            link.dataset.siconDone = '1';

            textSpan.innerHTML =
                '<span style="display:inline-flex;align-items:center;gap:10px;width:100%;">'
                + '<span style="display:flex;align-items:center;justify-content:center;'
                + 'width:28px;height:28px;border-radius:8px;flex-shrink:0;'
                + 'background:rgba(255,255,255,0.05);border:1px solid rgba(255,255,255,0.09);">'
                + svg + '</span>'
                + '<span style="color:#94A3B8;font-size:13px;font-weight:500;">'
                + label + '</span></span>';
        });
    }

    // ── Country button text — make Nigeria & Angola clearly visible ──
    function styleCountryButtons() {
        doc.querySelectorAll('button').forEach(btn => {
            const txt = btn.textContent.trim();
            if (txt !== 'Nigeria' && txt !== 'Angola') return;
            if (btn.dataset.countryStyled) return;
            btn.dataset.countryStyled = '1';
            // Bright blue text, slightly elevated background
            btn.style.setProperty('color', '#60A5FA', 'important');
            btn.style.setProperty('background', 'rgba(59,130,246,0.1)', 'important');
            btn.style.setProperty('border-color', 'rgba(59,130,246,0.35)', 'important');
            btn.style.setProperty('font-weight', '700', 'important');
            btn.style.setProperty('letter-spacing', '0.3px', 'important');
            btn.addEventListener('mouseenter', () => {
                btn.style.setProperty('background', 'rgba(59,130,246,0.22)', 'important');
                btn.style.setProperty('color', '#FFFFFF', 'important');
                btn.style.setProperty('border-color', 'rgba(96,165,250,0.7)', 'important');
                btn.style.setProperty('box-shadow', '0 0 14px rgba(59,130,246,0.3)', 'important');
            });
            btn.addEventListener('mouseleave', () => {
                btn.style.setProperty('background', 'rgba(59,130,246,0.1)', 'important');
                btn.style.setProperty('color', '#60A5FA', 'important');
                btn.style.setProperty('border-color', 'rgba(59,130,246,0.35)', 'important');
                btn.style.removeProperty('box-shadow');
            });
        });
    }

    const NAV_LABELS = ['Dashboard','Outlet Performance','Whitespace Detection','Expansion Strategy'];

    function highlightActiveNav() {
        const marker = doc.getElementById('shalina-active-page');
        if (!marker) return;
        const active = marker.getAttribute('data-page');
        doc.querySelectorAll('button').forEach(btn => {
            const txt = btn.textContent.trim();
            if (!NAV_LABELS.includes(txt)) return;
            const isActive = (txt === active);
            if (isActive) {
                btn.style.setProperty('background',
                    'linear-gradient(135deg,rgba(59,130,246,0.28),rgba(139,92,246,0.16))','important');
                btn.style.setProperty('border-color','rgba(59,130,246,0.65)','important');
                btn.style.setProperty('color','#FFFFFF','important');
                btn.style.setProperty('box-shadow',
                    '0 0 16px rgba(59,130,246,0.3),inset 0 1px 0 rgba(255,255,255,0.07)','important');
            } else {
                btn.style.setProperty('background','rgba(255,255,255,0.04)','important');
                btn.style.setProperty('border-color','rgba(255,255,255,0.08)','important');
                btn.style.setProperty('color','#CBD5E1','important');
                btn.style.removeProperty('box-shadow');
            }
        });
    }

    function injectStyles() {
        if (doc.getElementById('shalina-fx-styles')) return;
        const s = doc.createElement('style');
        s.id = 'shalina-fx-styles';
        s.textContent = `
            body::after{content:'';position:fixed;inset:0;pointer-events:none;z-index:9999;opacity:0.03;
            background-image:url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E");
            background-size:200px 200px;}
            .shalina-orb{position:fixed;border-radius:50%;pointer-events:none;z-index:0;filter:blur(80px);animation:orbFloat linear infinite;opacity:0;}
            @keyframes orbFloat{0%{transform:translate(0,0) scale(1);opacity:0.18;}25%{transform:translate(40px,-60px) scale(1.1);opacity:0.22;}50%{transform:translate(-30px,30px) scale(0.95);opacity:0.15;}75%{transform:translate(20px,50px) scale(1.05);opacity:0.20;}100%{transform:translate(0,0) scale(1);opacity:0.18;}}
            .kpi-card{position:relative;overflow:hidden;}
            .kpi-card .spotlight{position:absolute;width:300px;height:300px;background:radial-gradient(circle,rgba(255,255,255,0.1) 0%,transparent 70%);border-radius:50%;pointer-events:none;transform:translate(-50%,-50%);opacity:0;transition:opacity 0.2s ease;}
            .kpi-card:hover .spotlight{opacity:1;}
            .kpi-card::after{content:'';position:absolute;inset:-1px;border-radius:14px;background:linear-gradient(135deg,rgba(33,150,220,0),rgba(110,198,245,0.4),rgba(168,85,247,0.22),rgba(33,150,220,0));background-size:300% 300%;-webkit-mask:linear-gradient(#fff 0 0) content-box,linear-gradient(#fff 0 0);mask:linear-gradient(#fff 0 0) content-box,linear-gradient(#fff 0 0);-webkit-mask-composite:xor;mask-composite:exclude;opacity:0;transition:opacity 0.3s ease;animation:gradBorder 3s linear infinite;pointer-events:none;}
            .kpi-card:hover::after{opacity:1;}
            @keyframes gradBorder{0%{background-position:0% 50%;}50%{background-position:100% 50%;}100%{background-position:0% 50%;}}
            .shalina-reveal{opacity:0;transform:translateY(44px) scale(0.97);transition:opacity 0.75s cubic-bezier(.16,1,.3,1),transform 0.75s cubic-bezier(.16,1,.3,1);will-change:opacity,transform;}
            .shalina-reveal.visible{opacity:1;transform:translateY(0) scale(1);}
            .shalina-reveal:nth-child(2){transition-delay:0.08s;}.shalina-reveal:nth-child(3){transition-delay:0.16s;}.shalina-reveal:nth-child(4){transition-delay:0.24s;}
            .ds-banner,.insight-card,.odc-wrap{backdrop-filter:blur(20px) saturate(1.3) !important;-webkit-backdrop-filter:blur(20px) saturate(1.3) !important;}
            #shalina-particles{position:fixed;top:0;left:0;width:100%;height:100%;pointer-events:none;z-index:0;opacity:0.4;}
        `;
        doc.head.appendChild(s);
    }

    function addOrbs() {
        if (doc.getElementById('shalina-orb-1')) return;
        [{id:'shalina-orb-1',w:600,h:600,top:'5%', left:'10%',color:'rgba(33,100,200,0.5)', dur:'18s',delay:'0s'},
         {id:'shalina-orb-2',w:500,h:500,top:'50%',left:'70%',color:'rgba(100,50,200,0.4)', dur:'24s',delay:'-8s'},
         {id:'shalina-orb-3',w:400,h:400,top:'80%',left:'20%',color:'rgba(0,150,220,0.35)', dur:'20s',delay:'-5s'},
         {id:'shalina-orb-4',w:350,h:350,top:'20%',left:'55%',color:'rgba(80,20,180,0.3)',  dur:'15s',delay:'-12s'}
        ].forEach(o => {
            const el = doc.createElement('div');
            el.id = o.id; el.className = 'shalina-orb';
            Object.assign(el.style,{width:o.w+'px',height:o.h+'px',top:o.top,left:o.left,
                background:o.color,animationDuration:o.dur,animationDelay:o.delay});
            doc.body.prepend(el);
        });
    }

    function addParticles() {
        if (doc.getElementById('shalina-particles')) return;
        const canvas = doc.createElement('canvas');
        canvas.id = 'shalina-particles'; doc.body.prepend(canvas);
        const ctx = canvas.getContext('2d');
        let W, H, P = [];
        function resize(){W=canvas.width=doc.body.clientWidth||window.parent.innerWidth;H=canvas.height=doc.body.clientHeight||window.parent.innerHeight;}
        resize(); window.parent.addEventListener('resize',resize);
        for(let i=0;i<80;i++) P.push({x:Math.random()*W,y:Math.random()*H,r:Math.random()*1.8+0.4,vx:(Math.random()-.5)*.35,vy:(Math.random()-.5)*.35,alpha:Math.random()*.5+.15});
        (function draw(){
            ctx.clearRect(0,0,W,H);
            P.forEach(p=>{p.x+=p.vx;p.y+=p.vy;if(p.x<0)p.x=W;if(p.x>W)p.x=0;if(p.y<0)p.y=H;if(p.y>H)p.y=0;ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,Math.PI*2);ctx.fillStyle='rgba(110,198,245,'+p.alpha+')';ctx.fill();});
            for(let i=0;i<P.length;i++) for(let j=i+1;j<P.length;j++){const dx=P[i].x-P[j].x,dy=P[i].y-P[j].y,d=Math.sqrt(dx*dx+dy*dy);if(d<120){ctx.beginPath();ctx.moveTo(P[i].x,P[i].y);ctx.lineTo(P[j].x,P[j].y);ctx.strokeStyle='rgba(33,150,196,'+(0.12*(1-d/120))+')';ctx.lineWidth=.5;ctx.stroke();}}
            requestAnimationFrame(draw);
        })();
    }

    function addTiltCards() {
        doc.querySelectorAll('.kpi-card').forEach(card=>{
            if(card.dataset.tiltDone) return; card.dataset.tiltDone='1';
            const spot=doc.createElement('div'); spot.className='spotlight'; card.appendChild(spot);
            card.addEventListener('mousemove',e=>{const r=card.getBoundingClientRect();spot.style.left=(e.clientX-r.left)+'px';spot.style.top=(e.clientY-r.top)+'px';});
            card.addEventListener('mouseenter',()=>{card.style.transform='translateY(-4px) scale(1.015)';card.style.boxShadow='0 16px 40px rgba(0,0,0,0.4),0 0 20px rgba(33,150,220,0.16)';});
            card.addEventListener('mouseleave',()=>{card.style.transform='';card.style.boxShadow='';});
        });
    }

    function addRevealOnScroll() {
        doc.querySelectorAll('.kpi-card,.insight-card,.ds-banner,.odc-wrap,[data-testid="stPlotlyChart"],[data-testid="stDataFrame"],[data-testid="stMetric"]').forEach(el=>{
            if(el.dataset.revealDone) return;
            if(el.getBoundingClientRect().height<40) return;
            el.dataset.revealDone='1'; el.classList.add('shalina-reveal');
        });
        if(!window._shalinaRevealObs){window._shalinaRevealObs=new IntersectionObserver(entries=>{entries.forEach((e,i)=>{if(e.isIntersecting){setTimeout(()=>e.target.classList.add('visible'),Math.min(i*80,400));window._shalinaRevealObs.unobserve(e.target);}});},{threshold:.08,rootMargin:'0px 0px -40px 0px'});}
        doc.querySelectorAll('.shalina-reveal:not(.visible)').forEach(el=>window._shalinaRevealObs.observe(el));
    }

    function addMouseGradient() {
        if(doc.getElementById('mouse-gradient')) return;
        const el=doc.createElement('div'); el.id='mouse-gradient';
        Object.assign(el.style,{position:'fixed',width:'800px',height:'800px',borderRadius:'50%',background:'radial-gradient(circle,rgba(33,100,220,0.06) 0%,transparent 70%)',pointerEvents:'none',zIndex:'1',transform:'translate(-50%,-50%)',left:'50%',top:'50%'});
        doc.body.appendChild(el);
        doc.addEventListener('mousemove',e=>{el.style.left=e.clientX+'px';el.style.top=e.clientY+'px';});
    }

    function hideNav(){const n=doc.querySelector('[data-testid="stSidebarNav"]');if(n)n.remove();}
    function hideImgBtns(){doc.querySelectorAll('[data-testid="StyledFullScreenButton"],button[title="View fullscreen"],button[title="Fullscreen"]').forEach(b=>b.remove());}

    function fullInit(){
        try{injectStyles();}catch(e){}
        try{addOrbs();}catch(e){}
        try{addParticles();}catch(e){}
        try{addMouseGradient();}catch(e){}
        try{addTiltCards();}catch(e){}
        try{addRevealOnScroll();}catch(e){}
        try{hideNav();}catch(e){}
        try{hideImgBtns();}catch(e){}
        try{addSidebarIcons();}catch(e){}
        try{styleCountryButtons();}catch(e){}
        try{highlightActiveNav();}catch(e){}
    }

    function lightRefresh(){
        try{addSidebarIcons();}catch(e){}
        try{styleCountryButtons();}catch(e){}
        try{highlightActiveNav();}catch(e){}
        try{addTiltCards();}catch(e){}
        try{addRevealOnScroll();}catch(e){}
        try{hideNav();}catch(e){}
        try{hideImgBtns();}catch(e){}
        if(!doc.getElementById('shalina-particles')){try{addParticles();}catch(e){}}
        if(!doc.getElementById('shalina-orb-1')){try{addOrbs();}catch(e){}}
        if(!doc.getElementById('mouse-gradient')){try{addMouseGradient();}catch(e){}}
        if(!doc.getElementById('shalina-fx-styles')){try{injectStyles();}catch(e){}}
    }

    setTimeout(fullInit, 300);
    setTimeout(fullInit, 900);
    setInterval(lightRefresh, 850);
})();
</script>""", height=0)

# ── FILTERS ───────────────────────────────────────────────────────
st.markdown("<div style='margin-top:12px;'></div>", unsafe_allow_html=True)
f1, f2 = st.columns(2)
with f1:
    subtype_opts     = ["All"] + sorted(df_country['Retailer Subtype'].dropna().unique().tolist())
    selected_subtype = st.selectbox("Retailer Subtype", subtype_opts)
with f2:
    opp_opts         = ["All","Dead Whitespace","Underperforming","Low Performer","Active","High Performer"]
    selected_opp     = st.selectbox("Opportunity Category", opp_opts)

df = df_country.copy()
if selected_subtype != "All": df = df[df['Retailer Subtype'] == selected_subtype]
if selected_opp      != "All": df = df[df['Opportunity']      == selected_opp]

if len(df) == 0:
    st.markdown(
        '<div style="background:rgba(200,50,50,0.15);border:1px solid rgba(255,100,100,0.4);'
        'border-radius:10px;padding:14px 16px;font-size:13px;color:#FFAAAA;'
        'font-weight:600;margin:16px 0;">No outlets match the selected filters.</div>',
        unsafe_allow_html=True
    )
    st.stop()

map_center = {"lat": 9.0, "lon": 8.0}  if country == "Nigeria" else {"lat": -11.0, "lon": 17.5}
map_zoom   = 5 if country == "Nigeria" else 4

# ── OUTLET DRILL-DOWN ─────────────────────────────────────────────
if st.session_state.selected_outlet:
    _name = st.session_state.selected_outlet
    _rows = df_country[df_country['Shop Name'] == _name]

    if len(_rows) == 0:
        st.session_state.selected_outlet = None
    else:
        _o      = _rows.iloc[0]
        _ytd    = float(_o.get('YTD Retailing Value', 0))
        _sub    = str(_o.get('Retailer Subtype', '—'))
        _opp    = str(_o.get('Opportunity', '—'))
        _lat    = float(_o.get('latitude',  0))
        _lon    = float(_o.get('longitude', 0))
        _pct    = float((df_country['YTD Retailing Value'] <= _ytd).sum() / max(len(df_country),1) * 100)
        _avg    = float(df_country['YTD Retailing Value'].mean())
        _vs_avg = ((_ytd - _avg) / _avg * 100) if _avg > 0 else 0

        # Validate coordinates:
        # Step 1 — basic sanity (NaN, 0,0, out of Earth range)
        # Step 2 — must land inside a generous country bounding box
        #           catches junk defaults like (0.5, 6.7) near São Tomé
        #           Boxes are deliberately wide (+2° buffer on every edge)
        _COUNTRY_BOUNDS = {
            "Nigeria": dict(lat_min=2.5,  lat_max=15.0, lon_min=2.5,  lon_max=15.5),
            "Angola":  dict(lat_min=-19.0,lat_max=-3.5, lon_min=10.5, lon_max=25.5),
        }
        _bounds = _COUNTRY_BOUNDS.get(country, dict(lat_min=-90, lat_max=90, lon_min=-180, lon_max=180))
        try:
            _lat_f = float(_lat)
            _lon_f = float(_lon)
            _coords_valid = (
                not np.isnan(_lat_f) and not np.isnan(_lon_f)
                and not (_lat_f == 0 and _lon_f == 0)           # exact ocean default
                and abs(_lat_f) > 0.01 and abs(_lon_f) > 0.01  # near-zero catch
                and _bounds['lat_min'] <= _lat_f <= _bounds['lat_max']
                and _bounds['lon_min'] <= _lon_f <= _bounds['lon_max']
            )
            _lat = _lat_f
            _lon = _lon_f
        except (ValueError, TypeError):
            _coords_valid = False

        _palette = {
            'Dead Whitespace': ('#EF4444', 'rgba(239,68,68,0.15)'),
            'Underperforming': ('#F97316', 'rgba(249,115,22,0.15)'),
            'Low Performer':   ('#EAB308', 'rgba(234,179,8,0.15)'),
            'Active':          ('#22C55E', 'rgba(34,197,94,0.15)'),
            'High Performer':  ('#A855F7', 'rgba(168,85,247,0.15)'),
        }
        _opp_clr, _opp_bg = _palette.get(_opp, ('#94A3B8', 'rgba(148,163,184,0.15)'))
        _vs_clr   = "#22C55E" if _vs_avg >= 0 else "#EF4444"
        _vs_arrow = "&#8593;" if _vs_avg >= 0 else "&#8595;"
        _pct_clr  = "#22C55E" if _pct >= 66 else ("#F59E0B" if _pct >= 33 else "#EF4444")

        st.markdown(f"""
        <div class="odc-wrap">
            <div class="odc-eyebrow">Outlet Detail View</div>
            <div class="odc-name">{_name}</div>
            <div class="odc-meta">
                <span style="background:{_opp_bg};color:{_opp_clr};border:1px solid {_opp_clr}55;
                    border-radius:4px;padding:3px 10px;font-size:10px;font-weight:700;
                    letter-spacing:0.5px;text-transform:uppercase;">{_opp}</span>
                <span style="color:#475569;font-size:11px;">&middot;</span>
                <span style="color:#64748B;font-size:11px;">{_sub}</span>
                <span style="color:#475569;font-size:11px;">&middot;</span>
                <span style="color:#64748B;font-size:11px;">{country}</span>
                <span style="color:#475569;font-size:11px;">&middot;</span>
                <span style="color:#475569;font-size:11px;font-family:'JetBrains Mono',monospace;">
                    {'No GPS data' if not _coords_valid else f'{_lat:.4f}, {_lon:.4f}'}</span>
            </div>
            <div class="odc-stats">
                <div class="odc-stat">
                    <div class="odc-stat-label">YTD Revenue</div>
                    <div class="odc-stat-value" style="color:#F1F5F9;">&#8358;{_ytd:,.1f}K</div>
                </div>
                <div class="odc-divider"></div>
                <div class="odc-stat">
                    <div class="odc-stat-label">Percentile Rank</div>
                    <div class="odc-stat-value" style="color:{_pct_clr};">
                        {_pct:.0f}<span style="font-size:13px;color:#475569;">th</span></div>
                </div>
                <div class="odc-divider"></div>
                <div class="odc-stat">
                    <div class="odc-stat-label">vs Country Avg</div>
                    <div class="odc-stat-value" style="color:{_vs_clr};">
                        {_vs_arrow} {abs(_vs_avg):.1f}%</div>
                </div>
                <div class="odc-divider"></div>
                <div class="odc-stat">
                    <div class="odc-stat-label">Country Avg YTD</div>
                    <div class="odc-stat-value" style="color:#94A3B8;font-size:16px;">
                        &#8358;{_avg:,.1f}K</div>
                </div>
            </div>
        </div>""", unsafe_allow_html=True)

        # ── Mini map — only render when coordinates are valid ────────
        # ── Section label ──────────────────────────────────────────
        st.markdown('<div class="section-title">Outlet Location</div>', unsafe_allow_html=True)

        if _coords_valid:
            # ── Nearby outlets within 0.3° — valid coordinates only ──
            _nearby = df_country[
                df_country['latitude'].between(_lat - 0.3, _lat + 0.3) &
                df_country['longitude'].between(_lon - 0.3, _lon + 0.3) &
                df_country['latitude'].between(_bounds['lat_min'], _bounds['lat_max']) &
                df_country['longitude'].between(_bounds['lon_min'], _bounds['lon_max']) &
                (df_country['latitude']  != 0) &
                (df_country['longitude'] != 0)
            ].copy()

            # Ensure the selected outlet is always in the frame even if it
            # appears in zero nearby outlets (edge case with duplicate names)
            if _name not in _nearby['Shop Name'].values:
                _nearby = df_country[df_country['Shop Name'] == _name].copy()

            # Size: selected outlet is a large pin; neighbours are small dots
            _nearby['_sz']    = np.where(_nearby['Shop Name'] == _name, 32, 6)
            _nearby['_label'] = np.where(_nearby['Shop Name'] == _name,
                                          'Selected: ' + _nearby['Shop Name'],
                                          _nearby['Shop Name'])

            # Add a dedicated "YOU ARE HERE" pin row so it always sits on top
            _pin_df = _nearby[_nearby['Shop Name'] == _name].copy()
            _ctx_df = _nearby[_nearby['Shop Name'] != _name].copy()

            import plotly.graph_objects as go

            _fig_loc = go.Figure()

            # Layer 1 — context outlets (small coloured dots)
            for _opp_cat, _opp_hex in color_map.items():
                _sub_ctx = _ctx_df[_ctx_df['Opportunity'] == _opp_cat]
                if len(_sub_ctx) == 0:
                    continue
                _fig_loc.add_trace(go.Scattermapbox(
                    lat=_sub_ctx['latitude'],
                    lon=_sub_ctx['longitude'],
                    mode='markers',
                    marker=dict(size=7, color=_opp_hex, opacity=0.65),
                    text=_sub_ctx['Shop Name'] + '<br>' + _opp_cat +
                         '<br>YTD: ₦' + _sub_ctx['YTD Retailing Value'].apply(lambda x: f'{x:,.1f}') + 'K',
                    hoverinfo='text',
                    name=_opp_cat,
                    showlegend=True,
                ))

            # Layer 2 — selected outlet (large glowing pin)
            if len(_pin_df) > 0:
                _pin_color = color_map.get(_opp, '#3B82F6')
                _fig_loc.add_trace(go.Scattermapbox(
                    lat=_pin_df['latitude'],
                    lon=_pin_df['longitude'],
                    mode='markers+text',
                    marker=dict(
                        size=22,
                        color=_pin_color,
                        opacity=1.0,
                        symbol='circle',
                    ),
                    text=[_name],
                    textposition='top right',
                    textfont=dict(size=11, color='#FFFFFF'),
                    hovertext=f'<b>{_name}</b><br>{_opp}<br>{_sub}<br>YTD: ₦{_ytd:,.1f}K',
                    hoverinfo='text',
                    name=f'Selected: {_name}',
                    showlegend=True,
                ))

                # Outer ring for the selected pin
                _fig_loc.add_trace(go.Scattermapbox(
                    lat=_pin_df['latitude'],
                    lon=_pin_df['longitude'],
                    mode='markers',
                    marker=dict(size=34, color=_pin_color, opacity=0.25),
                    hoverinfo='skip',
                    showlegend=False,
                ))

            _fig_loc.update_layout(
                mapbox=dict(
                    style='carto-darkmatter',
                    center=dict(lat=_lat, lon=_lon),
                    zoom=13,
                ),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                height=380,
                margin=dict(l=0, r=0, t=0, b=0),
                legend=dict(
                    font=dict(color='#94A3B8', size=10),
                    bgcolor='rgba(8,13,26,0.85)',
                    bordercolor='rgba(255,255,255,0.08)',
                    borderwidth=1,
                    x=0, y=1,
                ),
                uirevision='outlet_map',
            )

            _mc, _cc = st.columns([10, 1])
            with _mc:
                st.plotly_chart(_fig_loc, use_container_width=True, key="drill_map")
            with _cc:
                st.markdown("<div style='height:160px;'></div>", unsafe_allow_html=True)
                if st.button("Close", key="close_drill", use_container_width=True):
                    st.session_state.selected_outlet = None
                    st.rerun()

        else:
            # No valid GPS — professional data quality notice
            _gps_valid_n, _gps_total_n, _gps_pct = gps_quality(df_country, country)
            _gps_missing = _gps_total_n - _gps_valid_n
            st.markdown(f"""
            <div style="display:flex;gap:16px;align-items:flex-start;
                background:rgba(15,25,50,0.6);border:1px solid rgba(255,255,255,0.08);
                border-radius:12px;padding:18px 20px;margin-bottom:16px;">
                <div style="width:36px;height:36px;border-radius:8px;flex-shrink:0;
                    background:rgba(245,158,11,0.12);border:1px solid rgba(245,158,11,0.3);
                    display:flex;align-items:center;justify-content:center;">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none"
                        stroke="#F59E0B" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <circle cx="12" cy="12" r="10"/>
                        <line x1="12" y1="8" x2="12" y2="12"/>
                        <line x1="12" y1="16" x2="12.01" y2="16"/>
                    </svg>
                </div>
                <div style="flex:1;">
                    <div style="font-size:13px;font-weight:700;color:#F1F5F9;margin-bottom:4px;">
                        GPS Coordinates Unavailable</div>
                    <div style="font-size:11px;color:#64748B;line-height:1.7;">
                        This outlet has a placeholder coordinate
                        <span style="font-family:'JetBrains Mono',monospace;color:#F59E0B;
                            background:rgba(245,158,11,0.1);padding:1px 6px;border-radius:4px;">
                            {_lat:.4f}, {_lon:.4f}</span>
                        assigned by the source system instead of a real GPS location.
                        All revenue and performance stats above are accurate.
                    </div>
                    <div style="margin-top:10px;padding-top:10px;
                        border-top:1px solid rgba(255,255,255,0.06);
                        display:flex;gap:20px;">
                        <div>
                            <div style="font-size:9px;font-weight:700;letter-spacing:1.5px;
                                text-transform:uppercase;color:#475569;margin-bottom:3px;">
                                Valid GPS in {country}</div>
                            <div style="font-size:15px;font-weight:800;color:#22C55E;">
                                {_gps_valid_n:,}
                                <span style="font-size:11px;color:#475569;font-weight:400;">
                                    / {_gps_total_n:,} outlets ({_gps_pct}%)</span>
                            </div>
                        </div>
                        <div>
                            <div style="font-size:9px;font-weight:700;letter-spacing:1.5px;
                                text-transform:uppercase;color:#475569;margin-bottom:3px;">
                                Missing GPS</div>
                            <div style="font-size:15px;font-weight:800;color:#F59E0B;">
                                {_gps_missing:,}
                                <span style="font-size:11px;color:#475569;font-weight:400;">
                                    outlets require re-geocoding</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>""", unsafe_allow_html=True)
            if st.button("Close", key="close_drill"):
                st.session_state.selected_outlet = None
                st.rerun()

# ── PAGE ROUTING ──────────────────────────────────────────────────
page = st.session_state.nav_page

# ══════════════════════════════════════════════════════════════════
#  DASHBOARD
# ══════════════════════════════════════════════════════════════════
if page == "Dashboard":
    total_outlets   = len(df)
    dead_outlets    = len(df[df['Opportunity'] == 'Dead Whitespace'])
    high_performers = len(df[df['Opportunity'] == 'High Performer'])
    total_ytd       = df['YTD Retailing Value'].sum()
    ws_pct          = dead_outlets   / max(total_outlets, 1) * 100
    hp_pct          = high_performers / max(total_outlets, 1) * 100
    active_df       = df[df['YTD Retailing Value'] > 0]
    avg_per_outlet  = active_df['YTD Retailing Value'].mean() if len(active_df) else 0

    _ws_delta = delta_html(ws_pct, 20, 35, reverse=True, suffix="%",
                           label_lo="managed", label_mid="elevated", label_hi="critical")
    _hp_delta = delta_html(hp_pct,  8, 15, suffix="%",
                           label_lo="low", label_mid="moderate", label_hi="strong")

    st.markdown(f"""
    <div class="kpi-row">
        <div class="kpi-card mc-blue">
            <div class="kpi-accent-line" style="background:linear-gradient(90deg,#3B82F6,#60A5FA);"></div>
            <div class="kpi-label">Total Outlets &mdash; {country}</div>
            <div class="kpi-value">{total_outlets:,}</div>
            <div class="kpi-delta" style="color:#475569;">Distribution network</div>
        </div>
        <div class="kpi-card mc-red">
            <div class="kpi-accent-line" style="background:linear-gradient(90deg,#EF4444,#F87171);"></div>
            <div class="kpi-label">Dead Whitespace</div>
            <div class="kpi-value">{dead_outlets:,}</div>
            <div class="kpi-delta">{_ws_delta} of outlets</div>
        </div>
        <div class="kpi-card mc-purple">
            <div class="kpi-accent-line" style="background:linear-gradient(90deg,#8B5CF6,#A78BFA);"></div>
            <div class="kpi-label">High Performers</div>
            <div class="kpi-value">{high_performers:,}</div>
            <div class="kpi-delta">{_hp_delta} of network</div>
        </div>
        <div class="kpi-card mc-amber">
            <div class="kpi-accent-line" style="background:linear-gradient(90deg,#F59E0B,#FCD34D);"></div>
            <div class="kpi-label">Total YTD Revenue</div>
            <div class="kpi-value">&#8358;{total_ytd/1000:,.0f}M</div>
            <div class="kpi-delta" style="color:#64748B;">Avg &#8358;{avg_per_outlet:,.0f}K per active outlet</div>
        </div>
    </div>""", unsafe_allow_html=True)

    st.markdown('<div class="section-title">Geographic Outlet Distribution</div>', unsafe_allow_html=True)
    # Filter rows with valid coordinates before mapping
    _valid_coords = (
        df['latitude'].notna()  & df['longitude'].notna() &
        (df['latitude']  != 0)  & (df['longitude']  != 0) &
        df['latitude'].between(*([2,16]   if country=='Nigeria' else [-20,-2])) &
        df['longitude'].between(*([1,17]  if country=='Nigeria' else [9,27]))
    )
    _map_src = df[_valid_coords]
    map_df = (_map_src.sample(min(5000,len(_map_src)), random_state=42) if len(_map_src)>5000 else _map_src).copy()
    map_df['_size'] = map_df['YTD Retailing Value'].clip(lower=0).fillna(0)
    if map_df['_size'].sum() == 0: map_df['_size'] = 1
    fig_map = px.scatter_mapbox(map_df, lat="latitude", lon="longitude",
        color="Opportunity", color_discrete_map=color_map, size="_size",
        size_max=14, zoom=map_zoom, height=520, hover_name="Shop Name",
        hover_data={"YTD Retailing Value":":,.1f","Retailer Subtype":True,"latitude":False,"longitude":False},
        center=map_center)
    fig_map.update_traces(marker=dict(opacity=0.85))
    fig_map.update_layout(mapbox_style="carto-darkmatter", paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        legend=dict(font=dict(color="#94A3B8",size=11), bgcolor="rgba(8,13,26,0.85)",
                    bordercolor="rgba(255,255,255,0.08)", borderwidth=1),
        margin=dict(l=0,r=0,t=0,b=0))
    st.plotly_chart(fig_map, use_container_width=True)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="section-title">Opportunity Breakdown</div>', unsafe_allow_html=True)
        opp_counts = df['Opportunity'].value_counts().reset_index()
        opp_counts.columns = ['Category','Count']
        fig_pie = px.pie(opp_counts, values='Count', names='Category',
                         color='Category', color_discrete_map=color_map, hole=0.5)
        fig_pie.update_layout(paper_bgcolor="rgba(0,0,0,0)",
                               legend=dict(font=dict(color="#FFFFFF")),
                               font=dict(color="#90C8E8"), margin=dict(l=0,r=0,t=20,b=0))
        st.plotly_chart(fig_pie, use_container_width=True)
    with c2:
        st.markdown('<div class="section-title">Retailer Subtype Split</div>', unsafe_allow_html=True)
        sub_counts = df['Retailer Subtype'].value_counts().reset_index()
        sub_counts.columns = ['Type','Count']
        fig_bar = px.bar(sub_counts, x='Type', y='Count', color='Type',
                         color_discrete_sequence=['#A855F7','#2196C4','#22C55E'])
        fig_bar.update_layout(**chart_layout)
        st.plotly_chart(fig_bar, use_container_width=True)

# ══════════════════════════════════════════════════════════════════
#  OUTLET PERFORMANCE
# ══════════════════════════════════════════════════════════════════
elif page == "Outlet Performance":
    st.markdown('<div class="section-title">Top 20 Outlets by YTD Retailing Value</div>', unsafe_allow_html=True)
    top20 = (df[df['YTD Retailing Value']>0]
             .nlargest(20,'YTD Retailing Value')
             [['Shop Name','Retailer Subtype','YTD Retailing Value','Opportunity']]
             .reset_index(drop=True))
    top20.index += 1
    top20['YTD Retailing Value'] = top20['YTD Retailing Value'].apply(lambda x: f"\u20a6{x:,.1f}K")
    st.dataframe(top20, use_container_width=True)

    st.markdown('<div class="section-title">YTD Revenue Distribution</div>', unsafe_allow_html=True)
    active_df = df[df['YTD Retailing Value'] > 0]
    fig_hist = px.histogram(active_df, x='YTD Retailing Value', nbins=60,
                             color='Retailer Subtype',
                             color_discrete_sequence=['#A855F7','#2196C4','#22C55E'])
    fig_hist.update_layout(**chart_layout)
    st.plotly_chart(fig_hist, use_container_width=True)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="section-title">Avg YTD by Opportunity Category</div>', unsafe_allow_html=True)
        avg_opp = df[df['YTD Retailing Value']>0].groupby('Opportunity')['YTD Retailing Value'].mean().reset_index()
        fig_avg = px.bar(avg_opp, x='YTD Retailing Value', y='Opportunity', orientation='h',
                         color='Opportunity', color_discrete_map=color_map)
        fig_avg.update_layout(**chart_layout)
        st.plotly_chart(fig_avg, use_container_width=True)
    with c2:
        st.markdown('<div class="section-title">Avg YTD by Retailer Subtype</div>', unsafe_allow_html=True)
        avg_sub = df[df['YTD Retailing Value']>0].groupby('Retailer Subtype')['YTD Retailing Value'].mean().reset_index()
        fig_sub = px.bar(avg_sub, x='Retailer Subtype', y='YTD Retailing Value',
                         color='Retailer Subtype',
                         color_discrete_sequence=['#A855F7','#2196C4','#22C55E'])
        fig_sub.update_layout(**chart_layout)
        st.plotly_chart(fig_sub, use_container_width=True)

# ══════════════════════════════════════════════════════════════════
#  WHITESPACE DETECTION
# ══════════════════════════════════════════════════════════════════
elif page == "Whitespace Detection":
    dead  = df_country[df_country['Opportunity'] == 'Dead Whitespace']
    under = df_country[df_country['Opportunity'] == 'Underperforming']
    total_ws          = len(dead) + len(under)
    ws_network_pct    = round(total_ws / max(len(df_country), 1) * 100, 1)
    revenue_potential = total_ws * mean_val

    _dead_pct    = len(dead)  / max(len(df_country), 1) * 100
    _under_pct   = len(under) / max(len(df_country), 1) * 100
    _dead_delta  = delta_html(_dead_pct,  15, 30, reverse=True, suffix="%",
                              label_lo="managed", label_mid="elevated", label_hi="critical")
    _under_delta = delta_html(_under_pct, 10, 25, reverse=True, suffix="%",
                              label_lo="low", label_mid="moderate", label_hi="high")

    st.markdown(f"""
    <div class="kpi-row">
        <div class="kpi-card mc-red">
            <div class="kpi-accent-line" style="background:linear-gradient(90deg,#EF4444,#F87171);"></div>
            <div class="kpi-label">Dead Whitespace Outlets</div>
            <div class="kpi-value">{len(dead):,}</div>
            <div class="kpi-delta">{_dead_delta} of network</div>
        </div>
        <div class="kpi-card mc-orange">
            <div class="kpi-accent-line" style="background:linear-gradient(90deg,#F97316,#FB923C);"></div>
            <div class="kpi-label">Underperforming Outlets</div>
            <div class="kpi-value">{len(under):,}</div>
            <div class="kpi-delta">{_under_delta} of network</div>
        </div>
        <div class="kpi-card mc-blue">
            <div class="kpi-accent-line" style="background:linear-gradient(90deg,#3B82F6,#60A5FA);"></div>
            <div class="kpi-label">Total Whitespace</div>
            <div class="kpi-value">{total_ws:,}</div>
            <div class="kpi-delta" style="color:#64748B;">{ws_network_pct}% of all {country} outlets</div>
        </div>
        <div class="kpi-card mc-green">
            <div class="kpi-accent-line" style="background:linear-gradient(90deg,#22C55E,#4ADE80);"></div>
            <div class="kpi-label">Revenue Potential</div>
            <div class="kpi-value">&#8358;{revenue_potential/1000:,.0f}M</div>
            <div class="kpi-delta" style="color:#64748B;">If activated to avg performance</div>
        </div>
    </div>""", unsafe_allow_html=True)

    st.markdown('<div class="section-title">Whitespace Outlets Map</div>', unsafe_allow_html=True)
    _ws_valid = (
        df_country['latitude'].notna()  & df_country['longitude'].notna() &
        (df_country['latitude']  != 0)  & (df_country['longitude']  != 0) &
        df_country['latitude'].between(*([2,16]   if country=='Nigeria' else [-20,-2])) &
        df_country['longitude'].between(*([1,17]  if country=='Nigeria' else [9,27]))
    )
    ws_df  = df_country[df_country['Opportunity'].isin(['Dead Whitespace','Underperforming']) & _ws_valid]
    map_ws = ws_df.sample(min(4000,len(ws_df)), random_state=42) if len(ws_df) > 4000 else ws_df
    fig_ws = px.scatter_mapbox(map_ws, lat="latitude", lon="longitude",
        color="Opportunity", color_discrete_map=color_map,
        zoom=map_zoom, height=480, hover_name="Shop Name",
        hover_data={"YTD Retailing Value":":,.1f","Retailer Subtype":True,"latitude":False,"longitude":False},
        center=map_center)
    fig_ws.update_layout(mapbox_style="carto-darkmatter", paper_bgcolor="rgba(0,0,0,0)",
        legend=dict(font=dict(color="#94A3B8",size=11), bgcolor="rgba(8,13,26,0.85)",
                    bordercolor="rgba(255,255,255,0.08)", borderwidth=1),
        margin=dict(l=0,r=0,t=0,b=0))
    st.plotly_chart(fig_ws, use_container_width=True)

    st.markdown('<div class="section-title">Dead Whitespace Outlet List</div>', unsafe_allow_html=True)
    dead_show = dead[['Shop Name','Retailer Subtype','latitude','longitude']].reset_index(drop=True)
    dead_show.index += 1
    st.dataframe(dead_show, use_container_width=True)
    csv = dead_show.to_csv().encode('utf-8')
    st.download_button("Export Dead Whitespace List", csv,
                       f"dead_whitespace_{country.lower()}.csv", "text/csv")

# ══════════════════════════════════════════════════════════════════
#  EXPANSION STRATEGY
# ══════════════════════════════════════════════════════════════════
elif page == "Expansion Strategy":
    dead     = df_country[df_country['Opportunity'] == 'Dead Whitespace']
    under    = df_country[df_country['Opportunity'] == 'Underperforming']
    active   = df_country[df_country['Opportunity'].isin(['Active','High Performer'])]
    pri_dead = dead[dead['Retailer Subtype'].str.contains('Primary', case=False, na=False)]
    sec_dead = dead[~dead['Retailer Subtype'].str.contains('Primary', case=False, na=False)]

    st.markdown(f"""
    <div class="insight-card">
        <span class="badge badge-dead">Critical Priority</span>
        <div class="insight-title">Activate {len(pri_dead):,} Dead Primary Outlets</div>
        <div class="insight-detail">Primary outlets with zero YTD sales require immediate field sales intervention.
        Revenue potential: <strong style="color:#FFFFFF">&#8358;{len(pri_dead)*mean_val/1000:,.0f}M</strong></div>
    </div>
    <div class="insight-card">
        <span class="badge badge-under">High Priority</span>
        <div class="insight-title">Convert {len(sec_dead):,} Dead Secondary Outlets</div>
        <div class="insight-detail">Secondary outlets with zero sales — largest untapped pool.
        Revenue potential: <strong style="color:#FFFFFF">&#8358;{len(sec_dead)*mean_val/1000:,.0f}M</strong></div>
    </div>
    <div class="insight-card">
        <span class="badge badge-low">Medium Priority</span>
        <div class="insight-title">Scale Up {len(under):,} Underperforming Outlets</div>
        <div class="insight-detail">Outlets selling below &#8358;{p25:,.0f}K YTD. Incremental revenue potential:
        <strong style="color:#FFFFFF">&#8358;{len(under)*(mean_val-p25)/1000:,.0f}M</strong></div>
    </div>
    <div class="insight-card">
        <span class="badge badge-high">Growth Opportunity</span>
        <div class="insight-title">Replicate {len(active):,} High-Performing Outlet Profiles</div>
        <div class="insight-detail">Analyse shared characteristics of active and high-performing outlets
        to identify new locations with equivalent potential.</div>
    </div>""", unsafe_allow_html=True)

    st.markdown('<div class="section-title">Active vs Whitespace by Retailer Type</div>', unsafe_allow_html=True)
    summary = df.groupby(['Retailer Subtype','Opportunity']).size().reset_index(name='Count')
    fig_grp = px.bar(summary, x='Retailer Subtype', y='Count', color='Opportunity',
                     color_discrete_map=color_map, barmode='stack')
    fig_grp.update_layout(**chart_layout)
    st.plotly_chart(fig_grp, use_container_width=True)
