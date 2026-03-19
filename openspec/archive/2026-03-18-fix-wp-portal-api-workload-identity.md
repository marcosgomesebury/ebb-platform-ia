# Delta Spec: Fix wp-portal-api Workload Identity Authentication

**Status**: Completed  
**Date**: 2026-03-18  
**Completed**: 2026-03-19  
**Ticket**: EPT-1890  
**Domains**: ebb-ebury-connect, ebb-platform (IAC)

---

## Context

O pod `wp-portal-api` no ambiente **ebb-dev** falha ao fazer upload para o bucket `ebb-wp-converter-process-dev` com o erro:

```
GCE metadata 'instance/service-accounts/default/token?scopes=...' not defined
```

Isso ocorre porque o pod tenta obter credenciais via **metadata server legado do GCE**, mas o cluster GKE usa **Workload Identity**, que bloqueia esse endpoint. O Workload Identity exige que o Kubernetes ServiceAccount (KSA) esteja corretamente vinculado ao Google Service Account (GSA) via annotation e IAM binding.

### Root Cause Analysis

Foram identificados **3 mismatches** entre o gitops (`ebb-wp-portal-api-gitops`) e o Terraform/Terragrunt (`ebb-iac-resource`):

| Atributo | Gitops (overlay ebb-dev) | Terragrunt (WI binding) | Match? |
|---|---|---|---|
| **Namespace** | `portal` | `ebb-wp-portal-api` | **NO** |
| **KSA name** | `wp-portal-api-sa` | `ebb-wp-portal-api-api` | **NO** |
| **GSA annotation** | `wp-portal-api@...` | `ebb-wp-portal-api@...` | **NO** |

O chain de autenticação do Workload Identity requer match exato em todos os 3 atributos:

```
KSA (annotation: GSA) → WI binding (namespace/KSA → GSA) → GSA (IAM no bucket)
```

### Arquivos Envolvidos

**Gitops** (`ebb-wp-portal-api-gitops`, overlay ebb-dev):
- `overlays/ebb-dev/sa.yaml` — ServiceAccount com nome, namespace e annotation incorretos
- `overlays/ebb-dev/kustomization.yaml` — Namespace override e serviceAccountName no Deployment

**Terragrunt** (`ebb-iac-resource`):
- `ebb-ebury-connect/dev/iam/service-accounts/ebb-wp-portal-api/terragrunt.hcl` — WI binding com `[ebb-wp-portal-api/ebb-wp-portal-api]`

---

## Decision: Corrigir o Gitops para alinhar com o Terragrunt

O Terragrunt já está aplicado e o GSA `ebb-wp-portal-api` existe com o binding para `ebb-wp-portal-api/ebb-wp-portal-api`. A correção envolve alinhar gitops (KSA name + annotation) e Terragrunt (namespace no WI binding) para convergir no namespace `portal` com KSA `ebb-wp-portal-api-api`.

---

## MODIFIED Requirements

### REQ-001: MODIFIED — KSA SHALL match Workload Identity binding

O Kubernetes ServiceAccount no overlay ebb-dev MUST alinhar com o binding de Workload Identity definido no Terragrunt.

#### Scenario: ServiceAccount definition matches WI binding
- GIVEN o WI binding `ebb-ebury-connect-dev.svc.id.goog[portal/ebb-wp-portal-api-api]`
- WHEN o overlay ebb-dev é aplicado
- THEN o KSA MUST ter:
  - `metadata.name`: `ebb-wp-portal-api-api`
  - `metadata.namespace`: `portal`
  - `annotations.iam.gke.io/gcp-service-account`: `ebb-wp-portal-api@ebb-ebury-connect-dev.iam.gserviceaccount.com`

#### Scenario: Deployment references correct ServiceAccount
- GIVEN o Deployment `wp-portal-api` no overlay ebb-dev
- WHEN o pod é criado
- THEN `spec.template.spec.serviceAccountName` MUST ser `ebb-wp-portal-api-api`

### REQ-002: MODIFIED — Pod SHALL authenticate via Workload Identity (não metadata server)

#### Scenario: Upload to Cloud Storage succeeds
- GIVEN um pod `wp-portal-api` com Workload Identity configurado
- WHEN o pod faz upload para `ebb-wp-converter-process-dev`
- THEN o upload MUST completar com sucesso
- AND a autenticação MUST usar Workload Identity (não GCE metadata server)

#### Scenario: Base kustomization removes legacy volume mount
- GIVEN o overlay ebb-dev
- WHEN aplicado sobre o base
- THEN o volume mount `/var/gcp/` com secret `wp-core` MUST ser removido
  - (O overlay ebb-dev já faz isso via `op: remove` dos volumes/volumeMounts)
- AND a aplicação MUST usar ADC (Application Default Credentials) do Workload Identity

---

## Affected Components

### 1. `ebb-wp-portal-api-gitops/overlays/ebb-dev/sa.yaml`

**Atual** (incorreto):
```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: wp-portal-api-sa
  namespace: portal
  annotations:
    iam.gke.io/gcp-service-account: wp-portal-api@ebb-ebury-connect-dev.iam.gserviceaccount.com
```

**Proposto**:
```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: ebb-wp-portal-api-api
  namespace: portal
  annotations:
    iam.gke.io/gcp-service-account: ebb-wp-portal-api@ebb-ebury-connect-dev.iam.gserviceaccount.com
```

### 2. `ebb-wp-portal-api-gitops/overlays/ebb-dev/kustomization.yaml`

**Mudanças**:
- `namespace: portal` — sem alteração (mantém)
- Patch `serviceAccountName`: `wp-portal-api-sa` → `ebb-wp-portal-api-api`

### 3. `ebb-iac-resource/ebb-ebury-connect/dev/iam/service-accounts/ebb-wp-portal-api/terragrunt.hcl`

**Alterar WI binding**:
- DE: `ebb-ebury-connect-dev.svc.id.goog[ebb-wp-portal-api/ebb-wp-portal-api]`
- PARA: `ebb-ebury-connect-dev.svc.id.goog[portal/ebb-wp-portal-api-api]`

### 4. `ebb-iac-resource/ebb-ebury-connect/dev/cloud-storage/ebb-wp-converter-process-dev/terragrunt.hcl`

**Sem alteração** — IAM no bucket já referencia a GSA correta `ebb-wp-portal-api@...`.

---

## Risk Assessment

| Risco | Severidade | Mitigação |
|---|---|---|
| KSA rename pode causar restart dos pods | Baixa | Deploy normal via ArgoCD |
| WI binding change precisa de apply antes do deploy | Média | Executar `terragrunt apply` antes do merge no gitops |

**Decisão**: Manter namespace `portal` e usar KSA `ebb-wp-portal-api-api`. Menor superfície de mudança — sem impacto em DNS/comunicação entre serviços.

---

## Implementation Plan

### Step 1: Fix Gitops — `overlays/ebb-dev/sa.yaml`
- Corrigir `name`: `wp-portal-api-sa` → `ebb-wp-portal-api-api`
- Manter `namespace: portal` (namespace atual do deploy)
- Corrigir `annotation`: `wp-portal-api@...` → `ebb-wp-portal-api@...`

### Step 2: Fix Gitops — `overlays/ebb-dev/kustomization.yaml`
- Corrigir patch `serviceAccountName`: `wp-portal-api-sa` → `ebb-wp-portal-api-api`

### Step 3: Fix Terragrunt — WI binding
- Alterar binding de `[ebb-wp-portal-api/ebb-wp-portal-api]` para `[portal/ebb-wp-portal-api-api]`
- Executar `terragrunt apply`

### Step 4: Validar
- Verificar se o pod reinicia e autentica via Workload Identity
- Testar upload para bucket `ebb-wp-converter-process-dev`

---

## Testing Checklist

- [ ] KSA `ebb-wp-portal-api-api` existe no namespace `portal` com annotation correta
- [ ] Deployment referencia `serviceAccountName: ebb-wp-portal-api-api`
- [ ] WI binding está como `portal/ebb-wp-portal-api-api`
- [ ] Pod inicia sem erro de metadata server
- [ ] Upload para `ebb-wp-converter-process-dev` funciona
- [ ] Comunicação entre serviços não foi afetada (PORTAL_API_ADDRESS resolve)
