"""
Shalina Healthcare — Data Connector (Upgraded)
===============================================

Connection priority (per country):
  1. Fabric SQL Analytics Endpoint  (pyodbc + Azure AD token) ← NEW, fastest
  2. Power BI REST API / DAX         (original method)        ← fallback
  3. Local CSV                       (always available)       ← last resort

Status returned:
  'live'   — SQL endpoint working for both countries
  'hybrid' — one or more countries on fallback/CSV
  'csv'    — no live connection at all

Write-back:
  write_churn_predictions(df)  — saves churn scores back to Fabric as a table
  write_whitespace_scores(df)  — saves whitespace opportunity scores to Fabric

HOW TO FIND YOUR SQL ENDPOINT:
  1. Open your Fabric workspace at app.fabric.microsoft.com
  2. Click on your Warehouse (or Lakehouse with SQL endpoint)
  3. Click the ⚙ Settings icon (top-right of the item)
  4. Copy the value next to "SQL connection string"
     It looks like:  xyz123abc.datawarehouse.fabric.microsoft.com
  5. Set FABRIC_SQL_ENDPOINT=that value in your .env file
  6. Set FABRIC_SQL_DATABASE to the name of your warehouse/database
"""

import os
import struct
import warnings
import requests
import pandas as pd
import numpy as np
from dotenv import load_dotenv

warnings.filterwarnings("ignore")

_env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
load_dotenv(_env_path)


# ── SECRET READER ─────────────────────────────────────────────────────────────
def _get_secret(key):
    """Read from Streamlit secrets (cloud) or .env (local)."""
    val = None
    try:
        import streamlit as st
        if hasattr(st, "secrets") and key in st.secrets:
            val = st.secrets[key]
    except Exception:
        pass
    if not val:
        val = os.getenv(key)
    if val:
        val = str(val).strip().strip('"').strip("'").strip()
    return val or None


# ══════════════════════════════════════════════════════════════════════════════
# METHOD 1 — SQL ANALYTICS ENDPOINT  (primary, fastest)
# ══════════════════════════════════════════════════════════════════════════════

def _get_sql_token():
    """
    Get an Azure AD access token scoped for Azure SQL / Fabric SQL endpoint.
    Uses the service principal credentials from .env / Streamlit secrets.
    """
    tenant = _get_secret("FABRIC_TENANT_ID")
    client = _get_secret("FABRIC_CLIENT_ID")
    secret = _get_secret("FABRIC_CLIENT_SECRET")
    if not all([tenant, client, secret]):
        raise Exception("Missing service principal credentials")
    url = f"https://login.microsoftonline.com/{tenant}/oauth2/v2.0/token"
    r = requests.post(url, data={
        "grant_type":    "client_credentials",
        "client_id":     client,
        "client_secret": secret,
        "scope":         "https://database.windows.net/.default",   # SQL scope
    }, timeout=15)
    if r.status_code != 200:
        raise Exception(f"SQL token auth failed {r.status_code}: {r.text[:200]}")
    return r.json()["access_token"]


def _get_sql_connection():
    """
    Open a pyodbc connection to the Fabric SQL Analytics Endpoint.
    Uses token-based auth (the recommended approach for service principals).

    Requires:
        FABRIC_SQL_ENDPOINT  — e.g. xyz.datawarehouse.fabric.microsoft.com
        FABRIC_SQL_DATABASE  — e.g. Shalina_Warehouse
    """
    try:
        import pyodbc
    except ImportError:
        raise Exception(
            "pyodbc is not installed. Run: pip install pyodbc --break-system-packages"
        )

    sql_endpoint = _get_secret("FABRIC_SQL_ENDPOINT")
    database     = _get_secret("FABRIC_SQL_DATABASE") or "Shalina_Warehouse"

    if not sql_endpoint:
        raise Exception(
            "FABRIC_SQL_ENDPOINT not set. See the HOW TO FIND YOUR SQL ENDPOINT "
            "section at the top of fabric_connector.py"
        )

    token       = _get_sql_token()
    token_bytes = token.encode("utf-16-le")
    # Pack the token into the structure pyodbc expects for SQL_COPT_SS_ACCESS_TOKEN
    token_struct = struct.pack(f"<I{len(token_bytes)}s", len(token_bytes), token_bytes)

    conn_str = (
        "Driver={ODBC Driver 18 for SQL Server};"
        f"Server={sql_endpoint},1433;"
        f"Database={database};"
        "Encrypt=yes;"
        "TrustServerCertificate=no;"
        "Connection Timeout=30;"
    )
    # 1256 = SQL_COPT_SS_ACCESS_TOKEN
    conn = pyodbc.connect(conn_str, attrs_before={1256: token_struct})
    return conn


def _fetch_nigeria_sql(conn):
    """Pull Nigeria outlet data via SQL."""
    query = """
        SELECT
            [name]                  AS [Shop Name],
            [latitude],
            [longitude],
            [Retailer Subtype],
            [YTD Retailing Value]
        FROM [dbo].[Final Nigeria]
        WHERE [latitude]  IS NOT NULL
          AND [longitude] IS NOT NULL
          AND [latitude]  <> 0
          AND [longitude] <> 0
    """
    df = pd.read_sql(query, conn)
    df["country"] = "Nigeria"
    return df


def _fetch_angola_sql(conn):
    """Pull Angola outlet data via SQL."""
    query = """
        SELECT
            [Retailer/Chemist Name]  AS [Shop Name],
            [Lat]                    AS [latitude],
            [Long]                   AS [longitude],
            [Type]                   AS [Retailer Subtype],
            [YTD Sales Value]        AS [YTD Retailing Value]
        FROM [dbo].[Angola - Chemist]
        WHERE [Lat]  IS NOT NULL
          AND [Long] IS NOT NULL
    """
    df = pd.read_sql(query, conn)
    df["country"] = "Angola"
    return df


# ══════════════════════════════════════════════════════════════════════════════
# METHOD 2 — POWER BI REST API / DAX  (original fallback)
# ══════════════════════════════════════════════════════════════════════════════

def _get_pbi_token():
    tenant = _get_secret("FABRIC_TENANT_ID")
    client = _get_secret("FABRIC_CLIENT_ID")
    secret = _get_secret("FABRIC_CLIENT_SECRET")
    if not all([tenant, client, secret]):
        raise Exception("Missing credentials")
    url = f"https://login.microsoftonline.com/{tenant}/oauth2/v2.0/token"
    r = requests.post(url, data={
        "grant_type":    "client_credentials",
        "client_id":     client,
        "client_secret": secret,
        "scope":         "https://analysis.windows.net/powerbi/api/.default",
    }, timeout=15)
    if r.status_code != 200:
        raise Exception(f"PBI auth failed {r.status_code}: {r.text[:200]}")
    return r.json()["access_token"]


def _run_dax(token, dax_query, workspace=None, dataset=None):
    workspace = workspace or _get_secret("FABRIC_WORKSPACE_ID") or "ccf72308-6884-43ee-a116-3d86fbe1553f"
    dataset   = dataset   or _get_secret("FABRIC_DATASET_ID")   or "4aea9823-3813-4fc8-a146-a7c5f986bf0a"
    url = (f"https://api.powerbi.com/v1.0/myorg/groups/{workspace}"
           f"/datasets/{dataset}/executeQueries")
    r = requests.post(
        url,
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
        json={"queries": [{"query": dax_query}], "serializerSettings": {"includeNulls": True}},
        timeout=60,
    )
    if r.status_code != 200:
        raise Exception(f"DAX failed {r.status_code}: {r.text[:150]}")
    rows = r.json()["results"][0]["tables"][0].get("rows", [])
    return pd.DataFrame(rows)



# UAT workspace/dataset — both Angola-Chemist and Final Nigeria live here.
# These IDs are hardcoded so that wrong values in Streamlit secrets can't
# accidentally point these fetches at the SFA workspace or any other dataset.
_UAT_WORKSPACE = "ccf72308-6884-43ee-a116-3d86fbe1553f"
_UAT_DATASET   = "4aea9823-3813-4fc8-a146-a7c5f986bf0a"


def _fetch_nigeria_dax(token):
    """Pull Nigeria outlet data via Power BI DAX (UAT dataset)."""
    dax = """
EVALUATE
SELECTCOLUMNS(
    FILTER('Final Nigeria',
        'Final Nigeria'[latitude]  <> BLANK() &&
        'Final Nigeria'[longitude] <> BLANK()
    ),
    "Shop Name",           'Final Nigeria'[name],
    "latitude",            'Final Nigeria'[latitude],
    "longitude",           'Final Nigeria'[longitude],
    "Retailer Subtype",    'Final Nigeria'[Retailer Subtype],
    "YTD Retailing Value", 'Final Nigeria'[YTD Retailing Value]
)
"""
    df = _run_dax(token, dax, workspace=_UAT_WORKSPACE, dataset=_UAT_DATASET)
    if df.empty:
        raise Exception("Nigeria DAX returned 0 rows")
    df.columns = ["Shop Name", "latitude", "longitude", "Retailer Subtype", "YTD Retailing Value"]
    df["country"] = "Nigeria"
    return df


def _fetch_angola_dax(token):
    """Pull Angola outlet data via Power BI DAX (UAT dataset)."""
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
    df = _run_dax(token, dax, workspace=_UAT_WORKSPACE, dataset=_UAT_DATASET)
    if df.empty:
        raise Exception("Angola DAX returned 0 rows")
    df.columns = ["Shop Name", "latitude", "longitude", "Retailer Subtype", "YTD Retailing Value"]
    df["country"] = "Angola"
    return df


# ══════════════════════════════════════════════════════════════════════════════
# METHOD 3 — CSV FALLBACK
# ══════════════════════════════════════════════════════════════════════════════

def _csv_path():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "shalina_combined_data.csv")


def _load_from_csv(country=None):
    path = _csv_path()
    if not os.path.exists(path):
        return None
    df = pd.read_csv(path)
    if country:
        df = df[df["country"] == country].copy()
    df["YTD Retailing Value"] = pd.to_numeric(df["YTD Retailing Value"], errors="coerce").fillna(0)
    df["latitude"]  = pd.to_numeric(df["latitude"],  errors="coerce")
    df["longitude"] = pd.to_numeric(df["longitude"], errors="coerce")
    df = df.dropna(subset=["latitude", "longitude"])
    return df


# ══════════════════════════════════════════════════════════════════════════════
# CLEAN & CLASSIFY
# ══════════════════════════════════════════════════════════════════════════════

def _clean(df):
    df = df.copy()
    df["latitude"]            = pd.to_numeric(df["latitude"],            errors="coerce")
    df["longitude"]           = pd.to_numeric(df["longitude"],           errors="coerce")
    df["YTD Retailing Value"] = pd.to_numeric(df["YTD Retailing Value"], errors="coerce").fillna(0)
    df["Retailer Subtype"]    = (
        df["Retailer Subtype"].astype(str)
        .str.replace(" Customers", "", regex=False).str.strip()
    )
    df = df.dropna(subset=["latitude", "longitude"])
    return df


def _classify(df):
    """
    Assign opportunity category per outlet, per country.
    Dead Whitespace  → YTD = 0
    Underperforming  → YTD < 25th percentile of active outlets
    Low Performer    → YTD < mean of active outlets
    Active           → YTD < 75th percentile
    High Performer   → YTD ≥ 75th percentile
    Pre-Churn        → Active outlet with negative 3-month sales trend (if available)
    """
    results = []
    for country in df["country"].unique():
        sub     = df[df["country"] == country].copy()
        nonzero = sub[sub["YTD Retailing Value"] > 0]["YTD Retailing Value"]
        if len(nonzero) == 0:
            sub["Opportunity"] = "Dead Whitespace"
            results.append(sub)
            continue
        p25  = nonzero.quantile(0.25)
        mean = nonzero.mean()
        p75  = nonzero.quantile(0.75)

        def clf(v, p25=p25, mean=mean, p75=p75):
            if v == 0:       return "Dead Whitespace"
            elif v < p25:    return "Underperforming"
            elif v < mean:   return "Low Performer"
            elif v < p75:    return "Active"
            else:            return "High Performer"

        sub["Opportunity"] = sub["YTD Retailing Value"].apply(clf)
        results.append(sub)
    return pd.concat(results, ignore_index=True)


# ══════════════════════════════════════════════════════════════════════════════
# MAIN LOAD — tries SQL → DAX → CSV in order
# ══════════════════════════════════════════════════════════════════════════════

def load_data():
    """
    Load outlet data using the best available method.

    Returns: (DataFrame, source_label, status)
      status = 'live'   : SQL endpoint working
      status = 'hybrid' : one method working, other on CSV
      status = 'csv'    : all from local CSV
      status = 'error'  : no data at all
    """
    import streamlit as st

    @st.cache_data(ttl=3600, show_spinner=False)
    def _cached():
        csv_exists = os.path.exists(_csv_path())
        ng_method  = "csv"
        ao_method  = "csv"
        ng = ao = None

        # ── Try SQL endpoint first ────────────────────────────────────────────
        sql_endpoint = _get_secret("FABRIC_SQL_ENDPOINT")
        if sql_endpoint:
            try:
                conn = _get_sql_connection()
                try:
                    ng = _fetch_nigeria_sql(conn)
                    ng_method = "sql"
                except Exception:
                    ng = None
                try:
                    ao = _fetch_angola_sql(conn)
                    ao_method = "sql"
                except Exception:
                    ao = None
                conn.close()
            except Exception:
                pass  # SQL endpoint unavailable → try DAX next

        # ── Try Power BI / DAX for any country that SQL missed ────────────────
        if ng is None or ao is None:
            # Try user-credentials token first (bypasses RLS on Final Nigeria).
            # Fall back to service-principal token if user creds aren't set.
            pbi_token = None
            try:
                pbi_token = _get_user_token()
                print("[FABRIC] Using user token for UAT DAX queries")
            except Exception as _user_tok_err:
                print(f"[FABRIC] User token failed ({_user_tok_err}), trying SP token")
                try:
                    pbi_token = _get_pbi_token()
                except Exception:
                    pass

            if pbi_token:
                if ng is None:
                    try:
                        ng = _fetch_nigeria_dax(pbi_token)
                        ng_method = "dax"
                    except Exception as _ng_err:
                        print(f"[FABRIC] Nigeria DAX error: {_ng_err}")
                        ng = None
                if ao is None:
                    try:
                        ao = _fetch_angola_dax(pbi_token)
                        ao_method = "dax"
                    except Exception as _ao_err:
                        print(f"[FABRIC] Angola DAX error: {_ao_err}")
                        ao = None

        # ── CSV fallback for anything still missing ───────────────────────────
        if ng is None:
            if not csv_exists:
                return None, "No data — shalina_combined_data.csv not found", "error"
            ng = _load_from_csv("Nigeria")
            ng_method = "csv"

        if ao is None:
            ao = _load_from_csv("Angola") if csv_exists else ng.iloc[0:0].copy()
            ao_method = "csv"

        # ── Combine, clean, classify ──────────────────────────────────────────
        df = pd.concat([ng, ao], ignore_index=True)
        df = _clean(df)
        df = _classify(df)

        # ── Build status ──────────────────────────────────────────────────────
        live_methods = {"sql", "dax"}
        ng_live = ng_method in live_methods
        ao_live = ao_method in live_methods

        def _method_label(m):
            return {"sql": "Fabric SQL", "dax": "Fabric DAX", "csv": "CSV"}[m]

        if ng_live and ao_live:
            if ng_method == ao_method == "sql":
                label  = "Connected to Microsoft Fabric SQL Analytics Endpoint"
                status = "live"
            else:
                label  = (f"Nigeria: {_method_label(ng_method)}  |  "
                          f"Angola: {_method_label(ao_method)}")
                status = "hybrid"
        elif ng_live or ao_live:
            live_c  = "Nigeria" if ng_live else "Angola"
            csv_c   = "Angola"  if ng_live else "Nigeria"
            live_m  = _method_label(ng_method if ng_live else ao_method)
            label   = f"{live_c}: {live_m}  |  {csv_c}: CSV fallback"
            status  = "hybrid"
        else:
            label  = "Nigeria + Angola: CSV (Fabric unreachable)"
            status = "csv"

        return df, label, status

    return _cached()


# ══════════════════════════════════════════════════════════════════════════════
# WRITE-BACK — save predictions back into Fabric
# ══════════════════════════════════════════════════════════════════════════════

def _ensure_churn_table(conn):
    """Create ChurnPredictions table in Fabric if it doesn't exist."""
    cursor = conn.cursor()
    cursor.execute("""
        IF NOT EXISTS (
            SELECT 1 FROM INFORMATION_SCHEMA.TABLES
            WHERE TABLE_SCHEMA = 'dbo' AND TABLE_NAME = 'ChurnPredictions'
        )
        CREATE TABLE [dbo].[ChurnPredictions] (
            [Shop Name]       NVARCHAR(500),
            [country]         NVARCHAR(50),
            [churn_prob]      FLOAT,
            [risk_tier]       NVARCHAR(20),
            [ytd_value]       FLOAT,
            [Opportunity]     NVARCHAR(50),
            [latitude]        FLOAT,
            [longitude]       FLOAT,
            [scored_at]       DATETIME2 DEFAULT GETDATE()
        )
    """)
    conn.commit()


def _ensure_whitespace_table(conn):
    """Create WhitespaceScores table in Fabric if it doesn't exist."""
    cursor = conn.cursor()
    cursor.execute("""
        IF NOT EXISTS (
            SELECT 1 FROM INFORMATION_SCHEMA.TABLES
            WHERE TABLE_SCHEMA = 'dbo' AND TABLE_NAME = 'WhitespaceScores'
        )
        CREATE TABLE [dbo].[WhitespaceScores] (
            [Shop Name]          NVARCHAR(500),
            [country]            NVARCHAR(50),
            [Opportunity]        NVARCHAR(50),
            [YTD Retailing Value] FLOAT,
            [latitude]           FLOAT,
            [longitude]          FLOAT,
            [Retailer Subtype]   NVARCHAR(100),
            [scored_at]          DATETIME2 DEFAULT GETDATE()
        )
    """)
    conn.commit()


def write_churn_predictions(scored_df: pd.DataFrame) -> dict:
    """
    Write churn prediction scores back to the Fabric warehouse.

    Parameters
    ----------
    scored_df : DataFrame returned by src.churn_model.train()
                Must have columns: Shop Name, country, churn_prob,
                risk_tier, ytd_value, Opportunity, latitude, longitude

    Returns
    -------
    dict with keys: success (bool), rows_written (int), error (str or None)
    """
    required_cols = ["Shop Name", "country", "churn_prob", "risk_tier",
                     "ytd_value", "latitude", "longitude"]
    missing = [c for c in required_cols if c not in scored_df.columns]
    if missing:
        return {"success": False, "rows_written": 0,
                "error": f"Missing columns: {missing}"}

    try:
        conn   = _get_sql_connection()
        cursor = conn.cursor()
        _ensure_churn_table(conn)

        # Truncate then re-insert (full refresh)
        cursor.execute("TRUNCATE TABLE [dbo].[ChurnPredictions]")
        conn.commit()

        cols = ["Shop Name", "country", "churn_prob", "risk_tier",
                "ytd_value", "Opportunity", "latitude", "longitude"]
        existing = [c for c in cols if c in scored_df.columns]
        rows     = scored_df[existing].values.tolist()

        placeholders = ", ".join(["?"] * len(existing))
        col_names    = ", ".join([f"[{c}]" for c in existing])
        sql = f"INSERT INTO [dbo].[ChurnPredictions] ({col_names}) VALUES ({placeholders})"

        cursor.fast_executemany = True
        cursor.executemany(sql, rows)
        conn.commit()
        conn.close()

        return {"success": True, "rows_written": len(rows), "error": None}

    except Exception as e:
        return {"success": False, "rows_written": 0, "error": str(e)[:300]}


def write_whitespace_scores(df: pd.DataFrame) -> dict:
    """
    Write outlet whitespace opportunity scores back to the Fabric warehouse.

    Parameters
    ----------
    df : The main outlet DataFrame (output of load_data())

    Returns
    -------
    dict with keys: success (bool), rows_written (int), error (str or None)
    """
    required_cols = ["Shop Name", "country", "Opportunity", "YTD Retailing Value"]
    missing = [c for c in required_cols if c not in df.columns]
    if missing:
        return {"success": False, "rows_written": 0,
                "error": f"Missing columns: {missing}"}

    try:
        conn   = _get_sql_connection()
        cursor = conn.cursor()
        _ensure_whitespace_table(conn)

        cursor.execute("TRUNCATE TABLE [dbo].[WhitespaceScores]")
        conn.commit()

        cols     = ["Shop Name", "country", "Opportunity",
                    "YTD Retailing Value", "latitude", "longitude", "Retailer Subtype"]
        existing = [c for c in cols if c in df.columns]
        rows     = df[existing].values.tolist()

        placeholders = ", ".join(["?"] * len(existing))
        col_names    = ", ".join([f"[{c}]" for c in existing])
        sql = f"INSERT INTO [dbo].[WhitespaceScores] ({col_names}) VALUES ({placeholders})"

        cursor.fast_executemany = True
        cursor.executemany(sql, rows)
        conn.commit()
        conn.close()

        return {"success": True, "rows_written": len(rows), "error": None}

    except Exception as e:
        return {"success": False, "rows_written": 0, "error": str(e)[:300]}


# ══════════════════════════════════════════════════════════════════════════════
# SFA / RFM TRANSACTION DATA  (unchanged from original)
# ══════════════════════════════════════════════════════════════════════════════

_SFA_DATASET_ID_FALLBACK = "5987c46c-0000-0000-0000-000000000000"


def _get_user_token():
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
        "scope":      "https://analysis.windows.net/powerbi/api/.default",
    }, timeout=15)
    if r.status_code != 200:
        raise Exception(f"User auth failed {r.status_code}: {r.text[:200]}")
    return r.json()["access_token"]


def _run_dax_sfa(dax_query):
    workspace   = "f2a6b294-ef89-4e41-b6b1-b49adb002715"
    sfa_dataset = _get_secret("FABRIC_SFA_DATASET_ID") or "66e7f737-eda2-47e9-95dc-ec12166cb34f"
    token = _get_user_token()
    url = (f"https://api.powerbi.com/v1.0/myorg/groups/{workspace}"
           f"/datasets/{sfa_dataset}/executeQueries")
    r = requests.post(
        url,
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
        json={"queries": [{"query": dax_query}], "serializerSettings": {"includeNulls": True}},
        timeout=60,
    )
    if r.status_code != 200:
        raise Exception(f"SFA DAX failed {r.status_code}: {r.text[:150]}")
    rows = r.json()["results"][0]["tables"][0].get("rows", [])
    return pd.DataFrame(rows)


def load_rfm_data(country="Nigeria"):
    """
    Attempt to load real RFM transaction data from SFA Reports.
    Returns (DataFrame, status_string) or (None, error_string).
    """
    import streamlit as st

    @st.cache_data(ttl=1800, show_spinner=False)
    def _cached(country):
        try:
            username = _get_secret("FABRIC_USERNAME")
            password = _get_secret("FABRIC_PASSWORD")
            if not all([username, password]):
                return None, "missing_user_credentials"

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
            if df is None or len(df) == 0:
                return None, "empty_result"
            df.columns = ["Shop Name", "last_order_date", "order_count", "total_spend"]
            df["last_order_date"] = pd.to_datetime(df["last_order_date"], errors="coerce")
            df["order_count"]     = pd.to_numeric(df["order_count"],     errors="coerce").fillna(0)
            df["total_spend"]     = pd.to_numeric(df["total_spend"],     errors="coerce").fillna(0)
            df["country"] = country
            return df, "live"
        except Exception as e:
            return None, str(e)[:120]

    return _cached(country)
