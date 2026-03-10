import pandas as pd
import numpy as np

np.random.seed(42)

regions = 300

data = pd.DataFrame({
    "region_id": range(1, regions + 1),
    "population": np.random.randint(50000, 1500000, regions),
    "urban_ratio": np.random.uniform(0.2, 0.9, regions),
    "hospitals": np.random.randint(1, 80, regions),
    "pharmacies": np.random.randint(5, 300, regions),
    "distributor_count": np.random.randint(0, 15, regions),
    "competitor_count": np.random.randint(0, 10, regions),
})

data["units_sold"] = (
    0.0006 * data["population"] +
    60 * data["hospitals"] +
    25 * data["pharmacies"] -
    120 * data["competitor_count"] +
    np.random.normal(0, 8000, regions)
)

data["units_sold"] = data["units_sold"].abs()

data.to_csv("data/sample_data.csv", index=False)

print("Dataset generated successfully.")