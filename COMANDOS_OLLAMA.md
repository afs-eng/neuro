# Comandos Ollama

## Objetivo

Guia rapido para subir a Ollama no Windows, testar a conexao local e validar a integracao com o backend Docker do sistema Neuro.

---

## 1. Instalar no Windows

Instale a Ollama Desktop no Windows e confirme que a API local responde em `11434`.

---

## 2. Verificar a Ollama

Com a Ollama aberta no Windows, valide a API local:

```bash
curl http://localhost:11434/api/tags
```

---

## 3. Baixar modelo

Modelo recomendado para o backend em Docker:

```bash
ollama pull qwen3.5:27b
```

Listar modelos instalados:

```bash
ollama list
```

---

## 4. Testar a API da Ollama

Verificar se o servidor esta respondendo:

```bash
curl http://localhost:11434/api/tags
```

Testar geracao simples:

```bash
curl -X POST http://localhost:11434/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "model": "qwen3.5:27b",
    "prompt": "Responda apenas: ok",
    "stream": false
  }'
```

---

## 5. Variaveis do projeto

Quando o backend roda em Docker e a Ollama roda no host Windows, use estas variaveis no `.env`:

```env
AI_PROVIDER=ollama
DOCKER_OLLAMA_BASE_URL=http://host.docker.internal:11434
DOCKER_OLLAMA_MODEL=qwen3.5:27b
```

Se voce tambem roda o Django fora do Docker, mantenha as variaveis locais separadas:

```env
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=qwen3.5:27b
```

---

## 6. Testar integracao com o backend Docker

Recrie o backend para carregar as novas variaveis:

```bash
docker compose up -d --build backend
```

Depois rode o script de verificacao completa:

```bash
./test_ia_suite.sh
```

Esse script faz:

- teste da Ollama em `localhost:11434`
- teste da Ollama dentro do container em `host.docker.internal:11434`
- `manage.py check`
- regeneracao real de uma secao do laudo via backend

---

## 7. Subir o backend manualmente

```bash
.venv/bin/python manage.py runserver
```

---

## 8. Pegar token de acesso

Exemplo para o usuario admin local:

```bash
.venv/bin/python manage.py shell -c "from apps.accounts.models import User; print(User.objects.get(email='admin@msn.com').api_token)"
```

---

## 9. Testar a API do sistema

Hoje o teste funcional real usa a secao `fdt` do laudo `1`.

```bash
curl -X POST http://127.0.0.1:8000/api/reports/1/regenerate-section/fdt \
  -H "Authorization: Bearer <TOKEN>"
```

Se tudo estiver certo, a resposta deve trazer algo como:

- `generated_text`
- `generation_metadata.provider = ollama`
- `generation_metadata.model = qwen3.5:27b`
- `warnings_payload = []`

---

## 10. Comandos uteis de debug

Ver modelos:

```bash
curl http://localhost:11434/api/tags
```

Testar modelo direto no terminal:

```bash
ollama run qwen3.5:27b "Responda apenas: ok"
```

Verificar backend Django:

```bash
.venv/bin/python manage.py check
```

Aplicar migrations pendentes:

```bash
.venv/bin/python manage.py migrate
```

---

## 11. Fluxo recomendado no dia a dia

1. Abrir a Ollama no Windows
2. Garantir que o modelo `qwen3.5:27b` existe
3. Recriar o backend com `docker compose up -d --build backend`
4. Rodar `./test_ia_suite.sh` quando quiser validar tudo rapido
5. Testar a rota `/api/reports/1/regenerate-section/fdt` quando quiser validar o fluxo HTTP
