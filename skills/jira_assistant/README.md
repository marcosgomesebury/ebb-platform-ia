# Jira Assistant Skill

**Version**: 1.0.0  
**Author**: Marcos Gomes  
**License**: CC-BY-4.0

## Overview

Direct REST API integration with Atlassian Jira - no external MCP servers required.

## Features

- ✓ Search issues with JQL
- ✓ Create issues (Task, Bug, Epic, Subtask)
- ✓ Update issue fields
- ✓ Transition issue status
- ✓ Add comments
- ✓ Get issue details

## Installation

```bash
cd skills/jira_assistant
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your credentials
```

## Configuration

### Get API Token

1. Go to https://id.atlassian.com/manage-profile/security/api-tokens
2. Click "Create API token"
3. Copy token to `.env` file

### Environment Variables

```env
JIRA_URL=https://ebury.atlassian.net
JIRA_EMAIL=your.email@ebury.com
JIRA_API_TOKEN=your_token_here
JIRA_PROJECT_KEY=EPT
```

## Usage

### With AI Agent

Activated automatically when you say:
- "Create a Jira ticket for..."
- "Search Jira issues about..."
- "Update EPT-123 status to Done"
- "Add comment to EPT-456"

### Standalone

```bash
python main.py
```

### As Library

```python
from main import JiraClient

client = JiraClient()

# Search issues
issues = client.search_issues("project = EPT AND assignee = currentUser()")

# Create issue
issue = client.create_issue(
    summary="Implement feature X",
    description="Detailed description here",
    issue_type="Task",
    priority="High"
)
print(f"Created: {issue['key']}")

# Transition
client.transition_issue("EPT-123", "Done")

# Add comment
client.add_comment("EPT-123", "Implementation completed")
```

## API Examples

### Search with JQL

```python
# My open issues
jql = "project = EPT AND assignee = currentUser() AND status != Done"
issues = client.search_issues(jql)

# Recent issues
jql = "project = EPT AND created >= -7d ORDER BY created DESC"
issues = client.search_issues(jql, max_results=10)

# Issues in sprint
jql = "project = EPT AND sprint in openSprints()"
issues = client.search_issues(jql)
```

### Create Issue

```python
issue = client.create_issue(
    summary="Fix authentication bug",
    description="Users unable to log in with SSO",
    issue_type="Bug",
    priority="High"
)
# Returns: {"key": "EPT-789", "id": "12345", "self": "https://..."}
```

### Update Issue

```python
client.update_issue("EPT-123", {
    "assignee": {"accountId": "123456:abcdef"},
    "priority": {"name": "Critical"}
})
```

### Transition Status

```python
# Available transitions: To Do → In Progress → Done
client.transition_issue("EPT-123", "In Progress")
client.transition_issue("EPT-123", "Done")
```

## Common JQL Queries

```jql
# My work
assignee = currentUser() AND status != Done

# Team work
project = EPT AND status = "In Progress"

# Recent bugs
project = EPT AND issuetype = Bug AND created >= -7d

# Blocked issues
project = EPT AND status = Blocked

# High priority
project = EPT AND priority = High ORDER BY created DESC

# Sprint issues
project = EPT AND sprint in openSprints()

# Unassigned
project = EPT AND assignee is EMPTY

# Search by text
project = EPT AND text ~ "authentication"
```

## Error Handling

### Authentication Failed (401)
```
❌ API error: 401 Unauthorized
Authentication failed. Check JIRA_EMAIL and JIRA_API_TOKEN
```

**Solution**: Verify credentials in `.env`, generate new API token if needed.

### Project Not Found (404)
```
❌ API error: 404 Not Found
Project 'EPT' not found or no access
```

**Solution**: Verify project key, check access permissions in Jira.

### Invalid Transition
```
ValueError: Transition 'Done' not found. Available: ['To Do', 'In Progress', 'Complete']
```

**Solution**: Use exact transition name from available options.

## Security

- **Never commit `.env`** - Contains API token
- **Token permissions**: Token inherits your Jira permissions
- **Rotate tokens**: Regenerate periodically
- **Use workspace rules**: Store project config in `.cursor/rules/jira-config.mdc`

## Documentation

- [SKILL.md](SKILL.md) - Agent instructions
- [Jira REST API v3](https://developer.atlassian.com/cloud/jira/platform/rest/v3/)
- [JQL Reference](https://support.atlassian.com/jira-service-management-cloud/docs/use-advanced-search-with-jira-query-language-jql/)

## Differences from MCP Version

This skill uses **direct REST API** instead of external MCP servers:

| Aspect | MCP Version | This Version |
|--------|-------------|--------------|
| Dependencies | Atlassian MCP Server | requests library |
| Setup | MCP server config | Just .env file |
| Authentication | MCP handles | Direct API token |
| Search | Rovo Search | JQL queries |
| Complexity | Lower (abstracted) | Higher (explicit) |
| Control | Limited | Full API access |

## Contributing

See [../../docs/CONTRIBUTING.md](../../docs/CONTRIBUTING.md)

## License

CC-BY-4.0 - See [LICENSE](../../LICENSE)
