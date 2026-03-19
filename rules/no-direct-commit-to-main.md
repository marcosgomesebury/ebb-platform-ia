# Rule: Never Commit Directly to Main

- **Nome da Regra:** no-direct-commit-to-main
- **Descrição:** Never commit or push directly to the `main` branch. All changes must go through a feature branch and be merged via Pull Request.
- **Condições de disparo:**
  - Ao fazer commit em qualquer repositório
  - Ao fazer push em qualquer repositório
  - Ao sugerir comandos git ao usuário
- **Ações automáticas:**
  - Verificar se a branch atual é `main` antes de qualquer commit ou push
  - Se estiver na `main`, alertar e recusar o commit
  - Sugerir criação de uma feature branch antes de prosseguir
  - Nunca gerar comandos que façam commit ou push direto na `main`
- **Exemplo de uso:**
  ```bash
  # Wrong — never do this:
  git checkout main
  git commit -m "fix: something"
  git push origin main

  # Correct — always use a feature branch:
  git checkout -b feat/my-change
  git commit -m "fix: something"
  git push origin feat/my-change
  # Then open a Pull Request to merge into main
  ```
