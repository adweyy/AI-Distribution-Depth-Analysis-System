"""
Shalina Healthcare — Data Connector
- Angola: Live from Microsoft Fabric (has YTD Sales)
- Nigeria: Live from Microsoft Fabric (GPS + outlet data)
- Fallback: shalina_combined_data.csv if Fabric unavailable
"""

import requests
import pandas as pd
import numpy as np
import os
from dotenv import load_dotenv

# Load .env for local development
_env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
load_dotenv(_env_path)


def _get_secret(key):
    """Read from Streamlit secrets (cloud) or .env (local)."""
    # Try Streamlit secrets first
    try:
        import streamlit as st
        if hasattr(st, 'secrets') and key in st.secrets:
            return st.secrets[key]
    except Exception:
        pass
    # Fall back to environment variable
    return os.getenv(key)


def _get_access_token():
    tenant   = _get_secret("FABRIC_TENANT_ID")
    client   = _get_secret("FABRIC_CLIENT_ID")
    secret   = _get_secret("FABRIC_CLIENT_SECRET")

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


def _run_dax(token, dax_query):
    workspace = _get_secret("FABRIC_WORKSPACE_ID")
    dataset   = _get_secret("FABRIC_DATASET_ID")
    url = f"https://api.powerbi.com/v1.0/myorg/groups/{workspace}/datasets/{dataset}/executeQueries"
    r = requests.post(url,
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
        json={"queries": [{"query": dax_query}], "serializerSettings": {"includeNulls": True}},
        timeout=60)
    if r.status_code != 200:
        raise Exception(f"DAX failed {r.status_code}: {r.text[:200]}")
    rows = r.json()["results"][0]["tables"][0].get("rows", [])
    return pd.DataFrame(rows)


def _fetch_nigeria(token):
    dax = """
    EVALUATE
    SELECTCOLUMNS(
        FILTER('Nigeria - Chemist', 'Nigeria - Chemist'[latitude] <> BLANK()),
        "Shop Name",           'Nigeria - Chemist'[name],
        "latitude",            'Nigeria - Chemist'[latitude],
        "longitude",           'Nigeria - Chemist'[longitude],
        "Retailer Subtype",    'Nigeria - Chemist'[retailer_subtype],
        "YTD Retailing Value", 0
    )
    """
    df = _run_dax(token, dax)
    df.columns = ['Shop Name', 'latitude', 'longitude', 'Retailer Subtype', 'YTD Retailing Value']
    df['country'] = 'Nigeria'
    return df


def _fetch_angola(token):
    dax = """
    EVALUATE
    SELECTCOLUMNS(
        FILTER('Angola - Chemist', 'Angola - Chemist'[Lat] <> BLANK()),
        "Shop Name",           'Angola - Chemist'[Retailer/Chemist Name],
        "latitude",            'Angola - Chemist'[Lat],
        "longitude",           'Angola - Chemist'[Long],
        "Retailer Subtype",    'Angola - Chemist'[Type new],
        "YTD Retailing Value", 'Angola - Chemist'[YTD Sales Value]
    )
    """
    df = _run_dax(token, dax)
    df.columns = ['Shop Name', 'latitude', 'longitude', 'Retailer Subtype', 'YTD Retailing Value']
    df['country'] = 'Angola'
    return df


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
            if v == 0:        return 'Dead Whitespace'
            elif v < p25:     return 'Underperforming'
            elif v < mean:    return 'Low Performer'
            elif v < p75:     return 'Active'
            else:             return 'High Performer'
        sub['Opportunity'] = sub['YTD Retailing Value'].apply(clf)
        results.append(sub)
    return pd.concat(results, ignore_index=True)


def _load_from_fabric():
    try:
        ws  = _get_secret("FABRIC_WORKSPACE_ID")
        ds  = _get_secret("FABRIC_DATASET_ID")
        tid = _get_secret("FABRIC_TENANT_ID")
        cid = _get_secret("FABRIC_CLIENT_ID")
        sec = _get_secret("FABRIC_CLIENT_SECRET")
        debug = f"TID={bool(tid)} CID={bool(cid)} SEC={bool(sec)} WS={bool(ws)} DS={bool(ds)}"
        if not all([tid, cid, sec, ws, ds]):
            return None, f"missing_creds:{debug}"
        token = _get_access_token()
        ng    = _fetch_nigeria(token)
        ao    = _fetch_angola(token)
        df    = pd.concat([ng, ao], ignore_index=True)
        df    = _clean(df)
        df    = _classify(df)
        return df, "live"
    except Exception as e:
        return None, f"error:{str(e)[:150]}"


def _load_from_csv():
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "shalina_combined_data.csv")
    if not os.path.exists(path):
        return None
    df = pd.read_csv(path)
    df['YTD Retailing Value'] = pd.to_numeric(df['YTD Retailing Value'], errors='coerce').fillna(0)
    if 'Opportunity' not in df.columns:
        df = _classify(df)
    return df


def load_data():
    """
    1. Try live Microsoft Fabric
    2. Fall back to local CSV
    Returns: (DataFrame, source_label, status)
    """
    import streamlit as st

    @st.cache_data(ttl=3600)
    def _cached():
        df, status = _load_from_fabric()
        if df is not None:
            return df, "🟢  Live — Microsoft Fabric Warehouse", "live"
        df = _load_from_csv()
        if df is not None:
            return df, f"🟡  Local CSV  ({status})", "csv"
        return None, f"🔴  No data source available ({status})", "error"

    return _cached()