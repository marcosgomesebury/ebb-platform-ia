# Image Pull Errors - ImagePullBackOff

Complete troubleshooting guide for container image pull failures in GKE.

## Symptoms

- Pod stuck in `ImagePullBackOff` or `ErrImagePull` status
- Events show: `Failed to pull image`, `403 Forbidden`, `unauthorized`
- Container not starting due to image issues

## Diagnostic Commands

```bash
# Check pod status
kubectl get pod <pod-name> -n <namespace>

# Get detailed error
kubectl describe pod <pod-name> -n <namespace> | grep -A 10 "Events:"

# Check image specified
kubectl get pod <pod-name> -n <namespace> \
  -o jsonpath='{.spec.containers[0].image}'
```

## Common Causes & Solutions

### 1. Workload Identity Not Configured

**Error**: `403 Forbidden` when pulling from Artifact Registry/GCR

**Check**:
```bash
# Verify service account annotation
kubectl get sa <sa-name> -n <namespace> -o yaml | grep gcp-service-account
```

**Solution**: Configure Workload Identity properly → See [workload-identity.md](workload-identity.md)

### 2. Missing Artifact Registry IAM Permissions

**Error**: `403` from `southamerica-east1-docker.pkg.dev`

**Check GCP Service Account permissions**:
```bash
gcloud projects get-iam-policy <project> \  --flatten="bindings[].members" \
  --filter="bindings.members:serviceAccount:<gcp-sa>@<project>.iam.gserviceaccount.com" \
  --format="table(bindings.role)"
```

**Solution**: Grant `roles/artifactregistry.reader`:
```bash
gcloud projects add-iam-policy-binding <project> \
  --member="serviceAccount:<gcp-sa>@<project>.iam.gserviceaccount.com" \
  --role="roles/artifactregistry.reader"
```

### 3. Image Tag Doesn't Exist

**Error**: `manifest unknown` or `not found`

**Check if image exists**:
```bash
# List Artifact Registry images
gcloud artifacts docker images list \
  southamerica-east1-docker.pkg.dev/<project>/<repository>

# Check specific tag
gcloud artifacts docker images describe \
  southamerica-east1-docker.pkg.dev/<project>/<repository>/<image>:<tag>
```

**Solution**: 
- Verify correct image path and tag
- Check CI/CD pipeline succeeded
- Update deployment with correct tag

### 4. Wrong Image Path

**Common mistakes**:
```yaml
# ❌ WRONG: Missing region
image: docker.pkg.dev/project/repo/image:tag

# ❌ WRONG: Wrong region
image: us-docker.pkg.dev/project/repo/image:tag

# ✓ CORRECT: Full path with region
image: southamerica-east1-docker.pkg.dev/project/repo/image:tag
```

### 5. NetworkPolicy Blocking Registry Access

**Error**: Timeout connecting to registry

**Check NetworkPolicy**:
```bash
kubectl get networkpolicy -n <namespace>
kubectl describe networkpolicy <policy-name> -n <namespace>
```

**Solution**: Ensure egress to Artifact Registry is allowed:
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-artifact-registry
  namespace: <namespace>
spec:
  podSelector: {}
  policyTypes:
  - Egress
  egress:
  - to:
    - ipBlock:
        cidr: 0.0.0.0/0
        except:
        - 169.254.169.254/32  # Keep metadata server separate
    ports:
    - protocol: TCP
      port: 443
```

### 6. ImagePullPolicy Issues

**Check policy**:
```bash
kubectl get pod <pod-name> -n <namespace> \
  -o jsonpath='{.spec.containers[0].imagePullPolicy}'
```

**Policies**:
- `Always`: Always pull (can cause rate limiting)
- `IfNotPresent`: Pull only if not cached (default)
- `Never`: Never pull (only use cached)

**For development**: Use `Always` to ensure latest changes  
**For production**: Use `IfNotPresent` with specific tags (not `latest`)

### 7. Rate Limiting

**Error**: `429 Too Many Requests`

**Cause**: Too many pulls in short time

**Solution**:
- Use `imagePullPolicy: IfNotPresent`
- Implement image caching strategy
- Use specific tags instead of `latest`
- Spread deployments over time

## Step-by-Step Troubleshooting

### Step 1: Get Exact Error
```bash
kubectl describe pod <pod-name> -n <namespace>
```

Look for:
- `Failed to pull image "<image>": rpc error`
- `403 Forbidden`
- `401 Unauthorized`
- `manifest unknown`
- `timeout`

### Step 2: Verify Image Path
```bash
# Get image from pod spec
IMAGE=$(kubectl get pod <pod-name> -n <namespace> \
  -o jsonpath='{.spec.containers[0].image}')

echo "Image: $IMAGE"

# Try to pull manually (from GKE node or local with gcloud auth)
docker pull $IMAGE
```

### Step 3: Check Workload Identity
```bash
# Get service account
SA=$(kubectl get pod <pod-name> -n <namespace> \
  -o jsonpath='{.spec.serviceAccountName}')

# Check annotation
kubectl get sa $SA -n <namespace> \
  -o jsonpath='{.metadata.annotations.iam\.gke\.io/gcp-service-account}'

# Check IAM binding
GCP_SA="<result-from-above>"
gcloud iam service-accounts get-iam-policy $GCP_SA
```

### Step 4: Test from Pod
Create debug pod with same Service Account:
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: debug-image-pull
  namespace: <namespace>
spec:
  serviceAccountName: <same-sa>
  containers:
  - name: debug
    image: google/cloud-sdk:alpine
    command: ["sleep", "3600"]
```

Test pull from inside:
```bash
kubectl exec -it debug-image-pull -n <namespace> -- sh

# Authenticate
gcloud auth list

# Try to pull
gcloud artifacts docker images list \
  southamerica-east1-docker.pkg.dev/<project>/<repo>
```

## Quick Fixes

### Fix 1: Update Image with Correct Tag
```bash
kubectl set image deployment/<name> \
  <container>=southamerica-east1-docker.pkg.dev/PROJECT/REPO/IMAGE:TAG \
  -n <namespace>
```

### Fix 2: Grant Artifact Registry Access
```bash
gcloud projects add-iam-policy-binding <project> \
  --member="serviceAccount:<gcp-sa>@<project>.iam.gserviceaccount.com" \
  --role="roles/artifactregistry.reader"

# Restart pods
kubectl rollout restart deployment/<name> -n <namespace>
```

### Fix 3: Fix Service Account Annotation
```bash
kubectl annotate serviceaccount <sa> \
  -n <namespace> \
  iam.gke.io/gcp-service-account=<gcp-sa>@<project>.iam.gserviceaccount.com \
  --overwrite

kubectl rollout restart deployment/<name> -n <namespace>
```

## Prevention

### ✓ Use Specific Tags
```yaml
# ❌ BAD: Unpredictable
image: company/app:latest

# ✓ GOOD: Reproducible
image: southamerica-east1-docker.pkg.dev/project/repo/app:v1.2.3-abc123
```

### ✓ Terraform Workload Identity Module
```hcl
module "workload_identity" {
  source = "../../modules/workload-identity"
  
  project_id = "ebb-client-journey-dev"
  namespace  = "ebb-temis-dev"
  sa_name    = "ebb-temis-compliance-sa"
  
  roles = [
    "roles/artifactregistry.reader",
    "roles/secretmanager.secretAccessor"
  ]
}
```

### ✓ CI/CD Image Signing
Verify image authenticity before deployment

### ✓ Monitor Pull Failures
Alert on ImagePullBackOff in production

## Checklist

✓ Image path correct (region, project, repo, image, tag)  
✓ Image exists in Artifact Registry  
✓ Service Account annotated with GCP SA  
✓ IAM binding for workloadIdentityUser exists  
✓ GCP SA has artifactregistry.reader role  
✓ NetworkPolicy allows egress to registry  
✓ Pods restarted after IAM changes  

## References

- [Workload Identity Setup](workload-identity.md)
- [Artifact Registry Documentation](https://cloud.google.com/artifact-registry/docs)
- [GKE Image Pull Authentication](https://cloud.google.com/kubernetes-engine/docs/how-to/workload-identity)
