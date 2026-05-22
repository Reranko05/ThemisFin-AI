from apscheduler.schedulers.blocking import (
    BlockingScheduler
)

from app.analytics.anomaly_detection import (
    fetch_transactions,
    combine_anomalies,
    persist_anomalies
)

scheduler = BlockingScheduler()


def nightly_scan():

    print("Running nightly scan...")

    transactions_df = fetch_transactions()

    anomalies_df = combine_anomalies(
        transactions_df
    )

    persist_anomalies(
        anomalies_df
    )

    print("Nightly scan complete.")


scheduler.add_job(
    nightly_scan,
    "interval",
    hours=24
)

print("Scheduler started...")

scheduler.start()