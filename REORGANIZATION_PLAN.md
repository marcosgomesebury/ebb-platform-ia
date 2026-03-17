# Plano de Reorganização - ebb-platform-ia

**Data**: 2026-03-17
**Objetivo**: Estrutura escalável e boas práticas

## 🗑️ Arquivos para DELETAR

### Duplicatas (manter ebb-* prefix)
- [ ] openspec/specs/clientjourney.md (duplicata de ebb-client-journey.md)
- [ ] openspec/specs/fx.md (duplicata de ebb-fx.md)
- [ ] openspec/specs/moneyflows.md (duplicata de ebb-money-flows.md)
- [ ] openspec/specs/platform.md (duplicata de ebb-platform.md)
- [ ] openspec/specs/treasury.md (duplicata de ebb-treasury.md)

### Arquivos obsoletos
- [ ] README_OLD.md (já migrado para README.md)
- [ ] skills/k8s_pod_test/ (teste temporário)
- [ ] mpc/ (typo, conteúdo movido)

### Docs temporários (já entendidos)
- [ ] skills/jira_assistant/REORGANIZATION_SUMMARY.md
- [ ] skills/jira_assistant/SKILL_VS_SERVER.md

## 📦 Arquivos para MOVER

### Testes
- [ ] tests/jira_assistant/ → skills/jira_assistant/tests/ (consolidar)

### Typo
- [ ] openspec/specs/jira_assinstant/ → excluir (typo, não usado)

## ✅ Estrutura Final

```
ebb-platform-ia/
├── openspec/
│   ├── specs/                    # Apenas ebb-* prefix
│   │   ├── ebb-client-journey.md
│   │   ├── ebb-money-flows.md
│   │   ├── ebb-treasury.md
│   │   ├── ebb-ebury-connect.md
│   │   ├── ebb-fx.md
│   │   ├── ebb-platform.md
│   │   ├── ebb-bigdata.md
│   │   └── webpayments.md        # Renomear para ebb-webpayments.md?
│   ├── changes/
│   └── archive/
├── skills/
│   ├── jira_assistant/
│   │   ├── SKILL.md
│   │   ├── README.md
│   │   ├── server/
│   │   ├── tests/                ← testes aqui
│   │   └── specs/
│   ├── kubernetes_debug/
│   ├── ssh_connect/
│   ├── mysql_connect/
│   ├── rdp_connect/
│   └── firestore_query/
├── docs/                          # Documentação geral
├── subagents/
└── pendencias/                    # Consolidado
