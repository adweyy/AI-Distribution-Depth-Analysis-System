import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import numpy as np
import os, sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

st.set_page_config(layout="wide", page_title="Upload Data | Shalina")
st.markdown("""
<style>
[data-testid="stSidebarNav"],
[data-testid="stSidebarNavItems"],
section[data-testid="stSidebar"] nav,
ul[data-testid="stSidebarNavItems"] { display: none !important; visibility: hidden !important; }
</style>
""", unsafe_allow_html=True)
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

#  SIDEBAR 
with st.sidebar:
    st.markdown("""
    <div style="padding:20px 8px 10px 8px;">
        <div style="font-family:'Poppins',sans-serif;font-size:10px;font-weight:700;
        color:rgba(100,180,220,0.7);text-transform:uppercase;letter-spacing:2px;margin-bottom:20px;">
            Navigation
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.page_link("app.py",                   label="Dashboard")
    st.page_link("pages/RFM_Analysis.py",   label="RFM Analysis")
    st.page_link("pages/Upload_Data.py",    label="Upload Data")
    st.markdown("""<div style="margin-top:16px;padding:0 8px;">
        <div style="height:1px;background:linear-gradient(90deg,transparent,rgba(33,150,196,0.35),transparent);"></div>
    </div>""", unsafe_allow_html=True)
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

#  HEADER 
st.markdown("""
<div class="mc-topbar">
    <div class="mc-title-wrap">
        <div class="mc-eyebrow">Shalina Healthcare &nbsp;·&nbsp; Distribution Intelligence Platform</div>
        <div class="mc-title">Data <span>Upload</span> Portal</div>
    </div>
    <div class="mc-status-group">
        <div class="mc-status-pill">
            <div class="mc-status-dot"></div>
            SYS: ONLINE
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("<div style='margin-top:10px;'></div>", unsafe_allow_html=True)

REQUIRED_COLUMNS = [
    "Shop Name", "latitude", "longitude",
    "Retailer Subtype", "YTD Retailing Value"
]

COL_INFO = [
    ("Shop Name",           "Text",    "Name of the outlet/pharmacy/store",       "e.g. CJ Pharmacy"),
    ("latitude",            "Float",   "GPS latitude of the outlet",              "e.g. 6.52"),
    ("longitude",           "Float",   "GPS longitude of the outlet",             "e.g. 3.38"),
    ("Retailer Subtype",    "Text",    "Primary or Secondary retailer",           "Primary / Secondary"),
    ("YTD Retailing Value", "Float",   "Year-to-date sales value in thousands",   "e.g. 245.5"),
]

template_df = pd.DataFrame({
    "Shop Name": ["CJ Pharmacy","Emeka Stores","Rahama Store"],
    "latitude": [10.067579, 10.022158, 10.133068],
    "longitude": [6.185902, 8.850164, 12.729449],
    "Retailer Subtype": ["Secondary","Secondary","Primary"],
    "YTD Retailing Value": [795.42, 214.37, 0.0],
})
template_csv = template_df.to_csv(index=False).encode("utf-8")

#  STATUS BANNER 
if "uploaded_data" in st.session_state:
    source = st.session_state.get("data_source", "uploaded file")
    st.markdown(f'<div class="status-success"><span style="font-size:18px;"></span> Dashboard is currently using: <b>{source}</b></div>', unsafe_allow_html=True)
else:
    st.markdown('<div class="status-warn">Dashboard is running on demo data. Upload your CSV below to analyse real data.</div>', unsafe_allow_html=True)

#  STEP 1 
st.markdown('<div class="section-title">Step 1 — Download the Data Template</div>', unsafe_allow_html=True)
st.markdown("""
<div style="background:white;border-radius:12px;padding:16px 20px;border:1px solid rgba(11,46,89,0.08);
box-shadow:0 2px 8px rgba(11,46,89,0.04);margin-bottom:12px;font-size:13px;color:#5B8DB8;line-height:1.7;">
Download the template, fill it with your real data from Fabric, then upload in Step 2.<br>
<b style="color:#0B2E59;">Do not rename or remove any columns</b> — the model requires all 14 columns.
</div>
""", unsafe_allow_html=True)

dl1, _ = st.columns([2, 8])
with dl1:
    st.download_button("Download CSV Template", data=template_csv,
        file_name="shalina_distribution_template.csv", mime="text/csv")

with st.expander("View all 5 column descriptions"):
    for col_name, col_type, col_desc, col_example in COL_INFO:
        st.markdown(f"""
        <div class="col-card">
            <div class="col-name">{col_name}</div>
            <span class="col-type">{col_type}</span>
            <div class="col-desc">{col_desc}</div>
            <div class="col-example">{col_example}</div>
        </div>
        """, unsafe_allow_html=True)

#  STEP 2 — UPLOADER (no HTML box above it) 
st.markdown('<div class="section-title">Step 2 — Upload Your CSV File</div>', unsafe_allow_html=True)

# The native uploader IS the drop target — nothing sits on top of it
uploaded_file = st.file_uploader(
    "Upload CSV", type=["csv"], label_visibility="collapsed"
)

#  PARALLAX JS via components.html (executes reliably unlike st.markdown) 
components.html("""
<script>
(function() {
    function attachParallax() {
        // Walk up into the parent window from the iframe
        const doc = window.parent.document;
        const zone = doc.querySelector('[data-testid="stFileUploaderDropzone"]');
        if (!zone) { setTimeout(attachParallax, 600); return; }

        zone.addEventListener('mousemove', function(e) {
            const rect = zone.getBoundingClientRect();
            const cx = rect.left + rect.width  / 2;
            const cy = rect.top  + rect.height / 2;
            const dx = (e.clientX - cx) / (rect.width  / 2);  // -1 to 1
            const dy = (e.clientY - cy) / (rect.height / 2);  // -1 to 1
            zone.style.transition = 'transform 0.08s ease, box-shadow 0.2s ease';
            zone.style.transform  = `perspective(900px) rotateX(${-dy * 6}deg) rotateY(${dx * 6}deg) translateY(-5px) scale(1.01)`;
            zone.style.boxShadow  = `${dx * -12}px ${dy * -12}px 40px rgba(33,150,196,0.15), 0 20px 60px rgba(11,46,89,0.1)`;
        });

        zone.addEventListener('mouseleave', function() {
            zone.style.transition = 'transform 0.45s ease, box-shadow 0.45s ease';
            zone.style.transform  = 'perspective(900px) rotateX(0deg) rotateY(0deg) translateY(0px) scale(1)';
            zone.style.boxShadow  = '0 8px 40px rgba(11,46,89,0.08)';
        });

        // Highlight on dragover
        zone.addEventListener('dragover', function(e) {
            e.preventDefault();
            zone.style.borderColor  = '#2196C4';
            zone.style.background   = 'linear-gradient(135deg,#e8f4ff,#f0faff)';
            zone.style.transform    = 'perspective(900px) rotateX(2deg) translateY(-6px) scale(1.02)';
            zone.style.boxShadow    = '0 24px 64px rgba(33,150,196,0.22)';
        });

        zone.addEventListener('dragleave', function() {
            zone.style.borderColor  = '#90CAF9';
            zone.style.background   = 'white';
            zone.style.transform    = 'perspective(900px) rotateX(0deg) translateY(0px) scale(1)';
            zone.style.boxShadow    = '0 8px 40px rgba(11,46,89,0.08)';
        });
    }
    attachParallax();
})();
</script>
""", height=0)

#  PROCESS UPLOAD 
if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
        missing_cols = [c for c in REQUIRED_COLUMNS if c not in df.columns]

        if missing_cols:
            st.markdown(f'<div class="status-error">Missing columns: <b>{", ".join(missing_cols)}</b><br>Check your CSV matches the template.</div>', unsafe_allow_html=True)
        else:
            df = df.dropna(subset=["latitude","longitude"])
            df["latitude"]            = pd.to_numeric(df["latitude"], errors="coerce")
            df["longitude"]           = pd.to_numeric(df["longitude"], errors="coerce")
            df["YTD Retailing Value"] = pd.to_numeric(df["YTD Retailing Value"], errors="coerce").fillna(0)
            df = df.dropna(subset=["latitude","longitude"])

            st.session_state["uploaded_data"] = df
            st.session_state["data_source"]   = uploaded_file.name

            st.markdown(f"""
            <div class="status-success">
                <span style="font-size:20px;"></span>
                <div><b>{uploaded_file.name}</b> uploaded — {len(df):,} rows loaded.<br>
                <span style="font-weight:400;font-size:12px;">Click below to go to the Dashboard.</span></div>
            </div>
            """, unsafe_allow_html=True)

            if st.button("Go to Dashboard →", key="go_dash"):
                st.switch_page("app.py")

            st.markdown('<div class="section-title">Data Summary</div>', unsafe_allow_html=True)
            s1, s2, s3, s4 = st.columns(4)
            s1.metric("Total Outlets",   f"{len(df):,}")
            s2.metric("Primary Outlets", f"{len(df[df['Retailer Subtype']=='Primary']):,}")
            s3.metric("Secondary Outlets", f"{len(df[df['Retailer Subtype']=='Secondary']):,}")
            s4.metric("Active Outlets",  f"{len(df[df['YTD Retailing Value']>0]):,}")

            st.markdown('<div class="section-title">Preview (first 20 rows)</div>', unsafe_allow_html=True)
            st.dataframe(df.head(20), use_container_width=True, hide_index=True)

    except Exception as e:
        st.markdown(f'<div class="status-error">Could not read file: <b>{str(e)}</b></div>', unsafe_allow_html=True)

#  RESET 
if "uploaded_data" in st.session_state:
    st.markdown("<div style='margin-top:24px;'></div>", unsafe_allow_html=True)
    st.markdown('<div class="section-title">Reset</div>', unsafe_allow_html=True)
    st.markdown('<div style="font-size:13px;color:#5B8DB8;margin-bottom:10px;">Clear your uploaded data and revert to demo.</div>', unsafe_allow_html=True)
    if st.button("Clear uploaded data — revert to demo", key="clear_data"):
        for key in ["uploaded_data","data_source","default_year","default_channel","default_brand","default_region"]:
            if key in st.session_state:
                del st.session_state[key]
        st.rerun()