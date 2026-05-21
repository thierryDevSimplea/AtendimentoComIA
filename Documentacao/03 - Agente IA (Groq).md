# Agente IA (Groq)

## Provedor atual: Groq (gratuito)

A IA original usava `aibee.cloud` (revenda de Claude), mas a chave deu **401 (morta)**. Trocamos pelo **Groq**:

- Endpoint: `https://api.groq.com/openai/v1/chat/completions`
- Modelo: `llama-3.3-70b-versatile`
- Autenticação: `Authorization: Bearer <GROQ_API_KEY>`
- Gratuito, sem cartão. Chave criada em `console.groq.com/keys`
- **API compatível com OpenAI** → migração futura é trocar só URL + chave

## proxy-ai.js

Proxy local na porta **3456** (`C:/Atendimento2/proxy-ai.js`). Recebe o POST do n8n e encaminha pro Groq. A chave vem da env var `GROQ_API_KEY` (não fica hardcoded).

```powershell
$env:GROQ_API_KEY = "gsk_..."; node proxy-ai.js
```

## Migração futura pra OpenAI (produção)

No `proxy-ai.js`, trocar:

- `UPSTREAM_HOST` → `api.openai.com`
- `UPSTREAM_PATH` → `/v1/chat/completions`
- `DEFAULT_MODEL` → ex. `gpt-4o-mini`
- env var → `OPENAI_API_KEY`

O nó do n8n não muda (já está no formato OpenAI). Ver [[04 - Workflow n8n]].

## Formato da chamada (compatível OpenAI)

```json
{
  "model": "llama-3.3-70b-versatile",
  "max_tokens": 700,
  "messages": [
    {"role": "system", "content": "<system prompt do agente>"},
    {"role": "user", "content": "<mensagem do cliente>"}
  ]
}
```

Resposta lida em `choices[0].message.content`.
