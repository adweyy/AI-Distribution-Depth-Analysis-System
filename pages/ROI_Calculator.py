import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import os

st.set_page_config(layout="wide", page_title="ROI Calculator | Shalina", initial_sidebar_state="expanded")

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
    st.page_link("app.py",                      label="🏠  Dashboard")
    st.page_link("pages/ROI_Calculator.py",     label="📊  ROI Calculator")
    st.page_link("pages/Upload_Data.py",        label="☁️  Upload Data")
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
[data-testid="stSidebarNav"], [data-testid="stSidebarNavItems"], section[data-testid="stSidebar"] nav { display: none !important; }
[data-testid="stToolbar"], [data-testid="stDecoration"], header[data-testid="stHeader"], #MainMenu, footer { display: none !important; }
.header-wrap { background: rgba(10,30,60,0.7); border-radius: 16px; padding: 20px 28px; border: 1px solid rgba(33,150,196,0.25); box-shadow: 0 4px 24px rgba(0,0,0,0.3); backdrop-filter: blur(20px); margin-bottom: 18px; }
.section-title { font-family: 'Poppins', sans-serif; font-size: 12px; font-weight: 700; color: #90C8E8; margin-top: 24px; margin-bottom: 12px; display: flex; align-items: center; gap: 10px; text-transform: uppercase; letter-spacing: 1.2px; }
.section-title::before { content: ''; display: inline-block; width: 4px; height: 14px; background: linear-gradient(180deg, #2196C4, #6EC6F5); border-radius: 2px; box-shadow: 0 0 8px rgba(33,150,196,0.5); }
.kpi-row { display: grid; grid-template-columns: repeat(4, 1fr); gap: 14px; margin-bottom: 22px; }
.kpi-card { border-radius: 14px; padding: 20px 22px; position: relative; overflow: hidden; min-height: 110px; border: 1px solid rgba(255,255,255,0.1); box-shadow: 0 4px 20px rgba(0,0,0,0.3); transition: transform 0.2s ease; }
.kpi-card:hover { transform: translateY(-2px); }
.kpi-card::before { content: ''; position: absolute; bottom: -20px; right: -20px; width: 100px; height: 100px; border-radius: 50%; background: rgba(255,255,255,0.10); }
.kpi-card::after  { content: ''; position: absolute; bottom: -40px; right: 20px; width: 80px; height: 80px; border-radius: 50%; background: rgba(255,255,255,0.06); }
.kpi-card.navy  { background: linear-gradient(135deg, #0B2E59 0%, #1A5276 100%); }
.kpi-card.blue  { background: linear-gradient(135deg, #1A7FC4 0%, #6EC6F5 100%); }
.kpi-card.gold  { background: linear-gradient(135deg, #F9A825 0%, #F7D080 100%); }
.kpi-card.green { background: linear-gradient(135deg, #1B8A4E 0%, #4CAF50 100%); }
.kpi-card.red   { background: linear-gradient(135deg, #C0392B 0%, #E74C3C 100%); }
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
.stDownloadButton > button { background: linear-gradient(135deg, #0D3B6E, #1A7FC4) !important; color: white !important; border: none !important; border-radius: 8px !important; font-weight: 600 !important; padding: 10px 24px !important; }
.stSlider label { color: #90C8E8 !important; font-size: 11px !important; font-weight: 600 !important; text-transform: uppercase; letter-spacing: 0.8px; }
</style>
""", unsafe_allow_html=True)

# ── HEADER ──────────────────────────────────────────────────
st.markdown("""
<div class="header-wrap">
    <div style="font-family:'DM Sans',sans-serif;font-size:11px;font-weight:600;color:#90C8E8;letter-spacing:2px;text-transform:uppercase;margin-bottom:4px;">Shalina Healthcare</div>
    <div style="font-family:'Poppins',sans-serif;font-size:32px;font-weight:700;color:#FFFFFF;letter-spacing:-0.5px;line-height:1.1;">ROI Calculator</div>
    <div style="font-family:'DM Sans',sans-serif;font-size:13px;color:#7AACCC;margin-top:4px;">Estimate revenue potential from activating whitespace outlets</div>
</div>
""", unsafe_allow_html=True)

# ── LOAD DATA ──────────────────────────────────────────────────
import sys as _sys
_sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from fabric_connector import load_data as _load_data

df_all_roi, _, _ = _load_data()

if df_all_roi is None:
    st.error("No data available. Please check Fabric connection or add shalina_combined_data.csv.")
    st.stop()

# Reclassify if needed
if 'Opportunity' not in df_all_roi.columns:
    def _classify_roi(df):
        import numpy as np
        results = []
        for country in df['country'].unique():
            sub = df[df['country'] == country].copy()
            nonzero = sub[sub['YTD Retailing Value'] > 0]['YTD Retailing Value']
            if len(nonzero) == 0:
                sub['Opportunity'] = 'Dead Whitespace'
                results.append(sub); continue
            p25 = nonzero.quantile(0.25); mean = nonzero.mean(); p75 = nonzero.quantile(0.75)
            def clf(v, p25=p25, mean=mean, p75=p75):
                if v == 0: return 'Dead Whitespace'
                elif v < p25: return 'Underperforming'
                elif v < mean: return 'Low Performer'
                elif v < p75: return 'Active'
                else: return 'High Performer'
            sub['Opportunity'] = sub['YTD Retailing Value'].apply(clf)
            results.append(sub)
        return pd.concat(results, ignore_index=True)
    df_all_roi = _classify_roi(df_all_roi)

# Country selector
roi_cc1, roi_cc2, roi_cc3 = st.columns([1,1,8])
with roi_cc1:
    if st.button("🇳🇬  Nigeria", use_container_width=True, key="roi_ng"):
        st.session_state.roi_country = "Nigeria"
with roi_cc2:
    if st.button("🇦🇴  Angola", use_container_width=True, key="roi_ao"):
        st.session_state.roi_country = "Angola"
if "roi_country" not in st.session_state:
    st.session_state.roi_country = "Nigeria"
roi_country = st.session_state.roi_country
df_roi = df_all_roi[df_all_roi['country'] == roi_country].copy()

nonzero = df_roi[df_roi['YTD Retailing Value']>0]['YTD Retailing Value']
p25   = nonzero.quantile(0.25) if len(nonzero) else 0
mean_val = nonzero.mean()      if len(nonzero) else 0
p75   = nonzero.quantile(0.75) if len(nonzero) else 0
df    = df_roi

chart_layout = dict(
    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(10,30,60,0.5)",
    font=dict(color="#90C8E8", size=11), height=360,
    xaxis=dict(gridcolor="rgba(33,150,196,0.1)", linecolor="rgba(33,150,196,0.2)", color="#6AACE0"),
    yaxis=dict(gridcolor="rgba(33,150,196,0.1)", linecolor="rgba(33,150,196,0.2)", color="#6AACE0"),
    margin=dict(l=0, r=0, t=20, b=0),
    legend=dict(font=dict(color="#FFFFFF"), bgcolor="rgba(10,30,60,0.7)")
)

# ── ASSUMPTIONS PANEL ──────────────────────────────────────────
st.markdown('<div class="section-title">Activation Assumptions</div>', unsafe_allow_html=True)

c1, c2, c3 = st.columns(3)
with c1:
    price_per_unit = st.slider("Avg Revenue per Outlet Activated (₦K)", 
                                min_value=50, max_value=2000, value=int(mean_val), step=50)
with c2:
    activation_cost = st.slider("Cost to Activate One Outlet (₦K)", 
                                  min_value=10, max_value=500, value=50, step=10)
with c3:
    activation_rate = st.slider("Expected Activation Rate (%)", 
                                  min_value=5, max_value=100, value=30, step=5)

# ── FILTER ──────────────────────────────────────────────────
f1, f2 = st.columns(2)
with f1:
    subtype = st.selectbox("Retailer Subtype", ["All","Primary","Secondary"])
with f2:
    focus = st.selectbox("Focus On", ["Dead Whitespace Only", "Dead + Underperforming", "All Non-High Performers"])

# Filter whitespace outlets
ws_df = df.copy()
if subtype != "All":
    ws_df = ws_df[ws_df['Retailer Subtype'] == subtype]

if focus == "Dead Whitespace Only":
    ws_df = ws_df[ws_df['Opportunity'] == 'Dead Whitespace']
elif focus == "Dead + Underperforming":
    ws_df = ws_df[ws_df['Opportunity'].isin(['Dead Whitespace','Underperforming'])]
else:
    ws_df = ws_df[ws_df['Opportunity'].isin(['Dead Whitespace','Underperforming','Low Performer'])]

total_ws         = len(ws_df)
outlets_activated = int(total_ws * activation_rate / 100)
gross_revenue    = outlets_activated * price_per_unit
total_cost       = outlets_activated * activation_cost
net_roi          = gross_revenue - total_cost
roi_pct          = (net_roi / total_cost * 100) if total_cost > 0 else 0

# ── KPI CARDS ──────────────────────────────────────────────────
st.markdown(f"""
<div class="kpi-row">
    <div class="kpi-card navy">
        <div class="kpi-label">Whitespace Outlets</div>
        <div class="kpi-value">{total_ws:,}</div>
        <div class="kpi-delta">Matching selected filters</div>
    </div>
    <div class="kpi-card blue">
        <div class="kpi-label">Expected Activations</div>
        <div class="kpi-value">{outlets_activated:,}</div>
        <div class="kpi-delta">At {activation_rate}% activation rate</div>
    </div>
    <div class="kpi-card {'green' if net_roi > 0 else 'red'}">
        <div class="kpi-label">Net ROI</div>
        <div class="kpi-value">₦{net_roi/1000:,.0f}M</div>
        <div class="kpi-delta">Revenue minus activation cost</div>
    </div>
    <div class="kpi-card gold">
        <div class="kpi-label">ROI %</div>
        <div class="kpi-value">{roi_pct:,.0f}%</div>
        <div class="kpi-delta">Return on investment</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── CHARTS ──────────────────────────────────────────────────
c1, c2 = st.columns(2)

with c1:
    st.markdown('<div class="section-title">Revenue vs Cost Breakdown</div>', unsafe_allow_html=True)
    fig_bar = px.bar(
        x=["Gross Revenue", "Activation Cost", "Net ROI"],
        y=[gross_revenue/1000, total_cost/1000, net_roi/1000],
        color=["Gross Revenue", "Activation Cost", "Net ROI"],
        color_discrete_map={"Gross Revenue":"#22C55E","Activation Cost":"#EF4444","Net ROI":"#A855F7"},
        labels={"x":"","y":"₦ Millions"}
    )
    fig_bar.update_layout(**chart_layout)
    st.plotly_chart(fig_bar, use_container_width=True)

with c2:
    st.markdown('<div class="section-title">ROI Sensitivity — Activation Rate</div>', unsafe_allow_html=True)
    rates = list(range(5, 105, 5))
    rois  = [(r/100 * total_ws * price_per_unit - r/100 * total_ws * activation_cost)/1000 for r in rates]
    fig_line = px.line(x=rates, y=rois, labels={"x":"Activation Rate (%)","y":"Net ROI (₦M)"},
                       markers=True)
    fig_line.update_traces(line_color="#2196C4", marker_color="#6EC6F5")
    fig_line.add_hline(y=0, line_dash="dash", line_color="rgba(239,68,68,0.6)")
    fig_line.update_layout(**chart_layout)
    st.plotly_chart(fig_line, use_container_width=True)

# ── OUTLET TABLE ──────────────────────────────────────────────
st.markdown('<div class="section-title">Whitespace Outlet List</div>', unsafe_allow_html=True)
show_df = ws_df[['Shop Name','Retailer Subtype','YTD Retailing Value','Opportunity']].copy()
show_df['YTD Retailing Value'] = show_df['YTD Retailing Value'].apply(lambda x: f"₦{x:,.1f}K")
show_df['Est. Revenue if Activated'] = f"₦{price_per_unit:,}K"
show_df = show_df.reset_index(drop=True)
show_df.index += 1
st.dataframe(show_df, use_container_width=True)

csv = ws_df.to_csv(index=False).encode('utf-8')
st.download_button("⬇️ Export Whitespace Outlet List", csv, "whitespace_outlets_roi.csv", "text/csv")