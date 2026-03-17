# Domain Specification: ebb-platform

**Status**: Active  
**Last Updated**: 2026-03-16  
**Repository**: `/home/marcosgomes/Projects/Ebury-Brazil/ebb-platform/`

---

## Overview

Platform domain provides infrastructure, IaC (Infrastructure as Code), CI/CD pipelines, engineering tools, and foundational services for all Ebury Brazil operations.

### Core Responsibilities
- Infrastructure provisioning and management (Terraform/Terragrunt)
- CI/CD pipeline management
- Kubernetes cluster management (GKE)
- Networking and security
- IAM and service account management
- Monitoring and observability infrastructure
- Developer tooling and templates

---

## Architecture

### Structure

```
ebb-platform/
├── cicd/               # CI/CD pipelines and templates
├── ebury-blueprints/   # Project scaffolding and templates
├── engineering/        # Engineering tools and utilities
├── iac/                # Infrastructure as Code (19 projects)
├── modules/            # Reusable Terraform modules
├── templates/          # Service and deployment templates
└── tools/              # DevOps automation tools
```

---

## Infrastructure as Code (iac/)

### Projects Overview

| Project | Purpose | Stack |
|---------|---------|-------|
| **ebb-iac-resource** | Main resource definitions | Terraform + Terragrunt |
| **ebb-gke-shared** | Shared GKE configurations | Terraform |
| **ebb-iac-network** | VPC, subnets, firewall rules | Terraform |
| **ebb-iac-iam** | IAM roles and service accounts | Terraform |
| **ebb-iac-management** | Management infrastructure | Terraform |
| **ebb-platform-groundzero-buckets** | Foundational GCS buckets | Terraform |
| **ebb-provisioning** | Resource provisioning automation | Terraform |

Additional 12+ projects for specific domains and environments.

### ebb-iac-resource Structure

Main IaC repository with resources organized by domain and environment:

```
ebb-iac-resource/
├── ebb-money-flows/
│   ├── dev/
│   │   ├── iam/
│   │   │   ├── service-accounts/
│   │   │   │   ├── ebb-account/
│   │   │   │   ├── ebb-jd-certificate-hsm/
│   │   │   │   └── ...
│   │   │   └── roles/
│   │   │       ├── ebb_account_general_privilege_role_dev/
│   │   │       ├── ebb_jd_certificate_hsm_least_privilege_role_dev/
│   │   │       └── ...
│   │   ├── cloudsql/
│   │   ├── pubsub/
│   │   └── ...
│   ├── stg/
│   └── prd/
├── ebb-client-journey/
├── ebb-ebury-connect/
└── ...
```

### Terragrunt Configuration

- **DRY principle**: Reusable modules, environment-specific overlays
- **State management**: GCS backend per environment
- **Dependencies**: Explicit dependency graphs between resources
- **Variables**: Environment-specific tfvars

### Naming Conventions

- **Projects**: `ebb-<domain>-<env>` (e.g., `ebb-money-flows-dev`)
- **Service Accounts**: `ebb-<service>@<project>.iam.gserviceaccount.com`
- **IAM Roles**: `ebb_<service>_<privilege_level>_role_<env>`
- **Resources**: Prefix with `ebb-` for all managed resources

---

## CI/CD (cicd/)

### Pipeline Types

1. **Application Pipelines**
   - Build & test application code
   - Build Docker images
   - Push to GCR/Artifact Registry
   - Update GitOps manifests

2. **Infrastructure Pipelines**
   - Terraform plan & apply
   - Compliance checks
   - Security scanning
   - State file management

3. **GitOps Pipelines**
   - Validate Kubernetes manifests
   - Kustomize build verification
   - ArgoCD sync triggers

### Tools
- **Jenkins** - Legacy CI/CD
- **GitHub Actions** - Modern CI/CD
- **ArgoCD** - GitOps deployment
- **Cloud Build** - GCP-native builds

### Deployment Flow

```
Code Push → CI Build → Tests → Image Build → Registry Push → 
              ↓
GitOps Update → ArgoCD Detects → Apply to ebb-dev → 
              ↓
Manual Approval → Apply to ebb-stg →
              ↓
Manual Approval → Apply to ebb-prd
```

---

## GKE Management

### Clusters

| Cluster | Environment | Purpose |
|---------|-------------|---------|
| `ebb-money-flows-dev` | Development | Money flows services |
| `ebb-client-journey-dev` | Development | Client journey services |
| `ebb-shared-dev` | Development | Shared/platform services |
| Similar for `stg` and `prd` | | |

### Standard Configuration
- **Region**: `southamerica-east1`
- **Node pools**: Separated by workload type
- **Workload Identity**: Enabled
- **Network Policy**: Calico
- **Monitoring**: Cloud Monitoring + Prometheus
- **Logging**: Cloud Logging

### Add-ons
- ArgoCD for GitOps
- Cert-manager for TLS
- External DNS
- Ingress NGINX

---

## Networking (ebb-iac-network)

### VPC Structure
- Separate VPCs per environment (dev/stg/prd)
- VPC peering between environments (controlled)
- Shared VPC for common services

### Subnets
- **GKE pod subnets** - /16 or larger
- **GKE service subnets** - /20
- **Cloud SQL private IPs** - VPC peering
- **VPN/Interconnect** - Hybrid connectivity

### Firewall Rules
- Default deny all
- Explicit allow rules per service
- Ingress/egress controls
- NetworkPolicy within clusters

### Cloud NAT
- Outbound internet access for pods
- Static IPs for allowlisting

---

## IAM & Service Accounts

### Service Account Patterns

1. **Application Service Accounts**
   - One per application/service
   - Workload Identity binding to K8s SA  
   - Principle of least privilege

2. **Role Types**
   - `least_privilege_role` - Minimal permissions
   - `general_privilege_role` - Standard operational permissions
   - `admin_role` - Administrative access (rare)

3. **Common Permissions**
   - Storage: For GCR, artifacts, backups
   - Cloud SQL: For database access
   - PubSub: For messaging
   - Secret Manager: For secrets
   - Logging/Monitoring: For observability

### Example Configuration

```hcl
# Service Account: ebb-account
resource "google_service_account" "ebb_account" {
  account_id   = "ebb-account"
  display_name = "EBB Account Service"
  project      = "ebb-money-flows-dev"
}

# Workload Identity Binding
resource "google_service_account_iam_binding" "ebb_account_wi" {
  service_account_id = google_service_account.ebb_account.name
  role               = "roles/iam.workloadIdentityUser"
  members = [
    "serviceAccount:ebb-money-flows-dev.svc.id.goog[core/ebb-account]"
  ]
}
```

---

## Modules (modules/)

Reusable Terraform modules for common patterns:

- **gke-cluster** - Standard GKE setup
- **service-account** - SA with WI binding
- **cloudsql** - Database provisioning
- **pubsub** - Topics and subscriptions
- **iam-role** - Custom role creation
- **network-security** - Firewall rules, policies

---

## Ebury Blueprints (ebury-blueprints/)

Project templates for new services:

- **go-service-template** - Go microservice skeleton
- **python-service-template** - Python service skeleton
- **gitops-template** - GitOps repository structure
- **terraform-module-template** - Reusable module structure

### Usage

```bash
# Create new service from blueprint
./ebury-blueprints/create-service.sh \
  --name my-service \
  --domain money-flows \
  --template go-service-template
```

---

## Engineering Tools (engineering/)

Developer productivity tools:

- **k8s-debug-helpers** - Scripts for K8s troubleshooting
- **terraform-helpers** - Terraform automation scripts
- **gitops-validators** - Manifest validation tools
- **migration-scripts** - Data/infrastructure migration utilities

---

## Operations

### Infrastructure Changes

```bash
# Navigate to resource
cd ebb-iac-resource/ebb-money-flows/dev/iam/service-accounts/ebb-account/

# Plan changes
terragrunt plan

# Apply after review
terragrunt apply

# Always update GitOps manifests if SA changes
```

### Adding New Service

1. Create service account in IaC
2. Create IAM roles/bindings
3. Create GitOps repository from template
4. Configure CI/CD pipeline
5. Deploy to ebb-dev first

### Disaster Recovery

- **Terraform state**: Backed up in GCS (versioned)
- **Cluster backup**: Velero for workload backup
- **Database backup**: Automated Cloud SQL backups
- **Configuration**: GitOps ensures reproducibility

---

## Security

### Principles
- Infrastructure as Code (no manual changes)
- Immutable infrastructure
- Least privilege access
- Secrets in Secret Manager (never in Git)
- Audit logging for all infrastructure changes

### Compliance
- CIS GKE Benchmark
- PCI DSS (where applicable)
- LGPD data residency
- ISO 27001 controls

---

## Common Tasks

### Add IAM Permission to Service Account

```bash
cd ebb-iac-resource/ebb-money-flows/dev/iam/roles/ebb_account_general_privilege_role_dev/

# Edit terragrunt.hcl:
permissions = [
  "cloudsql.instances.get",
  "cloudsql.instances.connect",
  # Add new permission
  "storage.objects.get",
]

terragrunt plan
terragrunt apply
```

### Debug Workload Identity Issue

```bash
# Check K8s service account annotation
kubectl get sa ebb-account -n core -o yaml

# Check IAM binding
gcloud iam service-accounts get-iam-policy ebb-account@ebb-money-flows-dev.iam.gserviceaccount.com

# Test from pod
kubectl run -it test --image=google/cloud-sdk:slim --serviceaccount=ebb-account -n core -- bash
gcloud auth list
```

### Roll Out New GKE Cluster Version

```bash
cd ebb-iac-resource/ebb-shared/dev/gke/

# Update version in terragrunt.hcl
terragrunt plan
# Apply in maintenance window
terragrunt apply

# Update node pools (rolling update)
```

---

## References

- [Terraform Best Practices](https://www.terraform-best-practices.com/)
- [GKE Hardening Guide](https://cloud.google.com/kubernetes-engine/docs/how-to/hardening-your-cluster)
- [Ebury-Brazil Structure](../EBURY_BRAZIL_STRUCTURE.md)
- Change History: [changes/](../changes/) | [archive/](../archive/)

---

**Domain Owner**: Platform Team  
**On-call**: Platform rotation  
**Slack**: #platform-infrastructure
