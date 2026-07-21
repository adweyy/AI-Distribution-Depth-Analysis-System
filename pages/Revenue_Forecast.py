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
from styles import apply_styles, sidebar_nav

# ── SIDEBAR ───────────────────────────────────────────────────────────────────
sidebar_nav(refresh_key="rev_refresh")
apply_styles(active_page="Revenue Forecast", active_country=st.session_state.get("country", "Nigeria"))

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
<div class="sh-topbar">
    <div>
        <div class="sh-eyebrow">Shalina Healthcare &nbsp;&middot;&nbsp; Predictive Analytics</div>
        <div class="sh-title">Revenue <span class="sh-title-dim">Forecast</span></div>
    </div>
    <div style="display:flex;align-items:center;gap:10px;">
        <div class="sh-pill"><span class="sh-dot"></span> Live Projections</div>
    </div>
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
def _fmt(v):
    """Auto-scale naira value to B/M/K so it always fits in a card."""
    if abs(v) >= 1_000_000_000:
        return f"&#8358;{v/1_000_000_000:.1f}B"
    elif abs(v) >= 1_000_000:
        return f"&#8358;{v/1_000_000:.1f}M"
    elif abs(v) >= 1_000:
        return f"&#8358;{v/1_000:.1f}K"
    return f"&#8358;{v:,.0f}"

st.markdown(f"""
<div class="sh-kpi-row">
    <div class="sh-kpi">
        <div class="sh-kpi-accent" style="background:linear-gradient(90deg,#3B82F6,#60A5FA);"></div>
        <div class="sh-kpi-label">YTD Revenue ({datetime.now().strftime('%b %Y')})</div>
        <div class="sh-kpi-value">{_fmt(ytd_total)}</div>
        <div class="sh-kpi-delta">{months_elapsed} months elapsed &mdash; {active_outlets:,} active outlets</div>
    </div>
    <div class="sh-kpi">
        <div class="sh-kpi-accent" style="background:linear-gradient(90deg,#22C55E,#4ADE80);"></div>
        <div class="sh-kpi-label">Base Year-End Forecast</div>
        <div class="sh-kpi-value">{_fmt(base_year_end)}</div>
        <div class="sh-kpi-delta">At current run-rate through Dec</div>
    </div>
    <div class="sh-kpi">
        <div class="sh-kpi-accent" style="background:linear-gradient(90deg,#8B5CF6,#A78BFA);"></div>
        <div class="sh-kpi-label">Bull Forecast (Optimistic)</div>
        <div class="sh-kpi-value">{_fmt(bull_year_end)}</div>
        <div class="sh-kpi-delta">+30% acceleration on remaining months</div>
    </div>
    <div class="sh-kpi">
        <div class="sh-kpi-accent" style="background:linear-gradient(90deg,#F59E0B,#FCD34D);"></div>
        <div class="sh-kpi-label">Forecast Range</div>
        <div class="sh-kpi-value">{_fmt(bull_year_end - bear_year_end)}</div>
        <div class="sh-kpi-delta">Bear {_fmt(bear_year_end)} &rarr; Bull {_fmt(bull_year_end)}</div>
    </div>
</div>""", unsafe_allow_html=True)

# ── SCENARIO WATERFALL CHART ──────────────────────────────────────────────────
st.markdown('<div class="sh-section">Year-End Revenue Scenarios</div>', unsafe_allow_html=True)

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
    font=dict(color="#333", size=11),
    height=380,
    xaxis=dict(gridcolor="rgba(255,255,255,0.04)", linecolor="rgba(255,255,255,0.06)"),
    yaxis=dict(gridcolor="rgba(255,255,255,0.04)", linecolor="rgba(255,255,255,0.06)",
               title="Monthly Revenue (₦K)"),
    legend=dict(font=dict(color="#555"), bgcolor="rgba(8,13,26,0.8)",
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
        <div class="sh-card" style="border-top:3px solid {color};">
            <div style="font-size:10px;font-weight:700;letter-spacing:1.5px;
                text-transform:uppercase;color:{color};margin-bottom:8px;">{label}</div>
            <div style="font-size:28px;font-weight:800;color:#0b1936;letter-spacing:-0.5px;">
                {_fmt(val)}</div>
            <div style="font-size:11px;color:{color};margin-top:4px;font-weight:600;">
                + {_fmt(uplift)} remaining</div>
            <div style="font-size:11px;color:#64748b;margin-top:6px;line-height:1.5;">{desc}</div>
        </div>""", unsafe_allow_html=True)

# ── BY COUNTRY ────────────────────────────────────────────────────────────────
st.markdown('<div class="sh-section">Year-End Forecast by Country</div>', unsafe_allow_html=True)

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
    marker=dict(symbol="diamond", size=14, color="#0b1936",
                line=dict(color="#635bff", width=2)),
    hovertemplate="<b>YTD Actual</b><br>%{x}: ₦%{y:.1f}M<extra></extra>",
))

fig_country.update_layout(
    barmode="group",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(255,255,255,0.02)",
    font=dict(color="#333", size=11), height=360,
    xaxis=dict(gridcolor="rgba(255,255,255,0.04)"),
    yaxis=dict(gridcolor="rgba(255,255,255,0.04)", title="Revenue (₦M)"),
    legend=dict(font=dict(color="#555"), bgcolor="rgba(8,13,26,0.8)",
                bordercolor="rgba(255,255,255,0.08)", borderwidth=1),
    margin=dict(l=0, r=0, t=10, b=0),
)
st.plotly_chart(fig_country, use_container_width=True)

# ── BY RETAILER SUBTYPE ───────────────────────────────────────────────────────
st.markdown('<div class="sh-section">Forecast by Retailer Type</div>', unsafe_allow_html=True)

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
    font=dict(color="#333", size=11),
    xaxis=dict(gridcolor="rgba(255,255,255,0.04)"),
    yaxis=dict(gridcolor="rgba(255,255,255,0.04)"),
    legend=dict(font=dict(color="#555"), bgcolor="rgba(8,13,26,0.8)",
                bordercolor="rgba(255,255,255,0.08)", borderwidth=1),
    margin=dict(l=0, r=0, t=10, b=0),
)
st.plotly_chart(fig_sub, use_container_width=True)

# ── OPPORTUNITY UPLIFT TABLE ──────────────────────────────────────────────────
st.markdown('<div class="sh-section">Revenue Uplift by Opportunity Category</div>',
            unsafe_allow_html=True)
st.markdown("""
<div style="background:rgba(34,197,94,0.06);border:1px solid rgba(34,197,94,0.18);
     border-radius:10px;padding:12px 18px;margin-bottom:14px;font-size:12px;color:#333;line-height:1.6;">
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
st.markdown('<div class="sh-section">Outlet-Level Growth Outlook</div>', unsafe_allow_html=True)
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
st.markdown('<div class="sh-section">Forecast Insights</div>', unsafe_allow_html=True)

total_recoverable = opp_df[
    opp_df["Category"].isin(["Underperforming","Dead Whitespace","Low Performer"])
]["Recoverable Revenue (₦M)"].sum()

bull_upside = (bull_year_end - base_year_end) / 1_000_000

st.markdown(f"""
<div class="sh-insight">
    <span class="sh-badge sh-badge-green" style="margin-bottom:10px;display:inline-block;">Growth Opportunity</span>
    <div class="sh-insight-title">
        {_fmt(total_recoverable * 1_000_000)} Recoverable from Underperforming Outlets</div>
    <div class="sh-insight-body">
        If underperforming and low-performer outlets were brought up to the active outlet median,
        Shalina could recover an additional <strong style="color:#0b1936">{_fmt(total_recoverable * 1_000_000)}</strong>
        in annual revenue without acquiring a single new outlet.
        Focus the commercial team on these existing but underactivated accounts first.
    </div>
</div>
<div class="sh-insight">
    <span class="sh-badge sh-badge-blue" style="margin-bottom:10px;display:inline-block;">Scenario Gap</span>
    <div class="sh-insight-title">
        Bull vs Base Gap is {_fmt((bull_year_end - base_year_end))} — Achievable with Right Actions</div>
    <div class="sh-insight-body">
        The difference between the base and optimistic scenario is
        <strong style="color:#0b1936">{_fmt(bull_year_end - base_year_end)}</strong>.
        This gap is closeable through three levers: activating dead whitespace outlets,
        upselling underperformers, and protecting high-risk active accounts from churning.
        The Churn Prediction and Command Center pages identify exactly which outlets to act on.
    </div>
</div>
<div class="sh-insight">
    <span class="sh-badge sh-badge-amber" style="margin-bottom:10px;display:inline-block;">Time Sensitivity</span>
    <div class="sh-insight-title">
        {months_remaining} Months Left — Every Month of Delay Costs Revenue</div>
    <div class="sh-insight-body">
        With {months_remaining} months remaining in the year, each month of inaction on
        dead whitespace outlets costs approximately
        <strong style="color:#0b1936">{_fmt((bull_year_end - base_year_end) / max(months_remaining, 1))}</strong>
        in potential upside. The activation campaigns should begin immediately to maximise year-end capture.
    </div>
</div>
""", unsafe_allow_html=True)

# ── EXPORT ────────────────────────────────────────────────────────────────────
st.markdown('<div class="sh-section">Export Forecast</div>', unsafe_allow_html=True)

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
