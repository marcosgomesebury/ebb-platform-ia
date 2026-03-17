# Especificação de Arquitetura - clientjourney

## Visão Geral
O projeto `clientjourney` (também conhecido centralmente pelas pastas `temis-*` e `ebb-temis-*`) parece ser o coração do Onboarding, Compliance e Gestão de Contas e Cadastros (Bureau, Risk, Fraud).

## Componentes Identificados
A maioria dos repositórios segue a nomenclatura `ebb-temis-[módulo]-gitops` ou `temis-[módulo]-gitops`, sugerindo uma arquitetura baseada em microsserviços com deploy via GitOps (provavelmente ArgoCD ou Flux).

Módulos principais identificados:
- **BFF (Backend for Frontend):** `ebb-temis-bff-gitops`
- **Bureau & Dados:** `ebb-temis-bureau-gitops`, `ebb-temis-bureau-data-integrator-gitops`
- **Compliance & Risco:** `ebb-temis-compliance-gitops`, `ebb-temis-compliance-action-gitops`, `ebb-temis-compliance-screening-gitops`, `ebb-temis-fraud-gitops`, `ebb-temis-risk-gitops`, `ebb-temis-restrictive-lists-gitops`
- **Gestão e Cadastro:** `ebb-temis-registration-gitops`, `ebb-temis-internal-account-management-gitops`, `ebb-temis-onboarding-engine-gitops`
- **Mensageria e Notificações:** `ebb-temis-email-sender-gitops`, `ebb-temis-notification-gitops`
- **Integrações (Adapters):** `ebb-temis-salesforce-adapter-gitops`, `ebb-temis-tree-adapter-gitops`, `ebb-temis-tas-integrator-gitops`
- **Outros:** `ebb-temis-config-gitops`, `ebb-temis-digital-signature-gitops`, `ebb-temis-enrichment-gitops`, `ebb-temis-expiration-date-gitops`, `ebb-temis-limit-gitops`, `ebb-temis-query-gitops`, `ebb-temis-mocks-v2-gitops`

## Tecnologias e Padrões (Inferidos)
- **GitOps:** Forte presença do sufixo `-gitops`, indicando repositórios declarativos de infraestrutura/deploy Kubernetes.
- **Arquitetura Orientada a Eventos / Microsserviços:** A divisão granular sugere comunicação via eventos ou APIs REST/gRPC entre módulos pequenos e especializados.
- **Integração com CRMs/Terceiros:** `salesforce-adapter` indica integração forte com SFDC para gestão de clientes.

## Status Analítico
- [x] Diretórios listados
- [ ] Código-fonte dos microsserviços analisado (Nota: os diretórios atuais são repositórios GitOps, o código-fonte das aplicações em si pode estar em subpastas ou em outros repositórios não listados aqui).
