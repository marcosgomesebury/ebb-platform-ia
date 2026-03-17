# Workload Identity Troubleshooting

Complete guide for diagnosing and fixing Workload Identity issues in GKE.

## What is Workload Identity?

Workload Identity allows Kubernetes Service Accounts to impersonate Google Cloud Service Accounts, enabling secure access to GCP services without managing keys.

## Common Symptoms

- `403 Forbidden` errors when accessing GCP APIs
- `401 Unauthorized` when calling Cloud SQL, Secret Manager, Storage
- Logs show: `Error: could not generate access token`
- Application fails to authenticate to GCP services

## Prerequisites Check

### 1. Workload Identity Enabled on Cluster

```bash
gcloud container clusters describe CLUSTER_NAME \
  --region=southamerica-east1 \
  --format="value(workloadIdentityConfig.workloadPool)"
```

Expected output: `PROJECT_ID.svc.id.goog`

If empty, Workload Identity is not enabled.

### 2. Node Pool Configuration

```bash
gcloud container node-pools describe NODE_POOL \
  --cluster=CLUSTER_NAME \
  --region=southamerica-east1 \
  --format="value(config.workloadMetadataConfig.mode)"
```

Expected output: `GKE_METADATA`

## Diagnostic Steps

### Step 1: Verify Service Account Annotation

**Check pod's Service Account**:
```bash
kubectl get pod <pod-name> -n <namespace> \
  -o jsonpath='{.spec.serviceAccountName}'
```

**Check annotation on Kubernetes SA**:
```bash
kubectl get serviceaccount <sa-name> -n <namespace> -o yaml
```

Expected annotation:
```yaml
metadata:
  annotations:
    iam.gke.io/gcp-service-account: <gcp-sa>@<project>.iam.gserviceaccount.com
```

**Missing annotation?** → Apply it:
```bash
kubectl annotate serviceaccount <k8s-sa> \
  -n <namespace> \
  iam.gke.io/gcp-service-account=<gcp-sa>@<project>.iam.gserviceaccount.com
```

### Step 2: Verify IAM Binding

**Check if binding exists**:
```bash
gcloud iam service-accounts get-iam-policy \
  <gcp-sa>@<project>.iam.gserviceaccount.com \
  --format=json | jq '.bindings[] | select(.role == "roles/iam.workloadIdentityUser")'
```

Expected member:
```json
{
  "role": "roles/iam.workloadIdentityUser",
  "members": [
    "serviceAccount:<project>.svc.id.goog[<namespace>/<k8s-sa>]"
  ]
}
```

**Missing binding?** → Create it:
```bash
gcloud iam service-accounts add-iam-policy-binding \
  <gcp-sa>@<project>.iam.gserviceaccount.com \
  --role=roles/iam.workloadIdentityUser \
  --member="serviceAccount:<project>.svc.id.goog[<namespace>/<k8s-sa>]"
```

### Step 3: Verify GCP Service Account Permissions

Check if GCP SA has required roles for the service:

**For Artifact Registry**:
```bash
gcloud projects get-iam-policy <project> \
  --flatten="bindings[].members" \
  --filter="bindings.members:serviceAccount:<gcp-sa>@<project>.iam.gserviceaccount.com" \
  --format="table(bindings.role)"
```

Required: `roles/artifactregistry.reader`

**For Secret Manager**:
Required: `roles/secretmanager.secretAccessor`

**For Cloud SQL**:
Required: `roles/cloudsql.client`

**Add missing role**:
```bash
gcloud projects add-iam-policy-binding <project> \
  --member="serviceAccount:<gcp-sa>@<project>.iam.gserviceaccount.com" \
  --role="roles/REQUIRED_ROLE"
```

### Step 4: Check NetworkPolicy for Metadata Server

Workload Identity requires access to GCP metadata server (169.254.169.254).

**Check if NetworkPolicy exists**:
```bash
kubectl get networkpolicy -n <namespace>
```

**If NetworkPolicy exists, verify egress to metadata server**:
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-metadata-server
  namespace: <namespace>
spec:
  podSelector: {}
  policyTypes:
  - Egress
  egress:
  - to:
    - ipBlock:
        cidr: 169.254.169.254/32
    ports:
    - protocol: TCP
      port: 80
```

**Test metadata server access from pod**:
```bash
kubectl exec -it <pod-name> -n <namespace> -- \
  curl -H "Metadata-Flavor: Google" \
  http://169.254.169.254/computeMetadata/v1/instance/service-accounts/default/token
```

Expected: JSON with access token  
Error: NetworkPolicy is blocking

### Step 5: Restart Deployment

After configuration changes:
```bash
kubectl rollout restart deployment/<deployment-name> -n <namespace>
```

Wait for new pods:
```bash
kubectl rollout status deployment/<deployment-name> -n <namespace>
```

## Complete Example: Setting Up Workload Identity

**Scenario**: Service `ebb-temis-compliance` needs to access Secret Manager.

### 1. Create GCP Service Account (Terraform preferred)
```bash
gcloud iam service-accounts create ebb-temis-compliance-sa \
  --display-name="Temis Compliance Service Account" \
  --project=ebb-client-journey-dev
```

### 2. Grant GCP Permissions
```bash
# Secret Manager access
gcloud projects add-iam-policy-binding ebb-client-journey-dev \
  --member="serviceAccount:ebb-temis-compliance-sa@ebb-client-journey-dev.iam.gserviceaccount.com" \
  --role="roles/secretmanager.secretAccessor"
```

### 3. Create Kubernetes Service Account
```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: ebb-temis-compliance-sa
  namespace: ebb-temis-dev
  annotations:
    iam.gke.io/gcp-service-account: ebb-temis-compliance-sa@ebb-client-journey-dev.iam.gserviceaccount.com
```

### 4. IAM Binding
```bash
gcloud iam service-accounts add-iam-policy-binding \
  ebb-temis-compliance-sa@ebb-client-journey-dev.iam.gserviceaccount.com \
  --role=roles/iam.workloadIdentityUser \
  --member="serviceAccount:ebb-client-journey-dev.svc.id.goog[ebb-temis-dev/ebb-temis-compliance-sa]"
```

### 5. Update Deployment
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ebb-temis-compliance
  namespace: ebb-temis-dev
spec:
  template:
    spec:
      serviceAccountName: ebb-temis-compliance-sa  # Add this
      containers:
      - name: app
        image: gcr.io/PROJECT/app:tag
```

### 6. Verify
```bash
# Check pod has correct SA
kubectl get pod <pod-name> -n ebb-temis-dev \
  -o jsonpath='{.spec.serviceAccountName}'

# Test from inside pod
kubectl exec -it <pod-name> -n ebb-temis-dev -- \
  gcloud auth list
```

Expected: Shows `ebb-temis-compliance-sa@ebb-client-journey-dev.iam.gserviceaccount.com`

## Common Mistakes

### ❌ Wrong Format in IAM Binding
```bash
# WRONG: Using namespace/sa without project prefix
--member="serviceAccount:ebb-temis-dev/ebb-temis-compliance-sa"

# CORRECT: Full format
--member="serviceAccount:ebb-client-journey-dev.svc.id.goog[ebb-temis-dev/ebb-temis-compliance-sa]"
```

### ❌ Service Account Not in Deployment
```yaml
# WRONG: Missing serviceAccountName
spec:
  template:
    spec:
      containers: [...]

# CORRECT: Explicit SA
spec:
  template:
    spec:
      serviceAccountName: ebb-temis-compliance-sa
      containers: [...]
```

### ❌ NetworkPolicy Blocks Metadata Server
```yaml
# WRONG: No egress to 169.254.169.254
egress:
- to:
  - podSelector: {}

# CORRECT: Allow metadata server
egress:
- to:
  - podSelector: {}
- to:
  - ipBlock:
      cidr: 169.254.169.254/32
```

### ❌ Forgot to Restart Pods
After changing annotation/binding, **always restart**:
```bash
kubectl rollout restart deployment/<name> -n <namespace>
```

## Quick Checklist

✓ Workload Identity enabled on cluster  
✓ Node pool has GKE_METADATA  
✓ Kubernetes SA has annotation  
✓ IAM binding created (workloadIdentityUser)  
✓ GCP SA has required permissions  
✓ NetworkPolicy allows metadata server  
✓ Deployment uses serviceAccountName  
✓ Pods restarted after changes  

## Testing

### Test Script
```bash
#!/bin/bash
POD_NAME="<pod-name>"
NAMESPACE="<namespace>"
GCP_SA="<gcp-sa>@<project>.iam.gserviceaccount.com"

echo "1. Checking K8s Service Account..."
kubectl get pod $POD_NAME -n $NAMESPACE -o jsonpath='{.spec.serviceAccountName}'

echo "\n2. Checking annotation..."
kubectl get sa $(kubectl get pod $POD_NAME -n $NAMESPACE -o jsonpath='{.spec.serviceAccountName}') \
  -n $NAMESPACE -o jsonpath='{.metadata.annotations.iam\.gke\.io/gcp-service-account}'

echo "\n3. Testing auth from pod..."
kubectl exec -it $POD_NAME -n $NAMESPACE -- gcloud auth list

echo "\n4. Testing API call..."
kubectl exec -it $POD_NAME -n $NAMESPACE -- \
  gcloud projects list --limit=1
```

## References

- [GKE Workload Identity Documentation](https://cloud.google.com/kubernetes-engine/docs/how-to/workload-identity)
- [IAM Roles for GCP Services](https://cloud.google.com/iam/docs/understanding-roles)
- [Terraform Module: Workload Identity](../../../platform/modules/workload-identity)
