from db_connection import fetch_data
import pandas as pd

# Queries for handset and manufacturer analysis
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

# Query for user aggregation
QUERY_AGGREGATE_USERS = """
SELECT "MSISDN/Number",
       COUNT(*) AS session_count,
       SUM("Total UL (Bytes)") AS total_upload,
       SUM("Total DL (Bytes)") AS total_download,
       SUM("Dur. (ms)") AS total_duration
FROM xdr_data
GROUP BY "MSISDN/Number"
ORDER BY session_count DESC;
"""

# Fetch data from DB for handsets
def load_handset_data():
    return fetch_data(QUERY_HANDSET)

# Fetch data from DB for manufacturers
def load_manufacturer_data():
    return fetch_data(QUERY_MANUFACTURER)

# Fetch top handsets per manufacturer
def load_top_handsets_per_manufacturer():
    return fetch_data(QUERY_TOP_HANDSETS)

# Fetch aggregated user data
def load_aggregated_user_data():
    return fetch_data(QUERY_AGGREGATE_USERS)

if __name__ == "__main__":
    # Handset Analysis
    print("Top 10 Handsets:\n", load_handset_data())
    print("\nTop 3 Manufacturers:\n", load_manufacturer_data())
    print("\nTop 5 Handsets per Manufacturer:\n", load_top_handsets_per_manufacturer())

    # User Data Aggregation
    user_data = load_aggregated_user_data()
    print("\nAggregated User Data:\n", user_data.head(10))  # Display top 10 results
