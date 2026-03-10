"""
Shalina Healthcare — Microsoft Fabric Live Connector
Uses Azure AD Service Principal + Power BI REST API to query
the Fabric semantic model directly. No CSV needed.
"""

import requests
import pandas as pd
import numpy as np
import streamlit as st
import os
from dotenv import load_dotenv

# Load .env from the same folder as this file
_env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
load_dotenv(_env_path)

# ── CONFIG — reads lazily so Streamlit secrets are available ─────
def _get_secret(key):
    """Try Streamlit secrets first, fall back to env var."""
    try:
        import streamlit as st
        val = st.secrets.get(key)
        if val:
            return val
    except Exception:
        pass
    return os.getenv(key)

def _get_config():
    """Returns config dict — called lazily inside functions."""
    return {
        "TENANT_ID":     _get_secret("FABRIC_TENANT_ID"),
        "CLIENT_ID":     _get_secret("FABRIC_CLIENT_ID"),
        "CLIENT_SECRET": _get_secret("FABRIC_CLIENT_SECRET"),
        "WORKSPACE_ID":  _get_secret("FABRIC_WORKSPACE_ID"),
        "DATASET_ID":    _get_secret("FABRIC_DATASET_ID"),
        "USERNAME":      _get_secret("FABRIC_USERNAME"),
        "PASSWORD":      _get_secret("FABRIC_PASSWORD"),
    }

def _get_access_token():
    cfg = _get_config()
    url = f"https://login.microsoftonline.com/{cfg['TENANT_ID']}/oauth2/v2.0/token"

    # Option 1: Service Principal
    if cfg['CLIENT_SECRET']:
        payload = {
            "grant_type":    "client_credentials",
            "client_id":     cfg['CLIENT_ID'],
            "client_secret": cfg['CLIENT_SECRET'],
            "scope":         "https://analysis.windows.net/powerbi/api/.default"
        }
        r = requests.post(url, data=payload, timeout=15)
        if r.status_code == 200:
            return r.json()["access_token"], cfg

    # Option 2: Username / Password
    if cfg['USERNAME'] and cfg['PASSWORD']:
        payload = {
            "grant_type": "password",
            "client_id":  cfg['CLIENT_ID'],
            "username":   cfg['USERNAME'],
            "password":   cfg['PASSWORD'],
            "scope":      "https://analysis.windows.net/powerbi/api/.default"
        }
        r = requests.post(url, data=payload, timeout=15)
        r.raise_for_status()
        return r.json()["access_token"], cfg

    raise Exception("No valid auth credentials configured")


# ── DAX QUERY RUNNER ─────────────────────────────────────────────
def _run_dax(token, dax_query, cfg):
    url = f"https://api.powerbi.com/v1.0/myorg/groups/{cfg['WORKSPACE_ID']}/datasets/{cfg['DATASET_ID']}/executeQueries"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type":  "application/json"
    }
    body = {
        "queries": [{"query": dax_query}],
        "serializerSettings": {"includeNulls": True}
    }
    r = requests.post(url, headers=headers, json=body, timeout=60)
    r.raise_for_status()
    rows = r.json()["results"][0]["tables"][0].get("rows", [])
    return pd.DataFrame(rows)


# ── FETCH NIGERIA DATA ────────────────────────────────────────────
def _fetch_nigeria(token, cfg):
    dax = """
    EVALUATE
    SELECTCOLUMNS(
        FILTER('Nigeria - Chemist', 'Nigeria - Chemist'[latitude] <> BLANK()),
        "Shop Name",        'Nigeria - Chemist'[name],
        "latitude",         'Nigeria - Chemist'[latitude],
        "longitude",        'Nigeria - Chemist'[longitude],
        "Retailer Subtype", 'Nigeria - Chemist'[retailer_subtype],
        "State",            'Nigeria - Chemist'[state],
        "YTD Retailing Value", 0
    )
    """
    df = _run_dax(token, dax, cfg)
    df.columns = ['Shop Name','latitude','longitude','Retailer Subtype','State','YTD Retailing Value']
    df['country'] = 'Nigeria'
    return df


# ── FETCH ANGOLA DATA ─────────────────────────────────────────────
def _fetch_angola(token, cfg):
    dax = """
    EVALUATE
    SELECTCOLUMNS(
        FILTER('Angola - Chemist', 'Angola - Chemist'[Lat] <> BLANK()),
        "Shop Name",        'Angola - Chemist'[Retailer/Chemist Name],
        "latitude",         'Angola - Chemist'[Lat],
        "longitude",        'Angola - Chemist'[Long],
        "Retailer Subtype", 'Angola - Chemist'[Type new],
        "YTD Retailing Value", 'Angola - Chemist'[YTD Sales Value]
    )
    """
    df = _run_dax(token, dax, cfg)
    df.columns = ['Shop Name','latitude','longitude','Retailer Subtype','YTD Retailing Value']
    df['country'] = 'Angola'
    return df


# ── CLEAN & CLASSIFY ──────────────────────────────────────────────
def _clean(df):
    df['latitude']            = pd.to_numeric(df['latitude'],            errors='coerce')
    df['longitude']           = pd.to_numeric(df['longitude'],           errors='coerce')
    df['YTD Retailing Value'] = pd.to_numeric(df['YTD Retailing Value'], errors='coerce').fillna(0)
    df['Retailer Subtype']    = df['Retailer Subtype'].astype(str)\
        .str.replace(' Customers','', regex=False).str.strip()
    df = df.dropna(subset=['latitude','longitude'])
    return df


def _classify(df):
    results = []
    for country in df['country'].unique():
        sub    = df[df['country'] == country].copy()
        nonzero = sub[sub['YTD Retailing Value'] > 0]['YTD Retailing Value']
        if len(nonzero) == 0:
            sub['Opportunity'] = 'Dead Whitespace'
            results.append(sub); continue
        p25  = nonzero.quantile(0.25)
        mean = nonzero.mean()
        p75  = nonzero.quantile(0.75)
        def clf(v, p25=p25, mean=mean, p75=p75):
            if v == 0:       return 'Dead Whitespace'
            elif v < p25:    return 'Underperforming'
            elif v < mean:   return 'Low Performer'
            elif v < p75:    return 'Active'
            else:            return 'High Performer'
        sub['Opportunity'] = sub['YTD Retailing Value'].apply(clf)
        results.append(sub)
    return pd.concat(results, ignore_index=True)


# ── LIVE FABRIC LOAD ──────────────────────────────────────────────
def _load_from_fabric():
    try:
        cfg = _get_config()
        if not all([cfg['TENANT_ID'], cfg['CLIENT_ID'], cfg['WORKSPACE_ID'], cfg['DATASET_ID']]):
            return None, "missing_env"
        token, cfg = _get_access_token()
        ng      = _fetch_nigeria(token, cfg)
        ao      = _fetch_angola(token, cfg)
        df      = pd.concat([ng, ao], ignore_index=True)
        df      = _clean(df)
        df      = _classify(df)
        return df, "live"
    except requests.exceptions.HTTPError as e:
        import traceback; traceback.print_exc()
        return None, f"http_error:{e.response.status_code}"
    except Exception as e:
        import traceback; traceback.print_exc()
        return None, f"error:{str(e)[:80]}"


# ── CSV FALLBACK ──────────────────────────────────────────────────
def _load_from_csv():
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "shalina_combined_data.csv")
    if not os.path.exists(path):
        return None
    df = pd.read_csv(path)
    df['YTD Retailing Value'] = pd.to_numeric(df['YTD Retailing Value'], errors='coerce').fillna(0)
    return df


# ── MAIN ENTRY POINT (cached 1 hour) ─────────────────────────────
@st.cache_data(ttl=3600)
def load_data():
    """
    1. Try live Fabric (REST API + service principal)
    2. Fall back to local CSV
    Returns: (DataFrame, source_label, status)
    """
    df, status = _load_from_fabric()
    if df is not None:
        return df, "🟢  Live — Microsoft Fabric Warehouse", "live"

    df = _load_from_csv()
    if df is not None:
        reason = "Fabric credentials not configured" if status == "missing_env" \
                 else f"Fabric connection failed ({status})"
        return df, f"🟡  Local CSV  ({reason})", "csv"

    return None, "🔴  No data source available", "error"