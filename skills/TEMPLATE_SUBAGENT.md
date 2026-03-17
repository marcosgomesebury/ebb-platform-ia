# Subagent: Database Diagnostic Agent

- **Nome do Subagent:** database_diagnostic_agent
- **Descrição:** Agente autônomo que diagnostica problemas de conectividade e performance de banco de dados remoto, orquestrando múltiplos skills
- **Skills orquestrados:**
  1. ssh_connect: Conecta ao servidor de banco via SSH
  2. mysql_connect: Testa conexão MySQL
  3. kubernetes_debug: Verifica pods relacionados ao banco (opcional)
- **Regras de execução:**
  - **Prioridade:** Alta (quando pod de aplicação falha por timeout de DB)
  - **Trigger:** Erro de conexão detectado em logs
  - **Retry:** 3 tentativas com backoff exponencial
  - **Timeout:** 60 segundos por skill
  - **Rollback:** Fechar todas as conexões em caso de falha
- **Fluxo de execução:**
  ```
  START → Check SSH Connectivity
    ├─ Success → Test MySQL Connection
    │            ├─ Success → Run Diagnostics
    │            │            ├─ Check DB Version
    │            │            ├─ Check Active Connections
    │            │            ├─ Check Slow Queries
    │            │            └─ Generate Report
    │            └─ Failed → Check Firewall/NetworkPolicy
    └─ Failed → Check Server Status (ping, port scan)
  ```
- **Exemplo de uso:**
  ```bash
  # Modo interativo
  python subagents/database_diagnostic.py --target ebb-conciliacao-db
  
  # Modo automático (quando detecta erro)
  python subagents/database_diagnostic.py --auto --error-log /var/log/app/error.log
  ```
- **Output esperado:**
  ```
  ═══════════════════════════════════════
  DATABASE DIAGNOSTIC REPORT
  ═══════════════════════════════════════
  
  [✓] SSH Connection: OK (10.23.129.3:22)
  [✓] MySQL Connection: OK (sistema_custo)
  [✓] Database Version: MySQL 8.0.35
  [!] Active Connections: 95/100 (HIGH)
  [✗] Slow Queries: 12 detected (last 1h)
  
  RECOMMENDATIONS:
  1. Increase max_connections to 150
  2. Optimize slow queries (see attached list)
  3. Add index on table `transacoes.data_criacao`
  
  NEXT STEPS:
  - Review slow query log: /var/log/mysql/slow.log
  - Monitor connection pool: kubectl logs -n core ebb-account
  ```
- **Integração com Memory:**
  - Salva resultados em /memories/repo/database-diagnostics.md
  - Registra padrões de erro para melhorar detecção futura
  - Aprende correlações entre erros de app e problemas de DB
