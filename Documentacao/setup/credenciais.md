# Acessos e Credenciais

> [!danger] Segredos NÃO ficam no vault
> Os **valores reais** (chaves, senhas, tokens) estão em `ACESSOS_SECRETO.md` na raiz do projeto, que está no `.gitignore` e **não é publicado no GitHub**. Este doc lista os pontos de acesso e onde encontrar cada segredo.

## Mapa de acessos

| Sistema | Onde / usuário | Segredo |
|---------|---------------|---------|
| Evolution API | `http://localhost:8080` + painel `/manager` | API key `evo_wattzap_2026` → `ACESSOS_SECRETO.md` |
| PostgreSQL | serviço `postgresql-x64-16`, banco `evolution` | usuário/senha `postgres`/`postgres` → `ACESSOS_SECRETO.md` |
| Groq (IA) | console.groq.com | API key `gsk_...` → `ACESSOS_SECRETO.md` (env `GROQ_API_KEY`) |
| n8n | `https://simplea-teste.37-148-135-242.sslip.io` | JWT da API → `ACESSOS_SECRETO.md` |
| GitHub | conta `thierryDevSimplea` / pessoal `@ThierryDev499` | senha + **PAT** → `ACESSOS_SECRETO.md` |
| Monday (futuro) | CRM, origem dos leads | sem credenciais ainda |
| WhatsApp | instância `wattzap`, número `5521994746793` | via Evolution API |

## Boas práticas

- **Nunca commitar segredos.** O `.gitignore` já protege `ACESSOS_SECRETO.md`, `.env`, `*.log` e temporários.
- A **chave do Groq** apareceu no chat → revogar e gerar nova antes de produção.
- A **senha do GitHub** apareceu no chat → trocar; usar **PAT** para push (o GitHub não aceita senha em push).
- Em produção, mover segredos para **variáveis de ambiente** / cofre, não arquivos.
- Tunnels Cloudflare são **efêmeros** — não são "acesso fixo"; regenerar e atualizar nos workflows quando reiniciar.

Ver também [Estrutura de Arquivos](../projeto/estrutura-arquivos.md) e [Como Subir o Ambiente](ambiente.md).
