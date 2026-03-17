# Rule: Validar .env antes de commit

- **Nome da Regra:** pre-commit-env-check
- **Descrição:** Garantir que arquivos .env e credentials nunca sejam commitados no repositório Git
- **Condições de disparo:** 
  - Ao criar novo arquivo .env em qualquer skill
  - Ao modificar .gitignore
  - Ao criar novo skill com credenciais
- **Ações automáticas:**
  - Verificar se .env está listado no .gitignore
  - Verificar se credentials*.yaml está no .gitignore
  - Alertar usuário se não estiver protegido
  - Sugerir adicionar padrões ao .gitignore:
    ```
    *.env
    .env*
    credentials*.yaml
    secrets/
    *.pem
    *.key
    ```
  - Criar .env.example como template seguro
- **Exemplo de uso:**
  ```bash
  # Ao criar novo skill:
  mkdir skills/novo_skill
  touch skills/novo_skill/.env
  # → Regra dispara: Verifica .gitignore e sugere proteção
  ```
