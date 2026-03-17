# Domain Specification: ebb-bigdata

**Status**: Active  
**Last Updated**: 2026-03-16  
**Repository**: `/home/marcosgomes/Projects/Ebury-Brazil/ebb-bigdata/`

---

## Overview

BigData domain manages data pipelines, ETL processes, analytics, and business intelligence for Ebury Brazil.

### Core Responsibilities
- Data ingestion from operational systems
- ETL (Extract, Transform, Load) pipelines
- Data warehousing
- Analytics and reporting
- ML model training data preparation

---

## Architecture

### Infrastructure as Code

**Airflow Deployment**: Usa **Helm** (`helm_apache_airflow/`) ao invés de Kustomize GitOps tradicional.

**DAGs Repository**: `ebb-airflow-dags/` contém:
- Python DAG definitions
- SQL transformations
- Data quality checks
- Scheduling configurations

**Deployment**: Airflow DAGs são sincronizados via Git sync do Airflow, não requerem repositórios GitOps separados.

### Data Platform Components

**Orchestration**: Apache Airflow  
**Storage**: BigQuery (warehouse), Cloud Storage (data lake)  
**Processing**: Dataflow, Dataproc  
**Visualization**: Looker, Data Studio

---

## Data Sources

### Internal Systems
- **ebb-money-flows** - Transaction data, payment events
- **ebb-client-journey** - Customer data, onboarding metrics
- **ebb-treasury** - Treasury positions, liquidity
- **ebb-fx** - Historical FX rates

### External Sources
- Bank statements (automated imports)
- Regulatory data feeds
- Third-party enrichment data

---

## Data Pipelines

### Operational Data Sync
**Frequency**: Real-time or hourly  
**Purpose**: Keep warehouse in sync with operational databases  
**Technology**: Change Data Capture (CDC) or scheduled dumps

### Aggregated Reporting
**Frequency**: Daily  
**Purpose**: Management dashboards, KPIs  
**Output**: Materialized views, summary tables

### ML Feature Engineering
**Frequency**: As needed  
**Purpose**: Prepare training datasets for fraud, risk models  
**Output**: Feature stores, labeled datasets

### Regulatory Reporting
**Frequency**: Monthly / On-demand  
**Purpose**: Bacen, tax, compliance reports  
**Output**: Structured reports, audit trails

---

## Data Warehouse Schema

### Core Tables

**Fact Tables**:
- `fact_transactions` - All transactions across services
- `fact_customer_events` - Customer lifecycle events
- `fact_compliance_checks` - Compliance actions/results

**Dimension Tables**:
- `dim_customers` - Customer master data
- `dim_accounts` - Account information
- `dim_products` - Product catalog
- `dim_time` - Time dimension for analytics

---

## Airflow DAGs

### Example DAGs

#### daily_transaction_aggregation
```python
# Aggregates daily transaction metrics
# Sources: Cloud SQL, Firestore
# Target: BigQuery fact_transactions
# Schedule: 02:00 daily
```

#### customer_360_refresh
```python
# Refreshes customer 360 view
# Sources: All customer-related tables
# Target: BigQuery dim_customers
# Schedule: 06:00 daily
```

#### bacen_monthly_report
```python
# Generates monthly Bacen compliance report
# Sources: BigQuery warehouse
# Target: Cloud Storage (encrypted)
# Schedule: 1st of month
```

---

## Infrastructure

### GCP Project
- `ebb-bigdata-{dev,stg,prd}`

### Key Services
- **Cloud Composer** (Managed Airflow)
- **BigQuery** - Data warehouse
- **Cloud Storage** - Data lake
- **Dataflow** - Stream/batch processing
- **Pub/Sub** - Event ingestion

---

## Data Governance

### Data Quality
- Validation checks in pipelines
- Data profiling and monitoring
- Anomaly detection

### Data Lineage
- Track data flow from source to destination
- Document transformations
- Enable impact analysis

### Access Control
- Column-level security in BigQuery
- Row-level security for sensitive data
- Audit logs for data access

### Privacy
- LGPD compliance (data anonymization where required)
- PII data handling procedures
- Data retention policies

---

## Operations

### Monitoring
- DAG success/failure rates
- Pipeline execution time
- Data freshness (SLA)
- BigQuery slot usage

### Alerting
- Failed DAG runs
- Data quality check failures
- SLA breaches (stale data)
- Excessive BigQuery costs

### Common Tasks

#### Debug Failed DAG
```bash
# Check Airflow logs
# Navigate to Cloud Composer UI
# Review task logs for specific failure

# Rerun failed task
# airflow tasks clear <dag_id> <task_id> <execution_date>
```

#### Query Recent Data
```sql
-- BigQuery example
SELECT 
  DATE(created_at) as date,
  COUNT(*) as transactions,
  SUM(amount) as total_amount
FROM `ebb-bigdata-prd.warehouse.fact_transactions`
WHERE DATE(created_at) >= DATE_SUB(CURRENT_DATE(), INTERVAL 7 DAY)
GROUP BY date
ORDER BY date DESC
```

#### Add New Data Source
1. Create connection in Airflow
2. Write DAG for extraction
3. Define schema in BigQuery
4. Add data quality checks
5. Document in data catalog
6. Test in dev, promote to prod

---

## References

- [Airflow Best Practices](https://airflow.apache.org/docs/apache-airflow/stable/best-practices.html)
- [BigQuery Optimization](https://cloud.google.com/bigquery/docs/best-practices-performance-overview)
- [Ebury-Brazil Structure](../EBURY_BRAZIL_STRUCTURE.md)
- Change History: [changes/](../changes/) | [archive/](../archive/)

---

**Domain Owner**: Data Engineering Team  
**Slack**: #data-engineering
