import pandas as pd
from sqlalchemy import text

from app.database.db import get_engine
from app.ai.report_generator import (
    generate_audit_finding
)

engine = get_engine()


def fetch_anomalies():

    query = """
        SELECT
            t.transaction_id,
            t.amount,
            af.anomaly_type,
            af.severity_score
        FROM anomaly_flags af
        JOIN transactions t
        ON af.transaction_id = t.transaction_id
        LIMIT 20;
    """

    return pd.read_sql(query, engine)


def store_ai_reports():

    anomalies_df = fetch_anomalies()

    with engine.connect() as conn:

        for _, row in anomalies_df.iterrows():

            anomaly_data = {
                "transaction_id": row["transaction_id"],
                "anomaly_type": row["anomaly_type"],
                "amount": row["amount"]
            }

            print(
                f"Generating report for "
                f"{row['transaction_id']}"
            )

            generated_report = (
                generate_audit_finding(
                    anomaly_data
                )
            )

            insert_query = text("""
                INSERT INTO ai_audit_reports (
                    transaction_id,
                    anomaly_type,
                    generated_report
                )
                VALUES (
                    :transaction_id,
                    :anomaly_type,
                    :generated_report
                )
            """)

            conn.execute(
                insert_query,
                {
                    "transaction_id":
                        str(row["transaction_id"]),
                    "anomaly_type":
                        row["anomaly_type"],
                    "generated_report":
                        generated_report
                }
            )

        conn.commit()

    print("AI audit reports stored.")


if __name__ == "__main__":

    store_ai_reports()