# Como Subir o Ambiente (do zero)

Passo a passo para ligar todo o stack do WattZap. Roda **nativo**, sem Docker.

## 1. PostgreSQL

Já roda como serviço do Windows. Conferir:

```powershell
Get-Service postgresql-x64-16
```

- Banco: `evolution` em `localhost:5432`
- Conexão (no `.env` da evolution-api): `postgresql://postgres:postgres@localhost:5432/evolution?schema=public`

## 2. Evolution API

```powershell
cd C:\Atendimento2\evolution-api
npm start
```

- Sobe na porta **8080**
- API Key global: `evo_wattzap_2026`
- Conferir: `curl http://localhost:8080` deve responder com `version` e `manager`

## 3. Proxy IA (Groq)

```powershell
cd C:\Atendimento2
$env:GROQ_API_KEY = "gsk_..."   # sua chave do Groq
node proxy-ai.js
```

- Sobe na porta **3456**
- Encaminha para o Groq. Ver [[03 - Agente IA (Groq)]]

## 4. Tunnel Cloudflare (expor proxy ao n8n)

```powershell
& "C:\Users\Thierry\ngrok\cloudflared.exe" tunnel --url http://localhost:3456
```

- Copiar a URL `https://*.trycloudflare.com` gerada
- Atualizar `TUNNEL_URL` no `update_workflow.py` e reimportar o workflow no n8n. Ver [[04 - Workflow n8n]]

## 5. WhatsApp

Reconectar a instância `wattzap`. Ver [[05 - WhatsApp e Evolution API]].

## 6. Validar

Enviar mensagem de teste ao número conectado e confirmar resposta da IA.
