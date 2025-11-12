
# pages/3_Dashboard.py
import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------------------
# Page Configuration
# ---------------------------
st.set_page_config(page_title="Video Game Dashboard", page_icon="📊", layout="wide")

st.title("🎮 Global Video Game Dashboard")
st.caption("Explore development costs, global sales, ratings, and most-played games around the world (2015–2024).")

# Remove chart fade animation for smoother reruns
st.markdown("""
    <style>
      [data-testid="stPlotlyChart"], .stPlotlyChart, .stElementContainer {
        transition: none !important;
        opacity: 1 !important;
      }
    </style>
""", unsafe_allow_html=True)


# =======================================
# SECTION 1: Development Costs (Bar Chart)
# =======================================
st.subheader("💸 Cost of Video Game Development")

df = pd.read_csv("data/top10.csv")

# Clean up missing data
median_cost = df["Cost of Development"].median()
df["Cost of Development"].fillna(median_cost, inplace=True)
df["Color"] = df["GOTY"].apply(lambda x: "gold" if x == 1 else "blue")

fig_cost = px.bar(
    df,
    x="Cost of Development",
    y="Video Games",
    color="Color",
    title="Development Costs of Popular Video Games",
    labels={"Video Games": "Video Games", "Cost of Development": "Development Cost ($)"},
    color_discrete_map={"gold": "gold", "blue": "blue"},
    hover_name="Video Games",
    hover_data=["Cost of Development"]
)

st.plotly_chart(fig_cost, use_container_width=True)
st.markdown("> **Insight:** Games with higher budgets don’t always guarantee GOTY status — quality still matters.")


# =======================================
# SECTION 2: Sales Over Time (Line Chart)
# =======================================
st.subheader("📈 Global Video Game Sales History")

sales_df = pd.read_csv("10salehistory.csv")

def convert_sales(value):
    if isinstance(value, str) and "m" in value:
        return float(value.replace("m", "")) * 1_000_000
    return None

for col in sales_df.columns[1:]:
    sales_df[col] = sales_df[col].apply(convert_sales)

sales_melted = sales_df.melt(id_vars=["Video Games"], var_name="Year", value_name="Units Sold")

# Year selector
year_options = sorted(sales_melted["Year"].unique())
selected_year = st.selectbox("Select Year", year_options, key="year_select")

filtered_sales_df = sales_melted[sales_melted["Year"] == selected_year]

fig_sales = px.line(
    filtered_sales_df,
    x="Year",
    y="Units Sold",
    color="Video Games",
    title="Sales Over Time (2015–2024)",
    labels={"Year": "Year", "Units Sold": "Units Sold"},
    hover_name="Video Games",
    hover_data=["Units Sold"]
)

st.plotly_chart(fig_sales, use_container_width=True)
st.markdown("> **Observation:** Some franchises sustain long-term sales growth through expansions and updates.")


# =======================================
# SECTION 3: Ratings and Reviews (Donut Chart)
# =======================================
st.subheader("⭐ Ratings and Reviews")

rating_df = pd.read_csv("rating.csv")

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

title_options = sorted(rating_melted["Video Games"].unique())
selected_title = st.selectbox("Select Game", title_options, key="rating_select")

filtered_rating_df = rating_melted[rating_melted["Video Games"] == selected_title]

fig_rating = px.pie(
    filtered_rating_df,
    names="Rating Type",
    values="Count",
    title=f"Positive vs Negative Reviews for {selected_title}",
    hole=0.4,
    color="Rating Type",
    color_discrete_map={"Positive Rating": "green", "Negative Rating": "red"},
)

st.plotly_chart(fig_rating, use_container_width=True)
st.markdown("> **Insight:** Even top-rated games receive negative feedback — balancing user expectations is key.")


# =======================================
# SECTION 4: Global Popularity (Geoplot)
# =======================================
st.subheader("🌍 Most Played Video Game by Country")

geo_df = pd.read_csv("most_played_game_by_country.csv")
geo_df["Players (millions)"].fillna(0, inplace=True)

fig_geo = px.choropleth(
    geo_df,
    locations="Country",
    locationmode="country names",
    color="Most Played Game",
    hover_name="Country",
    hover_data={"Players (millions)": True, "Most Played Game": True},
    title="Most Played Video Game Around the World",
    color_discrete_sequence=px.colors.qualitative.Set3,
)

fig_geo.update_layout(
    geo=dict(showframe=False, showcoastlines=True, projection_type="natural earth"),
    margin=dict(l=0, r=0, t=50, b=0),
)

st.plotly_chart(fig_geo, use_container_width=True)
st.markdown("> **Global Trend:** Player preferences vary by region — with distinct top games in Asia, Europe, and the Americas.")
