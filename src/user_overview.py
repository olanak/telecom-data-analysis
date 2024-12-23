import sys
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

sys.path.append("/home/olana/Desktop/KAIM 3/Week 2/telecom-data-analysis/scripts")

from visual_exports import export_visualizations
# Add the scripts directory to the Python path for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../scripts')))

from db_connection import fetch_data


# SQL Queries for Analysis
QUERY_HANDSET = """
SELECT "Handset Type", COUNT(*) AS count
FROM xdr_data
GROUP BY "Handset Type"
ORDER BY count DESC
LIMIT 10;
"""

QUERY_MANUFACTURER = """
SELECT "Handset Manufacturer", COUNT(*) AS count
FROM xdr_data
GROUP BY "Handset Manufacturer"
ORDER BY count DESC
LIMIT 3;
"""

QUERY_TOP_HANDSETS = """
SELECT "Handset Manufacturer", "Handset Type", COUNT(*) AS count
FROM xdr_data
GROUP BY "Handset Manufacturer", "Handset Type"
ORDER BY count DESC;
"""

QUERY_AGGREGATE_USERS = """
SELECT "MSISDN/Number",
       COUNT(*) AS session_count,
       SUM("Total UL (Bytes)") AS total_upload,
       SUM("Total DL (Bytes)") AS total_download,
       SUM("Dur. (ms)") AS total_duration,
       SUM("Social Media DL (Bytes)") AS "Social Media DL (Bytes)",
       SUM("Social Media UL (Bytes)" ) AS "Social Media UL (Bytes)",
       SUM("Google DL (Bytes)") AS "Google DL (Bytes)",
       SUM("Google UL (Bytes)") AS "Google UL (Bytes)",
       SUM("Email DL (Bytes)") AS "Email DL (Bytes)",
       SUM("Email UL (Bytes)") AS "Email UL (Bytes)",
       SUM("Youtube DL (Bytes)") AS "Youtube DL (Bytes)",
       SUM("Youtube UL (Bytes)") AS "Youtube UL (Bytes)",
       SUM("Netflix DL (Bytes)") AS "Netflix DL (Bytes)",
       SUM("Netflix UL (Bytes)") AS "Netflix UL (Bytes)",
       SUM("Gaming DL (Bytes)") AS "Gaming DL (Bytes)",
       SUM("Gaming UL (Bytes)") AS "Gaming UL (Bytes)"
FROM xdr_data
GROUP BY "MSISDN/Number"
ORDER BY session_count DESC;
"""

# --- Data Loading Functions ---
def load_handset_data():
    return fetch_data(QUERY_HANDSET)

def load_manufacturer_data():
    return fetch_data(QUERY_MANUFACTURER)

def load_top_handsets_per_manufacturer():
    return fetch_data(QUERY_TOP_HANDSETS)

def load_aggregated_user_data():
    return fetch_data(QUERY_AGGREGATE_USERS)


# --- Data Cleaning ---
def clean_aggregated_data(df):
    df_cleaned = df.dropna(subset=["MSISDN/Number"]).copy()
    print(f"\nData after cleaning (NaN removed): {len(df_cleaned)} rows remaining")
    return df_cleaned


# --- EDA and User Segmentation ---
def perform_eda(df):
    print("\nDescriptive Statistics (Aggregated User Data):")
    print(df.describe())
    print("\nMissing Values:")
    print(df.isna().sum())

    # Outlier detection
    Q1 = df['session_count'].quantile(0.25)
    Q3 = df['session_count'].quantile(0.75)
    IQR = Q3 - Q1
    outliers = df[(df['session_count'] < (Q1 - 1.5 * IQR)) | (df['session_count'] > (Q3 + 1.5 * IQR))]
    print(f"\nNumber of Outliers (Session Count): {len(outliers)}")

    # Total Data Volume and Decile Segmentation
    df['total_data'] = df['total_upload'] + df['total_download']
    df['decile_class'] = pd.qcut(df['total_duration'], 10, labels=False)
    decile_agg = df.groupby('decile_class')['total_data'].sum().reset_index()

    print("\nTotal Data Volume per Decile Class:")
    print(decile_agg)

    return df, decile_agg


# --- Correlation Analysis ---
def correlation_analysis(df):
    corr_columns = [
        "Social Media DL (Bytes)", "Social Media UL (Bytes)",
        "Google DL (Bytes)", "Google UL (Bytes)",
        "Email DL (Bytes)", "Email UL (Bytes)",
        "Youtube DL (Bytes)", "Youtube UL (Bytes)",
        "Netflix DL (Bytes)", "Netflix UL (Bytes)",
        "Gaming DL (Bytes)", "Gaming UL (Bytes)"
    ]

    filtered_df = df[corr_columns].dropna()

    if len(filtered_df) > 1:
        correlation_matrix = filtered_df.corr()
        print("\nCorrelation Matrix Computed Successfully")
    else:
        correlation_matrix = pd.DataFrame()
        print("Warning: Not enough data for correlation matrix.")

    return correlation_matrix


# --- Principal Component Analysis (PCA) ---
def perform_pca(df):
    pca_columns = [
        "Social Media DL (Bytes)", "Social Media UL (Bytes)",
        "Google DL (Bytes)", "Google UL (Bytes)",
        "Email DL (Bytes)", "Email UL (Bytes)",
        "Youtube DL (Bytes)", "Youtube UL (Bytes)",
        "Netflix DL (Bytes)", "Netflix UL (Bytes)",
        "Gaming DL (Bytes)", "Gaming UL (Bytes)"
    ]

    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(df[pca_columns].fillna(0))

    pca = PCA(n_components=2)
    pca_result = pca.fit_transform(scaled_data)

    df['PCA1'] = pca_result[:, 0]
    df['PCA2'] = pca_result[:, 1]

    print("\nExplained Variance Ratio by PCA Components:")
    print(pca.explained_variance_ratio_)

    return df


# --- Main Execution ---
if __name__ == "__main__":
    top_handsets = load_handset_data()
    top_manufacturers = load_manufacturer_data()
    user_data = load_aggregated_user_data()

    # Clean the data
    user_data_cleaned = clean_aggregated_data(user_data)

    # Perform EDA and segmentation
    segmented_data, decile_aggregation = perform_eda(user_data_cleaned)

    # Correlation Analysis
    correlation_matrix = correlation_analysis(user_data_cleaned)

    # PCA for Dimensionality Reduction
    segmented_data = perform_pca(user_data_cleaned)

    # Export Visualizations
    export_visualizations(
        top_handsets,
        top_manufacturers,
        user_data_cleaned,
        decile_aggregation,
        correlation_matrix,
        segmented_data
    )
