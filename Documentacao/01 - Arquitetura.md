# Arquitetura

> [!warning] Mudança importante (2026-05-21)
> O ambiente **não usa mais Docker**. O Docker Desktop quebrou (socket `dockerInference` órfão) e o projeto na verdade já rodava com PostgreSQL nativo + Node. O `ANDAMENTO_PROJETO.md` antigo diz "Docker Compose" — isso está **desatualizado**.

## Visão geral do fluxo

```
WhatsApp (cliente)
   │
   ▼
Evolution API (localhost:8080, Baileys)  ── Postgres 16 nativo (localhost:5432)
   │  webhook messages.upsert
   ▼
n8n (remoto: simplea-teste.37-148-135-242.sslip.io)
   │  Code node: filtro + monta prompt
   ▼
Proxy IA (localhost:3456)  ──► Groq API (llama-3.3-70b-versatile)
   │  resposta
   ▼
Evolution API /message/sendText  ──► WhatsApp (cliente)
```

O proxy local é exposto ao n8n remoto via **tunnel Cloudflare**.

## Componentes

| Componente | Onde roda | Como sobe |
|------------|-----------|-----------|
| PostgreSQL 16 | Serviço Windows `postgresql-x64-16` | Já inicia com o Windows |
| Evolution API v2.3.7 | `C:/Atendimento2/evolution-api` | `npm start` (tsx) |
| Proxy IA (Groq) | `C:/Atendimento2/proxy-ai.js` | `node proxy-ai.js` (porta 3456) |
| Consulta CNS | `C:/Atendimento2/consulta-cns.js` | `node` (porta 3457, Puppeteer) |
| n8n | Servidor remoto | Já hospedado |
| Tunnel Cloudflare | local | `cloudflared tunnel --url` |

Ver [[02 - Como Subir o Ambiente]] para o passo a passo.
