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

query = """
SELECT TOP 10
    SalesOrderID,
    OrderDate,
    CustomerID,
    TotalDue
FROM Sales.SalesOrderHeader
ORDER BY OrderDate DESC;
"""

df = pd.read_sql(query, engine)

output_path = "data/orders.csv"
df.to_csv(output_path, index=False)

print(f"Data extracted successfully and saved to {output_path}")

engine.dispose()