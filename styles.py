"""
Shalina Distribution Intelligence — Shared Design System
Light theme: #f4f7ff background, white cards, #635bff purple accent, Inter.
Clean, professional, presentation-ready.
"""
import streamlit as st
import streamlit.components.v1 as _stc

_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

/* ── Kill Streamlit chrome & the "keyboard_double_arrow_right" junk ── */
[data-testid="stDecoration"],
[data-testid="stStatusWidget"],
#MainMenu, footer,
[data-testid="stSidebarNav"],
[data-testid="stSidebarNavItems"],
[data-testid="stMainMenuPopover"],
[data-testid="stPageSwitcherButton"],
[data-testid="stToolbarActionButton"],
[data-testid="stToolbar"] [data-testid="baseButton-header"],
section[data-testid="stSidebar"] > div:first-child > div:first-child nav,
[data-testid="stImageContainer"] button,
[data-testid="StyledFullScreenButton"],
button[title="View fullscreen"],
button[title="Fullscreen"],
.stAppToolbar { display: none !important; }

header[data-testid="stHeader"] {
    background: transparent !important;
    height: 0 !important;
    min-height: 0 !important;
    border: none !important;
    padding: 0 !important;
    overflow: hidden !important;
}

/* ── App — light whitish-grey ── */
.stApp, body, html {
    background: #f4f7ff !important;
    font-family: 'Inter', -apple-system, sans-serif !important;
    font-size: 14px !important;
    color: #0f172a !important;
}

/* Very subtle purple tint at top */
.stApp::before {
    content: '' !important;
    position: fixed !important;
    top: 0; left: 0; right: 0; height: 320px !important;
    background: radial-gradient(ellipse 120% 80% at 60% 0%, rgba(99,91,255,0.07) 0%, transparent 65%) !important;
    pointer-events: none !important;
    z-index: 0 !important;
}

.main .block-container {
    background: transparent !important;
    padding: 1.5rem 2.5rem 4rem 2.5rem !important;
    max-width: 1440px !important;
    position: relative; z-index: 1;
}

/* ── Sidebar — dark navy panel ── */
section[data-testid="stSidebar"] {
    background: #0d0f1e !important;
    border-right: none !important;
    min-width: 240px !important;
    box-shadow: 4px 0 24px rgba(0,0,0,0.20) !important;
}
section[data-testid="stSidebar"] > div:first-child { padding-top: 20px !important; }

/* Nav links — base */
section[data-testid="stSidebar"] a[data-testid="stPageLink"] {
    border-radius: 10px !important;
    padding: 10px 14px !important;
    display: block !important;
    margin: 3px 12px !important;
    transition: background 0.18s !important;
    text-decoration: none !important;
    position: relative !important;
}
section[data-testid="stSidebar"] a[data-testid="stPageLink"] * {
    color: rgba(255,255,255,0.60) !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 14px !important;
    font-weight: 500 !important;
}
section[data-testid="stSidebar"] a[data-testid="stPageLink"]:hover {
    background: rgba(255,255,255,0.07) !important;
}
section[data-testid="stSidebar"] a[data-testid="stPageLink"]:hover * {
    color: #ffffff !important;
}

/* Sidebar misc text */
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] div,
section[data-testid="stSidebar"] span { color: rgba(255,255,255,0.45) !important; font-family: 'Inter',sans-serif !important; }

/* Sidebar refresh button */
section[data-testid="stSidebar"] .stButton > button {
    color: rgba(255,255,255,0.55) !important;
    border: 1px solid rgba(255,255,255,0.10) !important;
    background: rgba(255,255,255,0.05) !important;
    font-size: 12.5px !important; font-weight: 600 !important;
    padding: 9px 16px !important;
    border-radius: 10px !important;
    width: 100% !important;
    letter-spacing: 0.01em !important;
}
section[data-testid="stSidebar"] .stButton > button:hover {
    background: rgba(99,91,255,0.20) !important;
    color: #ffffff !important;
    border-color: rgba(99,91,255,0.50) !important;
}

/* Sidebar toggle */
[data-testid="stExpandSidebarButton"],
[data-testid="stSidebarCollapseButton"],
[data-testid="collapsedControl"] {
    display: flex !important; visibility: visible !important; opacity: 1 !important; z-index: 999 !important;
}
[data-testid="stExpandSidebarButton"] {
    position: fixed !important; top: 12px !important; left: 12px !important;
    width: 34px !important; height: 34px !important;
    background: #0d0f1e !important;
    border: 1px solid rgba(255,255,255,0.10) !important;
    border-radius: 8px !important;
    align-items: center !important; justify-content: center !important;
    box-shadow: 0 2px 10px rgba(0,0,0,0.30) !important;
}

/* ── Main content buttons ── */
.stButton > button {
    background: #ffffff !important;
    color: #374151 !important;
    border: 1.5px solid #e2e8f0 !important;
    border-radius: 8px !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 600 !important;
    font-size: 13.5px !important;
    padding: 9px 20px !important;
    transition: all 0.18s ease !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.06) !important;
}
.stButton > button:hover {
    background: #f8f5ff !important;
    color: #635bff !important;
    border-color: rgba(99,91,255,0.40) !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 14px rgba(99,91,255,0.14) !important;
}

.stDownloadButton > button {
    color: #635bff !important;
    border: 1.5px solid rgba(99,91,255,0.28) !important;
    background: rgba(99,91,255,0.05) !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    font-size: 13.5px !important;
}
.stDownloadButton > button:hover {
    background: rgba(99,91,255,0.10) !important;
    border-color: #635bff !important;
}

/* ── Inputs ── */
input, .stTextInput input {
    background: #ffffff !important;
    border: 1.5px solid #e2e8f0 !important;
    border-radius: 8px !important;
    color: #0f172a !important;
    font-size: 14px !important;
    padding: 10px 14px !important;
    transition: border-color 0.18s, box-shadow 0.18s !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04) !important;
}
input:focus, .stTextInput input:focus {
    border-color: #635bff !important;
    box-shadow: 0 0 0 3px rgba(99,91,255,0.12) !important;
    outline: none !important;
}
input::placeholder { color: #cbd5e1 !important; }
.stTextInput > div, .stTextInput > div > div { background: transparent !important; }
.stTextInput label { display: none !important; }

/* Selectbox */
[data-baseweb="select"] > div {
    background: #ffffff !important;
    border: 1.5px solid #e2e8f0 !important;
    border-radius: 8px !important;
    color: #0f172a !important;
    font-size: 14px !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04) !important;
}
[data-baseweb="select"] > div:hover,
[data-baseweb="select"] > div:focus-within {
    border-color: #635bff !important;
    box-shadow: 0 0 0 3px rgba(99,91,255,0.10) !important;
}
[data-baseweb="select"] svg { fill: #94a3b8 !important; }
[data-baseweb="popover"] {
    background: #ffffff !important;
    border: 1px solid #e8ecf7 !important;
    border-radius: 10px !important;
    box-shadow: 0 16px 48px rgba(15,23,42,0.12) !important;
}
[role="option"] { background: transparent !important; color: #374151 !important; font-size: 14px !important; border-radius: 6px !important; margin: 2px 6px !important; }
[role="option"]:hover, [aria-selected="true"] { background: rgba(99,91,255,0.07) !important; color: #635bff !important; }

.stSelectbox label { color: #635bff !important; font-size: 11px !important; font-weight: 700 !important; text-transform: uppercase !important; letter-spacing: 0.08em !important; margin-bottom: 6px !important; display: block !important; }

/* Slider */
[data-testid="stSlider"] label { color: #635bff !important; font-size: 11px !important; font-weight: 700 !important; text-transform: uppercase !important; letter-spacing: 0.08em !important; }

/* ── Data Table ── */
[data-testid="stDataFrame"] {
    border: 1px solid #e8ecf7 !important;
    border-radius: 10px !important; overflow: hidden !important;
    box-shadow: 0 1px 4px rgba(0,0,0,0.05) !important;
}
[data-testid="stDataFrame"] th {
    background: #f8f9fc !important;
    color: #635bff !important;
    font-size: 11px !important; font-weight: 700 !important;
    text-transform: uppercase !important; letter-spacing: 0.06em !important;
}
[data-testid="stDataFrame"] td { font-size: 13px !important; color: #374151 !important; border-color: #f1f5f9 !important; }
[data-testid="stDataFrame"] tr:hover td { background: rgba(99,91,255,0.04) !important; }

/* ── Metric ── */
[data-testid="stMetric"] {
    background: #ffffff !important;
    border: 1px solid #e8ecf7 !important;
    border-radius: 10px !important;
    padding: 22px !important;
    box-shadow: 0 1px 4px rgba(0,0,0,0.05) !important;
}
[data-testid="stMetricLabel"] { color: #635bff !important; font-size: 11px !important; font-weight: 700 !important; letter-spacing: 0.08em !important; text-transform: uppercase !important; }
[data-testid="stMetricValue"] { color: #0f172a !important; font-size: 36px !important; font-weight: 800 !important; letter-spacing: -1px !important; }
[data-testid="stMetricDelta"] { color: #94a3b8 !important; font-size: 12px !important; }

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background: #f1f5f9 !important;
    border-radius: 8px !important;
    border: 1px solid #e2e8f0 !important;
    padding: 4px !important; gap: 4px !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important; border-radius: 6px !important;
    color: #94a3b8 !important; font-size: 13px !important; font-weight: 600 !important;
    border: none !important; padding: 8px 20px !important;
}
.stTabs [aria-selected="true"] { background: #ffffff !important; color: #635bff !important; box-shadow: 0 1px 4px rgba(0,0,0,0.08) !important; }
.stTabs [data-baseweb="tab-border"], .stTabs [data-baseweb="tab-highlight"] { display: none !important; }

/* Expander */
[data-testid="stExpander"] {
    background: #ffffff !important;
    border: 1px solid #e8ecf7 !important;
    border-radius: 10px !important;
    box-shadow: 0 1px 4px rgba(0,0,0,0.04) !important;
}
[data-testid="stExpander"] summary { color: #374151 !important; font-size: 14px !important; }

/* ── General text ── */
p, .stMarkdown p { font-size: 14px !important; color: #64748b !important; line-height: 1.65 !important; }

/* ═══════════════════════════════════════════════════
   DESIGN COMPONENTS
═══════════════════════════════════════════════════ */

/* ─ Top bar ─ */
.sh-topbar {
    display: flex; align-items: flex-start;
    justify-content: space-between;
    padding: 4px 0 20px 0;
    border-bottom: 1px solid #e8ecf7;
    margin-bottom: 28px;
}
.sh-eyebrow {
    font-size: 11px; font-weight: 700; letter-spacing: 0.09em;
    text-transform: uppercase; color: #635bff; margin-bottom: 6px;
}
.sh-title {
    font-size: 30px; font-weight: 800; color: #0f172a;
    letter-spacing: -1.2px; line-height: 1.1;
}
.sh-title-dim { color: #94a3b8; }

.sh-pill-group { display: flex; gap: 8px; align-items: center; flex-wrap: wrap; margin-top: 4px; }
.sh-pill {
    display: inline-flex; align-items: center; gap: 7px;
    background: #f8f9fc;
    border: 1px solid #e2e8f0;
    border-radius: 8px; padding: 6px 14px;
    font-size: 10px; font-weight: 700; letter-spacing: 0.07em;
    text-transform: uppercase; color: #94a3b8;
}
.sh-dot {
    width: 7px; height: 7px; border-radius: 50%;
    background: #10b981;
    box-shadow: 0 0 6px rgba(16,185,129,0.8), 0 0 12px rgba(16,185,129,0.3);
    animation: sh-pulse 2.4s ease-in-out infinite; flex-shrink: 0;
}
.sh-dot-amber { background: #f59e0b; box-shadow: 0 0 6px rgba(245,158,11,0.8), 0 0 12px rgba(245,158,11,0.3); }
@keyframes sh-pulse { 0%,100%{opacity:1;} 50%{opacity:0.35;} }

/* ─ KPI row ─ */
.sh-kpi-row {
    display: grid !important;
    grid-template-columns: repeat(4, 1fr) !important;
    gap: 16px !important;
    margin-bottom: 28px !important;
}
@media(max-width:900px){ .sh-kpi-row { grid-template-columns: repeat(2,1fr) !important; } }

.sh-kpi {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    padding: 26px 22px 20px 22px;
    position: relative; overflow: hidden;
    transition: transform 0.2s, border-color 0.2s, box-shadow 0.2s;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05);
}
.sh-kpi:hover {
    transform: translateY(-3px);
    border-color: rgba(99,91,255,0.30);
    box-shadow: 0 8px 28px rgba(99,91,255,0.12);
}
.sh-kpi-accent { position: absolute; top: 0; left: 0; right: 0; height: 3px; }
.sh-kpi-label {
    font-size: 10px; font-weight: 700; letter-spacing: 0.11em;
    text-transform: uppercase; color: #64748b; margin-bottom: 12px; line-height: 1.4;
}
.sh-kpi-value {
    font-size: 44px; font-weight: 800; color: #0b1936;
    line-height: 1; letter-spacing: -2px; margin-bottom: 10px;
}
.sh-kpi-delta { font-size: 12px; color: #94a3b8; font-weight: 500; line-height: 1.5; }

/* ─ Section heading ─ */
.sh-section {
    font-size: 11px; font-weight: 700; letter-spacing: 0.09em;
    text-transform: uppercase; color: #635bff;
    margin-top: 30px; margin-bottom: 14px;
    display: flex; align-items: center; gap: 14px;
}
.sh-section::after { content:''; flex:1; height:1px; background:#e8ecf7; }

/* ─ Card ─ */
.sh-card {
    background: #ffffff;
    border: 1px solid #e8ecf7;
    border-radius: 12px; padding: 22px 24px;
    transition: border-color 0.18s, box-shadow 0.18s;
    box-shadow: 0 1px 4px rgba(0,0,0,0.05);
}
.sh-card:hover { border-color: rgba(99,91,255,0.28); box-shadow: 0 6px 22px rgba(99,91,255,0.09); }

/* ─ Insight ─ */
.sh-insight {
    background: #ffffff;
    border: 1px solid #e8ecf7;
    border-radius: 12px; padding: 18px 20px; margin-bottom: 10px;
    transition: border-color 0.18s, box-shadow 0.18s;
    box-shadow: 0 1px 4px rgba(0,0,0,0.04);
}
.sh-insight:hover { border-color: rgba(99,91,255,0.28); box-shadow: 0 6px 22px rgba(99,91,255,0.09); }
.sh-insight-title { font-size: 15px; font-weight: 700; color: #0f172a; margin-bottom: 6px; }
.sh-insight-body  { font-size: 13px; color: #64748b; line-height: 1.7; }

/* ─ Outlet detail card ─ */
.sh-odc {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 12px; padding: 26px 28px 22px 28px; margin-bottom: 24px;
    box-shadow: 0 4px 18px rgba(99,91,255,0.08);
}
.sh-odc-tag  { font-size: 11px; font-weight: 700; letter-spacing: 0.09em; text-transform: uppercase; color: #635bff; margin-bottom: 8px; }
.sh-odc-name { font-size: 26px; font-weight: 800; color: #0f172a; letter-spacing: -0.8px; line-height: 1.1; margin-bottom: 12px; }
.sh-odc-meta { display:flex; gap:8px; align-items:center; flex-wrap:wrap; padding-bottom:16px; margin-bottom:16px; border-bottom:1px solid #f1f5f9; }
.sh-odc-stats { display:flex; align-items:stretch; gap:0; }
.sh-odc-stat  { flex:1; padding:0 22px; }
.sh-odc-stat:first-child { padding-left:0; }
.sh-odc-divider { width:1px; background:#f1f5f9; flex-shrink:0; }
.sh-odc-stat-label { font-size:11px; font-weight:700; letter-spacing:0.09em; text-transform:uppercase; color:#635bff; margin-bottom:8px; }
.sh-odc-stat-value { font-size:26px; font-weight:800; letter-spacing:-0.8px; line-height:1; color:#0f172a; }

/* ─ Banner ─ */
.sh-banner {
    background: #ffffff;
    border: none;
    border-radius: 12px; padding: 14px 20px; margin-bottom: 20px;
    display: flex; align-items: center; gap: 14px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05);
}

/* ─ Badges ─ */
.sh-badge { display:inline-block; padding:3px 12px; border-radius:6px; font-size:10px; font-weight:700; letter-spacing:0.07em; text-transform:uppercase; }
.sh-badge-red    { background:rgba(239,68,68,0.08);   color:#dc2626; border:1px solid rgba(239,68,68,0.20); }
.sh-badge-orange { background:rgba(249,115,22,0.08);  color:#ea580c; border:1px solid rgba(249,115,22,0.20); }
.sh-badge-blue   { background:rgba(99,91,255,0.08);   color:#635bff; border:1px solid rgba(99,91,255,0.22); }
.sh-badge-purple { background:rgba(168,85,247,0.08);  color:#9333ea; border:1px solid rgba(168,85,247,0.22); }
.sh-badge-green  { background:rgba(16,185,129,0.08);  color:#059669; border:1px solid rgba(16,185,129,0.22); }
.sh-badge-amber  { background:rgba(245,158,11,0.08);  color:#d97706; border:1px solid rgba(245,158,11,0.22); }

/* ─ Sidebar labels ─ */
.sh-sidebar-label {
    font-size: 10px !important; font-weight: 700 !important;
    letter-spacing: 0.09em !important; text-transform: uppercase !important;
    color: rgba(255,255,255,0.22) !important; padding: 0 14px !important;
    margin-bottom: 6px !important; margin-top: 20px !important; display: block;
}
.sh-sidebar-divider { height: 1px; background: rgba(255,255,255,0.06); margin: 16px 12px; }

/* ─ Errors ─ */
.sh-error { background:rgba(239,68,68,0.06); border:1px solid rgba(239,68,68,0.20); border-radius:10px; padding:16px 20px; color:#dc2626; font-weight:600; font-size:14px; }
.sh-warn  { background:rgba(245,158,11,0.06); border:1px solid rgba(245,158,11,0.20); border-radius:10px; padding:16px 20px; color:#d97706; font-weight:600; font-size:14px; }

/* ─ Reveal ─ */
.sh-reveal { opacity:0; transform:translateY(18px); transition:opacity 0.45s cubic-bezier(.16,1,.3,1), transform 0.45s cubic-bezier(.16,1,.3,1); }
.sh-reveal.visible { opacity:1; transform:translateY(0); }
</style>
"""

_JS = """<script>
(function(){
    const doc = window.parent.document;

    /* Kill keyboard_double_arrow_right and any material icon text nodes */
    function killHeaderJunk(){
        const header = doc.querySelector('[data-testid="stHeader"]');
        if(header){ header.style.display='none'; header.style.height='0'; header.style.overflow='hidden'; }
        doc.querySelectorAll('*').forEach(el=>{
            if(el.children.length === 0){
                const t = el.textContent.trim();
                if(t.startsWith('keyboard_') || t.startsWith('arrow_') || t === 'menu'){
                    el.style.display = 'none';
                    if(el.parentElement) el.parentElement.style.display = 'none';
                }
            }
        });
    }

    /* ── Nav tab strip — borderless underline style ── */
    const NAV_LABELS = ['Dashboard','Outlet Performance','Whitespace Detection','Expansion Strategy'];
    function styleNavTabs(){
        const marker = doc.getElementById('sh-active-page');
        const active = marker ? marker.getAttribute('data-page') : 'Dashboard';
        const found = [];

        doc.querySelectorAll('button').forEach(btn=>{
            const txt = btn.textContent.trim();
            if(!NAV_LABELS.includes(txt)) return;
            found.push(btn);
            const isActive = txt === active;

            /* Make button look like a bare tab */
            btn.style.setProperty('background','transparent','important');
            btn.style.setProperty('border','none','important');
            btn.style.setProperty('border-radius','0','important');
            btn.style.setProperty('box-shadow','none','important');
            btn.style.setProperty('transform','none','important');
            btn.style.setProperty('padding','10px 18px','important');
            btn.style.setProperty('font-size','14px','important');
            btn.style.setProperty('font-weight', isActive ? '700' : '500','important');
            btn.style.setProperty('color', isActive ? '#0b1936' : '#64748b','important');
            btn.style.setProperty('border-bottom', isActive ? '2px solid #0b1936' : '2px solid transparent','important');
            btn.style.setProperty('transition','color 0.15s, border-color 0.15s','important');
        });

        /* Add bottom border to the tab row container */
        if(found.length > 0){
            let row = found[0].closest('[data-testid="stHorizontalBlock"]');
            if(!row) row = found[0].parentElement?.parentElement?.parentElement?.parentElement;
            if(row && !row.dataset.tabRowDone){
                row.dataset.tabRowDone = '1';
                row.style.setProperty('border-bottom','1px solid #e2e8f0','important');
                row.style.setProperty('margin-bottom','20px','important');
                row.style.setProperty('padding-bottom','0','important');
            }
        }
    }

    /* ── Country pill buttons — navy selected / white unselected ── */
    function styleCountryBtns(){
        const cm = doc.getElementById('sh-active-country');
        const activeCountry = cm ? cm.getAttribute('data-country') : 'Nigeria';

        doc.querySelectorAll('button').forEach(btn=>{
            const txt = btn.textContent.trim();
            if(txt !== 'Nigeria' && txt !== 'Angola') return;
            const sel = txt === activeCountry;
            btn.style.setProperty('border-radius','20px','important');
            btn.style.setProperty('padding','8px 22px','important');
            btn.style.setProperty('font-weight','600','important');
            btn.style.setProperty('font-size','13.5px','important');
            btn.style.setProperty('box-shadow','none','important');
            btn.style.setProperty('transform','none','important');
            btn.style.setProperty('background', sel ? '#0b1936' : '#ffffff','important');
            btn.style.setProperty('color',       sel ? '#ffffff' : '#374151','important');
            btn.style.setProperty('border',      sel ? 'none'   : '1px solid #e2e8f0','important');
        });
    }

    function addSidebarIcons(){ /* nav now rendered via st.markdown — no JS injection needed */ }

    /* Scroll reveal */
    function initReveal(){
        if(!window._shRevObs){
            window._shRevObs = new IntersectionObserver(entries=>{
                entries.forEach((e,i)=>{ if(e.isIntersecting){ setTimeout(()=>e.target.classList.add('visible'),Math.min(i*55,280)); window._shRevObs.unobserve(e.target); } });
            },{threshold:0.05,rootMargin:'0px 0px -20px 0px'});
        }
        doc.querySelectorAll('.sh-kpi,.sh-card,.sh-insight,.sh-banner,.sh-odc').forEach(el=>{
            if(el.dataset.revdone) return; el.dataset.revdone='1';
            el.classList.add('sh-reveal'); window._shRevObs.observe(el);
        });
    }

    function hideNav(){
        const n = doc.querySelector('[data-testid="stSidebarNav"]');
        if(n) n.remove();
    }

    function run(){
        killHeaderJunk(); addSidebarIcons();
        styleNavTabs(); styleCountryBtns();
        initReveal(); hideNav();
    }

    setTimeout(run,150); setTimeout(run,600); setTimeout(run,1400);
    setInterval(run,1200);
})();
</script>"""


def apply_styles(active_page: str = "", active_country: str = ""):
    st.markdown(_CSS, unsafe_allow_html=True)
    markers = ""
    if active_page:
        markers += f'<div id="sh-active-page" data-page="{active_page}" style="display:none;"></div>'
    if active_country:
        markers += f'<div id="sh-active-country" data-country="{active_country}" style="display:none;"></div>'
    if markers:
        st.markdown(markers, unsafe_allow_html=True)
    _stc.html(_JS, height=0)


def _nav_item(href: str, label: str, icon_svg: str, icon_bg: str) -> str:
    """Render one nav link — onclick prevents Streamlit's default _blank behaviour."""
    return f"""
<a href="{href}" target="_self" class="sh-nav-link" data-label="{label}"
   onclick="event.preventDefault();event.stopPropagation();window.location.href='{href}';return false;">
  <span class="sh-nav-icon" style="background:{icon_bg};">{icon_svg}</span>
  <span class="sh-nav-label">{label}</span>
</a>"""

_ICON = {
    'dashboard': '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2.3" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="7" height="7" rx="1.5"/><rect x="14" y="3" width="7" height="7" rx="1.5"/><rect x="3" y="14" width="7" height="7" rx="1.5"/><rect x="14" y="14" width="7" height="7" rx="1.5"/></svg>',
    'command':   '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2.3" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="3"/><path d="M12 1v4M12 19v4M4.22 4.22l2.83 2.83M16.95 16.95l2.83 2.83M1 12h4M19 12h4M4.22 19.78l2.83-2.83M16.95 7.05l2.83-2.83"/></svg>',
    'rfm':       '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2.3" stroke-linecap="round" stroke-linejoin="round"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg>',
    'churn':     '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2.3" stroke-linecap="round" stroke-linejoin="round"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>',
    'revenue':   '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2.3" stroke-linecap="round" stroke-linejoin="round"><polyline points="23 6 13.5 15.5 8.5 10.5 1 18"/><polyline points="17 6 23 6 23 12"/></svg>',
    'upload':    '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2.3" stroke-linecap="round" stroke-linejoin="round"><polyline points="16 16 12 12 8 16"/><line x1="12" y1="12" x2="12" y2="21"/><path d="M20.39 18.39A5 5 0 0 0 18 9h-1.26A8 8 0 1 0 3 16.3"/></svg>',
}

_NAV_CSS = """
<style>
/* ── Custom sidebar nav ── */
.sh-nav-brand {
    padding: 18px 14px 14px;
    border-bottom: 1px solid rgba(255,255,255,0.07);
    margin-bottom: 6px;
}
.sh-nav-brand-sub {
    font-size: 9.5px; font-weight: 700; letter-spacing: 0.12em;
    text-transform: uppercase; color: rgba(255,255,255,0.28);
}
.sh-nav-brand-title {
    font-size: 13.5px; font-weight: 700;
    color: rgba(255,255,255,0.85); margin-top: 3px; letter-spacing: -0.2px;
}
.sh-nav-links { padding: 4px 8px; }
.sh-nav-link {
    display: flex !important; align-items: center !important; gap: 12px !important;
    padding: 9px 10px !important; border-radius: 10px !important;
    margin-bottom: 2px !important; text-decoration: none !important;
    transition: background 0.14s !important; cursor: pointer !important;
    border-left: 3px solid transparent !important;
}
.sh-nav-link:hover { background: rgba(255,255,255,0.07) !important; }
.sh-nav-link:hover .sh-nav-label { color: #ffffff !important; }
.sh-nav-icon {
    width: 34px !important; height: 34px !important; border-radius: 50% !important;
    display: flex !important; align-items: center !important; justify-content: center !important;
    flex-shrink: 0 !important;
}
.sh-nav-label {
    font-size: 13.5px !important; font-weight: 500 !important;
    color: rgba(255,255,255,0.60) !important; white-space: nowrap !important;
    font-family: 'Inter', sans-serif !important;
}
/* Active state injected by JS below */
.sh-nav-link.sh-active {
    background: rgba(255,255,255,0.09) !important;
    border-left: 3px solid #635bff !important;
    padding-left: 7px !important;
}
.sh-nav-link.sh-active .sh-nav-label {
    color: #ffffff !important; font-weight: 700 !important;
}
</style>
"""

_NAV_ACTIVE_JS = """
<script>
(function(){
    var path = window.location.pathname.replace(/\\/+$/, '') || '/';
    var links = document.querySelectorAll('.sh-nav-link');
    links.forEach(function(a){
        var lp = a.getAttribute('href').replace(/\\/+$/, '') || '/';
        if(lp === path) a.classList.add('sh-active');
    });
})();
</script>
"""


def sidebar_nav(refresh_key: str = "refresh_data"):
    with st.sidebar:
        st.markdown(_NAV_CSS + """
<div class="sh-nav-brand">
  <div class="sh-nav-brand-sub">Shalina Healthcare</div>
  <div class="sh-nav-brand-title">Distribution Intelligence</div>
</div>
<div class="sh-nav-links">
""" + _nav_item("/",                 "Dashboard",        _ICON['dashboard'], "#f97316")
  + _nav_item("/Command_Center",     "Command Center",   _ICON['command'],   "#635bff")
  + _nav_item("/RFM_Analysis",       "RFM Analysis",     _ICON['rfm'],       "#ec4899")
  + _nav_item("/Churn_Prediction",   "Churn Prediction", _ICON['churn'],     "#f59e0b")
  + _nav_item("/Revenue_Forecast",   "Revenue Forecast", _ICON['revenue'],   "#10b981")
  + _nav_item("/Upload_Data",        "Upload Data",      _ICON['upload'],    "#06b6d4")
  + "</div>" + _NAV_ACTIVE_JS, unsafe_allow_html=True)

        st.markdown('<div class="sh-sidebar-divider"></div>', unsafe_allow_html=True)
        st.markdown('<span class="sh-sidebar-label">Data</span>', unsafe_allow_html=True)

        if st.button("⟳  Refresh Data", use_container_width=True, key=refresh_key):
            st.cache_data.clear()
            st.rerun()
