# Jira MCP Server Skill 🎫

**Servidor MCP (Model Context Protocol) para integração com Jira Cloud**, permitindo que AI assistants busquem, criem e gerenciem issues através de linguagem natural.

---

## 📁 Estrutura

```
skills/jira_assistant/
├── SKILL.md                    # 🤖 Instruções para AI agents
├── README.md                   # 📖 Esta documentação
├── requirements.txt            # 📦 Dependências Python
├── .env.example               # 🔐 Template de credenciais
├── .env                       # 🔐 Credenciais (gitignored)
├── server/                    # 💻 Servidor MCP
│   └── mcp_server_jira.py
├── tests/                     # ✅ Testes
│   └── test_mcp_client.py
└── specs/                     # 📋 OpenSpec
    └── jira-mcp-tools.md
```

---

## 🚀 Quick Start

### 1. Instalar Dependências

```bash
pip install mcp requests python-dotenv
```

### 2. Configurar Credenciais

Copie `.env.example` para `.env`:

```env
JIRA_URL=https://fxsolutions.atlassian.net
JIRA_EMAIL=seu.email@ebury.com
JIRA_API_TOKEN=seu_token_aqui
```

**Obter API Token**: https://id.atlassian.com/manage-profile/security/api-tokens

### 3. Testar

```bash
cd tests/
python3 test_mcp_client.py
```

### 4. Integrar com Cursor

`~/.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "jira": {
      "command": "python3",
      "args": ["/caminho/para/server/mcp_server_jira.py"],
      "env": {
        "JIRA_URL": "https://fxsolutions.atlassian.net",
        "JIRA_EMAIL": "email@ebury.com",
        "JIRA_API_TOKEN": "token"
      }
    }
  }
}
```

---

## 🛠️ Ferramentas

| Tool | Descrição |
|------|-----------|
| `jira_get_issue` | Buscar detalhes de issue específica |
| `jira_search_issues` | Buscar issues com JQL |
| `jira_create_issue` | Criar nova issue |
| `jira_add_comment` | Adicionar comentário |

---

## 📋 OpenSpec: Como Se Relaciona?

### O Que É OpenSpec?

**OpenSpec** é uma metodologia de **Spec-Driven Development** usada neste repositório para manter especificações de comportamento dos sistemas.

### Relação com Esta Skill

```
Portfolio OpenSpec (nível domínio)
openspec/specs/ebb-client-journey.md
openspec/specs/ebb-money-flows.md
           ↓ descreve business behavior
Skills (nível automação)
skills/jira_assistant/
skills/kubernetes_debug/
           ↓ cada skill tem seu spec
Tool Specs (nível ferramenta MCP)
skills/jira_assistant/specs/jira-mcp-tools.md
  ↳ Comportamento esperado (BDD-style)
  ↳ Input/output schemas
  ↳ Casos de erro
```

### Exemplo: OpenSpec para Jira MCP

**[specs/jira-mcp-tools.md](specs/jira-mcp-tools.md)**:

```gherkin
Scenario: Buscar issue existente
  GIVEN issue EPT-2030 exists in Jira
  WHEN tool jira_get_issue is called with key="EPT-2030"
  THEN response includes all fields
  AND link is "https://fxsolutions.atlassian.net/browse/EPT-2030"
```

**Benefícios**:
- ✅ Comportamento determinístico
- ✅ Documentação viva
- ✅ Evolução controlada (ADDED/MODIFIED/REMOVED)
- ✅ Onboarding rápido

---

## 🧪 Testes

```bash
cd tests/
python3 test_mcp_client.py
```

**Fluxo TDD com OpenSpec**:

1. **Especificar** em `specs/jira-mcp-tools.md`
2. **Testar** em `tests/test_mcp_client.py`
3. **Implementar** em `server/mcp_server_jira.py`

---

## 🔧 Adicionar Nova Ferramenta

1. Especificar em `specs/jira-mcp-tools.md`
2. Registrar em `server/mcp_server_jira.py` (`@server.list_tools()`)
3. Implementar handler (`_new_tool()`)
4. Testar em `tests/test_mcp_client.py`

---

## 📚 Referências

- **OpenSpec**: [/openspec/README.md](/openspec/README.md)
- **MCP Spec**: https://spec.modelcontextprotocol.io/
- **Jira API**: https://developer.atlassian.com/cloud/jira/platform/rest/v3/
