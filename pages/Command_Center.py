import os
import sys

import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fabric_connector import load_data as _load_data


st.set_page_config(
    layout="wide",
    page_title="Command Center | Shalina",
    initial_sidebar_state="expanded",
)


with st.sidebar:
    st.markdown(
        """
        <div style="padding:20px 8px 10px 8px;">
            <div style="font-family:Inter,sans-serif;font-size:10px;font-weight:700;
            color:rgba(100,180,220,0.7);text-transform:uppercase;letter-spacing:2px;margin-bottom:20px;">
                Navigation
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.page_link("app.py", label="Dashboard")
    st.page_link("pages/Command_Center.py", label="Command Center")
    st.page_link("pages/RFM_Analysis.py", label="RFM Analysis")
    st.page_link("pages/Churn_Prediction.py", label="Churn Prediction")
    st.page_link("pages/Upload_Data.py", label="Upload Data")
    st.markdown(
        """
        <div style="margin-top:16px;padding:0 8px;">
            <div style="height:1px;background:linear-gradient(90deg,transparent,
            rgba(33,150,196,0.35),transparent);"></div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if st.button("Refresh Data", use_container_width=True, key="cc_refresh"):
        st.cache_data.clear()
        st.rerun()

    import streamlit.components.v1 as _sc

    _sc.html(
        """<script>(function(){function r(){var n=window.parent.document.querySelector('[data-testid="stSidebarNav"]');if(n){n.remove();}else{setTimeout(r,200);}}r();setTimeout(r,800);setTimeout(r,2500);})();</script>""",
        height=0,
    )


st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500&display=swap');
* { box-sizing: border-box; }
.stApp {
    font-family: 'Inter', sans-serif;
    color: #E2E8F0;
    background: #0d1526;
    min-height: 100vh;
}
.stApp::before {
    content: '';
    position: fixed; inset: 0;
    background:
        radial-gradient(ellipse 70% 48% at 10% 0%, rgba(20,100,220,0.20) 0%, transparent 60%),
        radial-gradient(ellipse 48% 42% at 90% 10%, rgba(100,30,200,0.15) 0%, transparent 55%),
        radial-gradient(ellipse 55% 55% at 50% 100%, rgba(15,90,120,0.18) 0%, transparent 60%);
    pointer-events: none; z-index: 0;
}
.main .block-container {
    background: transparent;
    padding-top: 1rem;
    padding-left: 1.5rem;
    padding-right: 1.5rem;
    max-width: 1500px;
    position: relative;
    z-index: 1;
}
section[data-testid="stSidebar"] {
    background: rgba(8,13,26,0.95) !important;
    border-right: 1px solid rgba(255,255,255,0.06) !important;
}
section[data-testid="stSidebar"] * {
    color: #94A3B8 !important;
    font-family: 'Inter', sans-serif !important;
}
section[data-testid="stSidebar"] a:hover {
    color: #fff !important;
    background: rgba(255,255,255,0.06) !important;
    border-radius: 8px !important;
}
[data-testid="stSidebarNav"],[data-testid="stSidebarNavItems"],section[data-testid="stSidebar"] nav,
[data-testid="stDecoration"],#MainMenu,footer {
    display: none !important;
}
[data-testid="stToolbar"] { display:flex !important; background:transparent !important; }
header[data-testid="stHeader"] { background:transparent !important; }
[data-testid="collapsedControl"],[data-testid="stSidebarCollapseButton"],button[kind="header"] {
    display:flex !important;
    visibility:visible !important;
    opacity:1 !important;
    z-index:999999 !important;
}
[data-testid="stSidebarCollapseButton"] *,
[data-testid="collapsedControl"] *,
[data-testid="stExpandSidebarButton"] * { font-size:0 !important; }
[data-testid="stSidebarCollapseButton"]::before {
    content:"‹";
    color:#94A3B8;
    font-size:26px;
    line-height:1;
}
[data-testid="collapsedControl"]::before,
[data-testid="stExpandSidebarButton"]::before {
    content:"›";
    color:#94A3B8;
    font-size:26px;
    line-height:1;
}
[data-testid="stExpandSidebarButton"] {
    display:flex !important;
    visibility:visible !important;
    opacity:1 !important;
    position:fixed !important;
    top:16px !important;
    left:16px !important;
    width:34px !important;
    height:34px !important;
    min-width:34px !important;
    z-index:999999 !important;
    align-items:center !important;
    justify-content:center !important;
    background:rgba(8,13,26,0.82) !important;
    border:1px solid rgba(255,255,255,0.12) !important;
    border-radius:8px !important;
}
.cc-header {
    padding: 20px 0 16px 0;
    border-bottom: 1px solid rgba(255,255,255,0.06);
    margin-bottom: 18px;
}
.cc-eyebrow {
    font-size: 10px; font-weight: 700; letter-spacing: 3px;
    text-transform: uppercase; color: #5B8DB8; margin-bottom: 6px;
}
.cc-title {
    font-size: 28px; font-weight: 850; color: #F8FAFC;
    letter-spacing: -0.4px; line-height: 1.12;
}
.cc-title span { color: #38BDF8; }
.cc-subtitle {
    color: #8EA7C5; font-size: 13px; line-height: 1.6;
    max-width: 900px; margin-top: 8px;
}
.kpi-grid { display:grid; grid-template-columns:repeat(4,1fr); gap:12px; margin:18px 0 20px; }
.kpi-card {
    border-radius: 10px; padding: 18px 18px 16px; min-height: 118px;
    border: 1px solid rgba(255,255,255,0.08);
    background: rgba(255,255,255,0.035);
    box-shadow: 0 10px 32px rgba(0,0,0,0.22);
}
.kpi-card.blue { background: linear-gradient(135deg,#0f172a 0%,#1e3a5f 100%); border-color: rgba(59,130,246,0.25); }
.kpi-card.green { background: linear-gradient(135deg,#06170e 0%,#0f5132 100%); border-color: rgba(34,197,94,0.25); }
.kpi-card.amber { background: linear-gradient(135deg,#1a1400 0%,#5c4500 100%); border-color: rgba(245,158,11,0.25); }
.kpi-card.red { background: linear-gradient(135deg,#1a0505 0%,#5c1010 100%); border-color: rgba(239,68,68,0.25); }
.kpi-label {
    font-size: 10px; font-weight: 700; color: #7A8DA8;
    letter-spacing: 1.5px; text-transform: uppercase; margin-bottom: 8px;
}
.kpi-value { font-size: 34px; font-weight: 850; color: #F8FAFC; line-height: 1; }
.kpi-note { font-size: 11px; color: #9DB0C8; margin-top: 7px; line-height: 1.35; }
.section-title {
    font-size: 11px; font-weight: 750; letter-spacing: 2px;
    text-transform: uppercase; color: #607692;
    margin-top: 24px; margin-bottom: 12px;
    display: flex; align-items: center; gap: 10px;
}
.section-title::after {
    content: ''; flex: 1; height: 1px;
    background: linear-gradient(90deg,rgba(255,255,255,0.08),transparent);
}
.briefing-grid { display:grid; grid-template-columns:repeat(3,1fr); gap:12px; margin-bottom: 10px; }
.brief-card {
    min-height: 150px;
    border-radius: 10px;
    padding: 16px 18px;
    border: 1px solid rgba(255,255,255,0.08);
    background: rgba(255,255,255,0.03);
}
.brief-tag {
    display:inline-block; padding:3px 9px; border-radius:4px;
    font-size:9px; font-weight:800; letter-spacing:0.9px;
    text-transform:uppercase; margin-bottom:10px;
    background:rgba(56,189,248,0.12); color:#BAE6FD; border:1px solid rgba(56,189,248,0.26);
}
.brief-title { font-size:15px; font-weight:800; color:#F1F5F9; margin-bottom:7px; }
.brief-body { font-size:12px; color:#8EA7C5; line-height:1.55; }
.stSelectbox label,.stSlider label {
    color:#607692 !important; font-size:10px !important; font-weight:800 !important;
    text-transform:uppercase; letter-spacing:1px;
}
[data-baseweb="select"] > div {
    background:rgba(255,255,255,0.04) !important;
    border:1px solid rgba(255,255,255,0.08) !important;
    border-radius:8px !important; color:#E2E8F0 !important;
}
[data-baseweb="popover"] { background:#0f172a !important; border:1px solid rgba(255,255,255,0.1) !important; }
[role="option"] { background:#0f172a !important; color:#E2E8F0 !important; }
[role="option"]:hover { background:rgba(56,189,248,0.15) !important; }
[data-testid="stDataFrame"] { border-radius:10px !important; border:1px solid rgba(255,255,255,0.07) !important; }
.stDownloadButton > button {
    background:rgba(56,189,248,0.14) !important; color:#BAE6FD !important;
    border:1px solid rgba(56,189,248,0.3) !important; border-radius:8px !important;
    font-weight:700 !important;
}
@media (max-width: 900px) {
    .kpi-grid, .briefing-grid { grid-template-columns: 1fr; }
}
</style>
""",
    unsafe_allow_html=True,
)


@st.cache_data(show_spinner=False)
def load():
    return _load_data()


df_all, data_source, data_status = load()
if df_all is None or df_all.empty:
    st.error("No data available. Please check Fabric access or the CSV fallback.")
    st.stop()


def money(v):
    value = float(v or 0)
    if abs(value) >= 1_000_000:
        return f"{value / 1_000_000:.1f}M"
    if abs(value) >= 1_000:
        return f"{value / 1_000:.1f}K"
    return f"{value:,.0f}"


def compact(v):
    value = float(v or 0)
    if abs(value) >= 1_000_000:
        return f"{value / 1_000_000:.1f}M"
    if abs(value) >= 1_000:
        return f"{value / 1_000:.1f}K"
    return f"{value:,.0f}"


def gps_in_bounds(row):
    bounds = {
        "Nigeria": (2.5, 15.0, 2.5, 15.5),
        "Angola": (-19.0, -3.5, 10.5, 25.5),
    }.get(row.get("country"), (-90.0, 90.0, -180.0, 180.0))
    lat_min, lat_max, lon_min, lon_max = bounds
    return lat_min <= row["latitude"] <= lat_max and lon_min <= row["longitude"] <= lon_max


def next_action(row):
    if row["Opportunity"] == "Dead Whitespace":
        return "Recover outlet: verify status, assign visit, restart order cycle"
    if row["Opportunity"] == "Underperforming":
        return "Field visit: benchmark against nearby performers and push core SKUs"
    if row["Opportunity"] == "Low Performer":
        return "Upsell: check product mix and distributor service cadence"
    if row["Opportunity"] == "High Performer":
        return "Protect account: keep supply stable and use as local benchmark"
    return "Maintain: monitor performance and service consistency"


df = df_all.copy()
df["YTD Retailing Value"] = pd.to_numeric(df["YTD Retailing Value"], errors="coerce").fillna(0)
df["latitude"] = pd.to_numeric(df["latitude"], errors="coerce")
df["longitude"] = pd.to_numeric(df["longitude"], errors="coerce")
df = df.dropna(subset=["latitude", "longitude"])
df["Retailer Subtype"] = df["Retailer Subtype"].astype(str).replace({"nan": "Unknown"})
df["Opportunity"] = df["Opportunity"].astype(str)
df["gps_valid"] = df.apply(gps_in_bounds, axis=1)

st.markdown(
    """
    <div class="cc-header">
        <div class="cc-eyebrow">Shalina Healthcare &nbsp;&middot;&nbsp; Boardroom Decision Layer</div>
        <div class="cc-title">AI Whitespace <span>Command Center</span></div>
        <div class="cc-subtitle">
            Converts outlet, revenue, GPS, and opportunity signals into a prioritized commercial action plan.
            Existing dashboards remain unchanged; this page sits on top as the presentation-ready decision view.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

left, mid, right = st.columns([1.1, 1.1, 1])
with left:
    country = st.selectbox("Market", ["All"] + sorted(df["country"].dropna().unique().tolist()))
with mid:
    subtype_options = ["All"] + sorted(df["Retailer Subtype"].dropna().unique().tolist())
    subtype = st.selectbox("Retailer Type", subtype_options)
with right:
    activation_count = st.slider("Activation Scenario", 50, 1000, 250, 50)

view = df.copy()
if country != "All":
    view = view[view["country"] == country]
if subtype != "All":
    view = view[view["Retailer Subtype"] == subtype]

if view.empty:
    st.warning("No outlets match the selected filters.")
    st.stop()

active = view[view["YTD Retailing Value"] > 0]
targets = view[view["Opportunity"].isin(["Dead Whitespace", "Underperforming", "Low Performer"])].copy()

benchmark = (
    active.groupby(["country", "Retailer Subtype"])["YTD Retailing Value"].median().rename("peer_median")
)
targets = targets.join(benchmark, on=["country", "Retailer Subtype"])
fallback_median = active["YTD Retailing Value"].median() if len(active) else view["YTD Retailing Value"].median()
targets["peer_median"] = targets["peer_median"].fillna(fallback_median).fillna(0)
targets["revenue_gap"] = (targets["peer_median"] - targets["YTD Retailing Value"]).clip(lower=0)

targets["lat_bin"] = (targets["latitude"] / 0.25).round() * 0.25
targets["lon_bin"] = (targets["longitude"] / 0.25).round() * 0.25
zone_stats = (
    targets.groupby(["country", "lat_bin", "lon_bin"], as_index=False)
    .agg(
        zone_outlets=("Shop Name", "count"),
        zone_gap=("revenue_gap", "sum"),
        zone_dead=("Opportunity", lambda s: int((s == "Dead Whitespace").sum())),
        zone_under=("Opportunity", lambda s: int((s == "Underperforming").sum())),
        latitude=("latitude", "mean"),
        longitude=("longitude", "mean"),
    )
)

targets = targets.merge(
    zone_stats[["country", "lat_bin", "lon_bin", "zone_outlets", "zone_gap"]],
    on=["country", "lat_bin", "lon_bin"],
    how="left",
)

severity = {
    "Dead Whitespace": 1.0,
    "Underperforming": 0.72,
    "Low Performer": 0.45,
    "Active": 0.15,
    "High Performer": 0.05,
}
gap_rank = targets["revenue_gap"].rank(pct=True).fillna(0)
density_rank = targets["zone_outlets"].rank(pct=True).fillna(0)
targets["priority_score"] = (
    targets["Opportunity"].map(severity).fillna(0.2) * 48
    + gap_rank * 34
    + density_rank * 18
)
targets.loc[~targets["gps_valid"], "priority_score"] *= 0.72
targets["priority_score"] = targets["priority_score"].clip(0, 100).round(1)
targets["Next Best Action"] = targets.apply(next_action, axis=1)

action_plan = targets.sort_values(
    ["priority_score", "revenue_gap", "zone_outlets"], ascending=False
).head(max(activation_count, 50))

scenario_base = action_plan.head(activation_count)
conversion_rate = 0.35
scenario_uplift = scenario_base["revenue_gap"].sum() * conversion_rate
dead_count = int((view["Opportunity"] == "Dead Whitespace").sum())
under_count = int((view["Opportunity"] == "Underperforming").sum())
valid_gps_pct = float(view["gps_valid"].mean() * 100) if len(view) else 0

st.markdown(
    f"""
    <div class="kpi-grid">
        <div class="kpi-card blue">
            <div class="kpi-label">Outlets In Scope</div>
            <div class="kpi-value">{compact(len(view))}</div>
            <div class="kpi-note">{country if country != "All" else "Nigeria + Angola"} filtered commercial universe</div>
        </div>
        <div class="kpi-card red">
            <div class="kpi-label">Dead Whitespace</div>
            <div class="kpi-value">{compact(dead_count)}</div>
            <div class="kpi-note">Outlets with zero YTD value requiring recovery validation</div>
        </div>
        <div class="kpi-card amber">
            <div class="kpi-label">Underperforming</div>
            <div class="kpi-value">{compact(under_count)}</div>
            <div class="kpi-note">Active but below local commercial threshold</div>
        </div>
        <div class="kpi-card green">
            <div class="kpi-label">Scenario Value Gap</div>
            <div class="kpi-value">{money(scenario_uplift)}</div>
            <div class="kpi-note">At {int(conversion_rate * 100)}% recovery on top {activation_count} priorities</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

top_zone = zone_stats.sort_values(["zone_gap", "zone_outlets"], ascending=False).head(1)
top_zone_text = "No priority zone available"
if not top_zone.empty:
    z = top_zone.iloc[0]
    top_zone_text = (
        f"{z['country']} zone near {z['latitude']:.2f}, {z['longitude']:.2f} has "
        f"{int(z['zone_outlets'])} target outlets and {money(z['zone_gap'])} estimated gap."
    )

top_outlet_text = "No outlet priorities available"
if not action_plan.empty:
    o = action_plan.iloc[0]
    top_outlet_text = (
        f"{o['Shop Name']} is the highest-priority outlet with score {o['priority_score']:.1f}, "
        f"{o['Opportunity']} status, and {money(o['revenue_gap'])} peer gap."
    )

quality_text = (
    f"{valid_gps_pct:.1f}% of selected outlets have GPS inside expected country bounds. "
    "Prioritize corrections before sending field teams into weak-coordinate areas."
)

st.markdown('<div class="section-title">Executive Briefing</div>', unsafe_allow_html=True)
st.markdown(
    f"""
    <div class="briefing-grid">
        <div class="brief-card">
            <div class="brief-tag">Where To Attack</div>
            <div class="brief-title">Highest-density opportunity zone</div>
            <div class="brief-body">{top_zone_text}</div>
        </div>
        <div class="brief-card">
            <div class="brief-tag">Who To Visit First</div>
            <div class="brief-title">Priority outlet recommendation</div>
            <div class="brief-body">{top_outlet_text}</div>
        </div>
        <div class="brief-card">
            <div class="brief-tag">Data Confidence</div>
            <div class="brief-title">GPS reliability check</div>
            <div class="brief-body">{quality_text}</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

chart_left, chart_right = st.columns([1.15, 0.85])
with chart_left:
    st.markdown('<div class="section-title">Priority Zone Map</div>', unsafe_allow_html=True)
    map_zones = zone_stats.sort_values("zone_gap", ascending=False).head(80)
    if not map_zones.empty:
        fig_map = px.scatter_mapbox(
            map_zones,
            lat="latitude",
            lon="longitude",
            size="zone_outlets",
            color="zone_gap",
            hover_name="country",
            hover_data={
                "zone_outlets": True,
                "zone_dead": True,
                "zone_under": True,
                "zone_gap": ":,.0f",
                "latitude": ":.3f",
                "longitude": ":.3f",
            },
            color_continuous_scale=["#38BDF8", "#F59E0B", "#EF4444"],
            size_max=38,
            zoom=4 if country == "All" else 5,
            height=450,
        )
        center_lat = view["latitude"].mean()
        center_lon = view["longitude"].mean()
        fig_map.update_layout(
            mapbox_style="open-street-map",
            mapbox_center={"lat": center_lat, "lon": center_lon},
            margin=dict(l=0, r=0, t=0, b=0),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#E2E8F0"),
        )
        st.plotly_chart(fig_map, use_container_width=True)
    else:
        st.info("No target zones available for the selected filters.")

with chart_right:
    st.markdown('<div class="section-title">Action Mix</div>', unsafe_allow_html=True)
    action_mix = (
        action_plan.head(activation_count)["Opportunity"]
        .value_counts()
        .rename_axis("Opportunity")
        .reset_index(name="Outlets")
    )
    if not action_mix.empty:
        fig_mix = px.bar(
            action_mix,
            x="Outlets",
            y="Opportunity",
            orientation="h",
            color="Opportunity",
            color_discrete_map={
                "Dead Whitespace": "#EF4444",
                "Underperforming": "#F59E0B",
                "Low Performer": "#38BDF8",
            },
            height=450,
        )
        fig_mix.update_layout(
            showlegend=False,
            margin=dict(l=0, r=0, t=0, b=0),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#E2E8F0"),
            xaxis=dict(gridcolor="rgba(255,255,255,0.08)"),
            yaxis=dict(gridcolor="rgba(255,255,255,0.0)"),
        )
        st.plotly_chart(fig_mix, use_container_width=True)

st.markdown('<div class="section-title">Field Action Plan</div>', unsafe_allow_html=True)
show_cols = [
    "Shop Name",
    "country",
    "Retailer Subtype",
    "Opportunity",
    "YTD Retailing Value",
    "peer_median",
    "revenue_gap",
    "zone_outlets",
    "priority_score",
    "Next Best Action",
]
display_plan = action_plan[show_cols].rename(
    columns={
        "country": "Country",
        "peer_median": "Peer Median",
        "revenue_gap": "Estimated Gap",
        "zone_outlets": "Nearby Targets",
        "priority_score": "Priority Score",
    }
)
st.dataframe(display_plan.head(activation_count), use_container_width=True, hide_index=True)

# ── EXPORT BUTTONS ────────────────────────────────────────────────────────────
st.markdown('<div class="section-title">Export</div>', unsafe_allow_html=True)

_cc_filename = f"shalina_command_center_{country.lower().replace(' ', '_')}"
_cc_export_df = display_plan.head(activation_count)

dl1, dl2, dl3 = st.columns([1, 1, 4])

with dl1:
    csv = _cc_export_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        "⬇ Download CSV",
        data=csv,
        file_name=f"{_cc_filename}.csv",
        mime="text/csv",
        use_container_width=True,
    )

with dl2:
    import io
    _xl = io.BytesIO()
    with pd.ExcelWriter(_xl, engine="openpyxl") as _xw:
        _cc_export_df.to_excel(_xw, index=False, sheet_name="Action Plan")
        # Second sheet: full target universe
        targets[["Shop Name", "country", "Retailer Subtype", "Opportunity",
                  "YTD Retailing Value", "revenue_gap", "priority_score",
                  "Next Best Action"]].sort_values(
            "priority_score", ascending=False
        ).to_excel(_xw, index=False, sheet_name="All Targets")
    _xl.seek(0)
    st.download_button(
        "⬇ Download Excel",
        data=_xl,
        file_name=f"{_cc_filename}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True,
    )

# ── WRITE-BACK TO FABRIC ──────────────────────────────────────────────────────
st.markdown('<div class="section-title">Fabric Write-Back</div>', unsafe_allow_html=True)
st.markdown("""
<div style="background:rgba(56,189,248,0.05);border:1px solid rgba(56,189,248,0.2);
     border-radius:12px;padding:14px 20px;margin-bottom:12px;">
    <div style="font-size:12px;color:#BAE6FD;font-weight:600;margin-bottom:4px;">
        Publish whitespace scores back to your Fabric warehouse</div>
    <div style="font-size:11px;color:#64748B;line-height:1.6;">
        Creates a <code style="color:#BAE6FD">WhitespaceScores</code> table in Fabric containing
        every outlet's opportunity category and revenue gap. Available immediately in Power BI.
        Requires FABRIC_SQL_ENDPOINT to be configured.
    </div>
</div>
""", unsafe_allow_html=True)

if st.button("Push Whitespace Scores to Fabric", key="btn_write_whitespace"):
    with st.spinner("Writing whitespace scores to Fabric warehouse..."):
        from fabric_connector import write_whitespace_scores
        result = write_whitespace_scores(df_all)
    if result["success"]:
        st.success(f"✅ {result['rows_written']:,} outlet scores written to "
                   f"[dbo].[WhitespaceScores] in Fabric.")
    else:
        st.error(f"❌ Write-back failed: {result['error']}")
