#!/usr/bin/env python3
"""
Servidor MCP Python para Jira Cloud

Este é um exemplo de servidor MCP (Model Context Protocol) implementado
em Python puro, usando o SDK oficial `mcp`.

Uso:
    python3 mcp_server_jira.py

Configuração no cliente MCP (ex: ~/.cursor/mcp.json):
    {
      "mcpServers": {
        "jira-python": {
          "command": "python3",
          "args": ["/caminho/para/mcp_server_jira.py"],
          "env": {
            "JIRA_URL": "https://fxsolutions.atlassian.net",
            "JIRA_EMAIL": "marcos.gomes@ebury.com",
            "JIRA_API_TOKEN": "seu_token_aqui"
          }
        }
      }
    }
"""

import os
import sys
import json
import asyncio
from typing import Any
import requests
from dotenv import load_dotenv

# Importar SDK MCP Python
try:
    from mcp.server import Server
    from mcp.types import (
        Tool,
        TextContent,
        ImageContent,
        EmbeddedResource,
    )
    import mcp.server.stdio
except ImportError:
    print("❌ Erro: SDK MCP não instalado", file=sys.stderr)
    print("   Instale com: pip install mcp", file=sys.stderr)
    sys.exit(1)

# Carregar credenciais
load_dotenv()
JIRA_URL = os.getenv('JIRA_URL', 'https://fxsolutions.atlassian.net')
JIRA_EMAIL = os.getenv('JIRA_EMAIL')
JIRA_API_TOKEN = os.getenv('JIRA_API_TOKEN')

if not JIRA_EMAIL or not JIRA_API_TOKEN:
    print("❌ Erro: JIRA_EMAIL e JIRA_API_TOKEN devem estar definidos", file=sys.stderr)
    sys.exit(1)


class JiraMCPServer:
    """Servidor MCP para Jira Cloud"""
    
    def __init__(self):
        self.server = Server("jira-python-mcp")
        self.auth = (JIRA_EMAIL, JIRA_API_TOKEN)
        self.headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
        
        # Registrar handlers
        self._register_handlers()
    
    def _register_handlers(self):
        """Registrar ferramentas MCP"""
        
        @self.server.list_tools()
        async def list_tools() -> list[Tool]:
            """Lista todas as ferramentas disponíveis"""
            return [
                Tool(
                    name="jira_get_issue",
                    description="Buscar detalhes de uma issue do Jira por key (ex: EPT-2030)",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "key": {
                                "type": "string",
                                "description": "Issue key (ex: EPT-2030)"
                            }
                        },
                        "required": ["key"]
                    }
                ),
                Tool(
                    name="jira_search_issues",
                    description="Buscar issues usando JQL (Jira Query Language)",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "jql": {
                                "type": "string",
                                "description": "Query JQL (ex: 'project = EPT AND status = Open')"
                            },
                            "max_results": {
                                "type": "number",
                                "description": "Máximo de resultados (padrão: 50)",
                                "default": 50
                            }
                        },
                        "required": ["jql"]
                    }
                ),
                Tool(
                    name="jira_create_issue",
                    description="Criar nova issue no Jira",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "project": {
                                "type": "string",
                                "description": "Project key (ex: EPT)"
                            },
                            "summary": {
                                "type": "string",
                                "description": "Título da issue"
                            },
                            "description": {
                                "type": "string",
                                "description": "Descrição detalhada"
                            },
                            "issue_type": {
                                "type": "string",
                                "description": "Tipo (Bug, Task, Story, etc)",
                                "default": "Task"
                            }
                        },
                        "required": ["project", "summary"]
                    }
                ),
                Tool(
                    name="jira_add_comment",
                    description="Adicionar comentário em uma issue",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "key": {
                                "type": "string",
                                "description": "Issue key"
                            },
                            "comment": {
                                "type": "string",
                                "description": "Texto do comentário"
                            }
                        },
                        "required": ["key", "comment"]
                    }
                )
            ]
        
        @self.server.call_tool()
        async def call_tool(name: str, arguments: Any) -> list[TextContent]:
            """Executar ferramenta MCP"""
            
            try:
                if name == "jira_get_issue":
                    result = self._get_issue(arguments["key"])
                    
                elif name == "jira_search_issues":
                    max_results = arguments.get("max_results", 50)
                    result = self._search_issues(arguments["jql"], max_results)
                    
                elif name == "jira_create_issue":
                    result = self._create_issue(
                        project=arguments["project"],
                        summary=arguments["summary"],
                        description=arguments.get("description", ""),
                        issue_type=arguments.get("issue_type", "Task")
                    )
                    
                elif name == "jira_add_comment":
                    result = self._add_comment(
                        key=arguments["key"],
                        comment=arguments["comment"]
                    )
                    
                else:
                    result = {"error": f"Ferramenta desconhecida: {name}"}
                
                return [TextContent(
                    type="text",
                    text=json.dumps(result, indent=2, ensure_ascii=False)
                )]
                
            except Exception as e:
                return [TextContent(
                    type="text",
                    text=json.dumps({"error": str(e)}, indent=2)
                )]
    
    def _get_issue(self, key: str) -> dict:
        """Buscar issue por key"""
        url = f"{JIRA_URL}/rest/api/2/issue/{key}"
        response = requests.get(url, auth=self.auth, headers=self.headers)
        response.raise_for_status()
        
        issue = response.json()
        return {
            "key": issue['key'],
            "summary": issue['fields']['summary'],
            "status": issue['fields']['status']['name'],
            "type": issue['fields']['issuetype']['name'],
            "priority": issue['fields']['priority']['name'],
            "assignee": issue['fields']['assignee']['displayName'] if issue['fields'].get('assignee') else None,
            "reporter": issue['fields']['reporter']['displayName'],
            "created": issue['fields']['created'],
            "updated": issue['fields']['updated'],
            "description": issue['fields'].get('description', ''),
            "link": f"{JIRA_URL}/browse/{issue['key']}"
        }
    
    def _search_issues(self, jql: str, max_results: int) -> dict:
        """Buscar issues com JQL"""
        url = f"{JIRA_URL}/rest/api/3/search/jql"
        params = {
            'jql': jql,
            'maxResults': max_results,
            'fields': 'key,summary,status,assignee,priority,created'
        }
        
        response = requests.get(url, auth=self.auth, headers=self.headers, params=params)
        
        if response.status_code != 200:
            return {
                "error": f"HTTP {response.status_code}: {response.text[:500]}"
            }
        
        try:
            data = response.json()
        except Exception as e:
            return {
                "error": f"JSON parse error: {str(e)}. Response: {response.text[:500]}"
            }
        
        issues = []
        
        for issue in data.get('issues', []):
            issues.append({
                "key": issue['key'],
                "summary": issue['fields']['summary'],
                "status": issue['fields']['status']['name'],
                "priority": issue['fields']['priority']['name'],
                "assignee": issue['fields']['assignee']['displayName'] if issue['fields'].get('assignee') else None,
                "created": issue['fields']['created']
            })
        
        return {
            "total": data.get('total', len(issues)),
            "count": len(issues),
            "issues": issues
        }
    
    def _create_issue(self, project: str, summary: str, description: str, issue_type: str) -> dict:
        """Criar nova issue"""
        url = f"{JIRA_URL}/rest/api/2/issue"
        
        payload = {
            "fields": {
                "project": {"key": project},
                "summary": summary,
                "description": description,
                "issuetype": {"name": issue_type}
            }
        }
        
        response = requests.post(url, auth=self.auth, headers=self.headers, json=payload)
        response.raise_for_status()
        
        data = response.json()
        return {
            "key": data['key'],
            "link": f"{JIRA_URL}/browse/{data['key']}",
            "message": "Issue criada com sucesso"
        }
    
    def _add_comment(self, key: str, comment: str) -> dict:
        """Adicionar comentário"""
        url = f"{JIRA_URL}/rest/api/2/issue/{key}/comment"
        
        payload = {"body": comment}
        
        response = requests.post(url, auth=self.auth, headers=self.headers, json=payload)
        response.raise_for_status()
        
        return {
            "message": f"Comentário adicionado à issue {key}",
            "link": f"{JIRA_URL}/browse/{key}"
        }
    
    async def run(self):
        """Iniciar servidor MCP via stdio"""
        async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
            await self.server.run(
                read_stream,
                write_stream,
                self.server.create_initialization_options()
            )


async def main():
    """Ponto de entrada principal"""
    print("🚀 Iniciando servidor MCP Jira Python...", file=sys.stderr)
    print(f"📡 URL: {JIRA_URL}", file=sys.stderr)
    print(f"👤 Email: {JIRA_EMAIL}", file=sys.stderr)
    print("✅ Servidor pronto para receber requisições MCP", file=sys.stderr)
    print("", file=sys.stderr)
    
    server = JiraMCPServer()
    await server.run()


if __name__ == "__main__":
    asyncio.run(main())
