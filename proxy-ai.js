const http = require('http');
const https = require('https');

// Chave via variavel de ambiente: defina GROQ_API_KEY antes de iniciar.
//   PowerShell:  $env:GROQ_API_KEY = "gsk_..."; node proxy-ai.js
const GROQ_API_KEY = process.env.GROQ_API_KEY || '';

// Provedor atual: Groq (compativel com a API da OpenAI).
// Para migrar pra OpenAI em producao, troque host/path/chave abaixo:
//   host: 'api.openai.com', path: '/v1/chat/completions', OPENAI_API_KEY
const UPSTREAM_HOST = 'api.groq.com';
const UPSTREAM_PATH = '/openai/v1/chat/completions';
const DEFAULT_MODEL = 'llama-3.3-70b-versatile';

const server = http.createServer((req, res) => {
  if (req.method !== 'POST') {
    res.writeHead(405);
    res.end('Method not allowed');
    return;
  }

  if (!GROQ_API_KEY) {
    res.writeHead(500, { 'content-type': 'application/json' });
    res.end(JSON.stringify({ error: 'GROQ_API_KEY nao definida no ambiente do proxy' }));
    return;
  }

  let body = '';
  req.on('data', chunk => body += chunk);
  req.on('end', () => {
    // Garante que o body tenha um modelo valido do Groq se nao vier um.
    let payload = body;
    try {
      const parsed = JSON.parse(body);
      if (!parsed.model) parsed.model = DEFAULT_MODEL;
      payload = JSON.stringify(parsed);
    } catch (e) {
      // se nao for JSON valido, repassa como veio
    }

    const options = {
      hostname: UPSTREAM_HOST,
      path: UPSTREAM_PATH,
      method: 'POST',
      headers: {
        'Authorization': 'Bearer ' + GROQ_API_KEY,
        'Content-Type': 'application/json',
        'Content-Length': Buffer.byteLength(payload)
      }
    };

    const proxyReq = https.request(options, proxyRes => {
      res.writeHead(proxyRes.statusCode, proxyRes.headers);
      proxyRes.pipe(res);
    });

    proxyReq.on('error', err => {
      res.writeHead(500);
      res.end(JSON.stringify({ error: err.message }));
    });

    proxyReq.write(payload);
    proxyReq.end();
  });
});

server.listen(3456, () => console.log('AI Proxy (Groq) running on port 3456'));
