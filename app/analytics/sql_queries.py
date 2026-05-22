from sqlalchemy import text

from app.database.db import get_engine

engine = get_engine()


def top_risky_entities():

    query = text("""
        SELECT
            source_entity,
            COUNT(*) AS txn_count,
            AVG(amount) AS avg_amount
        FROM transactions
        GROUP BY source_entity
        ORDER BY avg_amount DESC
        LIMIT 10;
    """)

    with engine.connect() as conn:
        result = conn.execute(query)

        for row in result:
            print(row)


def self_approved_transactions():

    query = text("""
        SELECT *
        FROM transactions
        WHERE initiator_id = approver_id;
    """)

    with engine.connect() as conn:
        result = conn.execute(query)

        for row in result:
            print(row)


def weekend_transactions():

    query = text("""
        SELECT *
        FROM transactions
        WHERE EXTRACT(DOW FROM timestamp) IN (0,6);
    """)

    with engine.connect() as conn:
        result = conn.execute(query)

        for row in result:
            print(row)


def rolling_average_analysis():

    query = text("""
        SELECT
            transaction_id,
            source_entity,
            amount,
            AVG(amount) OVER (
                PARTITION BY source_entity
                ORDER BY timestamp
                ROWS BETWEEN 10 PRECEDING
                AND CURRENT ROW
            ) AS rolling_avg
        FROM transactions;
    """)

    with engine.connect() as conn:
        result = conn.execute(query)

        for row in result:
            print(row)


if __name__ == "__main__":

    print("\nTop Risky Entities")
    top_risky_entities()

    print("\nSelf Approved Transactions")
    self_approved_transactions()

    print("\nWeekend Transactions")
    weekend_transactions()

    print("\nRolling Average Analysis")
    rolling_average_analysis()