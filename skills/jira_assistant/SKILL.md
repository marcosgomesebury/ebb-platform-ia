---
name: jira_assistant
description: Manage Jira issues and tasks via MCP server - create, update, search, transition status, add comments. Auto-detects project configuration from workspace. Use when user says "create Jira ticket", "check Jira status", "search Jira", "add comment to ticket", "get issue details". MCP server integration with Jira Cloud REST API. Do NOT use for Confluence pages or general project planning.
license: CC-BY-4.0
metadata:
  author: Marcos Gomes
  version: 2.0.0
  type: mcp-server
  requires:
    - mcp (Python SDK 1.26.0+)
    - requests
    - python-dotenv
  api:
    - Atlassian Jira Cloud REST API v2/v3
  mcp_server: server/mcp_server_jira.py
  projects:
    - EPT (Ebury Platform Team)
---

# Jira Assistant Skill

MCP (Model Context Protocol) server for automated Jira issue management.

## When to Use

Use this skill when the user asks to:
- **Get issue details**: "Show me EPT-2030", "What's the status of EPT-1234"
- **Search issues**: "Find my Jira tickets", "List EPT issues about GitOps"
- **Create issues**: "Create a Jira task for X", "Open a bug about Y"
- **Add comments**: "Comment on EPT-2030 that it's resolved"

**Triggers**: "Jira", "ticket", "issue", "EPT-" (project prefix)

**Do NOT use for:**
- Confluence pages or documentation
- General project planning without Jira integration
- Creating technical specs (use docs/ or openspec/)

## MCP Tools Available

This skill provides 4 MCP tools via `server/mcp_server_jira.py`:

### 1. jira_get_issue
Get full details of a specific issue.

**Input**: `{"key": "EPT-2030"}`  
**Returns**: Summary, status, assignee, priority, description, link

### 2. jira_search_issues
Search issues using JQL (Jira Query Language).

**Input**: `{"jql": "project = EPT AND status = Open", "max_results": 10}`  
**Returns**: List of matching issues with key details

### 3. jira_create_issue
Create a new issue in Jira.

**Input**: `{"project": "EPT", "summary": "...", "description": "...", "issue_type": "Task"}`  
**Returns**: New issue key and link

### 4. jira_add_comment
Add a comment to an existing issue.

**Input**: `{"key": "EPT-2030", "comment": "Issue resolved"}`  
**Returns**: Confirmation message

## Configuration

### Auto-Detection Strategy

1. **Check workspace context**: Look for project mentions in conversation
2. **Default to EPT**: Ebury Platform Team (most common)
3. **If unclear**: Ask user to specify project key
4. **Remember**: Store project context for current conversation

### Environment Setup

The MCP server requires these environment variables (configured in MCP client):

```env
JIRA_URL=https://fxsolutions.atlassian.net
JIRA_EMAIL=user@ebury.com
JIRA_API_TOKEN=<token>
```

## Usage Examples

### Example 1: Get Issue Details

**User**: "Show me details of EPT-2030"

**Agent Action**:
1. Detect issue key: EPT-2030
2. Call MCP tool: `jira_get_issue(key="EPT-2030")`
3. Format response

**Output**:
```
✅ EPT-2030: Timeout issue in Tree/JD integration
📊 Status: Concluído
⚡ Priority: Highest
👤 Assignee: Andre Longo
📅 Created: 2026-03-12
🔗 https://fxsolutions.atlassian.net/browse/EPT-2030
```

### Example 2: Search Issues

**User**: "Find open issues in project EPT"

**Agent Action**:
1. Build JQL: `project = EPT AND status != Done`
2. Call MCP tool: `jira_search_issues(jql="...", max_results=10)`
3. Format results

**Output**:
```
Found 5 issues in EPT:

1. EPT-1919: Improve Function Governance Clean
   Status: Code Review | Assignee: Osório Santos

2. EPT-1891: Migration Workloads MoneyFlows
   Status: Code Review | Assignee: Felipe Nicodemos

3. EPT-1829: Tree FX Web Portal - SSL
   Status: Ready for Deployment | Assignee: Leonardo Santos
```

### Example 3: Create Issue

**User**: "Create a task in EPT to implement feature X"

**Agent Action**:
1. Detect project: EPT
2. Extract details: summary, description
3. Call MCP tool: `jira_create_issue(project="EPT", summary="...", issue_type="Task")`

**Output**:
```
✅ Task created: EPT-2099
📝 Summary: Implement feature X
🔗 https://fxsolutions.atlassian.net/browse/EPT-2099
```

### Example 4: Add Comment

**User**: "Add comment to EPT-2030: Issue resolved after restart"

**Agent Action**:
1. Parse issue key: EPT-2030
2. Extract comment text
3. Call MCP tool: `jira_add_comment(key="EPT-2030", comment="...")`

**Output**:
```
✅ Comment added to EPT-2030
```
## JQL (Jira Query Language) Examples

When searching issues, use JQL syntax:

```jql
# Find my assigned issues
project = EPT AND assignee = currentUser() AND status != Done

# Find issues in current sprint
project = EPT AND sprint in openSprints()

# Find recent issues
project = EPT AND created >= -7d ORDER BY created DESC

# Find high priority bugs
project = EPT AND type = Bug AND priority = High

# Find issues by label
project = EPT AND labels = "FinCore"
```

## Best Practices

### When Creating Issues

1. **Be specific**: "Create task for implementing OAuth2" (not "create task")
2. **Include context**: Mention if it's a bug, task, or epic
3. **Provide details**: Description helps assign and prioritize

### When Searching

1. **Use JQL**: More powerful than keywords
2. **Specify project**: Always include `project = EPT`
3. **Order results**: Add `ORDER BY created DESC` for recent first

### When Commenting

1. **Be concise**: One clear sentence
2. **Tag people**: Use @mentions if needed (handled by Jira)
3. **Reference PRs**: Link to GitHub PRs when applicable

## Common Patterns

### Pattern 1: Check Issue Status
```
User: "What's the status of EPT-2030?"
→ Use: jira_get_issue(key="EPT-2030")
```

### Pattern 2: Find My Work
```
User: "Show my open Jira tickets"
→ Use: jira_search_issues(jql="project = EPT AND assignee = currentUser() AND status != Done")
```

### Pattern 3: Create & Track
```
User: "Create task for implementing secrets in GitOps"
→ Use: jira_create_issue(...)
→ Save EPT-XXXX for tracking
```

### Pattern 4: Update Progress
```
User: "Add comment to EPT-2030 that implementation is complete"
→ Use: jira_add_comment(key="EPT-2030", comment="Implementation complete")
```

## Troubleshooting

### Issue Not Found (404)
- Verify issue key format: `PROJECT-NUMBER` (e.g., EPT-2030)
- Check if issue exists in Jira web UI
- Confirm user has access to the project

### Permission Denied (403)
- User may not have access to project
- API token may lack required permissions
- Check Jira user permissions in admin panel

### Invalid JQL
- Use Jira's query builder to validate syntax
- Common mistake: missing quotes around values with spaces
- Use `project = EPT` (not `project = "EPT"`)

## Implementation Details

**MCP Server**: `server/mcp_server_jira.py`  
**Tests**: `tests/test_mcp_client.py`  
**Specs**: `specs/jira-mcp-tools.md`  

**Full documentation**: See [README.md](README.md) for setup and architecture.

## Related Skills

- **kubernetes_debug**: Check if Jira-related services are running
- **ssh_connect**: SSH into servers to check Jira integrations
- **mysql_connect**: Query Jira database (if self-hosted)

## Security Notes

- ✅ API tokens stored in environment variables only
- ✅ Never log or expose tokens in responses
- ✅ Use HTTPS for all Jira API calls
- ✅ Follow principle of least privilege for API permissions
**Permission denied**:
```
❌ Cannot update EPT-1234: Insufficient permissions
Contact: Project admin or request access
```

**Invalid transition**:
```
❌ Cannot transition to 'Done': Missing required fields
Required: Resolution, Time Spent
```

## Tips

- **Be specific**: Use issue keys (EPT-1234) when possible
- **Check status**: Verify issue status before transitioning
- **Add context**: Always add comments when blocking or resolving
- **Link work**: Reference PRs, commits, or related issues
- **Use labels**: Tag issues for better organization (gitops, infrastructure, etc.)
