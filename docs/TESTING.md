# Testing Guide

## Requisitos
- Python 3.10+
- Dependencias instaladas via `requirements.txt`

## Executar testes
```bash
python -m pytest
```

A configuracao de testes esta em `pytest.ini`:
- `testpaths = tests`
- `norecursedirs = venv .git __pycache__`

## Escopo atual da suite
- `tests/test_student_model.py`
  - validacao do modelo `Student`
  - normalizacao de nome
  - geracao de contexto
- `tests/test_prompt_engine.py`
  - validacao de `content_type` e `prompt_version`
  - estrutura de mensagens para os 4 tipos de conteudo
  - diferenca entre versoes `v1` e `v2`
- `tests/test_json_handler.py`
  - criacao de perfis padrao
  - persistencia de geracoes
  - filtro de historico por estudante
- `tests/test_api_app.py`
  - endpoints principais (`/api/students`, `/api/generate`, `/api/compare`, `/api/history`)
  - validacoes de payload
  - fluxo de sucesso com `generator` mockado

## Resultado atual
- `17 passed`

## Observacao
- Existem warnings de `datetime.utcnow()` (deprecacao no Python 3.13).
  - Nao quebra a suite, mas vale migrar para `datetime.now(UTC)` em uma etapa de hardening.
