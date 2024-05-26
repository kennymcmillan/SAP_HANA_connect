import logging
import sys
import matplotlib.pyplot as plt
import pandas as pd
import pyodbc
from hdbcli import dbapi
import os
import openai
import streamlit as st
# import seaborn as sns
import json
# import pygwalker as pyg
# import streamlit.components.v1 as components
# from datetime import date, timedelta
# from llama_index import VectorStoreIndex, ServiceContext, Document
# from llama_index.llms import OpenAI
# from llama_index import SimpleDirectoryReader
# from llama_index import VectorStoreIndex, ServiceContext, Document
# from llama_index.query_engine import PandasQueryEngine
# from IPython.display import Markdown, display
# import numpy as np
# from mitosheet.streamlit.v1 import spreadsheet

# def get_connection():
#     # Replace these variables with your actual connection details
#     host = "AACSAPPRODB01"
#     port = "30015"
#     user = "SPORTS_ALL"
#     password = "Aspire2023"
    
#     connection = dbapi.connect(
#         address=host,
#         port=port,
#         user=user,
#         password=password
#     )
    
#     return connection

def get_connection():
    # Retrieve credentials from Streamlit secrets
    host = st.secrets["sap_hana"]["host"]
    port = st.secrets["sap_hana"]["port"]
    user = st.secrets["sap_hana"]["user"]
    password = st.secrets["sap_hana"]["password"]
    
    connection = dbapi.connect(
        address=host,
        port=port,
        user=user,
        password=password
    )
    return connection

def get_view_headers(connection, full_view_name):
    cursor = connection.cursor()
    # Extract schema and view names from the full view name
    schema_name = full_view_name.split('"."')[0].replace('"', '')
    view_name = full_view_name.split('"."')[-1].replace('"', '')
    # Execute the SQL query to retrieve column names for the view
    query = f"""
    SELECT COLUMN_NAME
    FROM SYS.VIEW_COLUMNS
    WHERE SCHEMA_NAME = '{schema_name}' AND VIEW_NAME = '{view_name}'
    ORDER BY POSITION
    """
    cursor.execute(query)
    
    columns = [row[0] for row in cursor.fetchall()]
    cursor.close()
    
    return columns

def list_schemas(connection):
    cursor = connection.cursor()
    # Execute the SQL query to list all schemas
    cursor.execute("SELECT SCHEMA_NAME FROM SCHEMAS")
    
    schemas = cursor.fetchall()
    for schema in schemas:
        print(schema[0])
    
    cursor.close()

def fetch_first_100_rows(connection, full_view_name):
    cursor = connection.cursor()
    # Execute the SQL query to fetch the first 100 rows from the specified view
    query = f"SELECT * FROM {full_view_name} LIMIT 100"
    cursor.execute(query)
    
    rows = cursor.fetchall()
    cursor.close()
    
    return rows

# Establish the connection
connection = get_connection()
list_schemas(connection)

full_view_name = '"_SYS_BIC"."ASPIRE_SPORTS.POWER_BI_MODELS.SPORTS_ALL/SP_CV_POWER_BI_SPORTS_ALL"'
headers = get_view_headers(connection, full_view_name)

rows = fetch_first_100_rows(connection, full_view_name)
df = pd.DataFrame(rows, columns=headers)

print(df.head(100))


cursor = connection.cursor()
    # Execute the SQL query to fetch all rows where formname = "Aerobic Stage Test"
query = f"SELECT * FROM {full_view_name} WHERE formname = 'Aerobic Stage Test'"
cursor.execute(query)
    
rows = cursor.fetchall()
cursor.close()

df = pd.DataFrame(rows, columns=headers)