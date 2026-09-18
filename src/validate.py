import pandas as pd

#Post transformation validations Pre-transformation validation

def validate_not_empty(df):
    if df.empty:
        raise ValueError("Validation failed: DataFrame is empty.")

    return True #Not needed to return True, but it can be useful for testing purposes


def validate_unique_orders(df):
    if df["SalesOrderID"].duplicated().any(): #.any() Checks if atleast one value
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
         ~df["CustomerID"].isin((customer["CustomerID"])) #The symbol ~ is the not operator in pandas. It reverses True and Fales
    ]

    if not invalid_customer.empty: #checks if the DataFrame is not empty, if it is not empty, it means that there are CustomerIDs in the orders DataFrame that do not exist in the Sales.Customer table.
        raise ValueError(
            "Validation failed: Orders contain CustomerIDs "
            "that do not exist in Sales.Customer."
        )

#Post transformation validations

def validate_transformed_orders(df):
    if df["OrderYear"].isna().any():
        raise ValueError(
            "Validation failed: OrderYear contains NULL values."
        )

    if df["OrderValueCategory"].isna().any():
        raise ValueError(
            "Validation failed: OrderValueCategory contains NULL values."
        )