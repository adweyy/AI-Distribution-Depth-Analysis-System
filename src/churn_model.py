"""
src/churn_model.py  —  Churn Prediction Model (Upgraded)
=========================================================
Upgraded from RandomForestClassifier → XGBClassifier with:
  · 2 new temporal features  (ytd_3m_trend, ytd_volatility)
  · SHAP-based explainability
  · Class-imbalance handling via scale_pos_weight
  · Early stopping on a held-out eval set

Install dependencies (if not already installed):
    pip install xgboost shap

Public API (unchanged — dashboard won't break):
    engineer_features(df)  → df with all feature columns added
    train(df)              → (model, scored_df, metrics)
    train_churn_model(df)  → alias for train(df)
    active_at_risk(df)     → filtered + sorted at-risk outlets
"""

import ast
import warnings
warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score
from sklearn.metrics import roc_auc_score, classification_report, confusion_matrix
from sklearn.cluster import KMeans
from scipy.spatial import cKDTree

# ── Optional heavy deps — degrade gracefully if missing ───────────────────────
try:
    from xgboost import XGBClassifier
    XGB_AVAILABLE = True
except ImportError:
    from sklearn.ensemble import RandomForestClassifier
    XGB_AVAILABLE = False

try:
    import shap
    SHAP_AVAILABLE = True
except ImportError:
    SHAP_AVAILABLE = False


# ── CONSTANTS ──────────────────────────────────────────────────────────────────
# Original 6 features kept exactly as before, 2 new temporal ones appended
FEATURE_COLS = [
    "is_primary",
    "country_enc",
    "neighbor_count",
    "neighbor_avg_ytd",
    "neighbor_churn_rate",
    "geo_cluster",
    "ytd_3m_trend",       # NEW: linear slope over last 3 monthly YTD values
    "ytd_volatility",     # NEW: std-dev of last 3 monthly YTD values
]

FEATURE_LABELS = {
    "is_primary":          "Retailer Type (Primary)",
    "country_enc":         "Country",
    "ytd_log":             "YTD Revenue (log)",
    "ytd_pct_country":     "YTD Percentile in Country",
    "neighbor_count":      "Nearby Outlet Count",
    "neighbor_avg_ytd":    "Neighbourhood Avg Revenue",
    "neighbor_churn_rate": "Neighbourhood Churn Rate",
    "geo_cluster":         "Geographic Zone",
    "ytd_3m_trend":        "3-Month Sales Trend (slope)",
    "ytd_volatility":      "3-Month Sales Volatility",
}

RISK_BINS   = [0.0, 0.35, 0.65, 1.001]
RISK_LABELS = ["Low Risk", "Medium Risk", "High Risk"]
RISK_COLORS = {
    "Low Risk":    "#22C55E",
    "Medium Risk": "#F59E0B",
    "High Risk":   "#EF4444",
}

NEIGHBOR_RADIUS_DEG = 0.05   # ~5.5 km at the equator


# ── SPATIAL FEATURES (unchanged) ──────────────────────────────────────────────
def _spatial_features(lats, lons, ytds):
    """
    For each outlet, query every other outlet within NEIGHBOR_RADIUS_DEG using
    a cKDTree for fast nearest-neighbour lookup. Returns:
        nc  — neighbour count
        na  — mean YTD of neighbours
        ncr — fraction of neighbours that are churned (YTD == 0)
    """
    coords  = np.column_stack([lats, lons])
    tree    = cKDTree(coords)
    indices = tree.query_ball_tree(tree, NEIGHBOR_RADIUS_DEG)

    n   = len(lats)
    nc  = np.zeros(n, dtype=float)
    na  = np.zeros(n, dtype=float)
    ncr = np.zeros(n, dtype=float)

    for i, nbrs in enumerate(indices):
        nbrs_excl = [j for j in nbrs if j != i]   # exclude self
        if nbrs_excl:
            nc[i]  = len(nbrs_excl)
            na[i]  = float(ytds[nbrs_excl].mean())
            ncr[i] = float((ytds[nbrs_excl] == 0).mean())

    return nc, na, ncr


# ── TEMPORAL FEATURES (NEW) ────────────────────────────────────────────────────
def _temporal_features(monthly_ytd_series):
    """
    Parse the `monthly_ytd` column and compute two churn-signal features per outlet.

    Input format accepted (per row):
        · Python list   — [m1, m2, m3]
        · JSON string   — "[100, 200, 150]"
        · dict          — {'Jan': 100, 'Feb': 200, 'Mar': 150}
        · JSON dict str — "{'Jan': 100, ...}"
        · None / NaN    — falls back to (0, 0)

    Returns:
        trend      (np.ndarray) — slope of np.polyfit(degree=1) through the values.
                                  Negative slope = sales are declining = churn signal.
        volatility (np.ndarray) — std-dev of the values.
                                  High volatility = erratic buyer = churn risk.
    """
    n          = len(monthly_ytd_series)
    trend      = np.zeros(n, dtype=float)
    volatility = np.zeros(n, dtype=float)

    for i, raw in enumerate(monthly_ytd_series):
        try:
            # Step 1 — coerce raw value into a plain Python list of floats
            if raw is None or (isinstance(raw, float) and np.isnan(raw)):
                vals = []
            elif isinstance(raw, (list, np.ndarray)):
                vals = [float(v) for v in raw]
            elif isinstance(raw, dict):
                # dict keyed by month name/number — preserve insertion order
                vals = [float(v) for v in raw.values()]
            elif isinstance(raw, str):
                parsed = ast.literal_eval(raw.strip())
                if isinstance(parsed, dict):
                    vals = [float(v) for v in parsed.values()]
                else:
                    vals = [float(v) for v in parsed]
            else:
                vals = []

            # Step 2 — need ≥2 points for a meaningful slope / std-dev
            if len(vals) >= 2:
                x             = np.arange(len(vals), dtype=float)
                slope, _      = np.polyfit(x, vals, 1)   # degree-1 → [slope, intercept]
                trend[i]      = slope
                volatility[i] = float(np.std(vals, ddof=0))
            # < 2 points → leave as 0 (neutral / no signal)

        except Exception:
            pass   # any parse error → neutral fallback, don't crash the pipeline

    return trend, volatility


# ── FEATURE ENGINEERING ────────────────────────────────────────────────────────
def engineer_features(df):
    """
    Add all model features to the dataframe and return it.

    Original 6 features:
        is_primary, country_enc, neighbor_count, neighbor_avg_ytd,
        neighbor_churn_rate, geo_cluster

    New temporal features (requires `monthly_ytd` column; zeroed-out if absent):
        ytd_3m_trend    — linear sales slope over last 3 months
        ytd_volatility  — sales volatility over last 3 months
    """
    feat = df.copy().reset_index(drop=True)

    # ── Demographic / categorical ────────────────────────────────────────────
    feat["is_primary"]  = (
        feat["Retailer Subtype"]
        .str.contains("Primary", case=False, na=False)
        .astype(int)
    )
    feat["country_enc"] = (feat["country"] == "Angola").astype(int)

    # ── Revenue base ─────────────────────────────────────────────────────────
    feat["ytd_value"]       = feat["YTD Retailing Value"].fillna(0).clip(lower=0)
    feat["ytd_log"]         = np.log1p(feat["ytd_value"])
    feat["ytd_pct_country"] = (
        feat.groupby("country")["ytd_value"].rank(pct=True).fillna(0)
    )

    # ── Spatial neighbourhood features ───────────────────────────────────────
    lats = feat["latitude"].fillna(0).values.astype(float)
    lons = feat["longitude"].fillna(0).values.astype(float)
    ytds = feat["ytd_value"].values

    nc, na, ncr = _spatial_features(lats, lons, ytds)
    feat["neighbor_count"]      = nc
    feat["neighbor_avg_ytd"]    = na
    feat["neighbor_churn_rate"] = ncr

    # ── Geographic clustering (KMeans on lat/lon) ────────────────────────────
    n_clusters          = min(30, max(2, len(feat) // 300))
    km                  = KMeans(n_clusters=n_clusters, random_state=42, n_init="auto")
    feat["geo_cluster"] = km.fit_predict(np.column_stack([lats, lons]))

    # ── NEW: Temporal features from monthly_ytd ──────────────────────────────
    if "monthly_ytd" in feat.columns:
        trend, vol              = _temporal_features(feat["monthly_ytd"])
        feat["ytd_3m_trend"]    = trend    # negative → declining sales → churn risk
        feat["ytd_volatility"]  = vol      # high → erratic buyer → churn risk
    else:
        # monthly_ytd not yet loaded — zero-fill so the model still runs
        feat["ytd_3m_trend"]   = 0.0
        feat["ytd_volatility"] = 0.0

    return feat


# ── MODEL TRAINING ─────────────────────────────────────────────────────────────
def train(df):
    """
    Train the churn model.

    Returns
    -------
    clf        : trained model (XGBClassifier or RandomForestClassifier)
    feat       : full dataframe with churn_prob and risk_tier columns added
    metrics    : dict with AUC, CV-AUC, precision/recall/F1, feature importances,
                 SHAP values (if shap is installed), and model metadata
    """
    feat = engineer_features(df)

    # Churn label: YTD == 0 → churned (1), else active (0)
    feat["is_churned"] = (feat["ytd_value"] == 0).astype(int)

    X = feat[FEATURE_COLS].fillna(0)
    y = feat["is_churned"]

    X_tr, X_te, y_tr, y_te = train_test_split(
        X, y, test_size=0.2, stratify=y, random_state=42
    )

    # ── Class-imbalance weight for XGBoost ──────────────────────────────────
    # scale_pos_weight = #negatives / #positives  (recommended by XGBoost docs)
    neg_count = int((y_tr == 0).sum())
    pos_count = int((y_tr == 1).sum())
    spw       = neg_count / max(pos_count, 1)

    # ── Classifier ───────────────────────────────────────────────────────────
    if XGB_AVAILABLE:
        clf = XGBClassifier(
            n_estimators        = 500,
            max_depth           = 6,
            learning_rate       = 0.05,
            subsample           = 0.85,
            colsample_bytree    = 0.8,
            early_stopping_rounds = 30,    # halt if val-AUC stalls for 30 rounds
            scale_pos_weight    = spw,     # corrects for class imbalance
            eval_metric         = "auc",
            random_state        = 42,
            n_jobs              = -1,
            verbosity           = 0,
        )
        # Pass eval_set so early stopping has something to monitor
        clf.fit(
            X_tr, y_tr,
            eval_set  = [(X_te, y_te)],
            verbose   = False,
        )
        model_type = "XGBoost"

    else:
        # Fallback — keeps the app functional without xgboost installed
        from sklearn.ensemble import RandomForestClassifier
        clf = RandomForestClassifier(
            n_estimators    = 300,
            max_depth       = 10,
            min_samples_leaf= 8,
            class_weight    = "balanced",
            random_state    = 42,
            n_jobs          = -1,
        )
        clf.fit(X_tr, y_tr)
        model_type = "RandomForest (xgboost not installed)"

    # ── Test-set predictions ─────────────────────────────────────────────────
    y_pred  = clf.predict(X_te)
    y_proba = clf.predict_proba(X_te)[:, 1]

    # ── 5-fold cross-validated AUC ───────────────────────────────────────────
    # Use a lighter model for CV speed (early stopping can't be used in CV easily)
    if XGB_AVAILABLE:
        cv_clf = XGBClassifier(
            n_estimators     = 300,
            max_depth        = 6,
            learning_rate    = 0.05,
            subsample        = 0.85,
            colsample_bytree = 0.8,
            scale_pos_weight = spw,
            eval_metric      = "auc",
            random_state     = 42,
            n_jobs           = -1,
            verbosity        = 0,
        )
    else:
        from sklearn.ensemble import RandomForestClassifier
        cv_clf = RandomForestClassifier(
            n_estimators=100, max_depth=8,
            class_weight="balanced", random_state=42, n_jobs=-1
        )

    cv_auc = cross_val_score(
        cv_clf, X, y,
        cv      = StratifiedKFold(n_splits=5, shuffle=True, random_state=42),
        scoring = "roc_auc",
    )

    report = classification_report(y_te, y_pred, output_dict=True)

    # ── Feature importance (XGBoost built-in gain scores) ───────────────────
    feat_imp_sorted = sorted(
        [
            (FEATURE_LABELS.get(c, c), round(float(v), 4))
            for c, v in zip(FEATURE_COLS, clf.feature_importances_)
        ],
        key=lambda x: x[1],
        reverse=True,
    )

    # ── SHAP explainability ──────────────────────────────────────────────────
    shap_values_out = None
    shap_feat_names = list(X_te.columns)
    shap_imp_sorted = None

    if SHAP_AVAILABLE:
        try:
            explainer   = shap.TreeExplainer(clf)
            shap_values = explainer.shap_values(X_te)

            # Binary classifiers may return a list [neg_class, pos_class]
            # We always want positive-class (churn) SHAP values
            if isinstance(shap_values, list) and len(shap_values) == 2:
                sv = shap_values[1]
            else:
                sv = shap_values

            shap_values_out = sv   # shape: (n_test_samples, n_features)

            # Rank features by mean |SHAP| — more interpretable than gain
            mean_abs_shap   = np.abs(sv).mean(axis=0)
            shap_imp_sorted = sorted(
                [
                    (FEATURE_LABELS.get(c, c), round(float(v), 4))
                    for c, v in zip(FEATURE_COLS, mean_abs_shap)
                ],
                key=lambda x: x[1],
                reverse=True,
            )
        except Exception:
            pass   # SHAP failure is non-fatal — dashboard degrades gracefully

    # ── Score the full dataset (all outlets get a churn probability) ─────────
    feat["churn_prob"] = clf.predict_proba(X)[:, 1]
    feat["risk_tier"]  = pd.cut(
        feat["churn_prob"],
        bins   = RISK_BINS,
        labels = RISK_LABELS,
    ).astype(str)

    metrics = {
        # Core performance
        "auc":             round(roc_auc_score(y_te, y_proba), 3),
        "cv_auc_mean":     round(float(cv_auc.mean()), 3),
        "cv_auc_std":      round(float(cv_auc.std()),  3),
        "precision_churn": round(report["1"]["precision"], 3),
        "recall_churn":    round(report["1"]["recall"],    3),
        "f1_churn":        round(report["1"]["f1-score"],  3),
        "accuracy":        round(report["accuracy"],       3),
        "conf_mat":        confusion_matrix(y_te, y_pred).tolist(),
        # Feature importance (XGBoost gain-based)
        "feat_imp":        feat_imp_sorted,
        # SHAP explainability (None if shap not installed)
        "shap_values":     shap_values_out,
        "shap_feat_names": shap_feat_names,
        "shap_imp":        shap_imp_sorted,
        # Dataset stats
        "n_train":         len(X_tr),
        "n_test":          len(X_te),
        "churn_rate_pct":  round(float(y.mean()) * 100, 1),
        "total_outlets":   len(df),
        "total_churned":   int(y.sum()),
        # Model metadata
        "model_type":      model_type,
        "n_features":      len(FEATURE_COLS),
        "temporal_active": "monthly_ytd" in df.columns,
    }

    return clf, feat, metrics


# ── PUBLIC ALIAS (matches prompt spec; dashboard keeps calling train()) ────────
def train_churn_model(df):
    """Alias for train(df) — same return signature."""
    return train(df)


# ── HELPERS ────────────────────────────────────────────────────────────────────
def active_at_risk(scored_df):
    """Return only currently-active outlets, sorted by churn probability desc."""
    active = scored_df[scored_df["ytd_value"] > 0].copy()
    return active.sort_values("churn_prob", ascending=False)
