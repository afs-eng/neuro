# Análise Comparativa: Implementação do BAI

## Estrutura Final Criada

```
apps/tests/bai/
├── __init__.py           # BAIModule(BaseTestModule) + registro
├── constants.py          # Constantes: 21 itens, faixas, opções de resposta
├── schemas.py            # Pydantic (API) + Dataclasses (interno)
├── validators.py         # Validação de entrada (API + módulo)
├── calculators.py        # BAICalculator: escores, tabelas, gráficos
├── classifiers.py        # BAIClassifier: classificação por faixas
├── interpreters.py       # Geração de texto clínico
└── charts.py             # BAIChartBuilder: 3 gráficos (perfil, curva, distribuição)

apps/tests/norms/bai/
├── README.md             # Documentação das normas
├── classification.csv    # Faixas de classificação (Beck et al., 1988)
└── t_score_lookup.csv    # Tabela normativa oficial de conversão bruto -> T
```

## Origem dos Arquivos

| Arquivo | Origem | Adaptações |
|---------|--------|------------|
| `__init__.py` | Novo | Integra com `BaseTestModule` do sistema |
| `constants.py` | `bai_module/apps/tests/bai/constants.py` | Sem alterações |
| `schemas.py` | Novo + `bai_module` | Pydantic para API + Dataclasses para módulo |
| `validators.py` | `bai_module/apps/tests/bai/validators.py` | Adicionada função para API |
| `calculators.py` | `bai_module/apps/tests/bai/calculators.py` | Adaptado para `TestContext` e lookup normativo oficial |
| `classifiers.py` | `bai_module/apps/tests/bai/classifiers.py` | Sem alterações |
| `interpreters.py` | `bai_module/apps/tests/bai/interpreters.py` | Adicionadas funções auxiliares |
| `charts.py` | `bai_module/apps/tests/bai/charts.py` | Sem alterações |

## Vantagens da Estrutura `bai_module`

### ✅ Pontos Fortes

1. **Separação clara de responsabilidades**
   - `calculators.py`: cálculo puro
   - `classifiers.py`: classificação normativa
   - `interpreters.py`: texto clínico
   - `charts.py`: visualização

2. **Suporte a escore T e percentil**
   - Escore T por tabela normativa oficial e percentil derivado do T-score

3. **Geração de gráficos automática**
   - 3 gráficos: perfil, curva normativa, distribuição
   - Útil para frontend e laudos

4. **Tabelas estruturadas**
   - `summary_table`: resumo do escore
   - `items_table`: análise item a item
   - `distribution_table`: estatísticas das respostas
   - `classification_table`: faixas de referência

5. **Validação robusta**
   - Checa itens duplicados
   - Checa itens inválidos
   - Checa valores fora da escala

6. **Preparado para evolução futura**
   - Intervalo de confiança
   - Estrutura pronta para percentil e IC por lookup
   - Estrutura para lookup por idade/sexo

### 🔄 Adaptações Necessárias para o Sistema

1. **Integração com `BaseTestModule`**
   - O `bai_module` original usava `BAIModule.run()` direto
   - Adaptado para `validate()`, `compute()`, `classify()`, `interpret()`

2. **Integração com `TestContext`**
   - O sistema usa `TestContext` para passar dados entre estágios
   - Adaptado `compute_from_dict()` no calculator

3. **Registro no `registry.py`**
   - Adicionado `register_test_module("bai", BAIModule())`

4. **Schema Pydantic para API**
   - Adicionado `BAIRawInput` para validação via Django Ninja

## Comparação com Outros Instrumentos do Sistema

| Característica | BAI | EPQ-J | BPA-2 |
|---|---|---|---|
| Arquivos | 8 | 7 | 8 |
| Gráficos | ✅ 3 | ❌ | ❌ |
| Escore T | ✅ (lookup oficial) | ❌ | ✅ |
| Percentil | ✅ (estimado) | ✅ | ✅ |
| Tabelas estruturadas | ✅ 4 | ❌ | ✅ |
| Classificação CSV | ✅ | ❌ (hardcoded) | ✅ |
| Interpretação textual | ✅ | ✅ | ✅ |

## Recomendações

### ✅ Manter
- Estrutura modular com separação de responsabilidades
- Geração de gráficos (diferencial para laudos)
- Tabelas estruturadas para frontend
- CSV de classificação (fácil manutenção)

### 🔧 Melhorias Futuras
1. Revisar percentil e intervalo de confiança assim que a norma oficial trouxer esses campos
2. Adicionar normas por idade e sexo quando disponíveis
3. Criar testes unitários para cada função de cálculo
4. Adicionar validação de consistência interna (ex: total_raw_score == soma dos itens)

### ⚠️ Atenção
- O `bai_module/` original pode ser removido (já migrado para `apps/tests/bai/`)
- Verificar se matplotlib está disponível no ambiente de produção
- Gráficos são salvos em `/tmp/bai_charts/` — configurar diretório persistente se necessário

## Status da Integração

- ✅ Arquivos criados e adaptados
- ✅ Módulo registrado no `registry.py`
- ✅ Regra de idade adicionada (18+ anos)
- ✅ Seed do instrumento na migração
- ✅ Schema da API criado (`BAISubmitIn`)
- ✅ Endpoints criados (`/bai/submit`, `/bai/result`)
- ✅ Instrumento adicionado à lista de auto-seed
- ✅ Tabela normativa oficial carregada de `t_score_lookup.csv`

## Próximos Passos para Produção

1. Rodar migrações: `uv run python manage.py migrate`
2. Testar submissão via API
3. Verificar geração de gráficos
4. Integrar frontend com endpoint
5. (Opcional) Substituir aproximações restantes por lookup completo de percentil e IC
