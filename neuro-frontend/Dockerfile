# ============================================================
# NeuroAvalia — Frontend Dockerfile (Multi-stage: dev + prod)
# ============================================================

FROM node:20-alpine AS base

RUN apk add --no-cache libc6-compat
WORKDIR /app

# --------------------------------------------------------
# Stage 1: Dev (hot-reload)
# --------------------------------------------------------
FROM base AS dev

COPY package.json package-lock.json* ./
RUN npm install

COPY . .

EXPOSE 3000
ENV PORT 3000
ENV HOSTNAME "0.0.0.0"

CMD ["npm", "run", "dev"]

# --------------------------------------------------------
# Stage 2: Deps (instalacao de dependencias)
# --------------------------------------------------------
FROM base AS deps

COPY package.json package-lock.json* ./
RUN \
  if [ -f package-lock.json ]; then npm ci; \
  else npm install; \
  fi

# --------------------------------------------------------
# Stage 3: Builder (build de producao)
# --------------------------------------------------------
FROM base AS builder

WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .

ARG NEXT_PUBLIC_API_BASE_URL
ENV NEXT_PUBLIC_API_BASE_URL=$NEXT_PUBLIC_API_BASE_URL
ENV BUILD_STANDALONE=true

RUN npm run build

# --------------------------------------------------------
# Stage 4: Prod (standalone otimizado)
# --------------------------------------------------------
FROM base AS prod

WORKDIR /app

ENV NODE_ENV production
ENV NEXT_TELEMETRY_DISABLED 1

RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs

COPY --from=builder /app/public ./public
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static

USER nextjs

EXPOSE 3000
ENV PORT 3000
ENV HOSTNAME "0.0.0.0"

CMD ["node", "server.js"]
