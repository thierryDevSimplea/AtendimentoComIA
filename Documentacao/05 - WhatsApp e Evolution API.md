# WhatsApp e Evolution API

## Instância

- Nome: `wattzap`
- Número conectado: **5521994746793**
- API Key: `evo_wattzap_2026`
- Base URL: `http://localhost:8080`

## Reconectar (QR code)

A instância desconecta de tempos em tempos (estado `close`). Para reconectar:

### Opção recomendada — Painel da Evolution API

1. Abrir `http://localhost:8080/manager`
2. Login: Server URL `http://localhost:8080` + API Key `evo_wattzap_2026`
3. Selecionar instância `wattzap` → **Connect**
4. O QR **se renova sozinho** no painel → escanear com calma
   - WhatsApp → Aparelhos conectados → Conectar um aparelho

### Opção via API (QR expira em ~40s)

```powershell
curl -H "apikey: evo_wattzap_2026" "http://localhost:8080/instance/connect/wattzap"
```

Retorna `base64` (imagem do QR). O QR expira rápido — o painel é mais confiável.

## Conferir estado

```powershell
curl -H "apikey: evo_wattzap_2026" "http://localhost:8080/instance/connectionState/wattzap"
```

Estados: `close` (desconectado) → `connecting` (aguardando scan) → `open` (conectado ✓).

## Webhook (Evolution → n8n)

Configurar o webhook da instância apontando pro n8n (`/webhook/wattzap-incoming`) após cada mudança de URL do tunnel.

## Problemas conhecidos

- **Pairing code** (`?number=`) retorna `None` nessa versão — usar QR pelo painel.
- Instância presa em `connecting`: reiniciar com `POST /instance/restart/wattzap`.
