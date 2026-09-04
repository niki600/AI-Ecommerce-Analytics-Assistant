import os
import psycopg2
import pandas as pd
from dotenv import load_dotenv

load_dotenv()


def get_connection():
    """Create and return a PostgreSQL database connection."""
    
    connection = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        port=os.getenv("DB_PORT")
    )
    
    return connection


def execute_query(query):
    """Execute a SELECT query and return results as a DataFrame."""

    connection = get_connection()

    try:
        dataframe = pd.read_sql_query(query, connection)
        return dataframe

    finally:
        connection.close()