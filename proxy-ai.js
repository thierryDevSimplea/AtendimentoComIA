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

// Servidor principal
const server = http.createServer((req, res) => {
  if (req.method !== 'POST') {
    res.writeHead(405);
    res.end('Method not allowed');
    return;
  }

  if (!CONFIG.GROQ_API_KEY) {
    res.writeHead(500, { 'content-type': 'application/json' });
    res.end(JSON.stringify({ error: 'GROQ_API_KEY nao definida no ambiente do proxy' }));
    return;
  }

  let body = '';
  req.on('data', chunk => body += chunk);
  req.on('end', () => {
    let payload = body;
    try {
      const parsed = JSON.parse(body);
      if (!parsed.model) parsed.model = CONFIG.DEFAULT_MODEL;
      payload = JSON.stringify(parsed);
    } catch (e) {
      // se nao for JSON valido, repassa como veio
    }

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
      res.writeHead(500);
      res.end(JSON.stringify({ error: err.message }));
    });

    proxyReq.write(payload);
    proxyReq.end();
  });
});

server.listen(CONFIG.PORT, () => {
  console.log(`AI Proxy (Groq) running on port ${CONFIG.PORT}`);
});