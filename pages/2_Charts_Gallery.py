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

sales_df = pd.read_csv("10salehistory.csv")

def convert_sales(value):
    if isinstance(value, str) and "m" in value:
        return float(value.replace("m", "")) * 1_000_000
    return None

for col in sales_df.columns[1:]:
    sales_df[col] = sales_df[col].apply(convert_sales)

sales_df_melted = salesdf.melt(id_vars = ["Video Games"], var_name = "Year", value_names = "Units Sold")

year_options = sorted(sales_df_melted["Year"].unique())
selected_year = st.selectbox("Select Year", year_options)

filtered_sales_df = sales_df_melted[sales_df_melted["Year"] == selected_year]

fis_sales = px.line(sales_df_melted, x = "Year", y = "Units Sold", color = "Video Games",
                    title = "Sales Over Time (2015 - 2024)",
                    labels = {"Year": "Year", "Units Sold": "Units Sold"},
                    hover_name = "Video Games", hover_data =["Units Sold"])

st.plotly_chart(fig_sales, use_container_width = True)
