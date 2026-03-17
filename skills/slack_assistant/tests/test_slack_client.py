"""
Unit tests for Slack MCP Server

Run with:
    pytest tests/test_slack_client.py -v
"""

import pytest
import os
from unittest.mock import Mock, patch, AsyncMock
from slack_sdk.errors import SlackApiError


@pytest.fixture
def mock_slack_client():
    """Mock Slack WebClient"""
    with patch('slack_sdk.WebClient') as mock:
        yield mock


@pytest.fixture
def mock_env():
    """Mock environment variables"""
    with patch.dict(os.environ, {
        'SLACK_BOT_TOKEN': 'xoxb-test-token',
        'SLACK_WORKSPACE': 'test-workspace'
    }):
        yield


class TestSlackPostMessage:
    """Test slack_post_message tool"""
    
    @pytest.mark.asyncio
    async def test_post_simple_message(self, mock_slack_client, mock_env):
        """Test posting a simple message"""
        # Setup mock response
        mock_response = {
            'ok': True,
            'channel': 'C1234567890',
            'ts': '1234567890.123456',
            'message': {'text': 'Test message', 'user': 'U1234567890'}
        }
        mock_slack_client.return_value.chat_postMessage.return_value = mock_response
        
        # Import after mocking
        from server.mcp_server_slack import SlackMCPServer
        
        server = SlackMCPServer()
        result = await server._post_message({
            'channel': '#test',
            'text': 'Test message'
        })
        
        assert result['ok'] is True
        assert result['channel'] == 'C1234567890'
        assert 'ts' in result
    
    @pytest.mark.asyncio
    async def test_post_message_with_channel_notify(self, mock_slack_client, mock_env):
        """Test posting message with @channel notification"""
        mock_response = {
            'ok': True,
            'channel': 'C1234567890',
            'ts': '1234567890.123456'
        }
        mock_slack_client.return_value.chat_postMessage.return_value = mock_response
        
        from server.mcp_server_slack import SlackMCPServer
        
        server = SlackMCPServer()
        result = await server._post_message({
            'channel': '#alerts',
            'text': 'Important alert',
            'notify_channel': True
        })
        
        assert result['ok'] is True
        # Verify that <!channel> was added
        call_args = mock_slack_client.return_value.chat_postMessage.call_args
        assert '<!channel>' in call_args[1]['text']
    
    @pytest.mark.asyncio
    async def test_post_message_error(self, mock_slack_client, mock_env):
        """Test error handling when posting fails"""
        # Setup mock to raise error
        mock_slack_client.return_value.chat_postMessage.side_effect = SlackApiError(
            message="not_in_channel",
            response={"error": "not_in_channel"}
        )
        
        from server.mcp_server_slack import SlackMCPServer
        
        server = SlackMCPServer()
        result = await server._post_message({
            'channel': '#restricted',
            'text': 'Test'
        })
        
        assert result['ok'] is False
        assert result['error'] == 'not_in_channel'


class TestSlackListChannels:
    """Test slack_list_channels tool"""
    
    @pytest.mark.asyncio
    async def test_list_public_channels(self, mock_slack_client, mock_env):
        """Test listing public channels"""
        mock_response = {
            'ok': True,
            'channels': [
                {
                    'id': 'C1234567890',
                    'name': 'general',
                    'is_private': False,
                    'num_members': 42,
                    'topic': {'value': 'General discussion'},
                    'purpose': {'value': 'Company-wide announcements'}
                },
                {
                    'id': 'C9876543210',
                    'name': 'engineering',
                    'is_private': False,
                    'num_members': 15,
                    'topic': {'value': 'Engineering team'},
                    'purpose': {'value': 'Technical discussions'}
                }
            ]
        }
        mock_slack_client.return_value.conversations_list.return_value = mock_response
        
        from server.mcp_server_slack import SlackMCPServer
        
        server = SlackMCPServer()
        result = await server._list_channels({
            'types': 'public_channel',
            'limit': 100
        })
        
        assert result['ok'] is True
        assert result['total'] == 2
        assert len(result['channels']) == 2
        assert result['channels'][0]['name'] == 'general'


class TestSlackGetChannelHistory:
    """Test slack_get_channel_history tool"""
    
    @pytest.mark.asyncio
    async def test_get_history(self, mock_slack_client, mock_env):
        """Test getting channel message history"""
        mock_response = {
            'ok': True,
            'messages': [
                {
                    'type': 'message',
                    'user': 'U1234567890',
                    'text': 'Hello world',
                    'ts': '1234567890.123456'
                },
                {
                    'type': 'message',
                    'user': 'U9876543210',
                    'text': 'How are you?',
                    'ts': '1234567891.123456'
                }
            ]
        }
        mock_slack_client.return_value.conversations_history.return_value = mock_response
        
        from server.mcp_server_slack import SlackMCPServer
        
        server = SlackMCPServer()
        result = await server._get_channel_history({
            'channel': 'C1234567890',
            'limit': 20
        })
        
        assert result['ok'] is True
        assert result['total'] == 2
        assert len(result['messages']) == 2


class TestSlackSearchUsers:
    """Test slack_search_users tool"""
    
    @pytest.mark.asyncio
    async def test_search_users_by_email(self, mock_slack_client, mock_env):
        """Test searching users by email"""
        mock_response = {
            'ok': True,
            'members': [
                {
                    'id': 'U1234567890',
                    'name': 'marcos.gomes',
                    'profile': {
                        'real_name': 'Marcos Gomes',
                        'display_name': 'Marcos',
                        'email': 'marcos.gomes@ebury.com'
                    },
                    'is_bot': False
                },
                {
                    'id': 'U9876543210',
                    'name': 'john.doe',
                    'profile': {
                        'real_name': 'John Doe',
                        'display_name': 'John',
                        'email': 'john.doe@ebury.com'
                    },
                    'is_bot': False
                }
            ]
        }
        mock_slack_client.return_value.users_list.return_value = mock_response
        
        from server.mcp_server_slack import SlackMCPServer
        
        server = SlackMCPServer()
        result = await server._search_users({
            'query': 'marcos.gomes@ebury.com'
        })
        
        assert result['ok'] is True
        assert result['total'] >= 1
        assert any(u['email'] == 'marcos.gomes@ebury.com' for u in result['users'])


@pytest.mark.integration
class TestSlackIntegration:
    """Integration tests (require real Slack workspace)"""
    
    def test_real_connection(self):
        """Test real connection to Slack (skip if no token)"""
        token = os.getenv('SLACK_BOT_TOKEN')
        if not token or token.startswith('xoxb-test'):
            pytest.skip("Real Slack token not available")
        
        from slack_sdk import WebClient
        client = WebClient(token=token)
        
        try:
            response = client.auth_test()
            assert response['ok'] is True
        except Exception as e:
            pytest.fail(f"Real Slack connection failed: {e}")
