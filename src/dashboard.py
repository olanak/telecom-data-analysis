import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from mysql_connection import execute_mysql_query
from db_connection import fetch_data

# Set Streamlit Page Config
st.set_page_config(
    page_title="Telecom Data Analysis Dashboard",
    page_icon="📊",
    layout="wide"
)

# Custom CSS for Professional Styling
st.markdown(
    """
    <style>
        .main {
            background-color: #4E5180;
        }
        .stApp {
            background-color: #1f2937;
        }
        h1, h2, h3, .css-18e3th9, .css-1aumxhk {
            color: #1f2937;  /* Dark Blue-Grey for headings */
            font-weight: bold;
        }
        p, .stMarkdown, .css-1d391kg p {
            color: #F5F5F5;  /* Medium Dark Grey for body text */
        }
        .sidebar .sidebar-content {
            background-color: #1f2937;  /* Dark Sidebar */
        }
        .sidebar .sidebar-content * {
            color: #f0f2f6;  /* Light Sidebar Text */
        }
        .css-1aumxhk {
            color: #1f2937 !important;
        }
        .stPlotlyChart, .stDataFrame, .stTable {
            background-color: #ffffff;
        }
        .css-1d391kg, .css-1xarl3l {
            border: 1px solid #d1d5db;  /* Light border for better definition */
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Load Data from MySQL or PostgreSQL
@st.cache_data
def load_data(query, source='mysql'):
    if source == 'mysql':
        return execute_mysql_query(query)
    else:
        return fetch_data(query)

# SQL Queries
QUERY_OVERVIEW = "SELECT \"Handset Type\", COUNT(*) AS count FROM xdr_data GROUP BY \"Handset Type\" ORDER BY count DESC LIMIT 10;"
QUERY_ENGAGEMENT = "SELECT \"MSISDN/Number\", COUNT(*) AS session_count, SUM(\"Dur. (ms)\") AS total_duration FROM xdr_data GROUP BY \"MSISDN/Number\";"
QUERY_EXPERIENCE = "SELECT \"MSISDN/Number\", AVG(\"Avg RTT DL (ms)\") AS avg_rtt_dl, AVG(\"Avg Bearer TP DL (kbps)\") AS avg_throughput_dl FROM xdr_data GROUP BY \"MSISDN/Number\";"
QUERY_SATISFACTION = "SELECT * FROM user_satisfaction;"

# Visualization Functions
def plot_overview(df):
    plt.figure(figsize=(12, 6))
    sns.barplot(x='Handset Type', y='count', data=df, palette='viridis')
    plt.title('Top 10 Handsets')
    plt.xticks(rotation=45)
    st.pyplot(plt)


def plot_engagement(df):
    plt.figure(figsize=(12, 6))
    sns.histplot(df['session_count'], bins=30, kde=True, color='#60a5fa')
    plt.title('User Engagement Distribution')
    plt.xlabel('Session Count')
    plt.ylabel('Frequency')
    st.pyplot(plt)


def plot_experience(df):
    plt.figure(figsize=(12, 6))
    sns.scatterplot(x='avg_throughput_dl', y='avg_rtt_dl', data=df, hue='avg_throughput_dl', palette='coolwarm', size='avg_throughput_dl')
    plt.title('User Experience Analysis')
    plt.xlabel('Avg Throughput DL (kbps)')
    plt.ylabel('Avg RTT DL (ms)')
    st.pyplot(plt)


def plot_satisfaction(df):
    plt.figure(figsize=(12, 6))
    sns.histplot(df['satisfaction_score'], bins=30, kde=True, color='#10b981')
    plt.title('User Satisfaction Distribution')
    plt.xlabel('Satisfaction Score')
    plt.ylabel('Frequency')
    st.pyplot(plt)

# Streamlit App Layout
st.title('📊 Telecom Data Analysis Dashboard')
st.markdown("### Gain insights into user engagement, experience, and satisfaction with interactive visualizations.")

# Sidebar Navigation
page = st.sidebar.selectbox(
    '📂 Select Analysis Page',
    ('User Overview Analysis', 'User Engagement Analysis', 'Experience Analysis', 'Satisfaction Analysis')
)

# Page Routing
if page == 'User Overview Analysis':
    st.header('📱 User Overview Analysis')
    data = load_data(QUERY_OVERVIEW, source='postgres')
    plot_overview(data)

elif page == 'User Engagement Analysis':
    st.header('👥 User Engagement Analysis')
    data = load_data(QUERY_ENGAGEMENT, source='postgres')
    plot_engagement(data)

elif page == 'Experience Analysis':
    st.header('⚙️ Experience Analysis')
    data = load_data(QUERY_EXPERIENCE, source='postgres')
    plot_experience(data)

elif page == 'Satisfaction Analysis':
    st.header('😊 Satisfaction Analysis')
    data = load_data(QUERY_SATISFACTION, source='mysql')
    plot_satisfaction(data)

# Footer
st.markdown("---")
st.markdown("**Dashboard created by Olana Kenea | © 2024**")
