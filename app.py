# app.py
import streamlit as st

# Page setup
st.set_page_config(
    page_title="Global Video Games Dashboard",
    page_icon="🎮",
    layout="wide"
)

# App title
st.title("🎮 Global Video Game Analytics Dashboard")
st.markdown("Welcome to the multi-page Streamlit app exploring the world of video game data.")

# Intro text
st.markdown("""
This dashboard is divided into several sections:
- **Bio:** Learn about the project and its goals.  
- **Charts Gallery:** Visual insights on game costs, sales, and ratings.  
- **Dashboard:** Interactive analysis including the global geoplot.  
- **Future Work:** Possible extensions and improvements.
""")

st.info("👈 Use the sidebar on the left to navigate between pages.")
