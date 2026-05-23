# Planilha de Leads

Arquivo: `planilha_leads.xlsx` (raiz do projeto). Gerada por `criar_planilha.py`. No fim de cada interação, os dados do lead são consolidados nela. Abas: **Dashboard**, **Leads PF**, **Leads PJ**.

> [!note] Documento vivo — atualizar quando colunas mudarem. Última atualização: **2026-05-21**.

## Origem de cada campo

| Grupo | Campos | Origem |
|-------|--------|--------|
| Identificação | ID Lead, Telefone, Status, Tipo | Sistema / lista |
| **Plano (Monday)** | Operadora, Saúde/Odonto, Tipo Plano, Produto, Boleto Adesão, Vigência, Mensalidade, Valor Mensal., Mens. Seguidas | **Monday** (fixo/dinâmico) |
| Dados pessoais / Beneficiário | Nome Completo, CPF, Data Nasc., Email (e Vínculo no PJ) | **Conversa** (agente) |
| | Idade | Fórmula `DATEDIF` (automática) |
| | CNS | Busca automática por CPF (`consulta-cns.js`) |
| | Cargo (PJ) | Documento (holerite/carteira) — **não obrigatório** |
| Endereço | CEP, Endereço, Número, Bairro, Cidade, Estado | **Documento** (comprovante residência — OCR) |
| Endereço Emp. (PJ) | CEP/Endereço/etc. da empresa | **Documento** (cartão CNPJ / contrato social — OCR) |
| Plano anterior | Plano Ant. (S/N), Nome Plano, Ano Plano | **Conversa** |
| Documentos | Doc c/ Foto, CPF (doc), Comp. Resid. (PF) / Doc c/ Foto, Comp. Resid., Cart./Holerite (PJ) | Status (PENDENTE/RECEBIDO/APROVADO) ao validar docs por IA |

## Valores Monday padrão (exemplo atual)

- Operadora: Santa Casa
- Saúde/Odonto: Saude + Odonto
- Tipo Plano: PME
- Produto: Confianca 200E - Sdt com Cpart
- Valor Mensal.: Sem valor
- Mens. Seguidas: 250
- Datas (Boleto Adesão, Vigência, Mensalidade): preenchidas pelo Monday

## Arquivo de dados do lead (espelho da planilha)

Além da planilha, cada lead tem um **arquivo consolidado** (`dados_consolidados.txt`) com os mesmos campos. Template: `template_dados_lead.txt` (raiz do projeto), com a origem marcada por campo: **[MONDAY] [CONVERSA] [DOC=OCR] [AUTO]**.

- Os campos do Monday (incluindo **Mens. Seguidas**) e todos os demais da planilha estão refletidos nesse template.
- Use uma cópia por lead. É o que alimenta a planilha no fim da interação.

## Observações

- PF **não** tem coluna de carteira de trabalho (dependente PF é vínculo familiar; carteira não é obrigatória).
- PJ tem **Cart./Holerite** para dependente com vínculo empregatício.
- Campos de Endereço e status de Documentos dependem do **OCR (ainda não implementado)**. Ver [Changelog](../projeto/changelog.md).
