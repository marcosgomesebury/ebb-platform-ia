---
name: slack_assistant
description: Send Slack messages, list channels, get message history, upload files via MCP server. Auto-detects workspace configuration. Use when user says "send Slack message", "notify channel", "list Slack channels", "upload to Slack". MCP server integration with Slack Web API. Do NOT use for interactive components or slash commands.
license: CC-BY-4.0
metadata:
  author: Marcos Gomes
  version: 1.0.0
  type: mcp-server
  requires:
    - mcp (Python SDK 1.26.0+)
    - slack-sdk
    - python-dotenv
  api:
    - Slack Web API
  mcp_server: server/mcp_server_slack.py
  workspace: ebury-brazil
---

# Slack Assistant Skill

MCP (Model Context Protocol) server for automated Slack messaging and workspace management.

## When to Use

Use this skill when the user asks to:
- **Send messages**: "Send a Slack message to #engineering", "Notify the team about X"
- **List channels**: "Show me Slack channels", "What channels are available"
- **Get history**: "Show recent messages from #general"
- **Upload files**: "Upload this file to Slack", "Share file in #docs"
- **Find users**: "Who is marcos.gomes on Slack"

**Triggers**: "Slack", "message", "notify", "channel", "upload"

**Do NOT use for:**
- Interactive components (buttons, modals)
- Slash commands
- Real-time event subscriptions
- OAuth flows or app installation

## MCP Tools Available

This skill provides 5 MCP tools via `server/mcp_server_slack.py`:

### 1. slack_post_message
Send a message to a Slack channel or user.

**Input**: 
```json
{
  "channel": "#engineering",
  "text": "Deployment completed successfully!",
  "notify_channel": false
}
```

**Returns**: Message timestamp, channel ID, success status

### 2. slack_list_channels
List all channels in the workspace.

**Input**: 
```json
{
  "types": "public_channel",
  "limit": 100
}
```

**Returns**: Array of channels with IDs, names, member counts

### 3. slack_get_channel_history
Get recent messages from a channel.

**Input**: 
```json
{
  "channel": "C1234567890",
  "limit": 20
}
```

**Returns**: Array of messages with text, user, timestamp

### 4. slack_upload_file
Upload a file to a channel.

**Input**: 
```json
{
  "channel": "#docs",
  "file_path": "/path/to/file.pdf",
  "title": "Q1 Report",
  "comment": "Here's the quarterly report"
}
```

**Returns**: File ID, URL, success status

### 5. slack_search_users
Find users by email or name.

**Input**: 
```json
{
  "query": "marcos.gomes@ebury.com"
}
```

**Returns**: Array of matching users with IDs and profiles

## Configuration

### Environment Variables
```bash
SLACK_BOT_TOKEN=xoxb-your-bot-token-here
SLACK_WORKSPACE=ebury-brazil
SLACK_DEFAULT_CHANNEL=C1234567890
```

### MCP Client Setup
Add to `~/.cursor/mcp.json`:
```json
{
  "mcpServers": {
    "slack": {
      "command": "python3",
      "args": ["/absolute/path/to/mcp_server_slack.py"],
      "env": {
        "SLACK_BOT_TOKEN": "xoxb-token",
        "SLACK_WORKSPACE": "ebury-brazil"
      }
    }
  }
}
```

## Usage Examples

### Example 1: Simple Notification
```python
from slack_assistant.main import SlackClient

slack = SlackClient()
slack.post_message(
    channel="#engineering",
    text="🚀 Deployment to production completed!"
)
```

### Example 2: Thread Reply
```python
# Post main message
response = slack.post_message(
    channel="#alerts",
    text="🚨 High memory usage detected"
)

# Reply in thread
slack.post_message(
    channel="#alerts",
    text="Memory: 85% used",
    thread_ts=response['ts']
)
```

### Example 3: Integration with Jira
```python
from jira_assistant.main import JiraClient
from slack_assistant.main import SlackClient

jira = JiraClient()
slack = SlackClient()

# Create issue
issue = jira.create_issue(
    project="EPT",
    summary="Fix database connection"
)

# Notify team
slack.post_message(
    channel="#platform-team",
    text=f"✅ Created issue: {issue['key']} - {issue['summary']}"
)
```

## Permissions Required

Bot token needs these OAuth scopes:
- `chat:write` - Send messages
- `channels:read` - List public channels
- `channels:history` - Read channel messages
- `files:write` - Upload files
- `users:read` - Search users
- `users:read.email` - Read user emails

## Troubleshooting

### Error: "not_in_channel"
**Solution**: Add the bot to the channel first: `/invite @YourBotName`

### Error: "invalid_auth"
**Solution**: Check that `SLACK_BOT_TOKEN` is set correctly and starts with `xoxb-`

### Error: "rate_limited"
**Solution**: Wait 60 seconds between requests or implement exponential backoff

## Development

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Run Tests
```bash
pytest tests/
```

### Test MCP Server Locally
```bash
python3 server/mcp_server_slack.py
```

## References

- [Slack Web API](https://api.slack.com/web)
- [slack-sdk Documentation](https://slack.dev/python-slack-sdk/)
- [MCP Protocol Spec](https://modelcontextprotocol.io/)
