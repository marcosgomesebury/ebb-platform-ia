# Domain Specification: ebb-money-flows

**Status**: Active  
**Last Updated**: 2026-03-16  
**Repository**: `/home/marcosgomes/Projects/Ebury-Brazil/ebb-money-flows/`

---

## Overview

Money flows domain handles payment processing, Pix integration, Bacen reporting, reconciliation, and money movement operations for Ebury Brazil.

### Core Responsibilities
- Payment processing and orchestration
- Pix (Brazilian instant payment) integration
- Bacen (Central Bank of Brazil) reporting and compliance
- Transaction reconciliation
- Statement generation
- Bexs platform integration

---

## Architecture

### Applications (apps/)

| Service | Purpose | Tech Stack | Critical |
|---------|---------|------------|----------|
| **ebb-bexs-bacen-adapter** | Bacen reporting adapter | - | ✓ |
| **ebb-bexs-compliance** | Compliance checks | - | ✓ |
| **ebb-bexs-forex-documentation** | FX documentation | - | - |
| **ebb-bexs-notification** | Notification service | - | ✓ |
| **ebb-bexs-sta** | STA processing | - | - |
| **ebb-bexs-statement** | Statement generation | - | ✓ |
| **ebb-conciliacao** | Reconciliation service | - | ✓ |
| **ebb-pix-spi** | Pix SPI integration | Go | ✓ |

### GitOps Repositories (5)

Todos usam **Kustomize** com estrutura base + overlays (ebb-dev, staging-platform, ebb-prd).

1. **ebb-account-gitops** - Manifests para ebb-account
2. **ebb-jd-certificate-hsm-gitops** - Manifests para certificado digital JD/HSM
3. **ebb-legal-proceedings-gitops** - Manifests para processos judiciais
4. **ebb-pix-dict-gitops** - Manifests para Pix DICT client
5. **ebb-pix-spi-gitops** - Manifests para Pix SPI client

**Estrutura padrão**:
```
<service>-gitops/
├── base/
│   ├── deployment.yaml
│   ├── service.yaml
│   ├── ingress.yaml
│   └── pod-monitor.yaml
├── overlays/
│   ├── ebb-dev/
│   ├── staging-platform/
│   └── ebb-prd/
└── application/
```

**Pendências**: Padronização de overlays (alguns repos têm `production` ao invés de `ebb-prd`). Ver [pendencias/gitops.md](/home/marcosgomes/Projects/ebb-platform-ia/pendencias/gitops.md)

---

## Key Services

### ebb-pix-spi
**Purpose**: Integration with Brazilian Pix instant payment system (SPI - Sistema de Pagamentos Instantâneos)

**Components**:
- `payin/` - Receive Pix payments
- `payout/` - Send Pix payments

**Infrastructure**:
- GKE cluster: `ebb-money-flows-{dev,stg,prd}`
- Namespace: `core`
- PubSub topics:
  - `ebb-pixspi-credit-validation-requests`
  - Additional topics (payin/payout)

**Known Issues**:
- Topic names hardcoded in code (need env var configuration)
- Requires prefixing with `ebb-` to match Terraform naming

### ebb-conciliacao
**Purpose**: Transaction reconciliation between different systems

**Infrastructure**:
- Database: Cloud SQL MySQL
  - Dev: `34.39.195.206` (projeto: `ebb-money-flows-dev`)
  - Database: `sistema_custo`
- Windows Server: `10.23.129.3` (dev), `10.23.129.4` (app server)

**Access**:
- SSH: `marcos@10.23.129.3`
- RDP: `marcos_gomes@10.23.129.4`

### ebb-bexs-bacen-adapter
**Purpose**: Central Bank reporting and compliance

**Responsibilities**:
- Submit required regulatory reports to Bacen
- Handle compliance data transformation
- Manage reporting schedules

---

## Infrastructure

### GCP Projects
- `ebb-money-flows-dev` - Development
- `ebb-money-flows-staging` - Staging
- `ebb-money-flows-prod` - Production

### GKE Clusters
- Region: `southamerica-east1`
- Namespaces:
  - `core` - Core services
  - Additional namespaces per service

### Databases
- **Cloud SQL MySQL** - Primary transactional database
- **Firestore** - Event store, real-time data
- **BigQuery** - Analytics and reporting

### Message/Event Infrastructure
- **PubSub** - Event streaming
- **Cloud Tasks** - Async job processing

---

## Dependencies

### External Services
- **Bexs Platform** - Core banking platform integration
- **SPI (Pix)** - Brazilian instant payment infrastructure
- **Bacen APIs** - Central Bank reporting
- **Salesforce** - CRM integration (via client-journey)

### Internal Dependencies
- **ebb-client-journey** - Customer data, KYC
- **ebb-treasury** - Liquidity management
- **ebb-fx** - Foreign exchange rates
- **ebb-platform** - Infrastructure, IaC, CI/CD

---

## Security & Compliance

### Authentication
- Workload Identity for GCP service accounts
- IAM roles with least privilege principle

### Compliance Requirements
- Bacen reporting (regulatory)
- AML/CFT transaction monitoring
- Data residency (Brazil)
- Audit logging

### Secrets Management
- Google Secret Manager
- Environment-specific secrets per overlay

---

## Operational Concerns

### Monitoring
- Cloud Monitoring (GCP)
- Custom metrics for Pix transactions
- Reconciliation status dashboards

### Alerting
- Failed Pix transactions
- Reconciliation discrepancies
- Bacen submission failures
- Database connection issues

### Known Issues
1. **Pix SPI Topics**: Hardcoded topic names need refactoring to env vars
2. **Conciliacao DB Access**: Network/firewall configuration for external access
3. **Cloud SQL Permissions**: Service accounts need `cloudsql.instances.get`, `cloudsql.instances.connect`

---

## Development

### Local Development
- Use SSH tunnel for database access
- Mock SPI endpoints for Pix testing
- Docker compose for local services

### Testing
- Unit tests per service
- Integration tests with test topics/queues
- E2E tests in ebb-dev environment

### Deployment
- GitOps via ArgoCD
- Progressive rollout: dev → stg → prd
- Automatic rollback on health check failures

---

## Common Tasks

### Debug Pix Transaction
```bash
# Check pod logs
kubectl logs -n core pix-spi-payin --tail=100

# Check PubSub messages
gcloud pubsub topics list --project=ebb-money-flows-dev

# Diagnose with subagent
python subagents/database_diagnostic_agent.py
```

### Access Reconciliation Database
```bash
# SSH access
ssh marcos@10.23.129.3

# Test MySQL connection
cd skills/mysql_connect
python main.py
```

### Update GitOps Configuration
```bash
cd Ebury-Brazil/ebb-money-flows/gitops/ebb-pix-spi-gitops/overlays/ebb-dev/
# Edit kustomization.yaml or manifests
git commit -m "feat(pix): update configuration"
# PR and merge triggers ArgoCD sync
```

---

## References

- [Ebury-Brazil Structure](../EBURY_BRAZIL_STRUCTURE.md)
- [Pix SPI Documentation](https://www.bcb.gov.br/estabilidadefinanceira/pix)
- Change History: [changes/](../changes/) | [archive/](../archive/)

---

**Domain Owner**: Money Flows Team  
**On-call**: TBD  
**Slack**: #money-flows
