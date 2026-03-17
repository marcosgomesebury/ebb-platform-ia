# Padrões do tech-leads-club/agent-skills

Análise e extração de padrões do repositório [tech-leads-club/agent-skills](https://github.com/tech-leads-club/agent-skills) para aplicar em `ebb-platform-ia`.

---

## Estrutura de Diretórios

### Estrutura Deles
```
packages/skills-catalog/skills/
├── (architecture)/          ← Categorias entre parênteses
├── (cloud)/
├── (development)/
│   ├── jira-assistant/
│   │   ├── SKILL.md        ← Instruções principais
│   │   └── README.md       ← Documentação pública
│   ├── tlc-spec-driven/
│   │   ├── SKILL.md
│   │   ├── README.md
│   │   └── references/     ← Docs on-demand (carregadas quando necessário)
│   │       ├── brownfield-mapping.md
│   │       ├── design.md
│   │       ├── discuss.md
│   │       ├── implement.md
│   │       ├── quick-mode.md
│   │       ├── tasks.md
│   │       └── validate.md
│   └── coding-guidelines/
│       └── SKILL.md        ← Skill simples (só arquivo principal)
├── (security)/
├── (tooling)/
└── _category.json          ← Metadata das categorias
```

### Nossa Estrutura Atual
```
ebb-platform-ia/
├── skills/
│   ├── rdp_connect/
│   │   ├── main.py
│   │   ├── requirements.txt
│   │   └── .env.example
│   ├── ssh_connect/
│   ├── mysql_connect/
│   └── kubernetes_debug/
├── subagents/
│   └── database_diagnostic_agent.py
└── docs/
    └── RULES_SKILLS_MCPS_SUBAGENTS.md
```

---

## YAML Frontmatter (Metadata)

### Padrão Completo (tlc-spec-driven)
```yaml
---
name: tlc-spec-driven
description: Project and feature planning with 4 adaptive phases - Specify, Design, Tasks, Execute. Auto-sizes depth by complexity. Creates atomic tasks with verification criteria, atomic git commits, requirement traceability, and persistent memory across sessions. Stack-agnostic. Use when (1) Starting new projects (initialize vision, goals, roadmap), (2) Working with existing codebases (map stack, architecture, conventions), (3) Planning features (requirements, design, task breakdown)...
license: CC-BY-4.0
metadata:
  author: Felipe Rodrigues - github.com/felipfr
  version: 2.0.0
---
```

### Padrão Simples (jira-assistant)
```yaml
---
description: Manage Jira issues via Atlassian MCP — search, create, update, transition status, and handle sprint tasks. Auto-detects workspace configuration. Use when user says "create a Jira ticket", "update my sprint", "check Jira status"...
name: jira-assistant
---
```

### Campos Importantes

| Campo | Obrigatório | Propósito |
|-------|-------------|-----------|
| `name` | ✓ | Identificador único da skill |
| `description` | ✓ | Descrição detalhada incluindo "Use when..." triggers |
| `license` | Recomendado | CC-BY-4.0 para skills próprias |
| `metadata.author` | Recomendado | Autoria e GitHub |
| `metadata.version` | Recomendado | Versionamento semântico |
| `tags` | Opcional | Tags para categorização |

**Nota importante sobre `description`**: 
- Deve ser **longo e detalhado**
- Incluir triggers explícitos ("Use when...")
- Incluir exclusões ("Do NOT use for...")
- Aparecer em uma única linha (quebras são espaços)

---

## References/ (Progressive Disclosure)

### Conceito
**Referencias são carregadas sob demanda** pelo agente quando precisa de mais contexto sobre um tópico específico.

### Quando Usar
- **Skill simples** (≤100 linhas): Apenas `SKILL.md`
- **Skill média** (100-300 linhas): `SKILL.md` + referências inline
- **Skill complexa** (>300 linhas): `SKILL.md` (overview) + `references/` (detalhes)

### Exemplo: tlc-spec-driven
```
SKILL.md (11KB) ← Overview do workflow, estrutura de pastas, comandos principais
references/
  ├── brownfield-mapping.md  (9KB)  ← Mapear codebases existentes
  ├── design.md              (5.5KB) ← Fase de design detalhada
  ├── discuss.md             (5KB)  ← Lidar com ambiguidades
  ├── implement.md           (6.4KB) ← Fase de execução detalhada
  ├── quick-mode.md          (3.7KB) ← Atalhos para tarefas rápidas
  ├── tasks.md               (6.3KB) ← Quebrar em tarefas atômicas
  └── validate.md            (6.6KB) ← UAT interativo
```

### Como Referenciar
No `SKILL.md`:
```markdown
- **Discuss is triggered within Specify** only when the agent detects ambiguous 
  gray areas that need user input → [discuss.md](references/discuss.md)
```

O agente **só carrega** `discuss.md` quando encontra essa referência e precisa daquele contexto.

---

## Padrões de Escrita

### 1. Description (YAML Frontmatter)
✅ **Bom exemplo**:
```yaml
description: Manage Jira issues via Atlassian MCP — search, create, update, transition status,
 and handle sprint tasks. Auto-detects workspace configuration. Use when user says "create a 
 Jira ticket", "update my sprint", "check Jira status", "transition this issue", "search Jira",
 or "move ticket to done". Do NOT use for Confluence pages (use confluence-assistant).
```

❌ **Evitar**:
```yaml
description: A skill for Jira
```

### 2. When to Use
Sempre incluir seção explícita:
```markdown
## When to Use

Use this skill when the user asks to:
- Search for Jira issues or tasks
- Create new Jira issues (Task, Epic, Subtask)
- Update existing issues
- Transition issue status (To Do → In Progress → Done, etc.)

**Do NOT use for:**
- Confluence pages (use confluence-assistant)
- General project management (use project-management skill)
```

### 3. Configuration
Se a skill precisa de configuração:
```markdown
## Configuration

**Project Detection Strategy (Automatic):**
1. **Check workspace rules first**: Look for config in `.cursor/rules/jira-config.mdc`
2. **If not found**: Use MCP search tools to discover available projects
3. **If still unclear**: Ask user to specify project key

**Note for skill users:** To configure this skill for your workspace, create 
`.cursor/rules/jira-config.mdc` with your project details.
```

### 4. Workflow / Usage
Estrutura clara de passos:
```markdown
## Workflow

### 1. Finding Issues (Always Start Here)
**Use `search` (Rovo Search) first** for general queries:
...

### 2. Creating Issues
When user wants a new Jira ticket:
...
```

---

## Comparação: Nossa Implementação vs Tech Leads Club

| Aspecto | Nosso (ebb-platform-ia) | Tech Leads Club | Recomendação |
|---------|-------------------------|-----------------|--------------|
| **Estrutura** | `skills/` plano | `(categoria)/skill/` | Manter nossa (mais simples) |
| **Metadata** | Sem frontmatter | YAML frontmatter completo | ✅ **Adotar** |
| **References** | Tudo inline | `references/` on-demand | ✅ **Adotar** para skills complexas |
| **README.md** | Ausente | Documentação pública | ✅ **Adicionar** |
| **Versionamento** | Ausente | Semantic versioning | ✅ **Adotar** |
| **Licença** | Ausente | CC-BY-4.0 explícita | ✅ **Adicionar** |
| **When to Use** | Implícito | Explícito com triggers | ✅ **Melhorar** |
| **Do NOT use** | Ausente | Anti-patterns claros | ✅ **Adicionar** |

---

## Proposta de Melhoria para ebb-platform-ia

### Estrutura Proposta
```
ebb-platform-ia/
├── skills/
│   ├── rdp_connect/
│   │   ├── SKILL.md              ← Novo! Instruções para agente
│   │   ├── README.md             ← Novo! Docs públicas
│   │   ├── main.py
│   │   ├── requirements.txt
│   │   └── .env.example
│   ├── ssh_connect/
│   │   ├── SKILL.md
│   │   ├── README.md
│   │   └── ...
│   ├── kubernetes_debug/
│   │   ├── SKILL.md
│   │   ├── README.md
│   │   ├── references/           ← Novo! Docs on-demand
│   │   │   ├── workload-identity.md
│   │   │   ├── network-policies.md
│   │   │   └── pod-troubleshooting.md
│   │   └── ...
│   └── jira_assistant/
│       ├── SKILL.md
│       ├── README.md
│       ├── main.py
│       └── requirements.txt
└── docs/
    ├── RULES_SKILLS_MCPS_SUBAGENTS.md
    └── AGENT_SKILLS_PATTERNS.md  ← Este documento
```

### Template de SKILL.md
```markdown
---
name: kubernetes_debug
description: Diagnose Kubernetes pod issues - ImagePullBackOff, CrashLoopBackOff, Workload Identity failures, NetworkPolicy blocks. Auto-detects GKE clusters, analyzes logs/events, identifies root cause. Use when user says "pod not starting", "image pull error", "workload identity issues", "check k8s logs", or "debug deployment". Do NOT use for kubectl commands (use kubectl skill) or Terraform changes (use iac skill).
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
---

# Kubernetes Debug Skill

Diagnose and troubleshoot Kubernetes pod issues in GKE clusters.

## When to Use

Use this skill when:
- Pod is stuck in ImagePullBackOff
- CrashLoopBackOff errors
- Workload Identity authentication failures
- NetworkPolicy blocking traffic
- Need to analyze pod logs and events

**Do NOT use for:**
- Running kubectl commands directly (use kubectl skill)
- Infrastructure changes (use iac skill)
- Application debugging (use app-debug skill)

## Prerequisites

- `kubectl` configured with cluster access
- `gcloud` authenticated
- Access to GKE clusters (ebb-money-flows-dev, ebb-client-journey-dev)

## Workflow

### 1. Identify the Issue

First, gather basic information:
```bash
kubectl get pods -n <namespace>
kubectl describe pod <pod-name> -n <namespace>
```

### 2. Analyze Error Pattern

Common patterns and solutions:
- **ImagePullBackOff**: Check image registry, Workload Identity, Artifact Registry permissions
- **CrashLoopBackOff**: Check application logs, environment variables, secrets
- **Pending**: Check resources, node selectors, taints/tolerations

See [references/pod-troubleshooting.md](references/pod-troubleshooting.md) for detailed troubleshooting.

### 3. Workload Identity Issues

If you see `403` or `401` errors in logs:
1. Verify Service Account annotations
2. Check IAM bindings
3. Validate NetworkPolicy allows metadata server access

See [references/workload-identity.md](references/workload-identity.md) for complete guide.

## Output Format

Provide diagnosis in this format:
1. **Issue Identified**: [Brief description]
2. **Root Cause**: [Detailed explanation]
3. **Solution**: [Step-by-step fix]
4. **Prevention**: [How to avoid in future]

## Common Commands

```bash
# Check pod status
kubectl get pod <pod-name> -n <namespace> -o yaml

# View recent logs
kubectl logs <pod-name> -n <namespace> --tail=100

# Check events
kubectl get events -n <namespace> --sort-by='.lastTimestamp'

# Describe node
kubectl describe node <node-name>
```
```

### Template de README.md (Documentação Pública)
```markdown
# Kubernetes Debug Skill

**Version**: 1.0.0  
**Author**: Marcos Gomes  
**License**: CC-BY-4.0

## Overview

Automated Kubernetes troubleshooting skill for diagnosing pod issues in GKE clusters.

## Features

- ImagePullBackOff diagnosis
- CrashLoopBackOff analysis
- Workload Identity troubleshooting
- NetworkPolicy debugging
- Log and event analysis

## Installation

```bash
cd skills/kubernetes_debug
pip install -r requirements.txt
```

## Usage

### With AI Agent

This skill is automatically activated when you ask the agent:
- "Why is my pod not starting?"
- "Debug ImagePullBackOff error"
- "Check Workload Identity issues"

### Standalone

```bash
python main.py --namespace ebb-temis-dev --pod temis-compliance-7d8f9b5c-x9z2k
```

## Configuration

Create `.env` file:
```env
GCP_PROJECT=ebb-client-journey-dev
GKE_CLUSTER=main-cluster
REGION=southamerica-east1
```

## Documentation

- [SKILL.md](SKILL.md) - Agent instructions
- [references/pod-troubleshooting.md](references/pod-troubleshooting.md) - Detailed guide
- [references/workload-identity.md](references/workload-identity.md) - WI troubleshooting

## Contributing

See [../../docs/CONTRIBUTING.md](../../docs/CONTRIBUTING.md)

## License

CC-BY-4.0 - See [LICENSE](../../LICENSE)
```

---

## Próximos Passos

### Fase 1: Adicionar Metadata (1-2h)
- [ ] Criar SKILL.md para cada skill existente com YAML frontmatter
- [ ] Adicionar README.md em cada skill
- [ ] Definir versões iniciais (1.0.0)

### Fase 2: Refatorar Skills Complexas (2-4h)
- [ ] Extrair `kubernetes_debug` → criar `references/`
  - `workload-identity.md`
  - `network-policies.md`
  - `pod-troubleshooting.md`
- [ ] Atualizar SKILL.md com links para references

### Fase 3: Melhorar Descrições (1-2h)
- [ ] Expandir "When to Use" com triggers explícitos
- [ ] Adicionar "Do NOT use" em cada skill
- [ ] Melhorar descriptions no frontmatter

### Fase 4: Validação (30min)
- [ ] Criar script de validação (verifica YAML válido, campos obrigatórios)
- [ ] CI/CD check opcional

---

## Referências

- **Repository**: https://github.com/tech-leads-club/agent-skills
- **CLI Tool**: `npx @tech-leads-club/agent-skills`
- **MCP Server**: `@tech-leads-club/agent-skills-mcp`
- **Security Report**: https://github.com/snyk/agent-scan/blob/main/.github/reports/skills-report.pdf
- **License**: MIT (software) + CC-BY-4.0 (skills)
