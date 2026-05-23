// src/utils/httpHelpers.js
const CONFIG = require('../config/proxyConfig');

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
    res.writeHead(500);
    res.end(JSON.stringify({ error: err.message }));
  });

  proxyReq.write(payload);
  proxyReq.end();
}