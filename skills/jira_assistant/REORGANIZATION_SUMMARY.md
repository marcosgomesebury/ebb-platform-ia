# Reorganização Jira Assistant - Resumo Executivo

## ✅ O Que Foi Feito

### Antes (Bagunçado)
```
jira_assistant/
├── main.py                      ❌ REST direto
├── test_ept2080.py              ❌ Teste REST
├── test_if_it_was_mcp.py        ❌ Exemplo conceitual
├── list_projects.py             ❌ Script avulso
├── mcp_server_jira.py           ✓ MCP (estava solto)
├── test_mcp_client.py           ✓ Teste (estava solto)
├── COMPARISON_REST_VS_MCP.md    ❌ Doc comparação
├── README_MCP_PYTHON.md         ❌ Doc fragmentado
└── README.md                    ❌ Doc desatualizado
```

### Depois (Organizado) ✅
```
jira_assistant/
├── SKILL.md                    # 🤖 Instruções AI agent
├── README.md                   # 📖 Documentação principal
├── requirements.txt            # 📦 Dependências
├── .env.example               # 🔐 Template
├── .env                       # 🔐 Credenciais
├── server/                    # 💻 Implementação
│   └── mcp_server_jira.py    #    Servidor MCP Python
├── tests/                     # ✅ Testes
│   └── test_mcp_client.py    #    Teste integração
└── specs/                     # 📋 OpenSpec
    └── jira-mcp-tools.md     #    Comportamentos esperados
```

---

## 🎯 Respostas às Suas Perguntas

### 1. "Onde colocar os testes?"

**Resposta**: Em `tests/` ✅

```
tests/
└── test_mcp_client.py         # Teste de integração end-to-end

# Como executar:
cd tests/
python3 test_mcp_client.py
```

**Tipos de teste**:
- ✅ **Integração**: `test_mcp_client.py` (testa servidor MCP completo)
- 🔜 **Unitário**: `test_jira_client.py` (testar JiraClient isolado - futuro)
- 🔜 **E2E**: `test_cursor_integration.py` (testar com Cursor real - futuro)

### 2. "Onde o OpenSpec entra nessa jogada?"

**Resposta**: OpenSpec tem **3 níveis** neste projeto:

#### Nível 1: Portfolio (Domínios de Negócio)
```
/openspec/
├── project.md                  # Visão geral portfolio
├── tasks.md                    # Tracking de trabalho
├── specs/                      # Specs estáveis por domínio
│   ├── ebb-client-journey.md  # Temis, CJ workflows
│   ├── ebb-money-flows.md     # Money flows, conciliação
│   ├── ebb-treasury.md        # Tree, FX, Treasury
│   └── ...
├── changes/                    # Delta specs em progresso
│   └── 2026-03-16-nova-feature.md
└── archive/                    # Specs concluídas
```

**Propósito**: Documentar **comportamento de negócio** dos sistemas (não código).

#### Nível 2: Skills (Automações)
```
/skills/
├── jira_assistant/            # Esta skill
├── kubernetes_debug/          # Debugging K8s
├── ssh_connect/               # SSH automation
└── mysql_connect/             # MySQL queries
```

**Propósito**: Ferramentas que **AI agents** usam para executar tarefas.

#### Nível 3: Tool Specs (Dentro de cada Skill)
```
/skills/jira_assistant/
└── specs/
    └── jira-mcp-tools.md      # ⭐ OpenSpec da skill

# Este arquivo especifica:
- Comportamento de cada ferramenta MCP
- Input/output schemas
- Casos de erro
- Exemplos BDD (GIVEN/WHEN/THEN)
```

**Propósito**: Documentar **comportamento esperado** de cada ferramenta MCP.

---

## 📊 Diagrama: Como Tudo Se Conecta

```
┌─────────────────────────────────────────────────────────────┐
│ NÍVEL 1: Portfolio OpenSpec                                 │
│ /openspec/specs/ebb-client-journey.md                       │
│                                                              │
│ "O sistema Temis deve processar onboarding aprovado         │
│  QUANDO status = APPROVED AND documents validated           │
│  ENTÃO criar conta interna AND notificar usuário"           │
└─────────────────────────────────────────────────────────────┘
                            ↓
    Descreve regras de negócio (independente de como implementar)
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ NÍVEL 2: Skills (Automações)                                │
│ /skills/jira_assistant/                                      │
│ /skills/kubernetes_debug/                                    │
│                                                              │
│ "AI agents usam estas skills para executar tarefas"         │
└─────────────────────────────────────────────────────────────┘
                            ↓
        Cada skill tem seu próprio spec de ferramentas
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ NÍVEL 3: Tool Specs (OpenSpec da Skill)                     │
│ /skills/jira_assistant/specs/jira-mcp-tools.md              │
│                                                              │
│ Scenario: Buscar issue existente                            │
│   GIVEN issue EPT-2030 exists                               │
│   WHEN tool jira_get_issue(key="EPT-2030")                  │
│   THEN return all fields AND link                           │
│                                                              │
│ Scenario: Issue não existe                                  │
│   GIVEN issue EPT-9999 does not exist                       │
│   WHEN tool jira_get_issue(key="EPT-9999")                  │
│   THEN return 404 error                                     │
└─────────────────────────────────────────────────────────────┘
                            ↓
              Implementado e testado em:
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ CÓDIGO                                                       │
│ server/mcp_server_jira.py  ← Implementação                  │
│ tests/test_mcp_client.py   ← Validação contra spec          │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔄 Workflow: Como Usar OpenSpec com Esta Skill

### Cenário 1: Adicionar Nova Ferramenta MCP

**Exemplo**: Adicionar `jira_transition_issue` (mudar status)

#### Passo 1: Especificar (specs/)
```markdown
# specs/jira-mcp-tools.md

### Tool: jira_transition_issue

**Purpose**: Transicionar issue para outro status (Open→In Progress→Done)

**Behavior**:
- GIVEN issue EPT-2030 in status "Open"
- WHEN tool jira_transition_issue(key="EPT-2030", transition="In Progress")
- THEN issue status changes to "In Progress"
- AND returns confirmation

**Input Schema**:
{
  "key": "EPT-2030",
  "transition": "In Progress"  // ou "Done", "Blocked", etc
}

**Error Cases**:
- Transition inválida: {"error": "Transition 'Invalid' not available"}
- Issue não existe: {"error": "Issue not found"}
```

#### Passo 2: Testar (tests/)
```python
# tests/test_mcp_client.py

# Teste 3: Transicionar issue
result = await session.call_tool("jira_transition_issue", {
    "key": "EPT-2030",
    "transition": "In Progress"
})
data = json.loads(result.content[0].text)

assert data["old_status"] == "Open"
assert data["new_status"] == "In Progress"
print(f"✅ Issue {data['key']} moved to {data['new_status']}")
```

#### Passo 3: Implementar (server/)
```python
# server/mcp_server_jira.py

@self.server.list_tools()
async def list_tools() -> list[Tool]:
    return [
        # ... ferramentas existentes
        Tool(
            name="jira_transition_issue",
            description="Transicionar issue para outro status",
            inputSchema={
                "type": "object",
                "properties": {
                    "key": {"type": "string"},
                    "transition": {"type": "string"}
                },
                "required": ["key", "transition"]
            }
        )
    ]

def _transition_issue(self, key: str, transition: str) -> dict:
    """Transicionar issue"""
    # 1. Get available transitions
    url = f"{JIRA_URL}/rest/api/2/issue/{key}/transitions"
    response = requests.get(url, auth=self.auth)
    transitions = response.json()['transitions']
    
    # 2. Find transition ID
    transition_id = None
    for t in transitions:
        if t['name'] == transition:
            transition_id = t['id']
            break
    
    if not transition_id:
        return {"error": f"Transition '{transition}' not available"}
    
    # 3. Execute transition
    payload = {"transition": {"id": transition_id}}
    response = requests.post(url, auth=self.auth, json=payload)
    
    return {
        "key": key,
        "old_status": "...",
        "new_status": transition,
        "message": f"Issue {key} transitioned to {transition}"
    }
```

#### Passo 4: Validar
```bash
cd tests/
python3 test_mcp_client.py

# ✅ Teste 3: Transicionar issue
# ✅ Issue EPT-2030 moved to In Progress
```

**Isso é TDD guiado por OpenSpec!** 🎯

---

### Cenário 2: Bug em Produção

**Exemplo**: Tool `jira_search_issues` retorna erro 410 (API deprecated)

#### Passo 1: Documentar no spec (specs/)
```markdown
# specs/jira-mcp-tools.md

## Change Log

### 2026-03-17 - MODIFIED: jira_search_issues

**MODIFIED Behavior**:
- OLD: Used API v2 `/rest/api/2/search`
- NEW: Uses API v3 `/rest/api/3/search/jql`
- REASON: Jira deprecated v2 search (HTTP 410 error)

**Error Cases**:
- REMOVED: API v2 deprecation error (now uses v3)
```

#### Passo 2: Atualizar teste
```python
# tests/test_mcp_client.py

# Teste que valida API v3
result = await session.call_tool("jira_search_issues", {
    "jql": "project = EPT",
    "max_results": 5
})
# Deve funcionar (não mais receber 410)
```

#### Passo 3: Fix no código
```python
# server/mcp_server_jira.py

def _search_issues(self, jql: str, max_results: int) -> dict:
    # OLD: url = f"{JIRA_URL}/rest/api/2/search"  ❌
    url = f"{JIRA_URL}/rest/api/3/search/jql"    # ✅
    # ...
```

**Spec documenta a mudança (ADDED/MODIFIED/REMOVED)!**

---

## 📚 Relação com OpenSpec Portfolio

### Exemplo Real: Como Skills e OpenSpec Trabalham Juntos

**Situação**: Você está implementando feature de onboarding no Temis.

#### 1. Consultar OpenSpec do Domínio
```bash
cat /openspec/specs/ebb-client-journey.md

# Você lê:
# "QUANDO onboarding aprovado
#  E documentos validados
#  ENTÃO criar conta interna
#  E enviar notificação"
```

#### 2. Usar Skills para Implementar
Durante desenvolvimento, AI agent pode:

```
Você: Crie uma task Jira para implementar notificação

AI: [Usa skill jira_assistant.jira_create_issue]
    ✅ Criado EPT-2099: Implementar notificação onboarding
    
Você: Verifique se o pod temis-notification está rodando

AI: [Usa skill kubernetes_debug]
    ✅ Pod temis-notification-abc123 Running
    ✅ 3/3 containers ready
```

#### 3. Documentar em OpenSpec Change
```bash
cat /openspec/changes/2026-03-17-notificacao-onboarding.md

# Delta Spec: Notificação Onboarding

**Ticket**: EPT-2099
**Status**: In Progress

## ADDED Requirements
- REQ-001: Sistema DEVE enviar email quando onboarding aprovado
- REQ-002: Template email DEVE incluir link de ativação

## Affected Components
- temis-notification service
- email-sender service

## Testing
- [x] Jira task criada (EPT-2099)
- [x] Pod notification verificado (usando kubernetes_debug skill)
- [ ] Teste de envio de email
```

**Skills são FERRAMENTAS para implementar o que OpenSpec documenta!**

---

## 🎯 Benefícios da Nova Estrutura

### ✅ Clareza
```
Antes: Arquivos misturados (REST + MCP + docs + testes)
Depois: Estrutura clara (server/ + tests/ + specs/)
```

### ✅ Testabilidade
```
tests/test_mcp_client.py
  ↓ valida contra
specs/jira-mcp-tools.md
  ↓ é implementado em
server/mcp_server_jira.py
```

### ✅ Manutenibilidade
```
Precisa debug? → tests/
Entender comportamento? → specs/
Modificar código? → server/
```

### ✅ Onboarding
```
Novo dev:
1. Lê: specs/jira-mcp-tools.md (entende O QUE faz)
2. Lê: server/mcp_server_jira.py (entende COMO faz)
3. Roda: tests/test_mcp_client.py (valida)
```

---

## 📋 Arquivos Mantidos vs Removidos

### ✅ Mantidos (Organizados)
- `SKILL.md` - Instruções para AI agent
- `requirements.txt` - Dependências
- `.env.example` - Template credenciais
- `server/mcp_server_jira.py` - Servidor MCP
- `tests/test_mcp_client.py` - Testes
- `specs/jira-mcp-tools.md` - OpenSpec (novo!)
- `README.md` - Doc consolidada (reescrita!)

### ❌ Removidos (Limpeza)
- `main.py` - Era implementação REST direta
- `test_ept2080.py` - Era teste REST direto
- `test_if_it_was_mcp.py` - Era exemplo conceitual
- `list_projects.py` - Era script avulso
- `COMPARISON_REST_VS_MCP.md` - Comparação não mais necessária
- `README_MCP_PYTHON.md` - Doc fragmentado (consolidado no README.md)

**Resultado**: Estrutura limpa focada em MCP! 🎯

---

## 🚀 Próximos Passos

### Curto Prazo
- [ ] Adicionar mais ferramentas MCP (transition, assign, etc)
- [ ] Expandir testes (casos de erro, edge cases)
- [ ] Documentar padrão para outras skills

### Médio Prazo
- [ ] Criar skill openspec_assistant (AI agent le specs via MCP)
- [ ] Integrar specs com CI/CD (validar contra testes)
- [ ] Dashboard de coverage (specs vs testes)

### Longo Prazo
- [ ] OpenSpec como fonte de verdade para geração de código
- [ ] AI agents criam delta specs automaticamente
- [ ] Sincronização specs ↔ Jira ↔ Código

---

## 📝 Resumo das Respostas

### 1. "Manter só o servidor MCP" ✅
- Removidos: `main.py`, `test_ept2080.py`, scripts REST
- Mantido: Apenas `server/mcp_server_jira.py`

### 2. "Reorganizar estrutura" ✅
```
server/  → Código do servidor MCP
tests/   → Testes de integração
specs/   → OpenSpec (comportamentos esperados)
```

### 3. "Onde colocar testes?" ✅
- `tests/test_mcp_client.py` - Integração end-to-end
- Futuro: `tests/test_unit.py` - Testes unitários

### 4. "Onde OpenSpec entra?" ✅
- **Portfolio**: `/openspec/specs/` - Comportamento de negócio
- **Skills**: `/skills/*/specs/` - Comportamento de ferramentas
- **Workflow**: Spec → Test → Implement (TDD guiado por spec)

---

**Estrutura final testada e funcionando!** 🎉
