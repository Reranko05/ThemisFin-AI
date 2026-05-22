import pandas as pd
from scipy import stats

from app.database.db import get_engine

engine = get_engine()


def fetch_transactions():

    query = """
        SELECT *
        FROM transactions;
    """

    return pd.read_sql(query, engine)


def detect_self_approvals(df):

    anomalies = df[
        df["initiator_id"] ==
        df["approver_id"]
    ].copy()

    anomalies["anomaly_type"] = (
        "Self Approval"
    )

    anomalies["severity_score"] = 90

    return anomalies


def detect_large_transactions(df):

    anomalies = df[
        df["amount"] > 500000
    ].copy()

    anomalies["anomaly_type"] = (
        "Large Transaction"
    )

    anomalies["severity_score"] = 75

    return anomalies


def detect_weekend_transactions(df):

    df["timestamp"] = pd.to_datetime(
        df["timestamp"]
    )

    anomalies = df[
        df["timestamp"].dt.dayofweek >= 5
    ].copy()

    anomalies["anomaly_type"] = (
        "Weekend Transaction"
    )

    anomalies["severity_score"] = 30

    return anomalies


def detect_statistical_outliers(df):

    df["z_score"] = stats.zscore(
        df["amount"]
    )

    anomalies = df[
        abs(df["z_score"]) > 3
    ].copy()

    anomalies["anomaly_type"] = (
        "Statistical Outlier"
    )

    anomalies["severity_score"] = 80

    return anomalies


def combine_anomalies(df):

    all_anomalies = pd.concat([
        detect_self_approvals(df),
        detect_large_transactions(df),
        detect_weekend_transactions(df),
        detect_statistical_outliers(df)
    ])

    all_anomalies = all_anomalies[
        [
            "transaction_id",
            "anomaly_type",
            "severity_score"
        ]
    ]

    all_anomalies.drop_duplicates(
        inplace=True
    )

    return all_anomalies


if __name__ == "__main__":

    transactions_df = fetch_transactions()

    anomalies_df = combine_anomalies(
        transactions_df
    )

    print(anomalies_df.head())

    anomalies_df.to_csv(
        "data/anomalies.csv",
        index=False
    )

    print("Anomaly detection complete.")