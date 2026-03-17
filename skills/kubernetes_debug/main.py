import os
import subprocess
import sys
from dotenv import load_dotenv

load_dotenv()

def run_command(cmd):
    """Executa comando e retorna output."""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
        return result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return -1, "", "Command timed out"

def get_pod_status(namespace, pod_name=None):
    """Obtém status do pod."""
    if pod_name:
        cmd = f"kubectl get pod {pod_name} -n {namespace} -o wide"
    else:
        cmd = f"kubectl get pods -n {namespace}"
    
    returncode, stdout, stderr = run_command(cmd)
    if returncode == 0:
        print(f"\n{'='*60}\nPOD STATUS\n{'='*60}")
        print(stdout)
    else:
        print(f"Error getting pod status: {stderr}")
    return returncode == 0

def describe_pod(namespace, pod_name):
    """Descreve o pod."""
    cmd = f"kubectl describe pod {pod_name} -n {namespace}"
    returncode, stdout, stderr = run_command(cmd)
    
    if returncode == 0:
        print(f"\n{'='*60}\nPOD DESCRIPTION\n{'='*60}")
        print(stdout)
    else:
        print(f"Error describing pod: {stderr}")
    return returncode == 0

def get_pod_logs(namespace, pod_name, tail=50):
    """Obtém logs do pod."""
    cmd = f"kubectl logs {pod_name} -n {namespace} --tail={tail}"
    returncode, stdout, stderr = run_command(cmd)
    
    if returncode == 0:
        print(f"\n{'='*60}\nPOD LOGS (last {tail} lines)\n{'='*60}")
        print(stdout)
    else:
        print(f"Error getting logs: {stderr}")
    return returncode == 0

def get_pod_events(namespace, pod_name):
    """Obtém eventos relacionados ao pod."""
    cmd = f"kubectl get events -n {namespace} --field-selector involvedObject.name={pod_name} --sort-by='.lastTimestamp'"
    returncode, stdout, stderr = run_command(cmd)
    
    if returncode == 0:
        print(f"\n{'='*60}\nPOD EVENTS\n{'='*60}")
        print(stdout)
    else:
        print(f"Error getting events: {stderr}")
    return returncode == 0

def analyze_common_errors(logs, stderr):
    """Analisa erros comuns e sugere soluções."""
    print(f"\n{'='*60}\nERROR ANALYSIS & RECOMMENDATIONS\n{'='*60}")
    
    suggestions = []
    
    if "ImagePullBackOff" in logs or "ImagePullBackOff" in stderr:
        suggestions.append("❌ ImagePullBackOff detected:")
        suggestions.append("   - Check GCR permissions (storage.objects.get, storage.objects.list)")
        suggestions.append("   - Verify service account has roles/artifactregistry.reader or storage permissions")
        suggestions.append("   - Check image name/tag is correct")
    
    if "CrashLoopBackOff" in logs or "CrashLoopBackOff" in stderr:
        suggestions.append("❌ CrashLoopBackOff detected:")
        suggestions.append("   - Application is crashing on startup")
        suggestions.append("   - Check application logs above for errors")
        suggestions.append("   - Verify environment variables and secrets")
        suggestions.append("   - Check liveness/readiness probes configuration")
    
    if "Pending" in logs or "Pending" in stderr:
        suggestions.append("❌ Pod Pending:")
        suggestions.append("   - Insufficient resources in cluster")
        suggestions.append("   - Check node availability")
        suggestions.append("   - Review resource requests/limits")
    
    if "failed to create default credentials" in logs:
        suggestions.append("❌ Workload Identity error:")
        suggestions.append("   - Check serviceAccountName annotation in pod spec")
        suggestions.append("   - Verify iam.gke.io/gcp-service-account annotation")
        suggestions.append("   - Check IAM binding for workloadIdentityUser")
        suggestions.append("   - Verify NetworkPolicy allows metadata server access")
    
    if "403" in logs or "permission" in logs.lower():
        suggestions.append("❌ Permission error detected:")
        suggestions.append("   - Review IAM roles for service account")
        suggestions.append("   - Check if required permissions are granted")
        suggestions.append("   - Verify resource names/projects are correct")
    
    if suggestions:
        for suggestion in suggestions:
            print(suggestion)
    else:
        print("✓ No common errors detected in logs")

def main():
    namespace = os.getenv("K8S_NAMESPACE", "core")
    pod_name = os.getenv("K8S_POD_NAME")
    
    if len(sys.argv) > 1:
        pod_name = sys.argv[1]
    
    if len(sys.argv) > 2:
        namespace = sys.argv[2]
    
    if not pod_name:
        print("Usage: python main.py <pod_name> [namespace]")
        print(f"Or set K8S_POD_NAME in .env file")
        print(f"\nListing all pods in namespace '{namespace}':")
        get_pod_status(namespace)
        sys.exit(1)
    
    print(f"\n🔍 Kubernetes Debug Helper")
    print(f"Pod: {pod_name}")
    print(f"Namespace: {namespace}\n")
    
    # 1. Get pod status
    get_pod_status(namespace, pod_name)
    
    # 2. Describe pod
    describe_pod(namespace, pod_name)
    
    # 3. Get logs
    _, logs, _ = run_command(f"kubectl logs {pod_name} -n {namespace} --tail=50")
    get_pod_logs(namespace, pod_name)
    
    # 4. Get events
    _, events, _ = run_command(f"kubectl get events -n {namespace} --field-selector involvedObject.name={pod_name}")
    get_pod_events(namespace, pod_name)
    
    # 5. Analyze errors
    analyze_common_errors(logs + events, "")
    
    print(f"\n{'='*60}")
    print("✓ Diagnostic complete!")
    print(f"{'='*60}\n")

if __name__ == "__main__":
    main()
