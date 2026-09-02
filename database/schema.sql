CREATE TABLE IF NOT EXISTS run_metadata (
    run_id UUID PRIMARY KEY,
    started_at TIMESTAMPTZ NOT NULL,
    ended_at TIMESTAMPTZ,
    rows_in INTEGER NOT NULL DEFAULT 0,
    rows_out INTEGER NOT NULL DEFAULT 0,
    status VARCHAR(20) NOT NULL,
    error_message TEXT
);

CREATE TABLE IF NOT EXISTS dead_letter (
    id BIGSERIAL PRIMARY KEY,
    run_id UUID NOT NULL,
    record_payload JSONB,
    error_message TEXT NOT NULL,
    failed_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS linkedin_outreach (
    lead_id VARCHAR(100) PRIMARY KEY,
    profile_url TEXT,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    job_title TEXT,
    company_name TEXT,
    industry TEXT,
    network_degree VARCHAR(20),
    pipeline_stage VARCHAR(50),
    invited_at TIMESTAMPTZ,
    accepted_at TIMESTAMPTZ,
    messaged_at TIMESTAMPTZ,
    replied_at TIMESTAMPTZ,
    last_updated_at TIMESTAMPTZ NOT NULL,
    source_updated_at TIMESTAMPTZ,
    raw_payload JSONB,
    loaded_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS ingestion_watermark (
    source_name VARCHAR(100) PRIMARY KEY,
    last_updated_at TIMESTAMPTZ
);