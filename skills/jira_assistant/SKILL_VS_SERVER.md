# SKILL.md + MCP Server: Como Funcionam Juntos

## ✅ Resposta Rápida

**SIM, você precisa de AMBOS:**

- **SKILL.md** → Instruções para o AI agent saber QUANDO e COMO usar a skill
- **server/mcp_server_jira.py** → Implementação que EXECUTA as ações

São **complementares**, não alternativos.

---

## 🎯 Fluxo Completo

```
Usuario fala:
"Crie uma task no Jira para implementar feature X"
                        ↓
┌──────────────────────────────────────────────────────┐
│ 1. AI AGENT DETECTA TRIGGER                         │
│                                                      │
│ • Lê SKILL.md                                       │
│ • Encontra trigger: "Crie uma task no Jira"        │
│ • Verifica "When to Use": ✅ Match                 │
│ • Detecta projeto: EPT (do contexto workspace)      │
└──────────────────────────────────────────────────────┘
                        ↓
┌──────────────────────────────────────────────────────┐
│ 2. AI AGENT INVOCA MCP TOOL                         │
│                                                      │
│ • Consulta "MCP Tools Available" no SKILL.md        │
│ • Escolhe: jira_create_issue                        │
│ • Monta chamada MCP:                                │
│   {                                                 │
│     "tool": "jira_create_issue",                    │
│     "arguments": {                                  │
│       "project": "EPT",                             │
│       "summary": "Implementar feature X",           │
│       "description": "...",                         │
│       "issue_type": "Task"                          │
│     }                                               │
│   }                                                 │
└──────────────────────────────────────────────────────┘
                        ↓
┌──────────────────────────────────────────────────────┐
│ 3. SERVIDOR MCP EXECUTA                             │
│                                                      │
│ • server/mcp_server_jira.py recebe chamada MCP      │
│ • Método _create_issue() é executado                │
│ • Faz chamada HTTP ao Jira REST API:               │
│   POST /rest/api/2/issue                            │
│ • Jira responde: {"key": "EPT-2099", ...}          │
│ • MCP server formata resposta                       │
└──────────────────────────────────────────────────────┘
                        ↓
┌──────────────────────────────────────────────────────┐
│ 4. AI AGENT RESPONDE USUÁRIO                        │
│                                                      │
│ • Recebe resposta do MCP server                     │
│ • Formata output (consulta SKILL.md para formato)   │
│ • Exibe:                                            │
│                                                     │
│   ✅ Task criada: EPT-2099                          │
│   📝 Summary: Implementar feature X                 │
│   🔗 https://fxsolutions.atlassian.net/browse/EPT-2099 │
└──────────────────────────────────────────────────────┘
```

---

## 📋 O Que Cada Arquivo Faz

### SKILL.md (Metadados + Instruções)

**Conteúdo**:
```yaml
---
name: jira_assistant
description: Manage Jira issues via MCP server...
metadata:
  type: mcp-server
  mcp_server: server/mcp_server_jira.py  # ← Aponta para o servidor
---

## When to Use
- "Create Jira ticket"        ← Triggers
- "Search Jira"
- "Get issue details"

## MCP Tools Available          ← Lista de ferramentas
- jira_get_issue
- jira_search_issues
- jira_create_issue
- jira_add_comment

## Usage Examples                ← Como usar cada tool
- "Show me EPT-2030"
  → Use: jira_get_issue(key="EPT-2030")
```

**Propósito**: Ensinar o AI agent...
- ✅ QUANDO usar a skill (triggers)
- ✅ QUE ferramentas estão disponíveis
- ✅ COMO invocar cada ferramenta
- ✅ QUE projeto usar (EPT)
- ✅ COMO formatar respostas

### server/mcp_server_jira.py (Implementação)

**Conteúdo**:
```python
class JiraMCPServer:
    def __init__(self):
        self.server = Server("jira-python-mcp")
        self.auth = (JIRA_EMAIL, JIRA_API_TOKEN)
    
    @server.list_tools()
    async def list_tools() -> list[Tool]:
        return [
            Tool(name="jira_get_issue", ...),
            Tool(name="jira_search_issues", ...),
            Tool(name="jira_create_issue", ...),
            Tool(name="jira_add_comment", ...)
        ]
    
    @server.call_tool()
    async def call_tool(name: str, arguments: Any):
        if name == "jira_create_issue":
            return self._create_issue(...)
    
    def _create_issue(self, project, summary, ...):
        url = f"{JIRA_URL}/rest/api/2/issue"
        response = requests.post(url, auth=self.auth, json=payload)
        return {"key": response.json()["key"], ...}
```

**Propósito**: EXECUTAR as ações...
- ✅ Registrar ferramentas MCP
- ✅ Receber chamadas via protocolo MCP
- ✅ Fazer requisições HTTP ao Jira API
- ✅ Tratar erros (404, 401, etc)
- ✅ Retornar dados formatados

---

## 🔄 Relação Entre Arquivos

```
┌─────────────────────────────────────────────────────────┐
│ SKILL.md                                                │
│ (Documentação para AI Agent)                            │
│                                                         │
│ metadata:                                               │
│   mcp_server: server/mcp_server_jira.py  ───────┐      │
│                                                  │      │
│ ## MCP Tools Available:                          │      │
│ - jira_get_issue                                 │      │
│ - jira_search_issues                             │      │
│ - jira_create_issue                              │      │
│ - jira_add_comment                               │      │
│                                                  │      │
│ ## Usage Examples:                               │      │
│ User: "Create task in EPT"                       │      │
│ → Use: jira_create_issue(project="EPT", ...)    │      │
└──────────────────────────────────────────────────┼──────┘
                                                   │
                  Aponta para implementação ───────┘
                                                   │
                                                   ↓
┌─────────────────────────────────────────────────────────┐
│ server/mcp_server_jira.py                               │
│ (Servidor MCP - Implementação)                          │
│                                                         │
│ class JiraMCPServer:                                    │
│     @server.list_tools()                                │
│     async def list_tools():                             │
│         return [                                        │
│             Tool(name="jira_get_issue"),                │
│             Tool(name="jira_search_issues"),            │
│             Tool(name="jira_create_issue"),             │
│             Tool(name="jira_add_comment")               │
│         ]  ← Implementa as ferramentas documentadas     │
│                                                         │
│     def _create_issue(project, summary, ...):           │
│         # Chamada real ao Jira REST API                 │
│         response = requests.post(JIRA_URL, ...)         │
│         return {"key": "EPT-2099", ...}                 │
└─────────────────────────────────────────────────────────┘
                        ↓
              Validado por testes
                        ↓
┌─────────────────────────────────────────────────────────┐
│ tests/test_mcp_client.py                                │
│                                                         │
│ result = await session.call_tool("jira_create_issue", {│
│     "project": "EPT",                                   │
│     "summary": "Test issue"                             │
│ })                                                      │
│ assert result["key"].startswith("EPT-")                 │
└─────────────────────────────────────────────────────────┘
                        ↓
              Especificado em
                        ↓
┌─────────────────────────────────────────────────────────┐
│ specs/jira-mcp-tools.md                                 │
│ (OpenSpec - Comportamento esperado)                     │
│                                                         │
│ Scenario: Criar issue válida                            │
│   GIVEN projeto EPT existe                              │
│   WHEN jira_create_issue(project="EPT", summary="...")  │
│   THEN retorna {"key": "EPT-XXXX", "link": "..."}      │
└─────────────────────────────────────────────────────────┘
```

---

## 💡 Analogia: Restaurante

### SKILL.md = Cardápio
```
🍕 Pizza Margherita
   Ingredientes: Tomate, queijo, manjericão
   Quando pedir: Se gosta de sabores clássicos
   Como pedir: "Uma margherita, por favor"

🍝 Spaghetti Carbonara
   Ingredientes: Ovos, bacon, queijo
   Quando pedir: Se quer algo cremoso
   Como pedir: "Um carbonara"
```

**Propósito**: Cliente (AI agent) sabe O QUE está disponível e QUANDO pedir.

### server/mcp_server_jira.py = Cozinha
```python
def fazer_pizza_margherita():
    # 1. Pegar massa
    # 2. Adicionar tomate
    # 3. Adicionar queijo
    # 4. Assar 10min
    return Pizza("Margherita")

def fazer_carbonara():
    # 1. Cozinhar macarrão
    # 2. Fritar bacon
    # 3. Misturar ovos
    # 4. Combinar tudo
    return Prato("Carbonara")
```

**Propósito**: Cozinheiro (servidor MCP) sabe COMO FAZER cada prato.

### Cliente Pede (AI Agent)
```
Cliente: "Quero uma pizza margherita"
   ↓
Garçom lê cardápio (SKILL.md): ✅ Temos margherita
   ↓
Garçom grita para cozinha: "Uma margherita!"
   ↓
Cozinha (server/mcp_server_jira.py) faz a pizza
   ↓
Garçom entrega: 🍕 "Sua margherita"
```

**Sem o cardápio (SKILL.md)**: Cliente não sabe o que pedir  
**Sem a cozinha (server/)**: Não tem quem faça o prato  
**PRECISA DOS DOIS!**

---

## 🎓 Resumo

### Você PRECISA de AMBOS porque:

#### SKILL.md é para o AI AGENT:
- ✅ Saber QUANDO usar a skill (triggers)
- ✅ Entender QUE projeto usar (EPT)
- ✅ Conhecer QUAIS ferramentas estão disponíveis
- ✅ Ver EXEMPLOS de como invocar
- ✅ Saber COMO formatar respostas

#### server/mcp_server_jira.py é para EXECUTAR:
- ✅ Registrar ferramentas no protocolo MCP
- ✅ Receber chamadas via stdin/stdout
- ✅ Fazer requisições HTTP ao Jira
- ✅ Tratar erros e edge cases
- ✅ Retornar dados estruturados

### Sem SKILL.md:
```
❌ AI agent não sabe QUANDO usar
❌ AI agent não sabe QUAL ferramenta chamar
❌ AI agent não sabe COMO formatar output
```

### Sem server/:
```
❌ Não tem QUEM execute as ações
❌ Não tem conexão com Jira API
❌ MCP client não encontra o servidor
```

---

## 📊 Comparação Visual

```
┌─────────────────┬──────────────────┬───────────────────┐
│                 │ SKILL.md         │ server/           │
├─────────────────┼──────────────────┼───────────────────┤
│ Tipo            │ Documentação     │ Código Python     │
│ Audiência       │ AI Agent         │ MCP Runtime       │
│ Conteúdo        │ Instruções       │ Implementação     │
│ Formato         │ Markdown+YAML    │ Python async      │
│ Responde        │ QUANDO/O QUÊ     │ COMO              │
│ Exemplo         │ "Use quando..."  │ requests.post()   │
│ Muda quando     │ Novos triggers   │ Nova feature      │
│ Testado por     │ AI agent         │ test_mcp_client   │
└─────────────────┴──────────────────┴───────────────────┘
```

---

## ✅ Checklist: Você Precisa de Ambos?

- [ ] **AI agent precisa saber QUANDO usar?** → SIM → SKILL.md
- [ ] **AI agent precisa saber QUAIS tools?** → SIM → SKILL.md
- [ ] **Precisa EXECUTAR ações no Jira?** → SIM → server/
- [ ] **Precisa fazer HTTP requests?** → SIM → server/
- [ ] **Precisa tratar erros 404/401?** → SIM → server/

**Resultado**: ✅ Precisa de AMBOS!

---

## 🔗 Arquivos Relacionados

- **SKILL.md** - Este arquivo (instruções AI agent)
- **server/mcp_server_jira.py** - Implementação do servidor MCP
- **tests/test_mcp_client.py** - Testes de integração
- **specs/jira-mcp-tools.md** - Especificação de comportamento
- **README.md** - Documentação completa

---

## 📝 TL;DR

**SKILL.md**: "Como usar" (para AI agent)  
**server/**: "Como funciona" (para executar)  

**Ambos são necessários!** 🎯
