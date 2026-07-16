"""
pages/Revenue_Forecast.py
=========================
Revenue Forecasting — Shalina Distribution Intelligence
Projects year-end revenue by country, territory, and retailer type
using current YTD run-rates and opportunity category signals.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import sys, os, io

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fabric_connector import load_data as _load_data

# ── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="padding:20px 8px 10px 8px;">
        <div style="font-family:Inter,sans-serif;font-size:10px;font-weight:700;
        color:rgba(100,180,220,0.7);text-transform:uppercase;letter-spacing:2px;
        margin-bottom:20px;">Navigation</div>
    </div>""", unsafe_allow_html=True)
    st.page_link("app.py",                       label="Dashboard")
    st.page_link("pages/Command_Center.py",       label="Command Center")
    st.page_link("pages/RFM_Analysis.py",         label="RFM Analysis")
    st.page_link("pages/Churn_Prediction.py",     label="Churn Prediction")
    st.page_link("pages/Revenue_Forecast.py",     label="Revenue Forecast")
    st.page_link("pages/Upload_Data.py",          label="Upload Data")
    st.markdown("""<div style="margin-top:16px;padding:0 8px;">
        <div style="height:1px;background:linear-gradient(90deg,transparent,
        rgba(33,150,196,0.35),transparent);"></div></div>""", unsafe_allow_html=True)
    import streamlit.components.v1 as _sc
    _sc.html("""<script>(function(){function r(){var n=window.parent.document
        .querySelector('[data-testid="stSidebarNav"]');
        if(n){n.remove();}else{setTimeout(r,200);}}
        r();setTimeout(r,800);setTimeout(r,2500);})();</script>""", height=0)

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
* { box-sizing: border-box; }
.stApp { font-family:'Inter',sans-serif; color:#E2E8F0; background:#0d1526; min-height:100vh; }
.stApp::before { content:''; position:fixed; inset:0;
    background:
        radial-gradient(ellipse 80% 50% at 10% 0%,  rgba(20,100,220,0.22) 0%, transparent 60%),
        radial-gradient(ellipse 50% 40% at 90% 10%,  rgba(100,30,200,0.18) 0%, transparent 55%),
        radial-gradient(ellipse 60% 60% at 50% 100%, rgba(15,60,160,0.20) 0%, transparent 60%);
    pointer-events:none; z-index:0; }
.main .block-container { background:transparent; padding-top:1rem;
    padding-left:1.5rem; padding-right:1.5rem; max-width:1500px; position:relative; z-index:1; }
section[data-testid="stSidebar"] { background:rgba(8,13,26,0.95) !important;
    border-right:1px solid rgba(255,255,255,0.06) !important; }
section[data-testid="stSidebar"] * { color:#94A3B8 !important; font-family:'Inter',sans-serif !important; }
[data-testid="stDecoration"],#MainMenu,footer { display:none !important; }
[data-testid="stToolbar"] { display:flex !important; background:transparent !important; }
header[data-testid="stHeader"] { background:transparent !important; }
[data-testid="stSidebarCollapseButton"]::before { content:"‹"; color:#94A3B8; font-size:26px; line-height:1; }
[data-testid="collapsedControl"]::before,[data-testid="stExpandSidebarButton"]::before {
    content:"›"; color:#94A3B8; font-size:26px; line-height:1; }
[data-testid="stExpandSidebarButton"] {
    display:flex !important; visibility:visible !important; opacity:1 !important;
    position:fixed !important; top:16px !important; left:16px !important;
    width:34px !important; height:34px !important; z-index:999999 !important;
    align-items:center !important; justify-content:center !important;
    background:rgba(8,13,26,0.82) !important; border:1px solid rgba(255,255,255,0.12) !important;
    border-radius:8px !important; }
.page-header { padding:20px 0 16px 0; border-bottom:1px solid rgba(255,255,255,0.06); margin-bottom:24px; }
.page-eyebrow { font-size:10px; font-weight:600; letter-spacing:3px; text-transform:uppercase; color:#475569; margin-bottom:6px; }
.page-title { font-size:24px; font-weight:800; color:#F1F5F9; letter-spacing:-0.5px; }
.page-title span { color:#22C55E; }
.kpi-row { display:grid; grid-template-columns:repeat(4,1fr); gap:12px; margin-bottom:24px; }
.kpi-card { border-radius:12px; padding:20px 20px 16px 20px; position:relative; overflow:hidden;
    min-height:110px; border:1px solid rgba(255,255,255,0.08); transition:transform 0.2s ease; }
.kpi-card:hover { transform:translateY(-2px); }
.kpi-card.mc-green  { background:linear-gradient(135deg,#051a0f 0%,#0d5c2a 100%); box-shadow:0 4px 24px rgba(34,197,94,0.15),inset 0 1px 0 rgba(34,197,94,0.2); border-color:rgba(34,197,94,0.25); }
.kpi-card.mc-blue   { background:linear-gradient(135deg,#0f172a 0%,#1e3a5f 100%); box-shadow:0 4px 24px rgba(59,130,246,0.15),inset 0 1px 0 rgba(59,130,246,0.2); border-color:rgba(59,130,246,0.25); }
.kpi-card.mc-purple { background:linear-gradient(135deg,#0f0a1a 0%,#3b1f6e 100%); box-shadow:0 4px 24px rgba(139,92,246,0.15),inset 0 1px 0 rgba(139,92,246,0.2); border-color:rgba(139,92,246,0.25); }
.kpi-card.mc-amber  { background:linear-gradient(135deg,#1a1400 0%,#5c4500 100%); box-shadow:0 4px 24px rgba(245,158,11,0.15),inset 0 1px 0 rgba(245,158,11,0.2); border-color:rgba(245,158,11,0.25); }
.kpi-accent-line { height:2px; width:40px; border-radius:1px; margin-bottom:12px; }
.kpi-label { font-size:10px; font-weight:600; letter-spacing:1.5px; text-transform:uppercase; color:#64748B; margin-bottom:6px; }
.kpi-value { font-size:32px; font-weight:800; color:#F8FAFC; line-height:1; letter-spacing:-1px; }
.kpi-delta { font-size:11px; color:#475569; margin-top:6px; }
.section-title { font-size:11px; font-weight:700; letter-spacing:2px; text-transform:uppercase;
    color:#475569; margin-top:24px; margin-bottom:12px; display:flex; align-items:center; gap:10px; }
.section-title::after { content:''; flex:1; height:1px; background:linear-gradient(90deg,rgba(255,255,255,0.08),transparent); }
.scenario-card { border-radius:12px; padding:18px 20px; border:1px solid; margin-bottom:8px; }
.scenario-bear  { background:rgba(239,68,68,0.06);  border-color:rgba(239,68,68,0.2); }
.scenario-base  { background:rgba(59,130,246,0.06); border-color:rgba(59,130,246,0.2); }
.scenario-bull  { background:rgba(34,197,94,0.06);  border-color:rgba(34,197,94,0.2); }
.insight-card { background:rgba(255,255,255,0.025); border-radius:12px; padding:16px 20px;
    border:1px solid rgba(255,255,255,0.07); margin-bottom:10px; }
.insight-title  { font-size:14px; font-weight:700; color:#F1F5F9; margin-bottom:4px; }
.insight-detail { font-size:12px; color:#64748B; line-height:1.6; }
[data-baseweb="select"] > div { background:rgba(255,255,255,0.04) !important;
    border:1px solid rgba(255,255,255,0.08) !important; border-radius:8px !important; color:#E2E8F0 !important; }
[data-baseweb="popover"] { background:#0f172a !important; border:1px solid rgba(255,255,255,0.1) !important; }
[role="option"] { background:#0f172a !important; color:#E2E8F0 !important; }
[role="option"]:hover { background:rgba(34,197,94,0.15) !important; }
.stSelectbox label,.stSlider label { color:#475569 !important; font-size:10px !important;
    font-weight:700 !important; text-transform:uppercase; letter-spacing:1px; }
[data-testid="stDataFrame"] { border-radius:10px !important; border:1px solid rgba(255,255,255,0.07) !important; }
.stDownloadButton > button { background:rgba(34,197,94,0.15) !important; color:#86EFAC !important;
    border:1px solid rgba(34,197,94,0.3) !important; border-radius:8px !important; font-weight:600 !important; }
</style>
""", unsafe_allow_html=True)

# ── LOAD DATA ─────────────────────────────────────────────────────────────────
@st.cache_data(show_spinner=False)
def load():
    df, _, _ = _load_data()
    return df

df_all = load()
if df_all is None:
    st.error("No data available.")
    st.stop()

# ── PAGE HEADER ───────────────────────────────────────────────────────────────
st.markdown("""
<div class="page-header">
    <div class="page-eyebrow">Shalina Healthcare &nbsp;&middot;&nbsp; Predictive Analytics</div>
    <div class="page-title">Revenue <span>Forecast</span></div>
</div>""", unsafe_allow_html=True)

# ── FORECAST ENGINE ───────────────────────────────────────────────────────────
# Current month drives how much of the year has elapsed
current_month   = datetime.now().month
months_elapsed  = current_month
months_remaining = 12 - months_elapsed
year_fraction   = months_elapsed / 12

# Scenario multipliers applied to the projected remaining months
SCENARIOS = {
    "Bear (Pessimistic)": 0.70,   # 30% below run-rate for rest of year
    "Base (Expected)":    1.00,   # same run-rate continues
    "Bull (Optimistic)":  1.30,   # 30% above run-rate
}
SCENARIO_COLORS = {
    "Bear (Pessimistic)": "#EF4444",
    "Base (Expected)":    "#3B82F6",
    "Bull (Optimistic)":  "#22C55E",
}

# Opportunity-based growth adjustment — High Performers likely to grow, Dead to stay flat
OPP_GROWTH = {
    "High Performer":  1.10,
    "Active":          1.00,
    "Low Performer":   0.90,
    "Underperforming": 0.75,
    "Dead Whitespace": 0.00,
}

def forecast_df(df, scenario_mult=1.0):
    """
    For each outlet:
      monthly_run_rate = YTD / months_elapsed
      remaining_revenue = monthly_run_rate × months_remaining × scenario_mult × opp_growth
      year_end_forecast = YTD + remaining_revenue
    """
    out = df.copy()
    out["ytd"]         = pd.to_numeric(out["YTD Retailing Value"], errors="coerce").fillna(0)
    out["opp_growth"]  = out["Opportunity"].map(OPP_GROWTH).fillna(1.0)
    out["run_rate"]    = np.where(months_elapsed > 0, out["ytd"] / months_elapsed, 0)
    out["remaining"]   = out["run_rate"] * months_remaining * scenario_mult * out["opp_growth"]
    out["year_end"]    = out["ytd"] + out["remaining"]
    out["growth_pct"]  = np.where(
        out["ytd"] > 0,
        (out["remaining"] / out["ytd"] * 100).round(1),
        0
    )
    return out

# ── FILTERS ───────────────────────────────────────────────────────────────────
f1, f2 = st.columns([1, 5])
with f1:
    country_sel = st.selectbox("Country", ["All", "Nigeria", "Angola"])

view = df_all.copy()
if country_sel != "All":
    view = view[view["country"] == country_sel]

# Run all three scenarios
df_bear = forecast_df(view, SCENARIOS["Bear (Pessimistic)"])
df_base = forecast_df(view, SCENARIOS["Base (Expected)"])
df_bull = forecast_df(view, SCENARIOS["Bull (Optimistic)"])

ytd_total       = df_base["ytd"].sum()
bear_year_end   = df_bear["year_end"].sum()
base_year_end   = df_base["year_end"].sum()
bull_year_end   = df_bull["year_end"].sum()
active_outlets  = int((df_base["ytd"] > 0).sum())
ytd_per_active  = df_base[df_base["ytd"] > 0]["ytd"].mean()

# ── KPI CARDS ─────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="kpi-row">
    <div class="kpi-card mc-blue">
        <div class="kpi-accent-line" style="background:linear-gradient(90deg,#3B82F6,#60A5FA);"></div>
        <div class="kpi-label">YTD Revenue ({datetime.now().strftime('%b %Y')})</div>
        <div class="kpi-value">&#8358;{ytd_total/1_000_000:.1f}M</div>
        <div class="kpi-delta">{months_elapsed} months elapsed &mdash; {active_outlets:,} active outlets</div>
    </div>
    <div class="kpi-card mc-green">
        <div class="kpi-accent-line" style="background:linear-gradient(90deg,#22C55E,#4ADE80);"></div>
        <div class="kpi-label">Base Year-End Forecast</div>
        <div class="kpi-value">&#8358;{base_year_end/1_000_000:.1f}M</div>
        <div class="kpi-delta">At current run-rate through Dec</div>
    </div>
    <div class="kpi-card mc-purple">
        <div class="kpi-accent-line" style="background:linear-gradient(90deg,#8B5CF6,#A78BFA);"></div>
        <div class="kpi-label">Bull Forecast (Optimistic)</div>
        <div class="kpi-value">&#8358;{bull_year_end/1_000_000:.1f}M</div>
        <div class="kpi-delta">+30% acceleration on remaining months</div>
    </div>
    <div class="kpi-card mc-amber">
        <div class="kpi-accent-line" style="background:linear-gradient(90deg,#F59E0B,#FCD34D);"></div>
        <div class="kpi-label">Forecast Range</div>
        <div class="kpi-value">&#8358;{(bull_year_end - bear_year_end)/1_000_000:.1f}M</div>
        <div class="kpi-delta">Bear &#8358;{bear_year_end/1_000_000:.1f}M &rarr; Bull &#8358;{bull_year_end/1_000_000:.1f}M</div>
    </div>
</div>""", unsafe_allow_html=True)

# ── SCENARIO WATERFALL CHART ──────────────────────────────────────────────────
st.markdown('<div class="section-title">Year-End Revenue Scenarios</div>', unsafe_allow_html=True)

months_labels = ["Jan","Feb","Mar","Apr","May","Jun",
                 "Jul","Aug","Sep","Oct","Nov","Dec"]
elapsed_months_list   = months_labels[:months_elapsed]
remaining_months_list = months_labels[months_elapsed:]

# Build monthly projection lines for each scenario
def monthly_series(df_scenario, scenario_mult):
    total_ytd       = df_scenario["ytd"].sum()
    monthly_ytd_avg = total_ytd / max(months_elapsed, 1)
    # Run-rate for remaining months (with scenario + opp-weighted adjustment)
    run_rates       = df_scenario["run_rate"] * scenario_mult * df_scenario["opp_growth"]
    monthly_future  = run_rates.sum()
    past   = [monthly_ytd_avg] * months_elapsed
    future = [monthly_future] * months_remaining
    return past + future

series_bear = monthly_series(df_bear, SCENARIOS["Bear (Pessimistic)"])
series_base = monthly_series(df_base, SCENARIOS["Base (Expected)"])
series_bull = monthly_series(df_bull, SCENARIOS["Bull (Optimistic)"])

fig_forecast = go.Figure()

# Shaded uncertainty band (bear to bull)
fig_forecast.add_trace(go.Scatter(
    x=months_labels + months_labels[::-1],
    y=[s/1000 for s in series_bull] + [s/1000 for s in series_bear[::-1]],
    fill="toself",
    fillcolor="rgba(34,197,94,0.08)",
    line=dict(color="rgba(0,0,0,0)"),
    name="Forecast Range",
    hoverinfo="skip",
))

# Divider line between actual and forecast
fig_forecast.add_vline(
    x=months_elapsed - 0.5,
    line=dict(color="rgba(255,255,255,0.2)", dash="dot", width=1),
)
fig_forecast.add_annotation(
    x=months_elapsed - 0.5, y=0, yref="paper",
    text="TODAY", showarrow=False,
    font=dict(color="#475569", size=9),
    textangle=-90, yanchor="bottom",
)

for name, series, color, dash in [
    ("Bear (Pessimistic)", series_bear, "#EF4444", "dot"),
    ("Base (Expected)",    series_base, "#3B82F6", "solid"),
    ("Bull (Optimistic)",  series_bull, "#22C55E", "dash"),
]:
    fig_forecast.add_trace(go.Scatter(
        x=months_labels,
        y=[s/1000 for s in series],
        mode="lines+markers",
        name=name,
        line=dict(color=color, width=2.5, dash=dash),
        marker=dict(size=5, color=color),
        hovertemplate=f"<b>{name}</b><br>%{{x}}: ₦%{{y:,.0f}}K<extra></extra>",
    ))

fig_forecast.update_layout(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(255,255,255,0.02)",
    font=dict(color="#64748B", size=11),
    height=380,
    xaxis=dict(gridcolor="rgba(255,255,255,0.04)", linecolor="rgba(255,255,255,0.06)"),
    yaxis=dict(gridcolor="rgba(255,255,255,0.04)", linecolor="rgba(255,255,255,0.06)",
               title="Monthly Revenue (₦K)"),
    legend=dict(font=dict(color="#94A3B8"), bgcolor="rgba(8,13,26,0.8)",
                bordercolor="rgba(255,255,255,0.08)", borderwidth=1),
    margin=dict(l=0, r=0, t=10, b=0),
    hovermode="x unified",
)
st.plotly_chart(fig_forecast, use_container_width=True)

# ── SCENARIO SUMMARY CARDS ────────────────────────────────────────────────────
sc1, sc2, sc3 = st.columns(3)
for col, label, val, cls, color, desc in [
    (sc1, "Bear — Pessimistic", bear_year_end, "scenario-bear", "#EF4444",
     "30% slowdown vs current run-rate. Assumes churn accelerates and no new activations."),
    (sc2, "Base — Expected",    base_year_end, "scenario-base", "#3B82F6",
     "Current run-rate continues unchanged through December. Most likely outcome."),
    (sc3, "Bull — Optimistic",  bull_year_end, "scenario-bull", "#22C55E",
     "30% acceleration. Assumes dead whitespace recovery campaign delivers results."),
]:
    with col:
        uplift = val - ytd_total
        st.markdown(f"""
        <div class="scenario-card {cls}">
            <div style="font-size:10px;font-weight:700;letter-spacing:1.5px;
                text-transform:uppercase;color:{color};margin-bottom:8px;">{label}</div>
            <div style="font-size:28px;font-weight:800;color:#F1F5F9;letter-spacing:-0.5px;">
                &#8358;{val/1_000_000:.1f}M</div>
            <div style="font-size:11px;color:{color};margin-top:4px;font-weight:600;">
                + &#8358;{uplift/1_000_000:.1f}M remaining</div>
            <div style="font-size:11px;color:#64748B;margin-top:6px;line-height:1.5;">{desc}</div>
        </div>""", unsafe_allow_html=True)

# ── BY COUNTRY ────────────────────────────────────────────────────────────────
st.markdown('<div class="section-title">Year-End Forecast by Country</div>', unsafe_allow_html=True)

country_summary = []
for cntry in df_all["country"].unique():
    sub      = df_all[df_all["country"] == cntry]
    db       = forecast_df(sub, SCENARIOS["Bear (Pessimistic)"])
    dbs      = forecast_df(sub, SCENARIOS["Base (Expected)"])
    dbu      = forecast_df(sub, SCENARIOS["Bull (Optimistic)"])
    country_summary.append({
        "Country":         cntry,
        "Active Outlets":  int((dbs["ytd"] > 0).sum()),
        "YTD Revenue":     dbs["ytd"].sum(),
        "Bear Forecast":   db["year_end"].sum(),
        "Base Forecast":   dbs["year_end"].sum(),
        "Bull Forecast":   dbu["year_end"].sum(),
        "Remaining (Base)": (dbs["year_end"] - dbs["ytd"]).sum(),
    })

country_df = pd.DataFrame(country_summary)

fig_country = go.Figure()
for scenario, color in [
    ("Bear Forecast", "#EF4444"),
    ("Base Forecast", "#3B82F6"),
    ("Bull Forecast", "#22C55E"),
]:
    fig_country.add_trace(go.Bar(
        name=scenario,
        x=country_df["Country"],
        y=country_df[scenario] / 1_000_000,
        marker_color=color,
        opacity=0.85,
        hovertemplate=f"<b>{scenario}</b><br>%{{x}}: ₦%{{y:.1f}}M<extra></extra>",
    ))

fig_country.add_trace(go.Scatter(
    name="YTD Actual",
    x=country_df["Country"],
    y=country_df["YTD Revenue"] / 1_000_000,
    mode="markers",
    marker=dict(symbol="diamond", size=14, color="#FFFFFF",
                line=dict(color="#94A3B8", width=2)),
    hovertemplate="<b>YTD Actual</b><br>%{x}: ₦%{y:.1f}M<extra></extra>",
))

fig_country.update_layout(
    barmode="group",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(255,255,255,0.02)",
    font=dict(color="#64748B", size=11), height=360,
    xaxis=dict(gridcolor="rgba(255,255,255,0.04)"),
    yaxis=dict(gridcolor="rgba(255,255,255,0.04)", title="Revenue (₦M)"),
    legend=dict(font=dict(color="#94A3B8"), bgcolor="rgba(8,13,26,0.8)",
                bordercolor="rgba(255,255,255,0.08)", borderwidth=1),
    margin=dict(l=0, r=0, t=10, b=0),
)
st.plotly_chart(fig_country, use_container_width=True)

# ── BY RETAILER SUBTYPE ───────────────────────────────────────────────────────
st.markdown('<div class="section-title">Forecast by Retailer Type</div>', unsafe_allow_html=True)

subtype_rows = []
for sub_t in df_all["Retailer Subtype"].dropna().unique():
    sub   = df_all[df_all["Retailer Subtype"] == sub_t]
    if country_sel != "All":
        sub = sub[sub["country"] == country_sel]
    dbs   = forecast_df(sub, SCENARIOS["Base (Expected)"])
    if dbs["ytd"].sum() == 0:
        continue
    subtype_rows.append({
        "Retailer Type": sub_t,
        "Outlets":       len(sub),
        "Active":        int((dbs["ytd"] > 0).sum()),
        "YTD (₦M)":     round(dbs["ytd"].sum() / 1_000_000, 2),
        "Year-End Base (₦M)": round(dbs["year_end"].sum() / 1_000_000, 2),
        "Remaining Rev (₦M)": round((dbs["year_end"] - dbs["ytd"]).sum() / 1_000_000, 2),
        "Avg YTD per Active (₦K)": round(dbs[dbs["ytd"]>0]["ytd"].mean(), 1),
    })

subtype_df = pd.DataFrame(subtype_rows).sort_values("Year-End Base (₦M)", ascending=False)

fig_sub = px.bar(
    subtype_df, x="Retailer Type",
    y=["YTD (₦M)", "Remaining Rev (₦M)"],
    barmode="stack",
    color_discrete_map={"YTD (₦M)": "#3B82F6", "Remaining Rev (₦M)": "#22C55E"},
    height=320,
    labels={"value": "Revenue (₦M)", "variable": ""},
)
fig_sub.update_layout(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(255,255,255,0.02)",
    font=dict(color="#64748B", size=11),
    xaxis=dict(gridcolor="rgba(255,255,255,0.04)"),
    yaxis=dict(gridcolor="rgba(255,255,255,0.04)"),
    legend=dict(font=dict(color="#94A3B8"), bgcolor="rgba(8,13,26,0.8)",
                bordercolor="rgba(255,255,255,0.08)", borderwidth=1),
    margin=dict(l=0, r=0, t=10, b=0),
)
st.plotly_chart(fig_sub, use_container_width=True)

# ── OPPORTUNITY UPLIFT TABLE ──────────────────────────────────────────────────
st.markdown('<div class="section-title">Revenue Uplift by Opportunity Category</div>',
            unsafe_allow_html=True)
st.markdown("""
<div style="background:rgba(34,197,94,0.06);border:1px solid rgba(34,197,94,0.18);
     border-radius:10px;padding:12px 18px;margin-bottom:14px;font-size:12px;color:#64748B;line-height:1.6;">
    <strong style="color:#86EFAC;">How to read this:</strong> The "Recoverable Revenue" column shows
    how much additional revenue Shalina could capture from currently underperforming outlets
    if they were brought up to the peer median. This is the commercial opportunity.
</div>""", unsafe_allow_html=True)

opp_rows = []
active_median = df_base[df_base["ytd"] > 0]["ytd"].median()
for opp in ["High Performer","Active","Low Performer","Underperforming","Dead Whitespace"]:
    sub   = df_base[df_base["Opportunity"] == opp]
    if country_sel != "All":
        sub = df_base[(df_base["Opportunity"] == opp) & (df_base["country"] == country_sel)]
    n         = len(sub)
    ytd_sum   = sub["ytd"].sum()
    ye_sum    = sub["year_end"].sum()
    gap       = max((active_median - sub["ytd"].mean()) * n, 0) if n > 0 else 0
    opp_rows.append({
        "Category":              opp,
        "Outlets":               n,
        "YTD Revenue (₦M)":     round(ytd_sum / 1_000_000, 2),
        "Year-End Forecast (₦M)": round(ye_sum / 1_000_000, 2),
        "Recoverable Revenue (₦M)": round(gap / 1_000_000, 2),
    })

opp_df = pd.DataFrame(opp_rows)
st.dataframe(opp_df, use_container_width=True, hide_index=True)

# ── TOP GROWTH & DECLINE OUTLETS ─────────────────────────────────────────────
st.markdown('<div class="section-title">Outlet-Level Growth Outlook</div>', unsafe_allow_html=True)
col_g, col_d = st.columns(2)

active_base = df_base[df_base["ytd"] > 0].copy()

with col_g:
    st.markdown("""<div style="font-size:11px;font-weight:700;color:#22C55E;
        text-transform:uppercase;letter-spacing:1px;margin-bottom:8px;">
        Top 10 Growth Outlets</div>""", unsafe_allow_html=True)
    top_growth = (
        active_base.nlargest(10, "year_end")
        [["Shop Name","country","Opportunity","ytd","year_end"]]
        .rename(columns={"Shop Name":"Outlet","country":"Country",
                         "ytd":"YTD (₦K)","year_end":"Forecast (₦K)"})
        .reset_index(drop=True)
    )
    top_growth.index += 1
    top_growth["YTD (₦K)"]      = top_growth["YTD (₦K)"].apply(lambda x: f"₦{x:,.0f}K")
    top_growth["Forecast (₦K)"] = top_growth["Forecast (₦K)"].apply(lambda x: f"₦{x:,.0f}K")
    st.dataframe(top_growth, use_container_width=True)

with col_d:
    st.markdown("""<div style="font-size:11px;font-weight:700;color:#EF4444;
        text-transform:uppercase;letter-spacing:1px;margin-bottom:8px;">
        10 Outlets with Lowest Forecast</div>""", unsafe_allow_html=True)
    low_base = df_base[
        (df_base["ytd"] > 0) &
        (df_base["Opportunity"].isin(["Low Performer","Underperforming"]))
    ].nsmallest(10, "year_end")[
        ["Shop Name","country","Opportunity","ytd","year_end"]
    ].rename(columns={"Shop Name":"Outlet","country":"Country",
                      "ytd":"YTD (₦K)","year_end":"Forecast (₦K)"}
    ).reset_index(drop=True)
    low_base.index += 1
    low_base["YTD (₦K)"]      = low_base["YTD (₦K)"].apply(lambda x: f"₦{x:,.0f}K")
    low_base["Forecast (₦K)"] = low_base["Forecast (₦K)"].apply(lambda x: f"₦{x:,.0f}K")
    st.dataframe(low_base, use_container_width=True)

# ── STRATEGIC INSIGHTS ────────────────────────────────────────────────────────
st.markdown('<div class="section-title">Forecast Insights</div>', unsafe_allow_html=True)

total_recoverable = opp_df[
    opp_df["Category"].isin(["Underperforming","Dead Whitespace","Low Performer"])
]["Recoverable Revenue (₦M)"].sum()

bull_upside = (bull_year_end - base_year_end) / 1_000_000

st.markdown(f"""
<div class="insight-card">
    <span style="display:inline-block;padding:3px 10px;border-radius:4px;font-size:10px;
         font-weight:700;letter-spacing:0.5px;text-transform:uppercase;margin-bottom:8px;
         background:rgba(34,197,94,0.12);color:#86EFAC;border:1px solid rgba(34,197,94,0.3);">
        Growth Opportunity</span>
    <div class="insight-title">
        &#8358;{total_recoverable:.1f}M Recoverable from Underperforming Outlets</div>
    <div class="insight-detail">
        If underperforming and low-performer outlets were brought up to the active outlet median,
        Shalina could recover an additional <strong style="color:#FFFFFF">&#8358;{total_recoverable:.1f}M</strong>
        in annual revenue without acquiring a single new outlet.
        Focus the commercial team on these existing but underactivated accounts first.
    </div>
</div>
<div class="insight-card">
    <span style="display:inline-block;padding:3px 10px;border-radius:4px;font-size:10px;
         font-weight:700;letter-spacing:0.5px;text-transform:uppercase;margin-bottom:8px;
         background:rgba(59,130,246,0.12);color:#93C5FD;border:1px solid rgba(59,130,246,0.3);">
        Scenario Gap</span>
    <div class="insight-title">
        Bull vs Base Gap is &#8358;{bull_upside:.1f}M — Achievable with Right Actions</div>
    <div class="insight-detail">
        The difference between the base and optimistic scenario is
        <strong style="color:#FFFFFF">&#8358;{bull_upside:.1f}M</strong>.
        This gap is closeable through three levers: activating dead whitespace outlets,
        upselling underperformers, and protecting high-risk active accounts from churning.
        The Churn Prediction and Command Center pages identify exactly which outlets to act on.
    </div>
</div>
<div class="insight-card">
    <span style="display:inline-block;padding:3px 10px;border-radius:4px;font-size:10px;
         font-weight:700;letter-spacing:0.5px;text-transform:uppercase;margin-bottom:8px;
         background:rgba(245,158,11,0.12);color:#FCD34D;border:1px solid rgba(245,158,11,0.3);">
        Time Sensitivity</span>
    <div class="insight-title">
        {months_remaining} Months Left — Every Month of Delay Costs Revenue</div>
    <div class="insight-detail">
        With {months_remaining} months remaining in the year, each month of inaction on
        dead whitespace outlets costs approximately
        <strong style="color:#FFFFFF">&#8358;{(bull_year_end - base_year_end) / max(months_remaining,1) / 1_000_000:.1f}M</strong>
        in potential upside. The activation campaigns should begin immediately to maximise year-end capture.
    </div>
</div>
""", unsafe_allow_html=True)

# ── EXPORT ────────────────────────────────────────────────────────────────────
st.markdown('<div class="section-title">Export Forecast</div>', unsafe_allow_html=True)

ex1, ex2, _ = st.columns([1, 1, 4])

_export = df_base[[
    "Shop Name", "country", "Retailer Subtype", "Opportunity",
    "ytd", "run_rate", "remaining", "year_end", "growth_pct"
]].rename(columns={
    "Shop Name": "Outlet",
    "ytd":        "YTD Revenue (K)",
    "run_rate":   "Monthly Run Rate (K)",
    "remaining":  "Projected Remaining (K)",
    "year_end":   "Year-End Forecast (K)",
    "growth_pct": "Projected Growth %",
})

with ex1:
    st.download_button(
        "⬇ Download CSV",
        _export.to_csv(index=False).encode("utf-8"),
        f"revenue_forecast_{country_sel.lower()}.csv",
        "text/csv",
        use_container_width=True,
    )

with ex2:
    _xl = io.BytesIO()
    with pd.ExcelWriter(_xl, engine="openpyxl") as _xw:
        _export.to_excel(_xw, index=False, sheet_name="Outlet Forecasts")
        country_df.to_excel(_xw, index=False, sheet_name="By Country")
        subtype_df.to_excel(_xw, index=False, sheet_name="By Retailer Type")
        opp_df.to_excel(_xw, index=False, sheet_name="By Opportunity")
    _xl.seek(0)
    st.download_button(
        "⬇ Download Excel",
        _xl,
        f"revenue_forecast_{country_sel.lower()}.xlsx",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True,
    )
