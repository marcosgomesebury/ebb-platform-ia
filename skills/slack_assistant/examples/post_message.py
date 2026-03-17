#!/usr/bin/env python3
"""
Exemplo: Enviar mensagem simples para canal do Slack

Uso:
    python examples/post_message.py
"""

import os
import sys
from pathlib import Path

# Adicionar parent directory ao path
sys.path.insert(0, str(Path(__file__).parent.parent))

from dotenv import load_dotenv
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

# Carregar variáveis de ambiente
load_dotenv()

def post_simple_message():
    """Enviar uma mensagem simples"""
    
    # Inicializar cliente
    token = os.getenv("SLACK_BOT_TOKEN")
    if not token:
        print("❌ Erro: SLACK_BOT_TOKEN não definido")
        sys.exit(1)
    
    client = WebClient(token=token)
    
    try:
        # Postar mensagem
        response = client.chat_postMessage(
            channel="#general",  # Altere para seu canal
            text="🚀 Olá do MCP Slack Assistant! Mensagem enviada via Python."
        )
        
        print("✅ Mensagem enviada com sucesso!")
        print(f"   Canal: {response['channel']}")
        print(f"   Timestamp: {response['ts']}")
        
    except SlackApiError as e:
        print(f"❌ Erro ao enviar mensagem: {e.response['error']}")
        print(f"   Detalhes: {e}")


def post_message_with_formatting():
    """Enviar mensagem com formatação Markdown"""
    
    token = os.getenv("SLACK_BOT_TOKEN")
    client = WebClient(token=token)
    
    message = """
*Deployment Report* 🚀

✅ *Status*: Success
📦 *Version*: v2.3.1
⏱️ *Duration*: 5 minutes
🌐 *Environment*: Production

_Deployed by Automation Bot_
"""
    
    try:
        response = client.chat_postMessage(
            channel="#engineering",
            text=message
        )
        
        print("✅ Mensagem formatada enviada!")
        print(f"   Link: https://app.slack.com/client/{response['channel']}/{response['ts']}")
        
    except SlackApiError as e:
        print(f"❌ Erro: {e.response['error']}")


def post_with_thread():
    """Enviar mensagem e responder em thread"""
    
    token = os.getenv("SLACK_BOT_TOKEN")
    client = WebClient(token=token)
    
    try:
        # Mensagem principal
        main_response = client.chat_postMessage(
            channel="#alerts",
            text="🚨 Alerta: Alto uso de memória detectado"
        )
        
        print(f"✅ Alerta principal enviado: {main_response['ts']}")
        
        # Responder na thread
        thread_response = client.chat_postMessage(
            channel="#alerts",
            text="📊 Detalhes:\n• Memória: 87% usada\n• Swap: 45% usado\n• Recomendação: Aumentar recursos",
            thread_ts=main_response['ts']  # Reply in thread
        )
        
        print(f"✅ Resposta em thread enviada: {thread_response['ts']}")
        
    except SlackApiError as e:
        print(f"❌ Erro: {e.response['error']}")


if __name__ == "__main__":
    print("=" * 60)
    print("Exemplo 1: Mensagem Simples")
    print("=" * 60)
    post_simple_message()
    
    print("\n" + "=" * 60)
    print("Exemplo 2: Mensagem com Formatação")
    print("=" * 60)
    post_message_with_formatting()
    
    print("\n" + "=" * 60)
    print("Exemplo 3: Thread Reply")
    print("=" * 60)
    post_with_thread()
