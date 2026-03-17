# Domain Specification: ebb-client-journey

**Status**: Active  
**Last Updated**: 2026-03-16  
**Repository**: `/home/marcosgomes/Projects/Ebury-Brazil/ebb-client-journey/`

---

## Overview

Client journey domain manages customer onboarding, compliance (KYC/AML), fraud detection, risk assessment, and customer lifecycle operations.

### Core Responsibilities
- Customer onboarding workflows
- KYC (Know Your Customer) verification
- AML/CFT compliance screening
- Fraud detection and prevention
- Risk assessment and scoring
- Document management
- Salesforce integration

---

## Architecture

### Applications (apps/)

| Application | Purpose | Critical |
|-------------|---------|----------|
| **temis** | Core Temis platform - Monorepo | ✓ |
| **temis-registration-config-data-keys-salesforce** | Salesforce field mapping config | ✓ |

### GitOps Services (30+ repositories)

#### Core Services
- **ebb-temis-bff-gitops** - Backend for Frontend orchestration
- **ebb-temis-onboarding-engine-gitops** - Onboarding workflow engine

#### Compliance & Risk
- **ebb-temis-compliance-gitops** - Main compliance service
- **ebb-temis-compliance-action-gitops** - Compliance action processor
- **ebb-temis-compliance-screening-gitops** - Screening checks (sanctions, PEP)
- **ebb-temis-risk-gitops** - Risk assessment engine
- **ebb-temis-fraud-gitops** - Fraud detection

#### Data & Integration
- **ebb-temis-bureau-gitops** - Credit bureau integration
- **ebb-temis-bureau-data-integrator-gitops** - Bureau data sync
- **ebb-temis-salesforce-adapter-gitops** - Salesforce bidirectional sync
- **temis-salesforce-adapter-gitops** - Legacy adapter

#### Registration & Customer Management
- **ebb-temis-registration-gitops** - Customer registration service
- **ebb-temis-query-gitops** - Query service for customer data
- **ebb-temis-internal-account-management-gitops** - Internal account ops
- **temis-internal-account-management-gitops** - Legacy version

#### Supporting Services
- **ebb-temis-config-gitops** - Configuration management
- **ebb-temis-notification-gitops** - Notification service
- **ebb-temis-email-sender-gitops** - Email delivery
- **temis-email-sender-gitops** - Legacy version
- **ebb-temis-digital-signature-gitops** - Digital signature integration
- **temis-digital-signature-gitops** - Legacy version
- **ebb-temis-enrichment-gitops** - Data enrichment
- **temis-enrichment-gitops** - Legacy version
- **ebb-temis-expiration-date-gitops** - Document expiration tracking
- **ebb-temis-limit-gitops** - Limit management
- **ebb-temis-mocks-v2-gitops** - Test mocks
- **ebb-temis-restrictive-lists-gitops** - Blocklists/allowlists
- **ebb-temis-tas-integrator-gitops** - TAS integration
- **ebb-temis-tree-adapter-gitops** - Tree system adapter
- **temis-compliance-gitops** - Legacy compliance

**Total**: 30 repositórios GitOps (24 ebb-temis-*, 6 temis-* legados)

**Estrutura padrão dos repositórios GitOps**:
```
<service>-gitops/
├── base/
│   ├── deployment.yaml           # Deployment principal
│   ├── deployment-sync.yaml      # Deployment síncrono
│   ├── deployment-async.yaml     # Deployment assíncrono
│   ├── deployment-sync-ext.yaml  # Deployment com exposição externa
│   ├── service.yaml
│   ├── service-sync.yaml
│   ├── service-async.yaml
│   ├── service-sync-ext.yaml
│   ├── ingress.yaml
│   ├── ingress-ext.yaml          # Ingress externo (quando necessário)
│   └── pod-monitor.yaml
├── overlays/
│   ├── ebb-dev/
│   │   ├── namespace.yaml
│   │   ├── configmap.yaml
│   │   ├── service-account.yaml
│   │   ├── external-secret.yaml
│   │   ├── hpa.yaml
│   │   ├── hpa-sync.yaml
│   │   ├── hpa-async.yaml
│   │   └── ingress-ext.yaml
│   ├── staging-platform/
│   └── ebb-prd/
└── application/
    └── kustomization.yaml
```

**Padrão multi-deployment**: Muitos serviços têm 3 deployments separados (sync, sync-ext, async) para:
- **sync**: Processamento síncrono interno
- **sync-ext**: Exposição externa com ingress público
- **async**: Processamento assíncrono (event-driven)

Todos usam **Kustomize** para gerenciamento de configurações por ambiente.

---

## Key Services

### ebb-temis-bff (Backend for Frontend)
**Purpose**: API orchestration layer for frontend applications

**Responsibilities**:
- Aggregate data from multiple Temis services
- Transform/format data for UI consumption
- Handle authentication/authorization
- Rate limiting and caching

**Consumers**:
- Web applications
- Mobile apps
- Partner integrations

### ebb-temis-onboarding-engine
**Purpose**: Orchestrate complete customer onboarding workflow

**Workflow Steps**:
1. Initial data capture
2. Document upload & validation
3. Bureau checks (credit)
4. Compliance screening (KYC, AML, sanctions)
5. Fraud analysis
6. Risk assessment
7. Approval/rejection decision
8. Account creation (if approved)
9. Salesforce sync

**State Machine**: Tracks customer progress through onboarding stages

### ebb-temis-compliance & Screening
**Purpose**: Ensure regulatory compliance for all customers

**Checks Performed**:
- **KYC**: Identity verification, document validation
- **AML/CFT**: Anti-money laundering, terrorist financing
- **Sanctions**: OFAC, EU, UN sanctions lists
- **PEP**: Politically Exposed Persons screening
- **Adverse Media**: Negative news screening

**Data Sources**:
- Internal databases
- External screening providers
- Government watchlists
- Bureau data

**Compliance Actions**:
- Block transactions
- Flag for manual review
- Trigger additional verification
- Close accounts (post-onboarding)

### ebb-temis-fraud
**Purpose**: Real-time fraud detection and prevention

**Detection Methods**:
- Rule-based engines
- ML models (behavior analysis)
- Velocity checks (transaction patterns)
- Device fingerprinting
- Geolocation analysis

**Actions**:
- Block suspicious transactions
- Step-up authentication (MFA)
- Manual review queue
- Account suspension

### ebb-temis-risk
**Purpose**: Assess and score customer risk

**Risk Factors**:
- Credit score (from bureau)
- Transaction patterns
- Industry/sector
- Geography
- Compliance history
- Relationship tenure

**Output**:
- Risk score (0-100)
- Risk category (low/medium/high)
- Recommended limits
- Monitoring frequency

### ebb-temis-salesforce-adapter
**Purpose**: Bidirectional sync with Salesforce CRM

**Sync Direction**:
- **Temis → Salesforce**: Customer data, status updates, documents
- **Salesforce → Temis**: Account changes, manual overrides

**Field Mapping**: Managed by `temis-registration-config-data-keys-salesforce`

---

## Infrastructure

### GCP Projects
- `ebb-client-journey-dev`
- `ebb-client-journey-staging`  
- `ebb-client-journey-prod`

### GKE Clusters
- Region: `southamerica-east1`
- Namespaces per service or grouped by function

### Databases
- **Cloud SQL** - Relational data (customers, applications)
- **Firestore** - Document storage, real-time updates
- **Cloud Storage** - Document/file storage (KYC docs)

### External Integrations
- **Salesforce** - CRM
- **Bureau Providers** - Credit checks (Serasa, Boa Vista)
- **Screening Providers** - Compliance checks
- **Tree Platform** - Treasury operations

---

## Dependencies

### Upstream (Consumes from)
- **ebb-treasury** - Account funding status
- **ebb-money-flows** - Payment history for risk scoring

### Downstream (Provides to)
- **ebb-money-flows** - Customer status, limits, compliance status
- **ebb-treasury** - Customer onboarding completion
- **Salesforce** - All customer data

---

## Security & Compliance

### Data Sensitivity
- **PII** - Name, CPF/CNPJ, address, phone, email
- **Financial Data** - Bank accounts, credit scores
- **Documents** - ID, proof of address, tax documents

### Encryption
- At rest: All databases and storage encrypted
- In transit: TLS 1.2+
- Field-level: Sensitive fields (CPF) additionally encrypted

### Access Control
- Workload Identity for service-to-service
- IAM with least privilege
- Audit logging for all PII access

### Compliance Standards
- **LGPD** (Brazilian GDPR)
- **Bacen regulations** (customer data)
- **PCI DSS** (if handling card data)

### Data Retention
- Active customers: Indefinite (with consent)
- Rejected applications: 5 years (compliance requirement)
- Closed accounts: 5 years (regulatory)

---

## Operational Concerns

### Monitoring
- Onboarding funnel metrics (drop-off rates)
- Compliance check latency
- Fraud detection accuracy (false positives/negatives)
- Salesforce sync lag

### Alerting
- Onboarding failures
- Compliance check API failures
- High fraud score alerts
- Salesforce sync errors
- Bureau API downtime

### SLAs
- Onboarding time: Target < 24 hours
- Compliance checks: < 5 minutes
- Fraud scoring: < 1 second (real-time)

---

## Common Tasks

### Debug Failed Onboarding
```bash
# Check onboarding engine logs
kubectl logs -n client-journey ebb-temis-onboarding-engine --tail=100

# Check customer journey state
# Query Firestore or database for customer ID

# Check compliance service
kubectl logs -n client-journey ebb-temis-compliance --tail=50
```

### Manual Compliance Override
```bash
# Access compliance dashboard or Salesforce
# Document reason for override (audit trail)
# Update customer status
```

### Investigate Fraud Alert
```bash
# Check fraud service logs
kubectl logs -n client-journey ebb-temis-fraud --tail=100

# Review transaction history
# Check risk score
# Escalate to fraud team if needed
```

---

## References

- [Ebury-Brazil Structure](../EBURY_BRAZIL_STRUCTURE.md)
- [LGPD Compliance Guide](https://www.gov.br/lgpd)
- Change History: [changes/](../changes/) | [archive/](../archive/)

---

**Domain Owner**: Client Journey Team  
**On-call**: TBD  
**Slack**: #client-journey
