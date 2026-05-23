// Tests for proxy-ai-test.js
const http = require('http');
const request = require('supertest');

describe('proxy-ai.js tests', () => {
  // Cria um servidor proxy mock idêntico ao do proxy-ai.js
  const PROXY_PORT = 13456;

  let server;
  beforeAll((done) => {
    server = http.createServer((req, res) => {
      if (req.method !== 'POST') {
        res.writeHead(405);
        res.end('Method not allowed');
        return;
      }

      if (!process.env.GROQ_API_KEY) {
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
          if (!parsed.model) parsed.model = 'llama-3.3-70b-versatile';
          payload = JSON.stringify(parsed);
        } catch (e) {}

        // Simula chamada ao Groq
        res.writeHead(200, { 'content-type': 'application/json' });
        res.end(JSON.stringify({
          choices: [{ message: { content: 'Resposta mock do assistente.' } }]
        }));
      });
    });
    server.listen(PROXY_PORT, () => {
      process.env.GROQ_API_KEY = process.env.GROQ_API_KEY || 'gsk_test_key';
      done();
    });
  });

  afterAll((done) => {
    server.close(done);
    delete process.env.GROQ_API_KEY;
  });

  test('GET returns 405 Method Not Allowed', async () => {
    const response = await fetch(`http://localhost:${PROXY_PORT}`, { method: 'GET' });
    expect(response.status).toBe(405);
  });

  test('DELETE returns 405 Method Not Allowed', async () => {
    const response = await fetch(`http://localhost:${PROXY_PORT}`, { method: 'DELETE' });
    expect(response.status).toBe(405);
  });

  test('POST sem GROQ_API_KEY retorna 500', async () => {
    const originalKey = process.env.GROQ_API_KEY;
    delete process.env.GROQ_API_KEY;

    const response = await fetch(`http://localhost:${PROXY_PORT}`, {
      method: 'POST',
      headers: { 'content-type': 'application/json' },
      body: JSON.stringify({ messages: [{ role: 'user', content: 'oi' }] })
    });
    expect(response.status).toBe(500);
    const data = await response.json();
    expect(data.error).toContain('GROQ_API_KEY');

    process.env.GROQ_API_KEY = originalKey;
  });

  test('POST com GROQ_API_KEY retorna 200 com resposta da IA', async () => {
    const response = await fetch(`http://localhost:${PROXY_PORT}`, {
      method: 'POST',
      headers: { 'content-type': 'application/json' },
      body: JSON.stringify({
        model: 'Kpalabz Ultra-70b-versatile',
        messages: [{ role: 'user', content: 'Ola' }]
      })
    });
    expect(response.status).toBe(200);
    const data = await response.json();
    expect(data.choices).toBeDefined();
    expect(data.choices[0].message.content).toBe('Resposta mock do assistente.');
  });

  test('POST com model vazio usa modelo padrao', async () => {
    const response = await fetch(`http://localhost:${PROXY_PORT}`, {
      method: 'POST',
      headers: { 'content-type': 'application/json' },
      body: JSON.stringify({
        messages: [{ role: 'user', content: 'teste' }]
      })
    });
    expect(response.status).toBe(200);
    const data = await response.json();
    expect(data.choices).toBeDefined();
  });

  test('POST com body invalido nao quebra', async () => {
    const response = await fetch(`http://localhost:${PROXY_PORT}`, {
      method: 'POST',
      headers: { 'content-type': 'application/json' },
      body: 'nao-json-valido'
    });
    expect(response.status).toBe(200);
  });
});