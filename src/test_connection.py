import pyodbc

connection_string = (
    "DRIVER={ODBC Driver 18 for SQL Server};"
    "SERVER=DESKTOP-3KP1DFI;"
    "DATABASE=AdventureWorks2025;"
    "Trusted_Connection=yes;"
    "TrustServerCertificate=yes;"
)

with pyodbc.connect(connection_string) as connection:
    print("Connection successful!")