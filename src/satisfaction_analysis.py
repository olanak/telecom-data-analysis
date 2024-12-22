from db_connection import fetch_data
from mysql_connection import execute_mysql_query
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import euclidean_distances
from sklearn.linear_model import LinearRegression

# Aggregate User Engagement and Experience Metrics
QUERY_SATISFACTION = """
SELECT e."MSISDN/Number",
       e.session_count,
       e.total_duration,
       e.total_download,
       e.total_upload,
       x.avg_rtt_dl,
       x.avg_throughput_dl,
       x.tcp_dl_retrans
FROM (
    SELECT "MSISDN/Number",
           COUNT(*) AS session_count,
           SUM("Dur. (ms)") AS total_duration,
           SUM("Total DL (Bytes)") AS total_download,
           SUM("Total UL (Bytes)") AS total_upload
    FROM xdr_data
    GROUP BY "MSISDN/Number"
) e
JOIN (
    SELECT "MSISDN/Number",
           AVG("Avg RTT DL (ms)") AS avg_rtt_dl,
           AVG("Avg Bearer TP DL (kbps)") AS avg_throughput_dl,
           AVG("TCP DL Retrans. Vol (Bytes)") AS tcp_dl_retrans
    FROM xdr_data
    GROUP BY "MSISDN/Number"
) x ON e."MSISDN/Number" = x."MSISDN/Number";
"""

# Fetch Data
def load_satisfaction_data():
    return fetch_data(QUERY_SATISFACTION)

# Data Cleaning
def clean_satisfaction_data(df):
    df.fillna(df.mean(numeric_only=True), inplace=True)
    print(f"\nData after cleaning: {len(df)} rows remaining")
    return df

# Normalize Data
def normalize_data(df):
    scaler = MinMaxScaler()
    scaled_features = scaler.fit_transform(df[['session_count', 'total_duration', 'total_download', 'total_upload', 'avg_rtt_dl', 'avg_throughput_dl', 'tcp_dl_retrans']])
    return scaled_features

# Compute Engagement and Experience Scores (Task 4.1)
def compute_scores(df, scaled_data):
    kmeans_engagement = KMeans(n_clusters=3, random_state=42).fit(scaled_data)
    kmeans_experience = KMeans(n_clusters=3, random_state=42).fit(scaled_data)
    
    engagement_distances = euclidean_distances(scaled_data, kmeans_engagement.cluster_centers_)
    experience_distances = euclidean_distances(scaled_data, kmeans_experience.cluster_centers_)
    
    df['engagement_score'] = engagement_distances.min(axis=1)
    df['experience_score'] = experience_distances.min(axis=1)
    return df

# Compute Satisfaction Score (Task 4.2)
def compute_satisfaction_score(df):
    df['satisfaction_score'] = (df['engagement_score'] + df['experience_score']) / 2
    print("Top 10 Satisfied Customers:")
    print(df.nlargest(10, 'satisfaction_score'))
    return df

# Train Regression Model (Task 4.3)
def train_regression_model(df):
    X = df[['session_count', 'total_duration', 'total_download', 'total_upload', 'avg_rtt_dl', 'avg_throughput_dl', 'tcp_dl_retrans']]
    y = df['satisfaction_score']
    model = LinearRegression()
    model.fit(X, y)
    print("Regression Model Coefficients:", model.coef_)
    return model

# Cluster Satisfaction and Experience Scores (Task 4.4)
def cluster_satisfaction(df):
    kmeans = KMeans(n_clusters=2, random_state=42)
    df['satisfaction_cluster'] = kmeans.fit_predict(df[['satisfaction_score', 'experience_score']])
    return df

# Aggregate Satisfaction Per Cluster (Task 4.5)
def aggregate_scores_per_cluster(df):
    aggregated = df.groupby('satisfaction_cluster').agg({'satisfaction_score': 'mean', 'experience_score': 'mean'}).reset_index()
    print("\nAverage Satisfaction and Experience Score Per Cluster:")
    print(aggregated)
    return aggregated

# Export Results to MySQL (Task 4.6)
def export_to_mysql(df):
    export_query = """
    INSERT INTO user_satisfaction (MSISDN, engagement_score, experience_score, satisfaction_score)
    VALUES (%s, %s, %s, %s)
    """
    values = df[['MSISDN/Number', 'engagement_score', 'experience_score', 'satisfaction_score']].values.tolist()
    execute_mysql_query(export_query, values)
    print("Data successfully exported to MySQL database.")

if __name__ == "__main__":
    # Load Data
    satisfaction_data = load_satisfaction_data()

    # Clean Data
    satisfaction_data_cleaned = clean_satisfaction_data(satisfaction_data)

    # Normalize Data
    normalized_data = normalize_data(satisfaction_data_cleaned)

    # Compute Scores
    scored_data = compute_scores(satisfaction_data_cleaned, normalized_data)
    scored_data = compute_satisfaction_score(scored_data)

    # Train Regression Model
    regression_model = train_regression_model(scored_data)

    # Cluster Satisfaction and Experience
    clustered_data = cluster_satisfaction(scored_data)

    # Aggregate Per Cluster
    aggregated_scores = aggregate_scores_per_cluster(clustered_data)

    # Export to MySQL
    export_to_mysql(clustered_data)
