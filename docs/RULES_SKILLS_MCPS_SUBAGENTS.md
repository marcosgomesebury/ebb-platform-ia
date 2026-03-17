# Guia Completo: Rules, Skills, MCPs e Subagents

Este documento explica os quatro conceitos fundamentais de automação e produtividade com IA implementados neste workspace.

---

## 📚 Visão Geral

```
┌─────────────────────────────────────────────────────────────────┐
│                         WORKSPACE                               │
│                                                                 │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐ │
│  │  RULES   │───▶│  SKILLS  │───▶│   MCPs   │───▶│SUBAGENTS │ │
│  └──────────┘    └──────────┘    └──────────┘    └──────────┘ │
│       │               │                │               │        │
│   Governança      Automação       Integração      Orquestração │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 1️⃣ RULES (Regras)

### 🎯 O que são?
Regras de governança e automação que devem ser seguidas automaticamente pelo assistente de IA ou pelo desenvolvedor.

### 📌 Características
- **Escopo**: Workflow, qualidade de código, segurança
- **Execução**: Automática (pelo assistente) ou checada em CI/CD
- **Persistência**: Definidas uma vez, aplicadas sempre
- **Complexidade**: Baixa a média

### 🔍 Exemplo Prático

**Regra**: `pre-commit-env-check`

```yaml
Trigger: Ao criar arquivo .env
Condição: Verificar se .env está no .gitignore
Ação: 
  - Alertar usuário
  - Sugerir adicionar ao .gitignore
  - Criar .env.example automaticamente
```

### 📁 Onde ficam?
- Template: `skills/TEMPLATE_RULE.md`
- Implementação: Podem ser integradas em:
  - `.github/workflows/` (GitHub Actions)
  - `.pre-commit-config.yaml` (pre-commit hooks)
  - Instruções do Copilot (`.github/copilot-instructions.md`)

### 🔗 Relação com outros conceitos
- **Rules → Skills**: Regras podem disparar a execução de skills
- **Rules → Subagents**: Regras definem quando subagents devem ser executados

---

## 2️⃣ SKILLS (Habilidades)

### 🎯 O que são?
Automações isoladas e reutilizáveis que executam uma tarefa específica.

### 📌 Características
- **Escopo**: Tarefa única e bem definida
- **Execução**: Manual ou chamada por subagent
- **Isolamento**: Dependências próprias (requirements.txt)
- **Reutilização**: Podem ser usados em múltiplos contextos
- **Complexidade**: Baixa a média

### 🔍 Exemplo Prático

**Skill**: `mysql_connect`

```python
# Input: Variáveis de ambiente (.env)
EBB_CONCILIACAO_MYSQL_DEV_HOST=10.23.129.3
EBB_CONCILIACAO_MYSQL_DEV_USER=root

# Função: Testar conexão MySQL
def testar_conexao():
    connection = pymysql.connect(host, user, password)
    return connection.is_connected()

# Output: Status da conexão + versão do MySQL
```

### 📁 Estrutura de um Skill

```
skills/mysql_connect/
├── main.py              # Lógica principal
├── requirements.txt     # Dependências isoladas
├── .env.example         # Template de configuração
├── README.md            # Documentação de uso
└── tests/               # Testes unitários
    └── README.md
```

### 🔗 Relação com outros conceitos
- **Skills → MCPs**: Skills compartilham dados via MCPs
- **Skills → Subagents**: Subagents orquestram múltiplos skills

---

## 3️⃣ MCPs (Model Context Protocols)

### 🎯 O que são?
Protocolos que definem **como skills compartilham contexto e dados** entre si.

### 📌 Características
- **Escopo**: Integração e comunicação entre skills
- **Execução**: Passivo (define estrutura de dados)
- **Função**: Contrato de interface entre componentes
- **Complexidade**: Média

### 🔍 Exemplo Prático

**MCP**: `remote_db_connection_protocol`

```python
# Fluxo de dados entre ssh_connect e mysql_connect

# 1. ssh_connect OUTPUT
ssh_context = {
    "host": "10.23.129.3",
    "port": 22,
    "status": "connected",
    "local_forward": "localhost:3306"
}

# 2. MCP define transformação
db_config = {
    "host": ssh_context["local_forward"].split(":")[0],
    "port": int(ssh_context["local_forward"].split(":")[1]),
    "tunnel_active": ssh_context["status"] == "connected"
}

# 3. mysql_connect INPUT (recebe contexto transformado)
mysql_connect.connect(
    host=db_config["host"],
    port=db_config["port"]
)
```

### 📁 Onde ficam?
- Template: `skills/TEMPLATE_MCP.md`
- Implementação: Podem ser:
  - Funções Python de transformação (`utils/mcp_helpers.py`)
  - Classes de contexto compartilhado
  - JSON schemas para validação de dados

### 🔗 Relação com outros conceitos
- **Skills → MCP → Skills**: Skill A passa dados via MCP para Skill B
- **Subagents usam MCPs**: Para coordenar múltiplos skills

---

## 4️⃣ SUBAGENTS (Agentes Autônomos)

### 🎯 O que são?
Agentes autônomos que **orquestram múltiplos skills** para realizar tarefas complexas, com lógica de decisão, tratamento de erros e geração de relatórios.

### 📌 Características
- **Escopo**: Tarefa complexa que requer múltiplos passos
- **Execução**: Autônoma (toma decisões baseadas em resultados intermediários)
- **Inteligência**: 
  - Tratamento de erros
  - Retry logic
  - Análise de resultados
  - Recomendações automáticas
- **Complexidade**: Alta

### 🔍 Exemplo Prático

**Subagent**: `database_diagnostic_agent`

```python
# Subagent orquestra 3 skills:

def main():
    # 1. Executar Skill: ssh_connect
    ssh_result = run_skill("ssh_connect")
    
    if not ssh_result.success:
        # Decisão: Tentar diagnóstico de rede
        print("SSH failed, checking connectivity...")
        ping_result = check_network()
        return generate_report([ssh_result, ping_result])
    
    # 2. Executar Skill: mysql_connect (usando contexto SSH)
    mysql_result = run_skill("mysql_connect", context=ssh_result.context)
    
    if not mysql_result.success:
        # Decisão: Verificar pods Kubernetes
        print("MySQL failed, checking K8s pods...")
        k8s_result = run_skill("kubernetes_debug", pod="account")
        
    # 3. Executar Skill: kubernetes_debug
    k8s_result = run_skill("kubernetes_debug")
    
    # 4. Analisar resultados e gerar relatório
    report = analyze_results([ssh_result, mysql_result, k8s_result])
    
    # 5. Gerar recomendações
    recommendations = generate_recommendations(report)
    
    return report + recommendations
```

### 📁 Estrutura de um Subagent

```python
subagents/database_diagnostic_agent.py
├── Orquestração de skills
├── Lógica de decisão (if/else baseado em resultados)
├── Tratamento de erros e retry
├── Análise de padrões
├── Geração de relatório
└── Recomendações automáticas
```

### 🔗 Relação com outros conceitos
- **Rules → Subagent**: Regras definem quando executar
- **Subagent → Skills**: Subagent coordena múltiplos skills
- **Subagent → MCP**: Usa MCPs para passar contexto entre skills

---

## 🔄 Como Tudo se Integra

### Fluxo Completo: Exemplo Real

```
┌─────────────────────────────────────────────────────────────────┐
│ CENÁRIO: Diagnosticar erro de conexão com banco de dados       │
└─────────────────────────────────────────────────────────────────┘

1️⃣  RULE: erro-database-detected
    ├─ Trigger: Detecta logs de erro "Connection timeout"
    ├─ Ação: Invoca subagent "database_diagnostic_agent"
    └─ Output: Subagent é executado

2️⃣  SUBAGENT: database_diagnostic_agent
    ├─ Decisão: Iniciar diagnóstico em camadas
    ├─ Passo 1: Executar SKILL "ssh_connect"
    │   ├─ Input: .env (RDP_SERVER, RDP_USER, RDP_PASS)
    │   ├─ Ação: Tenta conectar via SSH
    │   └─ Output: ssh_context { status: "connected", local_port: 3306 }
    │
    ├─ Passo 2: Usar MCP "remote_db_connection_protocol"
    │   ├─ Input: ssh_context
    │   ├─ Transformação: Converte para db_config
    │   └─ Output: db_config { host: "localhost", port: 3306 }
    │
    ├─ Passo 3: Executar SKILL "mysql_connect"
    │   ├─ Input: db_config (via MCP)
    │   ├─ Ação: Testa conexão MySQL
    │   └─ Output: mysql_result { status: "failed", error: "timeout" }
    │
    ├─ Decisão: MySQL falhou, verificar Kubernetes
    │
    ├─ Passo 4: Executar SKILL "kubernetes_debug"
    │   ├─ Input: pod_name="ebb-account"
    │   ├─ Ação: Analisa logs, eventos, status
    │   └─ Output: k8s_result { pod_status: "Running", errors: [...] }
    │
    ├─ Análise: Correlaciona resultados
    │   ├─ SSH: OK
    │   ├─ MySQL: FAIL (timeout)
    │   └─ K8s: Pod OK, mas com erros de conexão
    │
    └─ Output: Relatório completo + Recomendações
        ├─ ✗ MySQL connection timeout
        ├─ ✓ SSH tunnel working
        ├─ ✓ Pod is running
        └─ Recomendações:
            - Check NetworkPolicy for port 3306
            - Verify Cloud SQL proxy configuration
            - Review firewall rules

3️⃣  RULE: save-diagnostic-report
    ├─ Trigger: Subagent completa execução
    ├─ Ação: Salva relatório em /memories/repo/
    └─ Output: Histórico para análise futura
```

---

## 📊 Comparação Lado a Lado

| Aspecto | Rules | Skills | MCPs | Subagents |
|---------|-------|--------|------|-----------|
| **Propósito** | Governança | Execução | Integração | Orquestração |
| **Complexidade** | Baixa | Baixa-Média | Média | Alta |
| **Autonomia** | Reativa | Manual | Passivo | Autônoma |
| **Reutilização** | Alta | Alta | Média | Baixa |
| **Isolamento** | N/A | Alto | Médio | Baixo |
| **Dependências** | Nenhuma | Próprias | Entre skills | Múltiplos skills |
| **Output** | Ação/Alerta | Resultado | Contexto | Relatório |

---

## 🎓 Quando Usar Cada Um?

### Use **RULES** quando:
- ✅ Precisa garantir governança (ex: nunca commitar .env)
- ✅ Quer automatizar checagens repetitivas
- ✅ Necessita aplicar políticas em todo o workspace
- ✅ Quer prevenir erros comuns

### Use **SKILLS** quando:
- ✅ Tem uma tarefa isolada e bem definida
- ✅ Precisa reutilizar a automação em vários contextos
- ✅ Quer manter dependências isoladas
- ✅ A tarefa não depende de outras automações

### Use **MCPs** quando:
- ✅ Precisa integrar múltiplos skills
- ✅ Dados de um skill são input de outro
- ✅ Quer padronizar estrutura de dados compartilhados
- ✅ Necessita transformar contexto entre skills

### Use **SUBAGENTS** quando:
- ✅ Tarefa requer múltiplos passos coordenados
- ✅ Precisa tomar decisões baseadas em resultados intermediários
- ✅ Quer automatizar diagnóstico complexo
- ✅ Necessita análise e recomendações automáticas

---

## 🚀 Criando Novos Componentes

### 1. Criar uma Rule

```bash
# Use o template
cp skills/TEMPLATE_RULE.md skills/my-rule.md

# Edite e defina:
# - Nome da regra
# - Condições de disparo
# - Ações automáticas
# - Exemplos de uso

# Implemente em:
# - .github/workflows/ (GitHub Actions)
# - .pre-commit-config.yaml (hooks)
# - .github/copilot-instructions.md (instrução para IA)
```

### 2. Criar um Skill

```bash
# Estrutura
mkdir -p skills/my_skill/tests
cd skills/my_skill

# Arquivos base
touch main.py requirements.txt .env.example README.md

# Use templates como referência
cat ../TEMPLATE_SKILL.md

# Implemente lógica isolada
# Documente variáveis e uso
```

### 3. Criar um MCP

```bash
# Use o template
cp skills/TEMPLATE_MCP.md skills/my-mcp.md

# Defina:
# - Skills envolvidos
# - Estrutura de dados compartilhados
# - Transformações necessárias
# - Exemplos de integração

# Implemente em:
# - utils/mcp_helpers.py (funções de transformação)
# - models/context.py (classes de contexto)
```

### 4. Criar um Subagent

```bash
# Crie o arquivo
touch subagents/my_subagent.py
chmod +x subagents/my_subagent.py

# Use o template como base
cat skills/TEMPLATE_SUBAGENT.md

# Implemente:
# - Orquestração de skills
# - Lógica de decisão
# - Tratamento de erros
# - Geração de relatório
# - Recomendações automáticas
```

---

## 💡 Boas Práticas

### Rules
- ✅ Mantenha rules simples e focadas
- ✅ Documente claramente as condições de disparo
- ✅ Forneça mensagens de erro claras
- ✅ Teste em CI/CD antes de aplicar globalmente

### Skills
- ✅ Um skill = uma responsabilidade
- ✅ Isole dependências (requirements.txt próprio)
- ✅ Sempre forneça .env.example
- ✅ Documente inputs, outputs e erros possíveis
- ✅ Adicione testes unitários

### MCPs
- ✅ Defina contratos claros de dados
- ✅ Use JSON schema para validação
- ✅ Documente transformações esperadas
- ✅ Teste compatibilidade entre skills

### Subagents
- ✅ Decomponha tarefas complexas em passos claros
- ✅ Implemente retry logic para operações que podem falhar
- ✅ Sempre gere relatórios estruturados
- ✅ Forneça recomendações acionáveis
- ✅ Documente o fluxo de decisão
- ✅ Trate erros gracefully

---

## 📖 Exemplos Implementados

### Rules
- `pre-commit-env-check`: Valida que .env não seja commitado

### Skills
- `rdp_connect`: Conexão RDP remota
- `ssh_connect`: Conexão SSH interativa
- `mysql_connect`: Teste de conexão MySQL
- `kubernetes_debug`: Diagnóstico de pods K8s

### MCPs
- `remote_db_connection_protocol`: SSH → MySQL context sharing

### Subagents
- `database_diagnostic_agent`: SSH + MySQL + K8s diagnostic orchestration

---

## 🔗 Referências

- [Skills Directory](../skills/) - Todos os skills disponíveis
- [Subagents Directory](../subagents/) - Todos os subagents implementados
- [OpenSpec Methodology](../openspec/README.md) - Metodologia de trabalho
- [Copilot Instructions](../.github/copilot-instructions.md) - Rules para o assistente IA

---

**Última atualização**: 16-03-2026  
**Mantido por**: Marcos Gomes
