---
name: kubernetes_debug
description: Diagnose Kubernetes pod issues in GKE clusters - ImagePullBackOff, CrashLoopBackOff, Workload Identity failures, NetworkPolicy blocks, pending pods, resource issues. Analyzes logs, events, deployments, and provides root cause with solutions. Use when user says "pod not starting", "image pull error", "workload identity issue", "check k8s logs", "debug deployment", "pod pending", "crashloop". Supports GCP projects ebb-money-flows-dev, ebb-client-journey-dev, ebb-platform-dev. Do NOT use for kubectl commands execution (use terminal) or infrastructure changes (use iac skill).
license: CC-BY-4.0
metadata:
  author: Marcos Gomes
  version: 1.0.0
  requires:
    - kubectl
    - gcloud
  gcp_projects:
    - ebb-money-flows-dev
    - ebb-client-journey-dev
    - ebb-platform-dev
---

# Kubernetes Debug Skill

Automated diagnosis and troubleshooting for Kubernetes pods in GKE clusters.

## When to Use

Use this skill when:
- Pod is stuck in **ImagePullBackOff** (cannot pull container image)
- Pod has **CrashLoopBackOff** (application keeps crashing)
- **Workload Identity** authentication failures (403/401 GCP API errors)
- **NetworkPolicy** blocking traffic (timeout to services/metadata server)
- Pod stuck in **Pending** state (scheduling issues)
- Need to analyze pod **logs and events**
- Deployment rollout issues

**Do NOT use for:**
- Executing kubectl commands directly (use terminal)
- Making infrastructure changes (use iac skill)
- Application-level debugging (use app-debug skill)
- Helm chart modifications (use helm skill)

## Prerequisites

- `kubectl` configured with GKE cluster access
- `gcloud` authenticated to GCP projects
- Access to clusters: ebb-money-flows-dev, ebb-client-journey-dev, ebb-platform-dev
- GKE region: southamerica-east1

## Workflow

### 1. Identify the Issue

Gather basic information:
```bash
kubectl get pods -n <namespace>
kubectl describe pod <pod-name> -n <namespace>
kubectl logs <pod-name> -n <namespace> --tail=50
```

### 2. Analyze Error Pattern

Common patterns automatically detected:

#### ImagePullBackOff
**Symptoms**: Cannot pull container image from Artifact Registry

**Common causes**:
- Workload Identity misconfiguration
- Artifact Registry permissions missing
- Image doesn't exist or wrong tag
- NetworkPolicy blocking registry access

**Solution**: See [references/image-pull-errors.md](references/image-pull-errors.md)

#### CrashLoopBackOff
**Symptoms**: Container starts but immediately crashes

**Common causes**:
- Application errors (check logs)
- Missing environment variables
- Secrets not mounted
- Health check failures
- Port binding issues

**Solution**: See [references/crashloop-debug.md](references/crashloop-debug.md)

#### Workload Identity Issues
**Symptoms**: 403/401 errors when accessing GCP services (Cloud SQL, Secret Manager, etc.)

**Common causes**:
- Service Account annotation missing/wrong
- IAM binding not configured
- NetworkPolicy blocking metadata server (169.254.169.254)
- Wrong service account email

**Solution**: See [references/workload-identity.md](references/workload-identity.md)

#### NetworkPolicy Blocks
**Symptoms**: Timeout connecting to services, metadata server, or external APIs

**Common causes**:
- NetworkPolicy too restrictive
- Missing egress rules for metadata server
- DNS resolution blocked
- Cross-namespace communication blocked

**Solution**: See [references/network-policies.md](references/network-policies.md)

#### Pending Pods
**Symptoms**: Pod stuck in Pending, not scheduled

**Common causes**:
- Insufficient cluster resources (CPU/memory)
- Node selector doesn't match any node
- Taints/tolerations mismatch
- PersistentVolumeClaim not bound

**Solution**: Check node capacity, adjust resource requests, or scale cluster

### 3. Diagnostic Commands

**Pod status and details**:
```bash
kubectl get pod <pod-name> -n <namespace> -o yaml
kubectl describe pod <pod-name> -n <namespace>
```

**Logs**:
```bash
# Recent logs
kubectl logs <pod-name> -n <namespace> --tail=100

# Previous container (if crashed)
kubectl logs <pod-name> -n <namespace> --previous

# Follow logs
kubectl logs <pod-name> -n <namespace> -f
```

**Events**:
```bash
# All namespace events
kubectl get events -n <namespace> --sort-by='.lastTimestamp'

# Specific pod events
kubectl get events -n <namespace> --field-selector involvedObject.name=<pod-name>
```

**Deployment and ReplicaSet**:
```bash
kubectl get deployment <deployment-name> -n <namespace> -o yaml
kubectl get replicaset -n <namespace>
kubectl describe deployment <deployment-name> -n <namespace>
```

### 4. Root Cause Analysis

For each issue type, provide:

1. **Issue Identified**: Brief description
2. **Root Cause**: Detailed explanation with evidence (logs/events)
3. **Solution**: Step-by-step fix
4. **Prevention**: How to avoid in future
5. **Related Issues**: Links to common related problems

Example output:
```markdown
## Diagnosis: ImagePullBackOff

**Issue Identified**: Pod ebb-temis-compliance-7d8f9b5c-x9z2k cannot pull image

**Root Cause**: 
- Workload Identity not configured correctly
- Service Account missing IAM binding to Artifact Registry
- Evidence: Event shows "403 Forbidden" from gcr.io

**Solution**:
1. Verify Service Account annotation in pod:
   ```yaml
   spec:
     serviceAccountName: ebb-temis-compliance-sa
   ```

2. Check IAM binding:
   ```bash
   gcloud projects add-iam-policy-binding PROJECT_ID \
     --member="serviceAccount:ebb-temis-compliance-sa@PROJECT_ID.iam.gserviceaccount.com" \
     --role="roles/artifactregistry.reader"
   ```

3. Restart deployment:
   ```bash
   kubectl rollout restart deployment/ebb-temis-compliance -n ebb-temis-dev
   ```

**Prevention**:
- Use Terraform module for Workload Identity setup
- Document required IAM roles in service README
- Add startup probe to detect auth issues early

**Related**: See [Workload Identity Troubleshooting](references/workload-identity.md)
```

## Common Scenarios

### Scenario 1: New Service Won't Start
```
Problem: Just deployed new service, pods in ImagePullBackOff
Check:
1. Workload Identity configuration
2. Artifact Registry permissions
3. Image tag exists
4. NetworkPolicy allows registry access
```

### Scenario 2: Service Crashed After Deploy
```
Problem: Pods in CrashLoopBackOff after config change
Check:
1. Recent logs (kubectl logs <pod> --previous)
2. Environment variables changes
3. Secret/ConfigMap updates
4. Health check endpoints
```

### Scenario 3: Can't Connect to Cloud SQL
```
Problem: Application logs show connection timeout to Cloud SQL
Check:
1. Workload Identity for Cloud SQL
2. NetworkPolicy egress rules
3. Cloud SQL Proxy sidecar configuration
4. Connection string format
```

## Automated Analysis

When diagnosing, automatically check:

✓ Pod phase and conditions  
✓ Container statuses  
✓ Recent events (last 10 minutes)  
✓ Last 50 log lines  
✓ Service Account annotations  
✓ Resource requests vs limits  
✓ NetworkPolicy presence  
✓ Deployment replica count  

## Tips

- **Start broad**: Use `kubectl get pods -n <namespace>` to see overall health
- **Check events first**: Often reveal the immediate cause
- **Compare working pods**: Find differences in config
- **Use --previous**: Get logs from crashed containers
- **Check parent resources**: Deployment, ReplicaSet might have issues
- **Verify IAM**: Most GCP integration issues are IAM-related
- **Test NetworkPolicy**: Create debug pod to test connectivity

## Reference Documentation

For detailed troubleshooting guides:

- [Image Pull Errors](references/image-pull-errors.md) - ImagePullBackOff resolution
- [CrashLoop Debugging](references/crashloop-debug.md) - Application crash diagnosis
- [Workload Identity](references/workload-identity.md) - WI setup and troubleshooting
- [Network Policies](references/network-policies.md) - NetworkPolicy debugging
- [Resource Issues](references/resource-issues.md) - CPU/memory problems

## Output Format

Always provide diagnosis in this structure:

```markdown
## 🔍 Diagnosis: [Issue Type]

**Pod**: <pod-name>
**Namespace**: <namespace>
**Status**: <current-status>

### Issue Identified
[Brief description]

### Root Cause
[Detailed explanation with evidence]

### Solution
[Step-by-step fix with commands]

### Prevention
[How to avoid this in future]

### Related
[Links to reference docs]
```
