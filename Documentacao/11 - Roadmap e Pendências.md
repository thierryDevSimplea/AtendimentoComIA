# Roadmap e Pendências

Estado do projeto e o que falta pra finalizar. Atualizado: **2026-05-21**.

## ✅ Pronto

- Ambiente nativo (Postgres 16 + Evolution API via `npm start`) — ver [[01 - Arquitetura]]
- IA migrada pro Groq (gratuito), proxy funcionando — [[03 - Agente IA (Groq)]]
- WhatsApp conectado (instância `wattzap`, número 5521994746793)
- Workflow do agente (v4) e do disparo (Kaizen) publicados e ativos no n8n
- Tunnels Cloudflare ligados (Evolution + proxy)
- Fluxo PF/PJ revisado e documentado — [[08 - Fluxo do Agente (PF e PJ)]]
- Planilha + arquivo de lead estruturados — [[09 - Planilha de Leads]]

## ⏳ Pendente (ordem sugerida)

1. **Teste end-to-end** — disparar 1ª mensagem (Thierry PF ou Gabriel PJ), responder e validar a conversa completa até o fechamento.
2. **Gravar dados do lead** — ao fim da conversa, escrever o `dados_consolidados.txt` e/ou linha na `planilha_leads.xlsx` (hoje a planilha não é preenchida automaticamente pelo fluxo).
3. **Integrar CNS** — chamar o `consulta-cns.js` (porta 3457) pelo CPF e gravar o CNS. Já existe, falta plugar no fluxo.
4. **OCR de documentos** — ler os documentos enviados (doc com foto, comprovante de residência, cartão CNPJ/contrato, holerite) com IA Vision e:
   - preencher endereço (CEP, rua, número, bairro, cidade, estado)
   - preencher endereço da empresa (PJ)
   - validar/marcar status dos documentos (PENDENTE/RECEBIDO/APROVADO)
   - extrair Cargo (do holerite/carteira)
5. **Integração Monday** — webhook do Monday (status "Aprovado") cria o lead em `leads.json`/fila e dispara o 1º contato; preenche o bloco `monday` por lead. Ver [[07 - Pipeline de Leads (Monday)]].
6. **Migrar IA pra OpenAI** (produção) — trocar URL+chave no `proxy-ai.js`. Ver [[03 - Agente IA (Groq)]].
7. **Publicar no GitHub** — versionar o projeto (usar PAT, não senha).

## ⚠️ Riscos / atenções

- **Tunnels efêmeros**: as URLs `trycloudflare.com` mudam a cada reinício. Ao reiniciar, regenerar e atualizar nos dois workflows (`update_workflow.py` e `update_disparo.py`).
- **Chave Groq exposta no chat** — revogar e gerar nova antes de produção.
- **leadsDB hardcoded** — o número de teste real (5521994746793) não está na lista; é o número da Kaizen (envia/recebe), não um lead.
- **Segredos**: não commitar `.env`, chaves do Groq, JWT do n8n no GitHub.
