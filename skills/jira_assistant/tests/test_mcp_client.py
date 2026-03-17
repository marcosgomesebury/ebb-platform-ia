#!/usr/bin/env python3
"""
Cliente de teste para o servidor MCP Jira

Este script testa o servidor MCP localmente, simulando o que um
cliente MCP (como Cursor ou Claude Desktop) faria.
"""

import asyncio
import json
import subprocess
import sys
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def test_mcp_server():
    """Testar servidor MCP Jira"""
    
    print("=" * 70)
    print("TESTE: Servidor MCP Jira Python")
    print("=" * 70)
    print()
    
    # Parâmetros do servidor
    server_params = StdioServerParameters(
        command="/home/marcosgomes/Projects/.venv/bin/python",
        args=["../server/mcp_server_jira.py"],
        env=None  # Vai usar o .env local
    )
    
    print("📡 Iniciando servidor MCP...")
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            
            # Inicializar sessão
            await session.initialize()
            print("✅ Servidor MCP iniciado\n")
            
            # Listar ferramentas disponíveis
            print("🔧 Ferramentas disponíveis:")
            tools = await session.list_tools()
            for tool in tools.tools:
                print(f"   • {tool.name}: {tool.description}")
            print()
            
            # Teste 1: Buscar issue EPT-2030
            print("=" * 70)
            print("TESTE 1: Buscar Issue EPT-2030")
            print("=" * 70)
            
            result = await session.call_tool("jira_get_issue", {"key": "EPT-2030"})
            data = json.loads(result.content[0].text)
            
            print(f"✅ Issue encontrada!")
            print(f"📌 Key: {data['key']}")
            print(f"📝 Summary: {data['summary']}")
            print(f"📊 Status: {data['status']}")
            print(f"⚡ Priority: {data['priority']}")
            print(f"👤 Assignee: {data['assignee']}")
            print(f"🔗 Link: {data['link']}")
            print()
            
            # Teste 2: Buscar issues com JQL
            print("=" * 70)
            print("TESTE 2: Buscar Issues com JQL")
            print("=" * 70)
            
            jql = "project = EPT ORDER BY updated DESC"
            result = await session.call_tool("jira_search_issues", {
                "jql": jql,
                "max_results": 5
            })
            data = json.loads(result.content[0].text)
            
            print(f"🔍 JQL: {jql}")
            
            if 'error' in data:
                print(f"❌ Erro: {data['error']}\n")
            else:
                print(f"📊 Total encontrado: {data['total']}")
                print(f"📋 Mostrando: {data['count']} issues\n")
                
                for issue in data['issues']:
                    print(f"   • {issue['key']}: {issue['summary']}")
                    print(f"     Status: {issue['status']} | Assignee: {issue['assignee']}")
                print()
            
            # Teste 3: Adicionar comentário (COMENTAR ESTA PARTE SE NÃO QUISER MODIFICAR)
            """
            print("=" * 70)
            print("TESTE 3: Adicionar Comentário")
            print("=" * 70)
            
            result = await session.call_tool("jira_add_comment", {
                "key": "EPT-2030",
                "comment": "Teste de comentário via MCP Python!"
            })
            data = json.loads(result.content[0].text)
            
            print(f"✅ {data['message']}")
            print(f"🔗 {data['link']}")
            print()
            """
            
            print("=" * 70)
            print("✅ TODOS OS TESTES CONCLUÍDOS COM SUCESSO!")
            print("=" * 70)


if __name__ == "__main__":
    asyncio.run(test_mcp_server())
