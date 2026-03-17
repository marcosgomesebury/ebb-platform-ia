# Portfolio de Projetos - Marcos Gomes

Este diretório mantém a especificação global e o estado atual da arquitetura dos projetos de software de Marcos Gomes, localizados em `/home/marcosgomes/Projects`. 

A estrutura utiliza a metodologia OpenSpec (Spec-Driven Development) para garantir que a IA (Antigravity) mantenha o contexto contínuo, previsível e determinístico sobre as regras de negócio de cada módulo, impedindo a perda de contexto ou "amnésia" durante as sessões.

## Diretórios Monitorados
- **clientjourney**: Especificação inicial arquitetural arquivada (Onboarding, Risk, Bureau).
- **fx**: Especificação inicial arquitetural arquivada (Integração Câmbio).
- **moneyflows**: Especificação inicial arquitetural arquivada (Bacen, Contas, Conciliação).
- **platform**: Especificação inicial arquitetural arquivada (Engenharia e Plataforma).
- **pocs**: Provas de conceito (Ignoradas da documentação central).
- **treasury**: Especificação inicial arquitetural arquivada.
- **webpayments**: Especificação inicial arquitetural arquivada (Captura e Processamento).

## Regras de Trabalho (OpenSpec)
1. Antes de iniciar qualquer codificação profunda, documentar as especificações na pasta `specs/`.
2. As mudanças ou novas propostas devem ser descritas em arquivos provisórios na pasta `changes/` antes de serem implementadas, sendo movidas para `specs/` após concluídas.
3. Este arquivo manterá uma visão arquitetural de alto nível.
