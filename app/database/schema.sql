CREATE TABLE entities (
    entity_id SERIAL PRIMARY KEY,
    entity_name VARCHAR(100),
    region VARCHAR(50),
    risk_level VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE transactions (
    transaction_id UUID PRIMARY KEY,
    timestamp TIMESTAMP,
    source_entity INT REFERENCES entities(entity_id),
    target_entity INT REFERENCES entities(entity_id),
    initiator_id INT,
    approver_id INT,
    amount NUMERIC(15,2),
    currency VARCHAR(10),
    category VARCHAR(50),
    approval_status VARCHAR(20),
    fx_flag BOOLEAN,
    risk_score FLOAT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE anomaly_flags (
    anomaly_id SERIAL PRIMARY KEY,
    transaction_id UUID REFERENCES transactions(transaction_id),
    anomaly_type VARCHAR(100),
    severity_score FLOAT,
    confidence_score FLOAT,
    review_status VARCHAR(30),
    detected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE audit_logs (
    log_id SERIAL PRIMARY KEY,
    anomaly_id INT REFERENCES anomaly_flags(anomaly_id),
    action_taken TEXT,
    reviewer VARCHAR(100),
    action_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);