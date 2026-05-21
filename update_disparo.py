import json

p = 'C:/Atendimento2/disparo.json'
wf = json.load(open(p))

NEW_EVO = 'https://collectible-question-plc-rats.trycloudflare.com'

lista_code = """// Lista de leads para disparo (start da listinha)
// Campos: number, name, type (PJ ou PF)
const leads = [
  { number: '5521971059196', name: 'Thierry', type: 'PF' }
];

return leads.map(lead => ({json: lead}));"""

montar_code = """const lead = $input.all()[0].json;
const name = lead.name || '';
const number = lead.number;
const type = lead.type;

let text = '';

if (type === 'PJ') {
  text = `Ola${name ? ' ' + name : ''}. Aqui e da Kaizen Consultoria, consultoria em planos de saude empresariais.

Para dar andamento a cotacao do plano PME/PJ, pode me confirmar seu nome completo?`;
} else {
  text = `Ola${name ? ' ' + name : ''}. Aqui e da Kaizen Consultoria, consultoria em planos de saude.

Para dar andamento a sua cotacao, pode me confirmar seu nome completo?`;
}

return [{json: {number, text, name, type}}];"""

enviar_code = """const msg = $input.all()[0].json;

await this.helpers.httpRequest({
  method: 'POST',
  url: 'https://collectible-question-plc-rats.trycloudflare.com/message/sendText/wattzap',
  headers: {'apikey': 'evo_wattzap_2026', 'Content-Type': 'application/json'},
  body: JSON.stringify({number: msg.number, text: msg.text}),
});

return [{json: {status: 'sent', number: msg.number, name: msg.name, type: msg.type}}];"""

for n in wf['nodes']:
    if n['name'] == 'Lista de Leads':
        n['parameters']['jsCode'] = lista_code
    elif n['name'] == 'Montar Mensagem por Tipo':
        n['parameters']['jsCode'] = montar_code
    elif n['name'] == 'Enviar via WhatsApp':
        n['parameters']['jsCode'] = enviar_code
    if n['type'].endswith('webhook'):
        print('webhook path:', n['parameters'].get('path'))

payload = {'name': wf['name'], 'nodes': wf['nodes'], 'connections': wf['connections'], 'settings': wf.get('settings', {'executionOrder': 'v1'})}
json.dump(payload, open('C:/Atendimento2/disparo-payload.json', 'w'), ensure_ascii=False)
print('disparo payload pronto')
