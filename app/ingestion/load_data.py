import pandas as pd
from sqlalchemy import text

from app.database.db import get_engine

engine = get_engine()


def load_entities():

    entities_df = pd.read_csv(
        "data/entities.csv"
    )

    entities_df.to_sql(
        "entities",
        engine,
        if_exists="append",
        index=False
    )

    print("Entities loaded successfully.")


def load_transactions():

    transactions_df = pd.read_csv(
        "data/transactions.csv"
    )

    transactions_df.to_sql(
        "transactions",
        engine,
        if_exists="append",
        index=False,
        chunksize=5000,
        method="multi"
    )

    print("Transactions loaded successfully.")


def truncate_tables():

    with engine.connect() as conn:

        conn.execute(
            text("""
                TRUNCATE TABLE
                anomaly_flags,
                audit_logs,
                transactions,
                entities
                RESTART IDENTITY CASCADE;
            """)
        )

        conn.commit()

    print("Tables truncated.")


if __name__ == "__main__":

    truncate_tables()

    load_entities()

    load_transactions()

    print("Database ingestion complete.")