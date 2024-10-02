import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from streamlit import exception


def create_daily_orders_df(df):
    daily_orders_df = df.resample(rule='D', on='dteday').agg({
        "cnt": "sum",
    }).reset_index()

    return daily_orders_df

def create_monthly_orders_df(df):
    monthly_orders_df = df.groupby("mnth", observed=False).agg({
        "cnt": "mean",
    }).reset_index()
    monthly_orders_df["mnth"] = monthly_orders_df["mnth"].map({
        1: "Jan",
        2: "Feb",
        3: "Mar",
        4: "Apr",
        5: "May",
        6: "Jun",
        7: "Jul",
        8: "Aug",
        9: "Sep",
        10: "Oct",
        11: "Nov",
        12: "Dec"
    })

    return monthly_orders_df

def create_weekly_orders_df(df):
    weekly_orders_df = df.groupby("dteday", observed=False).agg({
        "cnt": "sum",
        "weekday": "first"
    }).reset_index()
    weekly_orders_df = weekly_orders_df.groupby("weekday").agg({
        "cnt": "mean"
    }).reset_index()
    weekly_orders_df["weekday"] = weekly_orders_df["weekday"].map({
        0: "Sun",
        1: "Mon",
        2: "Tue",
        3: "Wed",
        4: "Thu",
        5: "Fri",
        6: "Sat"
    })

    return weekly_orders_df

def create_hourly_orders_df(df):
    hourly_orders_df = df.groupby("hr", observed=False).agg({
        "cnt": "mean",
    }).reset_index()

    return hourly_orders_df

def create_seasonal_orders_df(df):
    seasonal_orders_df = df.groupby("season", observed=False).agg({
        "cnt": "mean",
    }).reset_index()
    seasonal_orders_df["season"] = seasonal_orders_df["season"].map({
        1: "Spring",
        2: "Summer",
        3: "Fall",
        4: "Winter"
    })

    return seasonal_orders_df

def create_weather_df(df):
    weather_df = df.groupby("weathersit", observed=False).agg({
        "cnt": "mean",
    }).reset_index()
    weather_df["weathersit"] = weather_df["weathersit"].map({
        1: "Clear",
        2: "Mist",
        3: "Light Rain/Snow",
        4: "Heavy Rain/Snow"
    })

    return weather_df

def create_user_segmentation_df(df):
    user_segmentation_df = df.agg({
        "registered": ["sum", "mean"],
        "casual": ["sum", "mean"]
    })

    return user_segmentation_df

def create_daytype_df(df):
    daytype_df = df.groupby("workingday", observed=False).agg({
        "cnt": ["sum", "mean"]
    }).reset_index()
    daytype_df["workingday"] = daytype_df["workingday"].map({
        0: "Holiday",
        1: "Working Day"
    })

    return daytype_df

all_df = pd.read_csv("./dashboard/main_data.csv")

all_df.sort_values(by="dteday", inplace=True)
all_df.reset_index(inplace=True)

all_df["dteday"] = pd.to_datetime(all_df["dteday"])

MIN_DATE = all_df["dteday"].min()
MAX_DATE = all_df["dteday"].max()

with st.sidebar:
    st.title("Dashboard")
    st.write("Enter The Date Range")
    MIN_DATE = st.date_input(
        label="Min Date",
        min_value=MIN_DATE, max_value=MAX_DATE,
        value=MIN_DATE
    )
    MAX_DATE = st.date_input(
        label="Max Date",
        min_value=MIN_DATE, max_value=MAX_DATE,
        value=MAX_DATE
    )

    st.divider()

    st.caption("by **Ashilpa Darrel Bumika** (darrell_ashl)")

main_df = all_df[(all_df["dteday"] >= str(MIN_DATE)) &
                 (all_df["dteday"] <= str(MAX_DATE))]

daily_orders_df = create_daily_orders_df(main_df)
monthly_orders_df = create_monthly_orders_df(main_df)
weekly_orders_df = create_weekly_orders_df(main_df)
hourly_orders_df = create_hourly_orders_df(main_df)
seasonal_orders_df = create_seasonal_orders_df(main_df)
weather_df = create_weather_df(main_df)
user_segmentation_df = create_user_segmentation_df(main_df)
daytype_df = create_daytype_df(main_df)

st.header("Bike Rental Dashboard 🚲⛅")

st.write(f"{MIN_DATE} to {MAX_DATE}")

st.divider()

st.subheader("Data Overview")

col1, col2, col3 = st.columns(3)

with col1:
    total_orders = daily_orders_df.cnt.sum()
    st.metric(label="Total Bike Rental", value=f"{total_orders:,}")

with col2:
    average_orders = daily_orders_df.cnt.mean()
    st.metric(label="Average per Day", value=f"{average_orders:,.2f}")

with col3:
    max_orders = daily_orders_df.cnt.max()
    st.write(f"Max : {max_orders:,}")

    min_orders = daily_orders_df.cnt.min()
    st.write(f"Min : {min_orders:,}")

fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    daily_orders_df["dteday"],
    daily_orders_df["cnt"],
    marker='o',
    linewidth=2,
    color="#2e8a7f"
)

ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)

st.pyplot(fig)

st.divider()

st.subheader("Time-Based Analysis")

tab1, tab2, tab3, tab4 = st.tabs(["by Month", "by Weekday", "by Hour", "by Season"])

with tab1:
    st.subheader("Average Monthly Orders")

    fig, ax = plt.subplots(figsize=(16, 8))
    sns.barplot(
        x=monthly_orders_df["mnth"],
        y=monthly_orders_df["cnt"],
        ax=ax,
        palette="viridis"
    )

    ax.set_xlabel("Month")
    ax.set_ylabel("Average Orders")

    plt.title("Average Monthly Orders")

    st.pyplot(fig)

    col1, col2 = st.columns(2)
    with col1:
        min_orders = monthly_orders_df.cnt.min()
        st.metric(label="Min", value=f"{min_orders:,.2f}")

    with col2:
        max_orders = monthly_orders_df.cnt.max()
        st.metric(label="Max", value=f"{max_orders:,.2f}")

with tab2:
    st.subheader("Average Weekday Rent")

    fig, ax = plt.subplots(figsize=(16, 8))
    sns.barplot(
        x='weekday',
        y='cnt',
        ax=ax,
        data=weekly_orders_df,
        palette="viridis"
    )

    ax.set_xlabel("Day")
    ax.set_ylabel("Average Orders")

    plt.title("Average Weekday Rent")

    st.pyplot(fig)

    col1, col2 = st.columns(2)
    with col1:
        min_orders = weekly_orders_df.cnt.min()
        st.metric(label="Min", value=f"{min_orders:,.2f}")

    with col2:
        max_orders = weekly_orders_df.cnt.max()
        st.metric(label="Max", value=f"{max_orders:,.2f}")

with tab3:
    st.subheader("Average Hourly Rent")

    fig, ax = plt.subplots(figsize=(16, 8))
    sns.barplot(
        x=hourly_orders_df.index,
        y=hourly_orders_df["cnt"],
        ax=ax,
        palette="viridis"
    )

    ax.set_xlabel("Hour")
    ax.set_ylabel("Average Orders")

    plt.title("Average Hourly Rent")

    st.pyplot(fig)

    col1, col2 = st.columns(2)
    with col1:
        min_orders = hourly_orders_df.cnt.min()
        st.metric(label="Min", value=f"{min_orders:,.2f}")

    with col2:
        max_orders = hourly_orders_df.cnt.max()
        st.metric(label="Max", value=f"{max_orders:,.2f}")

with tab4:
    st.subheader("Average Seasonal Rent")

    fig, ax = plt.subplots(figsize=(16, 8))
    sns.barplot(
        x='season',
        y='cnt',
        ax=ax,
        data=seasonal_orders_df,
        palette="viridis"
    )

    ax.set_xlabel("Season")
    ax.set_ylabel("Average Orders")

    plt.title("Average Seasonal Rent")

    st.pyplot(fig)

    col1, col2 = st.columns(2)
    with col1:
        min_orders = seasonal_orders_df.cnt.min()
        st.metric(label="Min", value=f"{min_orders:,.2f}")

    with col2:
        max_orders = seasonal_orders_df.cnt.max()
        st.metric(label="Max", value=f"{max_orders:,.2f}")

st.divider()

st.subheader("Weather Conditions")

cols = st.columns((2, 1))

with cols[0]:
    fig, ax = plt.subplots(figsize=(16, 8))
    plt.pie(
        weather_df["cnt"],
        labels=weather_df["weathersit"],
        autopct='%1.1f%%',
        startangle=90,
        colors=sns.color_palette("viridis", n_colors=4)
    )

    plt.title("Average Rent by Weather Conditions")

    st.pyplot(fig)

with cols[1]:
    st.write("- **Clear** : Clear, Few clouds, Partly cloudy, Partly cloudy")
    st.write("- **Mist** : Mist + Cloudy, Mist + Broken clouds, Mist + Few clouds, Mist")
    st.write("- **Light Rain/Snow** : Light Snow, Light Rain + Thunderstorm + Scattered clouds, Light Rain + Scattered clouds")
    st.write("- **Heavy Rain/Snow** : Heavy Rain + Ice Pallets + Thunderstorm + Mist, Snow + Fog")

col1, col2, col3, col4 = st.columns(4)

with col1:
    try:
        weather_avg = weather_df["cnt"][0] or 0
    except Exception as e:
        weather_avg = 0
    st.metric(label="Avg Rent when Clear", value=f"{weather_avg:,.2f}")

with col2:
    try:
        weather_avg = weather_df["cnt"][1] or 0
    except Exception as e:
        weather_avg = 0
    st.metric(label="Avg Rent when Mist", value=f"{weather_avg:,.2f}")

with col3:
    try:
        weather_avg = weather_df["cnt"][2] or 0
    except Exception as e:
        weather_avg = 0
    st.metric(label="Avg Rent when Light Rain/Snow", value=f"{weather_avg:,.2f}")

with col4:
    try:
        weather_avg = weather_df["cnt"][3] or 0
    except Exception as e:
        weather_avg = 0
    st.metric(label="Avg Rent when Heavy Rain/Snow", value=f"{weather_avg:,.2f}")

st.divider()

st.subheader("User Segmentation")

col1, col2 = st.columns(2)

with col1:
    st.metric(label="Registered Average", value=f"{user_segmentation_df['registered']["mean"]:.2f}")
    st.metric(label="Registered Total", value=f"{user_segmentation_df['registered']["sum"]:,.0f}")

with col2:
    st.metric(label="Casual Average", value=f"{user_segmentation_df['casual']["mean"]:.2f}")
    st.metric(label="Casual Total", value=f"{user_segmentation_df['casual']["sum"]:,.0f}")

fig, ax = plt.subplots(figsize=(16, 8))
plt.pie(
    (user_segmentation_df["registered"]["mean"], user_segmentation_df["casual"]["mean"]),
    labels=("Registered", "Casual"),
    autopct='%1.1f%%',
    startangle=90,
    colors=sns.color_palette("viridis", n_colors=2)
)

plt.title("Average Rent by User Segmentation")

st.pyplot(fig)

st.divider()

st.subheader("Holiday vs Working Day")

col1, col2 = st.columns(2)

with col1:
    st.metric(label="Rent when Holiday Average", value=f"{daytype_df['cnt']["mean"][0]:,.2f}")
    st.metric(label="Rent when Holiday Total", value=f"{daytype_df['cnt']["sum"][0]:,.0f}")

with col2:
    st.metric(label="Rent when Working Day Average", value=f"{daytype_df['cnt']["mean"][1]:,.2f}")
    st.metric(label="Rent when Working Day Total", value=f"{daytype_df['cnt']["sum"][1]:,.0f}")

fig, ax = plt.subplots(figsize=(16, 8))
plt.pie(
    daytype_df["cnt"]["mean"],
    labels=daytype_df["workingday"],
    autopct='%1.1f%%',
    startangle=90,
    colors=sns.color_palette("viridis", n_colors=2)
)

plt.title("Average Rent by Day Type")

st.pyplot(fig)
