# Architecture

## Visao Geral
O projeto gera conteudo educacional personalizado com base no perfil de estudante,
com cache local/redis, persistencia em JSON e comparacao entre versoes de prompts.

## Modulos
- `core/student.py`
  - modelo `Student` (idade, nivel, estilo, interesses)
- `core/prompt_engine.py`
  - gera prompts para 4 tipos de conteudo
  - suporta versoes `v1` e `v2`
- `core/generator.py`
  - integra OpenAI Async API
  - aplica cache
  - salva geracoes e comparacoes
- `storage/cache_manager.py`
  - cache em diskcache/redis
  - fallback em memoria para ambientes minimos
- `storage/jason_handler.py`
  - persistencia JSON de estudantes, geracoes e comparacoes
- `api/app.py`
  - endpoints Flask para consumo externo
- `cli/menu.py`
  - interface de operacao interativa

## Fluxo de Geracao
1. Usuario seleciona estudante e topico (CLI/API).
2. `PromptEngine` monta mensagens com contexto do estudante.
3. `ContentGenerator` consulta cache.
4. Se necessario, chama modelo OpenAI.
5. Resultado e metadados sao salvos em JSON.
6. Historico fica disponivel para consulta e comparacao.
