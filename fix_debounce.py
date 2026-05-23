import json, re

p = 'C:/Users/Thierry/Downloads/workflow-wattzap-v4.json'
wf = json.load(open(p))

nodes = {n['id']: n for n in wf['nodes']}

# 1) Historico 10 -> 50
bh = nodes['buscar-historico']
bh['parameters']['jsCode'] = bh['parameters']['jsCode'].replace('limit: 10', 'limit: 50')

# Extrai o tunnel da Evolution do proprio no de historico (sempre atual)
m = re.search(r"https://[a-z0-9-]+\.trycloudflare\.com", bh['parameters']['jsCode'])
EVO = m.group(0) if m else 'https://collectible-question-plc-rats.trycloudflare.com'

# 2) No de Debounce (espera rajada + aborta se chegou msg mais nova do cliente)
debounce_code = """const input = $input.all()[0].json;
const EVO = '__EVO__';
// Debounce: espera mensagens em rajada antes de responder
await new Promise(r => setTimeout(r, 7000));
try {
  const resp = await this.helpers.httpRequest({
    method: 'POST',
    url: EVO + '/chat/findMessages/wattzap',
    headers: { 'apikey': 'evo_wattzap_2026', 'Content-Type': 'application/json' },
    body: { where: { key: { remoteJid: input.remoteJid } }, limit: 8 }
  });
  let recs = [];
  if (resp && resp.messages && resp.messages.records) recs = resp.messages.records;
  else if (resp && resp.records) recs = resp.records;
  else if (resp && Array.isArray(resp.messages)) recs = resp.messages;
  let maxUserTs = 0;
  for (const mm of recs) {
    const fm = (mm.key || {}).fromMe;
    if (!fm) { const ts = mm.messageTimestamp || 0; if (ts > maxUserTs) maxUserTs = ts; }
  }
  if (maxUserTs && input.messageTimestamp && maxUserTs > input.messageTimestamp) {
    return []; // chegou mensagem mais nova do cliente: aborta (evita race/regressao)
  }
} catch (e) { /* em erro, segue normalmente */ }
return [{json: input}];""".replace('__EVO__', EVO)

filtro = nodes['filtro-parse']
fx, fy = filtro['position']

# remove no debounce antigo se ja existir (idempotente)
wf['nodes'] = [n for n in wf['nodes'] if n['id'] != 'debounce-msg']

wf['nodes'].append({
    'parameters': {'jsCode': debounce_code},
    'id': 'debounce-msg',
    'name': 'Debounce',
    'type': 'n8n-nodes-base.code',
    'typeVersion': 2,
    'position': [fx + 220, fy]
})

# 3) Reconectar: Filtrar e Parsear -> Debounce -> Buscar Historico
conns = wf['connections']
conns['Filtrar e Parsear'] = {'main': [[{'node': 'Debounce', 'type': 'main', 'index': 0}]]}
conns['Debounce'] = {'main': [[{'node': 'Buscar Historico', 'type': 'main', 'index': 0}]]}

json.dump(wf, open(p, 'w'), ensure_ascii=False)
print('debounce + historico 50 aplicados. EVO=', EVO)
print('conexoes:', {k: [[c['node'] for c in arr] for arr in v['main']] for k, v in conns.items()})
