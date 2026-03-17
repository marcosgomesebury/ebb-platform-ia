# Domain Specification: ebb-treasury

**Status**: Active  
**Last Updated**: 2026-03-16  
**Repository**: `/home/marcosgomes/Projects/Ebury-Brazil/ebb-treasury/`

---

## Overview

Treasury domain manages liquidity, treasury operations, and integration with Tree treasury platform.

### Core Responsibilities
- Treasury compliance monitoring
- Liquidity management
- Tree platform integration
- Treasury event processing
- Configuration management

---

## Architecture

### GitOps Repository (1)

**ebb-treasury-configs-gitops** - Configuration management for all treasury services

**Estrutura**: Usa Kustomize com overlays para dev/stg/prd.

**Nota**: Localizado diretamente em `ebb-treasury/ebb-treasury-configs-gitops/` (não dentro de subpasta `gitops/`).

### Services

| Service | Purpose | Type |
|---------|---------|------|
| **ebb-tree-compliance** | Treasury compliance checks | Application |
| **ebb-tree-consumer** | Tree event consumer | Application |
| **ebb-tree-producer** | Tree event producer | Application |
| **ebb-tree-provider-mock** | Mock Tree integration (testing) | Application |

---

## Key Services

### ebb-tree-compliance
**Purpose**: Ensure treasury operations comply with regulations

**Checks**:
- Transaction limits
- Regulatory reporting requirements
- Liquidity ratios
- Exposure limits

### ebb-tree-producer / consumer
**Purpose**: Event-driven integration with Tree platform

**Flow**:
```
Treasury Operation → ebb-tree-producer → Tree Platform
Tree Platform → ebb-tree-consumer → Internal Services
```

**Event Types**:
- Liquidity updates
- Treasury positions
- Settlement events
- Compliance notifications

---

## Infrastructure

### GCP Project
- `ebb-treasury-{dev,stg,prd}`

### Dependencies
- **Tree Platform** - External treasury system
- **ebb-money-flows** - Transaction data
- **ebb-client-journey** - Customer limits

---

## Operations

### Monitoring
- Tree API availability
- Event processing lag
- Compliance check failures

### Common Tasks

```bash
# Check Tree connection
kubectl logs -n treasury ebb-tree-producer --tail=50

# Review compliance alerts
kubectl logs -n treasury ebb-tree-compliance --tail=100
```

---

## References

- [Ebury-Brazil Structure](../EBURY_BRAZIL_STRUCTURE.md)
- Change History: [changes/](../changes/) | [archive/](../archive/)

---

**Domain Owner**: Treasury Team  
**Slack**: #treasury
