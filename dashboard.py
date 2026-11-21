
import pandas as pd
import matplotlib.pyplot as plt

# Load dataset
df = pd.read_csv("dataset/electricity_data.csv")

df["date"] = pd.to_datetime(df["date"])
df = df.sort_values("date")

# Calculate statistics
total = df["consumption_kwh"].sum()
average = df["consumption_kwh"].mean()
maximum = df["consumption_kwh"].max()
minimum = df["consumption_kwh"].min()

# Calculate moving average
df["moving_average"] = (
    df["consumption_kwh"].rolling(window=3).mean()
)

# Create dashboard
fig, axes = plt.subplots(2, 2, figsize=(14, 9))

fig.suptitle(
    "ELECTRICITY CONSUMPTION DASHBOARD",
    fontsize=18,
    fontweight="bold"
)

# Monthly bar chart
axes[0, 0].bar(
    df["date"].dt.strftime("%b"),
    df["consumption_kwh"]
)
axes[0, 0].set_title("Monthly Consumption")
axes[0, 0].set_ylabel("Consumption (kWh)")

# Consumption trend
axes[0, 1].plot(
    df["date"],
    df["consumption_kwh"],
    marker="o"
)
axes[0, 1].set_title("Consumption Trend")
axes[0, 1].set_ylabel("kWh")

# Moving average
axes[1, 0].plot(
    df["date"],
    df["moving_average"],
    marker="o"
)
axes[1, 0].set_title("3-Month Moving Average")
axes[1, 0].set_ylabel("kWh")

# Summary
axes[1, 1].axis("off")

summary = f"""
TOTAL CONSUMPTION

{total} kWh

AVERAGE CONSUMPTION

{average:.2f} kWh

MAXIMUM CONSUMPTION

{maximum} kWh

MINIMUM CONSUMPTION

{minimum} kWh
"""

axes[1, 1].text(
    0.1, 0.5,
    summary,
    fontsize=13,
    verticalalignment="center"
)

plt.tight_layout()

# Save dashboard
plt.savefig(
    "graphs/electricity_dashboard.png",
    dpi=300
)

plt.show()

print("Dashboard created successfully!")
