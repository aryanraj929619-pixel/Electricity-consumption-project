
import pandas as pd

# Load electricity dataset
df = pd.read_csv("dataset/electricity_data.csv")

# Convert date column into datetime
df["date"] = pd.to_datetime(df["date"])

# Calculate total and average consumption
total = df["consumption_kwh"].sum()
average = df["consumption_kwh"].mean()

# Find maximum and minimum consumption
maximum = df["consumption_kwh"].max()
minimum = df["consumption_kwh"].min()

# Find highest and lowest consumption months
highest_month = df.loc[
    df["consumption_kwh"].idxmax(), "date"
].strftime("%B")

lowest_month = df.loc[
    df["consumption_kwh"].idxmin(), "date"
].strftime("%B")

# Display report
print("\n================================")
print(" ELECTRICITY CONSUMPTION REPORT")
print("================================")

print(f"Total Consumption: {total} kWh")
print(f"Average Consumption: {average:.2f} kWh")
print(f"Maximum Consumption: {maximum} kWh")
print(f"Minimum Consumption: {minimum} kWh")

print(f"Highest Consumption Month: {highest_month}")
print(f"Lowest Consumption Month: {lowest_month}")

print("\nENERGY CONSERVATION SUGGESTIONS")

print("1. Switch off unnecessary electrical appliances.")
print("2. Use LED lights to save electricity.")
print("3. Use energy-efficient appliances.")
print("4. Monitor electricity consumption regularly.")

print("\nNote: This report uses illustrative sample data.")

print("\n================================")
print(" REPORT GENERATED SUCCESSFULLY")
print("================================")

# Save report into a text file

report_content = f"""
ELECTRICITY CONSUMPTION REPORT
================================

Total Consumption: {total} kWh
Average Consumption: {average:.2f} kWh

Maximum Consumption: {maximum} kWh
Minimum Consumption: {minimum} kWh

Highest Consumption Month: {highest_month}
Lowest Consumption Month: {lowest_month}

ENERGY CONSERVATION SUGGESTIONS

1. Switch off unnecessary electrical appliances.
2. Use LED lights to save electricity.
3. Use energy-efficient appliances.
4. Monitor electricity consumption regularly.

Note: This report uses illustrative sample data.
"""

with open("electricity_report.txt", "w", encoding="utf-8") as file:
    file.write(report_content)

print("Report saved successfully!")
