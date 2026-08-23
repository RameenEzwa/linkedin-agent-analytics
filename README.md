# LinkedIn Agent Analytics Platform

## Overview

The LinkedIn Agent Analytics Platform is an analytics solution for monitoring LinkedIn outreach activity, account health, data quality, risk signals, and recommended outreach capacity.

The platform moves data from source ingestion through an operational layer and analytical star schema into Power BI.

## Architecture

The main flow is:

Source API
→ API Client
→ Staging / Operational Layer
→ Transformation & Data Modeling
→ Star Schema
→ Power BI Presentation Layer

The analytical star schema contains:

- `dim_date`
- `dim_account`
- `dim_lead`
- `dim_campaign`
- `dim_segment`
- `fact_linkedin_activity`

The operational layer contains:

- `linkedin_outreach`
- `run_metadata`
- `dead_letter`
- `ingestion_watermark`

## Project Structure

```text
linkedin-agent-analytics/
├── database/
│   ├── schema.sql
│   └── dq_schema.sql
├── docs/
│   ├── architecture.md
│   ├── data_dictionary.md
│   ├── data_flow.md
│   ├── data_quality.md
│   ├── risk_model.md
│   └── star_schema.sql
├── powerbi/
│   └── Power BI report
├── src/
│   ├── analytics/
│   │   ├── capacity.py
│   │   └── risk_model.py
│   ├── ingestion/
│   │   ├── client.py
│   │   ├── database.py
│   │   └── loader.py
│   └── quality/
│       ├── dq_checks.py
│       ├── dq_runner.py
│       └── dq_score.py
├── tests/
│   ├── test_capacity.py
│   ├── test_database.py
│   ├── test_data_quality.py
│   ├── test_loader.py
│   └── test_risk_model.py
├── Scripts/
│   └── run_quality_check.ps1
├── requirements.txt
└── README.md