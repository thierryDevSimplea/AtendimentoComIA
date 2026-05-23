# Changelog

Histórico de mudanças e versões do projeto. Mais recente no topo.

## 2026-05-21

- **Documentação reorganizada:** vault Obsidian reestruturado em subpastas temáticas (`setup/`, `servicos/`, `negocio/`, `projeto/`) com links Markdown padrão. Ver [README](../README.md).
- **Handoff completo:** criados [Estrutura de Arquivos](estrutura-arquivos.md) (mapa de todos os scripts/arquivos), [Roadmap e Pendências](roadmap.md) (pronto vs. pendente) e [Acessos e Credenciais](../setup/credenciais.md) (mapa de acessos). Segredos reais em `ACESSOS_SECRETO.md` (raiz, não-versionado).
- **`.gitignore` criado:** protege `ACESSOS_SECRETO.md`, `.env`, `node_modules`, `*.log` e temporários antes de publicar no GitHub.
- **`leads.json`:** cada lead agora carrega o bloco `monday` (campos do plano, fixos hoje, dinâmicos depois).

- **Fluxo PF/PJ revisado:** após o nome, o agente confirma se é o titular/responsável (se não, pede o nome do titular); CPF e data de nascimento marcados como "do beneficiário"; quando 0 dependentes o agente confirma com o cliente em vez de pular; com dependentes coleta os mesmos dados de cada um.
- **Disparo padronizado:** criado `WattZap - Disparo Leads (Kaizen)` (id `EhCYZjF26O0hZSIi`). Marca unificada **Kaizen Consultoria** (antes o disparo dizia "Simplea"). 1ª mensagem alinhada ao fluxo (saudação + pedir nome completo). Tunnel atualizado. (O disparo antigo estava arquivado no n8n.)
- **WhatsApp conectado:** instância `wattzap` no número `5521994746793` (estado open) via painel `/manager`.
- **Tunnels Cloudflare novos:** Evolution `collectible-question-plc-rats`, Proxy `yale-results-concentration-mapping`. Workflow agente atualizado nos 3 nós (histórico, IA, envio).
- **Contexto pipeline:** documentado que os leads vêm do Monday.com → lista → disparo → agente. Ver [Pipeline de Leads](../negocio/pipeline-leads.md).
- **Regras PJ ajustadas:** empresa pede Contrato social **OU** Cartão CNPJ (um dos dois); razão social vem antes do CNPJ; dependente com vínculo familiar **não** precisa de documento de vínculo.
- **Fluxo do agente documentado:** criado [Fluxo do Agente (PF e PJ)](../negocio/fluxo-agente.md) como documento vivo (fluxo PF/PJ + exemplos de conversa). Atualizar sempre que o fluxo mudar.
- **Planilha reestruturada:** adicionado grupo **PLANO (MONDAY)** (Operadora, Saúde/Odonto, Tipo Plano, Produto, Boleto Adesão, Vigência, Mensalidade, Valor Mensal., Mens. Seguidas). PF sem carteira de trabalho; PJ ganhou Comp. Resid. + Cart./Holerite; corrigido o "<< Voltar" que sobrescrevia colunas; validação PENDENTE/RECEBIDO/APROVADO nos docs do PJ. Origem dos campos documentada em [Planilha de Leads](../negocio/planilha-leads.md).
- **Template do arquivo de lead:** criado `template_dados_lead.txt` (raiz) espelhando todos os campos da planilha (incluindo Monday + Mens. Seguidas), com a origem marcada por campo ([MONDAY]/[CONVERSA]/[DOC]/[AUTO]). É a base do `dados_consolidados.txt` de cada lead.

- **Arquitetura corrigida:** confirmado que o ambiente roda **nativo** (PostgreSQL 16 como serviço Windows + Evolution API via `npm start`), **não Docker**. Docker Desktop quebrou (socket `dockerInference` órfão) e foi abandonado.
- **IA trocada pra Groq:** `aibee.cloud` (chave 401, morta) → **Groq** (`llama-3.3-70b-versatile`, gratuito). `proxy-ai.js` reescrito pro formato OpenAI, chave via env var `GROQ_API_KEY`.
- **Nó de IA do n8n** ajustado pro formato OpenAI (`messages` system+user, lê `choices[0].message.content`).
- **Número WhatsApp** correto identificado: `5521994746793` (antes usava-se `5521971059196` de teste).
- **Documentação:** criado este vault Obsidian (`C:/Atendimento2/Documentacao`).

## 2026-05-20

- Workflow n8n v4: fluxos PJ/PF separados, sempre pergunta plano anterior, coleta vínculo dos dependentes, docs diferenciados (cartão CNPJ + contrato social PJ, comprovante parentesco familiar).

## Pendências abertas

- [ ] Teste end-to-end completo
- [ ] Gravar dados do lead automaticamente
- [ ] Integrar consulta CNS no fluxo
- [ ] OCR de documentos (API Vision)
- [ ] Integração Monday → n8n
- [ ] Migrar IA pra OpenAI (produção)
- [ ] Publicar no GitHub
