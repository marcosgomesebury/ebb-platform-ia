import os
import subprocess

from dotenv import load_dotenv

load_dotenv()


SERVER = os.getenv("RDP_SERVER")
# Prioriza RDP_SERVER_EBB_CONCILIACAO_USER, fallback para RDP_USER
USER = os.getenv("RDP_SERVER_EBB_CONCILIACAO_USER") or os.getenv("RDP_USER")
PASS = os.getenv("RDP_PASS")
DOMAIN = os.getenv("RDP_DOMAIN")

if not all([SERVER, USER, PASS]):
	raise ValueError(
		"RDP_SERVER, RDP_SERVER_EBB_CONCILIACAO_USER (or RDP_USER), and RDP_PASS must be set in .env file."
	)


remmina_conf = (
	f"[remmina]\n"
	f"protocol=RDP\n"
	f"server={SERVER}\n"
	f"username={USER}\n"
	f"password={PASS}\n"
	f"group=RDP\n"
	f"domain={DOMAIN if DOMAIN else ''}\n"
)


with open("/tmp/rdp-connection.remmina", "w") as f:
	f.write(remmina_conf)


# Tenta usar xfreerdp se disponível, senão usa Remmina
import shutil

def run_xfreerdp():
	cmd = [
		"xfreerdp",
		f"/v:{SERVER}",
		f"/u:{USER}",
		f"/p:{PASS}",
		f"/d:{DOMAIN if DOMAIN else ''}",
	]
	# Aspas simples para senha com caracteres especiais
	cmd = [c if not c.startswith("/p:") else f"/p:'{PASS}'" for c in cmd]
	print("Executando:", " ".join(cmd))
	subprocess.run(" ".join(cmd), shell=True)

if shutil.which("xfreerdp"):
	run_xfreerdp()
else:
	subprocess.run(["remmina", "-c", "/tmp/rdp-connection.remmina"])
