from sqlalchemy import text

from app.database.db import get_engine

from app.analytics.audit_logger import (
    log_action
)

engine = get_engine()


def update_anomaly_status(
    anomaly_id,
    new_status,
    reviewer,
    notes
):

    query = text("""
        UPDATE anomaly_flags
        SET
            review_status = :review_status,
            assigned_reviewer = :reviewer,
            investigation_notes = :notes,
            updated_at = CURRENT_TIMESTAMP
        WHERE anomaly_id = :anomaly_id
    """)

    with engine.connect() as conn:

        conn.execute(
            query,
            {
                "review_status": new_status,
                "reviewer": reviewer,
                "notes": notes,
                "anomaly_id": anomaly_id
            }
        )

        conn.commit()

    log_action(
        anomaly_id,
        reviewer,
        f"Status changed to {new_status}"
    )

    print("Workflow updated.")