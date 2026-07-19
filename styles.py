"""
Shalina Distribution Intelligence — Shared Design System
VocalIQ-inspired: clean cards, purple #635bff accent, Inter typography.
Dark dashboard variant — readable navy-dark (NOT pitch-black).

Usage:  from styles import apply_styles, sidebar_nav
        apply_styles()          ← inject CSS + JS
        sidebar_nav()           ← render sidebar with nav links
"""
import streamlit as st
import streamlit.components.v1 as _stc

# ── Color tokens ─────────────────────────────────────────────────────────────
# Background:    #0d1117  (GitHub-dark navy — far less oppressive than #0a0a14)
# Surface:       #161b27  (cards, sidebar)
# Surface-2:     #1e2640  (hover, selected)
# Purple accent: #635bff  (VocalIQ brand purple)
# Text primary:  #e2e8f0  (near-white — clear on dark)
# Text secondary:#94a3b8  (slate-400 — readable muted)
# Text muted:    #4a5568  (slate-600 — labels, dividers)
# Border:        rgba(99,91,255,0.15)
# ─────────────────────────────────────────────────────────────────────────────

_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;600&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

/* ─────────────────────────────────────────────────────────
   APP SHELL
───────────────────────────────────────────────────────── */
.stApp, body, html {
    background: #0d1117 !important;
    font-family: 'Inter', -apple-system, sans-serif !important;
    font-size: 14px !important;
    color: #e2e8f0 !important;
}

/* Subtle purple glow at top — like VocalIQ's gradient hero, dark version */
.stApp::before {
    content: '' !important;
    display: block !important;
    position: fixed !important;
    inset: 0 !important;
    background: radial-gradient(ellipse 80% 50% at 50% -10%, rgba(99,91,255,0.14) 0%, transparent 60%) !important;
    pointer-events: none !important;
    z-index: 0 !important;
}

.main .block-container {
    background: transparent !important;
    padding: 1rem 2rem 4rem 2rem !important;
    max-width: 1440px !important;
    position: relative;
    z-index: 1;
}

/* ─────────────────────────────────────────────────────────
   KILL STREAMLIT CHROME
───────────────────────────────────────────────────────── */
[data-testid="stDecoration"],
[data-testid="stStatusWidget"],
#MainMenu, footer,
[data-testid="stSidebarNav"],
[data-testid="stSidebarNavItems"],
section[data-testid="stSidebar"] > div:first-child > div:first-child nav,
[data-testid="stImageContainer"] button,
[data-testid="StyledFullScreenButton"],
button[title="View fullscreen"],
button[title="Fullscreen"] { display: none !important; }

header[data-testid="stHeader"] {
    background: transparent !important;
    border: none !important;
}

/* ─────────────────────────────────────────────────────────
   SIDEBAR — readable dark navy with clear links
───────────────────────────────────────────────────────── */
section[data-testid="stSidebar"] {
    background: #161b27 !important;
    border-right: 1px solid rgba(99,91,255,0.12) !important;
    min-width: 220px !important;
}
section[data-testid="stSidebar"] > div:first-child {
    padding-top: 20px !important;
}

/* Nav links — bright enough to actually see */
section[data-testid="stSidebar"] a[data-testid="stPageLink"],
section[data-testid="stSidebar"] a[data-testid="stPageLink"] * {
    color: #94a3b8 !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    text-decoration: none !important;
}
section[data-testid="stSidebar"] a[data-testid="stPageLink"] {
    border-radius: 0.5rem !important;
    padding: 8px 12px !important;
    display: block !important;
    margin: 2px 8px !important;
    transition: background 0.15s, color 0.15s !important;
}
section[data-testid="stSidebar"] a[data-testid="stPageLink"]:hover,
section[data-testid="stSidebar"] a[data-testid="stPageLink"]:hover * {
    background: rgba(99,91,255,0.10) !important;
    color: #a5b4fc !important;
}

/* Sidebar button text */
section[data-testid="stSidebar"] .stButton > button {
    color: #94a3b8 !important;
    border: 1px solid rgba(99,91,255,0.18) !important;
    background: transparent !important;
    font-size: 12px !important;
    font-weight: 600 !important;
}
section[data-testid="stSidebar"] .stButton > button:hover {
    background: rgba(99,91,255,0.08) !important;
    color: #a5b4fc !important;
    border-color: rgba(99,91,255,0.35) !important;
}

/* Sidebar markdown text (labels, dividers) */
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] div,
section[data-testid="stSidebar"] span {
    color: #94a3b8 !important;
    font-family: 'Inter', sans-serif !important;
}

/* Sidebar toggle button */
[data-testid="collapsedControl"],
[data-testid="stSidebarCollapseButton"],
[data-testid="stExpandSidebarButton"],
button[kind="header"] {
    display: flex !important; visibility: visible !important;
    opacity: 1 !important; z-index: 999999 !important;
}
[data-testid="stExpandSidebarButton"] {
    position: fixed !important; top: 14px !important; left: 14px !important;
    width: 32px !important; height: 32px !important;
    background: #161b27 !important;
    border: 1px solid rgba(99,91,255,0.20) !important;
    border-radius: 0.5rem !important;
    align-items: center !important; justify-content: center !important;
}

/* ─────────────────────────────────────────────────────────
   BUTTONS
───────────────────────────────────────────────────────── */
.stButton > button {
    background: transparent !important;
    color: #94a3b8 !important;
    border: 1.5px solid rgba(99,91,255,0.20) !important;
    border-radius: 0.5rem !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 600 !important;
    font-size: 13px !important;
    padding: 8px 18px !important;
    transition: all 0.18s ease !important;
    box-shadow: none !important;
    outline: none !important;
}
.stButton > button:hover {
    background: rgba(99,91,255,0.10) !important;
    color: #a5b4fc !important;
    border-color: rgba(99,91,255,0.50) !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 16px rgba(99,91,255,0.15) !important;
}
.stButton > button:active { transform: translateY(0) !important; }

.stDownloadButton > button {
    background: transparent !important;
    color: #a5b4fc !important;
    border: 1.5px solid rgba(99,91,255,0.30) !important;
    border-radius: 0.5rem !important;
    font-weight: 600 !important;
    font-size: 13px !important;
}
.stDownloadButton > button:hover {
    background: rgba(99,91,255,0.12) !important;
    border-color: #635bff !important;
}

/* ─────────────────────────────────────────────────────────
   INPUTS
───────────────────────────────────────────────────────── */
input, .stTextInput input {
    background: #1e2640 !important;
    border: 1.5px solid rgba(99,91,255,0.18) !important;
    border-radius: 0.5rem !important;
    color: #e2e8f0 !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 14px !important;
    padding: 9px 14px !important;
    transition: border-color 0.18s, box-shadow 0.18s !important;
}
input:focus, .stTextInput input:focus {
    border-color: #635bff !important;
    box-shadow: 0 0 0 3px rgba(99,91,255,0.18) !important;
    outline: none !important;
}
input::placeholder { color: #4a5568 !important; }
.stTextInput > div, .stTextInput > div > div { background: transparent !important; }
.stTextInput label { display: none !important; }

/* Selectbox */
[data-baseweb="select"] > div {
    background: #1e2640 !important;
    border: 1.5px solid rgba(99,91,255,0.18) !important;
    border-radius: 0.5rem !important;
    color: #e2e8f0 !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 14px !important;
    transition: border-color 0.18s !important;
}
[data-baseweb="select"] > div:hover,
[data-baseweb="select"] > div:focus-within {
    border-color: #635bff !important;
    box-shadow: 0 0 0 3px rgba(99,91,255,0.12) !important;
}
[data-baseweb="select"] svg { fill: #4a5568 !important; }
[data-baseweb="popover"] {
    background: #161b27 !important;
    border: 1px solid rgba(99,91,255,0.20) !important;
    border-radius: 0.75rem !important;
    box-shadow: 0 20px 60px rgba(0,0,0,0.5) !important;
}
[role="option"] {
    background: transparent !important;
    color: #94a3b8 !important;
    font-size: 14px !important;
    border-radius: 6px !important;
    margin: 2px 6px !important;
}
[role="option"]:hover, [aria-selected="true"] {
    background: rgba(99,91,255,0.12) !important;
    color: #a5b4fc !important;
}
.stSelectbox label {
    color: #635bff !important;
    font-size: 11px !important;
    font-weight: 700 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.08em !important;
    margin-bottom: 6px !important;
    display: block !important;
}

/* ─────────────────────────────────────────────────────────
   DATA TABLE
───────────────────────────────────────────────────────── */
[data-testid="stDataFrame"] {
    border: 1px solid rgba(99,91,255,0.15) !important;
    border-radius: 0.75rem !important;
    overflow: hidden !important;
}
[data-testid="stDataFrame"] th {
    background: #1e2640 !important;
    color: #635bff !important;
    font-size: 11px !important;
    font-weight: 700 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.06em !important;
}
[data-testid="stDataFrame"] td {
    font-size: 13px !important;
    color: #cbd5e1 !important;
    border-color: rgba(99,91,255,0.06) !important;
}

/* ─────────────────────────────────────────────────────────
   METRIC
───────────────────────────────────────────────────────── */
[data-testid="stMetric"] {
    background: #161b27 !important;
    border: 1px solid rgba(99,91,255,0.15) !important;
    border-radius: 0.75rem !important;
    padding: 20px 22px !important;
}
[data-testid="stMetricLabel"]  { color: #635bff !important; font-size: 11px !important; font-weight: 700 !important; letter-spacing: 0.08em !important; text-transform: uppercase !important; }
[data-testid="stMetricValue"]  { color: #e2e8f0 !important; font-size: 36px !important; font-weight: 800 !important; letter-spacing: -1px !important; }
[data-testid="stMetricDelta"]  { color: #4a5568 !important; font-size: 12px !important; }

/* ─────────────────────────────────────────────────────────
   TABS
───────────────────────────────────────────────────────── */
.stTabs [data-baseweb="tab-list"] {
    background: #161b27 !important;
    border-radius: 0.5rem !important;
    border: 1px solid rgba(99,91,255,0.14) !important;
    padding: 4px !important; gap: 4px !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    border-radius: 0.375rem !important;
    color: #64748b !important;
    font-size: 13px !important; font-weight: 600 !important;
    border: none !important; padding: 7px 18px !important;
}
.stTabs [aria-selected="true"] {
    background: rgba(99,91,255,0.16) !important;
    color: #a5b4fc !important;
}
.stTabs [data-baseweb="tab-border"],
.stTabs [data-baseweb="tab-highlight"] { display: none !important; }

/* Expander */
[data-testid="stExpander"] {
    background: #161b27 !important;
    border: 1px solid rgba(99,91,255,0.14) !important;
    border-radius: 0.75rem !important;
}
[data-testid="stExpander"] summary { color: #94a3b8 !important; font-size: 14px !important; }

/* ─────────────────────────────────────────────────────────
   DESIGN COMPONENT CLASSES
───────────────────────────────────────────────────────── */

/* — Top bar — */
.sh-topbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 20px 0 16px 0;
    border-bottom: 1px solid rgba(99,91,255,0.12);
    margin-bottom: 24px;
}
.sh-eyebrow {
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #635bff;
    margin-bottom: 6px;
}
.sh-title {
    font-size: 30px;
    font-weight: 800;
    color: #e2e8f0;
    letter-spacing: -1px;
    line-height: 1.1;
}
.sh-title-dim { color: rgba(226,232,240,0.35); }

.sh-pill-group { display: flex; gap: 8px; align-items: center; flex-wrap: wrap; }
.sh-pill {
    display: inline-flex;
    align-items: center;
    gap: 7px;
    background: rgba(99,91,255,0.08);
    border: 1px solid rgba(99,91,255,0.18);
    border-radius: 0.5rem;
    padding: 6px 14px;
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 0.07em;
    text-transform: uppercase;
    color: #64748b;
}
.sh-dot {
    width: 6px; height: 6px; border-radius: 50%;
    background: #10b981;
    box-shadow: 0 0 6px rgba(16,185,129,0.9), 0 0 12px rgba(16,185,129,0.4);
    animation: sh-pulse 2.2s ease-in-out infinite;
    flex-shrink: 0;
}
.sh-dot-amber { background: #f59e0b; box-shadow: 0 0 6px rgba(245,158,11,0.9), 0 0 12px rgba(245,158,11,0.4); }
@keyframes sh-pulse { 0%,100%{opacity:1;} 50%{opacity:0.3;} }

/* — KPI Row — */
.sh-kpi-row {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 16px;
    margin-bottom: 28px;
}
@media (max-width: 900px) { .sh-kpi-row { grid-template-columns: repeat(2,1fr); } }

.sh-kpi {
    background: #161b27;
    border: 1px solid rgba(99,91,255,0.15);
    border-radius: 0.875rem;
    padding: 26px 22px 20px 22px;
    position: relative;
    overflow: hidden;
    cursor: default;
    transition: transform 0.2s, border-color 0.2s, box-shadow 0.2s;
    box-shadow: 0 1px 4px rgba(0,0,0,0.3);
}
.sh-kpi:hover {
    transform: translateY(-3px);
    border-color: rgba(99,91,255,0.35);
    box-shadow: 0 8px 32px rgba(99,91,255,0.12);
}
.sh-kpi-accent {
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
}
.sh-kpi-label {
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #635bff;
    margin-bottom: 14px;
    line-height: 1.4;
}
.sh-kpi-value {
    font-size: 48px;
    font-weight: 800;
    color: #e2e8f0;
    line-height: 1;
    letter-spacing: -2px;
    margin-bottom: 10px;
}
.sh-kpi-delta {
    font-size: 12px;
    color: #4a5568;
    font-weight: 500;
    line-height: 1.5;
}

/* — Section heading — */
.sh-section {
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #635bff;
    margin-top: 32px;
    margin-bottom: 14px;
    display: flex;
    align-items: center;
    gap: 14px;
}
.sh-section::after {
    content: '';
    flex: 1;
    height: 1px;
    background: rgba(99,91,255,0.12);
}

/* — Card — */
.sh-card {
    background: #161b27;
    border: 1px solid rgba(99,91,255,0.12);
    border-radius: 0.875rem;
    padding: 20px 22px;
    transition: border-color 0.18s, box-shadow 0.18s;
    box-shadow: 0 1px 4px rgba(0,0,0,0.2);
}
.sh-card:hover {
    border-color: rgba(99,91,255,0.28);
    box-shadow: 0 4px 20px rgba(99,91,255,0.08);
}

/* — Insight card — */
.sh-insight {
    background: #161b27;
    border: 1px solid rgba(99,91,255,0.12);
    border-radius: 0.875rem;
    padding: 18px 20px;
    margin-bottom: 10px;
    transition: border-color 0.18s, box-shadow 0.18s;
}
.sh-insight:hover {
    border-color: rgba(99,91,255,0.28);
    box-shadow: 0 4px 20px rgba(99,91,255,0.08);
}
.sh-insight-title { font-size: 14px; font-weight: 700; color: #e2e8f0; margin-bottom: 6px; }
.sh-insight-body  { font-size: 13px; color: #64748b; line-height: 1.7; }

/* — Outlet detail card — */
.sh-odc {
    background: #161b27;
    border: 1px solid rgba(99,91,255,0.18);
    border-radius: 0.875rem;
    padding: 24px 26px 20px 26px;
    margin-bottom: 24px;
    box-shadow: 0 4px 24px rgba(99,91,255,0.08);
}
.sh-odc-tag  { font-size: 11px; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase; color: #635bff; margin-bottom: 8px; }
.sh-odc-name { font-size: 24px; font-weight: 800; color: #e2e8f0; letter-spacing: -0.6px; line-height: 1.1; margin-bottom: 12px; }
.sh-odc-meta { display: flex; gap: 8px; align-items: center; flex-wrap: wrap; padding-bottom: 16px; margin-bottom: 16px; border-bottom: 1px solid rgba(99,91,255,0.08); }
.sh-odc-stats { display: flex; align-items: stretch; gap: 0; }
.sh-odc-stat  { flex: 1; padding: 0 20px; }
.sh-odc-stat:first-child { padding-left: 0; }
.sh-odc-divider { width: 1px; background: rgba(99,91,255,0.08); flex-shrink: 0; }
.sh-odc-stat-label { font-size: 11px; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase; color: #635bff; margin-bottom: 8px; }
.sh-odc-stat-value { font-size: 24px; font-weight: 800; letter-spacing: -0.6px; line-height: 1; }

/* — Banner — */
.sh-banner {
    background: rgba(99,91,255,0.06);
    border: 1px solid rgba(99,91,255,0.16);
    border-radius: 0.875rem;
    padding: 14px 20px;
    margin-bottom: 18px;
    display: flex;
    align-items: center;
    gap: 14px;
}

/* — Badges — */
.sh-badge { display: inline-block; padding: 3px 12px; border-radius: 0.375rem; font-size: 10px; font-weight: 700; letter-spacing: 0.07em; text-transform: uppercase; }
.sh-badge-red    { background: rgba(239,68,68,0.12);   color: #fca5a5; border: 1px solid rgba(239,68,68,0.22); }
.sh-badge-orange { background: rgba(249,115,22,0.12);  color: #fdba74; border: 1px solid rgba(249,115,22,0.22); }
.sh-badge-blue   { background: rgba(99,91,255,0.12);   color: #a5b4fc; border: 1px solid rgba(99,91,255,0.28); }
.sh-badge-purple { background: rgba(168,85,247,0.12);  color: #d8b4fe; border: 1px solid rgba(168,85,247,0.28); }
.sh-badge-green  { background: rgba(16,185,129,0.12);  color: #6ee7b7; border: 1px solid rgba(16,185,129,0.28); }
.sh-badge-amber  { background: rgba(245,158,11,0.12);  color: #fde68a; border: 1px solid rgba(245,158,11,0.28); }

/* — Sidebar labels — */
.sh-sidebar-label {
    font-size: 10px !important; font-weight: 700 !important;
    letter-spacing: 0.08em !important; text-transform: uppercase !important;
    color: #4a5568 !important; padding: 0 8px !important;
    margin-bottom: 6px !important; margin-top: 20px !important;
    display: block;
}
.sh-sidebar-divider { height: 1px; background: rgba(99,91,255,0.10); margin: 16px 8px; }

/* — Page sub-header — */
.sh-page-title { font-size: 26px; font-weight: 800; color: #e2e8f0; letter-spacing: -0.8px; line-height: 1.1; margin-bottom: 4px; }
.sh-page-sub   { font-size: 13px; color: #4a5568; margin-bottom: 22px; }

/* — Error / warning — */
.sh-error { background: rgba(239,68,68,0.08); border: 1px solid rgba(239,68,68,0.22); border-radius: 0.75rem; padding: 16px 20px; color: #fca5a5; font-weight: 600; font-size: 14px; }
.sh-warn  { background: rgba(245,158,11,0.08); border: 1px solid rgba(245,158,11,0.22); border-radius: 0.75rem; padding: 16px 20px; color: #fde68a; font-weight: 600; font-size: 14px; }

/* — Body text — */
p, .stMarkdown p, li, label, span:not([class]) {
    font-size: 14px !important;
    line-height: 1.6 !important;
    color: #cbd5e1 !important;
}

/* — Plotly modebar — */
.js-plotly-plot .plotly .modebar { background: transparent !important; }
.js-plotly-plot .plotly .modebar-btn path { fill: #4a5568 !important; }

/* — Scroll reveal — */
.sh-reveal { opacity:0; transform:translateY(22px); transition:opacity 0.55s cubic-bezier(.16,1,.3,1),transform 0.55s cubic-bezier(.16,1,.3,1); }
.sh-reveal.visible { opacity:1; transform:translateY(0); }
</style>
"""

_JS = """<script>
(function(){
    const doc = window.parent.document;

    /* ── Nav active highlight — purple on dark ── */
    const NAV_LABELS = ['Dashboard','Outlet Performance','Whitespace Detection','Expansion Strategy'];

    function highlightActiveNav(){
        const marker = doc.getElementById('sh-active-page');
        if(!marker) return;
        const active = marker.getAttribute('data-page');
        doc.querySelectorAll('button').forEach(btn=>{
            const txt = btn.textContent.trim();
            if(!NAV_LABELS.includes(txt)) return;
            if(btn.dataset.navActive === String(txt===active) && btn.dataset.navStyled) return;
            btn.dataset.navStyled = '1';
            btn.dataset.navActive = String(txt===active);
            if(txt===active){
                btn.style.setProperty('background','rgba(99,91,255,0.16)','important');
                btn.style.setProperty('color','#a5b4fc','important');
                btn.style.setProperty('border-color','rgba(99,91,255,0.50)','important');
                btn.style.setProperty('font-weight','700','important');
            } else {
                btn.style.setProperty('background','transparent','important');
                btn.style.setProperty('color','#64748b','important');
                btn.style.setProperty('border-color','rgba(99,91,255,0.18)','important');
                btn.style.setProperty('font-weight','500','important');
            }
        });
    }

    /* ── Country buttons ── */
    function styleCountryBtns(){
        doc.querySelectorAll('button').forEach(btn=>{
            const txt = btn.textContent.trim();
            if(txt !== 'Nigeria' && txt !== 'Angola') return;
            if(btn.dataset.cbDone) return;
            btn.dataset.cbDone = '1';
            btn.style.setProperty('color','#e2e8f0','important');
            btn.style.setProperty('background','rgba(99,91,255,0.12)','important');
            btn.style.setProperty('border-color','rgba(99,91,255,0.35)','important');
            btn.style.setProperty('font-weight','700','important');
            btn.style.setProperty('font-size','13px','important');
            btn.addEventListener('mouseenter',()=>{
                btn.style.setProperty('background','rgba(99,91,255,0.22)','important');
                btn.style.setProperty('border-color','#635bff','important');
                btn.style.setProperty('box-shadow','0 4px 16px rgba(99,91,255,0.22)','important');
            });
            btn.addEventListener('mouseleave',()=>{
                btn.style.setProperty('background','rgba(99,91,255,0.12)','important');
                btn.style.setProperty('border-color','rgba(99,91,255,0.35)','important');
                btn.style.removeProperty('box-shadow');
            });
        });
    }

    /* ── Sidebar icons ── */
    const ICONS = {
        'Dashboard':       '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/></svg>',
        'Command Center':  '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="3"/><path d="M12 1v4M12 19v4M4.22 4.22l2.83 2.83M16.95 16.95l2.83 2.83M1 12h4M19 12h4M4.22 19.78l2.83-2.83M16.95 7.05l2.83-2.83"/></svg>',
        'RFM Analysis':    '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg>',
        'Churn Prediction':'<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>',
        'Revenue Forecast':'<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="1" x2="12" y2="23"/><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg>',
        'Upload Data':     '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><polyline points="16 16 12 12 8 16"/><line x1="12" y1="12" x2="12" y2="21"/><path d="M20.39 18.39A5 5 0 0 0 18 9h-1.26A8 8 0 1 0 3 16.3"/></svg>',
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
            ts.innerHTML =
                '<span style="display:inline-flex;align-items:center;gap:10px;width:100%;">'
                +'<span style="display:flex;align-items:center;justify-content:center;width:28px;height:28px;border-radius:7px;flex-shrink:0;background:rgba(99,91,255,0.10);border:1px solid rgba(99,91,255,0.18);color:#94a3b8;">'
                + ICONS[label] + '</span>'
                +'<span style="color:#94a3b8;font-size:13px;font-weight:500;">' + label + '</span></span>';
        });
    }

    /* ── Scroll reveal ── */
    function initReveal(){
        if(!window._shRevObs){
            window._shRevObs = new IntersectionObserver(entries=>{
                entries.forEach((e,i)=>{ if(e.isIntersecting){ setTimeout(()=>e.target.classList.add('visible'), Math.min(i*60,300)); window._shRevObs.unobserve(e.target); } });
            }, {threshold:0.05, rootMargin:'0px 0px -20px 0px'});
        }
        doc.querySelectorAll('.sh-kpi,.sh-card,.sh-insight,.sh-banner,.sh-odc,[data-testid="stPlotlyChart"],[data-testid="stDataFrame"]').forEach(el=>{
            if(el.dataset.revdone) return; el.dataset.revdone='1';
            el.classList.add('sh-reveal'); window._shRevObs.observe(el);
        });
    }

    function hideNav(){
        const n = doc.querySelector('[data-testid="stSidebarNav"]');
        if(n) n.remove();
    }

    function run(){
        addSidebarIcons(); styleCountryBtns();
        highlightActiveNav(); initReveal(); hideNav();
    }

    setTimeout(run, 200);
    setTimeout(run, 700);
    setInterval(run, 1000);
})();
</script>"""


def apply_styles(active_page: str = ""):
    """Inject the Shalina design system (VocalIQ-inspired dark nav)."""
    st.markdown(_CSS, unsafe_allow_html=True)
    if active_page:
        st.markdown(
            f'<div id="sh-active-page" data-page="{active_page}" style="display:none;"></div>',
            unsafe_allow_html=True,
        )
    _stc.html(_JS, height=0)


def sidebar_nav(refresh_key: str = "refresh_data"):
    """Standard sidebar: logo label + nav links + refresh button."""
    with st.sidebar:
        st.markdown("""
        <div style="padding:18px 16px 8px 16px;">
            <div style="font-size:10px;font-weight:700;letter-spacing:0.08em;text-transform:uppercase;
                 color:#4a5568;margin-bottom:14px;">Navigation</div>
        </div>""", unsafe_allow_html=True)

        st.page_link("app.py",                    label="Dashboard")
        st.page_link("pages/Command_Center.py",   label="Command Center")
        st.page_link("pages/RFM_Analysis.py",     label="RFM Analysis")
        st.page_link("pages/Churn_Prediction.py", label="Churn Prediction")
        st.page_link("pages/Revenue_Forecast.py", label="Revenue Forecast")
        st.page_link("pages/Upload_Data.py",      label="Upload Data")

        st.markdown('<div class="sh-sidebar-divider"></div>', unsafe_allow_html=True)
        st.markdown('<span class="sh-sidebar-label">Data</span>', unsafe_allow_html=True)

        if st.button("⟳  Refresh Data", use_container_width=True, key=refresh_key):
            st.cache_data.clear()
            st.rerun()

        _stc.html("""<script>(function(){
            function r(){var n=window.parent.document.querySelector('[data-testid="stSidebarNav"]');
            if(n){n.remove();}else{setTimeout(r,200);}}
            r(); setTimeout(r,800);
        })();</script>""", height=0)
