import streamlit as st
import pandas as pd
import requests
import plotly.express as px
import time

st.set_page_config(page_title="Video Games ", page_icon="📡", layout="wide")
# Disable fade/transition so charts don't blink between reruns
st.markdown("""
    <style>
      [data-testid="stPlotlyChart"], .stPlotlyChart, .stElementContainer {
        transition: none !important;
        opacity: 1 !important;
      }
    </style>
""", unsafe_allow_html=True)

st.title("Cost($) of Video Game Development")
st.caption("The development cost of well-received video games in the past decade (2015 - 2024).")

df = pd.read_csv("data/top10.csv")

median_cost = df["Cost of Development"].median()
df["Cost of Development"].fillna(median_cost, inplace = True)

df["Color"] = df["GOTY"].apply(lambda x: "gold" if x == 1 else "blue")

st.write(df.head())

fig_cost = px.bar(df, x = "Cost of Development", y = "Video Games", color = "Color",
             title = "Development Costs of Video Games",
             labels = {"Video Games": "Video Games", "Cost of Development": "Development Cost($)"},
             color_discrete_map = {"gold": "gold", "blue": "blue"},
             hover_name = "Video Games", hover_data = ["Cost of Development"])

st.plotly_chart(fig_cost, use_container_width=True)

statement1 = [
    "The bar chart above helps answering our questions of whether or not a higher budget affects quality of the video game. It also happens to answer if those games have won GOTY(Game of the Year awards)."
]

read1 = [
    "The x-axis of this chart indicates the cost of development of the listed video games.",
    "The y-axis are the titles of the listed video games.",
    "The color gold indicates if the game has won GOTY or blue if it has not."
]

insight1 = [
    "",
    "",
    ""
]

st.markdown("### Statement:")
for i, f in enumerate(statement1, start=1):
    st.write(f"- {f}")

st.markdown("### How to read this chart:")
for i, f in enumerate(read1, start=1):
    st.write(f"- {f}")

st.markdown("### Observations/Insights:")
for i, f in enumerate(insight1, start=1):
    st.write(f"- {f}")

st.title("Video Game Sale History")
st.caption("The amount of units each video game has sold since their release year.")

sales_df = pd.read_csv("10salehistory.csv")

def convert_sales(value):
    if isinstance(value, str) and "m" in value:
        return float(value.replace("m", "")) * 1_000_000
    return None

for col in sales_df.columns[1:]:
    sales_df[col] = sales_df[col].apply(convert_sales)

sales_melted = sales_df.melt(id_vars = ["Video Games"], var_name = "Year", value_name = "Units Sold")

year_options = sorted(sales_melted["Year"].unique())
selected_year = st.selectbox("Select Year", year_options)

filtered_sales_df = sales_melted[sales_melted["Year"] == selected_year]

fig_sales = px.line(filtered_sales_df, x = "Year", y = "Units Sold", color = "Video Games",
                    title = "Sales Over Time (2015 - 2024)",
                    labels = {"Year": "Year", "Units Sold": "Units Sold"},
                    hover_name = "Video Games", hover_data =["Units Sold"])

st.plotly_chart(fig_sales, use_container_width = True)


statement2 = [
    "The line chart above helps answering our questions of whether or not if consumers continue to purchase the game despite its age. And helps answer if DLC and subscriptions affects profits."
]

read2 = [
    "The x-axis of this chart indicates the year the video games are released.",
    "The y-axis helps visualize the amount of copies a video game has sold unil 2024.",
    "The chart is not completely accurate due to limited information from their company.",
    "The chart adds an additional video game each year rather than games released in the same year."
]

insight2 = [
    "",
    "",
    ""
]

st.markdown("### Statement:")
for i, f in enumerate(statement2, start=1):
    st.write(f"- {f}")

st.markdown("### How to read this chart:")
for i, f in enumerate(read2, start=1):
    st.write(f"- {f}")

st.markdown("### Observations/Insights:")
for i, f in enumerate(insight2, start=1):
    st.write(f"- {f}")


st.title("Ratings and Reviews")
st.caption("The positive vs negative reviews best video game of each year (2015 - 2024).")

rating_df = pd.read_csv("rating.csv")

st.write(rating_df.head())

rating_df["Rating"] = rating_df["Rating"].str.replace("%", "").astype(float)
rating_df["Reviews"] = rating_df["Reviews"].astype(int)

rating_df["Positive Rating"] = rating_df["Reviews"] * (rating_df["Rating"] / 100)
rating_df["Negative Rating"] = rating_df["Reviews"] - rating_df["Positive Rating"]

rating_melted = pd.melt(rating_df, id_vars = ["Video Games"], value_vars = ["Positive Rating", "Negative Rating"],
                        var_name = "Rating Type", value_name = "Count")

title_options = sorted(rating_melted["Video Games"].unique())
selected_title = st.selectbox("Select Game", title_options)

filtered_rating_df = rating_melted[rating_melted["Video Games"] == selected_title]

fig_rating = px.pie(filtered_rating_df, names = "Rating Type", values = "Count",
                    title = "Positive vs Negative Reviews",
                    hole = 0.4, color = "Rating Type",
                    color_discrete_map = {"Positive Rating": "green", "Negative Rating": "red"},
                    labels = {"Rating Type": "Rating Type", "Count": "Number of Reviews"})

st.plotly_chart(fig_rating, use_container_width = True)

statement3 = [
    "The donut chart above helps answering our questions of if a higher budget increases player enjoyment. It also answers if the video games have won GOTY due to its quality and how downloadable content (DLC) may influence profitability."
]

read3 = [
    "The infographic donut chart above shows how well-received the video games are by the public.",
    "The color green indicates the proportion of positive reviews/ratings since each games' release.",
    "The color red indicates the proportion of negative reviews/ratings since each games' release.",
    "The data is compiled from IMDb and reflects audience ratings from across multiple platforms."
]

insight3 = [
    "",
    "",
    ""
]

st.markdown("### Statement:")
for i, f in enumerate(statement3, start=1):
    st.write(f"- {f}")

st.markdown("### How to read this chart:")
for i, f in enumerate(read3, start=1):
    st.write(f"- {f}")

st.markdown("### Observations/Insights:")
for i, f in enumerate(insight3, start=1):
    st.write(f"- {f}")
