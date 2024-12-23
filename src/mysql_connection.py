import mysql.connector
import pandas as pd

def execute_mysql_query(query, values=None):
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Ola@336425",
            database="telecom_db"
        )
        cursor = connection.cursor()

        if values:
            cursor.execute(query, values)
        else:
            cursor.execute(query)

        # Fetch all results immediately and return as DataFrame
        result = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]

        cursor.close()
        connection.close()

        return pd.DataFrame(result, columns=columns)

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return pd.DataFrame()
