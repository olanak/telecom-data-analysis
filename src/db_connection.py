from sqlalchemy import create_engine
import pandas as pd

DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "telecom_db"
DB_USER = "postgres"
DB_PASS = "%40Kenne345"  # URL-encoded '@' to '%40'

def connect_db():
    engine = create_engine(f'postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}')
    return engine

# Fetch data from database
def fetch_data(query):
    engine = connect_db()
    with engine.connect() as connection:
        return pd.read_sql(query, connection)
