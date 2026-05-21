import puppeteer from 'puppeteer';
import http from 'http';

async function consultarCNS(cpf, dataNascimento) {
  const browser = await puppeteer.launch({
    headless: 'new',
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });
  
  try {
    const page = await browser.newPage();
    await page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36');
    
    await page.goto('https://cnesadm.datasus.gov.br/cnesadm/publico/usuarios/cadastro', {
      waitUntil: 'networkidle2',
      timeout: 30000
    });
    
    await new Promise(r => setTimeout(r, 3000));
    
    // Preenche CPF
    await page.click('input[name="cpf"]');
    await page.type('input[name="cpf"]', cpf, { delay: 30 });
    
    // Preenche data nascimento
    await page.click('input[name="dataNascimento"]');
    await page.type('input[name="dataNascimento"]', dataNascimento, { delay: 30 });
    
    // Tab para sair do campo e disparar a consulta automatica
    await page.keyboard.press('Tab');
    await new Promise(r => setTimeout(r, 5000));
    
    // Captura resultado
    const resultado = await page.evaluate(() => {
      const cnsInput = document.querySelector('input[name="cns"]');
      const nomeInput = document.querySelector('input[name="nome"]');
      const cns = cnsInput ? cnsInput.value : null;
      const nome = nomeInput ? nomeInput.value : null;
      return { cns, nome, found: !!cns };
    });
    
    await browser.close();
    return resultado;
    
  } catch (error) {
    await browser.close();
    return { cns: null, nome: null, found: false, error: error.message };
  }
}

// Servidor HTTP
const server = http.createServer(async (req, res) => {
  if (req.method !== 'POST') {
    res.writeHead(405);
    res.end(JSON.stringify({ error: 'Method not allowed' }));
    return;
  }

  let body = '';
  req.on('data', chunk => body += chunk);
  req.on('end', async () => {
    try {
      const { cpf, dataNascimento } = JSON.parse(body);
      if (!cpf || !dataNascimento) {
        res.writeHead(400);
        res.end(JSON.stringify({ error: 'cpf e dataNascimento obrigatorios' }));
        return;
      }
      
      console.log(`Consultando CNS: CPF=${cpf}, Nasc=${dataNascimento}`);
      const resultado = await consultarCNS(cpf, dataNascimento);
      console.log(`Resultado: CNS=${resultado.cns}, Nome=${resultado.nome}`);
      
      res.writeHead(200, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify(resultado));
    } catch (error) {
      res.writeHead(500);
      res.end(JSON.stringify({ error: error.message }));
    }
  });
});

server.listen(3457, () => console.log('CNS Consulta rodando na porta 3457'));
