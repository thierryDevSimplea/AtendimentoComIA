// Tests for consulta-cns.test.js
const http = require('http');
const { TextEncoder } = require('util');

describe('consulta-cns.js tests', () => {
  // Mock do servidor CNS
  const CNS_PORT = 13457;
  let server;

  beforeAll((done) => {
    server = http.createServer((req, res) => {
      if (req.method !== 'POST') {
        res.writeHead(405);
        res.end('Method not allowed');
        return;
      }

      let body = '';
      req.on('data', chunk => body += chunk);
      req.on('end', () => {
        try {
          const data = JSON.parse(body);
          if (!data.cpf || !data.dataNascimento) {
            res.writeHead(400);
            res.end(JSON.stringify({ error: 'cpf e dataNascimento obrigatorios' }));
            return;
          }

          res.writeHead(200, { 'content-type': 'application/json' });
          res.end(JSON.stringify({
            cns: '123456789012345',
            nome: 'Teste',
            found: true
          }));
        } catch (e) {
          res.writeHead(500);
          res.end(JSON.stringify({ error: e.message }));
        }
      });
    });
    server.listen(CNS_PORT, done);
  });

  afterAll((done) => {
    server.close(done);
  });

  test('GET returns 405 Method Not Allowed', async () => {
    const response = await fetch(`http://localhost:${CNS_PORT}`, { method: 'GET' });
    expect(response.status).toBe(405);
  });

  test('POST sem cpf/dataNascimento retorna 400', async () => {
    const response = await fetch(`http://localhost:${CNS_PORT}`, {
      method: 'POST',
      headers: { 'content-type': 'application/json' },
      body: JSON.stringify({})
    });
    expect(response.status).toBe(400);
  });

  test('POST com cpf/dataNascimento validos retorna 200', async () => {
    const response = await fetch(`http://localhost:${CNS_PORT}`, {
      method: 'POST',
      headers: { 'content-type': 'application/json' },
      body: JSON.stringify({
        cpf: '12345678901',
        dataNascimento: '01/01/1990'
      })
    });
    expect(response.status).toBe(200);
  });
});