#!/usr/bin/env python3
"""
Exemplo: Listar canais do workspace

Uso:
    python examples/list_channels.py
"""

import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from dotenv import load_dotenv
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

load_dotenv()


def list_public_channels():
    """Listar todos os canais públicos"""
    
    token = os.getenv("SLACK_BOT_TOKEN")
    if not token:
        print("❌ Erro: SLACK_BOT_TOKEN não definido")
        sys.exit(1)
    
    client = WebClient(token=token)
    
    try:
        response = client.conversations_list(
            types="public_channel",
            limit=100
        )
        
        channels = response["channels"]
        
        print(f"📋 Total de canais públicos: {len(channels)}\n")
        
        for channel in sorted(channels, key=lambda x: x.get("num_members", 0), reverse=True):
            name = channel["name"]
            members = channel.get("num_members", 0)
            topic = channel.get("topic", {}).get("value", "")
            
            print(f"#{name:<30} | {members:>3} membros")
            if topic:
                print(f"   └─ {topic[:60]}")
        
        print(f"\n✅ Listagem concluída!")
        
    except SlackApiError as e:
        print(f"❌ Erro: {e.response['error']}")


def list_all_channel_types():
    """Listar canais por tipo"""
    
    token = os.getenv("SLACK_BOT_TOKEN")
    client = WebClient(token=token)
    
    types = ["public_channel", "private_channel"]
    
    for channel_type in types:
        try:
            response = client.conversations_list(
                types=channel_type,
                limit=50
            )
            
            channels = response["channels"]
            print(f"\n{'=' * 60}")
            print(f"📁 {channel_type.upper()}: {len(channels)} canais")
            print(f"{'=' * 60}")
            
            for ch in channels[:10]:  # Mostrar apenas primeiros 10
                print(f"  • {ch['name']}")
            
            if len(channels) > 10:
                print(f"  ... e mais {len(channels) - 10} canais")
        
        except SlackApiError as e:
            print(f"❌ Erro ao listar {channel_type}: {e.response['error']}")


if __name__ == "__main__":
    print("=" * 60)
    print("Listando Canais Públicos")
    print("=" * 60)
    list_public_channels()
    
    print("\n" + "=" * 60)
    print("Listando por Tipo")
    print("=" * 60)
    list_all_channel_types()
