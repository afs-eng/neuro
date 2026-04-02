# Guia Oficial de Deploy na Vercel (Frontend Next.js)

Este documento detalha exatamente como configurar e hospedar o frontend do `NeuroAvalia` (`neuro-frontend`) na plataforma Vercel. 

> [!CAUTION]
> A Vercel hospedará **apenas o Frontend**. O servidor Django (Backend) deve estar no ar em outra plataforma (como Render ou Railway) antes de seguir este guia.

## 1. Importando o Projeto na Vercel

1. Faça login em [Vercel.com](https://vercel.com) com sua conta do Github.
2. Clique em **"Add New..."** e selecione **"Project"**.
3. Encontre o repositório `neuro` (o repositório completo) e clique em **"Import"**.

## 2. Configurações Iniciais da Build

> [!IMPORTANT]
> A etapa a seguir é **CRÍTICA**. O Vercel assumirá que o código está na raiz se você não especificar o "Root Directory".

Na tela "Configure Project":

1. Expanda a seção **"Project Settings"** (ou "Build and Output Settings").
2. No item **"Root Directory"**, clique em *Edit* e escolha a pasta `neuro-frontend`.
3. Os campos de *Framework Preset* mudarão sozinhos para "Next.js". Não precisa alterar o *Build Command* nem *Output Directory*.
4. Mantenha o *Install Command* com o padrão (`npm install`).

## 3. Configurando Variáveis de Ambiente

> [!WARNING]
> Sem estas variáveis, a aplicação não saberá se comunicar com o seu Backend e o Login (NextAuth) falhará silenciosamente!

Na mesma tela, expanda a aba **"Environment Variables"** e insira as seguintes chaves (uma por vez):

| Variable Name | Value a ser inserido | Descrição |
|:--------------|:---------------------|:----------|
| `NEXT_PUBLIC_API_URL` | `https://seu-backend.onrender.com` | A URL raiz pública da sua API (Render) |
| `INTERNAL_API_BASE_URL` | `https://seu-backend.onrender.com` | Usada pela Vercel em Server-Side para bater na API Django sem bater no Cors |
| `NEXTAUTH_URL` | `https://seu-frontend.vercel.app` | A URL temporária ou final que a Vercel vai te dar |
| `NEXTAUTH_SECRET` | `uma-chave-longa-e-secreta-qualquer` | Chave de Criptografia do Banco de Cookies |
| `NEXT_PUBLIC_APP_URL` | `https://seu-frontend.vercel.app` | Mesma URL do NextAuth (usada em links absolutos do app) |

*Nota sobre a URL Vercel*: Como você só vai saber o domínio oficial após o primeiro deploy, é normal gerar um domínio automático. Após o deploy finalizar, **copie o domínio final** (ex: `neuro-g1k3d.vercel.app`), vá em *Settings > Environment Variables* na Vercel e atualize `NEXTAUTH_URL` e `NEXT_PUBLIC_APP_URL`. Depois, faça um Redeploy.

## 4. O Lado do Django (Backend / Render)

Depois do Vercel subir seu site em um domínio (exemplo: `https://meu-neuro-front.vercel.app`), o Django precisa permitir que esse domínio faça acesso cruzado (CORS).

No **Painel do Render** (onde o backend Django está hospedado):

1. Vá ao serviço do Backend.
2. Acesse **"Environment"**.
3. Encontre a variável `FRONTEND_BASE_URL` ou crie-a.
4. Coloque como valor exatamente o domínio da Vercel: `https://meu-neuro-front.vercel.app` (Sem barra final e com HTTPS).
5. Salve. O Render vai reiniciar a API.

## 5. Teste Prático

Após os deployments da Vercel e do Render terminarem:
1. Acesse sua URL da Vercel no navegador.
2. Você deve ver a tela de Login. 
3. Tente fazer o acesso. Se acessar a Dashboard com sucesso, o fluxo Next.js ⟷ Django CORS está rodando em perfeita harmonia!
