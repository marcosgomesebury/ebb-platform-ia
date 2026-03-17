import os
import paramiko
from dotenv import load_dotenv

load_dotenv()

SERVER = os.getenv("RDP_SERVER_OVERRIDE") or os.getenv("RDP_SERVER_EBB_CONCILIACAO_DB") or os.getenv("RDP_SERVER")
USER = os.getenv("RDP_USER")
PASS = os.getenv("RDP_PASS")

PORT = int(os.getenv("RDP_SSH_PORT", 22))
TIMEOUT = int(os.getenv("RDP_SSH_TIMEOUT", 10))
KEY_PATH = os.getenv("RDP_SSH_KEY_PATH")

if not all([SERVER, USER, PASS]):
	raise ValueError("RDP_SERVER, RDP_USER, and RDP_PASS must be set in .env file.")

import socket
import sys

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

print(f"Conectando em {SERVER}:{PORT} como {USER} (timeout={TIMEOUT}s)...")
try:
	if KEY_PATH:
		print(f"Usando chave SSH: {KEY_PATH}")
		client.connect(
			SERVER,
			port=PORT,
			username=USER,
			key_filename=KEY_PATH,
			timeout=TIMEOUT,
		)
	else:
		client.connect(
			SERVER,
			port=PORT,
			username=USER,
			password=PASS,
			timeout=TIMEOUT,
		)
	print("Conectado! Digite comandos (Ctrl+D para sair):")
	while True:
		try:
			cmd = input("$ ")
		except EOFError:
			print("\nSaindo.")
			break
		if not cmd:
			continue
		stdin, stdout, stderr = client.exec_command(cmd)
		print(stdout.read().decode(), end="")
		print(stderr.read().decode(), end="")
except paramiko.AuthenticationException:
	print("Erro: Falha de autenticação SSH. Verifique usuário/senha ou chave.")
	sys.exit(1)
except (paramiko.SSHException, socket.timeout) as e:
	print(f"Erro de conexão SSH: {e}")
	sys.exit(1)
except Exception as e:
	print(f"Erro inesperado: {e}")
	sys.exit(1)
finally:
	client.close()
