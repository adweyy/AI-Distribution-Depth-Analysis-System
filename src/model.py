from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_squared_error

def train_models(data):

    features = [
        "population",
        "urban_ratio",
        "hospitals",
        "pharmacies",
        "distributor_count",
        "competitor_count"
    ]

    X = data[features]
    y = data["units_sold"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    lr = LinearRegression()
    lr.fit(X_train, y_train)
    lr_pred = lr.predict(X_test)

    rf = RandomForestRegressor(n_estimators=200, random_state=42)
    rf.fit(X_train, y_train)
    rf_pred = rf.predict(X_test)

    results = {
        "Linear Regression R2": r2_score(y_test, lr_pred),
        "Random Forest R2": r2_score(y_test, rf_pred),
        "Linear Regression MSE": mean_squared_error(y_test, lr_pred),
        "Random Forest MSE": mean_squared_error(y_test, rf_pred)
    }

    best_model = rf if results["Random Forest R2"] > results["Linear Regression R2"] else lr

    return best_model, results