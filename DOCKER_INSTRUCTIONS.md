# 🐳 NeuroAvalia - Guia Definitivo do Docker

Este guia contém os passos exatos para rodar a aplicação em três fases: **Local (Dev)**, **Produção (VPS)** e o ciclo de **Deploy Contínuo**.

A arquitetura usa:
- **Django** (Backend / API) - Porta 8000
- **Next.js** (Frontend) - Porta 3000
- **PostgreSQL** (Banco de Dados) - Porta 5432
- **Nginx** (Reverse Proxy para Produção) - Portas 80/443

---

## 💻 1. Ambiente Local (Desenvolvimento)

O foco aqui é o **hot-reload**. Sempre que você salvar um arquivo `.py` ou `.tsx`, a aplicação reiniciará no seu navegador imediatamente.

### A. Preparação Exigida (Apenas na 1ª vez)
Crie os arquivos de ambiente baseados nos exemplos:
```bash
# Na raiz do backend
cp .env.example .env

# Na raiz do frontend
cp neuro-frontend/.env.example neuro-frontend/.env.local
```

### B. O Comando Mágico (Subir o App)
Sempre na pasta raiz do seu projeto (onde está o `docker-compose.yml`), rode:
```bash
docker compose up --build
```
> **Nota:** Nas próximas vezes que você for codar, pode omitir o `--build`, usando apenas `docker compose up`.

**As portas abertas para você acessar:**
- 🌐 Frontend: `http://localhost:3000`
- 🖥️ API Docs (Swagger Ninja): `http://localhost:8000/api/docs`
- ⚙️ Django Admin: `http://localhost:8000/admin`
- 🗄️ PostgreSQL (DBeaver/PgAdmin): Conecte usando Host: `localhost`, Porta: `5432`, Usuário: `neuro_user`, Senha: `neuro_pass`.

### C. Desligando ao Final do Dia
```bash
# Aperte CTRL+C e digite:
docker compose down
```

---

## 🚀 2. Ambiente de Produção (Aprovação / VPS)

Para ambientes reais conectados na internet, não usamos hot-reload. O tráfego inteiro passará portão afora obrigatoriamente pelo NGINX com alta performance usando o arquivo modificado (`docker-compose.prod.yml`).

### A. Subir Carga Real Otimizada
Assegure que no `.env` do VPS os IPs e Domínios estejam perfeitamente configurados.
```bash
docker compose -f docker-compose.prod.yml up -d --build
```
O modo `-d` (detached) indica que você fará a liberação de volta do terminal e os servidores vão rodar nos "bastidores". 

### B. As portas protegidas
O acesso mundial ocorrerá apenas via **Porta 80**.
- Você não terá mais a Porta 3000 ou 8000 pendurada diretamente à mercê de hackers. As rotas `/api`, `/admin`, `/media` e `/static` foram elegantemente cortadas dentro do `nginx.conf`.

---

## 🔄 3. O Fluxo de Deploy Técnico (Atualizando o Servidor)

Quando você codar uma *V2* (versão nova) ou correção drástica, subiu pro Git, e deseja renovar o seu servidor VPS oficial (o código atualizado rodando), existe um fluxo blindado!

Entre na VPS via SSH, ou se estiver testando algo crítico, siga essa ordem exata:

```bash
# 1. Puxe a nova versão limpa do Github/Gitlab
git pull origin main

# 2. Pare apenas a "Produção" sem perder o banco/volumes (não digite -v jamais no passo abaixo)
docker compose -f docker-compose.prod.yml down

# 3. Rebuild as imagens com o código zero bala (O Entrypoint atualizará as novas as "migrations"!)
docker compose -f docker-compose.prod.yml build --no-cache

# 4. Solte no ar novamente
docker compose -f docker-compose.prod.yml up -d
```

---

## 🧰 Comandos do Dia a Dia (Cheat Sheet de Suporte Técnico)

**1. Eu instalei um pacote Python via `uv` e ele não pega! O que fazer?**
> R: Mande a imagem refazer do zero apagando lixo de cash:
> `docker compose up --build --force-recreate`

**2. Como eu crio o Admin Master do Django (Local ou Remoto)?**
> R: Logicamente você precisa entrar virtualmente num terminal do backend, é super simples:
```bash
docker exec -it neuro-backend python manage.py createsuperuser
# Se for no VPS de produção, mudamos o nome do container, portanto é:
# docker exec -it neuro-backend-prod python manage.py createsuperuser
```

**3. Como aplico as Makemigrations via terminal?**
> R: Em Desenvolvimento, a qualquer momento sem desligar o Docker:
```bash
docker exec -it neuro-backend python manage.py makemigrations
```

**4. Como leio os Logs se está tudo travado e eu apaguei minha tela?**
> R: Siga os containers rodando por baixo dos panos (Útil na Produção e Local):
```bash
# Local
docker compose logs -f --tail 100

# VPS
docker compose -f docker-compose.prod.yml logs -f --tail 100
```

Seu repositório profissional e altamente escalonável está pronto para dominar os mercados.
