from extract import get_engine, extract_orders
from transform import (
    transform_orders,
    create_customer_summary,
    filter_high_value_customers,
)
from load import load_dataframe
from validate import (
    validate_not_empty,
    validate_unique_orders,
    validate_required_columns,
    validate_order_values,
    validate_order_dates,
    validate_customer_ids,
)

def main():
    engine = get_engine()

    try:
        df = extract_orders(engine)

        validate_not_empty(df)
        validate_required_columns(df)
        validate_unique_orders(df)
        validate_order_values(df)
        validate_order_dates(df)
        validate_customer_ids(df, engine)

        df = transform_orders(df)

        customer_summary = create_customer_summary(df)

        high_value_customers = filter_high_value_customers(
            customer_summary
        )

        df.to_csv("data/orders.csv", index=False)
        high_value_customers.to_csv(
            "data/high_value_customers.csv",
            index=False
        )

        load_dataframe(df, "Orders", engine)
        load_dataframe(high_value_customers, "HighValueCustomers", engine)

        print("Data pipeline completed successfully.")

    finally:
        engine.dispose()


if __name__ == "__main__":
    main()