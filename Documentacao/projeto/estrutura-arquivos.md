# Estrutura do Projeto (arquivos)

Mapa dos arquivos em `C:\Atendimento2`. Para subir o ambiente ver [Como Subir o Ambiente](../setup/ambiente.md).

## Serviços / código

| Arquivo | O que faz | Porta |
|---------|-----------|-------|
| `proxy-ai.js` | Proxy da IA → encaminha pro **Groq** (formato OpenAI). Chave via env `GROQ_API_KEY`. Ver [Agente IA (Groq)](../servicos/agente-ia.md) | 3456 |
| `consulta-cns.js` | Serviço que busca o **CNS** no DataSUS por CPF+nascimento (Puppeteer). **Ainda não integrado** ao fluxo | 3457 |
| `consulta-cns.mjs` | Versão ESM do anterior | — |
| `evolution-api/` | Evolution API v2.3.7 (WhatsApp via Baileys). Sobe com `npm start`. Ver [WhatsApp e Evolution API](../servicos/whatsapp.md) | 8080 |

## Dados / configuração

| Arquivo | O que é |
|---------|---------|
| `leads.json` | Lista dos 4 leads (number, nome, tipo, dependentes) + bloco `monday` (fixo hoje). Ver [Pipeline de Leads](../negocio/pipeline-leads.md) |
| `planilha_leads.xlsx` | Planilha final (Dashboard + Leads PF + Leads PJ). Ver [Planilha de Leads](../negocio/planilha-leads.md) |
| `criar_planilha.py` | Gera/regenera a planilha acima |
| `template_dados_lead.txt` | Template do arquivo consolidado por lead (espelha a planilha) |

## Scripts de deploy do n8n

| Arquivo | O que faz |
|---------|-----------|
| `update_workflow.py` | Reescreve os nós `filtro-parse` e `chamar-ia` do **agente** + injeta `TUNNEL_URL` do proxy. Gera `workflow-wattzap-v4.json` (em Downloads) |
| `update_disparo.py` | Reescreve os nós do **disparo** (lista, mensagem, envio) com marca Kaizen + tunnel novo |
| `workflow-teste-lead.json` | Workflow de teste manual (legado) |
| `disparo*.json`, `wf-payload.json`, `wf-put-resp.json`, `qr.json` | Arquivos temporários de chamadas à API do n8n / Evolution |
| `*.log` (evo, proxy, tunnel-evo, tunnel-proxy) | Logs de execução dos serviços/tunnels |

## Documentação

| Arquivo | O que é |
|---------|---------|
| `PRD.md` | Requisitos completos do produto |
| `ANDAMENTO_PROJETO.md` | Doc legado — **desatualizado** (diz Docker). Usar este vault como fonte |
| `Documentacao/` | Este vault |

## IDs e endpoints úteis

- n8n: `https://simplea-teste.37-148-135-242.sslip.io` — workflows: agente `eRxPk9c1ZhjsLi05`, disparo `EhCYZjF26O0hZSIi`
- Evolution API: `http://localhost:8080` — instância `wattzap`, API key `evo_wattzap_2026`
- Webhooks n8n: agente `wattzap-incoming`, disparo `wattzap-disparo`
- Tunnels Cloudflare são **efêmeros** — mudam a cada reinício (atualizar nos workflows). Ver [Como Subir o Ambiente](../setup/ambiente.md)
