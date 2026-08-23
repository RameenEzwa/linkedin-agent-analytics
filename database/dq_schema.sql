CREATE TABLE IF NOT EXISTS dq_results_history (
    dq_run_id UUID PRIMARY KEY,
    run_id UUID,
    checked_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    completeness_score NUMERIC(5,2) NOT NULL,
    uniqueness_score NUMERIC(5,2) NOT NULL,
    validity_score NUMERIC(5,2) NOT NULL,
    timeliness_score NUMERIC(5,2) NOT NULL,
    referential_integrity_score NUMERIC(5,2) NOT NULL,

    composite_dq_score NUMERIC(5,2) NOT NULL,

    threshold NUMERIC(5,2) NOT NULL,
    status VARCHAR(20) NOT NULL,

    total_checks INTEGER NOT NULL DEFAULT 0,
    passed_checks INTEGER NOT NULL DEFAULT 0,
    failed_checks INTEGER NOT NULL DEFAULT 0,

    failure_details JSONB
);