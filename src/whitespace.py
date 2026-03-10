def detect_whitespace(model, data):

    features = [
        "population",
        "urban_ratio",
        "hospitals",
        "pharmacies",
        "distributor_count",
        "competitor_count"
    ]

    data["predicted_sales"] = model.predict(data[features])

    data["residual"] = data["predicted_sales"] - data["units_sold"]

    threshold = data["residual"].quantile(0.75)

    data["is_whitespace"] = data["residual"] > threshold

    data["opportunity_score"] = (
        data["residual"] * 0.7 +
        (data["population"] / data["population"].max()) * 0.3
    )

    data = data.sort_values(by="opportunity_score", ascending=False)

    return data