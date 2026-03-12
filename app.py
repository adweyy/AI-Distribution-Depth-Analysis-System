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
    st.page_link("app.py",                       label="🏠  Dashboard")
    st.page_link("pages/RFM_Analysis.py",        label="📊  RFM Analysis")
    st.page_link("pages/Upload_Data.py",         label="☁️  Upload Data")
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
is_live   = data_status == "live"
is_hybrid = data_status == "hybrid"

dot_color     = "#4CAF50" if is_live else ("#6EC6F5" if is_hybrid else "#F9A825")
dot_glow      = "rgba(76,175,80,0.6)"   if is_live else ("rgba(110,198,245,0.6)" if is_hybrid else "rgba(249,168,37,0.6)")
banner_bg     = "rgba(27,138,78,0.12)"  if is_live else ("rgba(33,150,196,0.10)" if is_hybrid else "rgba(249,168,37,0.10)")
banner_border = "rgba(76,175,80,0.35)"  if is_live else ("rgba(33,150,196,0.35)" if is_hybrid else "rgba(249,168,37,0.35)")
status_label  = "Connected to Microsoft Fabric Warehouse" if is_live else ("🇳🇬 Nigeria: CSV (33,588 outlets + YTD)   |   🇦🇴 Angola: Live Fabric" if is_hybrid else "Connected to Local CSV — Both Countries")
status_sub    = "Live data — auto refreshes every hour"   if is_live else ("Hybrid mode — Nigeria uses full CSV data, Angola pulls live from Fabric" if is_hybrid else "Fabric unreachable — using CSV fallback for both countries")
icon          = "🏭" if is_live else ("⚡" if is_hybrid else "📂")

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
            Live — Microsoft Fabric
        </div>
        <div class="ds-legend-item">
            <div class="ds-legend-dot" style="background:#6EC6F5;box-shadow:0 0 6px rgba(110,198,245,0.7);"></div>
            Hybrid — CSV + Fabric
        </div>
        <div class="ds-legend-item">
            <div class="ds-legend-dot" style="background:#F9A825;box-shadow:0 0 6px rgba(249,168,37,0.7);"></div>
            CSV Fallback
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
    const doc = window.parent.document;

    // ── INJECT GLOBAL STYLES ──────────────────────────────────────────
    function injectStyles() {
        if (doc.getElementById('shalina-fx-styles')) return;
        const style = doc.createElement('style');
        style.id = 'shalina-fx-styles';
        style.textContent = `
            /* ── GRAIN TEXTURE OVERLAY ── */
            body::after {
                content: '';
                position: fixed;
                inset: 0;
                pointer-events: none;
                z-index: 9999;
                opacity: 0.035;
                background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)'/%3E%3C/svg%3E");
                background-size: 200px 200px;
            }

            /* ── FLOATING GRADIENT ORBS ── */
            .shalina-orb {
                position: fixed;
                border-radius: 50%;
                pointer-events: none;
                z-index: 0;
                filter: blur(80px);
                animation: orbFloat linear infinite;
                opacity: 0;
            }
            @keyframes orbFloat {
                0%   { transform: translate(0px, 0px) scale(1);   opacity: 0.18; }
                25%  { transform: translate(40px, -60px) scale(1.1); opacity: 0.22; }
                50%  { transform: translate(-30px, 30px) scale(0.95); opacity: 0.15; }
                75%  { transform: translate(20px, 50px) scale(1.05); opacity: 0.20; }
                100% { transform: translate(0px, 0px) scale(1);   opacity: 0.18; }
            }

            /* ── MESH ANIMATED GRADIENT on main bg ── */
            @keyframes meshShift {
                0%   { background-position: 0% 50%; }
                50%  { background-position: 100% 50%; }
                100% { background-position: 0% 50%; }
            }

            /* ── TILT 3D CARDS ── */
            .kpi-card {
                transform-style: preserve-3d;
                will-change: transform;
                transition: transform 0.15s ease, box-shadow 0.15s ease !important;
            }

            /* ── SPOTLIGHT ON CARDS ── */
            .kpi-card { position: relative; overflow: hidden; }
            .kpi-card .spotlight {
                position: absolute;
                width: 300px; height: 300px;
                background: radial-gradient(circle, rgba(255,255,255,0.12) 0%, transparent 70%);
                border-radius: 50%;
                pointer-events: none;
                transform: translate(-50%, -50%);
                opacity: 0;
                transition: opacity 0.2s ease;
            }
            .kpi-card:hover .spotlight { opacity: 1; }

            /* ── REVEAL ON SCROLL ── */
            .shalina-reveal {
                opacity: 0;
                transform: translateY(28px);
                transition: opacity 0.6s cubic-bezier(.16,1,.3,1), transform 0.6s cubic-bezier(.16,1,.3,1);
            }
            .shalina-reveal.visible {
                opacity: 1;
                transform: translateY(0);
            }

            /* ── ELASTIC BUTTON ── */
            button { transition: transform 0.18s cubic-bezier(.34,1.56,.64,1), box-shadow 0.18s ease !important; }
            button:active { transform: scale(0.93) !important; }

            /* ── CURSOR TRAIL DOT ── */
            .cursor-trail-dot {
                position: fixed;
                width: 8px; height: 8px;
                border-radius: 50%;
                pointer-events: none;
                z-index: 99999;
                mix-blend-mode: screen;
                transition: opacity 0.4s ease;
            }

            /* ── GLASSMORPHISM PANELS ── */
            .header-wrap, .ds-banner, .insight-card, .navbar-wrap {
                backdrop-filter: blur(24px) saturate(1.4) !important;
                -webkit-backdrop-filter: blur(24px) saturate(1.4) !important;
                border: 1px solid rgba(255,255,255,0.10) !important;
            }

            /* ── ANIMATED GRADIENT BORDER on hover ── */
            .kpi-card::after {
                content: '';
                position: absolute;
                inset: -1px;
                border-radius: 14px;
                padding: 1px;
                background: linear-gradient(135deg, rgba(33,150,220,0), rgba(110,198,245,0.5), rgba(168,85,247,0.3), rgba(33,150,220,0));
                background-size: 300% 300%;
                -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
                mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
                -webkit-mask-composite: xor;
                mask-composite: exclude;
                opacity: 0;
                transition: opacity 0.3s ease;
                animation: gradBorderSpin 3s linear infinite;
                pointer-events: none;
            }
            .kpi-card:hover::after { opacity: 1; }
            @keyframes gradBorderSpin {
                0%   { background-position: 0% 50%; }
                50%  { background-position: 100% 50%; }
                100% { background-position: 0% 50%; }
            }

            /* ── MAGNETIC BUTTON glow ── */
            [data-testid="stHorizontalBlock"] button:hover {
                box-shadow: 0 0 24px rgba(33,150,220,0.55), 0 0 8px rgba(110,198,245,0.4), inset 0 0 20px rgba(33,150,220,0.2) !important;
            }

            /* ── PARTICLE CANVAS ── */
            #shalina-particles {
                position: fixed;
                top: 0; left: 0;
                width: 100%; height: 100%;
                pointer-events: none;
                z-index: 0;
                opacity: 0.45;
            }
        `;
        doc.head.appendChild(style);
    }

    // ── FLOATING ORBS ─────────────────────────────────────────────────
    function addOrbs() {
        if (doc.getElementById('shalina-orb-1')) return;
        const orbs = [
            { id:'shalina-orb-1', w:600, h:600, top:'5%',  left:'10%',  color:'rgba(33,100,200,0.5)',  dur:'18s', delay:'0s'  },
            { id:'shalina-orb-2', w:500, h:500, top:'50%', left:'70%',  color:'rgba(100,50,200,0.4)',  dur:'24s', delay:'-8s' },
            { id:'shalina-orb-3', w:400, h:400, top:'80%', left:'20%',  color:'rgba(0,150,220,0.35)',  dur:'20s', delay:'-5s' },
            { id:'shalina-orb-4', w:350, h:350, top:'20%', left:'55%',  color:'rgba(80,20,180,0.3)',   dur:'15s', delay:'-12s'},
        ];
        orbs.forEach(o => {
            const el = doc.createElement('div');
            el.id = o.id;
            el.className = 'shalina-orb';
            Object.assign(el.style, {
                width: o.w+'px', height: o.h+'px',
                top: o.top, left: o.left,
                background: o.color,
                animationDuration: o.dur,
                animationDelay: o.delay,
            });
            doc.body.prepend(el);
        });
    }

    // ── PARTICLE BACKGROUND ────────────────────────────────────────────
    function addParticles() {
        if (doc.getElementById('shalina-particles')) return;
        const canvas = doc.createElement('canvas');
        canvas.id = 'shalina-particles';
        doc.body.prepend(canvas);

        const ctx = canvas.getContext('2d');
        let W, H, particles = [];

        function resize() {
            W = canvas.width  = doc.body.clientWidth  || window.parent.innerWidth;
            H = canvas.height = doc.body.clientHeight || window.parent.innerHeight;
        }
        resize();
        window.parent.addEventListener('resize', resize);

        const N = 80;
        for (let i = 0; i < N; i++) {
            particles.push({
                x: Math.random() * W,
                y: Math.random() * H,
                r: Math.random() * 1.8 + 0.4,
                vx: (Math.random() - 0.5) * 0.35,
                vy: (Math.random() - 0.5) * 0.35,
                alpha: Math.random() * 0.5 + 0.15,
            });
        }

        function draw() {
            ctx.clearRect(0, 0, W, H);
            particles.forEach(p => {
                p.x += p.vx; p.y += p.vy;
                if (p.x < 0) p.x = W; if (p.x > W) p.x = 0;
                if (p.y < 0) p.y = H; if (p.y > H) p.y = 0;

                ctx.beginPath();
                ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
                ctx.fillStyle = `rgba(110,198,245,${p.alpha})`;
                ctx.fill();
            });

            // Draw connecting lines
            for (let i = 0; i < N; i++) {
                for (let j = i + 1; j < N; j++) {
                    const dx = particles[i].x - particles[j].x;
                    const dy = particles[i].y - particles[j].y;
                    const dist = Math.sqrt(dx*dx + dy*dy);
                    if (dist < 120) {
                        ctx.beginPath();
                        ctx.moveTo(particles[i].x, particles[i].y);
                        ctx.lineTo(particles[j].x, particles[j].y);
                        ctx.strokeStyle = `rgba(33,150,196,${0.12 * (1 - dist/120)})`;
                        ctx.lineWidth = 0.5;
                        ctx.stroke();
                    }
                }
            }
            requestAnimationFrame(draw);
        }
        draw();
    }

    // ── CURSOR TRAIL ──────────────────────────────────────────────────
    function addCursorTrail() {
        if (doc.getElementById('cursor-trail-0')) return;
        const colors = ['#6EC6F5','#A855F7','#2196C4','#22C55E','#F9A825'];
        const dots = [];
        const MAX = 12;
        let mx = 0, my = 0;
        const positions = Array(MAX).fill({x:0,y:0});

        for (let i = 0; i < MAX; i++) {
            const d = doc.createElement('div');
            d.id = 'cursor-trail-' + i;
            d.className = 'cursor-trail-dot';
            d.style.background = colors[i % colors.length];
            d.style.width  = (8 - i * 0.4) + 'px';
            d.style.height = (8 - i * 0.4) + 'px';
            d.style.opacity = (1 - i / MAX) * 0.7;
            doc.body.appendChild(d);
            dots.push(d);
        }

        doc.addEventListener('mousemove', e => { mx = e.clientX; my = e.clientY; });

        let frame = [];
        frame = Array(MAX).fill({x:0,y:0}).map(()=>({x:0,y:0}));
        let raf;
        function animate() {
            frame[0] = {x: mx, y: my};
            for (let i = MAX-1; i > 0; i--) {
                frame[i] = {
                    x: frame[i].x + (frame[i-1].x - frame[i].x) * 0.35,
                    y: frame[i].y + (frame[i-1].y - frame[i].y) * 0.35,
                };
            }
            dots.forEach((d, i) => {
                d.style.left = (frame[i].x - 4) + 'px';
                d.style.top  = (frame[i].y - 4) + 'px';
            });
            requestAnimationFrame(animate);
        }
        animate();
    }

    // ── 3D TILT + SPOTLIGHT on KPI cards ─────────────────────────────
    function addTiltCards() {
        const cards = doc.querySelectorAll('.kpi-card');
        cards.forEach(card => {
            if (card.dataset.tiltDone) return;
            card.dataset.tiltDone = '1';

            // Add spotlight div
            const spot = doc.createElement('div');
            spot.className = 'spotlight';
            card.appendChild(spot);

            card.addEventListener('mousemove', e => {
                const rect = card.getBoundingClientRect();
                const cx = rect.width / 2, cy = rect.height / 2;
                const x = e.clientX - rect.left - cx;
                const y = e.clientY - rect.top  - cy;
                const rotX = (-y / cy) * 12;
                const rotY = ( x / cx) * 12;
                card.style.transform = `perspective(600px) rotateX(${rotX}deg) rotateY(${rotY}deg) scale(1.03)`;
                card.style.boxShadow = `0 20px 60px rgba(0,0,0,0.5), ${-rotY}px ${-rotX}px 30px rgba(33,150,220,0.2)`;
                spot.style.left = (e.clientX - rect.left) + 'px';
                spot.style.top  = (e.clientY - rect.top)  + 'px';
            });
            card.addEventListener('mouseleave', () => {
                card.style.transform = 'perspective(600px) rotateX(0deg) rotateY(0deg) scale(1)';
                card.style.boxShadow = '';
            });
        });
    }

    // ── REVEAL ON SCROLL ──────────────────────────────────────────────
    function addRevealOnScroll() {
        const targets = doc.querySelectorAll(
            '.kpi-card, .insight-card, .ds-banner, [data-testid="stPlotlyChart"], [data-testid="stDataFrame"]'
        );
        targets.forEach(el => {
            if (el.dataset.revealDone) return;
            el.dataset.revealDone = '1';
            el.classList.add('shalina-reveal');
        });

        const observer = new IntersectionObserver(entries => {
            entries.forEach(e => {
                if (e.isIntersecting) {
                    setTimeout(() => e.target.classList.add('visible'), 60);
                    observer.unobserve(e.target);
                }
            });
        }, { threshold: 0.1 });

        doc.querySelectorAll('.shalina-reveal').forEach(el => observer.observe(el));
    }

    // ── MOUSE POSITION REACTIVE GRADIENT ─────────────────────────────
    function addMouseGradient() {
        if (doc.getElementById('mouse-gradient')) return;
        const el = doc.createElement('div');
        el.id = 'mouse-gradient';
        Object.assign(el.style, {
            position: 'fixed',
            width: '800px', height: '800px',
            borderRadius: '50%',
            background: 'radial-gradient(circle, rgba(33,100,220,0.07) 0%, transparent 70%)',
            pointerEvents: 'none',
            zIndex: '1',
            transform: 'translate(-50%,-50%)',
            transition: 'left 0.4s ease, top 0.4s ease',
            left: '50%', top: '50%',
        });
        doc.body.appendChild(el);
        doc.addEventListener('mousemove', e => {
            el.style.left = e.clientX + 'px';
            el.style.top  = e.clientY + 'px';
        });
    }

    // ── MAGNETIC BUTTONS ──────────────────────────────────────────────
    function addMagneticButtons() {
        const btns = doc.querySelectorAll('[data-testid="stHorizontalBlock"] button');
        btns.forEach(btn => {
            if (btn.dataset.magnetDone) return;
            btn.dataset.magnetDone = '1';
            btn.style.background = 'rgba(13,40,80,0.75)';
            btn.style.color = '#FFFFFF';
            btn.style.border = '1px solid rgba(33,150,196,0.25)';
            btn.style.borderRadius = '12px';
            btn.style.fontWeight = '600';
            btn.style.fontSize = '14px';
            btn.style.width = '100%';

            btn.addEventListener('mousemove', e => {
                const rect = btn.getBoundingClientRect();
                const x = e.clientX - rect.left - rect.width  / 2;
                const y = e.clientY - rect.top  - rect.height / 2;
                btn.style.transform = `translate(${x * 0.25}px, ${y * 0.25}px) scale(1.04)`;
            });
            btn.addEventListener('mouseleave', () => {
                btn.style.transform = 'translate(0,0) scale(1)';
            });
        });
    }

    // ── NAVBAR HIDE ───────────────────────────────────────────────────
    function hideNav() {
        const nav = doc.querySelector('[data-testid="stSidebarNav"]');
        if (nav) nav.remove();
    }

    // ── MAIN INIT ─────────────────────────────────────────────────────
    function init() {
        injectStyles();
        addOrbs();
        addParticles();
        addCursorTrail();
        addMouseGradient();
        addMagneticButtons();
        addTiltCards();
        addRevealOnScroll();
        hideNav();
    }

    // Re-run on DOM changes (Streamlit re-renders)
    const observer = new MutationObserver(() => {
        addMagneticButtons();
        addTiltCards();
        addRevealOnScroll();
        hideNav();
    });

    function start() {
        try {
            init();
            observer.observe(doc.body, { childList: true, subtree: true });
        } catch(e) {
            setTimeout(start, 300);
        }
    }

    setTimeout(start, 300);
    setTimeout(start, 900);
    setTimeout(start, 2500);
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