import pandas as pd

from app.database.db import get_engine

engine = get_engine()


def burst_transaction_detection():

    query = """
    WITH transaction_windows AS (

        SELECT
            source_entity,
            timestamp,
            COUNT(*) OVER (
                PARTITION BY source_entity
                ORDER BY timestamp
                RANGE BETWEEN INTERVAL '1 hour'
                PRECEDING AND CURRENT ROW
            ) AS txn_count

        FROM transactions
    )

    SELECT *
    FROM transaction_windows
    WHERE txn_count > 10;
    """

    return pd.read_sql(query, engine)


def dormant_entity_detection():

    query = """
    WITH entity_activity AS (

        SELECT
            source_entity,
            MAX(timestamp) AS last_activity

        FROM transactions

        GROUP BY source_entity
    )

    SELECT *
    FROM entity_activity

    WHERE last_activity <
    NOW() - INTERVAL '90 days';
    """

    return pd.read_sql(query, engine)


if __name__ == "__main__":

    burst_df = burst_transaction_detection()

    dormant_df = dormant_entity_detection()

    print("\nBurst Transactions\n")
    print(burst_df.head())

    print("\nDormant Entities\n")
    print(dormant_df.head())