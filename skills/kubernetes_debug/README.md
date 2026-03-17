# Skill: Kubernetes Debug Helper

Diagnostica problemas em pods Kubernetes, extraindo logs, eventos e sugerindo soluções.

## Uso

```bash
# Via argumentos
python main.py <pod_name> [namespace]

# Via variáveis de ambiente
K8S_POD_NAME=ebb-account K8S_NAMESPACE=core python main.py

# Listar todos os pods
python main.py
```

## Variáveis de ambiente
- `K8S_NAMESPACE`: Namespace do pod (padrão: core)
- `K8S_POD_NAME`: Nome do pod a diagnosticar

## Funcionalidades
- ✓ Status do pod
- ✓ Descrição completa (kubectl describe)
- ✓ Últimos 50 logs
- ✓ Eventos recentes
- ✓ Análise automática de erros comuns:
  - ImagePullBackOff
  - CrashLoopBackOff
  - Pending
  - Workload Identity
  - Permissões (403)

## Exemplos

```bash
# Diagnosticar pod específico
python main.py ebb-account core

# Diagnosticar com namespace padrão
python main.py ebb-jd-certificate-hsm

# Ver todos os pods do namespace
python main.py
```

## Requisitos
- kubectl configurado e autenticado
- Acesso ao cluster GKE
