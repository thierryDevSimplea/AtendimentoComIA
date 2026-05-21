import json

wf = json.load(open('C:/Users/Thierry/Downloads/workflow-wattzap-v4.json'))

new_filtro_code = """const input = $input.all()[0].json;
const body = input.body || input;
const event = body.event;
const data = body.data || {};
const key = data.key || {};
const fromMe = key.fromMe || false;
const remoteJid = key.remoteJid || '';
const pushName = data.pushName || 'Cliente';
const messageType = data.messageType || '';
const messageTimestamp = data.messageTimestamp || 0;

if (fromMe) return [];
if (remoteJid.includes('@g.us')) return [];
if (remoteJid.includes('@broadcast')) return [];
if (messageType === 'reactionMessage') return [];
if (messageType === 'protocolMessage') return [];
if (messageType === 'editedMessage') return [];
if (messageType === 'stickerMessage') return [];

const now = Math.floor(Date.now() / 1000);
if (messageTimestamp > 0 && (now - messageTimestamp) > 60) return [];

const leadsDB = {
  '5516991420538': {nome: 'Gilson Ferreira', dependentes: 1, tipo: 'PF'},
  '5518998171940': {nome: 'Gabriel Henrique', dependentes: 2, tipo: 'PJ'},
  '5516997868188': {nome: 'Affonso', dependentes: 0, tipo: 'PF'},
  '5521971059196': {nome: 'Thierry', dependentes: 0, tipo: 'PF'}
};

const number = remoteJid.replace('@s.whatsapp.net', '');
if (!leadsDB[number]) return [];

const leadInfo = leadsDB[number];

let messageText = '';
if (data.message) {
  if (data.message.conversation) {
    messageText = data.message.conversation;
  } else if (data.message.extendedTextMessage && data.message.extendedTextMessage.text) {
    messageText = data.message.extendedTextMessage.text;
  }
}

let hasMedia = false;
let mediaInfo = '';
if (messageType === 'imageMessage') {
  hasMedia = true;
  const caption = (data.message && data.message.imageMessage && data.message.imageMessage.caption) ? data.message.imageMessage.caption : '';
  mediaInfo = 'Imagem recebida' + (caption ? ': ' + caption : '');
} else if (messageType === 'documentMessage') {
  hasMedia = true;
  const doc = (data.message && data.message.documentMessage) ? data.message.documentMessage : {};
  mediaInfo = 'Documento recebido: ' + (doc.fileName || 'arquivo') + ' (' + (doc.mimetype || 'desconhecido') + ')';
} else if (messageType === 'audioMessage') {
  hasMedia = true;
  mediaInfo = 'Audio recebido';
}

if (!messageText && !hasMedia) return [];

return [{json: {
  number: number,
  pushName: pushName,
  messageText: messageText || mediaInfo,
  messageType: messageType,
  remoteJid: remoteJid,
  hasMedia: hasMedia,
  mediaInfo: mediaInfo,
  event: event,
  leadNome: leadInfo.nome,
  leadDependentes: leadInfo.dependentes,
  leadTipo: leadInfo.tipo
}}];"""

new_ia_code = """const NL = String.fromCharCode(10);
const input = $input.all()[0].json;
const number = input.number;
const pushName = input.pushName;
const messageText = input.messageText;
const hasMedia = input.hasMedia;
const mediaInfo = input.mediaInfo;
const history = input.conversationHistory || '';
const leadDependentes = input.leadDependentes || 0;
const leadTipo = input.leadTipo || 'PF';
const leadNome = input.leadNome || pushName;

const depInfoColeta = leadDependentes > 0 ? '- Este lead tem ' + leadDependentes + ' dependente(s). Para CADA dependente colete os MESMOS dados do beneficiario: nome completo, CPF do dependente, data de nascimento do dependente, email, e o vinculo (empregado/colaborador/funcionario/parente/familiar).' : '- Este lead NAO tem dependentes. CONFIRME isso com o cliente antes de seguir (ex: "Confirmando: nao ha dependentes a incluir, correto?"). NAO pule sem confirmar.';

const docsPJ = [
  'DOCUMENTOS OBRIGATORIOS (PJ):',
  'Da empresa:',
  '- Contrato social OU Cartao CNPJ (apenas um dos dois)',
  '- Comprovante de residencia da empresa',
  '',
  'Do titular:',
  '- Documento com foto (RG, CNH ou Passaporte)',
  '- Comprovante de residencia do titular',
  '',
  'De cada dependente (se houver):',
  '- Documento com foto',
  '- Comprovante de residencia',
  '- Se vinculo empregaticio (empregado/colaborador/funcionario): Holerite ou Carteira de trabalho',
  '- Se vinculo familiar (parente/familiar): NAO precisa de documento de vinculo'
].join(NL);

const docsPF = [
  'DOCUMENTOS OBRIGATORIOS (PF):',
  'Do titular:',
  '- Documento com foto (RG, CNH ou Passaporte)',
  '- Comprovante de residencia',
  '',
  'De cada dependente (se houver):',
  '- Documento com foto',
  '- Comprovante de residencia',
  '- Se vinculo empregaticio: Holerite ou Carteira de trabalho',
  '- Se vinculo familiar: NAO precisa de documento de vinculo'
].join(NL);

const docsInfo = leadTipo === 'PJ' ? docsPJ : docsPF;

const fluxoPJ = [
  'FLUXO PJ (UMA pergunta por vez):',
  '1. Nome completo (ja pediu na msg inicial)',
  '2. Confirme se o nome informado e o do TITULAR/responsavel pelo plano. Se SIM, segue. Se NAO, pergunte o nome completo do titular do beneficiario e confirme.',
  '3. Plano anterior? O beneficiario informado ja possuia plano de saude? Se sim: qual nome do plano e em que ano contratou',
  '4. Nome da empresa (razao social)',
  '5. CNPJ da empresa',
  '6. CPF do beneficiario',
  '7. Data de nascimento do beneficiario',
  '8. Email do beneficiario',
  depInfoColeta,
  '9. Apos coletar tudo: liste dados + informe CNS + peca documentos'
].join(NL);

const fluxoPF = [
  'FLUXO PF (UMA pergunta por vez):',
  '1. Nome completo (ja pediu na msg inicial)',
  '2. Confirme se o nome informado e o do TITULAR/responsavel pelo plano. Se SIM, segue. Se NAO, pergunte o nome completo do titular do beneficiario e confirme.',
  '3. Plano anterior? O beneficiario informado ja possuia plano de saude? Se sim: qual o nome do plano e em que ano contratou',
  '4. CPF do beneficiario',
  '5. Data de nascimento do beneficiario',
  '6. Email do beneficiario',
  depInfoColeta,
  '7. Apos coletar tudo: liste dados + informe CNS + peca documentos'
].join(NL);

const fluxoInfo = leadTipo === 'PJ' ? fluxoPJ : fluxoPF;

const promptLines = [
  'Voce e um consultor de planos de saude da Kaizen Consultoria.',
  '',
  'DADOS DO LEAD (ja conhecidos - NAO pergunte nada disso):',
  '- Nome no cadastro: ' + leadNome,
  '- Tipo: ' + leadTipo,
  '- Numero de dependentes: ' + leadDependentes,
  '',
  'TOM E ESTILO:',
  '- Formal e direto. Sem emojis excessivos.',
  '- Educado mas assertivo.',
  '- Maximo 2-3 paragrafos.',
  '- Faca UMA pergunta por vez.',
  '',
  'REGRA - RESUMO A CADA RESPOSTA:',
  '- A cada nova resposta, liste os dados JA coletados de forma organizada.',
  '- Formato:',
  '  Dados coletados:',
  '  - Nome: [nome]',
  '  - Plano anterior: [sim/nao]',
  '  - CPF: [cpf]',
  '  - (etc)',
  '- Depois faca a proxima pergunta.',
  '- Se ainda nao coletou nada, pule o resumo.',
  '',
  fluxoInfo,
  '',
  docsInfo,
  '',
  'REGRAS:',
  '- NAO pergunte numero de dependentes (ja sabe: ' + leadDependentes + ')',
  '- NAO pergunte tipo PF/PJ (ja sabe: ' + leadTipo + ')',
  '- SEMPRE pergunte sobre plano anterior (tanto PF quanto PJ)',
  '- Faca UMA pergunta por vez',
  '- Nunca peca info que ja foi fornecida',
  '- Para dependentes: pergunte o vinculo (empregado/colaborador/funcionario/parente/familiar)',
  '- Se vinculo empregaticio: peca holerite ou carteira de trabalho',
  '- Se vinculo familiar: NAO peca documento de vinculo',
  '',
  'ESCALACAO:',
  '- Cancelamento: "Vou direcionar para nosso setor de atendimento."',
  '- Insatisfeito: "Entendo. Vou encaminhar para um atendente."',
  '- Pede humano: "Claro, vou transferir agora."',
  '',
  'HISTORICO:',
  history || '(voce enviou a primeira msg pedindo nome completo)',
  '',
  'Responda APENAS a mensagem atual. UMA pergunta por vez.'
];

const systemPrompt = promptLines.join(NL);

let userMessage = 'Cliente ' + pushName + ' (' + number + ') disse: ' + messageText;
if (hasMedia) {
  userMessage += NL + '[' + mediaInfo + ']';
}

const response = await this.helpers.httpRequest({
  method: 'POST',
  url: TUNNEL_URL,
  headers: { 'content-type': 'application/json' },
  body: {
    model: 'llama-3.3-70b-versatile',
    max_tokens: 700,
    messages: [
      {role: 'system', content: systemPrompt},
      {role: 'user', content: userMessage}
    ]
  }
});

const aiResponse = response.choices[0].message.content;
return [{json: {number: number, pushName: pushName, messageText: messageText, aiResponse: aiResponse}}];"""

# URL do proxy exposto via Cloudflare tunnel. ATUALIZAR a cada novo tunnel.
TUNNEL_URL = 'https://yale-results-concentration-mapping.trycloudflare.com'
new_ia_code = new_ia_code.replace('TUNNEL_URL', "'" + TUNNEL_URL + "'")

for node in wf['nodes']:
    if node['id'] == 'filtro-parse':
        node['parameters']['jsCode'] = new_filtro_code
    elif node['id'] == 'chamar-ia':
        node['parameters']['jsCode'] = new_ia_code

json.dump(wf, open('C:/Users/Thierry/Downloads/workflow-wattzap-v4.json', 'w'), ensure_ascii=False)
print('Workflow atualizado - vinculo familiar + contrato social + cartao CNPJ + plano anterior sempre')
