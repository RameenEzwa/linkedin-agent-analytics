# LinkedIn Agent Analytics Platform

An end-to-end analytics platform for monitoring LinkedIn outreach activity, account health, data quality, risk signals, and recommended outreach capacity.

The platform demonstrates a complete data workflow from ingestion and operational storage through data-quality validation, analytical modeling, risk/capacity calculations, and Power BI reporting.

---

## Overview

The LinkedIn Agent Analytics Platform is designed to support outreach operations with reliable, auditable analytics.

The solution provides:

- LinkedIn outreach data ingestion
- Idempotent loading and ingestion watermark management
- Operational data storage in PostgreSQL
- Dead-letter handling for failed records
- Automated data-quality checks and scoring
- Dimensional star-schema modeling
- Account risk scoring
- Recommended daily outreach capacity
- Power BI analytics and visualization
- Automated Python tests
- GitHub Actions CI validation
- Docker and Docker Compose deployment

### End-to-end flow

```text
Source API
    |
    v
API Client
    |
    v
Operational / Staging Layer
    |
    +--> Ingestion Watermark
    |
    +--> Dead Letter Records
    |
    v
Data Quality Checks
    |
    v
Analytical Star Schema
    |
    +--> Risk Analytics
    |
    +--> Capacity Analytics
    |
    v
Power BI
