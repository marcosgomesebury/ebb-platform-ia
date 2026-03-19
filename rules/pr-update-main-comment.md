# Rule: Update PR Main Comment After Changes

- **Nome da Regra:** pr-update-main-comment
- **Descrição:** After updating a Pull Request (new commits, rebases, or amendments), the main PR description comment must be updated to reflect the current state of the changes. This ensures reviewers always have an accurate and up-to-date summary.
- **Condições de disparo:**
  - Ao fazer push de novos commits em uma PR existente
  - Ao fazer rebase ou amend em uma branch com PR aberta
  - Ao adicionar, remover ou modificar arquivos já descritos na PR
- **Ações automáticas:**
  - Revisar o comentário principal (description) da PR após cada push
  - Atualizar a descrição para refletir as mudanças atuais da branch
  - Garantir que a lista de arquivos alterados, motivação e escopo estejam corretos
  - Remover referências a mudanças que foram revertidas ou removidas
  - Adicionar descrição de novas mudanças introduzidas desde a última atualização
- **Exemplo de uso:**
  ```
  # After pushing new changes to an open PR:
  1. Review the current PR description
  2. Update the summary to reflect all current changes
  3. Ensure the description matches the latest commit(s)
  4. Save the updated PR description via GitHub UI or CLI:
  gh pr edit <PR-NUMBER> --body "Updated description..."
  ```
