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
    st.page_link("app.py",                       label="Dashboard")
    st.page_link("pages/RFM_Analysis.py",        label="RFM Analysis")
    st.page_link("pages/Upload_Data.py",         label="Upload Data")
    st.markdown("""<div style="margin-top:16px;padding:0 8px;">
        <div style="height:1px;background:linear-gradient(90deg,transparent,rgba(33,150,196,0.35),transparent);"></div>
    </div>""", unsafe_allow_html=True)
    st.markdown("<div style='margin-top:16px;padding:0 8px;font-family:Poppins,sans-serif;font-size:10px;font-weight:700;color:rgba(100,180,220,0.7);text-transform:uppercase;letter-spacing:2px;'>Data</div>", unsafe_allow_html=True)
    if st.button("Refresh Data", use_container_width=True, key="refresh_data"):
        st.cache_data.clear()
        st.rerun()
    import streamlit.components.v1 as _sc
    _sc.html("""<script>(function(){function r(){var n=window.parent.document.querySelector('[data-testid="stSidebarNav"]');if(n){n.remove();}else{setTimeout(r,200);}}r();setTimeout(r,800);setTimeout(r,2500);})();</script>""", height=0)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500&display=swap');
* { box-sizing: border-box; }

/*  DEEP SPACE BACKGROUND  */
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

/*  SIDEBAR  */
section[data-testid="stSidebar"] {
    background: rgba(8,13,26,0.95) !important;
    border-right: 1px solid rgba(255,255,255,0.06) !important;
}
section[data-testid="stSidebar"] * { color: #94A3B8 !important; font-family: 'Inter', sans-serif !important; }
section[data-testid="stSidebar"] a:hover { color: #fff !important; background: rgba(255,255,255,0.06) !important; border-radius: 8px !important; }
[data-testid="collapsedControl"],[data-testid="stSidebarCollapseButton"],button[kind="header"],
[data-testid="stSidebarNav"],[data-testid="stSidebarNavItems"],section[data-testid="stSidebar"] nav { display:none !important; }
[data-testid="stToolbar"],[data-testid="stDecoration"],header[data-testid="stHeader"],#MainMenu,footer { display:none !important; }

/*  MISSION CONTROL TOP BAR  */
.mc-topbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 14px 0 10px 0;
    border-bottom: 1px solid rgba(255,255,255,0.06);
    margin-bottom: 16px;
}
.mc-title-wrap {}
.mc-eyebrow {
    font-size: 10px; font-weight: 600; letter-spacing: 3px;
    text-transform: uppercase; color: #475569; margin-bottom: 4px;
}
.mc-title {
    font-size: 22px; font-weight: 800; color: #F1F5F9;
    letter-spacing: -0.5px; line-height: 1.1;
}
.mc-title span { color: #3B82F6; }
.mc-status-group { display: flex; gap: 16px; align-items: center; }
.mc-status-pill {
    display: flex; align-items: center; gap: 7px;
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 20px; padding: 5px 12px;
    font-size: 10px; font-weight: 700; letter-spacing: 1.5px;
    text-transform: uppercase; color: #94A3B8;
}
.mc-status-dot {
    width: 7px; height: 7px; border-radius: 50%;
    background: #22C55E;
    box-shadow: 0 0 8px rgba(34,197,94,0.8), 0 0 16px rgba(34,197,94,0.4);
    animation: statusPulse 2s ease-in-out infinite;
}
.mc-status-dot.amber { background:#F59E0B; box-shadow:0 0 8px rgba(245,158,11,0.8), 0 0 16px rgba(245,158,11,0.4); }
@keyframes statusPulse {
    0%,100% { opacity:1; } 50% { opacity:0.4; }
}

/*  FILTER BAR  */
.filter-bar {
    display: flex; align-items: center; gap: 12px;
    background: transparent;
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 10px; padding: 10px 16px;
    margin-bottom: 14px;
}

/*  NAV TABS  */
.nav-tab-bar {
    display: flex; gap: 2px;
    border-bottom: 1px solid rgba(255,255,255,0.06);
    margin-bottom: 20px;
}

/*  KPI CARDS — MISSION CONTROL STYLE  */
.kpi-row { display:grid; grid-template-columns:repeat(4,1fr); gap:12px; margin-bottom:20px; }
.kpi-card {
    border-radius: 12px; padding: 20px 20px 16px 20px;
    position: relative; overflow: hidden;
    min-height: 120px;
    border: 1px solid rgba(255,255,255,0.08);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
    cursor: default;
}
.kpi-card:hover { transform: translateY(-3px); }
.kpi-card::before {
    content: ''; position: absolute;
    top: -60px; right: -60px;
    width: 180px; height: 180px;
    border-radius: 50%;
    background: rgba(255,255,255,0.04);
    pointer-events: none;
}
/* Blue */
.kpi-card.mc-blue {
    background: linear-gradient(135deg, #0f172a 0%, #1e3a5f 100%);
    box-shadow: 0 4px 24px rgba(59,130,246,0.15), inset 0 1px 0 rgba(59,130,246,0.2);
    border-color: rgba(59,130,246,0.25);
}
/* Orange */
.kpi-card.mc-orange {
    background: linear-gradient(135deg, #1a0f00 0%, #5c2400 100%);
    box-shadow: 0 4px 24px rgba(249,115,22,0.15), inset 0 1px 0 rgba(249,115,22,0.2);
    border-color: rgba(249,115,22,0.25);
}
/* Purple */
.kpi-card.mc-purple {
    background: linear-gradient(135deg, #0f0a1a 0%, #3b1f6e 100%);
    box-shadow: 0 4px 24px rgba(139,92,246,0.15), inset 0 1px 0 rgba(139,92,246,0.2);
    border-color: rgba(139,92,246,0.25);
}
/* Amber */
.kpi-card.mc-amber {
    background: linear-gradient(135deg, #1a1400 0%, #5c4500 100%);
    box-shadow: 0 4px 24px rgba(245,158,11,0.15), inset 0 1px 0 rgba(245,158,11,0.2);
    border-color: rgba(245,158,11,0.25);
}
/* Red */
.kpi-card.mc-red {
    background: linear-gradient(135deg, #1a0505 0%, #5c1010 100%);
    box-shadow: 0 4px 24px rgba(239,68,68,0.15), inset 0 1px 0 rgba(239,68,68,0.2);
    border-color: rgba(239,68,68,0.25);
}
/* Green */
.kpi-card.mc-green {
    background: linear-gradient(135deg, #051a0f 0%, #0d5c2a 100%);
    box-shadow: 0 4px 24px rgba(34,197,94,0.15), inset 0 1px 0 rgba(34,197,94,0.2);
    border-color: rgba(34,197,94,0.25);
}
.kpi-accent-line {
    height: 2px; width: 40px; border-radius: 1px;
    margin-bottom: 12px;
}
.kpi-label {
    font-size: 10px; font-weight: 600; letter-spacing: 1.5px;
    text-transform: uppercase; color: #64748B; margin-bottom: 6px;
}
.kpi-value {
    font-size: 36px; font-weight: 800; color: #F8FAFC;
    line-height: 1; font-family: 'Inter', sans-serif;
    letter-spacing: -1px;
}
.kpi-delta { font-size: 11px; color: #475569; margin-top: 6px; }

/*  SECTION TITLE — BORDERLESS  */
.section-title {
    font-size: 11px; font-weight: 700; letter-spacing: 2px;
    text-transform: uppercase; color: #475569;
    margin-top: 24px; margin-bottom: 12px;
    display: flex; align-items: center; gap: 10px;
}
.section-title::after {
    content: ''; flex: 1; height: 1px;
    background: linear-gradient(90deg, rgba(255,255,255,0.08), transparent);
}

/*  INSIGHT CARDS  */
.insight-card {
    background: rgba(255,255,255,0.025);
    border-radius: 12px; padding: 16px 20px;
    border: 1px solid rgba(255,255,255,0.07);
    margin-bottom: 10px;
    transition: border-color 0.2s, background 0.2s;
}
.insight-card:hover {
    background: rgba(255,255,255,0.04);
    border-color: rgba(255,255,255,0.12);
}
.insight-title { font-size: 14px; font-weight: 700; color: #F1F5F9; margin-bottom: 4px; }
.insight-detail { font-size: 12px; color: #64748B; line-height: 1.6; }

/*  BADGES  */
.badge { display:inline-block; padding:3px 10px; border-radius:20px; font-size:10px; font-weight:700; margin-bottom:8px; letter-spacing:0.5px; }
.badge-dead  { background:rgba(239,68,68,0.12);  color:#FCA5A5; border:1px solid rgba(239,68,68,0.3); }
.badge-under { background:rgba(249,115,22,0.12); color:#FDBA74; border:1px solid rgba(249,115,22,0.3); }
.badge-low   { background:rgba(59,130,246,0.12); color:#93C5FD; border:1px solid rgba(59,130,246,0.3); }
.badge-high  { background:rgba(139,92,246,0.12); color:#C4B5FD; border:1px solid rgba(139,92,246,0.3); }

/*  DATA SOURCE BANNER  */
.ds-banner {
    background: rgba(255,255,255,0.025);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 10px; padding: 10px 16px;
    margin-bottom: 14px; display: flex;
    align-items: center; gap: 14px;
}
.ds-dot-wrap { position:relative; width:10px; height:10px; flex-shrink:0; }
.ds-dot { width:10px; height:10px; border-radius:50%; position:relative; z-index:2; animation: statusPulse 2s ease-in-out infinite; }
.ds-ripple { position:absolute; top:0; left:0; width:10px; height:10px; border-radius:50%; animation: ripple 2s ease-out infinite; z-index:1; }
@keyframes ripple { 0% { transform:scale(1); opacity:0.6; } 100% { transform:scale(2.8); opacity:0; } }
.ds-label { font-size:12px; font-weight:600; color:#E2E8F0; }
.ds-sub { font-size:11px; color:#475569; margin-top:1px; }
.ds-legend { display:flex; flex-direction:column; gap:4px; align-items:flex-end; margin-left:auto; }
.ds-legend-item { display:flex; align-items:center; gap:5px; font-size:9px; color:#475569; font-weight:600; text-transform:uppercase; letter-spacing:1px; }
.ds-legend-dot { width:6px; height:6px; border-radius:50%; flex-shrink:0; }

/*  COUNTRY BUTTON  */
div[data-testid="stHorizontalBlock"] div[data-testid="column"] .stButton > button {
    background: rgba(255,255,255,0.04) !important;
    color: #94A3B8 !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 8px !important;
    font-weight: 600 !important; font-size: 13px !important;
    width: 100% !important; transition: all 0.2s ease !important;
    letter-spacing: 0.3px;
}
div[data-testid="stHorizontalBlock"] div[data-testid="column"] .stButton > button:hover {
    background: rgba(59,130,246,0.15) !important;
    border-color: rgba(59,130,246,0.4) !important;
    color: #E2E8F0 !important;
}

/*  SELECTS  */
.stSelectbox label { color:#475569 !important; font-size:10px !important; font-weight:700 !important; text-transform:uppercase; letter-spacing:1px; }
[data-baseweb="select"] > div { background:rgba(255,255,255,0.04) !important; border:1px solid rgba(255,255,255,0.08) !important; border-radius:8px !important; color:#E2E8F0 !important; }
[data-baseweb="select"] svg { fill:#475569 !important; }
[data-baseweb="popover"] { background:#0f172a !important; border:1px solid rgba(255,255,255,0.1) !important; }
[role="option"] { background:#0f172a !important; color:#E2E8F0 !important; }
[role="option"]:hover { background:rgba(59,130,246,0.15) !important; }

/*  TABLE / DATAFRAME  */
[data-testid="stImageContainer"] button,
[data-testid="StyledFullScreenButton"] { display: none !important; }
[data-testid="stDataFrame"] { border-radius:10px !important; border:1px solid rgba(255,255,255,0.07) !important; }
.stDownloadButton > button { background:rgba(59,130,246,0.15) !important; color:#93C5FD !important; border:1px solid rgba(59,130,246,0.3) !important; border-radius:8px !important; font-weight:600 !important; }
.stDownloadButton > button:hover { background:rgba(59,130,246,0.25) !important; }

/*  SPOTLIGHT  */
.kpi-card .spotlight {
    position:absolute; width:250px; height:250px;
    background:radial-gradient(circle,rgba(255,255,255,0.08) 0%,transparent 70%);
    border-radius:50%; pointer-events:none;
    transform:translate(-50%,-50%); opacity:0;
    transition:opacity 0.2s ease;
}
.kpi-card:hover .spotlight { opacity:1; }

/*  REVEAL  */
.shalina-reveal { opacity:0; transform:translateY(40px) scale(0.98); transition:opacity 0.7s cubic-bezier(.16,1,.3,1), transform 0.7s cubic-bezier(.16,1,.3,1); will-change:opacity,transform; }
.shalina-reveal.visible { opacity:1; transform:translateY(0) scale(1); }
.shalina-reveal:nth-child(2) { transition-delay:0.08s; }
.shalina-reveal:nth-child(3) { transition-delay:0.16s; }
.shalina-reveal:nth-child(4) { transition-delay:0.24s; }
</style>
""", unsafe_allow_html=True)

#  LOAD DATA 
import sys, os as _os
sys.path.insert(0, _os.path.dirname(__file__))
from fabric_connector import load_data as _load_data

df_all, data_source, data_status = _load_data()

if df_all is None:
    st.markdown('''<div style="background:rgba(200,50,50,0.2);border:1px solid rgba(255,80,80,0.4);
    border-radius:12px;padding:16px 20px;color:#FFAAAA;font-weight:600;font-size:13px;">
     No data available. Please add shalina_combined_data.csv to the project folder or configure Fabric credentials in .env
    </div>''', unsafe_allow_html=True)
    st.stop()

def get_stats(df):
    nonzero = df[df['YTD Retailing Value'] > 0]['YTD Retailing Value']
    p25  = nonzero.quantile(0.25) if len(nonzero) else 0
    mean = nonzero.mean()         if len(nonzero) else 0
    p75  = nonzero.quantile(0.75) if len(nonzero) else 0
    return p25, mean, p75

#  MISSION CONTROL TOP BAR 
sync_color = "#22C55E" if data_status in ("live","hybrid") else "#F59E0B"
sync_label = "DATA SYNC: STABLE" if data_status in ("live","hybrid") else "DATA SYNC: CSV"

import base64 as _b64, os as _os
_logo_file = next((f for f in ['shalina_healthcare_logo.jfif','shalina_healthcare_logo.png','shalina_logo.png'] if _os.path.exists(f)), None)
if _logo_file:
    _logo_ext  = 'jpeg' if _logo_file.endswith('.jfif') else 'png'
    _logo_b64  = _b64.b64encode(open(_logo_file,'rb').read()).decode()
    _logo_mime = f'image/{_logo_ext}'
else:
    _logo_mime = 'image/png'
    _logo_b64  = "iVBORw0KGgoAAAANSUhEUgAAAjAAAACgCAYAAAASCFYFAAAXQUlEQVR4nO3de7QkVX3o8e9ATVE8ZmCAARERbOIAKgbFINooii8MxjsqBklICwZXWBrIijeLEGNi1It4cyVKriEkEcU24SoySiJGIwLx0QhBkiEqEYnNU1FA3o+iLDj3j10He9pzTlc/z6nu72etXnO6e1ftfWr3nP3rXfsBkiRJkiRJkiRJkiRJkiRJkiRJkiRJkiRJkqTltGrcGaxZv2Fu3HlovB648/tj/5xIktSPsTRMBi3Ty2BGkrQSjLQxMnCZHQYykqTlNJJGyMBldhnISJKWw1bDnsDgZbZZ/5Kk5TBUAGPjJfBzIEmavIEDGBstdfLzIEmapIECGBsrLcTPhSRpUvoOYGyktBQ/H5KkSegrgLFxUhl+TiRJ4zb0LCRJkqRJKx3A+K1a/fDzIkkaJ3tgJElS5ZQKYPw2rUH4uZEkjYs9MNIYpVl+Yprlcz0eFy53OVeSUV0zr7003QxgJElS5US9EngbQMNYs37D3KQ3fEyzfCvgucAhwIHAvsCewC7AGiAmBO8/Ax4G7gF+AtwMfA/YDHw9iaO7J1luSVJ5PQMYqSrSLH8xcALwa4RgpZdtisc6oAa8oOO9uTTLvwn8A9BM4ujBERdXkjQEbyGp8tIsf1ERbHwVOJ5ywUsvq4AXAn8F3JJm+e+lWT7RniRJ0uIMYFRZaZavTrP8LELgcugYs1oHfBj4bJrlO4wxH0lSSd5CUiWlWZ4A/wi8coLZbgS+lmb5YUkcPTzBfDWYG4FNPdJ8cxIFkTR6BjCqqo8x2eBl3nOAc4DGMuStPiRxdClw6XKXQ9J4GMCoctIsPxY4ts/D5oBbgTuBh4CtgbXA04B+bwv9VprlX0ji6NN9HidJGhEDGFVKMUX6/SWTPwqcB1wIfCOJo3SB860Cng68ATgZ2KPkud+VZvkFSRy5zIAkLQMH8apqXgXsUyLdd4FnJnF0UhJHX1koeAFI4mguiaPvJ3F0BrABaJYsx7OA15RMK0kaMQMYVc1RJdLcB7w6iaMf9HPiJI4eTOLozcAnSx5yTD/nlySNjreQVDXPK5GmmcTRrUPkcRLwcnrfTnpFmuWrRnAbacHj0yxfDRwJvBY4GHgqYdzOQ4SxPDcBlwAXJ3H0X0OWYbH8XwY8n7Ci8f7ATkUZtgUeAO4G7gKuAa4ALkvi6PZRl6XKrEdpPAxgVDV7l0hz5TAZJHH0cJrlfwH8nyWSPQjcTtii4LZh8gMe634hzfITgPcV5++2U/F4OvAK4M/TLL8AOC2JoxuHLAtplu8LnEYYF7RuiaTrise+hMbxbUBebJD4wSSOrhm2LMNIs/xE4O96JNuUxNHRJc51HvDmHsm2755ebz1K4+MtJFXNmhJpHh1BPp8B7iV8I/00cDphm4IXAXskcbQmiaODkjgaNniBsCcTAGmWr0mz/LOEaeILNXqL+XXg2jTLXzJoIdIs3ybN8jOB64ATWbrRW0wEvAm4Os3yM9Isn5YvSWX2xdpt/gfrURo/P5SqmhTYvkeaXxo2kySObmawP/yD+Bk8sTjf54HDBzzPGuBLaZa/Oomjy/s5MM3yXYGLgPqAeXdbRfj2/8I0y1+12CDqCnmgRJp1wE3WozQZ9sCoasp8Ez4hzfKtx16S0ZlvFM5h8EZv3jbAJ9IsX1s689DgXsLoGr1OLwbOm4J9pMps5rlT8a/1KE2AAYyq5r9LpNkP+EixZkwV3Jdm+UZ6j7Eoay/gvX2k/0vgoJJpHyOM/fkRkJc85hjgrX2UZyUqc1tyJ+tRmpyq/IGX5rVKpjsJuCTN8mePszAj8jBw5gKvp8ANxeORPs95Qprl2/VKlGb5L1OuUbqV0ICtTeLoyUkc7UnocTieMJOml3elWb5NiXQrVVYizS5Yj9LEGMCoai7qI+0RwH+kWf7FNMuPT7N89zGVaVjHArWO59cDbwR2TOJoQxJHGwjjK44mTLktYy1hQGgvp5VIcw9wWBJHF3TOskni6KEkjj5BmKLbq2Hei/63f1hJHi+R5hSsR2liHMTb5f47rh97Hmt322/seUyrJI6+m2b5ZYTgpIytCGtwHAnMpVn+beBy4BvAFUkc/Wg8Je3LAR0/Xwy8KYmjhzoTJHH0KLApzfJLCb1Qzyhx3iMIWyksKM3ybYHXlTjP/03i6JbF3kzi6Ntplp8D/H6P8xy5VHlWuDIBzIEdP1uP0pjZA6MqegcdU4/7sAp4NvB7hGnSP0yz/KY0y89Ps/zkNMufs8zjZjYDx3Q3ep2SOLqXcAugTIPaa9G/wwiDRXv5XIk055dIc8SMDALdjPUojZ09MKqcJI6uTbP8VOBDIzjd3sVjvlv8njTLvwp8kbAy6qR6aOaAk7oXQltIEkffSbP8IuD1PZLul2b5NsW3/oXcShg3sYawI/cOXT/vQJiy/t0S5d9MCCpXL5FmPWGcyF0lzldV1qM0IQYwqqQkjj5cTBt9P6FnZVTWARuLx1ya5S3g48D5Y14D4wtJHF3VR/rP0rvh24owQPMnC72ZxNH3gO/1keeikjjK0yy/DXhaj6S7Mt0NX7/1uAnrURqIt5BUWUkcfYBwP/6HY8piFaF7/lzCAmUnj3FF0rK7YM/7esl0O/ZbkCGUWext17GXYnn1W4/fKJlupz7POwzrUZVgAKNKS+Loy8AG4J3AHWPManfCOhtXpln+9DGc/yt9pr+VMP26l0kGMGXGJSVjL8XyGlc9ll7QbgSsR1WCt5BUecV4gzOK/V+OBn6TMCV0HOtVHEwIYo5I4ujaEZ3zxiSO7unngCSO5tIsvwPYp0fSka5IXKxwvLp4RB0/r2Y817tKrEdpggxgNDWSOMoIsyjOT7N8e+ClwMuLfw9kdGNldgY+n2b5IUkc/XgE5xt0Q8hFZ7kMI83ypxKu2fMIK7vuxs93LPZvxuIGrccy2xT0zXrUtPNDrKlUTGG9uHiQZvnOhPEsLwSeT/ijvsMQWewF/C3w2uFKCsB9Ax430kHFxTL4byMEfU6T7d+g9TiK3dOfYD1qVhjAaCYkcXQ38E/FY74L/SBCUPMK4CX03uW626+lWX5oEkdXDlm8kTZg/UqzfC/CBoS/upzlmALWozRBDuLVTEri6LEkjq5J4uisJI5eQ5hVcTTQzxRYCIviVVaa5RuAq7HRqzTrUbPIAEYCkjhKkzjalMTRoYR1OcoOxnxlhXa93kKa5U8CLiPMsOrHHGGq7d2EDQBvJ4z/KLPhoUbMetSs8haS1CWJo8+lWX4d8K/Ak3ok3xn4ZeA/xl2uMTgD2LNEunuAswl7SF0P3J7E0WPdidIs/xZhlpYmy3rUTDKAkRaQxNH1aZafAlxQIvmeVCyASbN8f6BRIum3gNckcbTgKrBdHDA6YdajZlklu76lCfkc5aYqrx93QcbgDfT+//8o8LqSjR6EabqaLOtRM8seGFVOmuW7AM8Anln8O/84Lomjy0aVT7EvzC3AAT2SbjeqPCfo1SXSfD6Jo1JrmxTjgHrdbtPoWY+aWQYwWvGKKc8fBp5FCFQW+4Z4HGEw4yiVWYp/LAuRjVmZ7RA293G+X8G/J8vBetTM8haSVrxioOEhhLValurePm6U+xSlWb4H5b6N3jyqPCchzfJVwC4lkvazt9SxAxZHA7IeNesMYFQVnyuRZjVwXprlo9rL5Xfp/X9kDvjOiPKblG0pt7dOqQ37ilt6x5XMe6R7+sw461EzzQBGVXEB8AtTPhfwQmBTmuVD7cKcZvn/AP6wRNJrkzi6a5i8Jq3Y/LLMWh+9xv7M+wvK9QQArCmZTj1Yj5p1BjCqhCSO2sDHSyY/CticZvkJaZav7iefNMv3TLP8Lwk9PmW+ZX6yn/OvIGWCro29erPSLD+VctN45+3dR1r1Zj1qZhnAqEreDTxSMu0+wMeAO9MsvyDN8nekWX5UmuUHp1m+f5rltTTLn5Vm+QvSLD82zfL3pFn+NeAm4GTKrYVxF3DuAL/HSvCtEmn2AM5eaKXhNMvXpFl+NvC/+8z38D7Ta2nWo2aWo81VGUkc/SjN8rcTApOydgTeWDxG7Q+SOBp0B+LldhnldtJ+C/DcNMs/CdxCuJ6HEK7nuq60NwH/TtiKYTFHpVl+dBJHF/ZdYi3EetTMMoBRpSRx9PFi9dFTl7koH03i6BPLXIZh/ANwOuV24D6oePRyEmGq+1IN31bAZ9Isv5kw/fxJwMFJHFVqJtcKYj1qZnkLSVV0GvABwgyg5fBx4HeWKe+RKAYef2SEpzw9iaN/Af6lZPq9CQsR7oJL1w/MetQsM4BR5SRxNJfE0R8BG4F7J5j1Q8DvJnH0liSOHp9gvuPyp8A3R3CevwP+BCCJo+8AV4zgnCrPetRMqswtpPvvuH65izAyk/pd1u6230TyWS5JHP1TmuX7Au8gDLxdO6asckJX/bunqYs8iaMszfKNwCbgsAFOkQN/lsTR6V2vn0xo/Ea1Ho+WYD1qVtkDo0pL4ujuJI7eRZh19HbgS4TN64Y1B1wDvBPYJ4mj46cpeJmXxNEdwBHAn9Ffb9aXgecv0OiRxNG/E6ayl9k88HHKre+jJViPmkU971muWb9hucYZbGGaemAmZaX0wDxw5/cnem88zfIdCAvaHVA89gd2B3YoHtsT1njJgIeBuwnLrd8I3EAIXK5K4ujOSZZ7uaVZvoYwK+WlwMGEXbZ3IgSEPwWuI3wjvzCJo/8qcb6EMBD0RcBTCJtepsW52oQpwK0kju4Z9e8yy6xHzQoDmCk2qwGMJGn6eQtJkiRVjgGMJEmqHAMYSZJUOQYwkiSpcgxgJElS5RjASJKkyjGAkSRJlWMAI0mSKscARpIkVY4BjCRJqhwDGEmSVDkGMJIkqXKi5S6AtJT6ex++crnLIGn6tP50u0OXuwwajj0wkiSpcgxgJElS5XgLSSua3bySpIXYAyNJkirHAEaSJFWOAYwkSaocAxhJklQ5BjCSJKlyKjMLae1u+00kn/vvuH7seUzqd5EkaVrZAyNJkirHAEaSJFWOAYwkSaocAxhJklQ5lRnEK02DWquxA/BAx0vXtOvN5036HJJUdQYwWvFqrcY+wI0dL/2kXW8+qccxFwNHdbz0xna9eeEYiidJWgYGMNIKVGs1zgF+p3i6ul1v5stZHklaaRwDI60wxS2i31juckjSSmYAI608xwJrlrsQkrSSeQtJM63WahwCnAS8CNgDWAXcBlwCnNmuN29c4thtgLcArwcOBHYGMuBW4FLgrHa9eUMfZfkUcMwCb/2s1moAXNuuNw9a4P3HiuP3Bk4DjgSeDPwU+Arwnna9+YMeeT8DeDvwUuApwDbAHcBVwLntevOLixw30DWotRo1oLNMZ7brzT+otRp/XJRjF+CUdr35N13HDVxfkqaLPTCaSbVWY+taq3EWoYE+AfglYHtgO2ADoRG9rtZqvH6R4/cGNgNnAy8HdgdWF+fYvzj+2lqrsXGsv0jwSK3VOBD4N0Ljvg8QExr43wKuLgKUBRVBw7eBtwEHEHp/YkIg8wbgn2utxmdqrUbSddww1+D+rudra63GicD/KsodA+s68hqqviRNHwMYzar3Aad0PP8BcAbwfqBdvJYAn6q1Gs/uPLDWaqwCNhEa6Xmt4vhPA3PFa9sCf19rNfYoWaZLgL8h9Hx0+tvi9c8sclwGNIHdgPuA7gG/6whBxi+otRqnEIKG+b8FPyvK8QXgno6kRwPndhw37DXIup7vCPzJgr9dMHB9SZpO3kLSzCmmZZ/a8dINwK+06837ivf/HPgW4Vv+auCDwCs70r8cOLjj+Wbgxe168/Hi+DbwR8V72wO/WZxjSe1681zg3FqrcRAhGJn39h6zkA4nBC2vA/6RcPvn3YTbSU+kqbUaT2nXm7fNv1BrNdYDH+hI8whweLvevLp4f1dCULKheP83aq3GWe16898Y/ho83vU7vIoQxPwV8FlCL9DNxbn2Ybj6kjSFDGBURbvXWo253skWdTywdcfzD803hgDtevO+WqvxQeCc4qWX1VqNPdv15g+L53cC7wB2KB5XzTfchS/w88YbwtiQcYqBP27XmxcVz9Naq/FOwriUDR3pnk0YLzLvzYQeknkfnQ9eANr15l21VuN0Qu/Pg4TF815AuFU16muwI8U4mAXeO57h6kvSFDKA0Syqdz2/doE0V3f8vFVxzAUA7XpzM6HHYQu1VmNrQkP7cNdbawcsZ1mP8fPGG4B2vTlXazUuYcsAZueu4w7vev6l7hO3680m4fZU9+ubGe01mAPOXOS9oepL0nQygNEs2qvreauY5bOUAzqf1FqNbYG3Em7bPJMQHGy9wHEQZsqM023tevPBBV6/vet59//3fbue39RPpiO+Bre1683u8s4bur4kTR8DGFXRfYTZNks5FXjOIu9tP0CenTNingxcBuw3wHnG4a5FXn+0x3Hda82kZTMcwzX46RLvDVVfkqaTAYyqKG3Xm59aKkGt1TiOxQOY7t6K9wA/7pHndR0/n82WDfflwHsJPRiPEHo2Wj3OtxI81PV8uz6OHfU1eGyJ94atL0lTyABGs+gWtpz+e3m73vxqmQNrrcYa4DUdL90P/Gq73kw70lTl9sXNbBmE7At8p9dBy3ANBq4vSdPLAEaz6Aq2nGZ7OFC2QdyDLcd53NXZcBfe1PV82PWWtuEX13YZha+z5XU4kjAN+wm1VuNlhBlFDxF6Qj5FWA9mktdgmPqSNKVcyE6zqMmW65CcUms1thjQWms1zqy1GvfWWo0baq3GFbVW42nFW90ryD61s7eh1mqcQBjY2mnPPsv3SNfzw/o8vqzzCAvXzTu+1mocOv+k6Gl5HyGA2hl4KmG9lUlcg07D1JekKWUPjGZOu968sdZqfAj4n8VLuwD/WWs1/hm4F3hu8YCwPsnV83vstOvNH9dajeuA+aX5I+CqWqtxJbA3YdryrYTejfkdpZ9TazX+mjDVt8zU3h8AL+l4vqnWalwObNeuN1/W56+7qHa9eVut1XgvIUiBsJLt12qtxqWEadAvBnbtOORy4MJiivbA16Bdb36sz3IOXF+SppcBjGbVaYTG7sTi+XaE5fK7XQD8dtdrv0+4rTL//2cN8Iri57uANxbnm2+8VxFmTR1AuQDmo4QNEuenHm9PGHOy1EDXQZ1OKP/8SrerCbeSun0ZOLpdb84vIDjMNegrgCkMU1+SppC3kDST2vVm3q4330roZfgkcCPh1s2DwPXA/wNe2a43j2nXm490Hftlwm7IFwN3E/b1uRH4CPDcdr15VbvevJzQkF5JGCx7DbDgjs4LlO1KYCPhds382JP/Bs4f4ldeLK+5dr35h4RtAT5KWKb/IcKU6psJY15e2643X9WuNx/oOG6s12CBcg5cX5KmU88Fttas3zDMku2Vc/8d1489j7W7rZTlQybjgTu/P+6F3CRJM8ZbSF1mLbiQJKmKvIUkSZIqxwBGkiRVjgGMJEmqHAMYSZJUOQYwkiSpcgxgJElS5TiNWr9g/UWHLvrenRuvnGBJJElamAvZ6QlLBS7d+glkXMhOkjRq3kIS0F/wMkh6SZJGyQBGAwcjBjGSpOViADPjhg1CDGIkScvBAGaGjSr4MIiRJE2aAYwkSaocA5gZNepeE3thJEmTZAAjSZIqxwBGkiRVjgGMJEmqnJ4BjKuoahh+fiRJ42APjCRJqhwDGEmSVDmlAhhvA0yfUe8qvdD5/NxIksbFHhhJklQ5pQMYv01Pn1H1wtj7IkmaNHtgZtywQcyob0VJklRGXwGM36qn06BByGLH+TmRJI1b3z0wNk7Tqd8gxuBFkrScBm5s1qzfMDfKgmjlWGpjxqUCHYMXSdKkDNXgGMRonsGLJGmShhrEa6Ml8HMgSZq8oWch2XjNNutfkrQcRtr4eEtpdhi4SJKW01gaIQOZ6WXgIklaCcbeGBnMVJ9BiyRJkiRJkiRJkiRJkiRJkiRJkiRJkiRJkjRW/x/D/Fb+IVMFYwAAAABJRU5ErkJggg=="
logo_col, title_col = st.columns([1, 11])
with logo_col:
    st.markdown(f'<img src="data:{_logo_mime};base64,{_logo_b64}" style="width:180px;margin-top:4px;" />', unsafe_allow_html=True)
with title_col:
    st.markdown(f"""
    <div class="mc-topbar">
        <div class="mc-title-wrap">
            <div class="mc-eyebrow">Shalina Healthcare &nbsp;·&nbsp; Distribution Intelligence Platform</div>
            <div class="mc-title">AI Distribution <span>Depth</span> Analysis System</div>
        </div>
        <div class="mc-status-group">
            <div class="mc-status-pill">
                <div class="mc-status-dot"></div>
                SYS: ONLINE
            </div>
            <div class="mc-status-pill">
                <div class="mc-status-dot {'amber' if data_status == 'csv' else ''}"></div>
                {sync_label}
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

#  DATA SOURCE BANNER 
is_live   = data_status == "live"
is_hybrid = data_status == "hybrid"

dot_color     = "#4CAF50" if is_live else ("#6EC6F5" if is_hybrid else "#F9A825")
dot_glow      = "rgba(76,175,80,0.6)"   if is_live else ("rgba(110,198,245,0.6)" if is_hybrid else "rgba(249,168,37,0.6)")
banner_bg     = "transparent"
banner_border = "rgba(255,255,255,0.06)"
status_label  = "Connected to Microsoft Fabric Warehouse" if is_live else (" Nigeria: CSV (33,588 outlets + YTD)   |    Angola: Live Fabric" if is_hybrid else "Connected to Local CSV — Both Countries")
status_sub    = "Live data — auto refreshes every hour"   if is_live else ("Hybrid mode — Nigeria uses full CSV data, Angola pulls live from Fabric" if is_hybrid else "Fabric unreachable — using CSV fallback for both countries")
icon          = "" if is_live else ("" if is_hybrid else "")

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

#  COUNTRY SWITCHER 
if "country" not in st.session_state:
    st.session_state.country = "Nigeria"

st.markdown("<div style='margin:12px 0 6px 0;font-family:Poppins,sans-serif;font-size:10px;font-weight:700;color:#90C8E8;text-transform:uppercase;letter-spacing:1.5px;'>Select Country</div>", unsafe_allow_html=True)
cc1, cc2, cc3 = st.columns([1, 1, 8])
with cc1:
    if st.button("Nigeria", use_container_width=True, key="btn_ng"):
        st.session_state.country = "Nigeria"
with cc2:
    if st.button("Angola", use_container_width=True, key="btn_ao"):
        st.session_state.country = "Angola"

country = st.session_state.country
df_country = df_all[df_all['country'] == country].copy()
p25, mean_val, p75 = get_stats(df_country)

# Country colour accent
accent = "#3B82F6" if country == "Nigeria" else "#8B5CF6"
st.markdown(f"<div style='height:2px;background:linear-gradient(90deg,{accent},transparent);margin-bottom:16px;'></div>", unsafe_allow_html=True)

#  NAVBAR 
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

import streamlit.components.v1 as _fx_c
_fx_c.html("""<script>
(function() {
    const doc = window.parent.document;

    //  INJECT GLOBAL STYLES 
    function injectStyles() {
        if (doc.getElementById('shalina-fx-styles')) return;
        const style = doc.createElement('style');
        style.id = 'shalina-fx-styles';
        style.textContent = `
            /*  GRAIN TEXTURE OVERLAY  */
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

            /*  FLOATING GRADIENT ORBS  */
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

            /*  MESH ANIMATED GRADIENT on main bg  */
            @keyframes meshShift {
                0%   { background-position: 0% 50%; }
                50%  { background-position: 100% 50%; }
                100% { background-position: 0% 50%; }
            }

            /*  TILT 3D CARDS  */
            .kpi-card {
                transform-style: preserve-3d;
                will-change: transform;
                transition: transform 0.15s ease, box-shadow 0.15s ease !important;
            }

            /*  SPOTLIGHT ON CARDS  */
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

            /*  REVEAL ON SCROLL  */
            .shalina-reveal {
                opacity: 0;
                transform: translateY(48px) scale(0.97);
                transition: opacity 0.75s cubic-bezier(.16,1,.3,1),
                            transform 0.75s cubic-bezier(.16,1,.3,1);
                will-change: opacity, transform;
            }
            .shalina-reveal.visible {
                opacity: 1;
                transform: translateY(0) scale(1);
            }
            /* stagger siblings */
            .shalina-reveal:nth-child(2) { transition-delay: 0.08s; }
            .shalina-reveal:nth-child(3) { transition-delay: 0.16s; }
            .shalina-reveal:nth-child(4) { transition-delay: 0.24s; }

            /*  ELASTIC BUTTON  */

            /*  GLASSMORPHISM PANELS  */
            .ds-banner, .insight-card {
                backdrop-filter: blur(24px) saturate(1.4) !important;
                -webkit-backdrop-filter: blur(24px) saturate(1.4) !important;
            }

            /*  ANIMATED GRADIENT BORDER on hover  */
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

            /*  MAGNETIC BUTTON glow  */
            [data-testid="stHorizontalBlock"] button:hover {
                box-shadow: 0 0 24px rgba(33,150,220,0.55), 0 0 8px rgba(110,198,245,0.4), inset 0 0 20px rgba(33,150,220,0.2) !important;
            }

            /*  PARTICLE CANVAS  */
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

    //  FLOATING ORBS 
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

    //  PARTICLE BACKGROUND 
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

    //  3D TILT + SPOTLIGHT on KPI cards 
    function addTiltCards() {
        // Subtle lift + spotlight only — no 3D rotation
        const cards = doc.querySelectorAll('.kpi-card');
        cards.forEach(card => {
            if (card.dataset.tiltDone) return;
            card.dataset.tiltDone = '1';

            const spot = doc.createElement('div');
            spot.className = 'spotlight';
            card.appendChild(spot);

            card.addEventListener('mousemove', e => {
                const rect = card.getBoundingClientRect();
                spot.style.left = (e.clientX - rect.left) + 'px';
                spot.style.top  = (e.clientY - rect.top)  + 'px';
            });
            card.addEventListener('mouseenter', () => {
                card.style.transform = 'translateY(-4px) scale(1.015)';
                card.style.boxShadow = '0 16px 40px rgba(0,0,0,0.45), 0 0 24px rgba(33,150,220,0.2)';
                card.style.transition = 'transform 0.2s ease, box-shadow 0.2s ease';
            });
            card.addEventListener('mouseleave', () => {
                card.style.transform = 'translateY(0) scale(1)';
                card.style.boxShadow = '';
            });
        });
    }

    //  REVEAL ON SCROLL 
    function addRevealOnScroll() {
        // Wider target list — catches charts, tables, cards, metric blocks
        const targets = doc.querySelectorAll(
            '.kpi-card, .insight-card, .ds-banner, ' +
            '[data-testid="stPlotlyChart"], [data-testid="stDataFrame"], ' +
            '[data-testid="stMetric"], [data-testid="stMarkdown"] .header-wrap, ' +
            '[data-testid="stVerticalBlock"] > div > div > div > div'
        );
        targets.forEach(el => {
            if (el.dataset.revealDone) return;
            // Skip tiny or already-visible elements
            const rect = el.getBoundingClientRect();
            if (rect.height < 40) return;
            el.dataset.revealDone = '1';
            el.classList.add('shalina-reveal');
        });

        if (!window._shalinaRevealObserver) {
            window._shalinaRevealObserver = new IntersectionObserver(entries => {
                entries.forEach((e, i) => {
                    if (e.isIntersecting) {
                        // Stagger each element by 80ms based on its position
                        const delay = Math.min(i * 80, 400);
                        setTimeout(() => e.target.classList.add('visible'), delay);
                        window._shalinaRevealObserver.unobserve(e.target);
                    }
                });
            }, { threshold: 0.08, rootMargin: '0px 0px -40px 0px' });
        }

        doc.querySelectorAll('.shalina-reveal:not(.visible)').forEach(el => {
            window._shalinaRevealObserver.observe(el);
        });
    }

    //  MOUSE POSITION REACTIVE GRADIENT 
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

    //  MAGNETIC BUTTONS 
    function addMagneticButtons() {
        // Only style the top navbar buttons (country switcher + nav row)
        // No magnetic movement — just glow on hover via CSS
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
            btn.style.transition = 'box-shadow 0.2s ease, border-color 0.2s ease';
            btn.addEventListener('mouseenter', () => {
                btn.style.borderColor = 'rgba(110,198,245,0.8)';
                btn.style.boxShadow = '0 0 20px rgba(33,150,220,0.5), inset 0 0 16px rgba(33,150,220,0.15)';
            });
            btn.addEventListener('mouseleave', () => {
                btn.style.borderColor = 'rgba(33,150,196,0.25)';
                btn.style.boxShadow = '';
            });
        });
    }

    //  NAVBAR HIDE 
    function hideNav() {
        const nav = doc.querySelector('[data-testid="stSidebarNav"]');
        if (nav) nav.remove();
    }

    function hideImageButtons() {
        // Remove the fullscreen expand button that appears on images
        doc.querySelectorAll('[data-testid="StyledFullScreenButton"]').forEach(b => b.remove());
        doc.querySelectorAll('[data-testid="stImageContainer"] button').forEach(b => b.remove());
        // Also catch by class pattern
        doc.querySelectorAll('button[title="View fullscreen"]').forEach(b => b.remove());
        doc.querySelectorAll('button[title="Fullscreen"]').forEach(b => b.remove());
    }

    //  PERSISTENT RE-INJECTION 
    // Streamlit wipes the DOM on every navigation — we poll every 800ms
    // to re-inject anything that got removed, and re-apply interactive effects.

    function fullInit() {
        try { injectStyles(); }    catch(e) {}
        try { addOrbs(); }         catch(e) {}
        try { addParticles(); }    catch(e) {}
        try { addMouseGradient(); } catch(e) {}
        try { addMagneticButtons(); } catch(e) {}
        try { addTiltCards(); }    catch(e) {}
        try { addRevealOnScroll(); } catch(e) {}
        try { hideNav(); }         catch(e) {}
        try { hideImageButtons(); } catch(e) {}
    }

    function lightRefresh() {
        // Only re-apply interactive effects to newly rendered elements
        // (particles/orbs persist on body so no need to re-add)
        try { addMagneticButtons(); } catch(e) {}
        try { addTiltCards(); }       catch(e) {}
        try { addRevealOnScroll(); }  catch(e) {}
        try { hideNav(); }            catch(e) {}
        try { hideImageButtons(); }   catch(e) {}

        // If canvas got removed (Streamlit full re-render), rebuild it
        if (!doc.getElementById('shalina-particles')) {
            try { addParticles(); } catch(e) {}
        }
        if (!doc.getElementById('shalina-orb-1')) {
            try { addOrbs(); } catch(e) {}
        }
        if (!doc.getElementById('mouse-gradient')) {
            try { addMouseGradient(); } catch(e) {}
        }
        if (!doc.getElementById('shalina-fx-styles')) {
            try { injectStyles(); } catch(e) {}
        }
    }

    // Initial load
    setTimeout(fullInit, 300);
    setTimeout(fullInit, 800);

    // Continuous polling — catches every Streamlit re-render
    setInterval(lightRefresh, 800);

})();
</script>
""", height=0)

#  FILTERS 
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
    st.markdown('<div style="background:rgba(200,50,50,0.15);border:1px solid rgba(255,100,100,0.4);border-radius:10px;padding:14px 16px;font-size:13px;color:#FFAAAA;font-weight:600;margin:16px 0;"> No outlets match the selected filters.</div>', unsafe_allow_html=True)
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
    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(255,255,255,0.02)",
    font=dict(color="#64748B", size=11), height=380,
    xaxis=dict(gridcolor="rgba(255,255,255,0.04)", linecolor="rgba(255,255,255,0.06)", color="#64748B"),
    yaxis=dict(gridcolor="rgba(255,255,255,0.04)", linecolor="rgba(255,255,255,0.06)", color="#64748B"),
    margin=dict(l=0, r=0, t=20, b=0),
    legend=dict(font=dict(color="#94A3B8"), bgcolor="rgba(8,13,26,0.8)", bordercolor="rgba(255,255,255,0.08)", borderwidth=1)
)

map_center = {"lat": 9.0, "lon": 8.0} if country == "Nigeria" else {"lat": -11.0, "lon": 17.5}
map_zoom   = 5 if country == "Nigeria" else 4

# 
# DASHBOARD
# 
if page == "Dashboard":
    total_outlets   = len(df)
    dead_outlets    = len(df[df['Opportunity'] == 'Dead Whitespace'])
    high_performers = len(df[df['Opportunity'] == 'High Performer'])
    total_ytd       = df['YTD Retailing Value'].sum()
    ws_pct          = round(dead_outlets / total_outlets * 100, 1)

    st.markdown(f"""
    <div class="kpi-row">
        <div class="kpi-card mc-blue">
            <div class="kpi-accent-line" style="background:linear-gradient(90deg,#3B82F6,#60A5FA);"></div>
            <div class="kpi-label">Total Outlets — {country}</div>
            <div class="kpi-value">{total_outlets:,}</div>
            <div class="kpi-delta">Distribution network</div>
        </div>
        <div class="kpi-card mc-red">
            <div class="kpi-accent-line" style="background:linear-gradient(90deg,#EF4444,#F87171);"></div>
            <div class="kpi-label">Dead Whitespace</div>
            <div class="kpi-value">{dead_outlets:,}</div>
            <div class="kpi-delta">{ws_pct}% of total — zero YTD sales</div>
        </div>
        <div class="kpi-card mc-purple">
            <div class="kpi-accent-line" style="background:linear-gradient(90deg,#8B5CF6,#A78BFA);"></div>
            <div class="kpi-label">High Performers</div>
            <div class="kpi-value">{high_performers:,}</div>
            <div class="kpi-delta">Above ₦{p75:,.0f}K YTD</div>
        </div>
        <div class="kpi-card mc-amber">
            <div class="kpi-accent-line" style="background:linear-gradient(90deg,#F59E0B,#FCD34D);"></div>
            <div class="kpi-label">Total YTD Revenue</div>
            <div class="kpi-value">₦{total_ytd/1000:,.0f}M</div>
            <div class="kpi-delta">Across all active outlets</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-title">Geographic Outlet Distribution</div>', unsafe_allow_html=True)
    map_df = df.sample(min(5000, len(df)), random_state=42) if len(df) > 5000 else df
    fig_map = px.scatter_mapbox(map_df, lat="latitude", lon="longitude",
        color="Opportunity", color_discrete_map=color_map,
        size="YTD Retailing Value" if map_df["YTD Retailing Value"].sum() > 0 else None,
        size_max=14, zoom=map_zoom, height=520,
        hover_name="Shop Name",
        hover_data={"YTD Retailing Value":":,.1f","Retailer Subtype":True,"latitude":False,"longitude":False},
        center=map_center)
    fig_map.update_traces(marker=dict(opacity=0.85))
    fig_map.update_layout(
        mapbox_style="carto-darkmatter",
        paper_bgcolor="rgba(0,0,0,0)",
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

# 
# OUTLET PERFORMANCE
# 
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

# 
# WHITESPACE DETECTION
# 
elif page == "Whitespace Detection":
    dead  = df[df['Opportunity'] == 'Dead Whitespace']
    under = df[df['Opportunity'] == 'Underperforming']
    total_ws = len(dead) + len(under)
    revenue_potential = total_ws * mean_val

    st.markdown(f"""
    <div class="kpi-row">
        <div class="kpi-card mc-red">
            <div class="kpi-accent-line" style="background:linear-gradient(90deg,#EF4444,#F87171);"></div>
            <div class="kpi-label">Dead Whitespace Outlets</div>
            <div class="kpi-value">{len(dead):,}</div>
            <div class="kpi-delta">Zero YTD sales — highest priority</div>
        </div>
        <div class="kpi-card mc-orange">
            <div class="kpi-accent-line" style="background:linear-gradient(90deg,#F97316,#FB923C);"></div>
            <div class="kpi-label">Underperforming Outlets</div>
            <div class="kpi-value">{len(under):,}</div>
            <div class="kpi-delta">Below ₦{p25:,.0f}K YTD</div>
        </div>
        <div class="kpi-card mc-blue">
            <div class="kpi-accent-line" style="background:linear-gradient(90deg,#3B82F6,#60A5FA);"></div>
            <div class="kpi-label">Total Whitespace</div>
            <div class="kpi-value">{total_ws:,}</div>
            <div class="kpi-delta">{round(total_ws/len(df)*100,1)}% of filtered outlets</div>
        </div>
        <div class="kpi-card mc-green">
            <div class="kpi-accent-line" style="background:linear-gradient(90deg,#22C55E,#4ADE80);"></div>
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
    st.download_button(" Export Dead Whitespace List", csv, f"dead_whitespace_{country.lower()}.csv", "text/csv")

# 
# EXPANSION STRATEGY
# 
elif page == "Expansion Strategy":
    dead   = df[df['Opportunity'] == 'Dead Whitespace']
    under  = df[df['Opportunity'] == 'Underperforming']
    active = df[df['Opportunity'].isin(['Active','High Performer'])]
    pri_dead = dead[dead['Retailer Subtype'].str.contains('Primary', case=False, na=False)]
    sec_dead = dead[~dead['Retailer Subtype'].str.contains('Primary', case=False, na=False)]

    st.markdown(f"""
    <div class="insight-card">
        <span class="badge badge-dead"> Critical Priority</span>
        <div class="insight-title">Activate {len(pri_dead):,} Dead Primary Outlets</div>
        <div class="insight-detail">Primary outlets with zero YTD sales need immediate sales team intervention.
        Revenue potential: <strong style="color:#FFFFFF">₦{len(pri_dead)*mean_val/1000:,.0f}M</strong></div>
    </div>
    <div class="insight-card">
        <span class="badge badge-under"> High Priority</span>
        <div class="insight-title">Convert {len(sec_dead):,} Dead Secondary Outlets</div>
        <div class="insight-detail">Secondary outlets with zero sales — largest untapped pool.
        Revenue potential: <strong style="color:#FFFFFF">₦{len(sec_dead)*mean_val/1000:,.0f}M</strong></div>
    </div>
    <div class="insight-card">
        <span class="badge badge-low"> Medium Priority</span>
        <div class="insight-title">Scale Up {len(under):,} Underperforming Outlets</div>
        <div class="insight-detail">Outlets selling below ₦{p25:,.0f}K YTD. Incremental revenue potential:
        <strong style="color:#FFFFFF">₦{len(under)*(mean_val-p25)/1000:,.0f}M</strong></div>
    </div>
    <div class="insight-card">
        <span class="badge badge-high"> Growth</span>
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