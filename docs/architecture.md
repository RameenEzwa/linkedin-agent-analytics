# LinkedIn Agent Analytics Platform
# Data Architecture & Modeling

## 1. Star Schema

The analytical database uses a star-schema architecture consisting
of one conformed fact table and shared dimension tables.

### Fact Table

**fact_linkedin_activity**

**Grain:** One outreach activity/event for one lead, account,
campaign, segment, and timestamp.

Primary key:

- activity_key

Foreign keys:

- date_key → dim_date.date_key
- account_key → dim_account.account_key
- lead_key → dim_lead.lead_key
- campaign_key → dim_campaign.campaign_key
- segment_key → dim_segment.segment_key

Measures/events:

- invite_sent
- invite_accepted
- message_sent
- reply_received
- conversion

### Dimension Tables

#### dim_date

Grain: One row per calendar date.

Surrogate key:

- date_key

#### dim_account

Grain: One row per account version.

Surrogate key:

- account_key

Business key:

- account_id

SCD strategy:

- Type 2

Historical versions are represented using:

- effective_from
- effective_to
- is_current

#### dim_lead

Grain: One row per lead version.

Surrogate key:

- lead_key

Business key:

- lead_id

SCD strategy:

- Type 2

Historical versions are represented using:

- effective_from
- effective_to
- is_current

#### dim_campaign

Grain: One row per campaign.

Surrogate key:

- campaign_key

Business key:

- campaign_id

#### dim_segment

Grain: One row per target segment.

Surrogate key:

- segment_key

Business key:

- segment_id

## 2. Relationships

The fact table references the shared dimensions through
foreign keys.

dim_date → fact_linkedin_activity

dim_account → fact_linkedin_activity

dim_lead → fact_linkedin_activity

dim_campaign → fact_linkedin_activity

dim_segment → fact_linkedin_activity

The dimensions are therefore conformed dimensions and can be
used consistently across analytical reporting.

## 3. Slowly Changing Dimensions

Type 2 SCD is used for account and lead dimensions where
historical changes may affect analytical reporting.

Each version contains:

- effective_from
- effective_to
- is_current

This preserves historical attribute values rather than
overwriting the previous version.

## 4. Operational and Analytical Layers

The Part 2 operational tables remain separate from the
analytical star schema.

Operational tables include:

- linkedin_outreach
- run_metadata
- dead_letter
- ingestion_watermark

The Part 3 analytical layer consists of:

- dim_date
- dim_account
- dim_lead
- dim_campaign
- dim_segment
- fact_linkedin_activity

This separation allows ingestion and operational processing
to remain independent from analytical reporting.