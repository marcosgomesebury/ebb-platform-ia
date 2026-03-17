#!/usr/bin/env python3
"""
Servidor MCP Python para Slack Web API

Este é um servidor MCP (Model Context Protocol) para integração com Slack,
permitindo que agentes de IA enviem mensagens, listem canais, façam upload
de arquivos e interajam com workspaces Slack.

Uso:
    python3 mcp_server_slack.py

Configuração no cliente MCP (ex: ~/.cursor/mcp.json):
    {
      "mcpServers": {
        "slack": {
          "command": "python3",
          "args": ["/caminho/para/mcp_server_slack.py"],
          "env": {
            "SLACK_BOT_TOKEN": "xoxb-your-bot-token",
            "SLACK_WORKSPACE": "ebury-brazil"
          }
        }
      }
    }
"""

import os
import sys
import json
import asyncio
from typing import Any, Optional
from pathlib import Path
from dotenv import load_dotenv

# Importar SDK MCP Python
try:
    from mcp.server import Server
    from mcp.types import Tool, TextContent
    import mcp.server.stdio
except ImportError:
    print("❌ Erro: SDK MCP não instalado", file=sys.stderr)
    print("   Instale com: pip install mcp", file=sys.stderr)
    sys.exit(1)

# Importar Slack SDK
try:
    from slack_sdk import WebClient
    from slack_sdk.errors import SlackApiError
except ImportError:
    print("❌ Erro: Slack SDK não instalado", file=sys.stderr)
    print("   Instale com: pip install slack-sdk", file=sys.stderr)
    sys.exit(1)

# Carregar credenciais
load_dotenv()
SLACK_BOT_TOKEN = os.getenv('SLACK_BOT_TOKEN')
SLACK_WORKSPACE = os.getenv('SLACK_WORKSPACE', 'ebury-brazil')

if not SLACK_BOT_TOKEN:
    print("❌ Erro: SLACK_BOT_TOKEN deve estar definido", file=sys.stderr)
    print("   Configure no .env ou como variável de ambiente", file=sys.stderr)
    sys.exit(1)


class SlackMCPServer:
    """Servidor MCP para Slack Web API"""
    
    def __init__(self):
        self.server = Server("slack-python-mcp")
        self.client = WebClient(token=SLACK_BOT_TOKEN)
        self.workspace = SLACK_WORKSPACE
        
        # Registrar handlers
        self._register_handlers()
    
    def _register_handlers(self):
        """Registrar ferramentas MCP"""
        
        @self.server.list_tools()
        async def list_tools() -> list[Tool]:
            """Lista todas as ferramentas disponíveis"""
            return [
                Tool(
                    name="slack_post_message",
                    description="Enviar mensagem para um canal ou usuário do Slack",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "channel": {
                                "type": "string",
                                "description": "ID ou nome do canal (ex: 'C1234567890' ou '#general')"
                            },
                            "text": {
                                "type": "string",
                                "description": "Texto da mensagem (suporta markdown do Slack)"
                            },
                            "thread_ts": {
                                "type": "string",
                                "description": "Opcional: responder em thread com este timestamp"
                            },
                            "notify_channel": {
                                "type": "boolean",
                                "description": "Notificar @channel",
                                "default": False
                            }
                        },
                        "required": ["channel", "text"]
                    }
                ),
                Tool(
                    name="slack_list_channels",
                    description="Listar todos os canais do workspace",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "types": {
                                "type": "string",
                                "description": "Tipos de canal: 'public_channel', 'private_channel', 'im', 'mpim'",
                                "default": "public_channel"
                            },
                            "limit": {
                                "type": "number",
                                "description": "Máximo de canais a retornar",
                                "default": 100
                            }
                        }
                    }
                ),
                Tool(
                    name="slack_get_channel_history",
                    description="Obter mensagens recentes de um canal",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "channel": {
                                "type": "string",
                                "description": "ID do canal"
                            },
                            "limit": {
                                "type": "number",
                                "description": "Número de mensagens a recuperar",
                                "default": 20
                            }
                        },
                        "required": ["channel"]
                    }
                ),
                Tool(
                    name="slack_upload_file",
                    description="Fazer upload de um arquivo para um canal",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "channel": {
                                "type": "string",
                                "description": "ID ou nome do canal"
                            },
                            "file_path": {
                                "type": "string",
                                "description": "Caminho local do arquivo para upload"
                            },
                            "title": {
                                "type": "string",
                                "description": "Título do arquivo"
                            },
                            "comment": {
                                "type": "string",
                                "description": "Comentário inicial"
                            }
                        },
                        "required": ["channel", "file_path"]
                    }
                ),
                Tool(
                    name="slack_search_users",
                    description="Buscar usuários por email ou nome",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "Email ou nome de exibição"
                            }
                        },
                        "required": ["query"]
                    }
                )
            ]
        
        @self.server.call_tool()
        async def call_tool(name: str, arguments: Any) -> list[TextContent]:
            """Executar ferramenta solicitada"""
            try:
                if name == "slack_post_message":
                    result = await self._post_message(arguments)
                elif name == "slack_list_channels":
                    result = await self._list_channels(arguments)
                elif name == "slack_get_channel_history":
                    result = await self._get_channel_history(arguments)
                elif name == "slack_upload_file":
                    result = await self._upload_file(arguments)
                elif name == "slack_search_users":
                    result = await self._search_users(arguments)
                else:
                    raise ValueError(f"Ferramenta desconhecida: {name}")
                
                return [TextContent(
                    type="text",
                    text=json.dumps(result, indent=2, ensure_ascii=False)
                )]
            
            except Exception as e:
                error_msg = f"Erro ao executar {name}: {str(e)}"
                print(error_msg, file=sys.stderr)
                return [TextContent(
                    type="text",
                    text=json.dumps({"error": error_msg}, ensure_ascii=False)
                )]
    
    async def _post_message(self, args: dict) -> dict:
        """Enviar mensagem para canal"""
        channel = args["channel"]
        text = args["text"]
        thread_ts = args.get("thread_ts")
        notify_channel = args.get("notify_channel", False)
        
        # Adicionar @channel se solicitado
        if notify_channel and not text.startswith("<!channel>"):
            text = f"<!channel> {text}"
        
        try:
            response = self.client.chat_postMessage(
                channel=channel,
                text=text,
                thread_ts=thread_ts
            )
            
            return {
                "ok": True,
                "channel": response["channel"],
                "ts": response["ts"],
                "message": {
                    "text": text,
                    "user": response.get("message", {}).get("user")
                }
            }
        
        except SlackApiError as e:
            return {
                "ok": False,
                "error": e.response["error"],
                "message": str(e)
            }
    
    async def _list_channels(self, args: dict) -> dict:
        """Listar canais do workspace"""
        types = args.get("types", "public_channel")
        limit = args.get("limit", 100)
        
        try:
            response = self.client.conversations_list(
                types=types,
                limit=limit
            )
            
            channels = []
            for channel in response["channels"]:
                channels.append({
                    "id": channel["id"],
                    "name": channel["name"],
                    "is_private": channel.get("is_private", False),
                    "num_members": channel.get("num_members", 0),
                    "topic": channel.get("topic", {}).get("value", ""),
                    "purpose": channel.get("purpose", {}).get("value", "")
                })
            
            return {
                "ok": True,
                "channels": channels,
                "total": len(channels)
            }
        
        except SlackApiError as e:
            return {
                "ok": False,
                "error": e.response["error"],
                "message": str(e)
            }
    
    async def _get_channel_history(self, args: dict) -> dict:
        """Obter histórico de mensagens do canal"""
        channel = args["channel"]
        limit = args.get("limit", 20)
        
        try:
            response = self.client.conversations_history(
                channel=channel,
                limit=limit
            )
            
            messages = []
            for msg in response["messages"]:
                messages.append({
                    "type": msg.get("type"),
                    "user": msg.get("user"),
                    "text": msg.get("text"),
                    "ts": msg.get("ts"),
                    "thread_ts": msg.get("thread_ts")
                })
            
            return {
                "ok": True,
                "messages": messages,
                "total": len(messages)
            }
        
        except SlackApiError as e:
            return {
                "ok": False,
                "error": e.response["error"],
                "message": str(e)
            }
    
    async def _upload_file(self, args: dict) -> dict:
        """Fazer upload de arquivo"""
        channel = args["channel"]
        file_path = args["file_path"]
        title = args.get("title", Path(file_path).name)
        comment = args.get("comment", "")
        
        try:
            # Verificar se arquivo existe
            if not os.path.exists(file_path):
                return {
                    "ok": False,
                    "error": "file_not_found",
                    "message": f"Arquivo não encontrado: {file_path}"
                }
            
            response = self.client.files_upload_v2(
                channel=channel,
                file=file_path,
                title=title,
                initial_comment=comment
            )
            
            file_info = response.get("file", {})
            
            return {
                "ok": True,
                "file": {
                    "id": file_info.get("id"),
                    "name": file_info.get("name"),
                    "title": file_info.get("title"),
                    "url": file_info.get("url_private"),
                    "size": file_info.get("size")
                }
            }
        
        except SlackApiError as e:
            return {
                "ok": False,
                "error": e.response["error"],
                "message": str(e)
            }
    
    async def _search_users(self, args: dict) -> dict:
        """Buscar usuários"""
        query = args["query"].lower()
        
        try:
            response = self.client.users_list()
            
            users = []
            for member in response["members"]:
                # Buscar por nome, email ou ID
                profile = member.get("profile", {})
                email = profile.get("email", "").lower()
                real_name = profile.get("real_name", "").lower()
                display_name = profile.get("display_name", "").lower()
                
                if (query in email or 
                    query in real_name or 
                    query in display_name or
                    query in member.get("name", "").lower()):
                    
                    users.append({
                        "id": member["id"],
                        "name": member.get("name"),
                        "real_name": profile.get("real_name"),
                        "display_name": profile.get("display_name"),
                        "email": profile.get("email"),
                        "is_bot": member.get("is_bot", False)
                    })
            
            return {
                "ok": True,
                "users": users,
                "total": len(users)
            }
        
        except SlackApiError as e:
            return {
                "ok": False,
                "error": e.response["error"],
                "message": str(e)
            }
    
    async def run(self):
        """Iniciar servidor MCP"""
        async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
            await self.server.run(
                read_stream,
                write_stream,
                self.server.create_initialization_options()
            )


async def main():
    """Função principal"""
    print(f"🚀 Iniciando Slack MCP Server para workspace: {SLACK_WORKSPACE}", file=sys.stderr)
    server = SlackMCPServer()
    await server.run()


if __name__ == "__main__":
    asyncio.run(main())
