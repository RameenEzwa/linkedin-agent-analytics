# Data Dictionary

## dim_date

| Column | Type | Business Definition |
|---|---|---|
| date_key | INTEGER | Surrogate calendar key used by the fact table. |
| full_date | DATE | Full calendar date. |
| year | INTEGER | Calendar year. |
| quarter | INTEGER | Calendar quarter, 1–4. |
| month | INTEGER | Calendar month number. |
| month_name | VARCHAR(20) | Calendar month name. |
| week_of_year | INTEGER | ISO/calendar week number. |
| day_of_month | INTEGER | Day number within the month. |
| day_of_week | INTEGER | Numeric day-of-week value. |
| day_name | VARCHAR(20) | Name of the day. |

## dim_account

| Column | Type | Business Definition |
|---|---|---|
| account_key | BIGINT | Surrogate key identifying an account dimension version. |
| account_id | VARCHAR(100) | Business identifier for the LinkedIn account. |
| account_name | VARCHAR(200) | Display name of the account/agent. |
| account_status | VARCHAR(50) | Current or historical account status. |
| account_age_tier | VARCHAR(50) | Account age tier used for capacity/risk rules. |
| daily_capacity_limit | INTEGER | Maximum planned daily activity for the account. |
| effective_from | TIMESTAMP | Start timestamp for this dimension version. |
| effective_to | TIMESTAMP | End timestamp for this dimension version. |
| is_current | BOOLEAN | Indicates whether this is the current account version. |

## dim_lead

| Column | Type | Business Definition |
|---|---|---|
| lead_key | BIGINT | Surrogate key identifying a lead dimension version. |
| lead_id | VARCHAR(100) | Source/business identifier for the lead. |
| profile_url | TEXT | LinkedIn profile URL. |
| first_name | VARCHAR(100) | Lead's first name. |
| last_name | VARCHAR(100) | Lead's last name. |
| job_title | TEXT | Lead's job title. |
| company_name | TEXT | Lead's company name. |
| industry | TEXT | Industry associated with the lead/company. |
| network_degree | VARCHAR(20) | LinkedIn network relationship degree. |
| effective_from | TIMESTAMP | Start timestamp for this dimension version. |
| effective_to | TIMESTAMP | End timestamp for this dimension version. |
| is_current | BOOLEAN | Indicates whether this is the current lead version. |

## dim_campaign

| Column | Type | Business Definition |
|---|---|---|
| campaign_key | BIGINT | Surrogate campaign key. |
| campaign_id | VARCHAR(100) | Business identifier for the campaign. |
| campaign_name | VARCHAR(200) | Campaign name. |
| campaign_status | VARCHAR(50) | Current campaign status. |
| start_date | DATE | Campaign start date. |
| end_date | DATE | Campaign end date. |

## dim_segment

| Column | Type | Business Definition |
|---|---|---|
| segment_key | BIGINT | Surrogate segment key. |
| segment_id | VARCHAR(100) | Business identifier for the target segment. |
| segment_name | VARCHAR(200) | Target segment name. |
| industry | VARCHAR(200) | Industry represented by the segment. |
| description | TEXT | Business description of the segment. |

## fact_linkedin_activity

| Column | Type | Business Definition |
|---|---|---|
| activity_key | BIGINT | Surrogate key identifying an activity record. |
| date_key | INTEGER | Foreign key to dim_date. |
| account_key | BIGINT | Foreign key to dim_account. |
| lead_key | BIGINT | Foreign key to dim_lead. |
| campaign_key | BIGINT | Foreign key to dim_campaign. |
| segment_key | BIGINT | Foreign key to dim_segment. |
| activity_timestamp | TIMESTAMP | Date and time when the activity occurred. |
| invite_sent | INTEGER | Indicator/count that an invitation was sent. |
| invite_accepted | INTEGER | Indicator/count that an invitation was accepted. |
| message_sent | INTEGER | Indicator/count that a message was sent. |
| reply_received | INTEGER | Indicator/count that a reply was received. |
| conversion | INTEGER | Indicator/count that the activity resulted in a conversion. |
| source_lead_id | VARCHAR(100) | Source-system lead identifier retained for traceability. |
| loaded_at | TIMESTAMP | Timestamp when the analytical record was loaded. |