# Especificação de Arquitetura - webpayments

## Visão Geral
O projeto `webpayments` lida com a captura, cotização e roteamento de pagamentos web.

## Componentes Identificados
- **Core / APIs:** `ebb-wp-core-gitops`, `ebb-wp-core-tests`, `ebb-wp-documentation-gitops`, `ebb-external-api-documentation-gitops`
- **Pré-processamento / Conversão:** `ebb-wp-pre-validation-gitops`, `ebb-wp-file-converter-gitops`, `ebb-wp-file-processor-gitops`, `ebb-wp-uploads-gitops`
- **Módulos de Negócio (WP):** 
  - `ebb-wp-quotes-gitops` (Cotações)
  - `ebb-wp-hedges-gitops` (Hedge de câmbio/risco)
  - `ebb-wp-merchants-gitops` e `ebb-proxy-merchants-gitops` (Gestão de lojistas/merchants)
  - `ebb-partners-settings-gitops` (Parceiros)
  - `ebb-wp-data-gitops`, `ebb-wp-query-gitops`
- **Suporte:** `ebb-wp-notification-adp-gitops` (Adapters de notificação), `ebb-wp-mocks-gitops`

## Tecnologias e Processos
Focado em processamento em lote de arquivos de pagamentos (`file-processor`, `uploads`, `converter`), além de transações síncronas para cotações (`quotes`) e proteção cambial (`hedges`), atendendo "merchants" e parceiros.
