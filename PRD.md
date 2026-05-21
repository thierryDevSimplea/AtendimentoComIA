# PRD - WattZap: Sistema de Captação e Processamento de Leads para Planos de Saúde

**Versão:** 1.1
**Data:** 21/05/2026 (orig. 18/05/2026)
**Autor:** Thierry de Matos Azevedo
**Status:** Em desenvolvimento — fase de teste do agente

---

## 0. Status de Implementação (2026-05-21)

> Documentação operacional completa no vault Obsidian em `Documentacao/`. Esta seção resume o que já foi construído vs. a visão do PRD.

**Pronto:**
- Ambiente roda **nativo** (PostgreSQL 16 + Evolution API via `npm start`), **sem Docker**.
- Agente conversacional no WhatsApp ativo (Evolution API + n8n).
- **IA conversacional: Groq** (`llama-3.3-70b-versatile`, gratuito) na fase de teste — formato compatível com OpenAI, **migração para OpenAI/ChatGPT em produção** é trocar URL+chave.
- Fluxos PF/PJ definidos (confirma titular, plano anterior, dados do beneficiário, dependentes com vínculo).
- Planilha + arquivo consolidado do lead estruturados, com grupo de campos vindos do Monday.

**Pendente (ver `11 - Roadmap e Pendências` no vault):**
- OCR/IA Vision dos documentos (endereço, status de docs, cargo).
- Integração Monday → n8n (hoje a lista de leads é manual em `leads.json`).
- Integração da busca de CNS (`consulta-cns.js`).
- Migração da IA para OpenAI em produção.

> Onde o PRD cita "API ChatGPT/Vision": é o alvo de **produção**. No teste atual a IA conversacional é o **Groq**.

---

## 1. Visão Geral

O WattZap é um sistema de automação para captação, validação e processamento de leads de planos de saúde PME/PJ. O fluxo integra Monday.com (CRM), WhatsApp (comunicação com o cliente), n8n (orquestração), OCR/IA (extração de dados de documentos) e uma planilha Excel (output final para aceitação do plano).

O objetivo é reduzir ao máximo o trabalho manual de coleta e preenchimento de dados, automatizando a extração de informações dos documentos enviados pelo cliente e consolidando tudo em uma planilha pronta para submissão à operadora.

---

## 2. Problema

Atualmente, o processo de cadastro de beneficiários para planos de saúde PME/PJ envolve:

- Coleta manual de dados de múltiplas fontes (Monday, WhatsApp, documentos)
- Preenchimento manual de planilhas extensas com dados de empresa, beneficiário e dependentes
- Verificação manual de documentos obrigatórios
- Retrabalho quando documentos estão incompletos ou dados inconsistentes
- Falta de visibilidade sobre o status de cada lead

---

## 3. Solução

Um pipeline automatizado que:

1. Capta leads do Monday.com
2. Inicia interação via WhatsApp para coleta de documentos
3. Recebe e organiza documentos em estrutura de pastas padronizada
4. Extrai dados automaticamente via OCR/IA (API ChatGPT Vision)
5. Consolida informações de todas as fontes
6. Identifica pendências e dados faltantes
7. Preenche automaticamente a planilha de aceitação do plano
8. Apresenta dashboard com status de cada lead

---

## 4. Arquitetura do Fluxo

```
Monday.com (CRM)
    │
    ▼
WhatsApp (Interação com cliente)
    │
    ▼
n8n (Orquestração)
    │
    ├── Cria pasta do lead
    ├── Organiza documentos recebidos
    ├── Dispara OCR/IA nos documentos
    │
    ▼
API ChatGPT Vision (Extração de dados)
    │
    ▼
Dados Consolidados (.txt)
    │
    ▼
Planilha Excel (Output final)
    │
    ▼
Dashboard (Visão de status)
```

---

## 5. Fontes de Dados

| Fonte | Dados Obtidos |
|-------|---------------|
| Monday.com | Nome do lead, telefone, tipo cadastro (PF/PJ), CNPJ/CPF, quantidade de dependentes, nomes dos dependentes, tipo de vínculo, plano escolhido, vendedor responsável |
| WhatsApp | Confirmação de dados, documentos enviados (fotos/PDFs), informações complementares da conversa |
| OCR/IA (Documentos) | CPF, nome completo, endereço, CEP, cidade, estado, data de nascimento, número de documento, validade |

---

## 6. Estrutura de Pastas por Lead

```
[Nome do Lead] [Telefone]/
├── dados_monday.txt           # Dados vindos do Monday
├── dados_wattzap.txt          # Dados vindos do WhatsApp
├── dados_consolidados.txt     # Junção de todas as fontes
├── dados.txt                  # Template com status de preenchimento
└── Documentos Obrigatorios/
    ├── [Beneficiário]/
    │   ├── DocFoto.pdf
    │   ├── CPF.pdf
    │   ├── ComprovanteResidencia.pdf
    │   └── ContratoSocial.pdf (se PJ)
    ├── [Dependente 1]/
    │   ├── DocFoto.pdf
    │   ├── CPF.pdf
    │   ├── ComprovanteResidencia.pdf
    │   └── ComprovanteVinculo.pdf (se empregado)
    └── [Dependente N]/
        └── ...
```

---

## 7. Regras de Negócio

### 7.1 Tipos de Cadastro

**Pessoa Jurídica (PJ):**
- Obrigatório: Contrato social, CNPJ, dados da empresa
- Beneficiário responsável com documentação completa

**Pessoa Física (PF):**
- Beneficiário responsável com documentação completa

### 7.2 Documentos Obrigatórios - Beneficiário

- Documento com foto (RG com CPF, CNH, Passaporte ou RNE)
- CPF
- Comprovante residencial
- Contrato social (apenas PJ)

### 7.3 Documentos Obrigatórios - Dependentes

- Documento com foto (RG com CPF, CNH, Passaporte ou RNE)
- CPF
- Comprovante residencial
- Se vínculo empregatício: Carteira de trabalho ou holerite

### 7.4 Tipos de Vínculo

- Sócio
- Empregado (requer comprovante: CTPS ou holerite)
- Familiar
- Filho

### 7.5 Regras de Validação

- Se PJ e sem contrato social → sinalizar pendência
- Se vínculo = Empregado e sem CTPS/holerite → sinalizar pendência
- Se documento enviado → executar OCR e extrair dados automaticamente
- Se dado não encontrado no documento → marcar como [PENDENTE]
- CNS deve ser buscado automaticamente pelo CPF no portal correspondente

---

## 8. Campos da Planilha Final (Output)

### Dados da Empresa / Lead
ID Monday, ID WattZap, Nome da Empresa, CNPJ, Nome do Lead, Cidade da Venda, E-mail Contrato, E-mail Financeiro, Telefone, Telefone Secundário, Vigência, Data Mensalidade, Operadora, Produto, Tipo de Plano, Valor Adesão, Fatura Para, Possui Plano Ativo, Qual Plano Atual, Data Plano Atual

### Beneficiário Responsável
Tipo Cadastro (PF/PJ), Nome, CPF, Data Nascimento, Idade, Estado Civil, CNS, CEP, Endereço, Número, Complemento, Cidade, Estado, Telefone, E-mail, Doc Foto (status), CPF Doc (status), Comprovante Residencial (status), Contrato Social (status), Status Docs

### Por Dependente (até 3+)
Nome, Vínculo, CPF, Data Nascimento, Idade, Estado Civil, CNS, CEP, Endereço, Número, Complemento, Cidade, Estado, Telefone, E-mail, Doc Foto (status), CPF Doc (status), Comprovante Residencial (status), Comprovante Vínculo (status), Status Docs

### Geral
Quantidade de Dependentes, Status Geral, Pendências

---

## 9. Integrações

| Sistema | Função | Status |
|---------|--------|--------|
| Monday.com | CRM - captação de leads | Ativo (manual) |
| WhatsApp | Comunicação com cliente, recebimento de docs | Aguardando aprovação Meta |
| n8n | Orquestração de automações | A configurar |
| API ChatGPT Vision | OCR e extração inteligente de dados | A implementar |
| Excel | Output final para operadora | Estrutura criada |
| Dashboard React | Visualização de status | Protótipo criado |

---

## 10. Fluxo de Status do Lead

```
NOVO → AGUARDANDO DOCS → PARCIAL → COMPLETO → ENVIADO À OPERADORA
                ↑                       │
                └── PENDÊNCIAS ←────────┘
```

- **NOVO:** Lead captado no Monday, primeiro contato via WhatsApp
- **AGUARDANDO DOCS:** Mensagem enviada, aguardando envio de documentos (janela 24h)
- **PARCIAL:** Alguns documentos recebidos, dados parcialmente extraídos
- **COMPLETO:** Todos os documentos e dados validados
- **ENVIADO À OPERADORA:** Planilha preenchida e submetida

---

## 11. Dashboard - Requisitos

O dashboard deve apresentar:

- KPIs gerais: total de leads, PF vs PJ, total de dependentes
- Status de cada lead (completo, parcial, incompleto)
- Checklist de documentos por beneficiário e dependente
- Barra de progresso por lead
- Detalhes expandíveis por beneficiário
- Resumo de pendências com próximas ações

---

## 12. Tecnologias

| Componente | Tecnologia |
|------------|-----------|
| Orquestração | n8n |
| Agente WhatsApp | Evolution API + n8n + API ChatGPT |
| OCR/Extração | API ChatGPT Vision (híbrido com n8n) |
| Armazenamento | Sistema de arquivos local (pastas estruturadas) |
| Planilha | Python (openpyxl) / HTML-Excel |
| Dashboard | React (JSX) com Tailwind CSS |
| Scripts auxiliares | Python |

---

## 13. Agente de Atendimento (WhatsApp)

### 13.1 Visão Geral

Agente de IA que atende leads via WhatsApp de forma autônoma. Responsável por todo o ciclo de comunicação com o cliente: primeiro contato, coleta de documentos, esclarecimento de dúvidas sobre planos, negociação e acompanhamento de pendências.

### 13.2 Tom e Personalidade

- **Tom:** Formal e direto
- Objetivo: resolver o cadastro com o mínimo de mensagens possível
- Sem enrolação, sem emojis excessivos, sem informalidade
- Educado mas assertivo — conduz a conversa, não espera o cliente adivinhar o próximo passo
- Sempre informa o que falta e o que o cliente precisa fazer

### 13.3 Capacidades do Agente

| Capacidade | Descrição |
|------------|-----------|
| Primeiro contato | Apresenta-se, explica o processo, solicita documentos obrigatórios |
| Coleta de documentos | Recebe e confirma recebimento de cada documento |
| Dúvidas sobre planos | Responde sobre cobertura, carência, valores, rede credenciada |
| Negociação | Pode apresentar opções de planos, comparar benefícios |
| Acompanhamento | Cobra documentos pendentes, informa status do cadastro |
| Validação | Identifica se documento enviado está legível e correto |
| Encerramento | Confirma que tudo foi recebido, informa próximos passos |

### 13.4 Fluxo de Atendimento

```
1. Lead entra no Monday (contrato aprovado)
       │
       ▼
2. Agente envia mensagem inicial via WhatsApp
   "Olá [Nome], sou o assistente da [Empresa].
    Seu plano foi aprovado. Para dar continuidade ao cadastro,
    preciso dos seguintes documentos: [lista]"
       │
       ▼
3. Aguarda resposta (janela de 24h)
       │
       ├── Cliente responde → Agente conduz coleta
       │
       ├── Cliente tem dúvida → Agente esclarece
       │
       └── Sem resposta → Sinaliza no sistema (follow-up manual)
       │
       ▼
4. Para cada documento recebido:
   - Confirma recebimento
   - Valida se está legível
   - Atualiza checklist
   - Informa o que ainda falta
       │
       ▼
5. Todos os docs recebidos → Encerra atendimento
   "Todos os documentos foram recebidos. Seu cadastro será
    processado e entraremos em contato com a confirmação."
```

### 13.5 Regras do Agente

- Nunca solicita dados que já possui (verificar dados_monday.txt antes)
- Adapta a lista de documentos ao tipo de cadastro (PF/PJ) e vínculo dos dependentes
- Se o cliente enviar documento ilegível, solicita reenvio educadamente
- Se o cliente perguntar algo fora do escopo (ex: sinistro, reembolso), informa que será direcionado ao setor responsável
- Respeita a janela de 24h do WhatsApp — após esse período, não envia novas mensagens sem template aprovado
- Registra todas as informações obtidas na conversa no arquivo dados_wattzap.txt
- Identifica automaticamente o tipo de documento recebido (CNH, RG, comprovante, CTPS, etc.)

### 13.6 Mensagens Padrão

**Primeiro contato (PJ):**
```
Olá, [Nome]. Aqui é o assistente de cadastro da [Empresa].

Seu plano empresarial foi aprovado. Para finalizar o cadastro, preciso dos seguintes documentos:

Da empresa:
• Contrato social
• CNPJ

Do beneficiário responsável ([Nome]):
• Documento com foto (RG, CNH ou Passaporte)
• CPF
• Comprovante de residência

Você possui [X] dependente(s). Para cada um, precisarei de:
• Documento com foto
• CPF
• Comprovante de residência

Pode enviar os documentos por aqui mesmo. Alguma dúvida?
```

**Confirmação de recebimento:**
```
Recebi o [tipo do documento] do(a) [nome]. ✓

Ainda faltam:
• [lista de pendências]
```

**Cobrança de pendência:**
```
[Nome], para dar continuidade ao seu cadastro, ainda preciso de:
• [lista de pendências]

Consegue enviar hoje?
```

**Encerramento:**
```
Todos os documentos foram recebidos com sucesso.

Seu cadastro será processado e você receberá a confirmação em até [X] dias úteis.

Qualquer dúvida, estou à disposição.
```

### 13.7 Base de Conhecimento do Agente

O agente deve ter acesso a:

- Tabela de planos disponíveis (cobertura, valores, carência)
- Rede credenciada por região
- Regras de elegibilidade por tipo de vínculo
- FAQ de perguntas frequentes sobre planos de saúde
- Regras da ANS sobre carência e portabilidade

### 13.8 Integrações do Agente

| Sistema | Função |
|---------|--------|
| Evolution API | Envio e recebimento de mensagens WhatsApp |
| Monday.com | Leitura de dados do lead, atualização de status |
| Sistema de arquivos | Salvar documentos recebidos na pasta do lead |
| n8n | Orquestração completa do fluxo de atendimento |

### 13.9 Fluxo n8n + Evolution API

O n8n será responsável por orquestrar o agente de atendimento usando a Evolution API para enviar e receber mensagens. O fluxo é simples e direto:

```
┌─────────────────────────────────────────────────────────┐
│                    FLUXO n8n                             │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  1. TRIGGER: Webhook (Evolution API)                    │
│     - Recebe mensagem do cliente via webhook            │
│     - Payload: número, mensagem, mídia (se houver)      │
│                                                         │
│  2. IDENTIFICAR LEAD                                    │
│     - Busca pelo número no sistema de pastas            │
│     - Se não existe → cria pasta nova                   │
│     - Carrega dados_consolidados.txt do lead            │
│                                                         │
│  3. PROCESSAR MÍDIA (se houver)                         │
│     - Baixa documento/imagem recebido                   │
│     - Salva na pasta Documentos Obrigatorios/           │
│     - Dispara OCR via API ChatGPT Vision                │
│     - Atualiza dados_wattzap.txt                        │
│                                                         │
│  4. CHAMAR IA (System Prompt do Agente)                 │
│     - Envia contexto: dados do lead + mensagem          │
│     - System prompt define tom, regras, capacidades     │
│     - IA gera resposta adequada                         │
│                                                         │
│  5. ENVIAR RESPOSTA (Evolution API)                     │
│     - POST para Evolution API com a resposta            │
│     - Endpoint: /message/sendText/{instance}            │
│                                                         │
│  6. ATUALIZAR DADOS                                     │
│     - Atualiza dados_wattzap.txt com info da conversa   │
│     - Atualiza dados_consolidados.txt                   │
│     - Atualiza status no Monday (se aplicável)          │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

**Configuração Evolution API no n8n:**

```
Base URL: http://localhost:8080
Endpoints utilizados:
  - POST /message/sendText/{instance}     → Enviar mensagem de texto
  - POST /message/sendMedia/{instance}    → Enviar mídia/documento
  - Webhook de entrada                    → Receber mensagens do cliente

Headers:
  - apikey: [CHAVE_EVOLUTION_API]
  - Content-Type: application/json

Payload envio:
{
  "number": "5521971059196",
  "text": "[resposta gerada pela IA]"
}

Payload recebimento (webhook):
{
  "event": "messages.upsert",
  "instance": "[INSTANCIA]",
  "data": {
    "key": { "remoteJid": "5521971059196@s.whatsapp.net" },
    "message": { "conversation": "[texto do cliente]" },
    "messageType": "conversation" | "imageMessage" | "documentMessage"
  }
}
```

**Nós do fluxo n8n:**

1. **Webhook Node** — Recebe POST da Evolution API quando chega mensagem
2. **IF Node** — Verifica se é texto ou mídia
3. **HTTP Request Node** — Baixa mídia (se houver) via Evolution API
4. **Code Node** — Identifica lead, carrega contexto, monta prompt
5. **HTTP Request Node** — Chama API ChatGPT com system prompt + contexto + mensagem
6. **HTTP Request Node** — Envia resposta via Evolution API (sendText)
7. **Code Node** — Atualiza arquivos .txt na pasta do lead

### 13.10 System Prompt do Agente

O system prompt é o coração do agente. Ele define como a IA se comporta em cada interação:

```
Você é um assistente de cadastro de planos de saúde PME/PJ.

REGRAS:
- Tom: formal e direto. Sem emojis excessivos, sem informalidade.
- Objetivo: coletar todos os documentos obrigatórios e esclarecer dúvidas.
- Sempre informe o que falta e o próximo passo.
- Nunca solicite dados que já possui (verifique o contexto fornecido).
- Adapte a lista de documentos ao tipo de cadastro (PF/PJ) e vínculo.

CAPACIDADES:
- Responder dúvidas sobre planos, cobertura, carência, valores, rede credenciada.
- Negociar e apresentar opções de planos.
- Confirmar recebimento de documentos.
- Cobrar pendências de forma educada mas assertiva.
- Identificar tipo de documento recebido.

CONTEXTO DO LEAD:
{dados_consolidados}

DOCUMENTOS JÁ RECEBIDOS:
{lista_documentos_recebidos}

DOCUMENTOS PENDENTES:
{lista_documentos_pendentes}

HISTÓRICO DA CONVERSA:
{ultimas_mensagens}

REGRAS DE ESCALAÇÃO:
- Se o cliente pedir cancelamento → "Vou direcionar para nosso setor de atendimento."
- Se o cliente demonstrar insatisfação → "Entendo sua preocupação. Vou encaminhar para um atendente."
- Se a dúvida estiver fora do seu conhecimento → "Vou verificar com a equipe e retorno."
- Se o cliente pedir para falar com humano → "Claro, vou transferir agora."

Responda APENAS a mensagem atual do cliente. Seja breve e objetivo.
```

### 13.11 Trigger de Primeiro Contato

Além de responder mensagens, o n8n também dispara o primeiro contato quando um novo lead é aprovado no Monday:

```
┌─────────────────────────────────────────┐
│  TRIGGER: Monday Webhook (status mudou) │
│  Condição: status = "Aprovado"          │
├─────────────────────────────────────────┤
│  1. Buscar dados do lead no Monday      │
│  2. Criar pasta do lead                 │
│  3. Criar dados_monday.txt              │
│  4. Montar mensagem inicial             │
│     (baseada no tipo PF/PJ + deps)      │
│  5. Enviar via Evolution API            │
│  6. Criar dados_wattzap.txt             │
└─────────────────────────────────────────┘
```

### 13.12 Métricas do Agente

- Tempo médio de coleta completa (primeiro contato → todos docs recebidos)
- Taxa de resolução sem intervenção humana
- Número de mensagens por atendimento
- Taxa de documentos ilegíveis/rejeitados
- Taxa de leads que não respondem dentro da janela de 24h

### 13.13 Limitações e Escalação

O agente deve escalar para atendimento humano quando:

- Cliente solicita cancelamento
- Cliente reclama ou demonstra insatisfação
- Dúvida técnica fora da base de conhecimento
- 3 tentativas de contato sem resposta
- Documento enviado 3x e continua ilegível
- Cliente solicita falar com um humano

---

## 14. Limitações Atuais

- API oficial do WhatsApp (Meta) ainda não aprovada → fluxo manual de envio
- Ambiente de execução Linux indisponível intermitentemente
- OCR de PDFs com imagem (CNH-e) requer API Vision (não funciona com extração de texto simples)
- Janela de atendimento WhatsApp limitada a 24h
- Base de conhecimento do agente (planos, valores, rede) precisa ser alimentada

---

## 15. Roadmap

### Fase 1 - Atual (MVP Manual)
- [x] Estrutura de pastas definida
- [x] Template de dados (dados.txt) criado
- [x] Separação de fontes (Monday, WhatsApp, Consolidado)
- [x] Planilha Excel com todos os campos
- [x] Dashboard React protótipo
- [ ] OCR via API ChatGPT Vision
- [ ] Script de preenchimento automático da planilha

### Fase 2 - Automação Parcial
- [ ] n8n monitorando pasta e disparando OCR
- [ ] Preenchimento automático da planilha a partir dos dados consolidados
- [ ] Notificação de pendências via WhatsApp (manual)
- [ ] Busca automática de CNS pelo CPF
- [ ] Construção da base de conhecimento do agente (planos, valores, rede)
- [ ] Protótipo do agente de atendimento com fluxo de mensagens padrão

### Fase 3 - Automação Completa
- [ ] Aprovação Meta → API oficial WhatsApp
- [ ] Agente de atendimento ativo via WhatsApp Business API
- [ ] Envio automático de mensagens para novos leads
- [ ] Recebimento automático de documentos via WhatsApp → pasta
- [ ] Identificação automática de tipo de documento recebido
- [ ] Pipeline completo: Monday → Agente WhatsApp → OCR → Planilha → Operadora
- [ ] Dashboard em tempo real com atualização automática
- [ ] Métricas do agente (tempo de coleta, taxa de resolução, etc.)

---

## 15. Estrutura Atual do Projeto

```
Dados do Wattzap/
├── PRD.md                          # Este documento
├── dashboard.jsx                   # Dashboard React
├── gerar_planilha.py              # Script gerador do Excel
├── planilha_leads.xls             # Planilha modelo
├── Gilson +55 16 99142-0538/      # Lead PF (estrutura antiga)
│   ├── dados.txt
│   └── PF/
│       ├── CNH-e.pdf
│       └── ComprovanteResidencia.jpeg
└── Thierry Azevedo +55 21 971059196/  # Lead PJ (estrutura nova)
    ├── dados.txt
    ├── dados_monday.txt
    ├── dados_wattzap.txt
    ├── dados_consolidados.txt
    └── Documentos Obrigatorios/
        └── Gilson/
            ├── CNH-e.pdf
            ├── ComprovanteResidencia.jpeg
            └── CTPSDigital_34890986847_10-09-2024 (1).pdf
```
