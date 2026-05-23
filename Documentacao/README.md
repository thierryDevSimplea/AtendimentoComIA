# WattZap — Documentação do Projeto

Sistema de captação e processamento de leads para planos de saúde PME/PJ via WhatsApp + IA.

> [!info] Status do ambiente (2026-05-21)
> Roda **nativo** (sem Docker). PostgreSQL 16 como serviço Windows + Evolution API via `npm start`. IA pelo **Groq** (gratuito), com migração futura pra OpenAI.

## Mapa da documentação

### Setup e Infraestrutura

| Doc | O que cobre |
|-----|-------------|
| [Arquitetura](setup/arquitetura.md) | Como as peças se conectam (nativo, não Docker) |
| [Como Subir o Ambiente](setup/ambiente.md) | Passo a passo pra ligar tudo do zero |
| [Acessos e Credenciais](setup/credenciais.md) | Mapa de acessos (segredos em arquivo local não-versionado) |

### Serviços

| Doc | O que cobre |
|-----|-------------|
| [Agente IA (Groq)](servicos/agente-ia.md) | Proxy, prompt e troca de provedor |
| [Workflow n8n](servicos/workflow-n8n.md) | Fluxo de atendimento, nós e atualização |
| [WhatsApp e Evolution API](servicos/whatsapp.md) | Instância, reconexão, painel |

### Negócio e Fluxo

| Doc | O que cobre |
|-----|-------------|
| [Pipeline de Leads (Monday)](negocio/pipeline-leads.md) | Origem dos leads (Monday) e disparo |
| [Fluxo do Agente (PF e PJ)](negocio/fluxo-agente.md) | Fluxo de conversa atual — documento vivo |
| [Planilha de Leads](negocio/planilha-leads.md) | Campos e origem (conversa/Monday/documento/automático) |

### Projeto

| Doc | O que cobre |
|-----|-------------|
| [Estrutura de Arquivos](projeto/estrutura-arquivos.md) | Mapa de todos os arquivos e scripts |
| [Roadmap e Pendências](projeto/roadmap.md) | O que está pronto e o que falta finalizar |
| [Testes e Correções](projeto/testes-correcoes.md) | Registro de testes end-to-end e correções aplicadas |
| [Changelog](projeto/changelog.md) | Histórico de versões e mudanças |

## Referências externas

- PRD completo: [`../PRD.md`](../PRD.md)
- Andamento (legado, parcialmente desatualizado): [`../ANDAMENTO_PROJETO.md`](../ANDAMENTO_PROJETO.md)
