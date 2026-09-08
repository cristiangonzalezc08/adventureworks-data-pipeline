import pyodbc
import pandas as pd

connection_string = (
    "DRIVER={ODBC Driver 18 for SQL Server};"
    "SERVER=DESKTOP-3KP1DFI;"
    "DATABASE=AdventureWorks2025;"
    "Trusted_Connection=yes;"
    "TrustServerCertificate=yes;"
)

query = """
SELECT TOP 10 
    SalesOrderID,
    OrderDate,
    CustomerID,
    TotalDue
FROM Sales.SalesOrderHeader
ORDER BY OrderDate DESC;
"""

with pyodbc.connect(connection_string) as connection:
    df = pd.read_sql(query,connection)

print(df)

