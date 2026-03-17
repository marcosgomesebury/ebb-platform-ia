---
name: jira_assistant
description: Manage Jira issues and tasks - create, update, search, transition status, add comments, manage sprints. Auto-detects project configuration from workspace. Use when user says "create Jira ticket", "update sprint", "check Jira status", "transition issue", "search Jira", "add comment to ticket", "assign issue". Integrates with Atlassian MCP tools. Do NOT use for Confluence pages (use confluence skill) or general project planning (use spec-driven skill).
license: CC-BY-4.0
metadata:
  author: Marcos Gomes
  version: 1.0.0
  requires:
    - Atlassian MCP Server
  projects:
    - EPT (Ebury Platform Team)
---

# Jira Assistant Skill

Automated Jira issue management with Atlassian MCP integration.

## When to Use

Use this skill when the user asks to:
- Search for Jira issues or tasks
- Create new Jira issues (Task, Epic, Subtask, Bug)
- Update existing issues (description, assignee, priority)
- Transition issue status (To Do → In Progress → Done)
- Add comments to issues
- Manage sprint tasks
- Query issues with specific criteria (JQL)

**Do NOT use for:**
- Confluence pages or documentation (use confluence-assistant)
- General project planning without Jira (use spec-driven skill)
- Creating technical specs (use spec-driven skill)

## Configuration

### Auto-Detection Strategy

1. **Check workspace configuration**: Look for `.cursor/rules/jira-config.mdc`
2. **If not found**: Use Atlassian MCP search to discover projects
3. **If still unclear**: Ask user to specify project key
4. **Store config**: Remember for current conversation

### Workspace Configuration (Optional)

Create `.cursor/rules/jira-config.mdc`:
```markdown
# Jira Configuration

**Project Key**: EPT
**Project Name**: Ebury Platform Team
**Board URL**: https://ebury.atlassian.net/jira/software/projects/EPT/boards/123
**Default Issue Type**: Task
```

## Workflow

### 1. Search Issues

**Use Rovo Search first** for natural language queries:
```
Search: "Jira issues assigned to me in sprint"
Search: "EPT tickets about GitOps"
```

**Use JQL** for precise queries:
```jql
project = EPT AND status = "In Progress" AND assignee = currentUser()
```

### 2. Create Issues

When user requests a new ticket:

1. **Detect project** (auto or ask)
2. **Determine type**: Task, Epic, Bug, Subtask
3. **Gather details**:
   - Summary (1 sentence)
   - Description (detailed)
   - Priority (if specified)
   - Assignee (default: reporter)
4. **Create issue** via MCP
5. **Confirm** with issue key and URL

**Example**:
```markdown
User: "Create a Jira ticket for implementing secrets in GitOps"

Agent:
1. Detected project: EPT
2. Creating Task...
3. ✓ Created: EPT-1234
   Summary: Implement secrets management in GitOps
   URL: https://ebury.atlassian.net/browse/EPT-1234
```

### 3. Update Issues

**Update fields**:
- Change assignee
- Update description
- Modify priority
- Update labels/components

**Example**:
```
User: "Update EPT-1234 assignee to marcos.gomes"
```

### 4. Transition Status

**Common transitions**:
- To Do → In Progress
- In Progress → Code Review
- Code Review → Done
- Any → Blocked

**Example**:
```
User: "Move EPT-1234 to Done"
```

### 5. Add Comments

**When to comment**:
- Status updates
- Blockers identified
- Additional context
- Links to PRs/commits

**Example**:
```
User: "Add comment to EPT-1234: Implemented in PR #456"
```

## Output Format

Always provide structured output:

**Search results**:
```markdown
Found 3 issues:

1. **EPT-1234** - Implement GitOps secrets
   Status: In Progress | Assignee: Marcos Gomes
   https://ebury.atlassian.net/browse/EPT-1234

2. **EPT-1235** - Update Terraform modules
   Status: To Do | Assignee: Unassigned
   https://ebury.atlassian.net/browse/EPT-1235
```

**Issue created/updated**:
```markdown
✓ Created EPT-1234: Implement GitOps secrets
  Status: To Do
  Assignee: Marcos Gomes
  Priority: High
  URL: https://ebury.atlassian.net/browse/EPT-1234
```

## Common Commands

### Search
```
- "Find my Jira tickets"
- "Search EPT issues about GitOps"
- "Show tickets in current sprint"
```

### Create
```
- "Create Jira ticket for [description]"
- "New bug: [description]"
- "Create epic for [feature]"
```

### Update
```
- "Update EPT-1234 assignee to [user]"
- "Change priority of EPT-1234 to High"
- "Add label 'gitops' to EPT-1234"
```

### Transition
```
- "Move EPT-1234 to In Progress"
- "Mark EPT-1234 as Done"
- "Block EPT-1234"
```

### Comment
```
- "Add comment to EPT-1234: [text]"
- "Comment on EPT-1234 with PR link"
```

## Error Handling

**Issue not found**:
```
❌ Issue EPT-9999 not found
Suggestion: Search for similar issues or verify issue key
```
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
