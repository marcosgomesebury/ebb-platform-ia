# MCP Slack Implementation Proposal

**Date**: March 17, 2026  
**Status**: Proposed  
**Author**: Marcos Gomes  
**Type**: MCP Server Implementation

---

## 1. Overview

### Purpose
Implement a Model Context Protocol (MCP) server for Slack integration, enabling AI agents to interact with Slack workspaces for notifications, channel management, and message operations.

### Scope
- **Post messages** to channels and users
- **List channels** and workspace information
- **Get message history** from channels
- **Upload files** to channels
- **Manage threads** (reply to messages)
- **User lookup** and presence information

### Non-Goals (Phase 1)
- Slash commands or bot interactions
- Interactive components (buttons, modals)
- App installation/OAuth flow (assumes pre-configured bot token)
- Real-time event subscriptions (WebSocket/RTM)

---

## 2. Architecture

### MCP Server Structure
```
skills/slack_assistant/
├── server/
│   └── mcp_server_slack.py          # Main MCP server implementation
├── tests/
│   ├── test_slack_client.py
│   └── test_mcp_integration.py
├── examples/
│   ├── post_message.py
│   ├── list_channels.py
│   └── upload_file.py
├── .env.example
├── .env                              # Git-ignored credentials
├── requirements.txt
├── README.md
└── SKILL.md                          # Skill documentation
```

### Dependencies
```python
# requirements.txt
mcp>=1.26.0                          # MCP Python SDK
slack-sdk>=3.23.0                    # Official Slack SDK
python-dotenv>=1.0.0
requests>=2.31.0
```

---

## 3. MCP Tools/Capabilities

### 3.1 slack_post_message
**Description**: Send a message to a Slack channel or user

**Input Schema**:
```json
{
  "type": "object",
  "properties": {
    "channel": {
      "type": "string",
      "description": "Channel ID or name (e.g., 'C1234567890' or '#general')"
    },
    "text": {
      "type": "string",
      "description": "Message text (Slack markdown supported)"
    },
    "thread_ts": {
      "type": "string",
      "description": "Optional: Reply to thread with this timestamp"
    },
    "notify_channel": {
      "type": "boolean",
      "description": "Notify @channel",
      "default": false
    }
  },
  "required": ["channel", "text"]
}
```

**Output**:
```json
{
  "ok": true,
  "channel": "C1234567890",
  "ts": "1234567890.123456",
  "message": {
    "text": "Message posted successfully",
    "user": "U1234567890"
  }
}
```

---

### 3.2 slack_list_channels
**Description**: List all channels in the workspace

**Input Schema**:
```json
{
  "type": "object",
  "properties": {
    "types": {
      "type": "string",
      "description": "Channel types: 'public_channel', 'private_channel', 'im', 'mpim'",
      "default": "public_channel"
    },
    "limit": {
      "type": "number",
      "description": "Max channels to return",
      "default": 100
    }
  }
}
```

**Output**:
```json
{
  "ok": true,
  "channels": [
    {
      "id": "C1234567890",
      "name": "general",
      "is_private": false,
      "num_members": 42
    }
  ]
}
```

---

### 3.3 slack_get_channel_history
**Description**: Get recent messages from a channel

**Input Schema**:
```json
{
  "type": "object",
  "properties": {
    "channel": {
      "type": "string",
      "description": "Channel ID"
    },
    "limit": {
      "type": "number",
      "description": "Number of messages to retrieve",
      "default": 20
    }
  },
  "required": ["channel"]
}
```

**Output**:
```json
{
  "ok": true,
  "messages": [
    {
      "type": "message",
      "user": "U1234567890",
      "text": "Hello world",
      "ts": "1234567890.123456"
    }
  ]
}
```

---

### 3.4 slack_upload_file
**Description**: Upload a file to a channel

**Input Schema**:
```json
{
  "type": "object",
  "properties": {
    "channel": {
      "type": "string",
      "description": "Channel ID or name"
    },
    "file_path": {
      "type": "string",
      "description": "Local file path to upload"
    },
    "title": {
      "type": "string",
      "description": "File title"
    },
    "comment": {
      "type": "string",
      "description": "Initial comment"
    }
  },
  "required": ["channel", "file_path"]
}
```

---

### 3.5 slack_search_users
**Description**: Find users by email or name

**Input Schema**:
```json
{
  "type": "object",
  "properties": {
    "query": {
      "type": "string",
      "description": "Email or display name"
    }
  },
  "required": ["query"]
}
```

**Output**:
```json
{
  "ok": true,
  "users": [
    {
      "id": "U1234567890",
      "name": "marcos.gomes",
      "real_name": "Marcos Gomes",
      "email": "marcos.gomes@ebury.com"
    }
  ]
}
```

---

## 4. Configuration

### Environment Variables
```bash
# .env.example
SLACK_BOT_TOKEN=xoxb-your-bot-token-here
SLACK_WORKSPACE=ebury-brazil
SLACK_DEFAULT_CHANNEL=C1234567890
```

### MCP Client Configuration
Add to `~/.cursor/mcp.json`:
```json
{
  "mcpServers": {
    "slack": {
      "command": "python3",
      "args": ["/home/marcosgomes/Projects/ebb-platform-ia/skills/slack_assistant/server/mcp_server_slack.py"],
      "env": {
        "SLACK_BOT_TOKEN": "xoxb-your-bot-token-here",
        "SLACK_WORKSPACE": "ebury-brazil"
      }
    }
  }
}
```

---

## 5. Implementation Plan

### Phase 1: Core Messaging (Week 1)
- [ ] Create project structure
- [ ] Implement `mcp_server_slack.py` foundation
- [ ] Implement `slack_post_message` tool
- [ ] Implement `slack_list_channels` tool
- [ ] Write unit tests
- [ ] Create `.env.example` and documentation

### Phase 2: Advanced Features (Week 2)
- [ ] Implement `slack_get_channel_history` tool
- [ ] Implement `slack_upload_file` tool
- [ ] Implement `slack_search_users` tool
- [ ] Add thread support
- [ ] Integration tests with real Slack workspace

### Phase 3: Integration & Documentation (Week 3)
- [ ] Create example scripts
- [ ] Update SKILL.md with usage patterns
- [ ] Add to workspace documentation
- [ ] Integration with existing subagents (e.g., Jira notifications)
- [ ] Performance testing and error handling

---

## 6. Usage Examples

### Example 1: Notify Channel on Jira Issue Creation
```python
# subagents/jira_workflow_agent.py
from skills.jira_assistant.main import JiraClient
from skills.slack_assistant.main import SlackClient

async def create_issue_and_notify(summary: str, channel: str):
    jira = JiraClient()
    slack = SlackClient()
    
    # Create Jira issue
    issue = await jira.create_issue(
        project="EPT",
        summary=summary
    )
    
    # Notify Slack
    await slack.post_message(
        channel=channel,
        text=f"✅ New Jira issue created: [{issue['key']}]({issue['url']}) - {summary}"
    )
    
    return issue
```

### Example 2: Daily Standup Reminder
```python
# Automated daily reminder
async def send_standup_reminder():
    slack = SlackClient()
    
    channels = ["#eng-platform", "#eng-money-flows"]
    
    for channel in channels:
        await slack.post_message(
            channel=channel,
            text="🌅 Good morning! Time for daily standup in 15 minutes.",
            notify_channel=False
        )
```

### Example 3: Error Alert with Thread
```python
# Deployment error notification
async def alert_deployment_error(service_name: str, error_msg: str):
    slack = SlackClient()
    
    # Post main alert
    response = await slack.post_message(
        channel="#alerts-prod",
        text=f"🚨 Deployment failed for {service_name}",
        notify_channel=True
    )
    
    # Add error details in thread
    await slack.post_message(
        channel="#alerts-prod",
        text=f"```\n{error_msg}\n```",
        thread_ts=response['ts']
    )
```

---

## 7. Security Considerations

### Authentication
- Use **Bot User OAuth Token** (`xoxb-*`)
- Store token in `.env` (git-ignored)
- Never log or expose token in error messages

### Permissions Required
Bot token needs these OAuth scopes:
- `chat:write` - Post messages
- `channels:read` - List public channels
- `channels:history` - Read channel history
- `files:write` - Upload files
- `users:read` - Look up user information
- `users:read.email` - Read user emails

### Rate Limiting
- Implement exponential backoff
- Respect Slack API rate limits (1 message/sec per channel)
- Cache channel lists for 5 minutes

---

## 8. Testing Strategy

### Unit Tests
```python
# tests/test_slack_client.py
import pytest
from slack_assistant.server.mcp_server_slack import SlackMCPServer

@pytest.mark.asyncio
async def test_post_message():
    server = SlackMCPServer()
    result = await server.post_message(
        channel="C1234567890",
        text="Test message"
    )
    assert result['ok'] is True
```

### Integration Tests
- Test with real Slack workspace
- Use dedicated test channel (`#test-mcp-integration`)
- Mock Slack API for CI/CD pipeline

---

## 9. Migration from Go Implementation

### Current Go Implementation
Located at: `Ebury-Brazil/ebb-ebury-connect/apps/ebb-wp-hedges/internal/app/gateway/slack/`

**Capabilities**:
- Post message with `@channel` notification
- Uses `github.com/slack-go/slack` library

**Differences**:
- Go implementation is **service-specific** (hedges app)
- Python MCP will be **workspace-wide** tool for AI agents
- MCP provides **broader capabilities** (not just posting)

---

## 10. Success Metrics

### Phase 1 Success Criteria
- [x] MCP server runs without errors
- [x] All 5 tools implemented and tested
- [x] Documentation complete
- [x] Can post messages to channels
- [x] Integration with at least 1 subagent

### Key Performance Indicators
- **Response Time**: < 2 seconds for message posting
- **Reliability**: 99.5% success rate
- **Test Coverage**: > 80% code coverage
- **Documentation**: All tools documented with examples

---

## 11. Future Enhancements (Post-MVP)

### Phase 4+
- [ ] Interactive components (buttons, modals)
- [ ] Slash command integration
- [ ] Real-time event subscriptions
- [ ] Message reaction tools
- [ ] Channel management (create/archive channels)
- [ ] Workflow builder integration
- [ ] Multi-workspace support

---

## 12. Alternatives Considered

### Option 1: Use External Slack MCP from tech-leads-club
**Pros**: Pre-built, maintained by community  
**Cons**: Less customization, external dependency, learning curve

### Option 2: Direct API Integration (No MCP)
**Pros**: Simple, direct control  
**Cons**: No agent integration, manual orchestration

### Option 3: Custom Python MCP (Chosen)
**Pros**: Full control, workspace-specific, agent-friendly  
**Cons**: Maintenance overhead

---

## 13. References

- [Slack API Documentation](https://api.slack.com/web)
- [slack-sdk Python Library](https://github.com/slackapi/python-slack-sdk)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [Existing Go Implementation](../../Ebury-Brazil/ebb-ebury-connect/apps/ebb-wp-hedges/internal/app/gateway/slack/)
- [Jira Assistant MCP Reference](../../skills/jira_assistant/)

---

## 14. Approval & Next Steps

### Required Approvals
- [ ] Technical Lead (Marcos Gomes)
- [ ] Security Review (token handling)
- [ ] Slack workspace admin approval

### Next Steps
1. Create feature branch: `feat/slack-mcp` ✅ (done)
2. Implement Phase 1 (Core Messaging)
3. Code review
4. Deploy to production workspace
5. Update documentation

---

**Estimated Effort**: 3 weeks  
**Priority**: Medium  
**Complexity**: Medium  
**Dependencies**: None (standalone MCP)
