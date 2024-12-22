import mysql.connector

def execute_mysql_query(query, values):
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Ola@336425",
            database="telecom_db"
        )
        cursor = connection.cursor()
        cursor.executemany(query, values)
        connection.commit()
        print(f"{cursor.rowcount} records inserted successfully.")
        cursor.close()
        connection.close()
    except mysql.connector.Error as err:
        print(f"Error: {err}")
