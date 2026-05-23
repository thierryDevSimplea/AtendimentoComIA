# Pipeline de Leads (Monday → Disparo → Agente)

## Visão completa

```
Monday.com (captação / CRM)
   │  gera lista de leads: nome, telefone, tipo (PF/PJ), nº dependentes
   ▼
Lista de Leads (hoje hardcoded no n8n; futuro = alimentada pelo Monday)
   │
   ▼
n8n DISPARO  ── SEMPRE inicia a conversa (primeiro contato)
   │  envia 1ª mensagem via Evolution API
   ▼
Cliente responde no WhatsApp
   │
   ▼
Agente v4 (reativo)  ── conduz a coleta de dados + documentos
```

> [!important] Quem inicia a conversa é SEMPRE o n8n (disparo), nunca o cliente. O agente v4 só entra quando o cliente responde.

## Origem dos leads: Monday.com

A captação acontece no **Monday.com** (CRM do cliente). De lá vêm os campos que alimentam a lista:

- Nome do lead
- Telefone
- Tipo de cadastro (PF / PJ)
- Quantidade de dependentes
- (e demais campos do PRD: CNPJ/CPF, plano escolhido, vendedor, etc.)

**Status:** integração Monday → n8n ainda **não implementada**. Hoje a lista está hardcoded (4 leads) em `leads.json`:

| Número | Nome | Tipo | Deps |
|--------|------|------|------|
| 5516991420538 | Gilson Ferreira | PF | 1 |
| 5518998171940 | Gabriel Henrique | PJ | 2 |
| 5516997868188 | Affonso | PF | 0 |
| 5521971059196 | Thierry | PF | 0 |

> O `5521994746793` é o número da **Kaizen** (envia/recebe), não é lead.

### Campos do Monday por lead (hoje fixos, depois dinâmicos)

Cada lead em `leads.json` carrega um bloco `monday` com os campos de plano. **Hoje são fixos** (iguais para todos); depois virão dinâmicos do Monday por lead:

- Operadora: Santa Casa
- Saúde/Odonto: Saude + Odonto
- Tipo Plano: PME
- Produto: Confianca 200E - Sdt com Cpart
- Valor Mensalidade: Sem valor
- Mensalidades Seguidas: 250
- Boleto Adesão / Vigência / Mensalidade: (datas, vazias até virem do Monday)

Esses campos alimentam o grupo PLANO (MONDAY) da planilha e o arquivo do lead. Ver [Planilha de Leads](planilha-leads.md).

> [!todo] Futuro: webhook do Monday (status = "Aprovado") dispara o primeiro contato automaticamente e preenche esses campos por lead. Ver PRD seção 13.11.

## Workflows n8n envolvidos

- **Disparo:** `WattZap - Disparo Leads (Kaizen)` (id `EhCYZjF26O0hZSIi`) — webhook `wattzap-disparo`. Lê a lista, monta a 1ª mensagem por tipo (PF/PJ) e envia. Marca: **Kaizen Consultoria**.
- **Agente:** `WattZap - Agente Kaizen v4` (id `eRxPk9c1ZhjsLi05`) — webhook `wattzap-incoming`. Reativo, conduz a conversa. Ver [Workflow n8n](../servicos/workflow-n8n.md).

## 1ª mensagem do disparo (alinhada ao fluxo)

Saudação + pedir **nome completo** (uma pergunta por vez). Ex. (PF):

> Olá Thierry. Aqui é da Kaizen Consultoria, consultoria em planos de saúde. Para dar andamento à sua cotação, pode me confirmar seu nome completo?

A partir da resposta, o agente v4 assume. Ver fluxo em [Workflow n8n](../servicos/workflow-n8n.md).
