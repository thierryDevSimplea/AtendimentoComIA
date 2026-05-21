# Fluxo do Agente (PF e PJ)

> [!note] Documento vivo
> Este é o fluxo **atual** de conversa do agente. Vai mudar com o tempo — manter sempre atualizado aqui a cada ajuste. Última atualização: **2026-05-21**.

Implementado no nó `chamar-ia` do workflow `WattZap - Agente Kaizen v4` (ver [[04 - Workflow n8n]]). Marca: **Kaizen Consultoria**. Tom: formal e direto, **uma pergunta por vez**, resume os dados coletados a cada resposta.

> Quem **inicia** a conversa é sempre o disparo n8n (ver [[07 - Pipeline de Leads (Monday)]]). O agente assume quando o cliente responde.

---

## Fluxo PF (pessoa física)

1. Nome completo (já pedido na 1ª mensagem do disparo)
2. **Confirma** se o nome é o do titular/responsável (se não → pede nome completo do titular → confirma)
3. Plano anterior? (se sim: nome do plano + ano)
4. CPF **do beneficiário**
5. Data de nascimento **do beneficiário**
6. E-mail
7. Se 0 dependentes → **confirma com o cliente** ("não há dependentes, correto?"). Se houver → coleta de cada um (ver regra de dependentes)
8. Fechamento: resumo + busca CNS + pede documentos

## Fluxo PJ (pessoa jurídica)

1. Nome completo
2. **Confirma** titular/responsável (se não → pede nome do titular → confirma)
3. Plano anterior? (nome + ano)
4. **Razão social (nome da empresa)** — vem antes do CNPJ
5. CNPJ da empresa
6. CPF **do beneficiário**
7. Data de nascimento **do beneficiário**
8. E-mail
9. Para **cada dependente**: nome completo, CPF, data de nascimento, e-mail, **vínculo**
10. Fechamento: resumo + busca CNS + pede documentos

## Regra de dependentes

- Coleta os mesmos dados de cada dependente (nome, CPF, nascimento, vínculo).
- Vínculo **empregatício** (empregado/colaborador/funcionário) → pede **holerite ou carteira de trabalho**.
- Vínculo **familiar** (parente/familiar) → **não** precisa de documento de vínculo.

## Documentos (fechamento)

**PF**
- Titular: doc com foto (RG/CNH/Passaporte) + comprovante de residência
- Dependentes (se houver): doc com foto + comprovante de residência (+ holerite/carteira se empregatício)

**PJ**
- Empresa: **Contrato social OU Cartão CNPJ (um dos dois)** + comprovante de residência da empresa
- Titular: doc com foto + comprovante de residência
- Cada dependente: doc com foto + comprovante de residência (+ holerite/carteira se empregatício; familiar não precisa)

---

## Exemplo — PF (Thierry, 0 dependentes)

> **Agente:** Olá Thierry. Aqui é da Kaizen Consultoria... pode me confirmar seu **nome completo**?
> **Thierry:** Thierry de Matos Azevedo
> **Agente:** O nome Thierry de Matos Azevedo é o do **titular/responsável**?
> **Thierry:** sim
> **Agente:** Você **já possuía plano de saúde**? Se sim, qual e em que ano?
> **Thierry:** não
> **Agente:** Qual o seu **CPF**?
> **Thierry:** 123.456.789-00
> **Agente:** Qual a sua **data de nascimento**?
> **Thierry:** 15/03/1990
> **Agente:** Qual o seu **e-mail**?
> **Thierry:** thierry@email.com
> **Agente:** Confirmando: **não há dependentes**, correto?
> **Thierry:** isso
> **Agente:** *(resumo)* Vou buscar seu **CNS**. Documentos: doc com foto + comprovante de residência.

## Exemplo — PJ (Gabriel, 2 dependentes)

> **Agente:** Olá Gabriel. Aqui é da Kaizen Consultoria (planos empresariais)... seu **nome completo**?
> **Gabriel:** Gabriel Henrique Souza
> **Agente:** É o **titular/responsável**?
> **Gabriel:** sim
> **Agente:** A empresa **já possuía plano**? Qual e ano?
> **Gabriel:** sim, Amil em 2021
> **Agente:** Qual a **razão social**?
> **Gabriel:** Souza Comércio LTDA
> **Agente:** Qual o **CNPJ**?
> **Gabriel:** 12.345.678/0001-90
> **Agente:** **CPF** do beneficiário?
> **Gabriel:** 111.222.333-44
> **Agente:** **Data de nascimento**?
> **Gabriel:** 20/08/1985
> **Agente:** **E-mail**?
> **Gabriel:** gabriel@souza.com
> **Agente:** Dependente 1: nome, CPF, nascimento e **vínculo**?
> **Gabriel:** Maria Souza, 555.666.777-88, 10/05/1990, esposa (familiar)
> **Agente:** Dependente 2: nome, CPF, nascimento e vínculo?
> **Gabriel:** João Lima, 999.888.777-66, 02/02/1995, funcionário
> **Agente:** *(resumo)* Buscarei os **CNS**. Documentos:
> - Empresa: Contrato social OU Cartão CNPJ + comprovante de residência
> - Gabriel: doc foto + comprovante
> - Maria (familiar): doc foto + comprovante
> - João (funcionário): doc foto + comprovante **+ holerite/carteira**
