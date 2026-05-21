import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.formatting.rule import CellIsRule
from openpyxl.worksheet.datavalidation import DataValidation

wb = openpyxl.Workbook()

thin_border = Border(left=Side('thin'), right=Side('thin'), top=Side('thin'), bottom=Side('thin'))
center = Alignment(horizontal='center', vertical='center')
left_align = Alignment(horizontal='left', vertical='center')
wrap_center = Alignment(horizontal='center', vertical='center', wrap_text=True)

DARK_BLUE = "1F3864"
BLUE = "2F5496"
LIGHT_BLUE = "D6E4F0"
GREEN = "375623"
LIGHT_GREEN = "E2EFDA"
PURPLE = "7030A0"
GOLD = "806000"
MONDAY = "C55A11"
LIGHT_GRAY = "F2F2F2"
GRAY = "404040"

# Campos vindos do Monday (nivel do plano/lead). (Fixo/Dinamico)
MONDAY_HEADERS = ['Operadora', 'Saude/Odonto', 'Tipo Plano', 'Produto',
                  'Boleto Adesao', 'Vigencia', 'Mensalidade', 'Valor Mensal.', 'Mens. Seguidas']
MONDAY_DEFAULTS = {
    'Operadora': 'Santa Casa',
    'Saude/Odonto': 'Saude + Odonto',
    'Tipo Plano': 'PME',
    'Produto': 'Confianca 200E - Sdt com Cpart',
    'Boleto Adesao': '',
    'Vigencia': '',
    'Mensalidade': '',
    'Valor Mensal.': 'Sem valor',
    'Mens. Seguidas': 250,
}
DATE_HEADERS = {'Boleto Adesao', 'Vigencia', 'Mensalidade'}

WIDTHS = {
    'Nome Completo': 28, 'Razao Social': 28, 'Endereco': 28, 'Endereco Emp.': 28,
    'Email': 24, 'Produto': 30, 'CNS': 18, 'CPF': 16, 'CNPJ': 20, 'Telefone': 16,
    'Status': 14, 'Tipo': 14, 'Vinculo': 14, 'Cargo': 16, 'Cidade': 16, 'Cidade Emp.': 16,
    'Bairro': 18, 'Bairro Emp.': 18, 'Operadora': 16, 'Saude/Odonto': 16, 'Tipo Plano': 12,
    'Nome Plano': 16, 'Cart./Holerite': 14,
}

# ============================================
# ABA 1: DASHBOARD
# ============================================
ws = wb.active
ws.title = "Dashboard"
ws.sheet_properties.tabColor = "2F5496"

ws.merge_cells('A1:H1')
title_cell = ws.cell(row=1, column=1, value="KAIZEN CONSULTORIA - PAINEL DE LEADS")
title_cell.font = Font(bold=True, size=14, color="FFFFFF")
title_cell.fill = PatternFill(start_color=DARK_BLUE, end_color=DARK_BLUE, fill_type="solid")
title_cell.alignment = Alignment(horizontal='center', vertical='center')
ws.row_dimensions[1].height = 30

dash_headers = ['#', 'Nome do Lead', 'Telefone', 'Tipo', 'N Benef.', 'Status', 'Ultima Interacao', 'Ir para Detalhes']
h_font = Font(bold=True, size=10, color="FFFFFF")
h_fill = PatternFill(start_color=BLUE, end_color=BLUE, fill_type="solid")

for col, h in enumerate(dash_headers, 1):
    cell = ws.cell(row=2, column=col, value=h)
    cell.font = h_font
    cell.fill = h_fill
    cell.alignment = wrap_center
    cell.border = thin_border

widths = [5, 28, 18, 8, 10, 16, 18, 18]
for i, w in enumerate(widths, 1):
    ws.column_dimensions[get_column_letter(i)].width = w
ws.row_dimensions[2].height = 22

status_dv = DataValidation(type="list", formula1='"NOVO,EM CONVERSA,PENDENTE,FINALIZADO"', allow_blank=True)
ws.add_data_validation(status_dv)

leads = [
    {'id': 1, 'nome': 'Gilson Ferreira', 'tel': '5516991420538', 'tipo': 'PF', 'benef': 2, 'status': 'NOVO'},
    {'id': 2, 'nome': 'Gabriel Henrique', 'tel': '5518998171940', 'tipo': 'PJ', 'benef': 3, 'status': 'NOVO'}
]

for row, lead in enumerate(leads, 3):
    row_fill = PatternFill(start_color=LIGHT_BLUE if row % 2 == 1 else "FFFFFF", end_color=LIGHT_BLUE if row % 2 == 1 else "FFFFFF", fill_type="solid")
    for col in range(1, 9):
        ws.cell(row=row, column=col).fill = row_fill
        ws.cell(row=row, column=col).border = thin_border
        ws.cell(row=row, column=col).alignment = center

    ws.cell(row=row, column=1, value=lead['id'])
    ws.cell(row=row, column=2, value=lead['nome']).alignment = left_align
    ws.cell(row=row, column=3, value=lead['tel'])
    ws.cell(row=row, column=4, value=lead['tipo'])
    ws.cell(row=row, column=5, value=lead['benef'])
    status_cell = ws.cell(row=row, column=6, value=lead['status'])
    status_dv.add(status_cell)
    ws.cell(row=row, column=7, value='-')
    aba = 'Leads PF' if lead['tipo'] == 'PF' else 'Leads PJ'
    link_cell = ws.cell(row=row, column=8, value=">> " + aba)
    link_cell.font = Font(color="0563C1", underline="single", bold=True)
    link_cell.hyperlink = "#'" + aba + "'!A1"

ws.conditional_formatting.add('F3:F100', CellIsRule(operator='equal', formula=['"NOVO"'], fill=PatternFill(start_color="FFC000", end_color="FFC000", fill_type="solid")))
ws.conditional_formatting.add('F3:F100', CellIsRule(operator='equal', formula=['"EM CONVERSA"'], fill=PatternFill(start_color="5B9BD5", end_color="5B9BD5", fill_type="solid"), font=Font(color="FFFFFF", bold=True)))
ws.conditional_formatting.add('F3:F100', CellIsRule(operator='equal', formula=['"PENDENTE"'], fill=PatternFill(start_color="FF6600", end_color="FF6600", fill_type="solid"), font=Font(color="FFFFFF", bold=True)))
ws.conditional_formatting.add('F3:F100', CellIsRule(operator='equal', formula=['"FINALIZADO"'], fill=PatternFill(start_color="70AD47", end_color="70AD47", fill_type="solid"), font=Font(color="FFFFFF", bold=True)))

ws.freeze_panes = 'A3'


def build_lead_sheet(title, tab_color, title_color, groups, sample_titular, sample_deps, freeze_col):
    """groups = list of (group_name, color, [headers...])"""
    sh = wb.create_sheet(title)
    sh.sheet_properties.tabColor = tab_color

    # headers achatados
    headers = []
    for _, _, hs in groups:
        headers.extend(hs)
    ncols = len(headers)

    # Titulo
    sh.merge_cells(start_row=1, start_column=1, end_row=1, end_column=ncols)
    t = sh.cell(row=1, column=1, value=title.upper())
    t.font = Font(bold=True, size=13, color="FFFFFF")
    t.fill = PatternFill(start_color=title_color, end_color=title_color, fill_type="solid")
    t.alignment = Alignment(horizontal='center', vertical='center')
    sh.row_dimensions[1].height = 28

    # Linha 2: grupos
    col_start = 1
    for gname, gcolor, hs in groups:
        span = len(hs)
        sh.merge_cells(start_row=2, start_column=col_start, end_row=2, end_column=col_start + span - 1)
        c = sh.cell(row=2, column=col_start, value=gname)
        c.font = Font(bold=True, size=10, color="FFFFFF")
        c.fill = PatternFill(start_color=gcolor, end_color=gcolor, fill_type="solid")
        c.alignment = Alignment(horizontal='center', vertical='center')
        c.border = thin_border
        col_start += span
    sh.row_dimensions[2].height = 20

    # Linha 3: headers
    for col, h in enumerate(headers, 1):
        c = sh.cell(row=3, column=col, value=h)
        c.font = Font(bold=True, size=9, color=GRAY)
        c.fill = PatternFill(start_color=LIGHT_GRAY, end_color=LIGHT_GRAY, fill_type="solid")
        c.alignment = wrap_center
        c.border = thin_border
        sh.column_dimensions[get_column_letter(col)].width = WIDTHS.get(h, 14)
    sh.row_dimensions[3].height = 22

    # indices uteis
    idx = {h: i + 1 for i, h in enumerate(headers)}
    light = LIGHT_GREEN if title.endswith('PJ') else LIGHT_BLUE

    # linhas de dados (titular + dependentes)
    rows_data = [sample_titular] + sample_deps
    for r_off, rowvals in enumerate(rows_data):
        row_idx = 4 + r_off
        alt = PatternFill(start_color=light if row_idx % 2 == 0 else "FFFFFF", end_color=light if row_idx % 2 == 0 else "FFFFFF", fill_type="solid")
        for col_idx in range(1, ncols + 1):
            c = sh.cell(row=row_idx, column=col_idx)
            c.border = thin_border
            c.fill = alt
            c.alignment = center if col_idx <= idx.get('Tipo', 4) else left_align
        for h, v in rowvals.items():
            if h in idx and v != '':
                sh.cell(row=row_idx, column=idx[h], value=v)

    # formato de data
    for h in DATE_HEADERS:
        if h in idx:
            for r in range(4, 50):
                sh.cell(row=r, column=idx[h]).number_format = 'DD/MM/YYYY'

    # formula idade
    if 'Idade' in idx and 'Data Nasc.' in idx:
        dn = get_column_letter(idx['Data Nasc.'])
        for r in range(4, 50):
            sh.cell(row=r, column=idx['Idade'], value='=IF({c}{r}="","",DATEDIF({c}{r},TODAY(),"Y"))'.format(c=dn, r=r))

    # validacao status dos documentos
    doc_cols = [idx[h] for h in ('Doc c/ Foto', 'CPF (doc)', 'Comp. Resid.', 'Cart./Holerite') if h in idx]
    if doc_cols:
        ddv = DataValidation(type="list", formula1='"PENDENTE,RECEBIDO,APROVADO"', allow_blank=True)
        sh.add_data_validation(ddv)
        for r in range(4, 50):
            for col in doc_cols:
                ddv.add(sh.cell(row=r, column=col))

    # link voltar (coluna livre apos os dados)
    back = sh.cell(row=3, column=ncols + 1, value="<< Voltar")
    back.font = Font(color="0563C1", underline="single", bold=True)
    back.hyperlink = "#'Dashboard'!A1"

    sh.freeze_panes = get_column_letter(freeze_col) + '4'
    return sh


# ============================================
# ABA 2: LEADS PF
# ============================================
groups_pf = [
    ('IDENTIFICACAO', BLUE, ['ID Lead', 'Telefone', 'Status', 'Tipo']),
    ('PLANO (MONDAY)', MONDAY, list(MONDAY_HEADERS)),
    ('DADOS PESSOAIS', "2E75B6", ['Nome Completo', 'CPF', 'Data Nasc.', 'Idade', 'CNS', 'Email']),
    ('ENDERECO', PURPLE, ['CEP', 'Endereco', 'Numero', 'Bairro', 'Cidade', 'Estado']),
    ('PLANO ANTERIOR', GOLD, ['Plano Ant. (S/N)', 'Nome Plano', 'Ano Plano']),
    ('DOCUMENTOS', GREEN, ['Doc c/ Foto', 'CPF (doc)', 'Comp. Resid.']),
]
pf_titular = {'ID Lead': 1, 'Telefone': '5516991420538', 'Status': 'NOVO', 'Tipo': 'TITULAR', 'Nome Completo': 'Gilson Ferreira'}
pf_titular.update(MONDAY_DEFAULTS)
pf_deps = [{'ID Lead': 1, 'Telefone': '5516991420538', 'Tipo': 'DEPENDENTE 1'}]
build_lead_sheet('Leads PF', "4472C4", "4472C4", groups_pf, pf_titular, pf_deps, freeze_col=14)

# ============================================
# ABA 3: LEADS PJ
# ============================================
groups_pj = [
    ('IDENTIFICACAO', BLUE, ['ID Lead', 'Telefone', 'Status']),
    ('PLANO (MONDAY)', MONDAY, list(MONDAY_HEADERS)),
    ('DADOS DA EMPRESA', GREEN, ['Razao Social', 'CNPJ', 'CEP Emp.', 'Endereco Emp.', 'N Emp.', 'Bairro Emp.', 'Cidade Emp.', 'Estado Emp.']),
    ('BENEFICIARIO', "2E75B6", ['Tipo', 'Nome Completo', 'CPF', 'Data Nasc.', 'Idade', 'CNS', 'Email', 'Vinculo', 'Cargo']),
    ('ENDERECO BENEF.', PURPLE, ['CEP', 'Endereco', 'Numero', 'Bairro', 'Cidade', 'Estado']),
    ('PLANO ANTERIOR', GOLD, ['Plano Ant. (S/N)', 'Nome Plano', 'Ano Plano']),
    ('DOCUMENTOS', "BF8F00", ['Doc c/ Foto', 'Comp. Resid.', 'Cart./Holerite']),
]
pj_titular = {'ID Lead': 2, 'Telefone': '5518998171940', 'Status': 'NOVO', 'Tipo': 'TITULAR', 'Nome Completo': 'Gabriel Henrique'}
pj_titular.update(MONDAY_DEFAULTS)
pj_deps = [
    {'ID Lead': 2, 'Telefone': '5518998171940', 'Tipo': 'DEP 1'},
    {'ID Lead': 2, 'Telefone': '5518998171940', 'Tipo': 'DEP 2'},
]
build_lead_sheet('Leads PJ', "548235", "548235", groups_pj, pj_titular, pj_deps, freeze_col=13)

wb.save('C:/Atendimento2/planilha_leads.xlsx')
print('Planilha regenerada com grupo PLANO (MONDAY)')
