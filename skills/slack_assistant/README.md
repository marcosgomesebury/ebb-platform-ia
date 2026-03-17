# Slack Assistant MCP Server

Model Context Protocol (MCP) server for Slack workspace integration, enabling AI agents to send messages, manage channels, and interact with Slack APIs.

## Features

✅ **Send Messages** - Post messages to channels or users  
✅ **List Channels** - Get all workspace channels  
✅ **Get History** - Retrieve channel message history  
✅ **Upload Files** - Share files to channels  
✅ **Search Users** - Find users by email or name  
✅ **Thread Support** - Reply to messages in threads  
✅ **Error Handling** - Robust error handling and retries  

## Quick Start

### 1. Install Dependencies

```bash
cd skills/slack_assistant
pip install -r requirements.txt
```

### 2. Configure Slack Bot

1. Go to https://api.slack.com/apps
2. Create a new app or select existing
3. Navigate to **OAuth & Permissions**
4. Add these Bot Token Scopes:
   - `chat:write`
   - `channels:read`
   - `channels:history`
   - `files:write`
   - `users:read`
   - `users:read.email`
5. Install app to workspace
6. Copy **Bot User OAuth Token**

### 3. Set Environment Variables

```bash
cp .env.example .env
# Edit .env with your bot token
```

### 4. Configure MCP Client

Add to `~/.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "slack": {
      "command": "python3",
      "args": ["/home/marcosgomes/Projects/ebb-platform-ia/skills/slack_assistant/server/mcp_server_slack.py"],
      "env": {
        "SLACK_BOT_TOKEN": "xoxb-your-token-here",
        "SLACK_WORKSPACE": "ebury-brazil"
      }
    }
  }
}
```

### 5. Test the Server

```bash
python3 server/mcp_server_slack.py
```

## Usage Examples

### Python Direct Usage

```python
from slack_assistant.main import SlackClient

# Initialize client
slack = SlackClient()

# Send message
slack.post_message(
    channel="#engineering",
    text="Deployment completed! 🚀"
)

# List channels
channels = slack.list_channels()
for channel in channels:
    print(f"{channel['name']}: {channel['num_members']} members")

# Upload file
slack.upload_file(
    channel="#docs",
    file_path="report.pdf",
    title="Q1 Report"
)
```

### MCP Tool Usage

When using through an MCP agent:

```
Agent: "Send a message to #engineering saying deployment is complete"
→ Uses: slack_post_message tool

Agent: "What Slack channels are available?"
→ Uses: slack_list_channels tool

Agent: "Upload this log file to #debugging"
→ Uses: slack_upload_file tool
```

## Testing

### Unit Tests

```bash
pytest tests/test_slack_client.py -v
```

### Integration Tests

```bash
# Requires real Slack workspace
export SLACK_BOT_TOKEN=xoxb-your-token
pytest tests/test_integration.py -v
```

### Test in Isolated Channel

Create a test channel `#test-mcp-slack` for safe testing.

## Architecture

```
slack_assistant/
├── server/
│   ├── mcp_server_slack.py      # Main MCP server
│   └── slack_client.py           # Slack API wrapper
├── tests/
│   ├── test_slack_client.py
│   └── test_mcp_integration.py
├── examples/
│   ├── post_message.py
│   └── upload_file.py
├── .env.example
├── requirements.txt
├── README.md
└── SKILL.md
```

## Troubleshooting

### Bot Not in Channel

**Error**: `not_in_channel`

**Fix**: Add bot to channel:
```
/invite @YourBotName
```

### Invalid Token

**Error**: `invalid_auth`

**Fix**: 
1. Verify token starts with `xoxb-`
2. Check token hasn't expired
3. Reinstall app to workspace

### Rate Limiting

**Error**: `rate_limited`

**Fix**: Implement delays between requests:
```python
import time
slack.post_message(channel="#ch1", text="msg1")
time.sleep(1)  # Wait 1 second
slack.post_message(channel="#ch2", text="msg2")
```

## Security

⚠️ **IMPORTANT**: Never commit `.env` file or expose bot tokens

- Store tokens in `.env` (git-ignored)
- Don't log tokens in error messages
- Use environment variables for CI/CD
- Rotate tokens if compromised

## Integration with Other Skills

### With Jira Assistant

```python
from jira_assistant.main import JiraClient
from slack_assistant.main import SlackClient

jira = JiraClient()
slack = SlackClient()

# Create issue and notify
issue = jira.create_issue(project="EPT", summary="Fix bug")
slack.post_message(
    channel="#platform-team",
    text=f"✅ Created: {issue['key']} - {issue['summary']}"
)
```

### With Kubernetes Debug

```python
from kubernetes_debug.main import K8sClient
from slack_assistant.main import SlackClient

k8s = K8sClient()
slack = SlackClient()

# Get pod status and alert
pods = k8s.get_pods(namespace="production")
failing = [p for p in pods if p['status'] != 'Running']

if failing:
    slack.post_message(
        channel="#alerts-prod",
        text=f"🚨 {len(failing)} pods failing in production!",
        notify_channel=True
    )
```

## Roadmap

### Phase 1 (Current) - Core Messaging
- [x] Post messages
- [x] List channels
- [ ] Get channel history
- [ ] Upload files
- [ ] Search users

### Phase 2 - Advanced Features
- [ ] Interactive components (buttons)
- [ ] Slash commands
- [ ] Real-time events (WebSocket)
- [ ] Multi-workspace support

### Phase 3 - Enterprise
- [ ] Message scheduling
- [ ] Analytics and reporting
- [ ] Workflow builder integration
- [ ] Admin controls

## Contributing

1. Create feature branch: `git checkout -b feat/your-feature`
2. Make changes and test
3. Run tests: `pytest tests/`
4. Format code: `black .`
5. Submit for review

## License

CC-BY-4.0 - Marcos Gomes

## References

- [Slack Web API](https://api.slack.com/web)
- [Python Slack SDK](https://slack.dev/python-slack-sdk/)
- [MCP Protocol](https://modelcontextprotocol.io/)
- [SKILL.md](SKILL.md) - Full skill documentation
