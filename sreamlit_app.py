import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from pathlib import Path

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Electricity Consumption Analysis",
    page_icon="⚡",
    layout="wide"
)

# ---------------- CUSTOM DESIGN ----------------
st.markdown("""
<style>
.main {
    background-color: #f5f7fb;
}
[data-testid="stMetric"] {
    background-color: white;
    padding: 18px;
    border-radius: 12px;
    border: 1px solid #e5e7eb;
}
h1 {
    color: #174ea6;
}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.title("⚡ Electricity Consumption Dashboard")
st.markdown(
    "### Analyse, monitor and understand electricity usage trends"
)
st.caption("Data Science Mini Project | Aryan Raj | Roll No. 124557")

# ---------------- SIDEBAR ----------------
st.sidebar.title("Dashboard Controls")

uploaded_file = st.sidebar.file_uploader(
    "Upload Electricity CSV Dataset",
    type=["csv"]
)

# ---------------- LOAD DATA ----------------
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    data_source = "Uploaded CSV"
else:
    possible_files = [
        Path("dataset/electricity_data.csv"),
        Path("electricity_data.csv")
    ]

    existing_file = next(
        (file for file in possible_files if file.exists()),
        None
    )

    if existing_file:
        df = pd.read_csv(existing_file)
        data_source = str(existing_file)
    else:
        # Clearly labelled demonstration data
        np.random.seed(42)
        dates = pd.date_range(
            start="2026-01-01",
            periods=180,
            freq="D"
        )

        consumption = (
            30
            + 8 * np.sin(np.arange(180) * 2 * np.pi / 30)
            + np.random.normal(0, 4, 180)
        )

        df = pd.DataFrame({
            "Date": dates,
            "Consumption": np.maximum(consumption, 5)
        })

        data_source = "Demonstration data (sample)"

# ---------------- COLUMN SELECTION ----------------
st.sidebar.subheader("Data Configuration")

date_candidates = [
    col for col in df.columns
    if any(word in col.lower() for word in ["date", "day", "time"])
]

default_date_index = (
    df.columns.get_loc(date_candidates[0])
    if date_candidates else 0
)

date_column = st.sidebar.selectbox(
    "Select Date Column",
    df.columns.tolist(),
    index=default_date_index
)

numeric_columns = df.select_dtypes(
    include=np.number
).columns.tolist()

if not numeric_columns:
    st.error("No numeric consumption column found in this CSV.")
    st.info("Please upload a CSV containing a numeric electricity consumption column.")
    st.stop()

consumption_candidates = [
    col for col in numeric_columns
    if any(word in col.lower() for word in [
        "consumption", "electricity", "units", "usage", "kwh"
    ])
]

default_consumption = (
    consumption_candidates[0]
    if consumption_candidates else numeric_columns[0]
)

consumption_column = st.sidebar.selectbox(
    "Select Consumption Column",
    numeric_columns,
    index=numeric_columns.index(default_consumption)
)

# ---------------- CLEAN DATA ----------------
df[date_column] = pd.to_datetime(
    df[date_column],
    errors="coerce"
)

df[consumption_column] = pd.to_numeric(
    df[consumption_column],
    errors="coerce"
)

df = df.dropna(
    subset=[date_column, consumption_column]
).copy()

df = df.rename(columns={
    date_column: "Date",
    consumption_column: "Consumption"
})

df = df.sort_values("Date")

if df.empty:
    st.error("No valid data found. Please check your CSV file.")
    st.stop()

st.sidebar.caption(f"Data source: {data_source}")

# ---------------- DATE FILTER ----------------
st.sidebar.subheader("Date Filter")

min_date = df["Date"].min().date()
max_date = df["Date"].max().date()

date_range = st.sidebar.date_input(
    "Select date range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

if isinstance(date_range, (tuple, list)) and len(date_range) == 2:
    start_date, end_date = date_range

    filtered_df = df[
        (df["Date"].dt.date >= start_date) &
        (df["Date"].dt.date <= end_date)
    ].copy()
else:
    filtered_df = df.copy()

if filtered_df.empty:
    st.warning("No data available for the selected date range.")
    st.stop()

# ---------------- CALCULATIONS ----------------
total_units = filtered_df["Consumption"].sum()
average_units = filtered_df["Consumption"].mean()
highest_units = filtered_df["Consumption"].max()
lowest_units = filtered_df["Consumption"].min()

highest_day = filtered_df.loc[
    filtered_df["Consumption"].idxmax(), "Date"
].strftime("%d %b %Y")

# ---------------- KPI CARDS ----------------
st.markdown("## 📊 Consumption Overview")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Consumption", f"{total_units:,.2f} units")
col2.metric("Average Usage", f"{average_units:,.2f} units")
col3.metric("Highest Usage", f"{highest_units:,.2f} units")
col4.metric("Lowest Usage", f"{lowest_units:,.2f} units")

st.caption(f"Highest consumption recorded on: {highest_day}")

# ---------------- DAILY TREND ----------------
st.markdown("---")
st.subheader("📈 Daily Electricity Consumption")

daily_df = filtered_df.copy()
daily_df["Moving Average"] = (
    daily_df["Consumption"]
    .rolling(window=7, min_periods=1)
    .mean()
)

fig_daily = px.line(
    daily_df,
    x="Date",
    y=["Consumption", "Moving Average"],
    title="Daily Usage and 7-Day Moving Average",
    labels={
        "value": "Electricity Units",
        "Date": "Date",
        "variable": "Metric"
    },
    template="plotly_white"
)

st.plotly_chart(fig_daily, use_container_width=True)

# ---------------- MONTHLY ANALYSIS ----------------
st.markdown("---")
st.subheader("📅 Monthly Consumption Analysis")

monthly_df = (
    filtered_df
    .set_index("Date")["Consumption"]
    .resample("MS")
    .sum()
    .reset_index()
)

monthly_df["Month"] = monthly_df["Date"].dt.strftime("%b %Y")

fig_monthly = px.bar(
    monthly_df,
    x="Month",
    y="Consumption",
    title="Monthly Electricity Consumption",
    text_auto=".2f",
    template="plotly_white"
)

st.plotly_chart(fig_monthly, use_container_width=True)

# ---------------- DISTRIBUTION ----------------
st.markdown("---")
st.subheader("📊 Usage Distribution")

fig_hist = px.histogram(
    filtered_df,
    x="Consumption",
    nbins=20,
    title="Distribution of Electricity Usage",
    template="plotly_white"
)

st.plotly_chart(fig_hist, use_container_width=True)

# ---------------- DATA TABLE ----------------
st.markdown("---")
st.subheader("📋 Electricity Consumption Records")

st.dataframe(
    filtered_df,
    use_container_width=True,
    hide_index=True
)

# ---------------- DOWNLOAD REPORT ----------------
csv_data = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="⬇️ Download Consumption Report (CSV)",
    data=csv_data,
    file_name="electricity_consumption_report.csv",
    mime="text/csv"
)

# ---------------- FOOTER ----------------
st.markdown("---")
st.markdown(
    "<center>Made by Aryan Raj | Data Science Mini Project ⚡</center>",
    unsafe_allow_html=True
)