# Delta Spec: Verify and Fix ebb-wp-pre-validation IAM Permissions

**Status**: Completed  
**Date**: 2026-03-19  
**Completed**: 2026-03-19  
**Ticket**: EPT-2023  
**Domains**: ebury-connect (ebb-wp-pre-validation)  

---

## Context

An audit of the `ebb-wp-pre-validation` service account IAM configuration in `ebb-iac-resource` revealed several gaps in permissions and IAM bindings for the **dev** environment (`ebb-ebury-connect-dev`).

The service account `ebb-wp-pre-validation` currently has:
- **1 custom role assigned** (`ebb_wp_pre_validation_general_privilege_role_dev`) — contains only Firestore (Datastore) permissions
- **1 custom role defined but NOT assigned** (`ebb_wp_pre_validation_least_privilege_role_dev`) — contains Pub/Sub and Storage permissions, applied only at topic-level IAM

### Current State Summary

| Resource | Exists in IAC? | IAM Binding to SA? | Status |
|---|---|---|---|
| **Firestore** (default) | YES | YES (via `general_privilege_role` at project level) | OK |
| **Bucket** `ebb-wp-pre-validation-process-dev` | YES | NO (no `iam_members` on bucket) | MISSING |
| **Secret Manager** `ebb-wp-pre-validation` | YES | NO (no `iam_members` on secret) | MISSING |
| **CloudSQL** `ebb-webpayments` | YES | NO (no `cloudsql.*` permissions in any role) | MISSING |
| **Topic** `ebb-pre-validation-operations-topic` | YES | YES (via `least_privilege_role` at topic level) | OK |
| **Topic** `ebb-pre-validation-exchange-rate-topic` | YES | YES (via `least_privilege_role` at topic level) | OK |
| **Topic** `ebb-pre-validation-upload-topic` | YES | NO (no `iam_members`) | MISSING |
| **Topic** `ebb-pre-validation-monitor-topic` | YES | YES (via `least_privilege_role` at topic level) | OK |
| **Topic** `ebb-pre-validation-compliance-response-topic` | YES | YES (via `least_privilege_role` at topic level) | OK |
| **Topic** `ebb-pre-validation-upload-file-topic` | YES | YES (via `least_privilege_role` at topic level) | OK |
| **Topic** `ebb-pre-validation-rectify-values-topic` | YES | YES (via `least_privilege_role` at topic level) | OK |
| **Topic** `ebb-generate-operations-results-file-topic` | YES (GCP) | NO (not in IAC) | MISSING |
| **Topic** `ebb-pre-validation-events-topic` | YES | YES (via `least_privilege_role` at topic level) | OK |
| **Topic** `ebb-pre-validation-regular-files-processed-topic` | YES | YES (via `least_privilege_role` at topic level) | OK |
| **Topic** `ebb-payment-events` | YES | NO (no `iam_members`) | MISSING |
| **Topic** `ebb-email-notifications` | YES | NO (no `iam_members`) | MISSING |

### Observations

1. **Firestore**: Access is granted via the `general_privilege_role_dev` custom role bound at project IAM level. This role includes comprehensive `datastore.*` permissions. **OK**.

2. **Cloud Storage bucket** (`ebb-wp-pre-validation-process-dev`): The bucket exists but has **no `iam_members`** block. The `least_privilege_role` includes `storage.objects.*` permissions, but this role is only applied at topic-level IAM — not at the bucket level or project level for the SA. The SA may still access the bucket if the project-level `general_privilege_role` were to include storage permissions, but **it does not**.

3. **Secret Manager** (`ebb-wp-pre-validation`): The secret exists but has **no `iam_members`** granting access to the SA. No `secretmanager.*` permissions exist in either custom role.

4. **CloudSQL** (`ebb-webpayments`): CloudSQL IAM authentication is enabled (`cloudsql.iam_authentication = on`), but **no `cloudsql.*` permissions** exist in any of the pre-validation custom roles, and no CloudSQL IAM user is defined for the SA.

5. **Pub/Sub topics with IAM**: 8 out of 12 requested topics have proper `iam_members` bindings using the `least_privilege_role`.

6. **Topics without IAM**: `ebb-pre-validation-upload-topic`, `ebb-payment-events`, and `ebb-email-notifications` exist but have **no `iam_members`** block.

7. **Topic not in IAC**: `ebb-generate-operations-results-file-topic` exists in GCP but is not managed by Terraform. Needs to be imported into IAC with IAM bindings.

---

## ADDED Requirements

### REQ-001: Secret Manager SHALL Grant Access to Service Account
**Priority**: CRITICAL  
**Rationale**: The application needs to read secrets for configuration (DB credentials, API keys, etc.)

**Scenario: Read Secret Versions**
```gherkin
GIVEN the secret "ebb-wp-pre-validation" in Secret Manager
WHEN the ebb-wp-pre-validation service account attempts to access secret versions
THEN it SHALL have the role "roles/secretmanager.secretAccessor"
  AND the IAM binding SHALL be defined in the secret's iam_members block
```

**Affected File**: `ebb-ebury-connect/dev/security/secret-manager/ebb-wp-pre-validation/terragrunt.hcl`  
**Change**: Add `iam_members` block with `roles/secretmanager.secretAccessor` for the SA.

---

### REQ-002: Cloud Storage Bucket SHALL Grant Access to Service Account
**Priority**: HIGH  
**Rationale**: The application processes files from the pre-validation bucket

**Scenario: Access Bucket Objects**
```gherkin
GIVEN the bucket "ebb-wp-pre-validation-process-dev"
WHEN the ebb-wp-pre-validation service account attempts to read/write objects
THEN it SHALL have storage.objects.{get,list,create,update} permissions
  AND the IAM binding SHALL be defined via the least_privilege_role at bucket level
```

**Affected File**: `ebb-ebury-connect/dev/cloud-storage/ebb-wp-pre-validation-process-dev/terragrunt.hcl`  
**Change**: Add dependency on SA and `least_privilege_role`, add `iam_members` block.

---

### REQ-003: CloudSQL SHALL Grant Connection Permissions to Service Account
**Priority**: HIGH  
**Rationale**: The application connects to the webpayments CloudSQL instance

**Scenario: Connect to CloudSQL via IAM Authentication**
```gherkin
GIVEN the CloudSQL instance "ebb-webpayments" with IAM authentication enabled
WHEN the ebb-wp-pre-validation service account attempts to connect
THEN it SHALL have cloudsql.instances.connect permission
  AND it SHALL have cloudsql.instances.get permission
```

**Affected Files**:
- `ebb-ebury-connect/dev/iam/roles/ebb_wp_pre_validation_general_privilege_role_dev/terragrunt.hcl` — Add `cloudsql.instances.connect`, `cloudsql.instances.get`

---

### REQ-004: Missing Pub/Sub Topics SHALL Have IAM Bindings
**Priority**: HIGH  
**Rationale**: Three existing topics lack IAM bindings for the SA

**Scenario: Publish/Subscribe to Topics**
```gherkin
GIVEN the topics "ebb-pre-validation-upload-topic", "ebb-payment-events", "ebb-email-notifications"
WHEN the ebb-wp-pre-validation service account attempts to publish or subscribe
THEN each topic SHALL have an iam_members block
  AND the binding SHALL use the least_privilege_role
```

**Affected Files**:
- `ebb-ebury-connect/dev/pub-sub/topics/ebb-pre-validation-upload-topic/terragrunt.hcl` — Add dependencies + `iam_members`
- `ebb-ebury-connect/dev/pub-sub/topics/ebb-payment-events/terragrunt.hcl` — Add dependencies + `iam_members`
- `ebb-ebury-connect/dev/pub-sub/topics/ebb-email-notifications/terragrunt.hcl` — Add dependencies + `iam_members`

---

### REQ-005: Topic ebb-generate-operations-result-file-topic SHALL Be Created
**Priority**: MEDIUM  
**Rationale**: This topic is required by the application but does not exist in IAC

**Scenario: Topic Exists and Has IAM**
```gherkin
GIVEN the application requires topic "ebb-generate-operations-results-file-topic"
WHEN the infrastructure is provisioned
THEN the topic SHALL exist in ebb-ebury-connect-dev
  AND it SHALL have an iam_members block for the pre-validation SA
  AND it SHALL have a corresponding dead-letter topic
```

**Affected Files**:
- NEW: `ebb-ebury-connect/dev/pub-sub/topics/ebb-generate-operations-results-file-topic/terragrunt.hcl`
- NEW: `ebb-ebury-connect/dev/pub-sub/topics/ebb-generate-operations-results-file-topic.dl/terragrunt.hcl`

---

## Affected Components

### Infrastructure (ebb-iac-resource)

All paths relative to `ebb-ebury-connect/dev/`:

| File | Change |
|---|---|
| `iam/roles/ebb_wp_pre_validation_general_privilege_role_dev/terragrunt.hcl` | Add `cloudsql.instances.connect`, `cloudsql.instances.get` |
| `security/secret-manager/ebb-wp-pre-validation/terragrunt.hcl` | Add SA dependency + `iam_members` with `roles/secretmanager.secretAccessor` |
| `cloud-storage/ebb-wp-pre-validation-process-dev/terragrunt.hcl` | Add SA + role dependencies + `iam_members` |
| `pub-sub/topics/ebb-pre-validation-upload-topic/terragrunt.hcl` | Upgrade module ref + add SA + role dependencies + `iam_members` |
| `pub-sub/topics/ebb-payment-events/terragrunt.hcl` | Upgrade module ref + add SA + role dependencies + `iam_members` |
| `pub-sub/topics/ebb-email-notifications/terragrunt.hcl` | Upgrade module ref + add SA + role dependencies + `iam_members` |
| `pub-sub/topics/ebb-generate-operations-results-file-topic/terragrunt.hcl` | NEW — import topic into IAC with IAM |
| `pub-sub/topics/ebb-generate-operations-results-file-topic.dl/terragrunt.hcl` | NEW — import dead-letter topic into IAC |

---

## Testing Checklist

- [x] Verify `terragrunt plan` succeeds for `iam/roles/ebb_wp_pre_validation_general_privilege_role_dev`
- [x] Verify `terragrunt plan` succeeds for `security/secret-manager/ebb-wp-pre-validation`
- [x] Verify `terragrunt plan` succeeds for `cloud-storage/ebb-wp-pre-validation-process-dev`
- [x] Verify `terragrunt plan` succeeds for `pub-sub/topics/ebb-pre-validation-upload-topic`
- [ ] Verify `terragrunt plan` succeeds for `pub-sub/topics/ebb-payment-events` (topic recreate in progress — PR #273/#274)
- [x] Verify `terragrunt plan` succeeds for `pub-sub/topics/ebb-email-notifications`
- [x] Verify `terragrunt plan` succeeds for `pub-sub/topics/ebb-generate-operations-results-file-topic`
- [ ] Apply changes and verify SA can access Secret Manager
- [ ] Apply changes and verify SA can connect to CloudSQL
- [ ] Apply changes and verify SA can read/write bucket objects
- [ ] Apply changes and verify SA can publish to all 12 topics
- [ ] Restart ebb-wp-pre-validation pods and verify application starts without errors

---

## Notes

- The `least_privilege_role_dev` already contains pubsub and storage permissions. It is applied **per-topic** via `iam_members`, not at project level. This is the correct least-privilege pattern for resource-level bindings.
- The `general_privilege_role_dev` is applied at **project level** via the SA's `project_iam_members`. This is appropriate for Firestore/Datastore (which doesn't support resource-level IAM) and for CloudSQL connection permissions.
- Topics `ebb-pre-validation-upload-topic`, `ebb-payment-events`, and `ebb-email-notifications` use an **older module version** (`v1.2.1`/`v1.2.2`) that may not support `iam_members`. They should be upgraded to `v1.4.0`.

---

## Implementation Summary

### PRs Created (ebb-iac-resource)

| PR | Title | Status |
|---|---|---|
| #260 | feat(EPT-2023): add ebb-wp-pre-validation IAM permissions | Merged |
| #262 | fix: resolve bad merge in ebb-pre-validation-upload-topic (dev/stg/prd) | Merged |
| #267 | fix(EPT-2023): remove resourcemanager.projects.list from least_privilege_role | Merged |
| #268 | fix(EPT-2023): add ebb-wp-pre-validation IAM permissions and trailing newline | Merged |
| #269 | style: add trailing blank line to ebb-payment-events (dev/stg/prd) | Merged |
| #273 | fix(EPT-2023): create ebb-payment-events topic without IAM (step 1/2) | Open |
| #274 | fix(EPT-2023): restore IAM for ebb-payment-events dev (step 2/2) | Open |

### Changes Applied (all environments: dev/stg/prd)

1. **general_privilege_role**: Added `cloudsql.instances.connect`, `cloudsql.instances.get`
2. **least_privilege_role**: Added `resourcemanager.projects.get`, `secretmanager.versions.access`
3. **Secret Manager** `ebb-wp-pre-validation`: Added IAM binding with `least_privilege_role`
4. **Cloud Storage** `ebb-wp-pre-validation-process-{env}`: Added IAM binding with `least_privilege_role`
5. **Pub/Sub** `ebb-pre-validation-upload-topic`: Upgraded v1.2.2→v1.4.0, added IAM (both pre-validation + portal-api SAs)
6. **New topics**: `ebb-payment-events`, `ebb-email-notifications`, `ebb-generate-operations-results-file-topic`, `ebb-generate-operations-results-file-topic.dl`

### Issues Encountered

- **Bad merge on main** (PR #260 + #257): upload-topic HCL was broken by interleaved dependency blocks → fixed by PR #262
- **`resourcemanager.projects.list` removed**: Not needed for the SA → removed via PR #267
- **`ebb-payment-events` topic deleted**: Topic was accidentally deleted from GCP dev; Terraform state still referenced it, causing 404 on plan. State was cleaned (`terragrunt state rm`) and topic recreation split into 2 PRs (#273 creates topic, #274 adds IAM back)
