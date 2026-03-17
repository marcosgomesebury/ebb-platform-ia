# Subagents

Agentes autônomos que orquestram múltiplos skills para realizar tarefas complexas.

## Subagentes Disponíveis

### database_diagnostic_agent.py
Diagnostica problemas de conectividade e performance de banco de dados remoto.

**Usage:**
```bash
python database_diagnostic_agent.py
```

**Skills orquestrados:**
- ssh_connect
- mysql_connect
- kubernetes_debug (opcional)

**Output:**
- Relatório completo de diagnóstico
- Recomendações automatizadas
- Status de cada componente

## Como criar um novo subagent

1. Defina quais skills serão orquestrados
2. Crie lógica de coordenação e tratamento de erros
3. Implemente geração de relatório
4. Adicione análise e recomendações automáticas
5. Documente o fluxo de execução

Use os templates em `skills/TEMPLATE_SUBAGENT.md` como base.
