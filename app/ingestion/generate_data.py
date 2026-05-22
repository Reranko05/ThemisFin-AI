import uuid
import random
from datetime import datetime, timedelta

import numpy as np
import pandas as pd
from faker import Faker

fake = Faker()

NUM_ENTITIES = 50
NUM_TRANSACTIONS = 100000

currencies = ["USD", "EUR", "GBP", "INR", "JPY"]

categories = [
    "Payroll",
    "Vendor Payment",
    "Intercompany Transfer",
    "Tax Settlement",
    "Investment",
    "Procurement"
]

approval_statuses = [
    "Approved",
    "Pending",
    "Rejected"
]


def generate_entities():
    entities = []

    for i in range(1, NUM_ENTITIES + 1):
        entities.append({
            "entity_id": i,
            "entity_name": f"{fake.company()} Holdings",
            "region": random.choice([
                "North America",
                "Europe",
                "Asia",
                "Middle East"
            ]),
            "risk_level": random.choice([
                "Low",
                "Medium",
                "High"
            ])
        })

    return pd.DataFrame(entities)


def random_timestamp():
    start_date = datetime.now() - timedelta(days=365)
    random_days = random.randint(0, 365)
    random_seconds = random.randint(0, 86400)

    return start_date + timedelta(
        days=random_days,
        seconds=random_seconds
    )


def generate_transactions():
    transactions = []

    dormant_entities = random.sample(
        range(1, NUM_ENTITIES + 1),
        5
    )

    for _ in range(NUM_TRANSACTIONS):

        timestamp = random_timestamp()

        source_entity = random.randint(1, NUM_ENTITIES)
        target_entity = random.randint(1, NUM_ENTITIES)

        while target_entity == source_entity:
            target_entity = random.randint(1, NUM_ENTITIES)

        initiator_id = random.randint(1000, 5000)
        approver_id = random.randint(1000, 5000)

        amount = round(
            np.random.lognormal(mean=10, sigma=1),
            2
        )

        currency = random.choice(currencies)

        category = random.choice(categories)

        approval_status = random.choice(
            approval_statuses
        )

        fx_flag = currency != "USD"

        # =====================================================
        # Inject anomalies intentionally
        # =====================================================

        # 1. Self approval anomaly
        if random.random() < 0.01:
            approver_id = initiator_id

        # 2. Large transaction anomaly
        if random.random() < 0.02:
            amount = round(
                random.uniform(500000, 5000000),
                2
            )

        # 3. Weekend anomaly
        if random.random() < 0.03:
            days_until_weekend = (
                5 - timestamp.weekday()
            ) % 7

            timestamp += timedelta(
                days=days_until_weekend
            )

        # 4. Dormant entity reactivation
        if source_entity in dormant_entities:
            if random.random() < 0.20:
                amount = round(
                    random.uniform(1000000, 10000000),
                    2
                )

        transaction = {
            "transaction_id": str(uuid.uuid4()),
            "timestamp": timestamp,
            "source_entity": source_entity,
            "target_entity": target_entity,
            "initiator_id": initiator_id,
            "approver_id": approver_id,
            "amount": amount,
            "currency": currency,
            "category": category,
            "approval_status": approval_status,
            "fx_flag": fx_flag,
            "risk_score": 0
        }

        transactions.append(transaction)

    return pd.DataFrame(transactions)


if __name__ == "__main__":

    print("Generating entities...")
    entities_df = generate_entities()

    print("Generating transactions...")
    transactions_df = generate_transactions()

    entities_df.to_csv(
        "data/entities.csv",
        index=False
    )

    transactions_df.to_csv(
        "data/transactions.csv",
        index=False
    )

    print("Data generation complete.")