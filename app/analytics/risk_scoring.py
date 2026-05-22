import pandas as pd


def calculate_risk_score(row):

    score = 0

    if row["anomaly_type"] == "Self Approval":
        score += 90

    elif row["anomaly_type"] == "Large Transaction":
        score += 75

    elif row["anomaly_type"] == "Weekend Transaction":
        score += 30

    elif row["anomaly_type"] == "Statistical Outlier":
        score += 80

    return min(score, 100)


def apply_risk_scores():

    anomalies_df = pd.read_csv(
        "data/anomalies.csv"
    )

    anomalies_df["final_risk_score"] = (
        anomalies_df.apply(
            calculate_risk_score,
            axis=1
        )
    )

    anomalies_df.to_csv(
        "data/anomalies_scored.csv",
        index=False
    )

    print("Risk scoring complete.")


if __name__ == "__main__":

    apply_risk_scores()