from db_connection import fetch_data
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import MinMaxScaler
from yellowbrick.cluster import KElbowVisualizer

# SQL Query to Aggregate User Experience Metrics
QUERY_EXPERIENCE = """
SELECT "MSISDN/Number",
       AVG("Avg RTT DL (ms)") AS avg_rtt_dl,
       AVG("Avg RTT UL (ms)") AS avg_rtt_ul,
       AVG("Avg Bearer TP DL (kbps)") AS avg_throughput_dl,
       AVG("Avg Bearer TP UL (kbps)") AS avg_throughput_ul,
       AVG("TCP DL Retrans. Vol (Bytes)") AS tcp_dl_retrans,
       AVG("TCP UL Retrans. Vol (Bytes)") AS tcp_ul_retrans,
       "Handset Type" AS handset_type
FROM xdr_data
GROUP BY "MSISDN/Number", "Handset Type"
"""

# Fetch Data
def load_experience_data():
    return fetch_data(QUERY_EXPERIENCE)

# Data Cleaning (Task 3.1)
def clean_experience_data(df):
    df.fillna(df.mean(numeric_only=True), inplace=True)
    df['handset_type'].fillna(df['handset_type'].mode()[0], inplace=True)
    print(f"\nData after cleaning: {len(df)} rows remaining")
    return df

# Compute Top/Bottom/Frequent Metrics (Task 3.2)
def compute_top_bottom_frequent(df, column, top_n=10):
    print(f"\nTop {top_n} {column} values:")
    print(df.nlargest(top_n, column))
    
    print(f"\nBottom {top_n} {column} values:")
    print(df.nsmallest(top_n, column))
    
    print(f"\nMost frequent {column} values:")
    print(df[column].value_counts().head(top_n))

# Distribution by Handset Type (Task 3.3)
def analyze_throughput_by_handset(df):
    distribution = df.groupby('handset_type')['avg_throughput_dl'].mean().sort_values()
    distribution.plot(kind='bar', figsize=(10, 6))
    plt.title('Average Throughput by Handset Type')
    plt.xlabel('Handset Type')
    plt.ylabel('Avg Throughput DL (kbps)')
    plt.show()
    print(distribution)

def analyze_tcp_by_handset(df):
    tcp_view = df.groupby('handset_type')['tcp_dl_retrans'].mean().sort_values()
    tcp_view.plot(kind='bar', figsize=(10, 6))
    plt.title('Average TCP Retransmission by Handset Type')
    plt.xlabel('Handset Type')
    plt.ylabel('Avg TCP DL Retransmission (Bytes)')
    plt.show()
    print(tcp_view)

# Normalize Data for Clustering (Task 3.4)
def normalize_data(df):
    scaler = MinMaxScaler()
    scaled_features = scaler.fit_transform(df[['avg_rtt_dl', 'avg_throughput_dl', 'tcp_dl_retrans']])
    return scaled_features

# Perform K-means Clustering (Task 3.4)
def perform_clustering(df, scaled_data, k=3):
    kmeans = KMeans(n_clusters=k, random_state=42)
    df['cluster'] = kmeans.fit_predict(scaled_data)
    return df

# Visualize Clusters
def visualize_clusters(df):
    plt.figure(figsize=(10, 6))
    plt.scatter(df['avg_throughput_dl'], df['avg_rtt_dl'], c=df['cluster'], cmap='viridis', alpha=0.6)
    plt.title('User Clustering Based on Experience Metrics')
    plt.xlabel('Avg Throughput DL (kbps)')
    plt.ylabel('Avg RTT DL (ms)')
    plt.colorbar(label='Cluster')
    plt.show()

if __name__ == "__main__":
    # Load Data
    experience_data = load_experience_data()

    # Clean Data (Task 3.1)
    experience_data_cleaned = clean_experience_data(experience_data)

    # Compute Top/Bottom/Frequent Values (Task 3.2)
    compute_top_bottom_frequent(experience_data_cleaned, 'tcp_dl_retrans')
    compute_top_bottom_frequent(experience_data_cleaned, 'avg_rtt_dl')
    compute_top_bottom_frequent(experience_data_cleaned, 'avg_throughput_dl')

    # Distribution Analysis (Task 3.3)
    analyze_throughput_by_handset(experience_data_cleaned)
    analyze_tcp_by_handset(experience_data_cleaned)

    # Normalize Data
    normalized_data = normalize_data(experience_data_cleaned)

    # Perform Clustering (Task 3.4)
    clustered_data = perform_clustering(experience_data_cleaned, normalized_data)

    # Visualize Clusters
    visualize_clusters(clustered_data)
