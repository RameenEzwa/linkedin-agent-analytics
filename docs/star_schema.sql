-- ============================================================
-- PART 3: LINKEDIN AGENT ANALYTICS STAR SCHEMA
-- ============================================================

-- ------------------------------------------------------------
-- Dimension: Date
-- Grain: one row per calendar date
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS dim_date (
    date_key INTEGER PRIMARY KEY,
    full_date DATE NOT NULL UNIQUE,
    year INTEGER NOT NULL,
    quarter INTEGER NOT NULL,
    month INTEGER NOT NULL,
    month_name VARCHAR(20) NOT NULL,
    week_of_year INTEGER NOT NULL,
    day_of_month INTEGER NOT NULL,
    day_of_week INTEGER NOT NULL,
    day_name VARCHAR(20) NOT NULL
);


-- ------------------------------------------------------------
-- Dimension: Account
-- Grain: one row per account version
-- SCD Type 2
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS dim_account (
    account_key BIGSERIAL PRIMARY KEY,
    account_id VARCHAR(100) NOT NULL,
    account_name VARCHAR(200),
    account_status VARCHAR(50),
    account_age_tier VARCHAR(50),
    daily_capacity_limit INTEGER,
    effective_from TIMESTAMP NOT NULL,
    effective_to TIMESTAMP,
    is_current BOOLEAN NOT NULL DEFAULT TRUE,

    CONSTRAINT uq_dim_account_version
        UNIQUE (account_id, effective_from)
);


-- ------------------------------------------------------------
-- Dimension: Lead
-- Grain: one row per lead version
-- SCD Type 2
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS dim_lead (
    lead_key BIGSERIAL PRIMARY KEY,
    lead_id VARCHAR(100) NOT NULL,
    profile_url TEXT,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    job_title TEXT,
    company_name TEXT,
    industry TEXT,
    network_degree VARCHAR(20),
    effective_from TIMESTAMP NOT NULL,
    effective_to TIMESTAMP,
    is_current BOOLEAN NOT NULL DEFAULT TRUE,

    CONSTRAINT uq_dim_lead_version
        UNIQUE (lead_id, effective_from)
);


-- ------------------------------------------------------------
-- Dimension: Campaign
-- Grain: one row per campaign
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS dim_campaign (
    campaign_key BIGSERIAL PRIMARY KEY,
    campaign_id VARCHAR(100) NOT NULL UNIQUE,
    campaign_name VARCHAR(200) NOT NULL,
    campaign_status VARCHAR(50),
    start_date DATE,
    end_date DATE
);


-- ------------------------------------------------------------
-- Dimension: Segment
-- Grain: one row per target segment
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS dim_segment (
    segment_key BIGSERIAL PRIMARY KEY,
    segment_id VARCHAR(100) NOT NULL UNIQUE,
    segment_name VARCHAR(200) NOT NULL,
    industry VARCHAR(200),
    description TEXT
);


-- ------------------------------------------------------------
-- Fact: LinkedIn Activity
-- Grain:
-- one outreach activity/event for one lead, account,
-- campaign, segment, and timestamp.
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS fact_linkedin_activity (
    activity_key BIGSERIAL PRIMARY KEY,

    date_key INTEGER NOT NULL,
    account_key BIGINT NOT NULL,
    lead_key BIGINT NOT NULL,
    campaign_key BIGINT,
    segment_key BIGINT,

    activity_timestamp TIMESTAMP NOT NULL,

    invite_sent INTEGER NOT NULL DEFAULT 0,
    invite_accepted INTEGER NOT NULL DEFAULT 0,
    message_sent INTEGER NOT NULL DEFAULT 0,
    reply_received INTEGER NOT NULL DEFAULT 0,
    conversion INTEGER NOT NULL DEFAULT 0,

    source_lead_id VARCHAR(100),
    loaded_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_activity_date
        FOREIGN KEY (date_key)
        REFERENCES dim_date(date_key),

    CONSTRAINT fk_activity_account
        FOREIGN KEY (account_key)
        REFERENCES dim_account(account_key),

    CONSTRAINT fk_activity_lead
        FOREIGN KEY (lead_key)
        REFERENCES dim_lead(lead_key),

    CONSTRAINT fk_activity_campaign
        FOREIGN KEY (campaign_key)
        REFERENCES dim_campaign(campaign_key),

    CONSTRAINT fk_activity_segment
        FOREIGN KEY (segment_key)
        REFERENCES dim_segment(segment_key)
);