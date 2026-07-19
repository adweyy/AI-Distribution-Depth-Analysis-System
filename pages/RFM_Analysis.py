import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import os, sys

# Ensure root project directory is on path
_here = os.path.dirname(os.path.abspath(__file__))
_root = os.path.dirname(_here)
if _root not in sys.path:
    sys.path.insert(0, _root)
if _here not in sys.path:
    sys.path.insert(0, _here)

from fabric_connector import load_data as _load_data, load_rfm_data as _load_rfm
from styles import apply_styles, sidebar_nav

st.set_page_config(layout="wide", page_title="RFM Analysis | Shalina", initial_sidebar_state="expanded")

sidebar_nav(refresh_key="rfm_refresh")
apply_styles()

# ── LOAD DATA ─────────────────────────────────────────────────────────────────

# (removed legacy FX block)

df_all, _, _ = _load_data()

if df_all is None:
    st.error("No data available. Please check Fabric connection or add shalina_combined_data.csv.")
    st.stop()

# ── PAGE HEADER ───────────────────────────────────────────────────────────────
st.markdown("""
<div class="sh-topbar">
    <div>
        <div class="sh-eyebrow">Shalina Healthcare &nbsp;&middot;&nbsp; Predictive Analytics</div>
        <div class="sh-title">RFM <span class="sh-title-dim">Analysis</span></div>
    </div>
    <div class="sh-pill-group">
        <div class="sh-pill"><div class="sh-dot"></div>SYSTEM ONLINE</div>
    </div>
</div>""", unsafe_allow_html=True)

# ── COUNTRY SWITCHER ──────────────────────────────────────────────────────────
if "rfm_country" not in st.session_state:
    st.session_state.rfm_country = "Nigeria"

st.markdown("<div style='margin:14px 0 8px 0;font-size:9px;font-weight:700;color:#635bff;text-transform:uppercase;letter-spacing:3px;'>Select Country</div>", unsafe_allow_html=True)
cc1, cc2, cc3 = st.columns([1, 1, 8])
with cc1:
    if st.button("Nigeria", use_container_width=True, key="rfm_ng"):
        st.session_state.rfm_country = "Nigeria"
with cc2:
    if st.button("Angola", use_container_width=True, key="rfm_ao"):
        st.session_state.rfm_country = "Angola"

country = st.session_state.rfm_country
df = df_all[df_all['country'] == country].copy()

accent = "#4CAF50" if country == "Nigeria" else "#CE93D8"
st.markdown(f"<div style='height:3px;background:linear-gradient(90deg,{accent},transparent);border-radius:2px;margin-bottom:16px;'></div>", unsafe_allow_html=True)

chart_layout = dict(
    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#94a3b8", size=12), height=380,
    xaxis=dict(gridcolor="rgba(99,91,255,0.08)", linecolor="rgba(99,91,255,0.10)", color="#94a3b8"),
    yaxis=dict(gridcolor="rgba(99,91,255,0.08)", linecolor="rgba(99,91,255,0.10)", color="#94a3b8"),
    margin=dict(l=0, r=0, t=20, b=0),
    legend=dict(font=dict(color="#e2e8f0"), bgcolor="rgba(22,27,39,0.95)",
                bordercolor="rgba(99,91,255,0.15)", borderwidth=1)
)

#  TRY REAL SFA TRANSACTION DATA 
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

    rfm_mode_label = "  Real RFM — SFA Transaction Data (Recency · Frequency · Monetary)"
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

    rfm_mode_label = "  Proxy RFM — YTD Sales Value (SFA data not yet available)"
    rfm_mode_color = "#F9A825"
    rfm_mode_sub   = ("R & M derived from YTD Retailing Value · F estimated from outlet type · "
                      "Activate real RFM: grant admin consent in Azure AD for Shalina-Whitespace-App")

#  MODE BANNER 
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

#  SEGMENTATION 
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
    'Hibernating':       '#333',
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

#  KPI ROW 
champs = seg_counts.get('Champions', 0)
loyal  = seg_counts.get('Loyal Customers', 0)
at_risk= seg_counts.get('At Risk', 0)
lost   = seg_counts.get('Lost', 0)

st.markdown(f"""
<div class="sh-kpi-row">
    <div class="sh-kpi purple">
        <div class="sh-kpi-label">Champions</div>
        <div class="sh-kpi-value">{champs:,}</div>
        <div class="sh-kpi-delta">RFM score ≥ 12 — top accounts</div>
    </div>
    <div class="sh-kpi green">
        <div class="sh-kpi-label">Loyal Customers</div>
        <div class="sh-kpi-value">{loyal:,}</div>
        <div class="sh-kpi-delta">Consistent high-value outlets</div>
    </div>
    <div class="sh-kpi gold">
        <div class="sh-kpi-label">At Risk</div>
        <div class="sh-kpi-value">{at_risk:,}</div>
        <div class="sh-kpi-delta">Were good — need urgent outreach</div>
    </div>
    <div class="sh-kpi red">
        <div class="sh-kpi-label">Lost</div>
        <div class="sh-kpi-value">{lost:,}</div>
        <div class="sh-kpi-delta">Zero engagement — reassess</div>
    </div>
</div>
""", unsafe_allow_html=True)

#  CHARTS 
c1, c2 = st.columns([3, 2])
with c1:
    st.markdown('<div class="sh-section">Segment Distribution</div>', unsafe_allow_html=True)
    seg_df = seg_counts.reset_index()
    seg_df.columns = ['Segment', 'Count']
    fig_seg = px.bar(seg_df, x='Count', y='Segment', orientation='h',
                     color='Segment', color_discrete_map=seg_colors, text='Count')
    fig_seg.update_traces(textposition='outside', textfont=dict(color='#FFFFFF', size=11))
    fig_seg.update_layout(**chart_layout)
    st.plotly_chart(fig_seg, use_container_width=True)

with c2:
    st.markdown('<div class="sh-section">Avg Monetary by Segment</div>', unsafe_allow_html=True)
    avg_m = rfm[rfm['M_raw'] > 0].groupby('Segment')['M_raw'].mean().reset_index()
    avg_m.columns = ['Segment', 'Avg Value']
    avg_m = avg_m.sort_values('Avg Value', ascending=False)
    fig_avg = px.bar(avg_m, x='Segment', y='Avg Value',
                     color='Segment', color_discrete_map=seg_colors)
    fig_avg.update_layout(**chart_layout)
    fig_avg.update_xaxes(tickangle=45)
    st.plotly_chart(fig_avg, use_container_width=True)

#  OUTLET TABLE 
st.markdown('<div class="sh-section">Full Outlet RFM Table</div>', unsafe_allow_html=True)
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
st.download_button(" Export RFM Scores", csv_rfm,
                   f"rfm_analysis_{country.lower()}.csv", "text/csv", key="rfm_export")

#  ACTION PLAYBOOK 
st.markdown('<div class="sh-section">Segment Action Playbook</div>', unsafe_allow_html=True)
action_cols = st.columns(2)
for i, (seg, action) in enumerate(seg_actions.items()):
    count = seg_counts.get(seg, 0)
    color = seg_colors.get(seg, '#2196C4')
    with action_cols[i % 2]:
        st.markdown(f"""
        <div class="sh-insight sh-card" style="border-left:4px solid {color};margin-bottom:10px;">
            <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:5px;">
                <div class="sh-insight-title" style="color:{color};">{seg}</div>
                <div style="font-family:'Poppins',sans-serif;font-size:18px;font-weight:700;color:#FFFFFF;">{count:,}</div>
            </div>
            <div class="sh-insight-body">{action}</div>
        </div>
        """, unsafe_allow_html=True)

