# Domain Specification: ebb-fx

**Status**: Active  
**Last Updated**: 2026-03-16  
**Repository**: `/home/marcosgomes/Projects/Ebury-Brazil/ebb-fx/`

---

## Overview

FX (Foreign Exchange) domain provides real-time currency exchange rates and trading operations.

### Core Responsibilities
- FX rate provisioning
- Rate aggregation from providers
- Historical rate storage
- Trading operations support

---

## Architecture

### GitOps

**Nota**: Este domínio não possui repositórios GitOps separados. O deployment do **forex-provider** é gerenciado pelo repositório de aplicação ou via templates compartilhados do ebb-platform.

### Services

| Service | Purpose |
|---------|---------|
| **forex-provider** | FX rate provider integration and aggregation |

---

## Key Service: forex-provider

**Purpose**: Aggregate FX rates from multiple providers and serve to other services

**Features**:
- Real-time rate updates
- Multiple provider support (fallback/redundancy)
- Rate caching for performance
- Historical rate storage
- Rate change notifications

**API**:
- `GET /rates` - Current rates for currency pairs
- `GET /rates/history` - Historical rates
- `WebSocket /rates/stream` - Real-time rate updates

**Consumers**:
- **ebb-money-flows** - Payment FX conversion
- **ebb-treasury** - Treasury operations
- **ebb-client-journey** - Customer rate quotes

---

## Infrastructure

### GCP Project
- `ebb-fx-{dev,stg,prd}`

### External Integrations
- FX rate provider APIs (Bloomberg, Reuters, etc.)
- Fallback providers for redundancy

### Data Storage
- **Firestore** - Real-time current rates
- **BigQuery** - Historical rates for analytics

---

## Operations

### Monitoring
- Provider API availability
- Rate stale check (alert if no update > threshold)
- API latency

### Alerting
- All providers down
- Stale rates (> 5 min without update)
- Abnormal rate volatility

### Common Tasks

```bash
# Check current rates
curl https://fx-api.ebury.com.br/rates

# Check provider status
kubectl logs -n fx forex-provider --tail=100

# Historical rate query
# Query BigQuery for specific date range
```

---

## References

- [Ebury-Brazil Structure](../EBURY_BRAZIL_STRUCTURE.md)
- Change History: [changes/](../changes/) | [archive/](../archive/)

---

**Domain Owner**: FX Team  
**Slack**: #fx-operations
