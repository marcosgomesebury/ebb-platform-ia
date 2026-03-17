# Ebury-Brazil Repository Structure

Documentation of the business domains repository structure located at `/home/marcosgomes/Projects/Ebury-Brazil/`.

This repository contains the actual business applications, GitOps configurations, and infrastructure code, while `ebb-platform-ia` provides the automation and intelligence layer.

---

## Repository Structure

```
Ebury-Brazil/
├── ebb-client-journey/         # Customer Journey Domain
├── ebb-money-flows/            # Money Flows Domain
├── ebb-fx/                     # Foreign Exchange Domain
├── ebb-treasury/               # Treasury Domain
├── ebb-platform/               # Platform & Infrastructure
├── ebb-ebury-connect/          # Ebury Connect Integration
└── ebb-bigdata/                # Data & Analytics
```

---

## Domain: ebb-client-journey

**Purpose**: Customer onboarding, compliance, fraud detection, and risk assessment.

### Structure
```
ebb-client-journey/
├── apps/
│   ├── temis/                  # Core Temis platform - monorepo
│   └── temis-registration-config-data-keys-salesforce/
└── gitops/                     # 30 GitOps repositories
    ├── ebb-temis-bff-gitops/
    ├── ebb-temis-bureau-gitops/
    ├── ebb-temis-bureau-data-integrator-gitops/
    ├── ebb-temis-compliance-gitops/
    ├── ebb-temis-compliance-action-gitops/
    ├── ebb-temis-compliance-screening-gitops/
    ├── ebb-temis-config-gitops/
    ├── ebb-temis-digital-signature-gitops/
    ├── ebb-temis-email-sender-gitops/
    ├── ebb-temis-enrichment-gitops/
    ├── ebb-temis-expiration-date-gitops/
    ├── ebb-temis-fraud-gitops/
    ├── ebb-temis-internal-account-management-gitops/
    ├── ebb-temis-limit-gitops/
    ├── ebb-temis-mocks-v2-gitops/
    ├── ebb-temis-notification-gitops/
    ├── ebb-temis-onboarding-engine-gitops/
    ├── ebb-temis-query-gitops/
    ├── ebb-temis-registration-gitops/
    ├── ebb-temis-restrictive-lists-gitops/
    ├── ebb-temis-risk-gitops/
    ├── ebb-temis-salesforce-adapter-gitops/
    ├── ebb-temis-tas-integrator-gitops/
    ├── ebb-temis-tree-adapter-gitops/
    └── temis-*-gitops/          # 6 legacy repos
```

**GitOps**: 30 repositórios (24 ebb-temis-*, 6 temis-* legados)  
**Padrão**: Kustomize com base + overlays (ebb-dev, staging-platform, ebb-prd)  
**Multi-deployment**: Muitos serviços têm 3 deployments (sync, sync-ext, async)

### Key Services
- **Temis BFF**: Backend for Frontend orchestration
- **Bureau Services**: Credit bureau integrations
- **Compliance Suite**: KYC, screening, sanctions
- **Fraud Detection**: Real-time fraud analysis
- **Onboarding Engine**: Customer onboarding workflow
- **Risk Assessment**: Risk scoring and evaluation

**Specification**: [specs/ebb-client-journey.md](specs/ebb-client-journey.md)

---

## Domain: ebb-money-flows

**Purpose**: Money movement, payment processing, Pix, Bacen integration, and reconciliation.

### Structure
```
ebb-money-flows/
├── apps/
│   ├── ebb-account/            # Account management
│   ├── ebb-bexs-bacen-adapter/
│   ├── ebb-bexs-compliance/
│   ├── ebb-bexs-forex-documentation/
│   ├── ebb-bexs-notification/
│   ├── ebb-bexs-sta/
│   ├── ebb-bexs-statement/
│   ├── ebb-conciliacao/        # Reconciliation service
│   ├── ebb-jd-certificate-hsm/
│   ├── ebb-legal-proceedings/
│   ├── ebb-pix-dict/
│   └── ebb-pix-spi/            # Pix SPI integration
└── gitops/                     # 5 GitOps repositories
    ├── ebb-account-gitops/
    ├── ebb-jd-certificate-hsm-gitops/
    ├── ebb-legal-proceedings-gitops/
    ├── ebb-pix-dict-gitops/
    └── ebb-pix-spi-gitops/
```

**GitOps**: 5 repositórios  
**Padrão**: Kustomize com base + overlays  
**Pendências**: Padronização de overlays (`production` → `ebb-prd`)

### Key Services
- **Bexs Adapters**: Integration with Bexs platform
- **Pix SPI**: Brazilian instant payment system
- **Reconciliation**: Transaction reconciliation (ebb-conciliacao)
- **Bacen Adapter**: Central Bank of Brazil integration
- **Statement Services**: Account statement generation
- **Compliance**: AML/CFT compliance checks

**Specification**: [specs/ebb-money-flows.md](specs/ebb-money-flows.md)

---

## Domain: ebb-fx

**Purpose**: Foreign exchange rate provisioning and trading operations.

### Structure
```
ebb-fx/
└── forex-provider/             # FX rate provider integration
```

### Key Services
- **Forex Provider**: Real-time FX rate integration

**Specification**: [specs/ebb-fx.md](specs/ebb-fx.md)

---

## Domain: ebb-treasury

**Purpose**: Treasury operations and liquidity management.

### Structure
```
ebb-treasury/
├── ebb-treasury-configs-gitops/
├── ebb-tree-compliance/
├── ebb-tree-consumer/
├── ebb-tree-producer/
└── ebb-tree-provider-mock/
```

### Key Services
- **Tree Compliance**: Treasury compliance checks
- **Tree Producer/Consumer**: Treasury event streaming
- **Treasury Configs**: Configuration management

**Specification**: [specs/ebb-treasury.md](specs/ebb-treasury.md)

---

## Domain: ebb-platform

**Purpose**: Infrastructure, IaC, CI/CD, and engineering tooling.

### Structure
```
ebb-platform/
├── cicd/                       # CI/CD pipelines and templates
├── ebury-blueprints/           # Project templates and blueprints
├── engineering/                # Engineering tools and utilities
├── iac/                        # Infrastructure as Code
│   ├── ebb-iac-resource/       # ~19 Terraform/Terragrunt projects
│   ├── ebb-gke-shared/
│   ├── ebb-iac-network/
│   ├── ebb-iac-iam/
│   └── ... (15+ more IaC projects)
├── modules/                    # Reusable Terraform modules
├── templates/                  # Service and deployment templates
└── tools/                      # DevOps and automation tools
```

### Key Components
- **IaC (Infrastructure as Code)**: Terraform/Terragrunt for GCP resources
- **CI/CD**: Jenkins, GitHub Actions, ArgoCD configurations
- **Blueprints**: Project scaffolding and templates
- **Modules**: Reusable infrastructure modules
- **Tools**: Engineering automation and utilities

**Specification**: [specs/ebb-platform.md](specs/ebb-platform.md)

---

## Domain: ebb-ebury-connect

**Purpose**: Integration with Ebury global platform (webpayments, partners, merchants).

### Structure
```
ebb-ebury-connect/
├── apps/                       # Application source code
└── gitops/                     # 17 GitOps repositories
    ├── ebb-wp-core-gitops/
    ├── ebb-wp-data-gitops/
    ├── ebb-wp-documentation-gitops/
    ├── ebb-wp-file-converter-gitops/
    ├── ebb-wp-file-processor-gitops/
    ├── ebb-wp-hedges-gitops/
    ├── ebb-wp-limit-gitops/
    ├── ebb-wp-mocks-gitops/
    ├── ebb-wp-notification-adp-gitops/
    ├── ebb-wp-pre-validation-gitops/
    ├── ebb-wp-query-gitops/
    ├── ebb-wp-quotes-gitops/
    ├── ebb-wp-uploads-gitops/
    ├── ebb-partners-settings-gitops/
    ├── ebb-proxy-merchants-gitops/
    ├── ebb-external-api-documentation-gitops/
    └── ebb-wp-core-tests/
```

**GitOps**: 17 repositórios (13 webpayments, 4 platform integration)  
**Webpayments (ebb-wp-*)**: Payment capture, processing, routing, and integration

**Specification**: [specs/ebb-ebury-connect.md](specs/ebb-ebury-connect.md)

---

## Domain: ebb-bigdata

**Purpose**: Data pipelines, ETL, and analytics.

### Structure
```
ebb-bigdata/
├── ebb-airflow-dags/           # Airflow DAG definitions
└── helm_apache_airflow/        # Helm charts for Airflow deployment
```

**Deployment**: Usa Helm charts ao invés de GitOps tradicional  
**DAGs**: Sincronizados via Git sync do Airflow

**Specification**: [specs/ebb-bigdata.md](specs/ebb-bigdata.md)

---

## Cross-Domain Patterns

### Apps vs GitOps

Most domains follow this structure:
- **`apps/`**: Source code repositories for applications
- **`gitops/`**: GitOps repositories with Kubernetes manifests and Kustomize overlays

### GitOps Repository Count

**Total**: 53 repositórios GitOps

| Domain | GitOps Repos | Deployment Tool |
|--------|--------------|----------------|
| ebb-client-journey | 30 | Kustomize |
| ebb-ebury-connect | 17 | Kustomize |
| ebb-money-flows | 5 | Kustomize |
| ebb-treasury | 1 | Kustomize |
| ebb-platform | - | Terraform/IaC |
| ebb-fx | - | (app-managed) |
| ebb-bigdata | - | Helm charts |

### GitOps Overlay Structure

Standard GitOps repository structure:
```
<service>-gitops/
├── base/                       # Base Kubernetes manifests
│   ├── deployment.yaml
│   ├── service.yaml
│   ├── ingress.yaml
│   └── pod-monitor.yaml
├── overlays/
│   ├── ebb-dev/                # Development environment
│   │   ├── namespace.yaml
│   │   ├── configmap.yaml
│   │   ├── service-account.yaml
│   │   ├── external-secret.yaml
│   │   └── hpa.yaml
│   ├── staging-platform/       # Staging environment
│   └── ebb-prd/                # Production environment
└── application/
    └── kustomization.yaml
```

**Nota**: Alguns repositórios ainda usam overlay `production` ao invés de `ebb-prd` (padronização em andamento).

### Naming Conventions

- **Apps**: `ebb-<service-name>/`
- **GitOps**: `ebb-<service-name>-gitops/`
- **IaC**: `ebb-iac-<resource-type>/`

---

## Integration with ebb-platform-ia

**ebb-platform-ia provides**:
- OpenSpec specifications for each domain
- Skills for automation (RDP, SSH, MySQL, K8s debug)
- Subagents for complex orchestration tasks
- Documentation and guides
- Task tracking and change management

**Ebury-Brazil contains**:
- Actual application source code
- GitOps configurations for deployments
- Infrastructure as Code (Terraform/Terragrunt)
- CI/CD pipeline definitions

---

## Working with Both Repositories

### Typical Workflow

1. **Understand requirements** - Read OpenSpec in `ebb-platform-ia/openspec/`
2. **Make changes** - Edit code in `Ebury-Brazil/<domain>/`
3. **Document changes** - Create delta spec in `ebb-platform-ia/openspec/changes/`
4. **Test locally** - Use skills from `ebb-platform-ia/skills/`
5. **Deploy via GitOps** - Update manifests in `Ebury-Brazil/<domain>/gitops/`
6. **Archive** - Move completed spec to `ebb-platform-ia/openspec/archive/`

### Accessing Ebury-Brazil

```bash
# Navigate to business domains
cd /home/marcosgomes/Projects/Ebury-Brazil/

# Example: Work on money flows
cd ebb-money-flows/apps/ebb-pix-spi/

# Example: Update GitOps for client journey
cd ../ebb-client-journey/gitops/ebb-temis-bff-gitops/
```

---

## References

- [OpenSpec Methodology](../README.md#-openspec-methodology)
- [Domain Specifications](specs/)
- [Current Tasks](tasks.md)

---

**Last Updated**: March 16, 2026  
**Repository**: /home/marcosgomes/Projects/Ebury-Brazil/
