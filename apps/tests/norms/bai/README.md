# Normas do BAI (Beck Anxiety Inventory)

## Arquivos neste diretório

- `classification.csv` — Faixas de classificação do escore bruto (Beck et al., 1988)
- `t_score_lookup.csv` — Tabela de conversão de escore bruto para escore T da amostra geral (18-90 anos)

## Faixas de classificação atuais

| Escore Bruto | Classificação | Descrição |
|---|---|---|
| 0–10 | Mínimo | Nível mínimo de ansiedade |
| 11–19 | Leve | Nível brando de ansiedade |
| 20–30 | Moderado | Nível moderado de ansiedade |
| 31–63 | Grave | Nível severo de ansiedade |

## Referência

Beck, A. T., Epstein, N., Brown, G., & Steer, R. A. (1988). An inventory for measuring clinical anxiety: Psychometric properties. *Journal of Consulting and Clinical Psychology, 56*(6), 893–897.

## Status atual

O sistema já usa `t_score_lookup.csv` como fonte normativa oficial para converter escore bruto em escore T.

## Notas para atualização futura

Quando a tabela normativa oficial por escore T, percentil e intervalo de confiança estiver disponível:

1. Expandir `t_score_lookup.csv` com colunas adicionais como `percentile`, `ci_lower` e `ci_upper`, se a norma oficial disponibilizar esses campos
2. Atualizar o cálculo de percentil para usar lookup direto, em vez de aproximação a partir do escore T
3. Atualizar o intervalo de confiança para usar valores normativos publicados
