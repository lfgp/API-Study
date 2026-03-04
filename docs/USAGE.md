# Usage

## Configuracao
1. Copie `.env.example` para `.env`.
2. Preencha `OPENAI_API_KEY`.

## CLI
```bash
python cli/menu.py
```

Menu principal:
1. List students
2. Generate 4 content types
3. Compare prompt versions
4. View generation history
5. Exit

## API
```bash
python api/app.py
```

### Endpoints
- `GET /api/students`
- `POST /api/students`
- `POST /api/generate`
- `POST /api/generate-all`
- `POST /api/compare`
- `GET /api/history`

### Exemplo de `POST /api/generate`
```json
{
  "student_id": "1",
  "topic": "fracoes",
  "type": "conceptual",
  "prompt_version": "v1",
  "use_cache": true
}
```
