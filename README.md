# NYC Taxi Lakehouse on Databricks

## Project Overview

This project demonstrates the implementation of an end-to-end Lakehouse architecture using Databricks, Delta Lake, Unity Catalog, and AWS S3.

The solution processes over 11 million NYC Taxi trip records through a Medallion Architecture (Bronze, Silver, and Gold layers), implementing data quality validations, dimensional modeling, workflow orchestration, and Delta Lake optimization features.

The project showcases industry-standard Data Engineering practices including data governance, lineage tracking, data quality management, workflow automation, and analytical data modeling.

---

## Architecture

```text
                AWS S3
            (Raw Taxi Files)
                     |
                     v
      +----------------------------+
      | Databricks Unity Catalog   |
      +----------------------------+
                     |
                     v
      +----------------------------+
      | Bronze Layer               |
      | Raw Delta Tables           |
      | Metadata Lineage Tracking  |
      +----------------------------+
                     |
                     v
      +----------------------------+
      | Silver Layer               |
      | Data Quality Validation    |
      | Rejected Records Handling  |
      | DQ Metrics                 |
      +----------------------------+
                     |
                     v
      +----------------------------+
      | Gold Layer                 |
      | Fact Tables                |
      | Dimension Tables           |
      | Business Data Mart         |
      +----------------------------+
                     |
                     v
      +----------------------------+
      | Analytics & Reporting      |
      +----------------------------+

       Databricks Workflow
               |
               v
    Bronze → Silver → Gold
```

---

## Technology Stack

| Category | Technologies |
|-----------|-------------|
| Cloud Storage | AWS S3 |
| Processing Engine | Databricks |
| Data Format | Delta Lake |
| Catalog & Governance | Unity Catalog |
| Programming Language | PySpark |
| Query Engine | Spark SQL |
| Workflow Orchestration | Databricks Workflows |
| Data Modeling | Star Schema |
| Data Quality | Custom Validation Framework |

---

## Dataset

### NYC Yellow Taxi Trip Data

Dataset Source:
https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page

### Files Processed

| File |
|--------|
| yellow_tripdata_2026-01.parquet |
| yellow_tripdata_2026-02.parquet |
| yellow_tripdata_2026-03.parquet |

### Dataset Statistics

| Metric | Value |
|----------|----------|
| Total Records | 11,077,206 |
| Files Processed | 3 |
| File Format | Parquet |
| Storage Format | Delta Lake |

---

# Medallion Architecture

## Bronze Layer

### Purpose

Store raw ingested data exactly as received from source systems.

### Transformations

- Raw Parquet ingestion
- Metadata extraction
- Lineage tracking
- Delta table creation

### Metadata Columns Added

- ingestion_timestamp
- source_file_path
- source_file_name

### Output Table

```sql
nyc_taxi.bronze.taxi_trip_bronze
```

---

## Silver Layer

### Purpose

Clean, validate, and standardize data for downstream consumption.

### Derived Columns

- pickup_date
- pickup_hour
- trip_duration_minutes
- trip_year
- trip_month

### Data Quality Rules

| Validation |
|------------|
| passenger_count > 0 |
| trip_distance > 0 |
| fare_amount > 0 |
| trip_duration_minutes > 0 |
| Null checks |

### Data Quality Results

| Metric | Value |
|----------|----------|
| Total Records | 11,077,206 |
| Valid Records | 7,668,647 |
| Rejected Records | 3,408,559 |
| DQ Percentage | 69.23% |

### Output Tables

```sql
nyc_taxi.silver.taxi_trip_silver
nyc_taxi.silver.taxi_trip_rejected
nyc_taxi.silver.dq_metrics
```

---

## Gold Layer

### Purpose

Provide business-ready data for reporting and analytics.

### Dimensional Model

Implemented using Star Schema.

### Dimension Tables

```sql
dim_date
dim_hour
dim_trip_category
dim_payment_type
```

### Fact Table

```sql
fact_trip
```

### Fact Measures

- trip_distance
- trip_duration_minutes
- fare_amount
- tip_amount
- total_amount

### Business Data Mart

```sql
monthly_revenue_summary
```

---

# Workflow Orchestration

A Databricks Workflow was created to automate pipeline execution.

### Workflow Name

```text
NYC_Taxi_Lakehouse_Pipeline
```

### Execution Flow

```text
Bronze_Ingestion
        ↓
Silver_Transformation
        ↓
Gold_Modeling
```

### Schedule

```text
Daily
06:00 AM
Asia/Calcutta
```

---

# Delta Lake Features

## Time Travel

Implemented:

```sql
VERSION AS OF
```

Use Cases:

- Historical reporting
- Data recovery
- Auditability

---

## Restore

Implemented:

```sql
RESTORE TABLE
```

Use Cases:

- Rollback accidental updates
- Disaster recovery

---

## Change Data Feed (CDF)

Enabled CDF for incremental data processing.

```sql
ALTER TABLE fact_trip
SET TBLPROPERTIES (
'delta.enableChangeDataFeed'='true'
)
```

Use Cases:

- Incremental ETL
- CDC Pipelines
- Data Synchronization

---

## OPTIMIZE

Implemented Delta file compaction.

```sql
OPTIMIZE fact_trip
```

Benefits:

- Reduced file fragmentation
- Faster query performance

---

## ZORDER

Implemented clustering on frequently queried columns.

```sql
OPTIMIZE fact_trip
ZORDER BY (date_key)
```

Benefits:

- Data skipping
- Reduced scan volume
- Faster analytics queries

---

# Key Learnings

- Databricks Lakehouse Architecture
- Medallion Data Design Pattern
- Delta Lake Internals
- Unity Catalog Governance
- Data Quality Framework Design
- Star Schema Modeling
- Workflow Automation
- Incremental Processing using CDF
- Query Optimization using ZORDER
- Data Recovery using Time Travel

---

# Project Outcomes

✅ Processed 11M+ records

✅ Implemented Bronze, Silver, Gold architecture

✅ Built Data Quality Framework

✅ Created Rejected Record Handling

✅ Designed Star Schema

✅ Automated Pipeline using Workflows

✅ Implemented Delta Lake Features

✅ Established Data Governance using Unity Catalog

---

# Future Enhancements

- Streaming ingestion using Auto Loader
- Real-time CDC processing
- Dashboarding using Power BI
- Data Observability Framework
- CI/CD Deployment Pipeline
- Infrastructure as Code using Terraform
