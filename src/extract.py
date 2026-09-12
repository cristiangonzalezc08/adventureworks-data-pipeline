import os

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine


load_dotenv()


server = os.getenv("DB_SERVER")
database = os.getenv("DB_NAME")
driver = os.getenv("DB_DRIVER")


from transform import (
    transform_orders,
    create_customer_summary,
    filter_high_value_customers,
)

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

df = transform_orders(df)

customer_summary = create_customer_summary(df)

high_value_customers = filter_high_value_customers(customer_summary)


output_path = "data/orders.csv"
df.to_csv(output_path, index=False)

print(f"Data extracted successfully and saved to {output_path}")

customer_output_path = "data/high_value_customers.csv"
high_value_customers.to_csv(customer_output_path, index=False)

print(
    f"High-value customer data saved to {customer_output_path}"
)


engine.dispose()


