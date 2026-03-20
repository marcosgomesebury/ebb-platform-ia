# Delta Spec: ebb-account CloudSQL Migration to ebb-conciliacao-dev

**Status**: In Progress  
**Date**: 2026-03-19  
**Ticket**: EPT-2023  
**Domains**: moneyflows (ebb-account)  

---

## Context

The ebb-account application was crashing on the `ebb-money-flows-dev` GKE cluster with:
```
googleapi: Error 404: The Cloud SQL instance does not exist (ebb-money-flows-dev:southamerica-east1:account-dev)
```

The Cloud SQL instance `account-dev` did not exist. The application needs to connect to `ebb-account-dev` on the `ebb-conciliacao-dev` Cloud SQL instance.

---

## Changes Applied

### 1. GitOps — DB_HOST Update
**PR**: https://github.com/Ebury-Brazil/ebb-account-gitops/pull/40  
**File**: `overlays/ebb-dev/kustomization.yaml`

| Variable | Before | After |
|---|---|---|
| `DB_HOST` | `cloudsql-mysql(ebb-money-flows-dev:southamerica-east1:account-dev)` | `cloudsql-mysql(ebb-money-flows-dev:southamerica-east1:ebb-account-dev)` |
| `DB_HOST_REPLICA` | same | same |

### 2. CloudSQL — IAM Service Account User
Created Cloud SQL IAM user on `ebb-account-dev` instance:
```bash
gcloud sql users create ebb-account@ebb-money-flows-dev.iam.gserviceaccount.com \
  --instance=ebb-account-dev \
  --type=CLOUD_IAM_SERVICE_ACCOUNT \
  --project=ebb-money-flows-dev
```

Granted MySQL privileges:
```sql
GRANT ALL PRIVILEGES ON account.* TO 'ebb-account'@'%';
GRANT ALL PRIVILEGES ON account_balance.* TO 'ebb-account'@'%';
GRANT ALL PRIVILEGES ON account_report.* TO 'ebb-account'@'%';
```

### 3. IAM — PubSub Cross-Project Permissions
**PR**: https://github.com/Ebury-Brazil/ebb-iac-resource/pull/283  

The ebb-account SA needs PubSub access to `bexs-digitalfx-dev` for the `digitalfx-notification` topic.

**Applied manually (and codified in Terraform):**
- `roles/pubsub.publisher` on `bexs-digitalfx-dev`
- `roles/pubsub.viewer` on `bexs-digitalfx-dev`

**Terraform changes:**
- `ebb_account_general_privilege_role_dev`: added PubSub permissions (`topics.get/list/publish`, `subscriptions.consume/get/list`)
- `ebb-account` service account: added `external_project_iam_members` for `bexs-digitalfx-dev`

### 4. Secret Manager
- Updated `ebb-account-db-passwd` secret (version 2) in `ebb-money-flows-dev`

---

## Pending Issues

### SQS Queue Missing
The application panics trying to access AWS SQS queue `ebb-payout-transfer-event` (with prefix `devgcp-`):
```
panic: failed trying to get swift queue: error getting queue name ebb-payout-transfer-event
AWS.SimpleQueueService.NonExistentQueue
```

**Action needed**: Create SQS queue `devgcp-ebb-payout-transfer-event` in AWS `sa-east-1`, or evaluate if this subscriber is needed in dev.

---

## Infrastructure Summary

| Resource | Instance/Value | Project |
|---|---|---|
| Cloud SQL Instance | `ebb-account-dev` (on `ebb-conciliacao-dev`) | `ebb-money-flows-dev` |
| Private IP | `10.23.249.7` | `ebb-money-flows-dev` |
| Databases | `account`, `account_balance`, `account_report` | |
| MySQL User | `ebb-account` (CLOUD_IAM_SERVICE_ACCOUNT) | |
| K8s Namespace | `core` | |
| K8s SA | `ebb-account` | |
| GCP SA | `ebb-account@ebb-money-flows-dev.iam.gserviceaccount.com` | |
