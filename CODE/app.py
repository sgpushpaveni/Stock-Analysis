import streamlit as st
import altair as alt
import mysql.connector
import pandas as pd

import app_pages.app_views as appviews
import app_common.db_operations as db_ops
import app_common.df_operations as df_ops


merged_csv_file = "stocks.csv"
#stocks_df = db_ops.get_db_data()

stocks_df = df_ops.get_df_with_returns(merged_csv_file)


# Streamlit App Title
st.set_page_config(
    page_title="Data-Driven Stock Analysis", 
    layout="wide",
    initial_sidebar_state="expanded", #"collapsed","expanded",
    page_icon="random"
)

# Inject custom CSS to reduce padding and margins
custom_css = """
<style>
    .block-container {
        padding-top: 1rem;
        padding-bottom: 0rem;
        padding-left: 1rem;
        padding-right: 1rem;
    }
    <p>Phonepe EDA</p>
    .main .block-container {
        max-width: 100%;
    }
</style>
"""
logo = '''
![logo]|("logo.svg")
'''
st.markdown(custom_css, unsafe_allow_html=True)
#st.markdown(logo, unsafe_allow_html=True)
alt.themes.enable("dark")

# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Stock Analysis", 
                        ["Project Introduction", 
                         "Dataframe Dashboard", 
                         "Visualizations",
                         "PowerBI Data Prep"]
                         )

visuals_list = ["Volatility Analysis", 
                "Cumulative Return Over Time", 
                "Sector-wise Performance", 
                "Stock Price Correlation", 
                "Top 5 Gainers and Losers"]
cases_list = [
  'Stock Performance Ranking'
, 'Market Overview'
, 'Investment Insights'
, 'Decision Support Insights'
]


# -------------------------------- PAGE: Introduction --------------------------------
if page == "Project Introduction":
    st.title("Stock Analysis")
    st.subheader("An Streamlit App to show the data driven Stock Analysis")
    st.write("""
    **Problem Statement:**
    * Stock Performance Dashboard aims to provide a comprehensive visualization and analysis of the Nifty 50 stocks' performance over the past year. 
    * The project will analyze daily stock data, including open, close, high, low, and volume values. 
    * Covered:
    * Processing the data
    * generating key performance insights
    * Visualizing the top-performing stocks in terms of price changes, as well as average stock metrics. 
    * Offering interactive dashboards using Streamlit and Power BI
    * hHelping Investors, analysts, and enthusiasts make informed decisions based on the stock performance trends.
             
    **Business Use Cases:**
    * Stock Performance Ranking: Identify the top 10 best-performing stocks (green stocks) and the top 10 worst-performing stocks (red stocks) over the past year.
    * Market Overview: Provide an overall market summary with average stock performance and insights into the percentage of green vs red stocks.
    * Investment Insights: Help investors quickly identify which stocks showed consistent growth and which ones had significant declines.
    * Decision Support: Provide insights on average prices, volatility, and overall stock behavior, useful for both retail and institutional traders.
    
    **Technologies & Techniques Used:**
    * PowerBI 
    * MySQL - `Stocks`
    * Streamlit 
    * Python 
        * Pandas 
        * Data Cleaning 
        * Data Analysis 
        * Visualization 
        * Interactive Filters
    """)

# -------------------------------- PAGE: Top rated movies --------------------------------
elif page == "Visualizations":
    selected_visual = st.sidebar.selectbox('Select a Visualization', visuals_list)
    appviews.get_view(selected_visual, stocks_df)

# -------------------------------- PAGE: Interactive Filtering --------------------------------
elif page == "PowerBI Data Prep":
    st.write("PowerBI Data Prep")
    appviews.powerbi_data_prep(stocks_df)

# -------------------------------- PAGE: App Info --------------------------------
elif page == "Dataframe Dashboard":
    appviews.dashboard(stocks_df)

