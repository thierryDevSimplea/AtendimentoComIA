# Testes e Correções

Registro dos testes do fluxo e correções necessárias. Documento vivo.

---

## Teste #1 — Thierry (PF) — 2026-05-21

**Como foi:** disparo iniciou a conversa, agente conduziu o fluxo PF corretamente até a coleta completa (nome, titular, plano anterior "Leve Saúde 2021", CPF, nascimento, e-mail, sem dependentes, CNS) e pediu os documentos. ✅

**Problema:** ao pedir os documentos, o cliente respondeu *"Só um instante q vou buscar"* e em seguida *"Preciso detalhar ou vc conseguiram identificar certinho?"*. O agente respondeu bem à primeira, mas **regrediu** em paralelo — voltou a "Confirmando: seu nome é... titular, correto?" (2ª execução paralela). Quando o cliente respondeu *"Sim já informei"*, a 3ª execução regrediu mais ainda: voltou ao início do fluxo perguntando *"Você já teve um plano de saúde anteriormente?"* — e a **pergunta apareceu duplicada** na mesma mensagem (*"Você já teve um plano de saúde anteriormente? Você já teve um plano de saúde?"*), indicando que o modelo repetiu a frase no mesmo turno por perda de contexto.

### Causa raiz (analisada no histórico real, 29 msgs)

1. **Execuções paralelas por mensagens rápidas** *(causa principal)* — as 2 mensagens do cliente quase simultâneas dispararam 2 execuções do webhook ao mesmo tempo. Uma respondeu certo; a outra (6s depois) regrediu para a confirmação de titular.
2. **Histórico curto (limit: 10)** — o nó `buscar-historico` pega só as 10 últimas mensagens. Como o agente envia várias mensagens por turno (múltiplos "Dados coletados"/"Confirmando"), as 10 últimas ficam poluídas pelas respostas dele e o estado real do fluxo se perde.
3. **Agente tagarela** — manda mensagens demais por turno, o que agrava o item 2.
4. **Modelo (Llama 3.3 70B via Groq)** — menos robusto pra manter estado de fluxo só pelo histórico; uma pergunta fora do script ("preciso detalhar?") o deixou inseguro.

### Correções aplicadas (2026-05-21)

- [x] **Debounce** — novo nó `Debounce` entre `Filtrar e Parsear` e `Buscar Historico`: espera 7s e, se chegou mensagem mais nova do cliente, aborta a execução (mata a race de execuções paralelas). *(correção principal)*
- [x] **Histórico 10 → 50** no `buscar-historico`.
- [x] **Uma mensagem por turno** — regra adicionada no prompt.
- [x] **Anti-regressão** — regra no prompt: "NUNCA repita pergunta cujo dado já está no histórico/Dados coletados; continue de onde parou". + "se o cliente perguntar algo fora do roteiro, responda e siga sem reiniciar".
- [ ] Reavaliar com OpenAI (produção) — modelo mais robusto deve reduzir regressões.

Cadeia nova do workflow: `Receber → Filtrar → Debounce → Buscar Histórico → IA → Enviar`.

**Status:** corrigido — **reteste pendente**.
