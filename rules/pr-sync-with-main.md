# Rule: Keep PRs Synchronized with Main

- **Nome da Regra:** pr-sync-with-main
- **Descrição:** Before creating or updating a Pull Request, always ensure the branch is synchronized with the `main` branch to avoid merge conflicts and keep the PR up to date.
- **Condições de disparo:**
  - Ao criar uma Pull Request
  - Ao atualizar uma Pull Request existente
  - Ao preparar uma branch para review
- **Ações automáticas:**
  - Fazer fetch da branch `main` antes de abrir ou atualizar a PR
  - Fazer rebase ou merge da `main` na branch de trabalho
  - Resolver conflitos se houver, antes de fazer push
  - Garantir que o push final contenha as últimas alterações da `main`
- **Exemplo de uso:**
  ```bash
  # Before opening or updating a PR, sync with main:
  git fetch origin main
  git rebase origin/main
  # Resolve any conflicts if needed, then:
  git push origin <branch-name> --force-with-lease
  ```
