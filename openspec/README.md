# OpenSpec - Portfolio de Projetos

Este diretório utiliza a metodologia **OpenSpec (Spec-Driven Development)** para manter contexto contínuo e determinístico sobre as regras de negócio e arquitetura dos projetos.

**Note**: Este repositório (`ebb-platform-ia`) mantém as especificações e automações. O código dos domínios de negócio está em `/Ebury-Brazil/`. Ver [EBURY_BRAZIL_STRUCTURE.md](EBURY_BRAZIL_STRUCTURE.md) para detalhes.

## 📚 Estrutura

```
openspec/
├── config.yaml           # Configuração do OpenSpec
├── project.md            # Visão geral do portfolio
├── tasks.md              # Tarefas e acompanhamento
├── EBURY_BRAZIL_STRUCTURE.md  # Mapeamento do repositório Ebury-Brazil
├── specs/                # Especificações estáveis por domínio
│   ├── ebb-client-journey.md
│   ├── ebb-fx.md
│   ├── ebb-money-flows.md
│   ├── ebb-platform.md
│   ├── ebb-treasury.md
│   ├── ebb-ebury-connect.md
│   └── ebb-bigdata.md
├── changes/              # Delta specs em progresso
│   └── YYYY-MM-DD-nome-da-mudanca.md
└── archive/              # Specs concluídas e movidas
```

## 🔄 Workflow

### 1. Propor Mudança (changes/)

Ao iniciar um trabalho, crie um delta spec em `changes/` com:

```markdown
# Delta Spec: [Nome da Mudança]

**Status**: In Progress
**Date**: YYYY-MM-DD
**Ticket**: [ID]
**Domains**: [domínio afetado]

## Context
[Explicação do problema/necessidade]

## ADDED Requirements
[Novos requisitos com scenarios]

## MODIFIED Requirements
[Requisitos alterados com o que mudou]

## REMOVED Requirements
[Requisitos removidos/deprecated]

## Affected Components
[Lista de arquivos e componentes afetados]

## Testing Checklist
- [ ] Testes necessários
```

### 2. Implementar & Validar

Durante o desenvolvimento:
- ✅ Marque itens do Testing Checklist conforme progride
- 📝 Atualize o delta spec com descobertas
- 🔗 Link PRs e tickets relacionados

### 3. Arquivar (specs/)

Após conclusão e validação:
- Mova o delta spec de `changes/` para `specs/` (ou archive/)
- Atualize o spec do domínio principal se necessário
- Marque como concluído em `tasks.md`

## 📝 Princípios OpenSpec

1. **Comportamento > Implementação**: Foque no "o que" e "quando", não no "como"
2. **Delta Specs**: Documente mudanças (ADDED/MODIFIED/REMOVED), não reescreva tudo
3. **Progressive Rigor**: Specs leves para trabalho normal, detalhadas para mudanças críticas
4. **Brownfield-First**: Funciona com código existente, não apenas novos projetos

## 🎯 Formato de Requirements

Use **RFC 2119 keywords**:
- **SHALL/MUST**: Obrigatório
- **SHOULD**: Recomendado
- **MAY**: Opcional

### Exemplo:

```markdown
### REQ-001: Service SHALL Authenticate Using Workload Identity

**Scenario: Application Startup**
GIVEN a pod with Workload Identity configured
  AND serviceAccountName has iam.gke.io/gcp-service-account annotation
WHEN the application starts
THEN it SHALL authenticate using the bound GCP service account
  AND it SHALL NOT require GOOGLE_APPLICATION_CREDENTIALS file
```

## 🔍 Níveis de Rigor

- **Lite**: Requisitos básicos sem scenarios detalhados (padrão)
- **Full**: Requisitos + scenarios completos (infraestrutura, segurança, crítico)

## 📖 Referências

- **OpenSpec Repo**: https://github.com/Fission-AI/OpenSpec
- **Metodologia Completa**: /openspec/OPENSPEC_METHODOLOGY_SUMMARY.md (se disponível)

## 🛠️ CLI (Opcional)

Se Node.js disponível:
```bash
npm install -g @fission-ai/openspec@latest
cd /home/marcosgomes/Projects/openspec
openspec init
```

Comandos úteis:
- `/opsx:propose <nome>` - Criar nova mudança
- `/opsx:apply` - Aplicar mudança ao sistema
- `/opsx:archive` - Mover para specs estáveis
