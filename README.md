# API-Study

Aplicacao para geracao de conteudo educacional personalizado por perfil de estudante.

## O que este projeto entrega
- Perfil de estudante: nome, idade, nivel e estilo de aprendizado.
- Geracao de 4 tipos de conteudo:
  - `conceptual` (explicacao conceitual com orientacao de chain-of-thought)
  - `examples` (exemplos praticos contextualizados)
  - `reflection` (perguntas de reflexao e pensamento critico)
  - `visual` (resumo visual com diagrama ASCII)
- Persistencia em JSON com timestamp para cada geracao e bundle consolidado.
- Comparacao entre versoes de prompts (`v1` e `v2`).
- Cache (disk ou redis) para reduzir chamadas repetidas.
- Interface CLI e API Flask.

## Configuracao
1. Crie o `.env` com base no `.env.example`.
2. Instale dependencias:
```bash
pip install -r requirements.txt
```

## Executar CLI
```bash
python cli/menu.py
```

## Executar API
```bash
python api/app.py
```

### Endpoints principais
- `GET /api/students`
- `POST /api/students`
- `POST /api/generate`
- `POST /api/generate-all`
- `POST /api/compare`
- `GET /api/history`
