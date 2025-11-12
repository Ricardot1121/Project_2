import streamlit as st
import pandas as pd
import plotly.express as px
import time

# ----------------------------------
# Streamlit Page Setup
# ----------------------------------
st.set_page_config(page_title="Video Games", page_icon="📡", layout="wide")

# Disable transitions so charts don't blink between reruns
st.markdown("""
    <style>
      [data-testid="stPlotlyChart"], .stPlotlyChart, .stElementContainer {
        transition: none !important;
        opacity: 1 !important;
      }
    </style>
""", unsafe_allow_html=True)

# ==================================
# SECTION 1: Game Development Costs
# ==================================
st.title("Cost($) of Video Game Development")
st.caption("The development cost of well-received video games in the past decade (2015 - 2024).")

# Load and clean data
df = pd.read_csv("data/top10.csv")
median_cost = df["Cost of Development"].median()
df["Cost of Development"].fillna(median_cost, inplace=True)
df["Color"] = df["GOTY"].apply(lambda x: "gold" if x == 1 else "blue")

st.write(df.head())

# Create a bar chart
fig_cost = px.bar(
    df,
    x="Cost of Development",
    y="Video Games",
    color="Color",
    title="Development Costs of Video Games",
    labels={"Video Games": "Video Games", "Cost of Development": "Development Cost($)"},
    color_discrete_map={"gold": "gold", "blue": "blue"},
    hover_name="Video Games",
    hover_data=["Cost of Development"]
)
st.plotly_chart(fig_cost, use_container_width=True)

# Explanation text blocks
statement1 = [
    "The bar chart above helps answer whether or not a higher budget affects the quality of a video game, and whether those games have won GOTY (Game of the Year)."
]
read1 = [
    "The x-axis indicates the cost of development of the listed video games.",
    "The y-axis shows the titles of the video games.",
    "Gold indicates GOTY winners; blue indicates non-winners."
]
insight1 = ["", "", ""]

st.markdown("### Statement:")
for f in statement1:
    st.write(f"- {f}")
st.markdown("### How to read this chart:")
for f in read1:
    st.write(f"- {f}")
st.markdown("### Observations/Insights:")
for f in insight1:
    st.write(f"- {f}")

# ==================================
# SECTION 2: Game Sales Over Time
# ==================================
st.title("Video Game Sale History")
st.caption("The amount of units each video game has sold since their release year.")

# Load and clean sales data
sales_df = pd.read_csv("10salehistory.csv")

# Helper function to convert 'm' to millions
def convert_sales(value):
    if isinstance(value, str) and "m" in value:
        return float(value.replace("m", "")) * 1_000_000
    return None

for col in sales_df.columns[1:]:
    sales_df[col] = sales_df[col].apply(convert_sales)

sales_melted = sales_df.melt(id_vars=["Video Games"], var_name="Year", value_name="Units Sold")

# Dropdown selector for year
year_options = sorted(sales_melted["Year"].unique())
selected_year = st.selectbox("Select Year", year_options)

# Filter data and plot
filtered_sales_df = sales_melted[sales_melted["Year"] == selected_year]
fig_sales = px.line(
    filtered_sales_df,
    x="Year",
    y="Units Sold",
    color="Video Games",
    title="Sales Over Time (2015 - 2024)",
    labels={"Year": "Year", "Units Sold": "Units Sold"},
    hover_name="Video Games",
    hover_data=["Units Sold"]
)
st.plotly_chart(fig_sales, use_container_width=True)

# Explanation text blocks
statement2 = [
    "This line chart shows whether consumers continue to purchase games as they age, and whether DLCs or subscriptions influence profits."
]
read2 = [
    "The x-axis indicates the year the video games were released.",
    "The y-axis visualizes total units sold until 2024.",
    "The data may be limited due to incomplete company disclosures.",
    "Each year introduces new games rather than showing only games from that year."
]
insight2 = ["", "", ""]

st.markdown("### Statement:")
for f in statement2:
    st.write(f"- {f}")
st.markdown("### How to read this chart:")
for f in read2:
    st.write(f"- {f}")
st.markdown("### Observations/Insights:")
for f in insight2:
    st.write(f"- {f}")

# ==================================
# SECTION 3: Ratings and Reviews
# ==================================
st.title("Ratings and Reviews")
st.caption("Positive vs negative reviews of the best video game of each year (2015 - 2024).")

# Load and clean rating data
rating_df = pd.read_csv("rating.csv")
st.write(rating_df.head())

rating_df["Rating"] = rating_df["Rating"].str.replace("%", "").astype(float)
rating_df["Reviews"] = rating_df["Reviews"].astype(int)
rating_df["Positive Rating"] = rating_df["Reviews"] * (rating_df["Rating"] / 100)
rating_df["Negative Rating"] = rating_df["Reviews"] - rating_df["Positive Rating"]

rating_melted = pd.melt(
    rating_df,
    id_vars=["Video Games"],
    value_vars=["Positive Rating", "Negative Rating"],
    var_name="Rating Type",
    value_name="Count"
)

# Dropdown selector for specific game
title_options = sorted(rating_melted["Video Games"].unique())
selected_title = st.selectbox("Select Game", title_options)

# Filter and plot donut chart
filtered_rating_df = rating_melted[rating_melted["Video Games"] == selected_title]
fig_rating = px.pie(
    filtered_rating_df,
    names="Rating Type",
    values="Count",
    title="Positive vs Negative Reviews",
    hole=0.4,
    color="Rating Type",
    color_discrete_map={"Positive Rating": "green", "Negative Rating": "red"},
    labels={"Rating Type": "Rating Type", "Count": "Number of Reviews"}
)
st.plotly_chart(fig_rating, use_container_width=True)

# Explanation text blocks
statement3 = [
    "The donut chart above explores if higher budgets increase player enjoyment, and whether GOTY winners correlate with better public reception."
]
read3 = [
    "Green represents the proportion of positive reviews.",
    "Red represents the proportion of negative reviews.",
    "The data is compiled from IMDb and reflects audience feedback across multiple platforms."
]
insight3 = ["", "", ""]

st.markdown("### Statement:")
for f in statement3:
    st.write(f"- {f}")
st.markdown("### How to read this chart:")
for f in read3:
    st.write(f"- {f}")
st.markdown("### Observations/Insights:")
for f in insight3:
    st.write(f"- {f}")

# ==================================
# SECTION 4: 🌍 NEW - Geoplot of Most Played Game by Country
# ==================================
# 💡 This is the NEW SECTION that I added for you.
# It creates a world map (choropleth) showing which game is most played per country.

st.title("Most Played Video Game by Country")
st.caption("A world map visualizing which game dominates in each country based on player count or popularity data.")

# Load data for the map (make sure you have this CSV)
geo_df = pd.read_csv("most_played_game_by_country.csv")

# Handle missing values for player counts
geo_df["Players (millions)"].fillna(0, inplace=True)

# Create the Plotly choropleth map
fig_geo = px.choropleth(
    geo_df,
    locations="Country",                 #
