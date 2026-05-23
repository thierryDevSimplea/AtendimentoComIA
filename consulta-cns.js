const http = require('http');

async function consultarCNS(cpf, dataNascimento) {
  const puppeteer = require('puppeteer');
  const browser = await puppeteer.launch({
    headless: 'new',
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });

  try {
    const page = await browser.newPage();
    await page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36');
    await page.goto('https://cnesadm.datasus.gov.br/cnesadm/publico/usuarios/cadastro', {
      waitUntil: 'networkidle2',
      timeout: 30000
    });
    await page.waitForSelector('input[ng-model="usuario.cpf"], input[name="cpf"], #cpf', { timeout: 15000 });

    const cpfInput = await page.$('input[ng-model="usuario.cpf"]') || await page.$('input[name="cpf"]') || await page.$('#cpf');
    if (cpfInput) {
      await cpfInput.click({ clickCount: 3 });
      await cpfInput.type(cpf, { delay: 50 });
    }

    const dataInput = await page.$('input[ng-model="usuario.dataNascimento"]') || await page.$('input[name="dataNascimento"]') || await page.$('#dataNascimento');
    if (dataInput) {
      await dataInput.click({ clickCount: 3 });
      await dataInput.type(dataNascimento, { delay: 50 });
    }

    const btnPesquisar = await page.$('button[ng-click*="pesquisar"]') || await page.$('button[type="submit"]') || await page.$('.btn-primary');
    if (btnPesquisar) {
      await btnPesquisar.click();
    }

    await page.waitForTimeout(5000);

    const resultado = await page.evaluate(() => {
      const cnsEl = document.querySelector('[ng-model="usuario.cns"]') ||
                    document.querySelector('input[name="cns"]') ||
                    document.querySelector('#cns');
      if (cnsEl) return { cns: cnsEl.value, found: true };

      const bodyText = document.body.innerText;
      const cnsMatch = bodyText.match(/CNS[:\s]*(\d{15})/i) || bodyText.match(/(\d{15})/);
      if (cnsMatch) return { cns: cnsMatch[1], found: true };

      const inputs = document.querySelectorAll('input[type="text"]');
      const values = {};
      inputs.forEach(input => {
        if (input.value) {
          values[input.name || input.id || 'unknown'] = input.value;
        }
      });

      return { cns: null, found: false, pageData: values, bodySnippet: bodyText.substring(0, 2000) };
    });

    await browser.close();
    return resultado;

  } catch (error) {
    await browser.close();
    return { cns: null, found: false, error: error.message };
  }
}

// Servidor HTTP
const server = http.createServer(async (req, res) => {
  if (req.method !== 'POST') {
    res.writeHead(405);
    res.end('Method not allowed');
    return;
  }

  let body = '';
  req.on('data', chunk => body += chunk);
  req.on('end', async () => {
    try {
      const { cpf, dataNascimento } = JSON.parse(body);

      if (!cpf || !dataNascimento) {
        res.writeHead(400);
        res.end(JSON.stringify({ error: 'cpf e dataNascimento sao obrigatorios' }));
        return;
      }

      console.log(`Consultando CNS para CPF: ${cpf}, Nascimento: ${dataNascimento}`);
      const resultado = await consultarCNS(cpf, dataNascimento);
      console.log('Resultado:', JSON.stringify(resultado));

      res.writeHead(200, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify(resultado));
    } catch (error) {
      res.writeHead(500);
      res.end(JSON.stringify({ error: error.message }));
    }
  });
});

server.listen(3457, () => console.log('CNS Consulta rodando na porta 3457'));