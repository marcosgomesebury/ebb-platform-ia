#!/usr/bin/env python3
"""
Database Diagnostic Subagent

Orquestra múltiplos skills para diagnosticar problemas de conectividade
e performance de banco de dados remoto.

Skills orquestrados:
- ssh_connect: Conecta ao servidor via SSH
- mysql_connect: Testa conexão MySQL
- kubernetes_debug: Verifica pods relacionados (opcional)
"""

import os
import sys
import subprocess
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# Cores para output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

def print_header(title):
    """Imprime cabeçalho formatado."""
    print(f"\n{'='*70}")
    print(f"{BLUE}{title.center(70)}{RESET}")
    print(f"{'='*70}\n")

def print_step(step_num, description):
    """Imprime passo da execução."""
    print(f"{YELLOW}[{step_num}]{RESET} {description}...")

def print_success(message):
    """Imprime mensagem de sucesso."""
    print(f"{GREEN}✓{RESET} {message}")

def print_error(message):
    """Imprime mensagem de erro."""
    print(f"{RED}✗{RESET} {message}")

def print_warning(message):
    """Imprime aviso."""
    print(f"{YELLOW}!{RESET} {message}")

def run_skill(skill_path, skill_name):
    """Executa um skill e retorna o resultado."""
    try:
        result = subprocess.run(
            [sys.executable, skill_path],
            capture_output=True,
            text=True,
            timeout=60
        )
        return {
            'success': result.returncode == 0,
            'stdout': result.stdout,
            'stderr': result.stderr,
            'returncode': result.returncode
        }
    except subprocess.TimeoutExpired:
        return {
            'success': False,
            'stdout': '',
            'stderr': f'{skill_name} timed out',
            'returncode': -1
        }
    except Exception as e:
        return {
            'success': False,
            'stdout': '',
            'stderr': str(e),
            'returncode': -1
        }

def check_ssh_connectivity():
    """Verifica conectividade SSH."""
    print_step(1, "Checking SSH connectivity")
    
    ssh_host = os.getenv("RDP_SERVER_EBB_CONCILIACAO_DB", "10.23.129.3")
    ssh_user = os.getenv("RDP_USER", "marcos")
    
    # Tenta ping primeiro
    try:
        result = subprocess.run(
            ['ping', '-c', '2', ssh_host],
            capture_output=True,
            timeout=10
        )
        if result.returncode == 0:
            print_success(f"Host {ssh_host} is reachable")
        else:
            print_warning(f"Host {ssh_host} ping failed")
    except:
        print_warning("Ping check skipped")
    
    # Verifica porta SSH
    try:
        result = subprocess.run(
            ['nc', '-zv', ssh_host, '22'],
            capture_output=True,
            timeout=5
        )
        if result.returncode == 0:
            print_success(f"SSH port 22 is open on {ssh_host}")
            return True
        else:
            print_error(f"SSH port 22 is closed on {ssh_host}")
            return False
    except:
        print_warning("Port check skipped (nc not available)")
        return True

def test_ssh_connection():
    """Testa conexão SSH via skill."""
    print_step(2, "Testing SSH connection")
    
    skills_dir = os.path.join(os.path.dirname(__file__), '..', 'skills')
    ssh_skill = os.path.join(skills_dir, 'ssh_connect', 'main.py')
    
    # Nota: ssh_connect é interativo, vamos apenas verificar se o script existe
    if os.path.exists(ssh_skill):
        print_success("SSH skill available")
        print("  Note: SSH connection test requires interactive mode")
        return True
    else:
        print_error("SSH skill not found")
        return False

def test_mysql_connection():
    """Testa conexão MySQL via skill."""
    print_step(3, "Testing MySQL connection")
    
    skills_dir = os.path.join(os.path.dirname(__file__), '..', 'skills')
    mysql_skill = os.path.join(skills_dir, 'mysql_connect', 'main.py')
    
    if not os.path.exists(mysql_skill):
        print_error("MySQL skill not found")
        return False
    
    result = run_skill(mysql_skill, "mysql_connect")
    
    if result['success']:
        print_success("MySQL connection successful")
        print(result['stdout'])
        return True
    else:
        print_error("MySQL connection failed")
        print(result['stderr'])
        return False

def check_kubernetes_pods():
    """Verifica pods relacionados ao banco."""
    print_step(4, "Checking Kubernetes pods (optional)")
    
    try:
        # Verifica se kubectl está disponível
        result = subprocess.run(
            ['kubectl', 'get', 'pods', '-n', 'core'],
            capture_output=True,
            timeout=10
        )
        
        if result.returncode == 0:
            print_success("Kubernetes access OK")
            # Procura por pods relacionados
            if 'account' in result.stdout.decode().lower():
                print("  Found related pods:")
                for line in result.stdout.decode().split('\n'):
                    if 'account' in line.lower():
                        print(f"    {line}")
            return True
        else:
            print_warning("No Kubernetes access")
            return False
    except FileNotFoundError:
        print_warning("kubectl not available")
        return False
    except Exception as e:
        print_warning(f"Kubernetes check failed: {e}")
        return False

def generate_report(results):
    """Gera relatório final."""
    print_header("DIAGNOSTIC REPORT")
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"Generated at: {timestamp}\n")
    
    # Resumo
    total_checks = len(results)
    passed_checks = sum(1 for r in results if r['passed'])
    
    print(f"Total checks: {total_checks}")
    print(f"Passed: {GREEN}{passed_checks}{RESET}")
    print(f"Failed: {RED}{total_checks - passed_checks}{RESET}")
    print()
    
    # Detalhes
    for check in results:
        status = f"{GREEN}✓{RESET}" if check['passed'] else f"{RED}✗{RESET}"
        print(f"{status} {check['name']}: {check['message']}")
    
    # Recomendações
    if passed_checks < total_checks:
        print_header("RECOMMENDATIONS")
        
        for check in results:
            if not check['passed']:
                print(f"• {check['name']}:")
                for rec in check.get('recommendations', []):
                    print(f"  - {rec}")
                print()

def main():
    """Executa o diagnóstico completo."""
    print_header("DATABASE DIAGNOSTIC AGENT")
    print("Orchestrating skills: ssh_connect → mysql_connect → kubernetes_debug\n")
    
    results = []
    
    # 1. Verificar conectividade SSH
    ssh_reachable = check_ssh_connectivity()
    results.append({
        'name': 'SSH Connectivity',
        'passed': ssh_reachable,
        'message': 'Host reachable' if ssh_reachable else 'Host unreachable',
        'recommendations': [
            'Check network connectivity',
            'Verify firewall rules',
            'Check VPN connection'
        ] if not ssh_reachable else []
    })
    
    # 2. Testar conexão SSH
    ssh_ok = test_ssh_connection()
    results.append({
        'name': 'SSH Connection',
        'passed': ssh_ok,
        'message': 'Skill available' if ssh_ok else 'Skill not found',
        'recommendations': [
            'Verify SSH credentials in .env',
            'Check SSH key permissions'
        ] if not ssh_ok else []
    })
    
    # 3. Testar conexão MySQL
    mysql_ok = test_mysql_connection()
    results.append({
        'name': 'MySQL Connection',
        'passed': mysql_ok,
        'message': 'Connected successfully' if mysql_ok else 'Connection failed',
        'recommendations': [
            'Check MySQL host and port',
            'Verify database credentials',
            'Check if MySQL service is running',
            'Review firewall rules for port 3306',
            'Check NetworkPolicy in Kubernetes'
        ] if not mysql_ok else []
    })
    
    # 4. Verificar pods Kubernetes
    k8s_ok = check_kubernetes_pods()
    results.append({
        'name': 'Kubernetes Pods',
        'passed': k8s_ok,
        'message': 'Pods accessible' if k8s_ok else 'Not available',
        'recommendations': [
            'Configure kubectl access',
            'Check GKE cluster permissions'
        ] if not k8s_ok else []
    })
    
    # Gerar relatório
    generate_report(results)
    
    # Exit code
    sys.exit(0 if all(r['passed'] or r['name'] == 'Kubernetes Pods' for r in results) else 1)

if __name__ == "__main__":
    main()
