from sqlalchemy import text

from app.database.db import get_engine

engine = get_engine()


def refresh_views():

    with engine.connect() as conn:

        conn.execute(
            text("""
                REFRESH MATERIALIZED VIEW
                entity_risk_summary;
            """)
        )

        conn.commit()

    print(
        "Materialized views refreshed."
    )


if __name__ == "__main__":

    refresh_views()