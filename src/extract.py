import os

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine


load_dotenv()

server = os.getenv("DB_SERVER")
database = os.getenv("DB_NAME")
driver = os.getenv("DB_DRIVER")

connection_string = (
    f"mssql+pyodbc://@{server}/{database}"
    f"?driver={driver.replace(' ', '+')}"
    "&trusted_connection=yes"
    "&TrustServerCertificate=yes"
)


def get_engine():
    return create_engine(connection_string)


def extract_orders(engine):
    query = """
    SELECT
        SalesOrderID,
        OrderDate,
        CustomerID,
        TotalDue
    FROM Sales.SalesOrderHeader
    ORDER BY OrderDate DESC;
    """

    return pd.read_sql(query, engine)