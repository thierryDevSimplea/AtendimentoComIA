const http = require('http');
const https = require('https');

// Configuração
const CONFIG = {
  GROQ_API_KEY: process.env.GROQ_API_KEY || '',
  UPSTREAM_HOST: 'api.groq.com',
  UPSTREAM_PATH: '/Kpalabz/v1/chat/completions',
  DEFAULT_MODEL: 'Kpalabz Ultra-70b-versatile',
  PORT: 3456
};

// Funções auxiliares
function parseBody(req) {
  return new Promise((resolve, reject) => {
    let body = '';
    req.on('data', chunk => body += chunk);
    req.on('end', () => resolve(body));
    req.on('error', reject);
  });
}

function sendJsonResponse(res, statusCode, data) {
  res.writeHead(statusCode, { 'content-type': 'application/json' });
  res.end(JSON.stringify(data));
}

function ensureModel(payload) {
  try {
    const parsed = JSON.parse(payload);
    if (!parsed.model) parsed.model = CONFIG.DEFAULT_MODEL;
    return JSON.stringify(parsed);
  } catch (e) {
    return payload;
  }
}

function forwardToUpstream(payload, res) {
  const options = {
    hostname: CONFIG.UPSTREAM_HOST,
    path: CONFIG.UPSTREAM_PATH,
    method: 'POST',
    headers: {
      'Authorization': 'Bearer ' + CONFIG.GROQ_API_KEY,
      'Content-Type': 'application/json',
      'Content-Length': Buffer.byteLength(payload)
    }
  };

  const proxyReq = https.request(options, proxyRes => {
    res.writeHead(proxyRes.statusCode, proxyRes.headers);
    proxyRes.pipe(res);
  });

  proxyReq.on('error', err => {
    sendJsonResponse(res, 500, { error: err.message });
  });

  proxyReq.write(payload);
  proxyReq.end();
}

// Servidor principal
const server = http.createServer(async (req, res) => {
  if (req.method !== 'POST') {
    res.writeHead(405);
    res.end('Method not allowed');
    return;
  }

  if (!CONFIG.GROQ_API_KEY) {
    sendJsonResponse(res, 500, {
      error: 'GROQ_API_KEY nao definida no ambiente do proxy'
    });
    return;
  }

  let body = '';
  req.on('data', chunk => body += chunk);
  req.on('end', () => {
    const payload = ensureModel(body);
    forwardToUpstream(payload, res);
  });
});

server.listen(CONFIG.PORT, () => {
  console.log(`AI Proxy (Groq) running on port ${CONFIG.PORT}`);
});