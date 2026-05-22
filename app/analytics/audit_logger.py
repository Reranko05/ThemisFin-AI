from sqlalchemy import text

from app.database.db import get_engine

engine = get_engine()


def log_action(
    anomaly_id,
    reviewer,
    action_taken
):

    query = text("""
        INSERT INTO audit_logs (
            anomaly_id,
            reviewer,
            action_taken
        )
        VALUES (
            :anomaly_id,
            :reviewer,
            :action_taken
        )
    """)

    with engine.connect() as conn:

        conn.execute(
            query,
            {
                "anomaly_id": anomaly_id,
                "reviewer": reviewer,
                "action_taken": action_taken
            }
        )

        conn.commit()

    print("Audit action logged.")