# Spec: Jira MCP Server Tools

**Status**: Stable  
**Version**: 1.0.0  
**Date**: 2026-03-16  
**Owner**: Platform Team  

---

## Overview

Servidor MCP (Model Context Protocol) que expõe ferramentas para interação com Jira Cloud, permitindo que AI assistants (Cursor, Claude Desktop, Cline) busquem, criem e gerenciem issues do Jira através de linguagem natural.

**Protocol**: Model Context Protocol v1.0 (stdio)  
**Implementation**: Python 3.12+ with `mcp` SDK 1.26.0  
**API**: Jira Cloud REST API v2/v3  

---

## Tools Specification

### Tool: jira_get_issue

**Purpose**: Buscar detalhes completos de uma issue específica do Jira.

**Behavior**:
- GIVEN uma issue key válida (ex: EPT-2030)
- WHEN o tool é chamado
- THEN deve retornar todos os campos principais da issue
- AND deve incluir link direto para o Jira

**Input Schema**:
```json
{
  "type": "object",
  "properties": {
    "key": {
      "type": "string",
      "description": "Issue key (ex: EPT-2030)",
      "pattern": "^[A-Z]+-\\d+$"
    }
  },
  "required": ["key"]
}
```

**Output Schema**:
```json
{
  "key": "string",           // Issue key
  "summary": "string",        // Título
  "status": "string",         // Status atual
  "type": "string",          // Bug, Task, Story, etc
  "priority": "string",       // Highest, High, Medium, Low
  "assignee": "string|null",  // Nome do assignee (ou null)
  "reporter": "string",       // Nome do reporter
  "created": "ISO8601",       // Data de criação
  "updated": "ISO8601",       // Última atualização
  "description": "string",    // Descrição completa
  "link": "URL"              // Link direto no Jira
}
```

**Error Cases**:
- Issue não encontrada (404): `{"error": "Issue EPT-9999 not found"}`
- Sem permissão (403): `{"error": "Access denied to issue EPT-2030"}`
- Autenticação inválida (401): `{"error": "Authentication failed"}`

**Examples**:

```gherkin
Scenario: Buscar issue existente
  GIVEN issue EPT-2030 exists in Jira
  WHEN tool is called with key="EPT-2030"
  THEN response includes all fields
  AND link is "https://fxsolutions.atlassian.net/browse/EPT-2030"

Scenario: Issue não existe
  GIVEN issue EPT-9999 does not exist
  WHEN tool is called with key="EPT-9999"
  THEN returns error with 404 status
```

---

### Tool: jira_search_issues

**Purpose**: Buscar múltiplas issues usando JQL (Jira Query Language).

**Behavior**:
- GIVEN uma query JQL válida
- WHEN o tool é chamado
- THEN deve retornar lista de issues que correspondem à query
- AND deve respeitar o limite de max_results
- AND deve incluir total de issues encontradas

**Input Schema**:
```json
{
  "type": "object",
  "properties": {
    "jql": {
      "type": "string",
      "description": "Jira Query Language query",
      "examples": [
        "project = EPT AND status = Open",
        "assignee = currentUser() ORDER BY priority DESC",
        "created >= -7d"
      ]
    },
    "max_results": {
      "type": "number",
      "description": "Máximo de resultados",
      "default": 50,
      "minimum": 1,
      "maximum": 100
    }
  },
  "required": ["jql"]
}
```

**Output Schema**:
```json
{
  "total": "number",         // Total de issues encontradas
  "count": "number",         // Quantidade retornada
  "issues": [
    {
      "key": "string",
      "summary": "string",
      "status": "string",
      "priority": "string",
      "assignee": "string|null",
      "created": "ISO8601"
    }
  ]
}
```

**Error Cases**:
- JQL inválido: `{"error": "Invalid JQL: [details]"}`
- API deprecada (410): `{"error": "API endpoint deprecated, migrate to v3"}`

**Examples**:

```gherkin
Scenario: Buscar issues abertas do projeto
  GIVEN project EPT has 43 open issues
  WHEN tool is called with jql="project = EPT AND status != Done" and max_results=10
  THEN returns 10 issues
  AND total is 43

Scenario: JQL inválido
  GIVEN jql query has syntax error
  WHEN tool is called with jql="project = [INVALID"
  THEN returns error explaining JQL syntax issue
```

---

### Tool: jira_create_issue

**Purpose**: Criar nova issue no Jira.

**Behavior**:
- GIVEN project key válido e summary preenchido
- WHEN o tool é chamado
- THEN deve criar issue no Jira
- AND deve retornar key da issue criada
- AND deve incluir link direto

**Input Schema**:
```json
{
  "type": "object",
  "properties": {
    "project": {
      "type": "string",
      "description": "Project key",
      "pattern": "^[A-Z]+$"
    },
    "summary": {
      "type": "string",
      "description": "Título da issue",
      "minLength": 1
    },
    "description": {
      "type": "string",
      "description": "Descrição detalhada",
      "default": ""
    },
    "issue_type": {
      "type": "string",
      "description": "Tipo da issue",
      "enum": ["Bug", "Task", "Story", "Epic"],
      "default": "Task"
    }
  },
  "required": ["project", "summary"]
}
```

**Output Schema**:
```json
{
  "key": "string",           // Key da issue criada (ex: EPT-2099)
  "link": "URL",             // Link direto
  "message": "string"        // Mensagem de confirmação
}
```

**Error Cases**:
- Projeto não existe: `{"error": "Project XYZ not found"}`
- Sem permissão para criar: `{"error": "No permission to create issues in project EPT"}`
- Issue type inválido: `{"error": "Issue type 'Invalid' not available in project"}`

**Examples**:

```gherkin
Scenario: Criar task simples
  GIVEN user has permission in project EPT
  WHEN tool is called with project="EPT", summary="Implementar feature X"
  THEN issue is created with type Task
  AND returns new issue key like EPT-2099

Scenario: Criar bug com descrição
  GIVEN user has permission in project EPT
  WHEN tool is called with project="EPT", summary="Bug X", description="Details...", issue_type="Bug"
  THEN issue is created with type Bug
  AND description is properly set
```

---

### Tool: jira_add_comment

**Purpose**: Adicionar comentário em issue existente.

**Behavior**:
- GIVEN issue key válida e comentário não vazio
- WHEN o tool é chamado
- THEN deve adicionar comentário à issue
- AND deve retornar confirmação com link

**Input Schema**:
```json
{
  "type": "object",
  "properties": {
    "key": {
      "type": "string",
      "description": "Issue key"
    },
    "comment": {
      "type": "string",
      "description": "Texto do comentário",
      "minLength": 1
    }
  },
  "required": ["key", "comment"]
}
```

**Output Schema**:
```json
{
  "message": "string",       // Confirmação
  "link": "URL"             // Link para a issue
}
```

**Error Cases**:
- Issue não encontrada: `{"error": "Issue not found"}`
- Sem permissão: `{"error": "No permission to comment on this issue"}`

**Examples**:

```gherkin
Scenario: Adicionar comentário válido
  GIVEN issue EPT-2030 exists
  WHEN tool is called with key="EPT-2030", comment="Problema resolvido"
  THEN comment is added to issue
  AND returns success message

Scenario: Comentário vazio
  GIVEN issue EPT-2030 exists
  WHEN tool is called with key="EPT-2030", comment=""
  THEN returns validation error
```

---

## Non-Functional Requirements

### Performance
- Response time < 2s for get_issue (single HTTP request)
- Response time < 3s for search_issues (may include pagination)
- Response time < 4s for create_issue (includes validation)

### Reliability
- Retry logic for transient failures (5xx errors)
- Graceful degradation if API v3 unavailable (fallback to v2 when possible)
- Clear error messages for all failure scenarios

### Security
- API token stored in environment variables only
- Never log or expose API tokens in responses
- Use HTTPS for all Jira API calls
- Follow Jira Cloud security best practices

### Compatibility
- Python 3.12+
- `mcp` SDK 1.26.0+
- Jira Cloud REST API v2/v3
- Works with Cursor, Claude Desktop, Cline (any MCP-compliant client)

---

## Testing Requirements

### Unit Tests
- ✅ Test each tool with valid inputs
- ✅ Test error cases (404, 401, 403, invalid JQL)
- ✅ Test input validation
- ✅ Test JSON parsing errors

### Integration Tests
- ✅ Test against real Jira instance
- ✅ Test MCP protocol communication (stdio)
- ✅ Test tool registration and discovery
- ✅ Test concurrent requests handling

### Test Scenarios (from tests/test_mcp_client.py)
```python
# Scenario 1: Get single issue
assert tool("jira_get_issue", {"key": "EPT-2030"})["key"] == "EPT-2030"

# Scenario 2: Search with JQL
result = tool("jira_search_issues", {"jql": "project = EPT", "max_results": 5})
assert result["count"] <= 5
assert "total" in result

# Scenario 3: Create issue (optional, modifies Jira)
# result = tool("jira_create_issue", {"project": "EPT", "summary": "Test"})
# assert result["key"].startswith("EPT-")

# Scenario 4: Add comment (optional, modifies Jira)
# result = tool("jira_add_comment", {"key": "EPT-2030", "comment": "Test comment"})
# assert "message" in result
```

---

## Configuration

### Environment Variables
```bash
JIRA_URL=https://fxsolutions.atlassian.net
JIRA_EMAIL=marcos.gomes@ebury.com
JIRA_API_TOKEN=<token_from_atlassian>
```

### MCP Client Configuration
```json
{
  "mcpServers": {
    "jira-python": {
      "command": "python3",
      "args": ["/path/to/skills/jira_assistant/server/mcp_server_jira.py"],
      "env": {
        "JIRA_URL": "https://fxsolutions.atlassian.net",
        "JIRA_EMAIL": "user@company.com",
        "JIRA_API_TOKEN": "token_here"
      }
    }
  }
}
```

---

## Change Log

### 2026-03-16 - v1.0.0 (Initial Stable Release)
- ✅ Implemented 4 core tools (get, search, create, comment)
- ✅ Full MCP protocol support via stdio
- ✅ Jira Cloud API v2/v3 integration
- ✅ Comprehensive error handling
- ✅ Integration tests with real Jira instance
- ✅ Documentation and examples

---

## Related Specs

- **Agent Skill**: [`SKILL.md`](../SKILL.md) - Instructions for AI agents
- **Implementation**: [`server/mcp_server_jira.py`](../server/mcp_server_jira.py)
- **Tests**: [`tests/test_mcp_client.py`](../tests/test_mcp_client.py)
- **OpenSpec Methodology**: [`/openspec/README.md`](/openspec/README.md)
