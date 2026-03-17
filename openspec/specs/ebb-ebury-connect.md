# Domain Specification: ebb-ebury-connect

**Status**: Active  
**Last Updated**: 2026-03-16  
**Repository**: `/home/marcosgomes/Projects/Ebury-Brazil/ebb-ebury-connect/`

---

## Overview

Ebury Connect domain provides integration between Ebury Brazil operations and the global Ebury platform.

### Core Responsibilities
- Data synchronization with global Ebury platform
- Cross-border transaction coordination
- Customer data replication
- Compliance data sharing
- Reporting aggregation

---

## Architecture

### GitOps Repositories (17)

Todos usam **Kustomize** com estrutura base + overlays (ebb-dev, staging-platform, ebb-prd).

**Webpayments (ebb-wp-*) - 13 repositórios**:
1. **ebb-wp-core-gitops** - Core payment processing
2. **ebb-wp-data-gitops** - Payment data management
3. **ebb-wp-documentation-gitops** - Payment documentation
4. **ebb-wp-file-converter-gitops** - Payment file format conversion
5. **ebb-wp-file-processor-gitops** - Payment file processing
6. **ebb-wp-hedges-gitops** - FX hedging for payments
7. **ebb-wp-limit-gitops** - Payment limits management
8. **ebb-wp-mocks-gitops** - Test mocks
9. **ebb-wp-notification-adp-gitops** - Payment notifications
10. **ebb-wp-pre-validation-gitops** - Payment pre-validation
11. **ebb-wp-query-gitops** - Payment queries
12. **ebb-wp-quotes-gitops** - FX quotes for payments
13. **ebb-wp-uploads-gitops** - Payment file uploads

**Platform Integration - 4 repositórios**:
1. **ebb-partners-settings-gitops** - Partner configurations
2. **ebb-proxy-merchants-gitops** - Merchant proxy service
3. **ebb-external-api-documentation-gitops** - External API docs
4. **ebb-wp-core-tests** - Core payment tests (não tem suffix -gitops)

**Estrutura padrão**: Base + overlays (ebb-dev, staging-platform, ebb-prd).

### Integration Patterns

**Synchronization Types**:
1. **Real-time sync** - Critical transaction data
2. **Batch sync** - Bulk customer/account data
3. **Event-driven** - Status changes, notifications
4. **On-demand** - Reports, queries

**Data Flow**:
```
Ebury Brazil Services ↔ ebb-ebury-connect ↔ Global Ebury Platform
```

---

## Key Integrations

### Customer Data
- Customer profiles
- KYC/AML status
- Account information
- Transaction history

### Compliance
- Regulatory reporting
- Sanctions screening results
- Audit logs

### Financial Data
- Payment instructions
- FX trades
- Treasury positions
- Settlement information

---

## Infrastructure

### GCP Project
- `ebb-ebury-connect-{dev,stg,prd}`

### Communication
- **REST APIs** - Synchronous operations
- **Message Queues** - Asynchronous events
- **VPN/Interconnect** - Secure connectivity to global platform

---

## Security

### Data Classification
- **Confidential** - Customer PII, financial data
- **Encryption** - TLS for transit, encryption at rest
- **Access Control** - Strict IAM, audit logging

### Compliance
- Cross-border data transfer agreements
- LGPD compliance for Brazilian data
- GDPR compliance for EU customer data

---

## Operations

### Monitoring
- Sync lag/delays
- API availability (global platform)
- Data quality checks
- Failed sync jobs

### Common Tasks

```bash
# Check sync status
kubectl logs -n ebury-connect <sync-service> --tail=100

# Manual sync trigger (if needed)
# Use admin API or Cloud Scheduler

# Investigate sync failure
# Check logs, verify connectivity, data validation errors
```

---

## References

- [Ebury-Brazil Structure](../EBURY_BRAZIL_STRUCTURE.md)
- [Global Ebury Platform Docs](https://docs.ebury.com/)
- Change History: [changes/](../changes/) | [archive/](../archive/)

---

**Domain Owner**: Integration Team  
**Slack**: #ebury-connect
