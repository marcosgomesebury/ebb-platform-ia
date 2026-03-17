# Conceitos: MCPs Externos vs MCPs Internos

## 📚 Dois Conceitos Diferentes

### 1. MCP Externo (Model Context Protocol)

**O que é**: Servidores externos que expõem APIs/ferramentas para agentes de IA via protocolo padronizado.

**Exemplos** (do tech-leads-club/agent-skills):
- **Atlassian MCP**: Expõe Jira/Confluence APIs
- **GitHub MCP**: Expõe GitHub APIs
- **Slack MCP**: Expõe Slack APIs
- **Database MCP**: Acesso a bancos de dados

**Como funciona**:
```
Agent (Cursor/Claude) ←→ MCP Server ←→ External API (Jira/GitHub)
                        (middleware)
```

**Requisitos**:
- Instalar servidor MCP local
- Configurar em `~/.cursor/mcp.json` ou similar
- Servidor roda em background
- Agent comunica via protocolo MCP

**Exemplo de configuração** (Cursor):
```json
{
  "mcpServers": {
    "atlassian": {
      "command": "npx",
      "args": ["-y", "@tech-leads-club/atlassian-mcp"],
      "env": {
        "JIRA_URL": "https://company.atlassian.net",
        "JIRA_API_TOKEN": "token"
      }
    }
  }
}
```

**Vantagens**:
- ✓ Abstração simplificada
- ✓ Protocolo padronizado
- ✓ Múltiplos agents podem usar o mesmo server

**Desvantagens**:
- ✗ Requer instalação de servidores
- ✗ Dependência externa
- ✗ Pode não funcionar em ambientes restritos
- ✗ Menos controle sobre autenticação

---

### 2. MCP Interno (seu projeto)

**O que é**: Protocolos de orquestração entre skills Python locais.

**Exemplos** (seu `TEMPLATE_MCP.md`):
- **remote_db_connection_protocol**: Orquestra `ssh_connect` + `mysql_connect`
- **kubernetes_diagnostic_protocol**: Orquestra múltiplas skills de diagnóstico

**Como funciona**:
```
Subagent Python ←→ Skill 1 (local) ←→ External Service
                ←→ Skill 2 (local)
                ←→ Skill 3 (local)
```

**Estrutura**:
```
skills/
  ├── ssh_connect/main.py      ← Skill independente
  ├── mysql_connect/main.py    ← Skill independente
  └── kubernetes_debug/main.py ← Skill independente

subagents/
  └── database_diagnostic_agent.py  ← Orquestra skills (MCP interno)
```

**Exemplo** (seu `database_diagnostic_agent.py`):
```python
# MCP Interno: Orquestração de skills locais
from skills.ssh_connect import main as ssh_connect
from skills.kubernetes_debug import main as k8s_debug

def diagnose_database_issue(pod_name):
    # Passo 1: Check pod
    k8s_result = k8s_debug(pod_name)
    
    # Passo 2: Se problema de conectividade, usa SSH
    if "connection refused" in k8s_result:
        ssh_result = ssh_connect(server)
        return combine_results(k8s_result, ssh_result)
```

**Vantagens**:
- ✓ Sem dependências externas
- ✓ Funciona em ambientes restritos
- ✓ Total controle sobre autenticação
- ✓ Skills testáveis isoladamente
- ✓ Composição flexível

**Desvantagens**:
- ✗ Mais código para escrever
- ✗ Precisa implementar clients manualmente (REST API, SDK)
- ✗ Menos abstraído

---

## 🔄 Comparação

| Aspecto | MCP Externo (tech-leads-club) | MCP Interno (seu projeto) |
|---------|-------------------------------|---------------------------|
| **Instalação** | Requer MCP server | Apenas Python |
| **Rede** | Localhost:port | Direto API |
| **Config** | `mcp.json` | `.env` files |
| **Autenticação** | MCP server gerencia | Você gerencia |
| **Skills** | Abstraídas pelo server | Implementadas em Python |
| **Orquestração** | MCP protocol | Subagents Python |
| **Portabilidade** | Depende de MCP runtime | 100% Python portável |
| **Restrições** | Pode ser bloqueado | Funciona anywhere |

---

## 📋 Seu Projeto: Abordagem Híbrida

### O que você TEM

✅ **MCPs Internos** (orquestração local):
```
subagents/database_diagnostic_agent.py
  ↓
  ├─ skills/ssh_connect/
  ├─ skills/mysql_connect/
  └─ skills/kubernetes_debug/
```

✅ **Skills Python com APIs Diretas**:
- `jira_assistant` → Jira REST API
- `mysql_connect` → pymysql direto
- `ssh_connect` → paramiko direto
- `kubernetes_debug` → kubectl + gcloud

### O que você NÃO TEM (nem precisa)

❌ **MCPs Externos**:
- Nenhum servidor MCP rodando
- Nenhum `~/.cursor/mcp.json`
- Nenhuma dependência de @tech-leads-club MCPs

---

## 🎯 Implementação: jira_assistant

### Antes (com MCP externo - tech-leads-club)

```yaml
requires:
  - Atlassian MCP Server  ← Dependência externa
```

```python
# Abstrato, via MCP
search("jira issues assigned to me")  # MCP faz mágica
create_issue(summary="...")           # MCP faz mágica
```

### Depois (sem MCP - seu projeto) ✅

```yaml
requires:
  - requests              ← Apenas biblioteca Python
  - python-dotenv
api:
  - Atlassian Jira REST API v3
```

```python
# Explícito, controle total
import requests

client = JiraClient()
issues = client.search_issues("assignee = currentUser()")
client.create_issue(summary="...", description="...")
```

---

## 💡 Quando Usar Cada Abordagem

### Use MCP Externo SE:
- ✓ Ambiente permite instalação de servidores
- ✓ Quer abstração máxima
- ✓ Usa múltiplos agents que compartilham server
- ✓ MCP server já existe e é mantido

### Use MCP Interno (Python direto) SE:
- ✓ Ambiente restrito (seu caso)
- ✓ Precisa de controle total
- ✓ Quer portabilidade máxima
- ✓ Prefere código explícito vs abstração
- ✓ Skills precisam rodar isoladamente

---

## 📁 Estrutura Recomendada (seu projeto)

```
ebb-platform-ia/
├── skills/                    # Skills isoladas (APIs diretas)
│   ├── jira_assistant/
│   │   ├── main.py           # Client REST API Jira
│   │   ├── SKILL.md
│   │   └── .env.example
│   ├── kubernetes_debug/
│   │   ├── main.py           # kubectl + gcloud CLI
│   │   └── SKILL.md
│   └── mysql_connect/
│       ├── main.py           # pymysql direto
│       └── SKILL.md
│
├── subagents/                 # MCPs internos (orquestração)
│   └── database_diagnostic_agent.py  # Usa skills acima
│
└── docs/
    ├── TEMPLATE_MCP.md       # Define protocolo interno
    └── MCPS_EXPLAINED.md     # Este documento
```

---

## 🔐 Autenticação

### MCP Externo
```json
{
  "mcpServers": {
    "jira": {
      "env": {
        "JIRA_TOKEN": "token"  ← MCP server usa
      }
    }
  }
}
```

### Seu Projeto (MCP Interno)
```env
# skills/jira_assistant/.env
JIRA_API_TOKEN=your_token  ← Seu código usa diretamente
```

---

## ✅ Conclusão

**Você está correto**: Não pode usar MCPs externos (servidores).

**Solução implementada**: 
- ✓ Skills Python com APIs REST diretas
- ✓ MCPs internos (subagents) para orquestração
- ✓ Zero dependências de servidores externos
- ✓ 100% portável e funcional em ambientes restritos

**Exemplo real** (jira_assistant agora):
```python
# Sem MCP server, apenas requests
import requests
response = requests.post(
    "https://ebury.atlassian.net/rest/api/3/issue",
    json=payload,
    auth=(email, token)
)
```

**MCP Interno** continua válido para orquestração:
```python
# subagents/jira_workflow_agent.py
from skills.jira_assistant.main import JiraClient
from skills.slack_notifier.main import SlackClient

def create_and_notify(summary):
    jira = JiraClient()
    slack = SlackClient()
    
    issue = jira.create_issue(summary)
    slack.send(f"Created {issue['key']}")
```

---

## 📚 Referências

- **MCP Externo**: https://github.com/tech-leads-club/agent-skills
- **Seu MCP Interno**: [TEMPLATE_MCP.md](../TEMPLATE_MCP.md)
- **Jira REST API**: https://developer.atlassian.com/cloud/jira/platform/rest/v3/
