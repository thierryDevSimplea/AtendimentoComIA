# WattZap — Documentação do Projeto

Vault de documentação do **WattZap**: sistema de captação e processamento de leads para planos de saúde PME/PJ via WhatsApp + IA.

> [!info] Status do ambiente (2026-05-21)
> Roda **nativo** (sem Docker). PostgreSQL 16 como serviço Windows + Evolution API via `npm start`. IA pelo **Groq** (gratuito), com migração futura pra OpenAI.

## Mapa da documentação

- [[01 - Arquitetura]] — como as peças se conectam (nativo, não Docker)
- [[02 - Como Subir o Ambiente]] — passo a passo pra ligar tudo do zero
- [[03 - Agente IA (Groq)]] — proxy, prompt e troca de provedor
- [[04 - Workflow n8n]] — fluxo de atendimento, nós e atualização
- [[05 - WhatsApp e Evolution API]] — instância, reconexão, painel
- [[07 - Pipeline de Leads (Monday)]] — origem dos leads (Monday) e disparo
- [[08 - Fluxo do Agente (PF e PJ)]] — fluxo de conversa atual (documento vivo)
- [[09 - Planilha de Leads]] — campos e origem (conversa/Monday/documento/automático)
- [[10 - Estrutura do Projeto (arquivos)]] — mapa de todos os arquivos/scripts
- [[11 - Roadmap e Pendências]] — o que está pronto e o que falta finalizar
- [[12 - Acessos e Credenciais]] — mapa de acessos (segredos em arquivo local não-versionado)
- [[06 - Changelog]] — histórico de versões e mudanças

## Referências externas

- PRD completo: `../PRD.md`
- Andamento (legado, parcialmente desatualizado): `../ANDAMENTO_PROJETO.md`
