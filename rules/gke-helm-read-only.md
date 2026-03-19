# Rule: GKE and Helm Read-Only Commands

- **Nome da Regra:** gke-helm-read-only
- **Descrição:** Never run mutating commands on GKE (kubectl apply, delete, patch, edit, create, replace, scale, rollout, etc.) or Helm (install, upgrade, delete, uninstall, rollback). Only read-only commands are allowed: get, describe, list, show, logs, top, diff, status.
- **Condições de disparo:**
  - Ao executar qualquer comando kubectl
  - Ao executar qualquer comando helm
  - Ao sugerir comandos Kubernetes ou Helm ao usuário
- **Ações automáticas:**
  - Verificar se o comando é read-only antes de executar
  - Se for um comando mutante (apply, delete, create, patch, edit, replace, scale, rollout restart, etc.), recusar a execução
  - Se for um comando Helm mutante (install, upgrade, delete, uninstall, rollback), recusar a execução
  - Alertar o usuário que apenas comandos de leitura são permitidos
- **Comandos permitidos (kubectl):**
  - `kubectl get`
  - `kubectl describe`
  - `kubectl logs`
  - `kubectl top`
  - `kubectl diff`
  - `kubectl api-resources`
  - `kubectl explain`
  - `kubectl config view`
  - `kubectl config get-contexts`
  - `kubectl cluster-info`
  - `kubectl version`
  - `kubectl auth can-i`
- **Comandos permitidos (helm):**
  - `helm list`
  - `helm status`
  - `helm get`
  - `helm show`
  - `helm search`
  - `helm history`
  - `helm template`
- **Comandos proibidos (kubectl):**
  - `kubectl apply`
  - `kubectl delete`
  - `kubectl create`
  - `kubectl patch`
  - `kubectl edit`
  - `kubectl replace`
  - `kubectl scale`
  - `kubectl rollout restart`
  - `kubectl rollout undo`
  - `kubectl set`
  - `kubectl label`
  - `kubectl annotate`
  - `kubectl taint`
  - `kubectl cordon` / `kubectl uncordon`
  - `kubectl drain`
  - `kubectl exec` (com comandos destrutivos)
- **Comandos proibidos (helm):**
  - `helm install`
  - `helm upgrade`
  - `helm delete`
  - `helm uninstall`
  - `helm rollback`
- **Exemplo de uso:**
  ```bash
  # Allowed — read-only commands:
  kubectl get pods -n my-namespace
  kubectl describe deployment my-app -n my-namespace
  kubectl logs my-pod -n my-namespace
  helm list -n my-namespace
  helm status my-release -n my-namespace
  helm show values my-chart

  # Forbidden — never do this:
  kubectl apply -f deployment.yaml
  kubectl delete pod my-pod
  helm install my-release my-chart
  helm upgrade my-release my-chart
  helm delete my-release
  ```
