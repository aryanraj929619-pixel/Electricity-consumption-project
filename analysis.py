
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Project folder paths
BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "dataset" / "electricity_data.csv"
GRAPH_DIR = BASE_DIR / "graphs"

# Create graphs folder if needed
GRAPH_DIR.mkdir(exist_ok=True)

# Load dataset
df = pd.read_csv(DATA_FILE)
df["date"] = pd.to_datetime(df["date"])

# Sort data by date
df = df.sort_values("date")

# Calculate 3-month moving average
df["moving_average"] = (
    df["consumption_kwh"].rolling(window=3).mean()
)

# Calculate statistics
average_usage = df["consumption_kwh"].mean()
maximum_usage = df["consumption_kwh"].max()
minimum_usage = df["consumption_kwh"].min()

highest_month = df.loc[
    df["consumption_kwh"].idxmax(), "date"
].strftime("%B")

lowest_month = df.loc[
    df["consumption_kwh"].idxmin(), "date"
].strftime("%B")

# Display results
print("\nELECTRICITY CONSUMPTION ANALYSIS")
print("--------------------------------")
print(f"Average Usage: {average_usage:.2f} kWh")
print(f"Maximum Usage: {maximum_usage} kWh")
print(f"Minimum Usage: {minimum_usage} kWh")
print(f"Highest Consumption Month: {highest_month}")
print(f"Lowest Consumption Month: {lowest_month}")

print("\nMonthly Consumption:")
print(df.to_string(index=False))

# Plot consumption trend
plt.figure(figsize=(11, 6))

plt.plot(
    df["date"],
    df["consumption_kwh"],
    marker="o",
    label="Monthly Consumption"
)

plt.plot(
    df["date"],
    df["moving_average"],
    linestyle="--",
    label="3-Month Moving Average"
)

plt.title("Electricity Consumption Trend Analysis")
plt.xlabel("Month")
plt.ylabel("Consumption (kWh)")
plt.legend()
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()

# Save graph
plt.savefig(GRAPH_DIR / "consumption_trend.png")
plt.show()

print("\nGraph saved successfully in graphs folder!")

# Monthly Consumption Bar Chart

month_labels = df["date"].dt.strftime("%b")

plt.figure(figsize=(10, 5))

plt.bar(month_labels, df["consumption_kwh"])

plt.title("Monthly Electricity Consumption")

plt.xlabel("Month")

plt.ylabel("Consumption (kWh)")

plt.grid(axis="y", linestyle="--", alpha=0.5)

plt.tight_layout()

# Save bar chart
plt.savefig(GRAPH_DIR / "monthly_consumption.png")

plt.show()

print("Monthly bar chart saved successfully!")
