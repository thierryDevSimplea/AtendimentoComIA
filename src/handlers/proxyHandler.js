// src/handlers/proxyHandler.js
const http = require('http');
const CONFIG = require('../config/proxyConfig');
const { parseBody, sendJsonResponse, ensureModel, forwardToUpstream } = require('../utils/httpHelpers');

function createServer() {
  return http.createServer(async (req, res) => {
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
}

module.exports = { createServer };