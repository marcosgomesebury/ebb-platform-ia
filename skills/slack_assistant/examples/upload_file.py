#!/usr/bin/env python3
"""
Exemplo: Upload de arquivo para canal

Uso:
    python examples/upload_file.py
"""

import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from dotenv import load_dotenv
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

load_dotenv()


def upload_text_file():
    """Upload de arquivo de texto"""
    
    token = os.getenv("SLACK_BOT_TOKEN")
    if not token:
        print("❌ Erro: SLACK_BOT_TOKEN não definido")
        sys.exit(1)
    
    client = WebClient(token=token)
    
    # Criar arquivo temporário
    temp_file = Path("/tmp/test_report.txt")
    temp_file.write_text("""
Relatório de Deployment
========================

Status: Sucesso ✅
Versão: v2.3.1
Ambiente: Production
Duração: 5 minutos

Serviços Atualizados:
- ebb-account-api
- ebb-payments-service
- ebb-notifications

Próximos Passos:
1. Monitorar logs por 24h
2. Validar métricas
3. Atualizar documentação
""")
    
    try:
        response = client.files_upload_v2(
            channel="#engineering",
            file=str(temp_file),
            title="Relatório de Deployment - v2.3.1",
            initial_comment="📄 Relatório do deployment de hoje"
        )
        
        file_info = response["file"]
        print("✅ Arquivo enviado com sucesso!")
        print(f"   Nome: {file_info['name']}")
        print(f"   ID: {file_info['id']}")
        print(f"   URL: {file_info.get('url_private', 'N/A')}")
        
    except SlackApiError as e:
        print(f"❌ Erro ao fazer upload: {e.response['error']}")
    
    finally:
        # Limpar arquivo temporário
        if temp_file.exists():
            temp_file.unlink()


def upload_with_thread():
    """Upload de arquivo em resposta a thread"""
    
    token = os.getenv("SLACK_BOT_TOKEN")
    client = WebClient(token=token)
    
    # Criar arquivo de log
    log_file = Path("/tmp/error_log.txt")
    log_file.write_text("""
[2026-03-17 10:23:45] ERROR: Connection timeout
[2026-03-17 10:23:46] ERROR: Retrying... (1/3)
[2026-03-17 10:23:51] ERROR: Retrying... (2/3)
[2026-03-17 10:23:56] INFO: Connection restored
[2026-03-17 10:23:57] INFO: Processing resumed
""")
    
    try:
        # Enviar mensagem principal
        msg_response = client.chat_postMessage(
            channel="#alerts",
            text="🚨 Erro de conexão detectado e resolvido"
        )
        
        print(f"✅ Alerta enviado: {msg_response['ts']}")
        
        # Upload do log na thread
        file_response = client.files_upload_v2(
            channel="#alerts",
            file=str(log_file),
            title="error_log.txt",
            initial_comment="📋 Log completo do erro",
            thread_ts=msg_response['ts']  # Upload na thread
        )
        
        print(f"✅ Log enviado na thread!")
        
    except SlackApiError as e:
        print(f"❌ Erro: {e.response['error']}")
    
    finally:
        if log_file.exists():
            log_file.unlink()


if __name__ == "__main__":
    print("=" * 60)
    print("Exemplo 1: Upload de Arquivo de Texto")
    print("=" * 60)
    upload_text_file()
    
    print("\n" + "=" * 60)
    print("Exemplo 2: Upload em Thread")
    print("=" * 60)
    upload_with_thread()
