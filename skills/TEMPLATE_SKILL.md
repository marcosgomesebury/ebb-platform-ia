# Skill: Kubernetes Debug Helper

- **Nome do Skill:** kubernetes_debug
- **Descrição:** Automação para diagnosticar problemas em pods Kubernetes (logs, describe, events, restart)
- **Dependências:**
  - kubectl configurado
  - Acesso ao cluster GKE
  - python-dotenv==1.2.2
  - kubernetes==29.0.0
- **Variáveis de ambiente:**
  - K8S_CLUSTER_NAME (ex: ebb-money-flows-dev)
  - K8S_NAMESPACE (ex: core)
  - K8S_POD_NAME (opcional, ou detecta automaticamente)
  - GCP_PROJECT (ex: ebb-money-flows-dev)
- **Estrutura do Skill:**
  ```
  skills/kubernetes_debug/
  ├── main.py
  ├── requirements.txt
  ├── .env.example
  ├── README.md
  └── tests/
  ```
- **Exemplo de uso:**
  ```python
  # Diagnosticar pod com erro
  python main.py --pod ebb-account --namespace core
  
  # Output:
  # - Status do pod
  # - Últimos 50 logs
  # - Eventos recentes
  # - Recursos (CPU/Memory)
  # - Sugestões de correção
  ```
- **Ações automáticas:**
  1. kubectl get pod -n namespace
  2. kubectl describe pod
  3. kubectl logs --tail=50
  4. kubectl get events --field-selector involvedObject.name=pod
  5. Análise automática de erros comuns:
     - ImagePullBackOff → verificar permissões GCR
     - CrashLoopBackOff → analisar logs de startup
     - Pending → verificar recursos do cluster
