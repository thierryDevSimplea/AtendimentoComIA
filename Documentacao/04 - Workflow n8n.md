# Workflow n8n

## Onde fica

- n8n remoto: `https://simplea-teste.37-148-135-242.sslip.io`
- Arquivo exportável: `C:/Users/Thierry/Downloads/workflow-wattzap-v4.json`
- Script que regenera os nós Code: `C:/Atendimento2/update_workflow.py`

## Nós do fluxo

1. **Webhook** (`wattzap-incoming`) — recebe `messages.upsert` da Evolution API
2. **filtro-parse** (Code) — ignora fromMe/grupos/broadcast/mensagens antigas (>60s); casa o número no `leadsDB`; extrai texto/mídia; anexa `leadNome/leadTipo/leadDependentes`
3. **chamar-ia** (Code) — monta system prompt (fluxo PJ/PF, plano anterior, docs, vínculo dependentes) e chama o proxy via `TUNNEL_URL` no **formato OpenAI/Groq**, lê `choices[0].message.content`
4. **enviar** (HTTP) — `POST /message/sendText/wattzap` na Evolution API

## leadsDB (hardcoded, teste)

| Número        | Nome             | Tipo | Deps |
| ------------- | ---------------- | ---- | ---- |
| 5516991420538 | Gilson Ferreira  | PF   | 1    |
| 5518998171940 | Gabriel Henrique | PJ   | 2    |
| 5516997868188 | Affonso          | PF   | 0    |
| 5521971059196 | Thierry          | PF   | 0    |

> [!note] O número real conectado agora é **5521994746793**. Se for testar com ele, adicionar ao `leadsDB`.

## Atualizar o workflow

1. Editar `TUNNEL_URL` em `update_workflow.py` com a URL nova do Cloudflare
2. `python C:/Atendimento2/update_workflow.py`
3. Reimportar o JSON no n8n e ativar

Ver [[03 - Agente IA (Groq)]] para o formato da chamada.
