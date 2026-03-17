# Domain Specifications

Domain specifications for Ebury Brazil business domains located in `/Ebury-Brazil/`.

## Available Specifications

| Domain | Services | GitOps Repos | Complexity | Spec |
|--------|----------|--------------|------------|------|
| **ebb-money-flows** | 9+ apps | 5 | High | [ebb-money-flows.md](ebb-money-flows.md) |
| **ebb-client-journey** | 30+ services | 30 | High | [ebb-client-journey.md](ebb-client-journey.md) |
| **ebb-platform** | IaC, CI/CD | - | High | [ebb-platform.md](ebb-platform.md) |
| **ebb-treasury** | 5 services | 1 | Medium | [ebb-treasury.md](ebb-treasury.md) |
| **ebb-fx** | 1 service | - | Low | [ebb-fx.md](ebb-fx.md) |
| **ebb-ebury-connect** | 17+ services | 17 | Medium | [ebb-ebury-connect.md](ebb-ebury-connect.md) |
| **ebb-bigdata** | Data pipelines | Helm | Medium | [ebb-bigdata.md](ebb-bigdata.md) |

**Total GitOps Repositories**: 53 (money-flows: 5, client-journey: 30, ebury-connect: 17, treasury: 1)

## GitOps Structure

Todos os repositórios GitOps usam **Kustomize** com a seguinte estrutura:

```
<service>-gitops/
├── base/                    # Recursos base
│   ├── deployment.yaml
│   ├── service.yaml
│   ├── ingress.yaml
│   └── pod-monitor.yaml
├── overlays/                # Configurações por ambiente
│   ├── ebb-dev/
│   ├── staging-platform/
│   └── ebb-prd/
└── application/
    └── kustomization.yaml
```

**Overlays** contém configurações específicas por ambiente:
- `namespace.yaml` - Definição do namespace
- `configmap.yaml` - Variáveis de ambiente
- `service-account.yaml` - Service account com Workload Identity
- `external-secret.yaml` - Secrets do Google Secret Manager
- `hpa.yaml` - Horizontal Pod Autoscaler
- `ingress.yaml` / `ingress-ext.yaml` - Exposição de serviços

**Pendências**: Alguns repositórios ainda usam overlay `production` ao invés de `ebb-prd`. Ver [pendencias/gitops.md](/home/marcosgomes/Projects/ebb-platform-ia/pendencias/gitops.md)

## Specification Structure

Each specification includes:

### Core Sections
- **Overview** - Purpose and responsibilities
- **Architecture** - Services, infrastructure
- **Key Services** - Detailed service descriptions
- **Infrastructure** - GCP resources, databases
- **Dependencies** - Service relationships
- **Security & Compliance** - Security requirements
- **Operations** - Monitoring, alerting, common tasks

### Usage

1. **Understand domain**: Read spec before making changes
2. **Plan changes**: Use spec to identify affected components
3. **Document changes**: Create delta spec in `/openspec/changes/`
4. **Update spec**: Update stable spec after change is complete

## Quick Links

### By Responsibility

**Customer Management**:
- [ebb-client-journey](ebb-client-journey.md) - Onboarding, KYC, compliance

**Money Movement**:
- [ebb-money-flows](ebb-money-flows.md) - Payments, Pix, reconciliation
- [ebb-treasury](ebb-treasury.md) - Treasury operations
- [ebb-fx](ebb-fx.md) - Foreign exchange

**Platform & Data**:
- [ebb-platform](ebb-platform.md) - Infrastructure, IaC, CI/CD
- [ebb-bigdata](ebb-bigdata.md) - Data pipelines, analytics

**Integration**:
- [ebb-ebury-connect](ebb-ebury-connect.md) - Global platform integration

### By Complexity

**High Complexity** (detailed specs):
- [ebb-money-flows](ebb-money-flows.md)
- [ebb-client-journey](ebb-client-journey.md)
- [ebb-platform](ebb-platform.md)

**Medium/Low Complexity** (concise specs):
- [ebb-treasury](ebb-treasury.md)
- [ebb-fx](ebb-fx.md)
- [ebb-ebury-connect](ebb-ebury-connect.md)
- [ebb-bigdata](ebb-bigdata.md)

## Contributing

### Updating Specifications

1. Read current spec
2. Make changes to domain code/infra
3. Update spec with new information
4. Commit with clear description

### Creating New Specifications

Use existing specs as templates. Include:
- Clear overview and responsibilities
- Service architecture
- Infrastructure details
- Common operational tasks
- Links to related docs

---

**Repository**: `/home/marcosgomes/Projects/Ebury-Brazil/`  
**Automation Layer**: `/home/marcosgomes/Projects/ebb-platform-ia/`
