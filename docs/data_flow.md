# End-to-End Data Flow

## Overview

The platform moves LinkedIn outreach data from the source API
through ingestion and operational storage, into the analytical
star schema and finally into the presentation layer.

## Data Flow

```text
┌─────────────────────┐
│   LinkedIn API      │
│      Source         │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│     API Client      │
│                     │
│ • Authentication    │
│ • Retries           │
│ • Rate limiting     │
│ • Error handling    │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│     Staging /       │
│ Operational Layer   │
│                     │
│ linkedin_outreach   │
│ run_metadata        │
│ dead_letter         │
│ ingestion_watermark │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Transformation &    │
│ Data Modeling       │
│                     │
│ • Standardisation   │
│ • Business rules    │
│ • Dimension loading │
│ • Fact loading      │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────────────┐
│       Star Schema           │
│                             │
│ dim_date                    │
│ dim_account                 │
│ dim_lead                    │
│ dim_campaign                │
│ dim_segment                 │
│ fact_linkedin_activity      │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────┐
│ Presentation Layer  │
│                     │
│      Power BI       │
│                     │
│ • KPI reporting     │
│ • Account health    │
│ • Risk intelligence │
│ • Campaign ROI      │
└─────────────────────┘