"""
Shalina Distribution Intelligence — Shared Design System
Inject into every page with: from styles import apply_styles; apply_styles()
"""
import streamlit as st
import streamlit.components.v1 as _stc

_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;600&display=swap');

/* ─────────────────────────────────────────────────────────
   BASE RESET
───────────────────────────────────────────────────────── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

/* ─────────────────────────────────────────────────────────
   APP SHELL — pure black canvas
───────────────────────────────────────────────────────── */
.stApp, body, html {
    background: #060606 !important;
    font-family: 'Inter', -apple-system, sans-serif !important;
    color: #ffffff !important;
}
.stApp::before { display: none !important; }

/* main content area */
.main .block-container {
    background: transparent !important;
    padding: 0 2rem 4rem 2rem !important;
    max-width: 1440px !important;
    position: relative;
    z-index: 1;
}

/* ─────────────────────────────────────────────────────────
   KILL ALL STREAMLIT CHROME
───────────────────────────────────────────────────────── */
[data-testid="stDecoration"],
[data-testid="stStatusWidget"],
#MainMenu, footer,
[data-testid="stSidebarNav"],
[data-testid="stSidebarNavItems"],
section[data-testid="stSidebar"] nav,
[data-testid="stImageContainer"] button,
[data-testid="StyledFullScreenButton"],
button[title="View fullscreen"],
button[title="Fullscreen"] {
    display: none !important;
}
header[data-testid="stHeader"] {
    background: transparent !important;
    border: none !important;
}
[data-testid="stToolbar"] {
    display: flex !important;
    background: transparent !important;
}

/* ─────────────────────────────────────────────────────────
   SIDEBAR
───────────────────────────────────────────────────────── */
section[data-testid="stSidebar"] {
    background: #030303 !important;
    border-right: 1px solid rgba(255,255,255,0.05) !important;
    min-width: 220px !important;
}
section[data-testid="stSidebar"] > div:first-child {
    padding-top: 24px !important;
}
section[data-testid="stSidebar"] * {
    color: #666 !important;
    font-family: 'Inter', sans-serif !important;
}
section[data-testid="stSidebar"] a[data-testid="stPageLink"] {
    border-radius: 100px !important;
    padding: 8px 14px !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    transition: background 0.15s, color 0.15s !important;
    display: block !important;
    margin-bottom: 2px !important;
}
section[data-testid="stSidebar"] a[data-testid="stPageLink"]:hover {
    background: rgba(255,255,255,0.05) !important;
    color: #fff !important;
}

/* Sidebar toggle buttons */
[data-testid="collapsedControl"],
[data-testid="stSidebarCollapseButton"],
[data-testid="stExpandSidebarButton"],
button[kind="header"] {
    display: flex !important;
    visibility: visible !important;
    opacity: 1 !important;
    z-index: 999999 !important;
}
[data-testid="stSidebarCollapseButton"] *,
[data-testid="collapsedControl"] *,
[data-testid="stExpandSidebarButton"] * { font-size: 0 !important; }
[data-testid="stSidebarCollapseButton"]::before { content:"‹"; color:#444; font-size:22px; line-height:1; }
[data-testid="collapsedControl"]::before,
[data-testid="stExpandSidebarButton"]::before { content:"›"; color:#444; font-size:22px; line-height:1; }
[data-testid="stExpandSidebarButton"] {
    position: fixed !important;
    top: 14px !important;
    left: 14px !important;
    width: 32px !important;
    height: 32px !important;
    background: #0f0f0f !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 100px !important;
    align-items: center !important;
    justify-content: center !important;
}

/* ─────────────────────────────────────────────────────────
   BUTTONS — full pill, clean dark
───────────────────────────────────────────────────────── */
.stButton > button {
    background: #111 !important;
    color: #888 !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 100px !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 600 !important;
    font-size: 12px !important;
    letter-spacing: 0.3px !important;
    padding: 8px 18px !important;
    transition: all 0.15s ease !important;
    box-shadow: none !important;
    outline: none !important;
}
.stButton > button:hover {
    background: #1a1a1a !important;
    color: #fff !important;
    border-color: rgba(255,255,255,0.18) !important;
}
.stButton > button:active {
    background: #222 !important;
    border-color: rgba(255,255,255,0.28) !important;
}
/* Download button variant */
.stDownloadButton > button {
    background: #111 !important;
    color: #666 !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 100px !important;
    font-weight: 600 !important;
}
.stDownloadButton > button:hover {
    background: #1c1c1c !important;
    color: #fff !important;
}

/* ─────────────────────────────────────────────────────────
   INPUTS & SELECTS
───────────────────────────────────────────────────────── */
input, .stTextInput input {
    background: #0f0f0f !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 100px !important;
    color: #fff !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 13px !important;
    padding: 8px 16px !important;
    box-shadow: none !important;
    outline: none !important;
    transition: border-color 0.15s !important;
}
input:focus, .stTextInput input:focus {
    border-color: rgba(255,255,255,0.22) !important;
    box-shadow: none !important;
    outline: none !important;
}
input::placeholder, .stTextInput input::placeholder { color: #333 !important; }

.stTextInput > div, .stTextInput > div > div { background: transparent !important; }
.stTextInput label { display: none !important; }

[data-baseweb="select"] > div {
    background: #0f0f0f !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 100px !important;
    color: #fff !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 13px !important;
    box-shadow: none !important;
    transition: border-color 0.15s !important;
}
[data-baseweb="select"] > div:hover { border-color: rgba(255,255,255,0.16) !important; }
[data-baseweb="select"] svg { fill: #444 !important; }
[data-baseweb="popover"] {
    background: #0f0f0f !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 14px !important;
    box-shadow: 0 20px 60px rgba(0,0,0,0.8) !important;
}
[role="option"] {
    background: transparent !important;
    color: #888 !important;
    font-size: 13px !important;
    border-radius: 8px !important;
    margin: 2px 6px !important;
}
[role="option"]:hover, [aria-selected="true"] {
    background: rgba(255,255,255,0.06) !important;
    color: #fff !important;
}
.stSelectbox label {
    color: #333 !important;
    font-size: 9px !important;
    font-weight: 700 !important;
    text-transform: uppercase !important;
    letter-spacing: 2.5px !important;
    margin-bottom: 6px !important;
    display: block !important;
}

/* ─────────────────────────────────────────────────────────
   DATA TABLE
───────────────────────────────────────────────────────── */
[data-testid="stDataFrame"] {
    border: 1px solid rgba(255,255,255,0.06) !important;
    border-radius: 14px !important;
    overflow: hidden !important;
}
[data-testid="stDataFrame"] th {
    background: #0a0a0a !important;
    color: #444 !important;
    font-size: 10px !important;
    font-weight: 700 !important;
    text-transform: uppercase !important;
    letter-spacing: 1.5px !important;
}
[data-testid="stDataFrame"] td {
    font-size: 12px !important;
    color: #ccc !important;
    border-color: rgba(255,255,255,0.04) !important;
}

/* ─────────────────────────────────────────────────────────
   DESIGN COMPONENT CLASSES
───────────────────────────────────────────────────────── */

/* — Top bar — */
.sh-topbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 20px 0 18px 0;
    border-bottom: 1px solid rgba(255,255,255,0.05);
    margin-bottom: 24px;
}
.sh-eyebrow {
    font-size: 9px;
    font-weight: 600;
    letter-spacing: 3.5px;
    text-transform: uppercase;
    color: #2e2e2e;
    margin-bottom: 8px;
}
.sh-title {
    font-size: 32px;
    font-weight: 900;
    color: #ffffff;
    letter-spacing: -1.5px;
    line-height: 1.0;
}
.sh-title-dim { color: rgba(255,255,255,0.22); }
.sh-pill-group { display: flex; gap: 8px; align-items: center; }
.sh-pill {
    display: flex;
    align-items: center;
    gap: 7px;
    background: #0f0f0f;
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 100px;
    padding: 6px 14px;
    font-size: 9px;
    font-weight: 700;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: #444;
}
.sh-dot {
    width: 6px; height: 6px; border-radius: 50%;
    background: #22C55E;
    box-shadow: 0 0 6px rgba(34,197,94,0.9), 0 0 12px rgba(34,197,94,0.4);
    animation: sh-pulse 2.2s ease-in-out infinite;
    flex-shrink: 0;
}
.sh-dot-amber { background: #F59E0B; box-shadow: 0 0 6px rgba(245,158,11,0.9), 0 0 12px rgba(245,158,11,0.4); }
@keyframes sh-pulse { 0%,100%{opacity:1;} 50%{opacity:0.3;} }

/* — KPI Row — */
.sh-kpi-row {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 12px;
    margin-bottom: 28px;
}
.sh-kpi {
    background: #0a0a0a;
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 18px;
    padding: 28px 24px 22px 24px;
    position: relative;
    overflow: hidden;
    cursor: default;
    transition: transform 0.2s cubic-bezier(.16,1,.3,1), border-color 0.2s;
}
.sh-kpi:hover { transform: translateY(-3px); border-color: rgba(255,255,255,0.12); }
.sh-kpi-accent {
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 1px;
}
.sh-kpi-label {
    font-size: 9px;
    font-weight: 700;
    letter-spacing: 2.5px;
    text-transform: uppercase;
    color: #2d2d2d;
    margin-bottom: 10px;
}
.sh-kpi-value {
    font-size: 56px;
    font-weight: 900;
    color: #ffffff;
    line-height: 1;
    letter-spacing: -3px;
    margin-bottom: 8px;
}
.sh-kpi-delta {
    font-size: 11px;
    color: #333;
    font-weight: 500;
}

/* — Section heading — */
.sh-section {
    font-size: 9px;
    font-weight: 700;
    letter-spacing: 3.5px;
    text-transform: uppercase;
    color: #2a2a2a;
    margin-top: 32px;
    margin-bottom: 16px;
    display: flex;
    align-items: center;
    gap: 14px;
}
.sh-section::after {
    content: '';
    flex: 1;
    height: 1px;
    background: rgba(255,255,255,0.04);
}

/* — Card — */
.sh-card {
    background: #0a0a0a;
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 16px;
    padding: 20px 22px;
    transition: border-color 0.15s, background 0.15s;
}
.sh-card:hover { background: #0e0e0e; border-color: rgba(255,255,255,0.10); }

/* — Outlet detail — */
.sh-odc {
    background: #0a0a0a;
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 18px;
    padding: 26px 28px 22px 28px;
    margin-bottom: 24px;
}
.sh-odc-tag {
    font-size: 9px;
    font-weight: 700;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: #2563eb;
    margin-bottom: 8px;
}
.sh-odc-name {
    font-size: 26px;
    font-weight: 900;
    color: #fff;
    letter-spacing: -0.8px;
    line-height: 1.05;
    margin-bottom: 12px;
}
.sh-odc-meta {
    display: flex;
    gap: 8px;
    align-items: center;
    flex-wrap: wrap;
    padding-bottom: 18px;
    margin-bottom: 18px;
    border-bottom: 1px solid rgba(255,255,255,0.05);
}
.sh-odc-stats { display: flex; align-items: stretch; gap: 0; }
.sh-odc-stat { flex: 1; padding: 0 22px; }
.sh-odc-stat:first-child { padding-left: 0; }
.sh-odc-divider { width: 1px; background: rgba(255,255,255,0.05); flex-shrink: 0; }
.sh-odc-stat-label { font-size: 9px; font-weight: 700; letter-spacing: 2px; text-transform: uppercase; color: #2d2d2d; margin-bottom: 8px; }
.sh-odc-stat-value { font-size: 26px; font-weight: 900; letter-spacing: -0.8px; line-height: 1; }

/* — Banner (data source) — */
.sh-banner {
    background: #0a0a0a;
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 14px;
    padding: 14px 20px;
    margin-bottom: 18px;
    display: flex;
    align-items: center;
    gap: 14px;
}

/* — Badge pill — */
.sh-badge {
    display: inline-block;
    padding: 3px 12px;
    border-radius: 100px;
    font-size: 9px;
    font-weight: 700;
    letter-spacing: 0.8px;
    text-transform: uppercase;
}
.sh-badge-red    { background: rgba(220,38,38,0.10);  color: #fca5a5; border: 1px solid rgba(220,38,38,0.20); }
.sh-badge-orange { background: rgba(234,88,12,0.10);  color: #fdba74; border: 1px solid rgba(234,88,12,0.20); }
.sh-badge-blue   { background: rgba(37,99,235,0.10);  color: #93c5fd; border: 1px solid rgba(37,99,235,0.20); }
.sh-badge-purple { background: rgba(124,58,237,0.10); color: #c4b5fd; border: 1px solid rgba(124,58,237,0.20); }
.sh-badge-green  { background: rgba(22,163,74,0.10);  color: #86efac; border: 1px solid rgba(22,163,74,0.20); }
.sh-badge-amber  { background: rgba(217,119,6,0.10);  color: #fcd34d; border: 1px solid rgba(217,119,6,0.20); }

/* — Country switcher label — */
.sh-country-label {
    font-size: 9px;
    font-weight: 700;
    letter-spacing: 3.5px;
    text-transform: uppercase;
    color: #2a2a2a;
    margin: 16px 0 8px 0;
}

/* — Nav container — */
.sh-nav-wrap {
    display: flex;
    gap: 6px;
    background: #0a0a0a;
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 100px;
    padding: 5px;
    margin-bottom: 6px;
    width: fit-content;
}

/* — Insight card — */
.sh-insight {
    background: #0a0a0a;
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 14px;
    padding: 18px 20px;
    margin-bottom: 10px;
    transition: border-color 0.15s;
}
.sh-insight:hover { border-color: rgba(255,255,255,0.10); }
.sh-insight-title { font-size: 14px; font-weight: 700; color: #fff; margin-bottom: 5px; }
.sh-insight-body  { font-size: 12px; color: #3a3a3a; line-height: 1.7; }

/* — Scroll reveal — */
.sh-reveal { opacity:0; transform:translateY(32px); transition:opacity 0.65s cubic-bezier(.16,1,.3,1),transform 0.65s cubic-bezier(.16,1,.3,1); }
.sh-reveal.visible { opacity:1; transform:translateY(0); }

/* — Error / warning box — */
.sh-error { background:#0f0505; border:1px solid rgba(220,38,38,0.25); border-radius:14px; padding:16px 20px; color:#fca5a5; font-weight:600; font-size:13px; }
.sh-warn  { background:#0f0a00; border:1px solid rgba(217,119,6,0.25); border-radius:14px; padding:16px 20px; color:#fcd34d; font-weight:600; font-size:13px; }

/* — Page title (sub-pages) — */
.sh-page-title {
    font-size: 28px;
    font-weight: 900;
    color: #fff;
    letter-spacing: -1px;
    line-height: 1.05;
    margin-bottom: 4px;
}
.sh-page-sub {
    font-size: 12px;
    color: #2a2a2a;
    margin-bottom: 24px;
}

/* ─────────────────────────────────────────────────────────
   PLOTLY CHART CLEANUP
───────────────────────────────────────────────────────── */
.js-plotly-plot .plotly .modebar {
    background: transparent !important;
}
.js-plotly-plot .plotly .modebar-btn path { fill: #333 !important; }

/* ─────────────────────────────────────────────────────────
   METRIC WIDGET
───────────────────────────────────────────────────────── */
[data-testid="stMetric"] {
    background: #0a0a0a !important;
    border: 1px solid rgba(255,255,255,0.06) !important;
    border-radius: 16px !important;
    padding: 20px !important;
}
[data-testid="stMetricLabel"] { color: #2d2d2d !important; font-size: 9px !important; font-weight: 700 !important; letter-spacing: 2.5px !important; text-transform: uppercase !important; }
[data-testid="stMetricValue"] { color: #fff !important; font-size: 36px !important; font-weight: 900 !important; letter-spacing: -1px !important; }
[data-testid="stMetricDelta"] { color: #444 !important; font-size: 11px !important; }

/* ─────────────────────────────────────────────────────────
   SIDEBAR LABEL OVERRIDES (nav section labels)
───────────────────────────────────────────────────────── */
.sh-sidebar-label {
    font-size: 9px !important;
    font-weight: 700 !important;
    letter-spacing: 3px !important;
    text-transform: uppercase !important;
    color: #1e1e1e !important;
    padding: 0 8px !important;
    margin-bottom: 8px !important;
    margin-top: 22px !important;
    display: block;
}
.sh-sidebar-divider {
    height: 1px;
    background: rgba(255,255,255,0.04);
    margin: 18px 0;
}

/* Tabs (if used) */
.stTabs [data-baseweb="tab-list"] {
    background: #0a0a0a !important;
    border-radius: 100px !important;
    border: 1px solid rgba(255,255,255,0.06) !important;
    padding: 4px !important;
    gap: 4px !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    border-radius: 100px !important;
    color: #555 !important;
    font-size: 12px !important;
    font-weight: 600 !important;
    border: none !important;
    padding: 6px 16px !important;
}
.stTabs [aria-selected="true"] {
    background: #1a1a1a !important;
    color: #fff !important;
}
.stTabs [data-baseweb="tab-border"] { display: none !important; }
.stTabs [data-baseweb="tab-highlight"] { display: none !important; }

/* Expander */
[data-testid="stExpander"] {
    background: #0a0a0a !important;
    border: 1px solid rgba(255,255,255,0.06) !important;
    border-radius: 14px !important;
}
[data-testid="stExpander"] summary { color: #888 !important; font-size: 13px !important; }

/* Slider */
[data-testid="stSlider"] [data-baseweb="slider"] [data-testid="stSliderThumb"] {
    background: #fff !important;
}
[data-testid="stSlider"] [data-baseweb="slider"] div[data-baseweb="slider-inner-thumb"] {
    background: #fff !important;
}

/* Checkbox / Radio */
input[type="checkbox"] + div, input[type="radio"] + div { color: #888 !important; font-size: 13px !important; }

/* Progress / spinner */
[data-testid="stSpinner"] { color: #333 !important; }
</style>
"""

_JS = """<script>
(function(){
    const doc = window.parent.document;

    /* ── Nav active state highlight ── */
    const NAV_LABELS = ['Dashboard','Outlet Performance','Whitespace Detection','Expansion Strategy'];

    function highlightActiveNav(){
        const marker = doc.getElementById('sh-active-page');
        if(!marker) return;
        const active = marker.getAttribute('data-page');
        doc.querySelectorAll('button').forEach(btn=>{
            const txt = btn.textContent.trim();
            if(!NAV_LABELS.includes(txt)) return;
            const isActive = (txt === active);
            if(isActive){
                btn.style.setProperty('background','#ffffff','important');
                btn.style.setProperty('color','#000000','important');
                btn.style.setProperty('border-color','rgba(255,255,255,0.0)','important');
                btn.style.setProperty('font-weight','700','important');
            } else {
                btn.style.setProperty('background','transparent','important');
                btn.style.setProperty('color','#555','important');
                btn.style.setProperty('border-color','transparent','important');
                btn.style.setProperty('font-weight','500','important');
            }
        });
    }

    /* ── Country button styling ── */
    function styleCountryBtns(){
        doc.querySelectorAll('button').forEach(btn=>{
            const txt = btn.textContent.trim();
            if(txt !== 'Nigeria' && txt !== 'Angola') return;
            if(btn.dataset.csBtndone) return;
            btn.dataset.csBtndone = '1';
            btn.style.setProperty('color','#fff','important');
            btn.style.setProperty('background','#1a1a1a','important');
            btn.style.setProperty('border-color','rgba(255,255,255,0.14)','important');
            btn.style.setProperty('font-weight','700','important');
            btn.addEventListener('mouseenter',()=>{
                btn.style.setProperty('background','#252525','important');
                btn.style.setProperty('border-color','rgba(255,255,255,0.25)','important');
            });
            btn.addEventListener('mouseleave',()=>{
                btn.style.setProperty('background','#1a1a1a','important');
                btn.style.setProperty('border-color','rgba(255,255,255,0.14)','important');
            });
        });
    }

    /* ── KPI card tilt / spotlight ── */
    function injectSpotlightCSS(){
        if(doc.getElementById('sh-spotlight-css')) return;
        const s = doc.createElement('style');
        s.id = 'sh-spotlight-css';
        s.textContent = `
            .sh-kpi { position:relative; overflow:hidden; }
            .sh-spotlight { position:absolute; width:250px; height:250px;
                background:radial-gradient(circle,rgba(255,255,255,0.04) 0%,transparent 70%);
                border-radius:50%; pointer-events:none; transform:translate(-50%,-50%);
                opacity:0; transition:opacity 0.2s; }
            .sh-kpi:hover .sh-spotlight { opacity:1; }
        `;
        doc.head.appendChild(s);
    }

    function addKpiSpotlight(){
        doc.querySelectorAll('.sh-kpi').forEach(card=>{
            if(card.dataset.spotDone) return;
            card.dataset.spotDone='1';
            const s=doc.createElement('div'); s.className='sh-spotlight'; card.appendChild(s);
            card.addEventListener('mousemove',e=>{const r=card.getBoundingClientRect();s.style.left=(e.clientX-r.left)+'px';s.style.top=(e.clientY-r.top)+'px';});
        });
    }

    /* ── Sidebar icons ── */
    const ICONS = {
        'Dashboard': '<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/></svg>',
        'Command Center': '<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="3"/><path d="M12 1v4M12 19v4M4.22 4.22l2.83 2.83M16.95 16.95l2.83 2.83M1 12h4M19 12h4M4.22 19.78l2.83-2.83M16.95 7.05l2.83-2.83"/></svg>',
        'RFM Analysis': '<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg>',
        'Churn Prediction': '<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>',
        'Revenue Forecast': '<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="1" x2="12" y2="23"/><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg>',
        'Upload Data': '<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><polyline points="16 16 12 12 8 16"/><line x1="12" y1="12" x2="12" y2="21"/><path d="M20.39 18.39A5 5 0 0 0 18 9h-1.26A8 8 0 1 0 3 16.3"/></svg>',
    };

    function addSidebarIcons(){
        const sb = doc.querySelector('[data-testid="stSidebar"]');
        if(!sb) return;
        sb.querySelectorAll('a[data-testid="stPageLink"]').forEach(link=>{
            if(link.dataset.icondone) return;
            const spans = link.querySelectorAll('span');
            let ts = null;
            for(const sp of spans){ const t=sp.textContent.trim(); if(ICONS[t]){ts=sp;break;} }
            if(!ts) return;
            const label = ts.textContent.trim();
            link.dataset.icondone='1';
            ts.innerHTML = '<span style="display:inline-flex;align-items:center;gap:10px;width:100%;">'
                + '<span style="display:flex;align-items:center;justify-content:center;width:26px;height:26px;border-radius:8px;flex-shrink:0;background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.07);">'
                + ICONS[label] + '</span>'
                + '<span style="color:#555;font-size:13px;font-weight:500;">' + label + '</span></span>';
        });
    }

    /* ── Scroll reveal ── */
    function initReveal(){
        if(!window._shRevealObs){
            window._shRevealObs = new IntersectionObserver(entries=>{
                entries.forEach((e,i)=>{
                    if(e.isIntersecting){
                        setTimeout(()=>e.target.classList.add('visible'), Math.min(i*60,300));
                        window._shRevealObs.unobserve(e.target);
                    }
                });
            },{threshold:0.05,rootMargin:'0px 0px -30px 0px'});
        }
        doc.querySelectorAll('.sh-kpi,.sh-card,.sh-insight,.sh-banner,.sh-odc,[data-testid="stPlotlyChart"],[data-testid="stDataFrame"]').forEach(el=>{
            if(el.dataset.revdone) return;
            el.dataset.revdone='1';
            el.classList.add('sh-reveal');
            window._shRevealObs.observe(el);
        });
    }

    function hideNavItems(){
        const n=doc.querySelector('[data-testid="stSidebarNav"]'); if(n) n.remove();
    }

    function run(){
        injectSpotlightCSS();
        addKpiSpotlight();
        addSidebarIcons();
        styleCountryBtns();
        highlightActiveNav();
        initReveal();
        hideNavItems();
    }

    setTimeout(run, 200);
    setTimeout(run, 700);
    setInterval(run, 900);
})();
</script>"""


def apply_styles(active_page: str = ""):
    """Inject the global Shalina design system into the current page."""
    st.markdown(_CSS, unsafe_allow_html=True)
    if active_page:
        st.markdown(
            f'<div id="sh-active-page" data-page="{active_page}" style="display:none;"></div>',
            unsafe_allow_html=True,
        )
    _stc.html(_JS, height=0)


def sidebar_nav(refresh_key: str = "refresh_data"):
    """Render the standard sidebar navigation block."""
    with st.sidebar:
        st.markdown("""
        <div style="padding:22px 10px 10px 10px;">
            <div style="font-size:9px;font-weight:700;letter-spacing:3.5px;text-transform:uppercase;color:#1a1a1a;margin-bottom:18px;">
                Navigation
            </div>
        </div>""", unsafe_allow_html=True)

        st.page_link("app.py",                    label="Dashboard")
        st.page_link("pages/Command_Center.py",   label="Command Center")
        st.page_link("pages/RFM_Analysis.py",     label="RFM Analysis")
        st.page_link("pages/Churn_Prediction.py", label="Churn Prediction")
        st.page_link("pages/Revenue_Forecast.py", label="Revenue Forecast")
        st.page_link("pages/Upload_Data.py",      label="Upload Data")

        st.markdown('<div class="sh-sidebar-divider"></div>', unsafe_allow_html=True)
        st.markdown('<span class="sh-sidebar-label">Data</span>', unsafe_allow_html=True)

        if st.button("Refresh Data", use_container_width=True, key=refresh_key):
            st.cache_data.clear()
            st.rerun()

        # Kill the auto Streamlit nav
        _stc.html("""<script>(function(){
            function r(){var n=window.parent.document.querySelector('[data-testid="stSidebarNav"]');
            if(n){n.remove();}else{setTimeout(r,200);}}r();setTimeout(r,800);
        })();</script>""", height=0)
