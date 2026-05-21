# WattZap - Andamento do Projeto

**Última atualização:** 19/05/2026  
**Status geral:** Fase 1 parcialmente concluída, Fase 2 em andamento

---

## ✅ O QUE JÁ FOI FEITO

### 1. Infraestrutura Base
- [x] **Evolution API** instalada e configurada (Docker Compose)
  - Container: evolution_api (porta 8080)
  - Container: evolution_redis
  - Container: evolution_postgres (PostgreSQL 15)
  - Container: evolution_frontend (porta 3000)
  - API Key: `evo_wattzap_2026`
- [x] **Instância WhatsApp "wattzap"** criada e conectada
- [x] **n8n** rodando no servidor remoto: `https://simplea-teste.37-148-135-242.sslip.io`
- [x] **Cloudflare Tunnel** configurado para expor a Evolution API local ao n8n

### 2. Documentação
- [x] **PRD.md** completo com:
  - Visão geral, problema, solução
  - Arquitetura do fluxo
  - Fontes de dados e estrutura de pastas
  - Regras de negócio (tipos de cadastro, documentos obrigatórios, vínculos)
  - Campos da planilha final
  - Fluxo do agente de atendimento WhatsApp
  - System prompt do agente
  - Mensagens padrão
  - Roadmap completo

### 3. Scripts Auxiliares
- [x] **proxy-ai.js** — Proxy local (porta 3456) para API Claude via aibee.cloud
  - Redireciona chamadas para `api.aibee.cloud/v1/messages`
  - Usado pelo n8n para chamar a IA sem expor a chave diretamente
- [x] **consulta-cns.js / consulta-cns.mjs** — Serviço de consulta CNS (porta 3457)
  - Usa Puppeteer para consultar CNS pelo CPF + data de nascimento
  - Acessa portal CNES/DataSUS automaticamente
- [x] **workflow-teste-lead.json** — Workflow n8n de teste para envio de primeira mensagem

### 4. Workflows n8n (Testados)
- [x] Múltiplas versões de workflow testadas no n8n remoto
- [x] Webhook de entrada configurado: `wattzap-incoming`
- [x] Integração Evolution API → n8n (webhook de mensagens recebidas)
- [x] Envio de mensagens via Evolution API (`/message/sendText/wattzap`)
- [x] Testes de payload simulando mensagens de cliente

### 5. Configuração Evolution API
- [x] `.env` configurado com:
  - PostgreSQL local
  - Cache local (Redis desabilitado para simplificar)
  - Webhook de mensagens habilitado
  - Idioma PT-BR
  - Nome do cliente: "WattZap"

---

## ❌ O QUE FALTA IMPLEMENTAR

### Fase 1 - MVP (Prioridade Alta)

| # | Tarefa | Descrição | Complexidade |
|---|--------|-----------|--------------|
| 1 | **OCR via API ChatGPT Vision** | Receber documento (imagem/PDF), enviar para API Vision, extrair dados estruturados (nome, CPF, endereço, etc.) | Alta |
| 2 | **Script de preenchimento da planilha** | Python/openpyxl que lê dados_consolidados.txt e preenche a planilha Excel modelo | Média |
| 3 | **Workflow n8n definitivo** | Versão final do workflow com todos os nós funcionando end-to-end | Alta |

### Fase 2 - Automação Parcial (Prioridade Média)

| # | Tarefa | Descrição | Complexidade |
|---|--------|-----------|--------------|
| 4 | **Agente IA no n8n** | Nó Code que monta o prompt com contexto do lead + histórico e chama a API Claude | Alta |
| 5 | **Processamento de mídia** | Detectar quando cliente envia imagem/documento, baixar via Evolution API, salvar na pasta do lead | Média |
| 6 | **Gerenciamento de pastas** | Criar pasta do lead automaticamente, organizar documentos por beneficiário/dependente | Média |
| 7 | **Atualização de dados_wattzap.txt** | Após cada interação, registrar informações obtidas na conversa | Baixa |
| 8 | **Busca automática de CNS** | Integrar consulta-cns.js no fluxo (já tem o script, falta integrar no n8n) | Média |
| 9 | **Base de conhecimento do agente** | Criar arquivo com planos disponíveis, valores, carência, rede credenciada | Baixa |
| 10 | **Notificação de pendências** | Agente cobra documentos faltantes após período sem resposta | Média |

### Fase 3 - Automação Completa (Prioridade Futura)

| # | Tarefa | Descrição | Complexidade |
|---|--------|-----------|--------------|
| 11 | **Integração Monday.com** | Webhook do Monday dispara primeiro contato quando lead é aprovado | Alta |
| 12 | **Dashboard React em tempo real** | Conectar dashboard aos dados reais (atualmente é protótipo estático) | Alta |
| 13 | **Pipeline completo end-to-end** | Monday → WhatsApp → OCR → Planilha → Operadora sem intervenção | Alta |
| 14 | **Métricas do agente** | Tempo de coleta, taxa de resolução, mensagens por atendimento | Média |
| 15 | **Aprovação Meta (API oficial)** | Migrar de Baileys para WhatsApp Business API oficial | Externa |

---

## 🔧 PROBLEMAS CONHECIDOS / PENDÊNCIAS TÉCNICAS

1. **API Key aibee.cloud** — Erro 401 (Invalid API key) na última tentativa de chamar a IA
   - Possível expiração da chave `sk-kpa-94878f18...`
   - Ação: verificar/renovar chave ou trocar para outra API compatível

2. **Cloudflare Tunnel** — URL temporária muda a cada reinício
   - URL atual pode estar expirada (era `attempt-toddler-generations-attractive.trycloudflare.com`)
   - Ação: configurar tunnel fixo ou usar alternativa (ngrok com domínio fixo)

3. **Redis desabilitado** — Usando cache local por simplicidade
   - Para produção, habilitar Redis para persistência de sessão

4. **n8n remoto** — Workflows criados via API podem precisar ser recriados
   - Vários workflows foram deletados durante testes
   - O workflow definitivo precisa ser criado e ativado

5. **Webhook Evolution → n8n** — Precisa reconfigurar após mudança de URL do tunnel
   - Endpoint: `POST /webhook/set/wattzap` com a URL correta do n8n

---

## 📋 PRÓXIMOS PASSOS RECOMENDADOS (em ordem)

1. **Resolver o erro 401 da API de IA** — Sem isso, o agente não funciona
2. **Estabilizar o tunnel** — URL fixa para o webhook funcionar consistentemente
3. **Criar workflow n8n definitivo** com:
   - Webhook de entrada (recebe mensagem)
   - Filtro (ignora mensagens próprias/fromMe)
   - Chamada à IA com system prompt + contexto
   - Envio de resposta via Evolution API
4. **Adicionar processamento de mídia** ao workflow
5. **Implementar OCR** para documentos recebidos
6. **Criar script Python** para preencher planilha

---

## 🗂️ ESTRUTURA DE ARQUIVOS DO PROJETO

```
C:\Atendimento2\
├── PRD.md                      # Documento de requisitos completo
├── ANDAMENTO_PROJETO.md        # Este arquivo
├── proxy-ai.js                 # Proxy para API Claude (porta 3456)
├── consulta-cns.js             # Consulta CNS via Puppeteer (porta 3457)
├── consulta-cns.mjs            # Versão ESM do consulta-cns
├── workflow-teste-lead.json    # Workflow n8n de teste
├── package.json                # Dependências (puppeteer)
├── node_modules/               # Dependências instaladas
└── evolution-api/              # Evolution API (Docker)
    ├── .env                    # Configuração da API
    ├── docker-compose.yaml     # Stack Docker
    └── src/                    # Código fonte da Evolution API
```

---

## 🔑 CREDENCIAIS E ENDPOINTS

| Recurso | Valor |
|---------|-------|
| Evolution API (local) | `http://localhost:8080` |
| Evolution API Key | `evo_wattzap_2026` |
| Instância WhatsApp | `wattzap` |
| n8n (remoto) | `https://simplea-teste.37-148-135-242.sslip.io` |
| n8n API Key | JWT (ver settings.local.json) |
| Proxy IA (local) | `http://localhost:3456` |
| Consulta CNS (local) | `http://localhost:3457` |
| API IA (aibee) | `https://api.aibee.cloud/v1/messages` |
| Número WhatsApp teste | `5521971059196` |
