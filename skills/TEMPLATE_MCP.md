# MCP: Remote Database Connection Protocol

- **Nome do MCP:** remote_db_connection_protocol
- **Descrição:** Protocolo para estabelecer conexão segura com banco de dados remoto via SSH tunnel e validar conectividade
- **Skills envolvidos:**
  - ssh_connect: Estabelece túnel SSH para o host remoto
  - mysql_connect: Testa conexão MySQL através do túnel
- **Fluxo de dados/contexto:**
  ```
  1. ssh_connect recebe:
     - RDP_SERVER_EBB_CONCILIACAO_DB (10.23.129.3)
     - RDP_USER, RDP_PASS
  
  2. ssh_connect estabelece túnel e retorna:
     - connection_status: "connected"
     - local_port: 3306
     - remote_host: "10.23.129.3"
  
  3. mysql_connect recebe contexto:
     - EBB_CONCILIACAO_MYSQL_DEV_HOST (do túnel SSH)
     - Credenciais do banco
  
  4. mysql_connect retorna:
     - db_version: "MySQL 8.0.x"
     - connection_test: "success"
     - tables: [lista de tabelas]
  ```
- **Compartilhamento de Contexto:**
  ```json
  {
    "ssh_tunnel": {
      "host": "10.23.129.3",
      "port": 22,
      "status": "connected",
      "local_forward": "localhost:3306"
    },
    "database": {
      "host": "localhost",
      "port": 3306,
      "user": "ebb-conciliacao",
      "database": "sistema_custo"
    }
  }
  ```
- **Exemplo de integração:**
  ```python
  # Arquivo: skills/remote_db_mcp/orchestrator.py
  from skills.ssh_connect import main as ssh_connect
  from skills.mysql_connect import main as mysql_connect
  
  def connect_remote_db():
      # 1. Estabelece SSH tunnel
      ssh_context = ssh_connect.connect(
          host="10.23.129.3",
          user="marcos",
          forward_port=3306
      )
      
      # 2. Passa contexto para MySQL
      db_result = mysql_connect.test_connection(
          host="localhost",  # via tunnel
          port=ssh_context['local_port']
      )
      
      return {**ssh_context, **db_result}
  ```
