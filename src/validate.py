import pandas as pd

def validate_not_empty(df):
    if df.empty:
        raise ValueError("Validation failed: DataFrame is empty.")

    return True #Not needed to return True, but it can be useful for testing purposes


def validate_unique_orders(df):
    if df["SalesOrderID"].duplicated().any():
        raise ValueError(
            "Validation failed: Duplicate SalesOrderID values found."
        )

    return True #Not needed to return True, but it can be useful for testing purposes


def validate_required_columns(df):
    required_columns = [
        "SalesOrderID",
        "OrderDate",
        "CustomerID",
        "TotalDue",
    ]

    missing_columns = [
        column
        for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Validation failed: Missing columns: {missing_columns}"
        )

    return True #Not needed to return True, but it can be useful for testing purposes


def validate_order_values(df):
    if df["TotalDue"].isna().any():
        raise ValueError(
            "Validation failed: TotalDue contains NULL values."
        )

    if (df["TotalDue"] < 0).any():
        raise ValueError(
            "Validation failed: TotalDue contains negative values."
        )

    if df["CustomerID"].isna().any():
        raise ValueError(
            "Validation failed: CustomerID contains NULL values."
        )

    return True #Not needed to return True, but it can be useful for testing purposes

def validate_order_dates(df):
    if df["OrderDate"].isna().any():
        raise ValueError(
            "Validation failed: OrderDate contains NULL values."
        )

    if (df["OrderDate"] > pd.Timestamp.now()).any():
        raise ValueError(
            "Validation failed: OrderDate contains future dates."
        )

    return True #Not needed to return True, but it can be useful for testing purposes

def validate_customer_ids(df,engine):
    query = """
    SELECT CustomerID
    FROM Sales.Customer
    """

    customer = pd.read_sql(query,engine)

    invalid_customer = df[
         ~df["CustomerID"].isin((customer["CustomerID"]))
    ]

    if not invalid_customer.empty:
        raise ValueError(
            "Validation failed: Orders contain CustomerIDs "
            "that do not exist in Sales.Customer."
        )