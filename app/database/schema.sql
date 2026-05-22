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

CREATE TABLE ai_audit_reports (
    report_id SERIAL PRIMARY KEY,
    transaction_id UUID,
    anomaly_type VARCHAR(100),
    generated_report TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

ALTER TABLE anomaly_flags
ADD COLUMN assigned_reviewer VARCHAR(100);

ALTER TABLE anomaly_flags
ADD COLUMN investigation_notes TEXT;

ALTER TABLE anomaly_flags
ADD COLUMN updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;

CREATE MATERIALIZED VIEW entity_risk_summary AS

SELECT
    t.source_entity,
    COUNT(af.anomaly_id) AS anomaly_count,
    AVG(af.severity_score) AS avg_severity,
    SUM(t.amount) AS total_volume

FROM transactions t

LEFT JOIN anomaly_flags af
ON t.transaction_id = af.transaction_id

GROUP BY t.source_entity;