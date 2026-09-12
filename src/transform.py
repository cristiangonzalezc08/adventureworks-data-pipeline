import pandas as pd


def transform_orders(df):
    df["OrderDate"] = pd.to_datetime(df["OrderDate"])

    df["OrderYear"] = df["OrderDate"].dt.year

    df["OrderValueCategory"] = pd.cut(
        df["TotalDue"],
        bins=[-float("inf"), 100, 500, float("inf")],
        labels=["Low", "Medium", "High"],
        right=False
    )

    return df


def create_customer_summary(df):
    customer_summary = (
        df.groupby("CustomerID")
        .agg(
            NumberOfOrders=("SalesOrderID", "count"),
            TotalSpent=("TotalDue", "sum"),
            AverageOrderValue=("TotalDue", "mean")
        )
        .reset_index()
    )

    return customer_summary


def filter_high_value_customers(customer_summary):
    return customer_summary[
        (customer_summary["NumberOfOrders"] > 5)
        & (customer_summary["TotalSpent"] > 10000)
    ]