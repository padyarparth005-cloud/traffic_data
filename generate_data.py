
import pandas as pd
import numpy as np
from pathlib import Path

np.random.seed(42)
Path("data").mkdir(exist_ok=True)
Path("outputs").mkdir(exist_ok=True)

n = 2000
dates = pd.date_range("2026-09-01", periods=30, freq="D")
hours = np.random.randint(0, 24, n)
days = np.random.randint(0, 30, n)

rush = np.where(
    ((hours >= 7) & (hours <= 10)) |
    ((hours >= 16) & (hours <= 19)),
    1.6, 0.8
)

vehicles = (
    np.random.normal(900, 250, n) * rush
).clip(100, 2500).astype(int)

speed = (
    np.random.normal(55, 10, n) - vehicles / 250
).clip(5, 90).round(2)

df = pd.DataFrame({
    "timestamp": [
        dates[d] + pd.Timedelta(hours=int(h))
        for d, h in zip(days, hours)
    ],
    "district": np.random.choice(
        ["Central", "North", "South", "East", "West"], n
    ),
    "road": np.random.choice(
        ["Main Road", "Ring Road", "Market Road",
         "Airport Road", "Highway"], n
    ),
    "vehicle_count": vehicles,
    "avg_speed_kmh": speed,
    "road_occupancy_pct": np.random.uniform(10, 100, n).round(2),
    "incident": np.random.choice(
        ["None", "Accident", "Roadwork"],
        n, p=[0.88, 0.07, 0.05]
    ),
    "weather": np.random.choice(
        ["Clear", "Rain", "Cloudy"], n
    )
})

df.to_csv("data/traffic_data.csv", index=False)

# Generate a static dashboard output image
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

fig, axes = plt.subplots(2, 2, figsize=(12, 7))
fig.suptitle("SMART CITY TRAFFIC ANALYSIS", fontsize=17, weight="bold")

df["hour"] = pd.to_datetime(df["timestamp"]).dt.hour

df.groupby("hour")["vehicle_count"].mean().plot(
    ax=axes[0, 0], marker="o", color="royalblue"
)
axes[0, 0].set_title("Hourly Traffic")

df.groupby("road")["vehicle_count"].mean().sort_values().plot(
    kind="barh", ax=axes[0, 1], color="teal"
)
axes[0, 1].set_title("Road Congestion")

df.groupby("district")["vehicle_count"].sum().plot(
    kind="bar", ax=axes[1, 0], color="orange"
)
axes[1, 0].set_title("District-wise Traffic")

df[df["incident"] != "None"]["incident"].value_counts().plot(
    kind="pie", autopct="%1.1f%%", ax=axes[1, 1]
)
axes[1, 1].set_title("Traffic Incidents")
axes[1, 1].set_ylabel("")

plt.tight_layout()
plt.savefig("outputs/traffic_dashboard.png", dpi=160)
plt.close()

print("Dataset created: data/traffic_data.csv")
print("Output image created: outputs/traffic_dashboard.png")