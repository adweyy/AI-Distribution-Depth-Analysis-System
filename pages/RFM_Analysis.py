import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import os, sys

# Ensure root project directory is on path so fabric_connector can be found
# Works both locally (pages/ subfolder) and on Streamlit Cloud
_here = os.path.dirname(os.path.abspath(__file__))          # .../pages/
_root = os.path.dirname(_here)                               # .../project root/
if _root not in sys.path:
    sys.path.insert(0, _root)
if _here not in sys.path:
    sys.path.insert(0, _here)

st.set_page_config(layout="wide", page_title="RFM Analysis | Shalina", initial_sidebar_state="expanded")

# ── SIDEBAR ───────────────────────────────────────────────────
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
    if st.button("🔄  Refresh Data", use_container_width=True, key="rfm_refresh"):
        st.cache_data.clear()
        st.rerun()
    import streamlit.components.v1 as _sc
    _sc.html("""<script>(function(){function r(){var n=window.parent.document.querySelector('[data-testid="stSidebarNav"]');if(n){n.remove();}else{setTimeout(r,200);}}r();setTimeout(r,800);setTimeout(r,2500);})();</script>""", height=0)

# ── STYLES ────────────────────────────────────────────────────
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
.header-wrap { background:rgba(10,30,60,0.7); border-radius:16px; padding:20px 28px; border:1px solid rgba(33,150,196,0.25); box-shadow:0 4px 24px rgba(0,0,0,0.3); backdrop-filter:blur(20px); margin-bottom:18px; }
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
.insight-card { background:rgba(10,30,60,0.7); border-radius:14px; padding:16px 20px; border:1px solid rgba(33,150,196,0.15); margin-bottom:10px; box-shadow:0 2px 16px rgba(0,0,0,0.2); backdrop-filter:blur(10px); }
.insight-title { font-size:14px; font-weight:700; color:#FFFFFF; font-family:'Poppins',sans-serif; margin-bottom:4px; }
.insight-detail { font-size:12px; color:#90B8D0; line-height:1.6; }
[data-baseweb="select"] > div { background:rgba(10,30,60,0.8) !important; border:1px solid rgba(33,150,196,0.3) !important; border-radius:10px !important; color:#E0F0FF !important; }
[data-baseweb="select"] svg { fill:#6EC6F5 !important; }
[data-baseweb="popover"] { background:#0B2A50 !important; border:1px solid rgba(33,150,196,0.25) !important; }
[role="option"] { background:#0B2A50 !important; color:#E0F0FF !important; }
[role="option"]:hover { background:rgba(33,150,196,0.2) !important; }
[data-testid="stDataFrame"] { border-radius:12px !important; border:1px solid rgba(33,150,196,0.2) !important; }
.stDownloadButton > button { background:linear-gradient(135deg,#0D3B6E,#1A7FC4) !important; color:white !important; border:none !important; border-radius:8px !important; font-weight:600 !important; padding:10px 24px !important; }
.country-btn { display:inline-block; padding:8px 28px; border-radius:30px; font-size:14px; font-weight:700; font-family:'Poppins',sans-serif; cursor:pointer; transition:all 0.2s; border:2px solid rgba(33,150,196,0.4); background:rgba(10,30,60,0.6); color:#90C8E8; margin-right:10px; }
div[data-testid="stHorizontalBlock"] div[data-testid="column"] .stButton > button { background:rgba(255,255,255,0.06) !important; color:#C8E8FF !important; border:1px solid rgba(255,255,255,0.12) !important; border-radius:8px !important; font-weight:600 !important; font-size:14px !important; width:100% !important; transition:all 0.2s ease !important; }
</style>
""", unsafe_allow_html=True)

# ── LOAD DATA ─────────────────────────────────────────────────
from fabric_connector import load_data as _load_data, load_rfm_data as _load_rfm
import streamlit.components.v1 as _fx_c
_fx_c.html("""<script>
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

            /* ── ELASTIC BUTTON ── */

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

    // ── 3D TILT + SPOTLIGHT on KPI cards ─────────────────────────────
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

    // ── REVEAL ON SCROLL ──────────────────────────────────────────────
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

    // ── NAVBAR HIDE ───────────────────────────────────────────────────
    function hideNav() {
        const nav = doc.querySelector('[data-testid="stSidebarNav"]');
        if (nav) nav.remove();
    }

    // ── PERSISTENT RE-INJECTION ───────────────────────────────────────
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
    }

    function lightRefresh() {
        // Only re-apply interactive effects to newly rendered elements
        // (particles/orbs persist on body so no need to re-add)
        try { addMagneticButtons(); } catch(e) {}
        try { addTiltCards(); }       catch(e) {}
        try { addRevealOnScroll(); }  catch(e) {}
        try { hideNav(); }            catch(e) {}

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

df_all, _, _ = _load_data()

if df_all is None:
    st.error("No data available. Please check Fabric connection or add shalina_combined_data.csv.")
    st.stop()

# ── HEADER ────────────────────────────────────────────────────
col1, col2 = st.columns([1, 9])
with col1:
    if os.path.exists(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "shalina_healthcare_logo.png")):
        st.image(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "shalina_healthcare_logo.png"), width=110)
with col2:
    st.markdown("""
    <div class="header-wrap">
        <div style="font-family:'DM Sans',sans-serif;font-size:11px;font-weight:600;color:#90C8E8;letter-spacing:2px;text-transform:uppercase;margin-bottom:4px;">Shalina Healthcare</div>
        <div style="font-family:'Poppins',sans-serif;font-size:32px;font-weight:700;color:#FFFFFF;letter-spacing:-0.5px;line-height:1.1;">RFM Analysis</div>
        <div style="font-family:'DM Sans',sans-serif;font-size:13px;color:#7AACCC;margin-top:4px;">Outlet segmentation by Recency · Frequency · Monetary value</div>
    </div>
    """, unsafe_allow_html=True)

# ── COUNTRY SWITCHER ──────────────────────────────────────────
if "rfm_country" not in st.session_state:
    st.session_state.rfm_country = "Nigeria"

st.markdown("<div style='margin:12px 0 6px 0;font-family:Poppins,sans-serif;font-size:10px;font-weight:700;color:#90C8E8;text-transform:uppercase;letter-spacing:1.5px;'>Select Country</div>", unsafe_allow_html=True)
cc1, cc2, cc3 = st.columns([1, 1, 8])
with cc1:
    if st.button("🇳🇬  Nigeria", use_container_width=True, key="rfm_ng"):
        st.session_state.rfm_country = "Nigeria"
with cc2:
    if st.button("🇦🇴  Angola", use_container_width=True, key="rfm_ao"):
        st.session_state.rfm_country = "Angola"

country = st.session_state.rfm_country
df = df_all[df_all['country'] == country].copy()

accent = "#4CAF50" if country == "Nigeria" else "#CE93D8"
st.markdown(f"<div style='height:3px;background:linear-gradient(90deg,{accent},transparent);border-radius:2px;margin-bottom:16px;'></div>", unsafe_allow_html=True)

chart_layout = dict(
    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(10,30,60,0.5)",
    font=dict(color="#90C8E8", size=11), height=380,
    xaxis=dict(gridcolor="rgba(33,150,196,0.1)", linecolor="rgba(33,150,196,0.2)", color="#6AACE0"),
    yaxis=dict(gridcolor="rgba(33,150,196,0.1)", linecolor="rgba(33,150,196,0.2)", color="#6AACE0"),
    margin=dict(l=0, r=0, t=20, b=0),
    legend=dict(font=dict(color="#FFFFFF"), bgcolor="rgba(10,30,60,0.7)")
)

# ── TRY REAL SFA TRANSACTION DATA ────────────────────────────
sfa_df, sfa_status = _load_rfm(country)
using_real_rfm = sfa_df is not None and len(sfa_df) > 0

rfm = df.copy()

if using_real_rfm:
    sfa_df['Shop Name'] = sfa_df['Shop Name'].astype(str).str.strip()
    rfm['Shop Name']    = rfm['Shop Name'].astype(str).str.strip()
    rfm = rfm.merge(sfa_df[['Shop Name','last_order_date','order_count','total_spend']],
                    on='Shop Name', how='left')
    rfm['order_count']     = rfm['order_count'].fillna(0)
    rfm['total_spend']     = rfm['total_spend'].fillna(0)
    rfm['last_order_date'] = pd.to_datetime(rfm['last_order_date'], errors='coerce')

    today = pd.Timestamp.today()
    rfm['recency_days'] = (today - rfm['last_order_date']).dt.days.fillna(9999)

    r_max = rfm[rfm['recency_days'] < 9999]['recency_days']
    r_q20, r_q40, r_q60, r_q80 = (r_max.quantile(q) if len(r_max) else 0 for q in [.20,.40,.60,.80])

    def r_score_real(d):
        if d >= 9999:     return 1
        elif d <= r_q20:  return 5
        elif d <= r_q40:  return 4
        elif d <= r_q60:  return 3
        elif d <= r_q80:  return 2
        else:             return 1

    f_vals = rfm[rfm['order_count'] > 0]['order_count']
    f_q20, f_q40, f_q60, f_q80 = (f_vals.quantile(q) if len(f_vals) else 0 for q in [.20,.40,.60,.80])

    def f_score_real(c):
        if c == 0:        return 1
        elif c <= f_q20:  return 2
        elif c <= f_q40:  return 3
        elif c <= f_q60:  return 4
        elif c <= f_q80:  return 4
        else:             return 5

    m_vals = rfm[rfm['total_spend'] > 0]['total_spend']
    m_q20, m_q40, m_q60, m_q80 = (m_vals.quantile(q) if len(m_vals) else 0 for q in [.20,.40,.60,.80])

    def m_score_real(v):
        if v == 0:        return 1
        elif v <= m_q20:  return 2
        elif v <= m_q40:  return 3
        elif v <= m_q60:  return 4
        elif v <= m_q80:  return 4
        else:             return 5

    rfm['R'] = rfm['recency_days'].apply(r_score_real)
    rfm['F'] = rfm['order_count'].apply(f_score_real)
    rfm['M'] = rfm['total_spend'].apply(m_score_real)
    rfm['M_raw'] = rfm['total_spend']

    rfm_mode_label = "🟢  Real RFM — SFA Transaction Data (Recency · Frequency · Monetary)"
    rfm_mode_color = "#4CAF50"
    rfm_mode_sub   = (f"Based on {len(sfa_df):,} outlet transaction records · "
                      f"R = days since last order · F = order count · M = total spend")
else:
    rfm['M_raw'] = rfm['YTD Retailing Value']
    active_vals  = rfm[rfm['M_raw'] > 0]['M_raw']
    q20, q40, q60, q80 = (active_vals.quantile(q) if len(active_vals) >= 5 else 0 for q in [.20,.40,.60,.80])

    def m_score(v):
        if v == 0:      return 1
        elif v <= q20:  return 2
        elif v <= q40:  return 3
        elif v <= q60:  return 4
        elif v <= q80:  return 4
        else:           return 5

    def r_score(v):
        if v == 0:      return 1
        elif v <= q20:  return 2
        elif v <= q40:  return 3
        elif v <= q60:  return 4
        else:           return 5

    def f_score(row):
        subtype = str(row['Retailer Subtype']).lower()
        m = row['M']
        if 'primary' in subtype:    return min(5, m + 1)
        elif 'secondary' in subtype: return m
        else:                        return max(1, m - 1)

    rfm['M'] = rfm['M_raw'].apply(m_score)
    rfm['R'] = rfm['M_raw'].apply(r_score)
    rfm['F'] = rfm.apply(f_score, axis=1)

    rfm_mode_label = "🟡  Proxy RFM — YTD Sales Value (SFA data not yet available)"
    rfm_mode_color = "#F9A825"
    rfm_mode_sub   = ("R & M derived from YTD Retailing Value · F estimated from outlet type · "
                      "Activate real RFM: grant admin consent in Azure AD for Shalina-Whitespace-App")

# ── MODE BANNER ───────────────────────────────────────────────
st.markdown(f"""
<div style="background:rgba(10,30,60,0.7);border:1px solid {rfm_mode_color};border-radius:14px;
padding:16px 22px;margin-bottom:20px;backdrop-filter:blur(10px);">
    <div style="font-family:'Poppins',sans-serif;font-size:14px;font-weight:700;
    color:{rfm_mode_color};margin-bottom:5px;">{rfm_mode_label}</div>
    <div style="font-size:12px;color:#90B8D0;line-height:1.7;">{rfm_mode_sub}</div>
    <div style="margin-top:10px;font-size:12px;color:#90B8D0;line-height:1.7;">
        <strong style="color:#6EC6F5;">R — Recency</strong> &nbsp;|&nbsp;
        <strong style="color:#A855F7;">F — Frequency</strong> &nbsp;|&nbsp;
        <strong style="color:#F9A825;">M — Monetary</strong>
        &nbsp;&nbsp;Each scored 1 (worst) → 5 (best). RFM Total = R + F + M (max 15).
    </div>
</div>
""", unsafe_allow_html=True)

# ── SEGMENTATION ──────────────────────────────────────────────
rfm['RFM_Score'] = rfm['R'] + rfm['F'] + rfm['M']

def rfm_segment(row):
    r, f, m = row['R'], row['F'], row['M']
    total   = r + f + m
    if r >= 4 and f >= 4 and m >= 4:    return 'Champions'
    elif r >= 3 and f >= 3 and m >= 3:  return 'Loyal Customers'
    elif r >= 3 and f <= 2:             return 'Promising'
    elif r <= 2 and f >= 3 and m >= 3:  return 'At Risk'
    elif r >= 2 and f >= 2 and m <= 2:  return 'Need Attention'
    elif r == 1 and f == 1 and m == 1:  return 'Lost'
    elif total <= 5:                     return 'Hibernating'
    else:                                return 'Potential Loyalist'

rfm['Segment'] = rfm.apply(rfm_segment, axis=1)

seg_colors = {
    'Champions':         '#A855F7',
    'Loyal Customers':   '#22C55E',
    'Promising':         '#6EC6F5',
    'Potential Loyalist':'#F9A825',
    'Need Attention':    '#F97316',
    'At Risk':           '#EF4444',
    'Hibernating':       '#64748B',
    'Lost':              '#1E293B',
}

seg_actions = {
    'Champions':         'Reward & retain — top priority for new product launches.',
    'Loyal Customers':   'Upsell and cross-sell. Ask for referrals to nearby outlets.',
    'Promising':         'Activate with promotions. Build engagement and habits.',
    'Potential Loyalist':'Offer loyalty programmes and targeted incentives.',
    'Need Attention':    'Reactivate with special offers. Reach out before they go cold.',
    'At Risk':           'Urgent outreach needed — at risk of becoming Lost.',
    'Hibernating':       'Low-cost re-engagement campaign. Check if outlet still open.',
    'Lost':              'Confirm outlet status. Consider reassigning territory.',
}

seg_counts = rfm['Segment'].value_counts()

# ── KPI ROW ───────────────────────────────────────────────────
champs = seg_counts.get('Champions', 0)
loyal  = seg_counts.get('Loyal Customers', 0)
at_risk= seg_counts.get('At Risk', 0)
lost   = seg_counts.get('Lost', 0)

st.markdown(f"""
<div class="kpi-row">
    <div class="kpi-card purple">
        <div class="kpi-label">Champions</div>
        <div class="kpi-value">{champs:,}</div>
        <div class="kpi-delta">RFM score ≥ 12 — top accounts</div>
    </div>
    <div class="kpi-card green">
        <div class="kpi-label">Loyal Customers</div>
        <div class="kpi-value">{loyal:,}</div>
        <div class="kpi-delta">Consistent high-value outlets</div>
    </div>
    <div class="kpi-card gold">
        <div class="kpi-label">At Risk</div>
        <div class="kpi-value">{at_risk:,}</div>
        <div class="kpi-delta">Were good — need urgent outreach</div>
    </div>
    <div class="kpi-card red">
        <div class="kpi-label">Lost</div>
        <div class="kpi-value">{lost:,}</div>
        <div class="kpi-delta">Zero engagement — reassess</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── CHARTS ────────────────────────────────────────────────────
c1, c2 = st.columns([3, 2])
with c1:
    st.markdown('<div class="section-title">Segment Distribution</div>', unsafe_allow_html=True)
    seg_df = seg_counts.reset_index()
    seg_df.columns = ['Segment', 'Count']
    fig_seg = px.bar(seg_df, x='Count', y='Segment', orientation='h',
                     color='Segment', color_discrete_map=seg_colors, text='Count')
    fig_seg.update_traces(textposition='outside', textfont=dict(color='#FFFFFF', size=11))
    fig_seg.update_layout(**chart_layout)
    st.plotly_chart(fig_seg, use_container_width=True)

with c2:
    st.markdown('<div class="section-title">Avg Monetary by Segment</div>', unsafe_allow_html=True)
    avg_m = rfm[rfm['M_raw'] > 0].groupby('Segment')['M_raw'].mean().reset_index()
    avg_m.columns = ['Segment', 'Avg Value']
    avg_m = avg_m.sort_values('Avg Value', ascending=False)
    fig_avg = px.bar(avg_m, x='Segment', y='Avg Value',
                     color='Segment', color_discrete_map=seg_colors)
    fig_avg.update_layout(**chart_layout)
    fig_avg.update_xaxes(tickangle=45)
    st.plotly_chart(fig_avg, use_container_width=True)

# ── RFM SCATTER ───────────────────────────────────────────────
st.markdown('<div class="section-title">RFM Score Map — Recency vs Monetary</div>', unsafe_allow_html=True)
jitter_df = rfm.copy()
jitter_df['R_j'] = jitter_df['R'] + np.random.uniform(-0.3, 0.3, len(jitter_df))
jitter_df['M_j'] = jitter_df['M'] + np.random.uniform(-0.3, 0.3, len(jitter_df))
sample_rfm = jitter_df.sample(min(4000, len(jitter_df)), random_state=42)

fig_scatter = px.scatter(
    sample_rfm, x='R_j', y='M_j',
    color='Segment', color_discrete_map=seg_colors,
    hover_name='Shop Name',
    hover_data={'R': True, 'F': True, 'M': True, 'RFM_Score': True, 'R_j': False, 'M_j': False},
    labels={'R_j': 'Recency Score', 'M_j': 'Monetary Score'},
)
fig_scatter.update_traces(marker=dict(size=7, opacity=0.75, line=dict(width=0)))
fig_scatter.update_layout(
    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(10,30,60,0.5)",
    font=dict(color="#90C8E8", size=11), height=440,
    margin=dict(l=0, r=0, t=20, b=0),
    legend=dict(font=dict(color="#FFFFFF"), bgcolor="rgba(10,30,60,0.7)"),
    xaxis=dict(title='Recency Score (1=inactive → 5=most recent)', tickvals=[1,2,3,4,5],
               gridcolor='rgba(33,150,196,0.1)', linecolor='rgba(33,150,196,0.2)', color='#6AACE0'),
    yaxis=dict(title='Monetary Score (1=zero → 5=top spender)', tickvals=[1,2,3,4,5],
               gridcolor='rgba(33,150,196,0.1)', linecolor='rgba(33,150,196,0.2)', color='#6AACE0'),
)
st.plotly_chart(fig_scatter, use_container_width=True)

# ── ACTION PLAYBOOK ───────────────────────────────────────────
st.markdown('<div class="section-title">Segment Action Playbook</div>', unsafe_allow_html=True)
action_cols = st.columns(2)
for i, (seg, action) in enumerate(seg_actions.items()):
    count = seg_counts.get(seg, 0)
    color = seg_colors.get(seg, '#2196C4')
    with action_cols[i % 2]:
        st.markdown(f"""
        <div class="insight-card" style="border-left:4px solid {color};margin-bottom:10px;">
            <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:5px;">
                <div class="insight-title" style="color:{color};">{seg}</div>
                <div style="font-family:'Poppins',sans-serif;font-size:18px;font-weight:700;color:#FFFFFF;">{count:,}</div>
            </div>
            <div class="insight-detail">{action}</div>
        </div>
        """, unsafe_allow_html=True)

# ── OUTLET TABLE ──────────────────────────────────────────────
st.markdown('<div class="section-title">Full Outlet RFM Table</div>', unsafe_allow_html=True)
seg_filter = st.selectbox("Filter by Segment", ["All"] + sorted(rfm['Segment'].unique().tolist()), key="rfm_seg_filter")
rfm_show = rfm if seg_filter == "All" else rfm[rfm['Segment'] == seg_filter]

if using_real_rfm:
    rfm_table = rfm_show[['Shop Name','Retailer Subtype','R','F','M','RFM_Score','Segment',
                           'recency_days','order_count','total_spend']].copy()
    rfm_table = rfm_table.rename(columns={
        'recency_days': 'Days Since Last Order',
        'order_count':  'Order Count',
        'total_spend':  'Total Spend'
    })
    rfm_table['Total Spend'] = rfm_table['Total Spend'].apply(lambda x: f"₦{x:,.1f}K")
else:
    rfm_table = rfm_show[['Shop Name','Retailer Subtype','R','F','M','RFM_Score','Segment','YTD Retailing Value']].copy()
    rfm_table['YTD Retailing Value'] = rfm_table['YTD Retailing Value'].apply(lambda x: f"₦{x:,.1f}K")

rfm_table = rfm_table.sort_values('RFM_Score', ascending=False).reset_index(drop=True)
rfm_table.index += 1
st.dataframe(rfm_table, use_container_width=True)

csv_rfm = rfm_table.to_csv().encode('utf-8')
st.download_button("⬇️ Export RFM Scores", csv_rfm,
                   f"rfm_analysis_{country.lower()}.csv", "text/csv", key="rfm_export")