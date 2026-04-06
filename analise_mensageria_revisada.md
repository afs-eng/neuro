# Análise Revisada: Mensageria na Anamnese (E-mail + WhatsApp)

> **Projeto:** NeuroAvalia  
> **Módulo:** `apps/anamnesis` + `apps/messaging`  
> **Data:** 2026-04-06

## Visão Geral

A análise original está bem estruturada, tecnicamente consistente e adequada como base de decisão arquitetural. Ela acerta principalmente em três pontos:

1. identifica corretamente o estado atual da implementação;
2. separa bem problemas técnicos de decisões de produto;
3. propõe um caminho coerente com a stack atual do projeto, baseada em Django, API e Docker.

O diagnóstico do estado atual está correto ao apontar que o envio de e-mail ocorre de forma síncrona e que o fluxo de WhatsApp atual não realiza envio automático, apenas gera um link `wa.me`. Esse mapeamento está alinhado com a realidade operacional do sistema e ajuda a diferenciar claramente o que já funciona do que ainda não está pronto para produção.

## Pontos Fortes da Análise

### 1. Diagnóstico técnico correto

A análise reconhece adequadamente que o e-mail atual utiliza envio síncrono no request HTTP, o que pode causar timeout, lentidão perceptível ao usuário e erro 500 em caso de falha do provedor SMTP.

Também identifica corretamente que o WhatsApp atual não é uma integração real, mas apenas um gerador de link para envio manual.

Esses dois pontos são críticos e foram bem destacados na análise original.

### 2. Boa separação entre lacunas e opções de solução

A tabela de lacunas ficou clara, objetiva e priorizou corretamente os pontos com maior impacto, especialmente:

- e-mail síncrono;
- ausência de envio automático no WhatsApp;
- falta de retry;
- ausência de visibilidade mais robusta do status de entrega.

Isso facilita bastante a tomada de decisão técnica.

### 3. Recomendação compatível com a stack do projeto

A proposta de usar **Resend** para e-mail e **Evolution API** para WhatsApp é plausível para o contexto do projeto, principalmente porque:

- reduz a complexidade de implementação inicial;
- combina bem com uma arquitetura em containers;
- evita dependências mais pesadas logo no início;
- permite um avanço relativamente rápido do módulo de mensageria.

## Ajustes Necessários na Análise

Embora a direção geral esteja correta, alguns pontos precisam ser refinados para que o documento fique mais sólido do ponto de vista de arquitetura.

### 1. API HTTP não significa processamento assíncrono

A análise dá a entender que, por usar uma API HTTP em vez de SMTP, o envio deixaria de bloquear a request. Isso precisa ser corrigido.

Mesmo usando Resend por HTTP, se a chamada acontecer dentro do ciclo da requisição Django, o comportamento ainda continua síncrono do ponto de vista da aplicação. O request só termina depois que a API externa responder.

Portanto, o correto é dizer:

- usar Resend tende a simplificar a integração e melhorar a confiabilidade em comparação com SMTP direto;
- porém, isso **não elimina o bloqueio da request** por si só;
- para robustez real, o envio deve futuramente ir para fila, tarefa assíncrona ou job em background.

### 2. Falta separar melhor MVP de produção robusta

A análise já propõe a automação completa do WhatsApp, mas ainda não diferencia claramente o que seria uma entrega inicial viável do que seria uma solução mais madura.

A recomendação mais saudável para o projeto é organizar a evolução em fases.

#### Fase 1 — MVP funcional
- E-mail com Resend
- WhatsApp ainda via `wa.me`, mas com UX melhorada
- Persistência básica do status de envio

#### Fase 2 — Robustez operacional
- Registro detalhado de tentativas
- Retry controlado
- Webhooks de status no e-mail
- Histórico de falhas

#### Fase 3 — Automação de WhatsApp
- Integração com Evolution API
- Atualização de status real de entrega
- Possível envio de anexos ou mídia

#### Fase 4 — Escala/compliance maior
- Avaliação de WhatsApp Cloud API oficial
- Política mais forte de observabilidade e auditoria

Essa separação deixa a decisão mais estratégica e evita implementar complexidade cedo demais.

### 3. Falta uma modelagem explícita do domínio de mensageria

A análise fala bem dos providers, mas ainda não formaliza como o sistema deve representar internamente cada envio.

Para o projeto crescer de forma escalável, o ideal é que cada tentativa de envio registre campos como:

- `channel`: `email` ou `whatsapp`
- `provider`: `smtp`, `resend`, `wa_me`, `evolution`, `meta`
- `status`: `pending`, `queued`, `sent`, `delivered`, `read`, `failed`
- `external_id`
- `attempt_count`
- `last_error`
- `sent_at`
- `delivered_at`
- `read_at`

Esse desenho facilita auditoria, rastreamento, dashboard e reprocessamento.

### 4. Risco operacional do Evolution API precisa ser descrito com mais cautela

A análise apresenta o Evolution API como recomendação principal para WhatsApp, o que pode fazer sentido em contexto de operação moderada, mas o texto precisa ser mais cuidadoso.

Uma formulação melhor seria:

- é uma opção interessante para automação rápida e custo reduzido;
- combina bem com infraestrutura Docker/self-hosted;
- pode atender bem operações pequenas e médias;
- porém envolve maior sensibilidade operacional do que soluções oficiais;
- deve ser adotada com consciência dos riscos de manutenção, disponibilidade e política da plataforma.

Esse ajuste evita passar uma sensação de “risco quase zero”, que não é a forma mais segura de documentar a decisão.

### 5. Falta prever estratégia de fallback

A análise ficaria mais completa se previsse um fluxo de contingência entre canais.

Exemplo recomendado:

1. sistema tenta enviar o convite por e-mail;
2. se não houver abertura ou ação em determinado período, o sistema sugere reenvio por WhatsApp;
3. se WhatsApp automático não estiver disponível, gera link `wa.me` com mensagem pronta;
4. todas as tentativas ficam registradas no histórico do convite.

Essa lógica conversa bem com o fluxo real de anamnese e melhora a operação sem exigir automação máxima desde o início.

## Recomendação Final Revisada

A direção geral da análise está correta, mas a execução recomendada deve ser mais gradual.

### Recomendação prática para o projeto

#### E-mail
Adotar **Resend** como provedor principal de e-mail transacional.

Motivos:
- integração simples;
- suporte a HTML;
- melhor experiência de monitoramento;
- webhooks disponíveis;
- menor atrito de setup em comparação com alternativas mais burocráticas.

#### WhatsApp
Não iniciar imediatamente com automação completa, a menos que isso já seja uma dor operacional comprovada.

Ordem sugerida:
1. manter `wa.me` no curto prazo, com UX melhorada;
2. medir uso real e gargalos operacionais;
3. evoluir para Evolution API somente se o envio manual virar problema frequente.

### Estratégia recomendada por fase

| Fase | Objetivo | Solução |
|------|----------|---------|
| 1 | Colocar mensageria em operação confiável | Resend + `wa.me` |
| 2 | Melhorar rastreabilidade | status, logs, tentativas, webhooks |
| 3 | Automatizar WhatsApp | Evolution API |
| 4 | Escalar com mais previsibilidade | avaliar Cloud API oficial |

## Decisão Arquitetural Sugerida

A recomendação final mais equilibrada para o projeto é:

- **adotar Resend para e-mail desde já;**
- **manter o WhatsApp inicialmente com link `wa.me`;**
- **estruturar o módulo de mensageria para suportar múltiplos providers;**
- **implementar automação de WhatsApp apenas na etapa seguinte, se houver ganho operacional real;**
- **preparar o backend para persistir status, tentativas e falhas desde o início.**

Essa abordagem reduz risco, acelera entrega e mantém o sistema preparado para crescer sem retrabalho estrutural.

## Conclusão

A análise original é boa e pode ser usada como base técnica. A principal melhoria necessária não está na direção da solução, mas no grau de maturidade da recomendação.

Ela está correta ao apontar os problemas do cenário atual e ao sugerir modernização do módulo de mensageria. No entanto, para o contexto do projeto, a melhor decisão é seguir uma implementação em camadas:

- primeiro resolver o e-mail de forma sólida;
- depois estruturar persistência e observabilidade;
- por fim automatizar o WhatsApp quando isso fizer sentido operacional.

Em análise arquitetural, essa é a alternativa mais segura, escalável e compatível com o estágio atual do sistema.
