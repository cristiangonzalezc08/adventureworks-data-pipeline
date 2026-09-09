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

engine = create_engine(connection_string)

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

df = extract_orders(engine)

df["OrderDate"] = pd.to_datetime(df["OrderDate"])
df["OrderYear"] = df["OrderDate"].dt.year

df["OrderValueCategory"] = pd.cut(
    df["TotalDue"],
    bins=[-float("inf"), 100, 500, float("inf")],
    labels=["Low", "Medium", "High"],
    right=False
)

output_path = "data/orders.csv"
df.to_csv(output_path, index=False)

print(f"Data extracted successfully and saved to {output_path}")

engine.dispose()