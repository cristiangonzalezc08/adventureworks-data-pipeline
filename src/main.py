from extract import get_engine, extract_orders
from transform import (
    transform_orders,
    create_customer_summary,
    filter_high_value_customers,
)


def main():
    engine = get_engine()

    try:
        df = extract_orders(engine)

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

        print("Data pipeline completed successfully.")

    finally:
        engine.dispose()


if __name__ == "__main__":
    main()