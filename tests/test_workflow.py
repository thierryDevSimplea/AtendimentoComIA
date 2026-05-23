# tests/test_workflow.py - Testes de caracterização para os scripts de workflow
# Captura o comportamento atual: scripts Python que injetam código JS nos workflows n8n

import json
import os
import pytest


class TestUpdateWorkflow:
    """Testes de caracterização para update_workflow.py."""

    def test_imports_completam(self):
        """O módulo deve importar sem erros."""
        import update_workflow

    def test_script_lido_como_modulo(self):
        """Verifica que as strings de código JS existem no script."""
        with open("update_workflow.py", "r", encoding="utf-8") as f:
            content = f.read()
        assert "new_filtro_code" in content, "Script deve conter new_filtro_code"
        assert "new_ia_code" in content, "Script deve conter new_ia_code"
        assert "filtro-parse" in content, "Script deve referenciar nó filtro-parse"
        assert "chamar-ia" in content, "Script deve referenciar nó chamar-ia"

    def test_tunnel_url_injetado(self):
        """O script deve injetar TUNNEL_URL nas strings de código."""
        with open("update_workflow.py", "r", encoding="utf-8") as f:
            content = f.read()
        assert "TUNNEL_URL" in content


class TestWorkflowJson:
    """Testes de caracterização para o workflow exportado."""

    def test_workflow_teste_json_existe(self):
        """O arquivo workflow-teste-lead.json deve existir."""
        assert os.path.exists("workflow-teste-lead.json"), "workflow-teste-lead.json nao encontrado"

    def test_workflow_teste_json_valido(self):
        """O JSON deve ser válido e conter nós."""
        with open("workflow-teste-lead.json", "r", encoding="utf-8") as f:
            wf = json.load(f)
        assert "nodes" in wf, "Workflow deve ter lista de nós"
        assert len(wf["nodes"]) > 0, "Workflow deve ter pelo menos 1 nó"


class TestDisparoJson:
    """Testes de caracterização para os arquivos de disparo."""

    def test_disparo_json_existe(self):
        """O arquivo disparo.json deve existir."""
        assert os.path.exists("disparo.json"), "disparo.json nao encontrado"

    def test_disparo_json_valido(self):
        """O JSON de disparo deve ser válido com nós e conexões."""
        with open("disparo.json", "r", encoding="utf-8") as f:
            content = json.load(f)
        assert "nodes" in content
        assert len(content["nodes"]) > 0
        assert "connections" in content