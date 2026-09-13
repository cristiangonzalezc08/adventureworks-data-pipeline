import pandas as pd


def load_dataframe(df, table_name, engine):
    df.to_sql(
        table_name,
        engine,
        schema="dbo",
        if_exists="replace",
        index=False
    )

    print(f"Loaded {len(df)} rows into dbo.{table_name}")