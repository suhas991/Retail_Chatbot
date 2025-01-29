import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "Suhas@123")
DB_NAME = os.getenv("DB_NAME", "global_tshirts")

# 1. Database Connection Configuration
def test_db_connection():
    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        print("Database connection successful!")
        conn.close()
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        raise

# 7. Query Execution Function
def run_query(sql_query):
    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        cursor = conn.cursor()
        cursor.execute(sql_query)
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return result
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        raise
