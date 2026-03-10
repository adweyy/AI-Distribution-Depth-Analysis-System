import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import numpy as np
import os

st.set_page_config(layout="wide", page_title="Upload Data | Shalina")

# ── SIDEBAR ──────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="padding:20px 8px 10px 8px;">
        <div style="font-family:'Poppins',sans-serif;font-size:10px;font-weight:700;
        color:rgba(100,180,220,0.7);text-transform:uppercase;letter-spacing:2px;margin-bottom:20px;">
            Navigation
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.page_link("app.py",                  label="🏠  Dashboard")
    st.page_link("pages/ROI_Calculator.py", label="📊  ROI Calculator")
    st.page_link("pages/Upload_Data.py",    label="☁️  Upload Data")
    st.markdown("""<div style="margin-top:16px;padding:0 8px;">
        <div style="height:1px;background:linear-gradient(90deg,transparent,rgba(33,150,196,0.35),transparent);"></div>
    </div>""", unsafe_allow_html=True)
    import streamlit.components.v1 as _sc
    _sc.html("""<script>(function(){function r(){var n=window.parent.document.querySelector('[data-testid="stSidebarNav"]');if(n){n.remove();}else{setTimeout(r,200);}}r();setTimeout(r,800);setTimeout(r,2500);})();</script>""", height=0)


st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&family=DM+Sans:wght@400;500;600&display=swap');
* { box-sizing: border-box; }
.stApp {
    font-family: 'DM Sans', sans-serif; color: #E0F0FF;
    background: linear-gradient(145deg, #071830 0%, #0B2A50 40%, #0A2040 70%, #071830 100%);
    min-height: 100vh; position: relative;
}
.stApp::before {
    content: ''; position: fixed; inset: 0;
    background:
        radial-gradient(ellipse 90% 50% at 15% 0%, rgba(0,100,200,0.25) 0%, transparent 55%),
        radial-gradient(ellipse 60% 40% at 85% 15%, rgba(0,150,220,0.15) 0%, transparent 50%),
        radial-gradient(ellipse 70% 60% at 50% 100%, rgba(0,60,140,0.20) 0%, transparent 55%);
    pointer-events: none; z-index: 0;
}
.main .block-container { background: transparent; padding-top: 0rem; max-width: 1400px; padding-left: 2rem; padding-right: 2rem; position: relative; z-index: 1; }
section[data-testid="stSidebar"] { background: linear-gradient(180deg, #0B2E59 0%, #0D3B6E 100%) !important; border-right: 1px solid rgba(33,150,196,0.2) !important; }
section[data-testid="stSidebar"] * { color: #B8D4EE !important; font-family: 'DM Sans', sans-serif !important; }
section[data-testid="stSidebar"] [aria-selected="true"] { color: #ffffff !important; background: rgba(255,255,255,0.1) !important; border-radius: 8px !important; }
section[data-testid="stSidebar"] a:hover { color: #ffffff !important; background: rgba(255,255,255,0.08) !important; border-radius: 8px !important; }
[data-testid="collapsedControl"], [data-testid="stSidebarCollapseButton"], button[kind="header"] { display: none !important; }
/* Hide Streamlit auto-generated top nav in sidebar */
[data-testid="stSidebarNav"],
[data-testid="stSidebarNavItems"],
[data-testid="stSidebarNavSeparator"],
section[data-testid="stSidebar"] > div > div > div > ul,
section[data-testid="stSidebar"] nav { display: none !important; visibility: hidden !important; height: 0 !important; overflow: hidden !important; }
[data-testid="stToolbar"], [data-testid="stDecoration"], header[data-testid="stHeader"], #MainMenu, footer { display: none !important; }
.top-header, .header-wrap { background: rgba(10,30,60,0.7); border-radius: 16px; padding: 20px 28px; border: 1px solid rgba(33,150,196,0.25); box-shadow: 0 4px 24px rgba(0,0,0,0.3); backdrop-filter: blur(20px); margin-bottom: 18px; }
.brand-name { font-size: 22px; font-weight: 700; color: #FFFFFF; font-family: 'Poppins', sans-serif; }
.brand-sub  { font-size: 11px; color: #90C8E8; text-transform: uppercase; letter-spacing: 1.5px; margin-top: 3px; }
.section-title { font-size: 12px; font-weight: 700; color: #90C8E8; margin-top: 24px; margin-bottom: 12px; display: flex; align-items: center; gap: 10px; text-transform: uppercase; letter-spacing: 1.2px; }
.section-title::before { content: ''; display: inline-block; width: 4px; height: 14px; background: linear-gradient(180deg, #2196C4, #6EC6F5); border-radius: 2px; box-shadow: 0 0 8px rgba(33,150,196,0.5); }
.kpi-row { display: grid; grid-template-columns: repeat(4, 1fr); gap: 14px; margin-bottom: 22px; }
.kpi-card { border-radius: 14px; padding: 20px 22px; position: relative; overflow: hidden; min-height: 100px; border: 1px solid rgba(255,255,255,0.1); box-shadow: 0 4px 20px rgba(0,0,0,0.3); transition: transform 0.2s ease; }
.kpi-card:hover { transform: translateY(-2px); }
.kpi-card::before { content: ''; position: absolute; bottom: -20px; right: -20px; width: 100px; height: 100px; border-radius: 50%; background: rgba(255,255,255,0.10); }
.kpi-card::after  { content: ''; position: absolute; bottom: -40px; right: 20px; width: 80px; height: 80px; border-radius: 50%; background: rgba(255,255,255,0.06); }
.kpi-card.navy  { background: linear-gradient(135deg, #0B2E59 0%, #1A5276 100%); }
.kpi-card.blue  { background: linear-gradient(135deg, #1A7FC4 0%, #6EC6F5 100%); }
.kpi-card.sky   { background: linear-gradient(135deg, #74C0E8 0%, #B8E4F7 100%); }
.kpi-card.gold, .kpi-card.amber { background: linear-gradient(135deg, #F9A825 0%, #F7D080 100%); }
.kpi-card.green { background: linear-gradient(135deg, #1B8A4E 0%, #4CAF50 100%); }
.kpi-label { font-size: 10px; color: rgba(255,255,255,0.85); text-transform: uppercase; letter-spacing: 1px; margin-bottom: 8px; font-weight: 700; font-family: 'Poppins', sans-serif; }
.kpi-value { font-size: 32px; font-weight: 700; color: #ffffff; line-height: 1.1; font-family: 'Poppins', sans-serif; }
.kpi-delta { font-size: 11px; color: rgba(255,255,255,0.75); margin-top: 5px; }
.stSelectbox label { color: #90C8E8 !important; font-size: 10px !important; font-weight: 700 !important; text-transform: uppercase; }
[data-baseweb="select"] > div { background: rgba(10,30,60,0.8) !important; border: 1px solid rgba(33,150,196,0.3) !important; border-radius: 10px !important; color: #E0F0FF !important; }
[data-baseweb="select"] svg { fill: #6EC6F5 !important; }
[data-baseweb="popover"] { background: #0B2A50 !important; border: 1px solid rgba(33,150,196,0.25) !important; }
[role="option"] { background: #0B2A50 !important; color: #E0F0FF !important; }
[role="option"]:hover { background: rgba(33,150,196,0.2) !important; }
[data-testid="stMetric"] { background: rgba(10,30,60,0.7) !important; border-radius: 12px !important; padding: 16px !important; border: 1px solid rgba(33,150,196,0.2) !important; }
[data-testid="stMetricLabel"] { color: #90C8E8 !important; font-size: 10px !important; font-weight: 700 !important; text-transform: uppercase; }
[data-testid="stMetricValue"] { color: #FFFFFF !important; font-weight: 700 !important; font-family: 'Poppins', sans-serif !important; }
[data-testid="stDataFrame"] { border-radius: 12px !important; border: 1px solid rgba(33,150,196,0.2) !important; }
.stDownloadButton > button, .stButton > button { background: linear-gradient(135deg, #0D3B6E, #1A7FC4) !important; color: white !important; border: none !important; border-radius: 8px !important; font-weight: 600 !important; padding: 10px 24px !important; }
/* Upload zone */
[data-testid="stFileUploaderDropzone"] { background: rgba(10,30,60,0.6) !important; border: 2px dashed rgba(33,150,196,0.5) !important; border-radius: 20px !important; min-height: 320px !important; display: flex !important; align-items: center !important; justify-content: center !important; }
[data-testid="stFileUploaderDropzone"]:hover { border-color: rgba(33,150,196,0.9) !important; background: rgba(10,40,80,0.7) !important; }
[data-testid="stFileUploaderDropzone"] * { color: #90C8E8 !important; }
[data-testid="stFileUploaderDropzone"] > div { padding: 60px 40px !important; text-align: center !important; width: 100% !important; }
[data-testid="stFileUploaderDropzone"] span { font-size: 16px !important; }
[data-testid="stFileUploaderDropzone"] button { font-size: 15px !important; padding: 10px 28px !important; border-radius: 10px !important; }
</style>
""", unsafe_allow_html=True)

# ── HEADER ────────────────────────────────────────────────────────────────────
hcol1, hcol2 = st.columns([1, 9])
with hcol1:
    if os.path.exists("shalina_healthcare_logo.png"):
        st.image("shalina_healthcare_logo.png", width=110)
with hcol2:
    st.markdown("""
    <div style="padding-top:10px;">
        <div style="font-size:20px;font-weight:700;color:#0B2E59;">Shalina Healthcare</div>
        <div style="font-size:11px;color:#5B8DB8;text-transform:uppercase;letter-spacing:1px;">Data Upload Portal</div>
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

# ── STATUS BANNER ─────────────────────────────────────────────────────────────
if "uploaded_data" in st.session_state:
    source = st.session_state.get("data_source", "uploaded file")
    st.markdown(f'<div class="status-success"><span style="font-size:18px;">✓</span> Dashboard is currently using: <b>{source}</b></div>', unsafe_allow_html=True)
else:
    st.markdown('<div class="status-warn">Dashboard is running on demo data. Upload your CSV below to analyse real data.</div>', unsafe_allow_html=True)

# ── STEP 1 ────────────────────────────────────────────────────────────────────
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

# ── STEP 2 — UPLOADER (no HTML box above it) ──────────────────────────────────
st.markdown('<div class="section-title">Step 2 — Upload Your CSV File</div>', unsafe_allow_html=True)

# The native uploader IS the drop target — nothing sits on top of it
uploaded_file = st.file_uploader(
    "Upload CSV", type=["csv"], label_visibility="collapsed"
)

# ── PARALLAX JS via components.html (executes reliably unlike st.markdown) ────
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

# ── PROCESS UPLOAD ────────────────────────────────────────────────────────────
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
                <span style="font-size:20px;">✓</span>
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

# ── RESET ─────────────────────────────────────────────────────────────────────
if "uploaded_data" in st.session_state:
    st.markdown("<div style='margin-top:24px;'></div>", unsafe_allow_html=True)
    st.markdown('<div class="section-title">Reset</div>', unsafe_allow_html=True)
    st.markdown('<div style="font-size:13px;color:#5B8DB8;margin-bottom:10px;">Clear your uploaded data and revert to demo.</div>', unsafe_allow_html=True)
    if st.button("Clear uploaded data — revert to demo", key="clear_data"):
        for key in ["uploaded_data","data_source","default_year","default_channel","default_brand","default_region"]:
            if key in st.session_state:
                del st.session_state[key]
        st.rerun()