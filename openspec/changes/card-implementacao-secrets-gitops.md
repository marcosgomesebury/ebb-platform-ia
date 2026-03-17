# Card: Como Implementar Secrets no GitOps

## Contexto
A gestão de secrets é crítica para segurança e conformidade em ambientes GitOps. Secrets nunca devem ser commitados diretamente no repositório.

## Requisitos
- **NUNCA** commitar secrets reais em repositórios GitOps.
- **Utilizar Secret Manager (GCP)** para armazenamento seguro.
- **Templates de secrets**: Criar arquivos `secrets-template.env` ou `credentials-template.yaml` sem valores reais.
- **Atualizar `.gitignore`** para bloquear arquivos de secrets.
- **Remover secrets do histórico** caso já tenham sido commitados.

## Passos para Implementação
1. **Identificar todos os secrets** já commitados e rotacionar imediatamente.
2. **Remover secrets do histórico** usando `git-filter-repo` ou BFG.
3. **Adicionar templates**:
   - Exemplo: `secrets-template.env`, `credentials-template.yaml`
4. **Configurar `.gitignore`**:
   ```
   *.env
   *.pem
   *.key
   *credentials*.yaml
   secrets/
   ```
5. **Armazenar secrets reais** no Secret Manager (GCP).
6. **Referenciar secrets** nos manifests GitOps via integração com GCP Secret Manager.

## Referências
- [GCP Secret Manager](https://cloud.google.com/secret-manager/docs)
- [git-filter-repo](https://github.com/newren/git-filter-repo)
- [BFG Repo-Cleaner](https://rtyley.github.io/bfg-repo-cleaner/)

## Checklist
- [ ] Todos os secrets removidos do git
- [ ] Templates criados
- [ ] `.gitignore` atualizado
- [ ] Integração com Secret Manager implementada

---
**OpenSpec Workflow:** Documentar mudanças em `/openspec/changes/` e atualizar `/openspec/tasks.md`.
