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

df["Color"] = df{"GOTY"].apply(lambda x: "gold" if x == 1 else "blue")

st.write(df.head())

fig = px.bar(df, x = "Development Cost($)", y = "Game Title", color = "Color",
             title = "Development Costs of Video Games",
             labels = {"Video Games": "Video Games", "Cost of Development": "Development Cost($)"},
             color_map = {"gold": "gold", "blue": "blue"])

st.plotly_chart(fig, use_container_width=True)
