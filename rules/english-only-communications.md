# Rule: English-Only for PRs, GitHub, and Code

- **Nome da Regra:** english-only-communications
- **Descrição:** All comments in Pull Requests, GitHub (issues, discussions, reviews), and code (inline comments, docstrings, commit messages) must be written in English.
- **Condições de disparo:**
  - Ao escrever comentários em código (inline comments, docstrings, TODOs)
  - Ao criar ou revisar Pull Requests (título, descrição, review comments)
  - Ao escrever commit messages
  - Ao criar ou comentar em GitHub Issues e Discussions
- **Ações automáticas:**
  - Garantir que todo texto gerado para PRs, reviews e issues esteja em inglês
  - Garantir que comentários em código (inline, block, docstrings) sejam escritos em inglês
  - Garantir que commit messages sigam convenções em inglês
  - Alertar se detectar comentários em outro idioma no código
- **Exemplo de uso:**
  ```python
  # Good:
  # Calculate the total amount after applying discounts
  def calculate_total(amount, discount):
      ...

  # Bad:
  # Calcula o valor total após aplicar descontos
  def calculate_total(amount, discount):
      ...
  ```

  ```
  # Good commit message:
  feat: add currency conversion endpoint

  # Bad commit message:
  feat: adiciona endpoint de conversão de moeda
  ```

  ```markdown
  # Good PR description:
  ## Summary
  This PR adds the currency conversion endpoint for the FX module.

  # Bad PR description:
  ## Resumo
  Este PR adiciona o endpoint de conversão de moeda para o módulo FX.
  ```
