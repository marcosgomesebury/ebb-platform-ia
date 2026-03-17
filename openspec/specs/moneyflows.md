# Especificação de Arquitetura - moneyflows

## Visão Geral
O projeto `moneyflows` lida com o trânsito de dinheiro financeiro, conciliações e integrações com o Banco Central (Bacen).

## Componentes Identificados
- **Integração BACEN/PIX:** 
  - `bacen`
  - `ebb-pix-dict-gitops` (Diretório de Identificadores de Contas Transacionais - DICT do Pix)
  - `ebb-pix-spi-gitops` e `ebb-pix-spi` (Sistema de Pagamentos Instantâneos)
- **Conciliação e Contas:** 
  - `ebb-conciliacao`
  - `ebb-account-gitops`
- **Contencioso/Judicial:**
  - `ebb-legal-proceedings-gitops`
- **Segurança/Infra:**
  - `ebb-jd-certificate-hsm-gitops` (Integração com Hardware Security Modules para certificados)

## Tecnologias e Padrões (Inferidos)
- Forte presença do ecossistema de pagamentos brasileiro (PIX, BACEN, SPB/SPI, DICT).
- Necessidade de alta segurança (uso de HSM).
- Processos de backoffice (conciliação, processos legais/bloqueios judiciais).
