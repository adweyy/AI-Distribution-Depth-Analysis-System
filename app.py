import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import os
import sys as _sys
_sys.path.insert(0, os.path.dirname(__file__))
from styles import apply_styles, sidebar_nav

st.set_page_config(
    layout="wide",
    page_title="Shalina | Distribution Intelligence",
    initial_sidebar_state="expanded"
)

# ── SESSION STATE INIT ────────────────────────────────────────────
if "country"         not in st.session_state: st.session_state.country         = "Nigeria"
if "nav_page"        not in st.session_state: st.session_state.nav_page        = "Dashboard"
if "selected_outlet" not in st.session_state: st.session_state.selected_outlet = None

# ── SIDEBAR ───────────────────────────────────────────────────────
sidebar_nav(refresh_key="refresh_data")

# Outlet search (sidebar part 2 — added after data loads below)
with st.sidebar:
    pass  # sidebar_nav() above already handles nav

# ── STYLES ───────────────────────────────────────────────────────
apply_styles(active_page=st.session_state.get("nav_page","Dashboard"))

# ── LOAD DATA ─────────────────────────────────────────────────────
import sys, os as _os
sys.path.insert(0, _os.path.dirname(__file__))
from fabric_connector import load_data as _load_data

df_all, data_source, data_status = _load_data()

if df_all is None:
    st.markdown(
        '<div style="background:rgba(200,50,50,0.2);border:1px solid rgba(255,80,80,0.4);'
        'border-radius:12px;padding:16px 20px;color:#FFAAAA;font-weight:600;font-size:13px;">'
        'No data available. Please add shalina_combined_data.csv or configure Fabric credentials in .env'
        '</div>', unsafe_allow_html=True
    )
    st.stop()

# ── HELPERS ───────────────────────────────────────────────────────
def get_stats(df):
    nonzero = df[df['YTD Retailing Value'] > 0]['YTD Retailing Value']
    p25  = nonzero.quantile(0.25) if len(nonzero) else 0
    mean = nonzero.mean()         if len(nonzero) else 0
    p75  = nonzero.quantile(0.75) if len(nonzero) else 0
    return p25, mean, p75

def gps_quality(df, country):
    """Return (valid_count, total_count, pct_valid) for a country dataframe."""
    _bounds_map = {
        "Nigeria": dict(lat_min=2.5, lat_max=15.0, lon_min=2.5,  lon_max=15.5),
        "Angola":  dict(lat_min=-19.0,lat_max=-3.5,lon_min=10.5, lon_max=25.5),
    }
    b = _bounds_map.get(country, dict(lat_min=-90,lat_max=90,lon_min=-180,lon_max=180))
    valid = df[
        df['latitude'].notna()  & df['longitude'].notna() &
        (df['latitude']  != 0)  & (df['longitude']  != 0) &
        (df['latitude'].abs()  > 0.01) &
        (df['longitude'].abs() > 0.01) &
        df['latitude'].between(b['lat_min'],  b['lat_max']) &
        df['longitude'].between(b['lon_min'], b['lon_max'])
    ]
    total = max(len(df), 1)
    return len(valid), len(df), round(len(valid) / total * 100, 1)

def delta_html(value, low, high, reverse=False, prefix="", suffix="",
               label_lo="low", label_mid="moderate", label_hi="strong"):
    if reverse:
        if value > high:   color, arrow, lbl = "#EF4444", "&#8593;", label_hi
        elif value > low:  color, arrow, lbl = "#F59E0B", "&#8593;", label_mid
        else:              color, arrow, lbl = "#22C55E", "&#8595;", label_lo
    else:
        if value >= high:  color, arrow, lbl = "#22C55E", "&#8593;", label_hi
        elif value >= low: color, arrow, lbl = "#F59E0B", "&#8594;", label_mid
        else:              color, arrow, lbl = "#EF4444", "&#8595;", label_lo
    return (f'<span style="color:{color};font-weight:700;">{arrow} '
            f'{prefix}{value:.1f}{suffix}</span>'
            f'<span style="color:{color};opacity:0.75;"> &mdash; {lbl}</span>')

color_map = {
    'Dead Whitespace': '#EF4444',
    'Underperforming': '#F97316',
    'Low Performer':   '#EAB308',
    'Active':          '#22C55E',
    'High Performer':  '#A855F7'
}
chart_layout = dict(
    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(255,255,255,0.02)",
    font=dict(color="#8b949e", size=11), height=380,
    xaxis=dict(gridcolor="rgba(99,91,255,0.05)", linecolor="rgba(99,91,255,0.08)", color="#4a4a6a"),
    yaxis=dict(gridcolor="rgba(99,91,255,0.05)", linecolor="rgba(99,91,255,0.08)", color="#4a4a6a"),
    margin=dict(l=0, r=0, t=20, b=0),
    legend=dict(font=dict(color="#8b8fa8"), bgcolor="rgba(15,15,28,0.95)",
                bordercolor="rgba(99,91,255,0.14)", borderwidth=1)
)

# ── SIDEBAR PART 2 : Outlet Search ────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="margin-top:20px;padding:0 8px;">
        <div style="height:1px;background:rgba(255,255,255,0.04);"></div>
    </div>""", unsafe_allow_html=True)
    st.markdown("""
    <div style='margin-top:20px;padding:0 8px;font-family:Inter,sans-serif;font-size:9px;
         font-weight:700;color:#3d4a5c;text-transform:uppercase;
         letter-spacing:3px;margin-bottom:8px;'>Outlet Search</div>
    """, unsafe_allow_html=True)

    search_q   = st.text_input("", placeholder="Type a shop name...",
                               key="outlet_search_input", label_visibility="collapsed")
    _s_country = st.session_state.get("country", "Nigeria")
    _s_df      = df_all[df_all['country'] == _s_country]

    if search_q and len(search_q) >= 2:
        _matches = _s_df[_s_df['Shop Name'].str.contains(search_q, case=False, na=False)]
        if len(_matches) > 0:
            _names  = _matches['Shop Name'].tolist()[:20]
            _chosen = st.selectbox("", _names, key="outlet_pick", label_visibility="collapsed")
            if st.button("View Details", key="btn_view_outlet", use_container_width=True):
                st.session_state.selected_outlet = _chosen
                st.rerun()
        else:
            st.markdown(
                "<div style='color:#333;font-size:11px;padding:4px 0 0 2px;'>No outlets found.</div>",
                unsafe_allow_html=True
            )

    if st.session_state.selected_outlet:
        if st.button("Clear Drill-down", key="btn_clear_outlet", use_container_width=True):
            st.session_state.selected_outlet = None
            st.rerun()

# ── TOP BAR ───────────────────────────────────────────────────────
sync_label = "DATA SYNC: STABLE" if data_status in ("live","hybrid") else "DATA SYNC: CSV"

import base64 as _b64
_logo_file = next(
    (f for f in ['shalina_healthcare_logo.jfif','shalina_healthcare_logo.png','shalina_logo.png']
     if _os.path.exists(f)), None
)
if _logo_file:
    _logo_ext  = 'jpeg' if _logo_file.endswith('.jfif') else 'png'
    _logo_b64  = _b64.b64encode(open(_logo_file,'rb').read()).decode()
    _logo_mime = f'image/{_logo_ext}'
else:
    _logo_mime = 'image/png'
    _logo_b64  = ("iVBORw0KGgoAAAANSUhEUgAAAjAAAACMCAYAAABRTFQrAAAABmJLR0QA"
                  "/wD/AP+gvaeTAAAADUlEQVQI12NgYGD4DwABBAEBhc9HaQAAAABJRU5ErkJggg==")

# ── TOP BAR ───────────────────────────────────────────────────────
is_live   = data_status == "live"
is_hybrid = data_status == "hybrid"
status_label = data_source
status_sub = (
    "Live — both countries pulling from Microsoft Fabric" if is_live else
    ("Hybrid — one country live, one on CSV fallback" if is_hybrid else
     "CSV fallback — Fabric unreachable")
)
dot_color = "#22C55E" if is_live else ("#6EC6F5" if is_hybrid else "#F59E0B")
_dot_cls  = "" if is_live else ("" if is_hybrid else "sh-dot-amber")
_dot_cls2 = "sh-dot-amber" if data_status == "csv" else ""

logo_col, title_col = st.columns([1, 11])
with logo_col:
    st.markdown(
        f'<img src="data:{_logo_mime};base64,{_logo_b64}" style="height:64px;width:auto;margin-top:6px;opacity:1;border-radius:8px;" />',
        unsafe_allow_html=True
    )
with title_col:
    st.markdown(f"""
    <div class="sh-topbar">
        <div>
            <div class="sh-eyebrow">Shalina Healthcare &nbsp;&middot;&nbsp; Distribution Intelligence</div>
            <div class="sh-title">Distribution <span class="sh-title-dim">Depth</span> Analysis</div>
        </div>
        <div class="sh-pill-group">
            <div class="sh-pill"><div class="sh-dot"></div>SYSTEM ONLINE</div>
            <div class="sh-pill"><div class="sh-dot {_dot_cls2}"></div>{sync_label}</div>
        </div>
    </div>""", unsafe_allow_html=True)

# ── DATA SOURCE BANNER ────────────────────────────────────────────
st.markdown(f"""
<div class="sh-banner">
    <div style="width:8px;height:8px;border-radius:50%;background:{dot_color};
         box-shadow:0 0 8px {dot_color};flex-shrink:0;
         animation:sh-pulse 2.2s ease-in-out infinite;"></div>
    <div style="flex:1;">
        <div style="font-size:13px;font-weight:700;color:#fff;">{status_label}</div>
        <div style="font-size:11px;color:#6b7280;margin-top:2px;">{status_sub}</div>
    </div>
    <div style="display:flex;gap:16px;align-items:center;">
        <div style="display:flex;align-items:center;gap:6px;font-size:9px;color:#6b7280;font-weight:700;text-transform:uppercase;letter-spacing:2px;">
            <div style="width:5px;height:5px;border-radius:50%;background:#22C55E;"></div>Live Fabric
        </div>
        <div style="display:flex;align-items:center;gap:6px;font-size:9px;color:#6b7280;font-weight:700;text-transform:uppercase;letter-spacing:2px;">
            <div style="width:5px;height:5px;border-radius:50%;background:#6EC6F5;"></div>Hybrid
        </div>
        <div style="display:flex;align-items:center;gap:6px;font-size:9px;color:#6b7280;font-weight:700;text-transform:uppercase;letter-spacing:2px;">
            <div style="width:5px;height:5px;border-radius:50%;background:#F59E0B;"></div>CSV
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── COUNTRY SWITCHER ──────────────────────────────────────────────
st.markdown(
    "<div style='margin:14px 0 8px 0;font-family:Inter,sans-serif;font-size:9px;font-weight:700;"
    "color:#635bff;text-transform:uppercase;letter-spacing:3px;'>Select Country</div>",
    unsafe_allow_html=True
)
cc1, cc2, cc3 = st.columns([1, 1, 8])
with cc1:
    if st.button("Nigeria", use_container_width=True, key="btn_ng"):
        st.session_state.country = "Nigeria"
        st.session_state.selected_outlet = None
with cc2:
    if st.button("Angola", use_container_width=True, key="btn_ao"):
        st.session_state.country = "Angola"
        st.session_state.selected_outlet = None

country    = st.session_state.country
df_country = df_all[df_all['country'] == country].copy()
p25, mean_val, p75 = get_stats(df_country)

accent = "#635bff"
st.markdown(
    f"<div style='height:1px;background:linear-gradient(90deg,{accent}88,transparent);margin-bottom:20px;'></div>",
    unsafe_allow_html=True
)

# ── NAVBAR ────────────────────────────────────────────────────────
st.markdown("""
<div style="background:#1c2333;border:1px solid rgba(99,91,255,0.18);
     border-radius:12px;padding:5px;display:flex;gap:4px;margin-bottom:4px;">
</div>""", unsafe_allow_html=True)
n1, n2, n3, n4 = st.columns(4)
with n1:
    if st.button("Dashboard",            use_container_width=True, key="nav_dash"):
        st.session_state.nav_page = "Dashboard"
with n2:
    if st.button("Outlet Performance",   use_container_width=True, key="nav_perf"):
        st.session_state.nav_page = "Outlet Performance"
with n3:
    if st.button("Whitespace Detection", use_container_width=True, key="nav_white"):
        st.session_state.nav_page = "Whitespace Detection"
with n4:
    if st.button("Expansion Strategy",   use_container_width=True, key="nav_expand"):
        st.session_state.nav_page = "Expansion Strategy"

st.markdown(
    f'<div id="shalina-active-page" data-page="{st.session_state.nav_page}" style="display:none;"></div>',
    unsafe_allow_html=True
)

# ── FILTERS────────────────────────────────────────────
st.markdown("<div style='margin-top:12px;'></div>", unsafe_allow_html=True)
f1, f2 = st.columns(2)
with f1:
    subtype_opts     = ["All"] + sorted(df_country['Retailer Subtype'].dropna().unique().tolist())
    selected_subtype = st.selectbox("Retailer Subtype", subtype_opts)
with f2:
    opp_opts         = ["All","Dead Whitespace","Underperforming","Low Performer","Active","High Performer"]
    selected_opp     = st.selectbox("Opportunity Category", opp_opts)

df = df_country.copy()
if selected_subtype != "All": df = df[df['Retailer Subtype'] == selected_subtype]
if selected_opp      != "All": df = df[df['Opportunity']      == selected_opp]

if len(df) == 0:
    st.markdown(
        '<div style="background:rgba(200,50,50,0.15);border:1px solid rgba(255,100,100,0.4);'
        'border-radius:10px;padding:14px 16px;font-size:13px;color:#FFAAAA;'
        'font-weight:600;margin:16px 0;">No outlets match the selected filters.</div>',
        unsafe_allow_html=True
    )
    st.stop()

map_center = {"lat": 9.0, "lon": 8.0}  if country == "Nigeria" else {"lat": -11.0, "lon": 17.5}
map_zoom   = 5 if country == "Nigeria" else 4

# ── OUTLET DRILL-DOWN ─────────────────────────────────────────────
if st.session_state.selected_outlet:
    _name = st.session_state.selected_outlet
    _rows = df_country[df_country['Shop Name'] == _name]

    if len(_rows) == 0:
        st.session_state.selected_outlet = None
    else:
        _o      = _rows.iloc[0]
        _ytd    = float(_o.get('YTD Retailing Value', 0))
        _sub    = str(_o.get('Retailer Subtype', '—'))
        _opp    = str(_o.get('Opportunity', '—'))
        _lat    = float(_o.get('latitude',  0))
        _lon    = float(_o.get('longitude', 0))
        _pct    = float((df_country['YTD Retailing Value'] <= _ytd).sum() / max(len(df_country),1) * 100)
        _avg    = float(df_country['YTD Retailing Value'].mean())
        _vs_avg = ((_ytd - _avg) / _avg * 100) if _avg > 0 else 0

        # Validate coordinates:
        # Step 1 — basic sanity (NaN, 0,0, out of Earth range)
        # Step 2 — must land inside a generous country bounding box
        #           catches junk defaults like (0.5, 6.7) near São Tomé
        #           Boxes are deliberately wide (+2° buffer on every edge)
        _COUNTRY_BOUNDS = {
            "Nigeria": dict(lat_min=2.5,  lat_max=15.0, lon_min=2.5,  lon_max=15.5),
            "Angola":  dict(lat_min=-19.0,lat_max=-3.5, lon_min=10.5, lon_max=25.5),
        }
        _bounds = _COUNTRY_BOUNDS.get(country, dict(lat_min=-90, lat_max=90, lon_min=-180, lon_max=180))
        try:
            _lat_f = float(_lat)
            _lon_f = float(_lon)
            _coords_valid = (
                not np.isnan(_lat_f) and not np.isnan(_lon_f)
                and not (_lat_f == 0 and _lon_f == 0)           # exact ocean default
                and abs(_lat_f) > 0.01 and abs(_lon_f) > 0.01  # near-zero catch
                and _bounds['lat_min'] <= _lat_f <= _bounds['lat_max']
                and _bounds['lon_min'] <= _lon_f <= _bounds['lon_max']
            )
            _lat = _lat_f
            _lon = _lon_f
        except (ValueError, TypeError):
            _coords_valid = False

        _palette = {
            'Dead Whitespace': ('#EF4444', 'rgba(239,68,68,0.15)'),
            'Underperforming': ('#F97316', 'rgba(249,115,22,0.15)'),
            'Low Performer':   ('#EAB308', 'rgba(234,179,8,0.15)'),
            'Active':          ('#22C55E', 'rgba(34,197,94,0.15)'),
            'High Performer':  ('#A855F7', 'rgba(168,85,247,0.15)'),
        }
        _opp_clr, _opp_bg = _palette.get(_opp, ('#94A3B8', 'rgba(148,163,184,0.15)'))
        _vs_clr   = "#22C55E" if _vs_avg >= 0 else "#EF4444"
        _vs_arrow = "&#8593;" if _vs_avg >= 0 else "&#8595;"
        _pct_clr  = "#22C55E" if _pct >= 66 else ("#F59E0B" if _pct >= 33 else "#EF4444")

        st.markdown(f"""
        <div class="sh-odc">
            <div class="sh-odc-tag">Outlet Detail View</div>
            <div class="sh-odc-name">{_name}</div>
            <div class="sh-odc-meta">
                <span style="background:{_opp_bg};color:{_opp_clr};border:1px solid {_opp_clr}55;
                    border-radius:4px;padding:3px 10px;font-size:10px;font-weight:700;
                    letter-spacing:0.5px;text-transform:uppercase;">{_opp}</span>
                <span style="color:#475569;font-size:11px;">&middot;</span>
                <span style="color:#64748B;font-size:11px;">{_sub}</span>
                <span style="color:#475569;font-size:11px;">&middot;</span>
                <span style="color:#64748B;font-size:11px;">{country}</span>
                <span style="color:#475569;font-size:11px;">&middot;</span>
                <span style="color:#475569;font-size:11px;font-family:'JetBrains Mono',monospace;">
                    {'No GPS data' if not _coords_valid else f'{_lat:.4f}, {_lon:.4f}'}</span>
            </div>
            <div class="sh-odc-stats">
                <div class="sh-odc-stat">
                    <div class="sh-odc-stat-label">YTD Revenue</div>
                    <div class="sh-odc-stat-value" style="color:#F1F5F9;">&#8358;{_ytd:,.1f}K</div>
                </div>
                <div class="sh-odc-divider"></div>
                <div class="sh-odc-stat">
                    <div class="sh-odc-stat-label">Percentile Rank</div>
                    <div class="sh-odc-stat-value" style="color:{_pct_clr};">
                        {_pct:.0f}<span style="font-size:13px;color:#475569;">th</span></div>
                </div>
                <div class="sh-odc-divider"></div>
                <div class="sh-odc-stat">
                    <div class="sh-odc-stat-label">vs Country Avg</div>
                    <div class="sh-odc-stat-value" style="color:{_vs_clr};">
                        {_vs_arrow} {abs(_vs_avg):.1f}%</div>
                </div>
                <div class="sh-odc-divider"></div>
                <div class="sh-odc-stat">
                    <div class="sh-odc-stat-label">Country Avg YTD</div>
                    <div class="sh-odc-stat-value" style="color:#94A3B8;font-size:16px;">
                        &#8358;{_avg:,.1f}K</div>
                </div>
            </div>
        </div>""", unsafe_allow_html=True)

        # ── Mini map — only render when coordinates are valid ────────
        # ── Section label ──────────────────────────────────────────
        st.markdown('<div class="sh-section">Outlet Location</div>', unsafe_allow_html=True)

        if _coords_valid:
            # ── Nearby outlets within 0.3° — valid coordinates only ──
            _nearby = df_country[
                df_country['latitude'].between(_lat - 0.3, _lat + 0.3) &
                df_country['longitude'].between(_lon - 0.3, _lon + 0.3) &
                df_country['latitude'].between(_bounds['lat_min'], _bounds['lat_max']) &
                df_country['longitude'].between(_bounds['lon_min'], _bounds['lon_max']) &
                (df_country['latitude']  != 0) &
                (df_country['longitude'] != 0)
            ].copy()

            # Ensure the selected outlet is always in the frame even if it
            # appears in zero nearby outlets (edge case with duplicate names)
            if _name not in _nearby['Shop Name'].values:
                _nearby = df_country[df_country['Shop Name'] == _name].copy()

            # Size: selected outlet is a large pin; neighbours are small dots
            _nearby['_sz']    = np.where(_nearby['Shop Name'] == _name, 32, 6)
            _nearby['_label'] = np.where(_nearby['Shop Name'] == _name,
                                          'Selected: ' + _nearby['Shop Name'],
                                          _nearby['Shop Name'])

            # Add a dedicated "YOU ARE HERE" pin row so it always sits on top
            _pin_df = _nearby[_nearby['Shop Name'] == _name].copy()
            _ctx_df = _nearby[_nearby['Shop Name'] != _name].copy()

            import plotly.graph_objects as go

            _fig_loc = go.Figure()

            # Layer 1 — context outlets (small coloured dots)
            for _opp_cat, _opp_hex in color_map.items():
                _sub_ctx = _ctx_df[_ctx_df['Opportunity'] == _opp_cat]
                if len(_sub_ctx) == 0:
                    continue
                _fig_loc.add_trace(go.Scattermapbox(
                    lat=_sub_ctx['latitude'],
                    lon=_sub_ctx['longitude'],
                    mode='markers',
                    marker=dict(size=7, color=_opp_hex, opacity=0.65),
                    text=_sub_ctx['Shop Name'] + '<br>' + _opp_cat +
                         '<br>YTD: ₦' + _sub_ctx['YTD Retailing Value'].apply(lambda x: f'{x:,.1f}') + 'K',
                    hoverinfo='text',
                    name=_opp_cat,
                    showlegend=True,
                ))

            # Layer 2 — selected outlet (large glowing pin)
            if len(_pin_df) > 0:
                _pin_color = color_map.get(_opp, '#3B82F6')
                _fig_loc.add_trace(go.Scattermapbox(
                    lat=_pin_df['latitude'],
                    lon=_pin_df['longitude'],
                    mode='markers+text',
                    marker=dict(
                        size=22,
                        color=_pin_color,
                        opacity=1.0,
                        symbol='circle',
                    ),
                    text=[_name],
                    textposition='top right',
                    textfont=dict(size=11, color='#FFFFFF'),
                    hovertext=f'<b>{_name}</b><br>{_opp}<br>{_sub}<br>YTD: ₦{_ytd:,.1f}K',
                    hoverinfo='text',
                    name=f'Selected: {_name}',
                    showlegend=True,
                ))

                # Outer ring for the selected pin
                _fig_loc.add_trace(go.Scattermapbox(
                    lat=_pin_df['latitude'],
                    lon=_pin_df['longitude'],
                    mode='markers',
                    marker=dict(size=34, color=_pin_color, opacity=0.25),
                    hoverinfo='skip',
                    showlegend=False,
                ))

            _fig_loc.update_layout(
                mapbox=dict(
                    style='carto-darkmatter',
                    center=dict(lat=_lat, lon=_lon),
                    zoom=13,
                ),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                height=380,
                margin=dict(l=0, r=0, t=0, b=0),
                legend=dict(
                    font=dict(color='#94A3B8', size=10),
                    bgcolor='rgba(8,13,26,0.85)',
                    bordercolor='rgba(255,255,255,0.08)',
                    borderwidth=1,
                    x=0, y=1,
                ),
                uirevision='outlet_map',
            )

            _mc, _cc = st.columns([10, 1])
            with _mc:
                st.plotly_chart(_fig_loc, use_container_width=True, key="drill_map")
            with _cc:
                st.markdown("<div style='height:160px;'></div>", unsafe_allow_html=True)
                if st.button("Close", key="close_drill", use_container_width=True):
                    st.session_state.selected_outlet = None
                    st.rerun()

        else:
            # No valid GPS — professional data quality notice
            _gps_valid_n, _gps_total_n, _gps_pct = gps_quality(df_country, country)
            _gps_missing = _gps_total_n - _gps_valid_n
            st.markdown(f"""
            <div style="display:flex;gap:16px;align-items:flex-start;
                background:rgba(15,25,50,0.6);border:1px solid rgba(255,255,255,0.08);
                border-radius:12px;padding:18px 20px;margin-bottom:16px;">
                <div style="width:36px;height:36px;border-radius:8px;flex-shrink:0;
                    background:rgba(245,158,11,0.12);border:1px solid rgba(245,158,11,0.3);
                    display:flex;align-items:center;justify-content:center;">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none"
                        stroke="#F59E0B" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <circle cx="12" cy="12" r="10"/>
                        <line x1="12" y1="8" x2="12" y2="12"/>
                        <line x1="12" y1="16" x2="12.01" y2="16"/>
                    </svg>
                </div>
                <div style="flex:1;">
                    <div style="font-size:13px;font-weight:700;color:#F1F5F9;margin-bottom:4px;">
                        GPS Coordinates Unavailable</div>
                    <div style="font-size:11px;color:#64748B;line-height:1.7;">
                        This outlet has a placeholder coordinate
                        <span style="font-family:'JetBrains Mono',monospace;color:#F59E0B;
                            background:rgba(245,158,11,0.1);padding:1px 6px;border-radius:4px;">
                            {_lat:.4f}, {_lon:.4f}</span>
                        assigned by the source system instead of a real GPS location.
                        All revenue and performance stats above are accurate.
                    </div>
                    <div style="margin-top:10px;padding-top:10px;
                        border-top:1px solid rgba(255,255,255,0.06);
                        display:flex;gap:20px;">
                        <div>
                            <div style="font-size:9px;font-weight:700;letter-spacing:1.5px;
                                text-transform:uppercase;color:#475569;margin-bottom:3px;">
                                Valid GPS in {country}</div>
                            <div style="font-size:15px;font-weight:800;color:#22C55E;">
                                {_gps_valid_n:,}
                                <span style="font-size:11px;color:#475569;font-weight:400;">
                                    / {_gps_total_n:,} outlets ({_gps_pct}%)</span>
                            </div>
                        </div>
                        <div>
                            <div style="font-size:9px;font-weight:700;letter-spacing:1.5px;
                                text-transform:uppercase;color:#475569;margin-bottom:3px;">
                                Missing GPS</div>
                            <div style="font-size:15px;font-weight:800;color:#F59E0B;">
                                {_gps_missing:,}
                                <span style="font-size:11px;color:#475569;font-weight:400;">
                                    outlets require re-geocoding</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>""", unsafe_allow_html=True)
            if st.button("Close", key="close_drill"):
                st.session_state.selected_outlet = None
                st.rerun()

# ── PAGE ROUTING ──────────────────────────────────────────────────
page = st.session_state.nav_page

# ══════════════════════════════════════════════════════════════════
#  DASHBOARD
# ══════════════════════════════════════════════════════════════════
if page == "Dashboard":
    total_outlets   = len(df)
    dead_outlets    = len(df[df['Opportunity'] == 'Dead Whitespace'])
    high_performers = len(df[df['Opportunity'] == 'High Performer'])
    total_ytd       = df['YTD Retailing Value'].sum()
    ws_pct          = dead_outlets   / max(total_outlets, 1) * 100
    hp_pct          = high_performers / max(total_outlets, 1) * 100
    active_df       = df[df['YTD Retailing Value'] > 0]
    avg_per_outlet  = active_df['YTD Retailing Value'].mean() if len(active_df) else 0

    _ws_delta = delta_html(ws_pct, 20, 35, reverse=True, suffix="%",
                           label_lo="managed", label_mid="elevated", label_hi="critical")
    _hp_delta = delta_html(hp_pct,  8, 15, suffix="%",
                           label_lo="low", label_mid="moderate", label_hi="strong")

    st.markdown(f"""
    <div class="sh-kpi-row">
        <div class="sh-kpi">
            <div class="sh-kpi-accent" style="background:linear-gradient(90deg,#635bff,transparent);"></div>
            <div class="sh-kpi-label">Total Outlets &mdash; {country}</div>
            <div class="sh-kpi-value">{total_outlets:,}</div>
            <div class="sh-kpi-delta">Distribution network</div>
        </div>
        <div class="sh-kpi">
            <div class="sh-kpi-accent" style="background:linear-gradient(90deg,#dc2626,transparent);"></div>
            <div class="sh-kpi-label">Dead Whitespace</div>
            <div class="sh-kpi-value">{dead_outlets:,}</div>
            <div class="sh-kpi-delta">{_ws_delta} of outlets</div>
        </div>
        <div class="sh-kpi">
            <div class="sh-kpi-accent" style="background:linear-gradient(90deg,#635bff,transparent);"></div>
            <div class="sh-kpi-label">High Performers</div>
            <div class="sh-kpi-value">{high_performers:,}</div>
            <div class="sh-kpi-delta">{_hp_delta} of network</div>
        </div>
        <div class="sh-kpi">
            <div class="sh-kpi-accent" style="background:linear-gradient(90deg,#d97706,transparent);"></div>
            <div class="sh-kpi-label">Total YTD Revenue</div>
            <div class="sh-kpi-value" style="font-size:42px;">&#8358;{total_ytd/1000:,.0f}M</div>
            <div class="sh-kpi-delta">Avg &#8358;{avg_per_outlet:,.0f}K per active outlet</div>
        </div>
    </div>""", unsafe_allow_html=True)

    st.markdown('<div class="sh-section">Geographic Outlet Distribution</div>', unsafe_allow_html=True)
    # Filter rows with valid coordinates before mapping
    _valid_coords = (
        df['latitude'].notna()  & df['longitude'].notna() &
        (df['latitude']  != 0)  & (df['longitude']  != 0) &
        df['latitude'].between(*([2,16]   if country=='Nigeria' else [-20,-2])) &
        df['longitude'].between(*([1,17]  if country=='Nigeria' else [9,27]))
    )
    _map_src = df[_valid_coords]
    map_df = (_map_src.sample(min(5000,len(_map_src)), random_state=42) if len(_map_src)>5000 else _map_src).copy()
    map_df['_size'] = map_df['YTD Retailing Value'].clip(lower=0).fillna(0)
    if map_df['_size'].sum() == 0: map_df['_size'] = 1
    fig_map = px.scatter_mapbox(map_df, lat="latitude", lon="longitude",
        color="Opportunity", color_discrete_map=color_map, size="_size",
        size_max=14, zoom=map_zoom, height=520, hover_name="Shop Name",
        hover_data={"YTD Retailing Value":":,.1f","Retailer Subtype":True,"latitude":False,"longitude":False},
        center=map_center)
    fig_map.update_traces(marker=dict(opacity=0.85))
    fig_map.update_layout(mapbox_style="carto-darkmatter", paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        legend=dict(font=dict(color="#888",size=11), bgcolor="rgba(5,5,5,0.92)",
                    bordercolor="rgba(255,255,255,0.06)", borderwidth=1),
        margin=dict(l=0,r=0,t=0,b=0))
    st.plotly_chart(fig_map, use_container_width=True)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="sh-section">Opportunity Breakdown</div>', unsafe_allow_html=True)
        opp_counts = df['Opportunity'].value_counts().reset_index()
        opp_counts.columns = ['Category','Count']
        fig_pie = px.pie(opp_counts, values='Count', names='Category',
                         color='Category', color_discrete_map=color_map, hole=0.5)
        fig_pie.update_layout(paper_bgcolor="rgba(0,0,0,0)",
                               legend=dict(font=dict(color="#FFFFFF")),
                               font=dict(color="#90C8E8"), margin=dict(l=0,r=0,t=20,b=0))
        st.plotly_chart(fig_pie, use_container_width=True)
    with c2:
        st.markdown('<div class="sh-section">Retailer Subtype Split</div>', unsafe_allow_html=True)
        sub_counts = df['Retailer Subtype'].value_counts().reset_index()
        sub_counts.columns = ['Type','Count']
        fig_bar = px.bar(sub_counts, x='Type', y='Count', color='Type',
                         color_discrete_sequence=['#A855F7','#2196C4','#22C55E'])
        fig_bar.update_layout(**chart_layout)
        st.plotly_chart(fig_bar, use_container_width=True)

# ══════════════════════════════════════════════════════════════════
#  OUTLET PERFORMANCE
# ══════════════════════════════════════════════════════════════════
elif page == "Outlet Performance":
    st.markdown('<div class="sh-section">Top 20 Outlets by YTD Retailing Value</div>', unsafe_allow_html=True)
    top20 = (df[df['YTD Retailing Value']>0]
             .nlargest(20,'YTD Retailing Value')
             [['Shop Name','Retailer Subtype','YTD Retailing Value','Opportunity']]
             .reset_index(drop=True))
    top20.index += 1
    top20['YTD Retailing Value'] = top20['YTD Retailing Value'].apply(lambda x: f"\u20a6{x:,.1f}K")
    st.dataframe(top20, use_container_width=True)

    st.markdown('<div class="sh-section">YTD Revenue Distribution</div>', unsafe_allow_html=True)
    active_df = df[df['YTD Retailing Value'] > 0]
    fig_hist = px.histogram(active_df, x='YTD Retailing Value', nbins=60,
                             color='Retailer Subtype',
                             color_discrete_sequence=['#A855F7','#2196C4','#22C55E'])
    fig_hist.update_layout(**chart_layout)
    st.plotly_chart(fig_hist, use_container_width=True)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="sh-section">Avg YTD by Opportunity Category</div>', unsafe_allow_html=True)
        avg_opp = df[df['YTD Retailing Value']>0].groupby('Opportunity')['YTD Retailing Value'].mean().reset_index()
        fig_avg = px.bar(avg_opp, x='YTD Retailing Value', y='Opportunity', orientation='h',
                         color='Opportunity', color_discrete_map=color_map)
        fig_avg.update_layout(**chart_layout)
        st.plotly_chart(fig_avg, use_container_width=True)
    with c2:
        st.markdown('<div class="sh-section">Avg YTD by Retailer Subtype</div>', unsafe_allow_html=True)
        avg_sub = df[df['YTD Retailing Value']>0].groupby('Retailer Subtype')['YTD Retailing Value'].mean().reset_index()
        fig_sub = px.bar(avg_sub, x='Retailer Subtype', y='YTD Retailing Value',
                         color='Retailer Subtype',
                         color_discrete_sequence=['#A855F7','#2196C4','#22C55E'])
        fig_sub.update_layout(**chart_layout)
        st.plotly_chart(fig_sub, use_container_width=True)

# ══════════════════════════════════════════════════════════════════
#  WHITESPACE DETECTION
# ══════════════════════════════════════════════════════════════════
elif page == "Whitespace Detection":
    dead  = df_country[df_country['Opportunity'] == 'Dead Whitespace']
    under = df_country[df_country['Opportunity'] == 'Underperforming']
    total_ws          = len(dead) + len(under)
    ws_network_pct    = round(total_ws / max(len(df_country), 1) * 100, 1)
    revenue_potential = total_ws * mean_val

    _dead_pct    = len(dead)  / max(len(df_country), 1) * 100
    _under_pct   = len(under) / max(len(df_country), 1) * 100
    _dead_delta  = delta_html(_dead_pct,  15, 30, reverse=True, suffix="%",
                              label_lo="managed", label_mid="elevated", label_hi="critical")
    _under_delta = delta_html(_under_pct, 10, 25, reverse=True, suffix="%",
                              label_lo="low", label_mid="moderate", label_hi="high")

    st.markdown(f"""
    <div class="sh-kpi-row">
        <div class="sh-kpi">
            <div class="sh-kpi-accent" style="background:linear-gradient(90deg,#ef4444,transparent);"></div>
            <div class="sh-kpi-label">Dead Whitespace Outlets</div>
            <div class="sh-kpi-value">{len(dead):,}</div>
            <div class="sh-kpi-delta">{_dead_delta} of network</div>
        </div>
        <div class="sh-kpi">
            <div class="sh-kpi-accent" style="background:linear-gradient(90deg,#f97316,transparent);"></div>
            <div class="sh-kpi-label">Underperforming Outlets</div>
            <div class="sh-kpi-value">{len(under):,}</div>
            <div class="sh-kpi-delta">{_under_delta} of network</div>
        </div>
        <div class="sh-kpi">
            <div class="sh-kpi-accent" style="background:linear-gradient(90deg,#3b82f6,transparent);"></div>
            <div class="sh-kpi-label">Total Whitespace</div>
            <div class="sh-kpi-value">{total_ws:,}</div>
            <div class="sh-kpi-delta">{ws_network_pct}% of all {country} outlets</div>
        </div>
        <div class="sh-kpi">
            <div class="sh-kpi-accent" style="background:linear-gradient(90deg,#22c55e,transparent);"></div>
            <div class="sh-kpi-label">Revenue Potential</div>
            <div class="sh-kpi-value" style="font-size:40px;">&#8358;{revenue_potential/1000:,.0f}M</div>
            <div class="sh-kpi-delta">If activated to avg performance</div>
        </div>
    </div>""", unsafe_allow_html=True)

    st.markdown('<div class="sh-section">Whitespace Outlets Map</div>', unsafe_allow_html=True)
    _ws_valid = (
        df_country['latitude'].notna()  & df_country['longitude'].notna() &
        (df_country['latitude']  != 0)  & (df_country['longitude']  != 0) &
        df_country['latitude'].between(*([2,16]   if country=='Nigeria' else [-20,-2])) &
        df_country['longitude'].between(*([1,17]  if country=='Nigeria' else [9,27]))
    )
    ws_df  = df_country[df_country['Opportunity'].isin(['Dead Whitespace','Underperforming']) & _ws_valid]
    map_ws = ws_df.sample(min(4000,len(ws_df)), random_state=42) if len(ws_df) > 4000 else ws_df
    fig_ws = px.scatter_mapbox(map_ws, lat="latitude", lon="longitude",
        color="Opportunity", color_discrete_map=color_map,
        zoom=map_zoom, height=480, hover_name="Shop Name",
        hover_data={"YTD Retailing Value":":,.1f","Retailer Subtype":True,"latitude":False,"longitude":False},
        center=map_center)
    fig_ws.update_layout(mapbox_style="carto-darkmatter", paper_bgcolor="rgba(0,0,0,0)",
        legend=dict(font=dict(color="#b0bac9",size=11), bgcolor="rgba(15,22,41,0.88)",
                    bordercolor="rgba(99,91,255,0.20)", borderwidth=1),
        margin=dict(l=0,r=0,t=0,b=0))
    st.plotly_chart(fig_ws, use_container_width=True)

    st.markdown('<div class="sh-section">Dead Whitespace Outlet List</div>', unsafe_allow_html=True)
    dead_show = dead[['Shop Name','Retailer Subtype','latitude','longitude']].reset_index(drop=True)
    dead_show.index += 1
    st.dataframe(dead_show, use_container_width=True)
    csv = dead_show.to_csv().encode('utf-8')
    st.download_button("Export Dead Whitespace List", csv,
                       f"dead_whitespace_{country.lower()}.csv", "text/csv")

# ══════════════════════════════════════════════════════════════════
#  EXPANSION STRATEGY
# ══════════════════════════════════════════════════════════════════
elif page == "Expansion Strategy":
    dead     = df_country[df_country['Opportunity'] == 'Dead Whitespace']
    under    = df_country[df_country['Opportunity'] == 'Underperforming']
    active   = df_country[df_country['Opportunity'].isin(['Active','High Performer'])]
    pri_dead = dead[dead['Retailer Subtype'].str.contains('Primary', case=False, na=False)]
    sec_dead = dead[~dead['Retailer Subtype'].str.contains('Primary', case=False, na=False)]

    st.markdown(f"""
    <div class="sh-insight sh-card">
        <span class="badge badge-dead">Critical Priority</span>
        <div class="sh-insight-title">Activate {len(pri_dead):,} Dead Primary Outlets</div>
        <div class="sh-insight-body">Primary outlets with zero YTD sales require immediate field sales intervention.
        Revenue potential: <strong style="color:#FFFFFF">&#8358;{len(pri_dead)*mean_val/1000:,.0f}M</strong></div>
    </div>
    <div class="sh-insight sh-card">
        <span class="badge badge-under">High Priority</span>
        <div class="sh-insight-title">Convert {len(sec_dead):,} Dead Secondary Outlets</div>
        <div class="sh-insight-body">Secondary outlets with zero sales — largest untapped pool.
        Revenue potential: <strong style="color:#FFFFFF">&#8358;{len(sec_dead)*mean_val/1000:,.0f}M</strong></div>
    </div>
    <div class="sh-insight sh-card">
        <span class="badge badge-low">Medium Priority</span>
        <div class="sh-insight-title">Scale Up {len(under):,} Underperforming Outlets</div>
        <div class="sh-insight-body">Outlets selling below &#8358;{p25:,.0f}K YTD. Incremental revenue potential:
        <strong style="color:#FFFFFF">&#8358;{len(under)*(mean_val-p25)/1000:,.0f}M</strong></div>
    </div>
    <div class="sh-insight sh-card">
        <span class="badge badge-high">Growth Opportunity</span>
        <div class="sh-insight-title">Replicate {len(active):,} High-Performing Outlet Profiles</div>
        <div class="sh-insight-body">Analyse shared characteristics of active and high-performing outlets
        to identify new locations with equivalent potential.</div>
    </div>""", unsafe_allow_html=True)

    st.markdown('<div class="sh-section">Active vs Whitespace by Retailer Type</div>', unsafe_allow_html=True)
    summary = df.groupby(['Retailer Subtype','Opportunity']).size().reset_index(name='Count')
    fig_grp = px.bar(summary, x='Retailer Subtype', y='Count', color='Opportunity',
                     color_discrete_map=color_map, barmode='stack')
    fig_grp.update_layout(**chart_layout)
    st.plotly_chart(fig_grp, use_container_width=True)
