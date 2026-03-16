"""
Shalina Healthcare — Data Connector (Hybrid Mode)

Nigeria  → live from Microsoft Fabric (Final Nigeria table, YTD Retailing Value)
           falls back to CSV if Fabric is unreachable
Angola   → live from Microsoft Fabric (Angola - Chemist table, YTD Sales Value)
           falls back to CSV if Fabric is unreachable

Both countries attempt live Fabric connection first.
Status: 'live' = both live, 'hybrid' = one live, 'csv' = both CSV
"""

import requests
import pandas as pd
import numpy as np
import os
from dotenv import load_dotenv

_env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
load_dotenv(_env_path)


# ── SECRET READER ──────────────────────────────────────────────────────────────
def _get_secret(key):
    """Read from Streamlit secrets (cloud) or .env (local)."""
    val = None
    try:
        import streamlit as st
        if hasattr(st, 'secrets') and key in st.secrets:
            val = st.secrets[key]
    except Exception:
        pass
    if not val:
        val = os.getenv(key)
    if val:
        val = str(val).strip().strip('"').strip("'").strip()
    return val or None


# ── AUTH ───────────────────────────────────────────────────────────────────────
def _get_access_token():
    tenant = _get_secret("FABRIC_TENANT_ID")
    client = _get_secret("FABRIC_CLIENT_ID")
    secret = _get_secret("FABRIC_CLIENT_SECRET")
    if not all([tenant, client, secret]):
        raise Exception(f"Missing credentials: TENANT={bool(tenant)} CLIENT={bool(client)} SECRET={bool(secret)}")
    url = f"https://login.microsoftonline.com/{tenant}/oauth2/v2.0/token"
    r = requests.post(url, data={
        "grant_type":    "client_credentials",
        "client_id":     client,
        "client_secret": secret,
        "scope":         "https://analysis.windows.net/powerbi/api/.default"
    }, timeout=15)
    if r.status_code != 200:
        raise Exception(f"Auth failed {r.status_code}: {r.text[:200]}")
    return r.json()["access_token"]


# ── DAX RUNNER ─────────────────────────────────────────────────────────────────
def _run_dax(token, dax_query):
    workspace = _get_secret("FABRIC_WORKSPACE_ID") or "ccf72308-6884-43ee-a116-3d86fbe1553f"
    dataset   = _get_secret("FABRIC_DATASET_ID")   or "4aea9823-3813-4fc8-a146-a7c5f986bf0a"
    url = f"https://api.powerbi.com/v1.0/myorg/groups/{workspace}/datasets/{dataset}/executeQueries"
    r = requests.post(url,
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
        json={"queries": [{"query": dax_query}], "serializerSettings": {"includeNulls": True}},
        timeout=60)
    if r.status_code != 200:
        raise Exception(f"DAX failed {r.status_code}: {r.text[:150]}")
    rows = r.json()["results"][0]["tables"][0].get("rows", [])
    return pd.DataFrame(rows)


# ── NIGERIA — always from CSV ──────────────────────────────────────────────────
def _load_nigeria_from_csv(csv_path):
    """
    Load Nigeria data from shalina_combined_data.csv.
    This CSV has 33,588 outlets with real YTD Retailing Values — far richer
    than the live Fabric table which has no YTD column.
    """
    df_csv = pd.read_csv(csv_path)
    ng = df_csv[df_csv['country'] == 'Nigeria'].copy()
    # Normalise column names
    ng['YTD Retailing Value'] = pd.to_numeric(ng['YTD Retailing Value'], errors='coerce').fillna(0)
    ng['latitude']  = pd.to_numeric(ng['latitude'],  errors='coerce')
    ng['longitude'] = pd.to_numeric(ng['longitude'], errors='coerce')
    ng = ng.dropna(subset=['latitude', 'longitude'])
    ng['country'] = 'Nigeria'
    return ng


# ── ANGOLA — live from Fabric ──────────────────────────────────────────────────
def _fetch_angola_live(token):
    dax = """
    EVALUATE
    SELECTCOLUMNS(
        FILTER('Angola - Chemist', 'Angola - Chemist'[Lat] <> BLANK()),
        "Shop Name",           'Angola - Chemist'[Retailer/Chemist Name],
        "latitude",            'Angola - Chemist'[Lat],
        "longitude",           'Angola - Chemist'[Long],
        "Retailer Subtype",    'Angola - Chemist'[Type],
        "YTD Retailing Value", 'Angola - Chemist'[YTD Sales Value]
    )
    """
    df = _run_dax(token, dax)
    df.columns = ['Shop Name', 'latitude', 'longitude', 'Retailer Subtype', 'YTD Retailing Value']
    df['country'] = 'Angola'
    return df


def _load_angola_from_csv(csv_path):
    df_csv = pd.read_csv(csv_path)
    ao = df_csv[df_csv['country'] == 'Angola'].copy()
    ao['YTD Retailing Value'] = pd.to_numeric(ao['YTD Retailing Value'], errors='coerce').fillna(0)
    ao['latitude']  = pd.to_numeric(ao['latitude'],  errors='coerce')
    ao['longitude'] = pd.to_numeric(ao['longitude'], errors='coerce')
    ao = ao.dropna(subset=['latitude', 'longitude'])
    ao['country'] = 'Angola'
    return ao

# ── NIGERIA — live from Fabric ─────────────────────────────────────────────────
def _fetch_nigeria_live(token):
    dax = """
    EVALUATE
    SELECTCOLUMNS(
        FILTER('Final Nigeria',
            'Final Nigeria'[latitude] <> BLANK() &&
            'Final Nigeria'[longitude] <> BLANK()
        ),
        "Shop Name",           'Final Nigeria'[name],
        "latitude",            'Final Nigeria'[latitude],
        "longitude",           'Final Nigeria'[longitude],
        "Retailer Subtype",    'Final Nigeria'[Retailer Subtype],
        "YTD Retailing Value", 'Final Nigeria'[YTD Retailing Value]
    )
    """
    df = _run_dax(token, dax)
    df.columns = ['Shop Name', 'latitude', 'longitude', 'Retailer Subtype', 'YTD Retailing Value']
    df['country'] = 'Nigeria'
    return df




# ── CLEAN & CLASSIFY ───────────────────────────────────────────────────────────
def _clean(df):
    df['latitude']            = pd.to_numeric(df['latitude'],            errors='coerce')
    df['longitude']           = pd.to_numeric(df['longitude'],           errors='coerce')
    df['YTD Retailing Value'] = pd.to_numeric(df['YTD Retailing Value'], errors='coerce').fillna(0)
    df['Retailer Subtype']    = df['Retailer Subtype'].astype(str)\
        .str.replace(' Customers', '', regex=False).str.strip()
    df = df.dropna(subset=['latitude', 'longitude'])
    return df


def _classify(df):
    results = []
    for country in df['country'].unique():
        sub     = df[df['country'] == country].copy()
        nonzero = sub[sub['YTD Retailing Value'] > 0]['YTD Retailing Value']
        if len(nonzero) == 0:
            sub['Opportunity'] = 'Dead Whitespace'
            results.append(sub)
            continue
        p25  = nonzero.quantile(0.25)
        mean = nonzero.mean()
        p75  = nonzero.quantile(0.75)
        def clf(v, p25=p25, mean=mean, p75=p75):
            if v == 0:      return 'Dead Whitespace'
            elif v < p25:   return 'Underperforming'
            elif v < mean:  return 'Low Performer'
            elif v < p75:   return 'Active'
            else:           return 'High Performer'
        sub['Opportunity'] = sub['YTD Retailing Value'].apply(clf)
        results.append(sub)
    return pd.concat(results, ignore_index=True)


# ── MAIN LOAD ──────────────────────────────────────────────────────────────────
def load_data():
    """
    Hybrid strategy:
      Nigeria  → CSV (always)        — 33,588 outlets, real YTD
      Angola   → Fabric live first   — 5,819 outlets, real YTD
               → CSV fallback        — 5,656 outlets, real YTD

    Returns: (DataFrame, source_label, status)
      status = 'hybrid'  : Nigeria=CSV, Angola=Fabric live
      status = 'csv'     : Both from CSV (Fabric unreachable)
      status = 'error'   : No data at all
    """
    import streamlit as st

    @st.cache_data(ttl=3600)
    def _cached():
        csv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "shalina_combined_data.csv")
        csv_exists = os.path.exists(csv_path)

        # Try to get Fabric token once for both countries
        token = None
        try:
            tid = _get_secret("FABRIC_TENANT_ID")
            cid = _get_secret("FABRIC_CLIENT_ID")
            sec = _get_secret("FABRIC_CLIENT_SECRET")
            if all([tid, cid, sec]):
                token = _get_access_token()
        except Exception:
            token = None

        # Try Nigeria from Fabric live
        ng = None
        nigeria_status = "csv"
        if token:
            try:
                ng = _fetch_nigeria_live(token)
                nigeria_status = "live"
            except Exception:
                ng = None

        # Fall back to Nigeria from CSV
        if ng is None:
            if not csv_exists:
                return None, "No data — shalina_combined_data.csv not found", "error"
            ng = _load_nigeria_from_csv(csv_path)
            nigeria_status = "csv"

        # Try Angola from Fabric live
        ao = None
        angola_status = "csv"
        if token:
            try:
                ao = _fetch_angola_live(token)
                angola_status = "live"
            except Exception:
                ao = None

        # Fall back to Angola from CSV
        if ao is None:
            if csv_exists:
                ao = _load_angola_from_csv(csv_path)
            else:
                ao = ng.iloc[0:0].copy()
            angola_status = "csv"

        df = pd.concat([ng, ao], ignore_index=True)
        df = _clean(df)
        df = _classify(df)

        if nigeria_status == "live" and angola_status == "live":
            label  = "Connected to Microsoft Fabric Warehouse"
            status = "live"
        elif nigeria_status == "live" or angola_status == "live":
            live_c = "Nigeria" if nigeria_status == "live" else "Angola"
            csv_c  = "Angola"  if nigeria_status == "live" else "Nigeria"
            label  = f"{live_c}: Live Fabric  |  {csv_c}: CSV fallback"
            status = "hybrid"
        else:
            label  = "Nigeria + Angola: CSV (Fabric unreachable)"
            status = "csv"

        return df, label, status

    return _cached()


# ══════════════════════════════════════════════════════════════════════════════
# REAL RFM — SFA TRANSACTION DATA
# ══════════════════════════════════════════════════════════════════════════════
# Once IT grants service principal access to "SFA Reports - UAT", this pulls
# real transaction-level data: last order date, order count, total spend.
# Until then, load_rfm_data() returns None and the app falls back to YTD proxy.
#
# TO ACTIVATE:
#   1. Ask IT to grant the service principal (Shalina-Whitespace-App) access
#      to the "SFA Reports - UAT" semantic model in the UAT workspace.
#   2. Set FABRIC_SFA_DATASET_ID in .env / Streamlit secrets to the correct ID.
#   3. Update the DAX column names below to match the actual SFA table schema.
# ══════════════════════════════════════════════════════════════════════════════

# SFA Reports - UAT dataset ID (partial — confirm full GUID with IT)
_SFA_DATASET_ID_FALLBACK = "5987c46c-0000-0000-0000-000000000000"


def _get_user_token():
    """
    Authenticate using bi4nav@shalina.com (ROPC flow).
    Used for datasets that only allow user account access, not service principals.
    """
    tenant   = _get_secret("FABRIC_TENANT_ID")
    client   = _get_secret("FABRIC_CLIENT_ID")
    username = _get_secret("FABRIC_USERNAME")
    password = _get_secret("FABRIC_PASSWORD")
    if not all([tenant, client, username, password]):
        raise Exception("Missing user credentials for SFA auth")
    url = f"https://login.microsoftonline.com/{tenant}/oauth2/v2.0/token"
    r = requests.post(url, data={
        "grant_type": "password",
        "client_id":  client,
        "username":   username,
        "password":   password,
        "scope":      "https://analysis.windows.net/powerbi/api/.default"
    }, timeout=15)
    if r.status_code != 200:
        raise Exception(f"User auth failed {r.status_code}: {r.text[:200]}")
    return r.json()["access_token"]


def _run_dax_sfa(dax_query):
    """
    Run a DAX query against the SFA Reports dataset.
    Uses username/password auth (bi4nav@shalina.com) since this workspace
    only allows email accounts, not service principals.
    """
    workspace   = "f2a6b294-ef89-4e41-b6b1-b49adb002715"
    sfa_dataset = _get_secret("FABRIC_SFA_DATASET_ID") or "66e7f737-eda2-47e9-95dc-ec12166cb34f"
    token = _get_user_token()
    url = f"https://api.powerbi.com/v1.0/myorg/groups/{workspace}/datasets/{sfa_dataset}/executeQueries"
    r = requests.post(url,
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
        json={"queries": [{"query": dax_query}], "serializerSettings": {"includeNulls": True}},
        timeout=60)
    if r.status_code != 200:
        raise Exception(f"SFA DAX failed {r.status_code}: {r.text[:150]}")
    rows = r.json()["results"][0]["tables"][0].get("rows", [])
    return pd.DataFrame(rows)


def _fetch_sfa_tables():
    """
    Lists all tables in the SFA dataset — run this once to find the right
    table and column names. Prints to terminal / Streamlit logs.
    """
    dax = "EVALUATE SELECTCOLUMNS(INFO.TABLES(), \"TableName\", [Name])"
    df = _run_dax_sfa(dax)
    return df


def _fetch_sfa_transactions(country="Nigeria"):
    """
    Pull real transaction data from SFA Reports.
    Returns one row per outlet with:
      - Shop Name
      - last_order_date  (most recent order date)
      - order_count      (total number of orders)
      - total_spend      (sum of all order values)

    ⚠️  TABLE AND COLUMN NAMES BELOW ARE PLACEHOLDERS.
        Once you paste the actual table/column names from Power BI,
        update the DAX queries here.
    """
    if country == "Nigeria":
        dax = """
        EVALUATE
        SUMMARIZECOLUMNS(
            'SFA Orders'[Outlet Name],
            "Last Order Date", MAX('SFA Orders'[Order Date]),
            "Order Count",     COUNTROWS('SFA Orders'),
            "Total Spend",     SUM('SFA Orders'[Order Value])
        )
        """
    else:
        dax = """
        EVALUATE
        SUMMARIZECOLUMNS(
            'SFA Orders Angola'[Outlet Name],
            "Last Order Date", MAX('SFA Orders Angola'[Order Date]),
            "Order Count",     COUNTROWS('SFA Orders Angola'),
            "Total Spend",     SUM('SFA Orders Angola'[Order Value])
        )
        """
    df = _run_dax_sfa(dax)
    df.columns = ['Shop Name', 'last_order_date', 'order_count', 'total_spend']
    df['last_order_date'] = pd.to_datetime(df['last_order_date'], errors='coerce')
    df['order_count']     = pd.to_numeric(df['order_count'],     errors='coerce').fillna(0)
    df['total_spend']     = pd.to_numeric(df['total_spend'],     errors='coerce').fillna(0)
    df['country'] = country
    return df


def load_rfm_data(country="Nigeria"):
    """
    Attempt to load real RFM transaction data from SFA Reports.

    Returns a DataFrame with columns:
        Shop Name, last_order_date, order_count, total_spend, country
    or None if SFA data is unavailable (no access yet).

    The app uses this to compute true R/F/M scores.
    Falls back to YTD-proxy RFM if this returns None.
    """
    import streamlit as st

    @st.cache_data(ttl=1800, show_spinner=False)
    def _cached(country):
        try:
            username = _get_secret("FABRIC_USERNAME")
            password = _get_secret("FABRIC_PASSWORD")
            if not all([username, password]):
                return None, "missing_user_credentials"
            df = _fetch_sfa_transactions(country)
            if df is None or len(df) == 0:
                return None, "empty_result"
            return df, "live"
        except Exception as e:
            return None, str(e)[:120]

    result, status = _cached(country)
    return result, status