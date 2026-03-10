import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import os

st.set_page_config(layout="wide", page_title="Shalina | Distribution Intelligence", initial_sidebar_state="expanded")

with st.sidebar:
    st.markdown("""
    <div style="padding:20px 8px 10px 8px;">
        <div style="font-family:'Poppins',sans-serif;font-size:10px;font-weight:700;
        color:rgba(100,180,220,0.7);text-transform:uppercase;letter-spacing:2px;margin-bottom:20px;">
            Navigation
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.page_link("app.py",                      label="🏠  Dashboard")
    st.page_link("pages/ROI_Calculator.py",     label="📊  ROI Calculator")
    st.page_link("pages/Upload_Data.py",        label="☁️  Upload Data")
    st.markdown("""<div style="margin-top:16px;padding:0 8px;">
        <div style="height:1px;background:linear-gradient(90deg,transparent,rgba(33,150,196,0.35),transparent);"></div>
    </div>""", unsafe_allow_html=True)
    st.markdown("<div style='margin-top:16px;padding:0 8px;font-family:Poppins,sans-serif;font-size:10px;font-weight:700;color:rgba(100,180,220,0.7);text-transform:uppercase;letter-spacing:2px;'>Data</div>", unsafe_allow_html=True)
    if st.button("🔄  Refresh Data", use_container_width=True, key="refresh_data"):
        st.cache_data.clear()
        st.rerun()
    import streamlit.components.v1 as _sc
    _sc.html("""<script>(function(){function r(){var n=window.parent.document.querySelector('[data-testid="stSidebarNav"]');if(n){n.remove();}else{setTimeout(r,200);}}r();setTimeout(r,800);setTimeout(r,2500);})();</script>""", height=0)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&family=DM+Sans:wght@400;500;600&display=swap');
* { box-sizing: border-box; }
.stApp { font-family:'DM Sans',sans-serif; color:#E0F0FF; background:linear-gradient(145deg,#071830 0%,#0B2A50 40%,#0A2040 70%,#071830 100%); min-height:100vh; position:relative; }
.stApp::before { content:''; position:fixed; inset:0; background: radial-gradient(ellipse 90% 50% at 15% 0%,rgba(0,100,200,0.25) 0%,transparent 55%), radial-gradient(ellipse 60% 40% at 85% 15%,rgba(0,150,220,0.15) 0%,transparent 50%), radial-gradient(ellipse 70% 60% at 50% 100%,rgba(0,60,140,0.20) 0%,transparent 55%); pointer-events:none; z-index:0; }
.main .block-container { background:transparent; padding-top:0rem; max-width:1400px; padding-left:2rem; padding-right:2rem; position:relative; z-index:1; }
section[data-testid="stSidebar"] { background:linear-gradient(180deg,#0B2E59 0%,#0D3B6E 100%) !important; border-right:1px solid rgba(33,150,196,0.2) !important; }
section[data-testid="stSidebar"] * { color:#B8D4EE !important; font-family:'DM Sans',sans-serif !important; }
section[data-testid="stSidebar"] [aria-selected="true"] { color:#fff !important; background:rgba(255,255,255,0.1) !important; border-radius:8px !important; }
section[data-testid="stSidebar"] a:hover { color:#fff !important; background:rgba(255,255,255,0.08) !important; border-radius:8px !important; }
[data-testid="collapsedControl"],[data-testid="stSidebarCollapseButton"],button[kind="header"],[data-testid="stSidebarNav"],[data-testid="stSidebarNavItems"],section[data-testid="stSidebar"] nav { display:none !important; }
[data-testid="stToolbar"],[data-testid="stDecoration"],header[data-testid="stHeader"],#MainMenu,footer { display:none !important; }
.header-wrap { background:rgba(10,30,60,0.7); border-radius:16px; padding:20px 28px; border:1px solid rgba(33,150,196,0.25); box-shadow:0 4px 24px rgba(0,0,0,0.3); backdrop-filter:blur(20px); margin-bottom:12px; }
.navbar-wrap { background:rgba(10,30,60,0.6); border-radius:12px; padding:6px 10px; border:1px solid rgba(33,150,196,0.2); backdrop-filter:blur(20px); margin-bottom:8px; }
.section-title { font-family:'Poppins',sans-serif; font-size:12px; font-weight:700; color:#90C8E8; margin-top:24px; margin-bottom:12px; display:flex; align-items:center; gap:10px; text-transform:uppercase; letter-spacing:1.2px; }
.section-title::before { content:''; display:inline-block; width:4px; height:14px; background:linear-gradient(180deg,#2196C4,#6EC6F5); border-radius:2px; box-shadow:0 0 8px rgba(33,150,196,0.5); }
.kpi-row { display:grid; grid-template-columns:repeat(4,1fr); gap:14px; margin-bottom:22px; margin-top:16px; }
.kpi-card { border-radius:14px; padding:20px 22px; position:relative; overflow:hidden; min-height:110px; border:1px solid rgba(255,255,255,0.1); box-shadow:0 4px 20px rgba(0,0,0,0.3); transition:transform 0.2s ease; }
.kpi-card:hover { transform:translateY(-2px); }
.kpi-card::before { content:''; position:absolute; bottom:-20px; right:-20px; width:100px; height:100px; border-radius:50%; background:rgba(255,255,255,0.10); }
.kpi-card::after  { content:''; position:absolute; bottom:-40px; right:20px; width:80px; height:80px; border-radius:50%; background:rgba(255,255,255,0.06); }
.kpi-card.navy  { background:linear-gradient(135deg,#0B2E59 0%,#1A5276 100%); }
.kpi-card.blue  { background:linear-gradient(135deg,#1A7FC4 0%,#6EC6F5 100%); }
.kpi-card.gold  { background:linear-gradient(135deg,#F9A825 0%,#F7D080 100%); }
.kpi-card.red   { background:linear-gradient(135deg,#C0392B 0%,#E74C3C 100%); }
.kpi-card.green { background:linear-gradient(135deg,#1B8A4E 0%,#4CAF50 100%); }
.kpi-card.purple{ background:linear-gradient(135deg,#6B21A8 0%,#A855F7 100%); }
.kpi-label { font-size:10px; color:rgba(255,255,255,0.85); text-transform:uppercase; letter-spacing:1px; margin-bottom:8px; font-weight:700; font-family:'Poppins',sans-serif; }
.kpi-value { font-size:32px; font-weight:700; color:#fff; line-height:1.1; font-family:'Poppins',sans-serif; }
.kpi-delta { font-size:11px; color:rgba(255,255,255,0.75); margin-top:5px; }
.country-btn { display:inline-block; padding:8px 28px; border-radius:30px; font-size:14px; font-weight:700; font-family:'Poppins',sans-serif; cursor:pointer; transition:all 0.2s; border:2px solid rgba(33,150,196,0.4); background:rgba(10,30,60,0.6); color:#90C8E8; margin-right:10px; }
.country-btn.active-ng { background:linear-gradient(135deg,#1B5E20,#4CAF50); border-color:#4CAF50; color:#fff; box-shadow:0 0 20px rgba(76,175,80,0.4); }
.country-btn.active-ao { background:linear-gradient(135deg,#7B1FA2,#CE93D8); border-color:#CE93D8; color:#fff; box-shadow:0 0 20px rgba(206,147,216,0.4); }
.insight-card { background:rgba(10,30,60,0.7); border-radius:14px; padding:16px 20px; border:1px solid rgba(33,150,196,0.15); margin-bottom:10px; box-shadow:0 2px 16px rgba(0,0,0,0.2); backdrop-filter:blur(10px); transition:border-color 0.2s; }
.insight-card:hover { border-color:rgba(33,150,196,0.4); }
.insight-title { font-size:14px; font-weight:700; color:#FFFFFF; font-family:'Poppins',sans-serif; margin-bottom:4px; }
.insight-detail { font-size:12px; color:#90B8D0; line-height:1.6; }
.badge { display:inline-block; padding:3px 10px; border-radius:20px; font-size:11px; font-weight:600; margin-bottom:8px; }
.badge-dead  { background:rgba(239,68,68,0.15);  color:#FCA5A5; border:1px solid rgba(239,68,68,0.4); }
.badge-under { background:rgba(249,168,37,0.15); color:#FCD34D; border:1px solid rgba(249,168,37,0.4); }
.badge-low   { background:rgba(33,150,196,0.15); color:#90C8E8; border:1px solid rgba(33,150,196,0.4); }
.badge-high  { background:rgba(168,85,247,0.15); color:#D8B4FE; border:1px solid rgba(168,85,247,0.4); }
.stSelectbox label { color:#90C8E8 !important; font-size:10px !important; font-weight:700 !important; text-transform:uppercase; letter-spacing:0.8px; }
[data-baseweb="select"] > div { background:rgba(10,30,60,0.8) !important; border:1px solid rgba(33,150,196,0.3) !important; border-radius:10px !important; color:#E0F0FF !important; }
[data-baseweb="select"] svg { fill:#6EC6F5 !important; }
[data-baseweb="popover"] { background:#0B2A50 !important; border:1px solid rgba(33,150,196,0.25) !important; }
[role="option"] { background:#0B2A50 !important; color:#E0F0FF !important; }
[role="option"]:hover { background:rgba(33,150,196,0.2) !important; }
[data-testid="stMetric"] { background:rgba(10,30,60,0.7) !important; border-radius:12px !important; padding:16px !important; border:1px solid rgba(33,150,196,0.2) !important; }
[data-testid="stMetricLabel"] { color:#90C8E8 !important; font-size:10px !important; font-weight:700 !important; text-transform:uppercase; }
[data-testid="stMetricValue"] { color:#FFFFFF !important; font-weight:700 !important; font-family:'Poppins',sans-serif !important; }
[data-testid="stDataFrame"] { border-radius:12px !important; border:1px solid rgba(33,150,196,0.2) !important; }
.stDownloadButton > button { background:linear-gradient(135deg,#0D3B6E,#1A7FC4) !important; color:white !important; border:none !important; border-radius:8px !important; font-weight:600 !important; padding:10px 24px !important; }
div[data-testid="stHorizontalBlock"] div[data-testid="column"] .stButton > button { background:rgba(255,255,255,0.06) !important; color:#C8E8FF !important; border:1px solid rgba(255,255,255,0.12) !important; border-radius:8px !important; font-weight:600 !important; font-size:14px !important; width:100% !important; transition:all 0.2s ease !important; }
</style>
""", unsafe_allow_html=True)

# ── LOAD DATA ──────────────────────────────────────────────────
import sys, os as _os
sys.path.insert(0, _os.path.dirname(__file__))
from fabric_connector import load_data as _load_data

df_all, data_source, data_status = _load_data()
# Debug — show in terminal
import sys
print(f"DATA STATUS: {data_status}", file=sys.stderr)
print(f"DATA SOURCE: {data_source}", file=sys.stderr)
if df_all is not None:
    print(f"ROWS LOADED: {len(df_all)}", file=sys.stderr)

if df_all is None:
    st.markdown('''<div style="background:rgba(200,50,50,0.2);border:1px solid rgba(255,80,80,0.4);
    border-radius:12px;padding:16px 20px;color:#FFAAAA;font-weight:600;font-size:13px;">
    🔴 No data available. Please add shalina_combined_data.csv to the project folder or configure Fabric credentials in .env
    </div>''', unsafe_allow_html=True)
    st.stop()

def get_stats(df):
    nonzero = df[df['YTD Retailing Value'] > 0]['YTD Retailing Value']
    p25  = nonzero.quantile(0.25) if len(nonzero) else 0
    mean = nonzero.mean()         if len(nonzero) else 0
    p75  = nonzero.quantile(0.75) if len(nonzero) else 0
    return p25, mean, p75

# ── HEADER ──────────────────────────────────────────────────
col1, col2 = st.columns([1, 9])
with col1:
    if os.path.exists("shalina_healthcare_logo.png"):
        st.image("shalina_healthcare_logo.png", width=110)
with col2:
    st.markdown("""
    <div class="header-wrap">
        <div style="font-family:'DM Sans',sans-serif;font-size:11px;font-weight:600;color:#90C8E8;letter-spacing:2px;text-transform:uppercase;margin-bottom:4px;">Shalina Healthcare</div>
        <div style="font-family:'Poppins',sans-serif;font-size:36px;font-weight:700;color:#FFFFFF;letter-spacing:-0.5px;line-height:1.1;">AI Distribution Depth Analysis System</div>
    </div>
    """, unsafe_allow_html=True)

# ── DATA SOURCE BANNER ────────────────────────────────────────
is_live = data_status == "live"
dot_color     = "#4CAF50" if is_live else "#F9A825"
dot_glow      = "rgba(76,175,80,0.6)"  if is_live else "rgba(249,168,37,0.6)"
banner_bg     = "rgba(27,138,78,0.12)" if is_live else "rgba(249,168,37,0.10)"
banner_border = "rgba(76,175,80,0.35)" if is_live else "rgba(249,168,37,0.35)"
status_label  = "Connected to Microsoft Fabric Warehouse" if is_live else "Connected to Local CSV File"
status_sub    = "Live data — auto refreshes every hour"   if is_live else "Waiting for Fabric credentials from IT"
icon          = "🏭" if is_live else "📂"

st.markdown(f"""
<style>
@keyframes pulse {{
  0%   {{ box-shadow: 0 0 0 0 {dot_glow}, 0 0 8px {dot_color}; opacity:1; }}
  50%  {{ box-shadow: 0 0 0 8px transparent, 0 0 16px {dot_color}; opacity:0.7; }}
  100% {{ box-shadow: 0 0 0 0 {dot_glow}, 0 0 8px {dot_color}; opacity:1; }}
}}
@keyframes ripple {{
  0%   {{ transform: scale(1);   opacity:0.6; }}
  100% {{ transform: scale(2.5); opacity:0; }}
}}
.ds-banner {{
    background: {banner_bg};
    border: 1px solid {banner_border};
    border-radius: 12px;
    padding: 12px 20px;
    margin-bottom: 14px;
    display: flex;
    align-items: center;
    gap: 16px;
    backdrop-filter: blur(10px);
}}
.ds-dot-wrap {{
    position: relative;
    width: 14px;
    height: 14px;
    flex-shrink: 0;
}}
.ds-dot {{
    width: 14px; height: 14px;
    border-radius: 50%;
    background: {dot_color};
    animation: pulse 2s ease-in-out infinite;
    position: relative; z-index: 2;
}}
.ds-ripple {{
    position: absolute;
    top: 0; left: 0;
    width: 14px; height: 14px;
    border-radius: 50%;
    background: {dot_color};
    animation: ripple 2s ease-out infinite;
    z-index: 1;
}}
.ds-icon {{ font-size: 20px; }}
.ds-text {{ flex: 1; }}
.ds-label {{ font-family:'Poppins',sans-serif; font-size:13px; font-weight:700; color:#FFFFFF; }}
.ds-sub {{ font-size:11px; color:#90B8D0; margin-top:2px; font-weight:400; }}
.ds-legend {{ display:flex; flex-direction:column; gap:5px; align-items:flex-end; }}
.ds-legend-item {{ display:flex; align-items:center; gap:6px; font-size:10px; color:#90B8D0; font-weight:600; text-transform:uppercase; letter-spacing:0.8px; }}
.ds-legend-dot {{ width:8px; height:8px; border-radius:50%; flex-shrink:0; }}
</style>
<div class="ds-banner">
    <div class="ds-dot-wrap">
        <div class="ds-ripple"></div>
        <div class="ds-dot"></div>
    </div>
    <div class="ds-icon">{icon}</div>
    <div class="ds-text">
        <div class="ds-label">{status_label}</div>
        <div class="ds-sub">{status_sub}</div>
    </div>
    <div class="ds-legend">
        <div class="ds-legend-item">
            <div class="ds-legend-dot" style="background:#4CAF50;box-shadow:0 0 6px rgba(76,175,80,0.7);"></div>
            Microsoft Fabric Warehouse
        </div>
        <div class="ds-legend-item">
            <div class="ds-legend-dot" style="background:#F9A825;box-shadow:0 0 6px rgba(249,168,37,0.7);"></div>
            Local CSV File
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── COUNTRY SWITCHER ──────────────────────────────────────────
if "country" not in st.session_state:
    st.session_state.country = "Nigeria"

st.markdown("<div style='margin:12px 0 6px 0;font-family:Poppins,sans-serif;font-size:10px;font-weight:700;color:#90C8E8;text-transform:uppercase;letter-spacing:1.5px;'>Select Country</div>", unsafe_allow_html=True)
cc1, cc2, cc3 = st.columns([1, 1, 8])
with cc1:
    if st.button("🇳🇬  Nigeria", use_container_width=True, key="btn_ng"):
        st.session_state.country = "Nigeria"
with cc2:
    if st.button("🇦🇴  Angola", use_container_width=True, key="btn_ao"):
        st.session_state.country = "Angola"

country = st.session_state.country
df_country = df_all[df_all['country'] == country].copy()
p25, mean_val, p75 = get_stats(df_country)

# Country colour accent
accent = "#4CAF50" if country == "Nigeria" else "#CE93D8"
st.markdown(f"<div style='height:3px;background:linear-gradient(90deg,{accent},transparent);border-radius:2px;margin-bottom:12px;'></div>", unsafe_allow_html=True)

# ── NAVBAR ──────────────────────────────────────────────────
if "nav_page" not in st.session_state:
    st.session_state.nav_page = "Dashboard"

st.markdown('<div class="navbar-wrap"></div>', unsafe_allow_html=True)
n1, n2, n3, n4 = st.columns(4)
with n1:
    if st.button("Dashboard",            use_container_width=True, key="nav_dash"):   st.session_state.nav_page = "Dashboard"
with n2:
    if st.button("Outlet Performance",   use_container_width=True, key="nav_perf"):   st.session_state.nav_page = "Outlet Performance"
with n3:
    if st.button("Whitespace Detection", use_container_width=True, key="nav_white"):  st.session_state.nav_page = "Whitespace Detection"
with n4:
    if st.button("Expansion Strategy",   use_container_width=True, key="nav_expand"): st.session_state.nav_page = "Expansion Strategy"

import streamlit.components.v1 as components
components.html("""
<script>
(function() {
    function applyStyles() {
        const doc = window.parent.document;
        const allBtns = doc.querySelectorAll('[data-testid="stHorizontalBlock"] button');
        if (!allBtns || allBtns.length === 0) { setTimeout(applyStyles, 300); return; }
        allBtns.forEach(function(btn) {
            btn.style.background='rgba(13,40,80,0.75)'; btn.style.color='#FFFFFF';
            btn.style.border='1px solid rgba(33,150,196,0.25)'; btn.style.borderRadius='12px';
            btn.style.fontWeight='600'; btn.style.fontSize='14px';
            btn.style.boxShadow='0 2px 12px rgba(0,0,0,0.3)'; btn.style.transition='all 0.25s ease'; btn.style.width='100%';
            btn.onmouseenter=function(){btn.style.background='rgba(33,150,220,0.35)';btn.style.borderColor='rgba(110,198,245,0.9)';btn.style.boxShadow='0 0 22px rgba(33,150,220,0.6),0 0 8px rgba(110,198,245,0.5),inset 0 0 20px rgba(33,150,220,0.25)';btn.style.transform='scale(1.025)';};
            btn.onmouseleave=function(){btn.style.background='rgba(13,40,80,0.75)';btn.style.borderColor='rgba(33,150,196,0.25)';btn.style.boxShadow='0 2px 12px rgba(0,0,0,0.3)';btn.style.transform='scale(1)';};
        });
        const nav=doc.querySelector('[data-testid="stSidebarNav"]'); if(nav) nav.remove();
    }
    setTimeout(applyStyles,400); setTimeout(applyStyles,1200); setTimeout(applyStyles,3000);
})();
</script>
""", height=0)

# ── FILTERS ──────────────────────────────────────────────────
st.markdown("<div style='margin-top:12px;'></div>", unsafe_allow_html=True)
f1, f2 = st.columns(2)
with f1:
    subtype_opts = ["All"] + sorted(df_country['Retailer Subtype'].dropna().unique().tolist())
    selected_subtype = st.selectbox("Retailer Subtype", subtype_opts)
with f2:
    opp_opts = ["All", "Dead Whitespace", "Underperforming", "Low Performer", "Active", "High Performer"]
    selected_opp = st.selectbox("Opportunity Category", opp_opts)

df = df_country.copy()
if selected_subtype != "All": df = df[df['Retailer Subtype'] == selected_subtype]
if selected_opp != "All":     df = df[df['Opportunity'] == selected_opp]

if len(df) == 0:
    st.markdown('<div style="background:rgba(200,50,50,0.15);border:1px solid rgba(255,100,100,0.4);border-radius:10px;padding:14px 16px;font-size:13px;color:#FFAAAA;font-weight:600;margin:16px 0;">⚠️ No outlets match the selected filters.</div>', unsafe_allow_html=True)
    st.stop()

page = st.session_state.nav_page

color_map = {
    'Dead Whitespace': '#EF4444',
    'Underperforming': '#F97316',
    'Low Performer':   '#EAB308',
    'Active':          '#22C55E',
    'High Performer':  '#A855F7'
}
chart_layout = dict(
    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(10,30,60,0.5)",
    font=dict(color="#90C8E8", size=11), height=380,
    xaxis=dict(gridcolor="rgba(33,150,196,0.1)", linecolor="rgba(33,150,196,0.2)", color="#6AACE0"),
    yaxis=dict(gridcolor="rgba(33,150,196,0.1)", linecolor="rgba(33,150,196,0.2)", color="#6AACE0"),
    margin=dict(l=0, r=0, t=20, b=0),
    legend=dict(font=dict(color="#FFFFFF"), bgcolor="rgba(10,30,60,0.7)")
)

map_center = {"lat": 9.0, "lon": 8.0} if country == "Nigeria" else {"lat": -11.0, "lon": 17.5}
map_zoom   = 5 if country == "Nigeria" else 4

# ════════════════════════════════════════════════════════
# DASHBOARD
# ════════════════════════════════════════════════════════
if page == "Dashboard":
    total_outlets   = len(df)
    dead_outlets    = len(df[df['Opportunity'] == 'Dead Whitespace'])
    high_performers = len(df[df['Opportunity'] == 'High Performer'])
    total_ytd       = df['YTD Retailing Value'].sum()
    ws_pct          = round(dead_outlets / total_outlets * 100, 1)

    st.markdown(f"""
    <div class="kpi-row">
        <div class="kpi-card navy">
            <div class="kpi-label">Total Outlets — {country}</div>
            <div class="kpi-value">{total_outlets:,}</div>
            <div class="kpi-delta">Distribution network</div>
        </div>
        <div class="kpi-card red">
            <div class="kpi-label">Dead Whitespace</div>
            <div class="kpi-value">{dead_outlets:,}</div>
            <div class="kpi-delta">{ws_pct}% of total — zero YTD sales</div>
        </div>
        <div class="kpi-card purple">
            <div class="kpi-label">High Performers</div>
            <div class="kpi-value">{high_performers:,}</div>
            <div class="kpi-delta">Above ₦{p75:,.0f}K YTD</div>
        </div>
        <div class="kpi-card gold">
            <div class="kpi-label">Total YTD Revenue</div>
            <div class="kpi-value">₦{total_ytd/1000:,.0f}M</div>
            <div class="kpi-delta">Across all active outlets</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-title">Geographic Outlet Distribution Map</div>', unsafe_allow_html=True)
    map_df = df.sample(min(5000, len(df)), random_state=42) if len(df) > 5000 else df
    fig_map = px.scatter_mapbox(map_df, lat="latitude", lon="longitude",
        color="Opportunity", color_discrete_map=color_map,
        size_max=12, zoom=map_zoom, height=500,
        hover_name="Shop Name",
        hover_data={"YTD Retailing Value":":,.1f","Retailer Subtype":True,"latitude":False,"longitude":False},
        center=map_center)
    fig_map.update_layout(mapbox_style="open-street-map", paper_bgcolor="rgba(0,0,0,0)",
        legend=dict(font=dict(color="#FFFFFF",size=12), bgcolor="rgba(10,30,60,0.85)",
                    bordercolor="rgba(33,150,196,0.3)", borderwidth=1),
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

# ════════════════════════════════════════════════════════
# OUTLET PERFORMANCE
# ════════════════════════════════════════════════════════
elif page == "Outlet Performance":
    st.markdown('<div class="section-title">Top 20 Outlets by YTD Retailing Value</div>', unsafe_allow_html=True)
    top20 = df[df['YTD Retailing Value'] > 0].nlargest(20, 'YTD Retailing Value')[
        ['Shop Name','Retailer Subtype','YTD Retailing Value','Opportunity']].reset_index(drop=True)
    top20.index += 1
    top20['YTD Retailing Value'] = top20['YTD Retailing Value'].apply(lambda x: f"₦{x:,.1f}K")
    st.dataframe(top20, use_container_width=True)

    st.markdown('<div class="section-title">YTD Revenue Distribution</div>', unsafe_allow_html=True)
    active_df = df[df['YTD Retailing Value'] > 0]
    fig_hist = px.histogram(active_df, x='YTD Retailing Value', nbins=60,
                             color='Retailer Subtype', color_discrete_sequence=['#A855F7','#2196C4','#22C55E'])
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
                         color='Retailer Subtype', color_discrete_sequence=['#A855F7','#2196C4','#22C55E'])
        fig_sub.update_layout(**chart_layout)
        st.plotly_chart(fig_sub, use_container_width=True)

# ════════════════════════════════════════════════════════
# WHITESPACE DETECTION
# ════════════════════════════════════════════════════════
elif page == "Whitespace Detection":
    dead  = df[df['Opportunity'] == 'Dead Whitespace']
    under = df[df['Opportunity'] == 'Underperforming']
    total_ws = len(dead) + len(under)
    revenue_potential = total_ws * mean_val

    st.markdown(f"""
    <div class="kpi-row">
        <div class="kpi-card red">
            <div class="kpi-label">Dead Whitespace Outlets</div>
            <div class="kpi-value">{len(dead):,}</div>
            <div class="kpi-delta">Zero YTD sales — highest priority</div>
        </div>
        <div class="kpi-card gold">
            <div class="kpi-label">Underperforming Outlets</div>
            <div class="kpi-value">{len(under):,}</div>
            <div class="kpi-delta">Below ₦{p25:,.0f}K YTD</div>
        </div>
        <div class="kpi-card blue">
            <div class="kpi-label">Total Whitespace</div>
            <div class="kpi-value">{total_ws:,}</div>
            <div class="kpi-delta">{round(total_ws/len(df)*100,1)}% of filtered outlets</div>
        </div>
        <div class="kpi-card green">
            <div class="kpi-label">Revenue Potential</div>
            <div class="kpi-value">₦{revenue_potential/1000:,.0f}M</div>
            <div class="kpi-delta">If activated to avg performance</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-title">Whitespace Outlets Map</div>', unsafe_allow_html=True)
    ws_df = df[df['Opportunity'].isin(['Dead Whitespace','Underperforming'])]
    map_ws = ws_df.sample(min(4000,len(ws_df)), random_state=42) if len(ws_df) > 4000 else ws_df
    fig_ws = px.scatter_mapbox(map_ws, lat="latitude", lon="longitude",
        color="Opportunity", color_discrete_map=color_map,
        zoom=map_zoom, height=480, hover_name="Shop Name",
        hover_data={"YTD Retailing Value":":,.1f","Retailer Subtype":True,"latitude":False,"longitude":False},
        center=map_center)
    fig_ws.update_layout(mapbox_style="open-street-map", paper_bgcolor="rgba(0,0,0,0)",
        legend=dict(font=dict(color="#FFFFFF",size=12), bgcolor="rgba(10,30,60,0.85)",
                    bordercolor="rgba(33,150,196,0.3)", borderwidth=1),
        margin=dict(l=0,r=0,t=0,b=0))
    st.plotly_chart(fig_ws, use_container_width=True)

    st.markdown('<div class="section-title">Dead Whitespace Outlet List</div>', unsafe_allow_html=True)
    dead_show = dead[['Shop Name','Retailer Subtype','latitude','longitude']].reset_index(drop=True)
    dead_show.index += 1
    st.dataframe(dead_show, use_container_width=True)
    csv = dead_show.to_csv().encode('utf-8')
    st.download_button("⬇️ Export Dead Whitespace List", csv, f"dead_whitespace_{country.lower()}.csv", "text/csv")

# ════════════════════════════════════════════════════════
# EXPANSION STRATEGY
# ════════════════════════════════════════════════════════
elif page == "Expansion Strategy":
    dead   = df[df['Opportunity'] == 'Dead Whitespace']
    under  = df[df['Opportunity'] == 'Underperforming']
    active = df[df['Opportunity'].isin(['Active','High Performer'])]
    pri_dead = dead[dead['Retailer Subtype'].str.contains('Primary', case=False, na=False)]
    sec_dead = dead[~dead['Retailer Subtype'].str.contains('Primary', case=False, na=False)]

    st.markdown(f"""
    <div class="insight-card">
        <span class="badge badge-dead">🔴 Critical Priority</span>
        <div class="insight-title">Activate {len(pri_dead):,} Dead Primary Outlets</div>
        <div class="insight-detail">Primary outlets with zero YTD sales need immediate sales team intervention.
        Revenue potential: <strong style="color:#FFFFFF">₦{len(pri_dead)*mean_val/1000:,.0f}M</strong></div>
    </div>
    <div class="insight-card">
        <span class="badge badge-under">🟠 High Priority</span>
        <div class="insight-title">Convert {len(sec_dead):,} Dead Secondary Outlets</div>
        <div class="insight-detail">Secondary outlets with zero sales — largest untapped pool.
        Revenue potential: <strong style="color:#FFFFFF">₦{len(sec_dead)*mean_val/1000:,.0f}M</strong></div>
    </div>
    <div class="insight-card">
        <span class="badge badge-low">🟡 Medium Priority</span>
        <div class="insight-title">Scale Up {len(under):,} Underperforming Outlets</div>
        <div class="insight-detail">Outlets selling below ₦{p25:,.0f}K YTD. Incremental revenue potential:
        <strong style="color:#FFFFFF">₦{len(under)*(mean_val-p25)/1000:,.0f}M</strong></div>
    </div>
    <div class="insight-card">
        <span class="badge badge-high">🟣 Growth</span>
        <div class="insight-title">Replicate {len(active):,} High Performing Outlet Profiles</div>
        <div class="insight-detail">Analyse what active & high-performing outlets have in common and use that
        profile to identify new outlet locations with similar characteristics.</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-title">Active vs Whitespace by Retailer Type</div>', unsafe_allow_html=True)
    summary = df.groupby(['Retailer Subtype','Opportunity']).size().reset_index(name='Count')
    fig_grp = px.bar(summary, x='Retailer Subtype', y='Count', color='Opportunity',
                     color_discrete_map=color_map, barmode='stack')
    fig_grp.update_layout(**chart_layout)
    st.plotly_chart(fig_grp, use_container_width=True)