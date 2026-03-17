# Delta Spec: Fix Workload Identity and GCR Access for Money Flows Services

**Status**: In Progress  
**Date**: 2026-03-15  
**Ticket**: EPT-1890  
**Domains**: moneyflows (ebb-account, ebb-jd-certificate-hsm)  

---

## Context

Two critical issues were identified in the money-flows services running on GKE:

1. **ebb-account**: Application failing with "failed to create default credentials" error
2. **ebb-jd-certificate-hsm**: Pod failing with ImagePullBackOff when pulling from gcr.io

Root cause analysis revealed:
- NetworkPolicy `deny-all` blocking metadata server access (169.254.169.254:80) required by Workload Identity
- Incorrect Cloud SQL project references in GitOps overlays
- Missing GCR access permissions for service accounts

---

## ADDED Requirements

### REQ-001: NetworkPolicy SHALL Allow Metadata Server Access
**Priority**: CRITICAL  
**Rationale**: Workload Identity depends on metadata server access for authentication

**Scenario: Workload Identity Authentication**
```gherkin
GIVEN a pod with Workload Identity configuration
  AND serviceAccountName is properly annotated with iam.gke.io/gcp-service-account
WHEN the application attempts to create default credentials
THEN it SHALL successfully access metadata server at 169.254.169.254:80
  AND it SHALL authenticate using the bound GCP service account
```

---

### REQ-002: GCR Image Pull SHALL Use Storage Permissions
**Priority**: HIGH  
**Rationale**: Service accounts need storage permissions to pull images from GCR

**Scenario: Pull Image from GCR**
```gherkin
GIVEN a service account with Workload Identity configured
  AND the service account has storage.objects.get permission
  AND the service account has storage.objects.list permission
WHEN a pod attempts to pull an image from gcr.io/bexs-platform/*
THEN the image pull SHALL succeed
  AND the pod SHALL start successfully
```

**Implementation Notes**:
- Add permissions to `least_privilege_role`, not directly to service account
- Apply to all environments (dev, stg, prd)

---

### REQ-003: Cloud SQL IAM Roles SHALL Include Connection Permissions
**Priority**: HIGH  
**Rationale**: Service accounts need proper permissions to connect to Cloud SQL instances

**Scenario: Connect to Cloud SQL Instance**
```gherkin
GIVEN a service account with Workload Identity configured
  AND the service account has cloudsql.instances.get permission
  AND the service account has cloudsql.instances.connect permission
  AND the service account has cloudsql.instances.executeSql permission
WHEN the application attempts to connect to Cloud SQL
THEN the connection SHALL succeed
  AND database operations SHALL be permitted
```

---

## MODIFIED Requirements

### REQ-004: GitOps Overlays SHALL Use Correct GCP Project References
**Priority**: HIGH  
**What Changed**: Project IDs in Cloud SQL connection strings were referencing legacy project names

**Scenario: Cloud SQL Connection String Format (ebb-dev)**
```gherkin
GIVEN the ebb-dev overlay configuration
WHEN defining DB_HOST environment variable
THEN it SHALL use format "cloudsql-mysql(ebb-money-flows-dev:southamerica-east1:account-dev)"
  AND it SHALL NOT use "cloudsql-mysql(account-develop:southamerica-east1:account-dev)"
```

**Scenario: Cloud SQL Connection String Format (ebb-stg)**
```gherkin
GIVEN the ebb-stg overlay configuration
WHEN defining DB_HOST environment variable
THEN it SHALL use format "cloudsql-mysql(ebb-money-flows-staging:southamerica-east1:account-stg)"
  AND it SHALL NOT use "cloudsql-mysql(account-develop:southamerica-east1:account-dev)"
```

**Scenario: Cloud SQL Connection String Format (ebb-prd)**
```gherkin
GIVEN the ebb-prd overlay configuration
WHEN defining DB_HOST environment variable
THEN it SHALL use format "cloudsql-mysql(ebb-money-flows-prod:southamerica-east1:account-prd)"
  AND it SHALL NOT use "cloudsql-mysql(account-production:southamerica-east1:account-prd)"
```

---

## Affected Components

### Infrastructure (Terraform/Terragrunt)

**ebb-account (dev environment)**:
- File: `/platform/iac/ebb-iac-resource/ebb-money-flows/dev/iam/roles/ebb_account_general_privilege_role_dev/terragrunt.hcl`
- Added permissions: `cloudsql.instances.connect`, `cloudsql.instances.get`

**ebb-jd-certificate-hsm (all environments)**:
- Files: `/platform/iac/ebb-iac-resource/ebb-money-flows/{dev,stg,prd}/iam/roles/ebb_jd_certificate_hsm_least_privilege_role_{dev,stg,prd}/terragrunt.hcl`
- Added permissions: `storage.objects.get`, `storage.objects.list`
- Files: `/platform/iac/ebb-iac-resource/ebb-money-flows/{dev,stg,prd}/iam/service-accounts/ebb-jd-certificate-hsm/terragrunt.hcl`
- Added binding: `least_privilege_role`

### GitOps (Kustomize)

**ebb-account**:
- File: `/moneyflows/gitops/ebb-account-gitops/overlays/ebb-dev/kustomization.yaml`
- Changed: `DB_HOST` project from `account-develop` to `ebb-money-flows-dev`
- File: `/moneyflows/gitops/ebb-account-gitops/overlays/ebb-stg/kustomization.yaml`
- Changed: `DB_HOST` project from `account-develop` to `ebb-money-flows-staging`
- Changed: Instance name from `account-dev` to `account-stg`
- File: `/moneyflows/gitops/ebb-account-gitops/overlays/ebb-prd/kustomization.yaml`
- Changed: `DB_HOST` project from `account-production` to `ebb-money-flows-prod`

---

## Testing Checklist

- [x] Verified Workload Identity binding exists: `gcloud iam service-accounts get-iam-policy`
- [x] Verified K8s service account has correct annotation
- [x] Verified pod uses correct serviceAccountName
- [x] Verified nodepool has GKE_METADATA enabled
- [x] Tested metadata server access from pod: `curl http://169.254.169.254/computeMetadata/v1/instance/service-accounts/default/email`
- [ ] Apply Terraform changes for IAM roles
- [ ] Restart pods to pick up new permissions
- [ ] Verify ebb-account connects to Cloud SQL successfully
- [x] Verify ebb-jd-certificate-hsm pulls image from GCR successfully ✅
- [ ] **NEW**: Resolve SQL Server connection timeout (10.46.0.55) - Pending discussion with Rodrigo

---

## Known Issues

### Issue: ebb-jd-certificate-hsm SQL Server Connection Timeout
**Status**: Identified, Pending Action  
**Error**: `Timeout expired. The timeout period elapsed prior to obtaining a connection from the pool`  
**Details**:
- Database: `DB_JD-HSM`
- Server: `10.46.0.55:1433` (SQL Server, not Cloud SQL)
- Connection string stored in secret: `ebb-jd-certificate-hsm` (key: `JDPI_ConnectionStrings__JDPI_CERTIFICATE`)

**Possible Causes**:
1. NetworkPolicy blocking egress to 10.46.0.55:1433
2. SQL Server unreachable from GKE cluster
3. VPC/Firewall rules preventing connectivity
4. Wrong IP address or database unavailable

**Action Required**: Discuss with Rodrigo about SQL Server accessibility from GKE dev cluster

---

## Pull Requests

- **GitOps**: https://github.com/Ebury-Brazil/ebb-account-gitops/pull/34 (EPT-1890)
- **IAC**: (pending)

---

## Lessons Learned

1. **NetworkPolicies and Workload Identity**: Always ensure NetworkPolicies allow egress to 169.254.169.254:80 for Workload Identity to function
2. **Permission Placement**: Add permissions to custom roles (least_privilege_role), not directly as service account bindings
3. **GCP Project Consistency**: Always verify GitOps configurations reference the same GCP project as Terraform IAC
4. **Storage Permissions for GCR**: Service accounts need `storage.objects.get` and `storage.objects.list` to pull from GCR
5. **Testing Strategy**: Use test pods with same serviceAccountName to validate Workload Identity before debugging application issues
