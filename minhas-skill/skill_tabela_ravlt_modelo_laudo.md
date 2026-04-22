# SKILL: Padronização de Tabela no Laudo – Modelo RAVLT

## Objetivo
Esta skill orienta a IA a gerar tabelas no laudo **exatamente no padrão visual do modelo aprovado**, evitando erros comuns de cabeçalho, alinhamento, quebra de texto, largura inadequada e distorção visual na exportação para `.docx`.

O foco principal é a tabela de desempenho do **RAVLT**, mas a mesma lógica pode ser aplicada a outras tabelas clínicas do sistema.

## Resultado esperado
A tabela final deve ficar com este padrão estrutural:

| Desempenho | A1 | A2 | A3 | A4 | A5 | B1 | A6 | A7 | R | ALT | RET | I.P. | I.R. |
|-----------|----|----|----|----|----|----|----|----|---|-----|-----|------|------|
| Média     | 4  | 6  | 7  | 8  | 8  | 4  | 7  | 7  | 10 | 12 | 1 | 1 | 0,88 |
| Mínimo    | 3  | 5  | 5  | 6  | 7  | 3  | 5  | 6  | 8  | 6  | 0,89 | 0,75 | 0,71 |
| Obtido    | 2  | 4  | 5  | 5  | 5  | 4  | 2  | 2  | 8  | 11 | 1 | 2 | 0,4 |

## Regra principal
A IA deve **reproduzir o modelo visual com fidelidade**, sem reinterpretar os títulos, sem abreviar de forma diferente e sem alterar a ordem das colunas.

## Estrutura obrigatória da tabela
A tabela deve ter **14 colunas**, nesta ordem exata:

```text
Desempenho | A1 | A2 | A3 | A4 | A5 | B1 | A6 | A7 | R | ALT | RET | I.P. | I.R.
```

As linhas devem seguir esta ordem:

```text
Média
Mínimo
Obtido
```

## Erros que a IA deve evitar

### 1. Cortar o primeiro caractere do cabeçalho
Este foi o erro identificado no laudo gerado anteriormente.

Erro incorreto:

```text
1 | 2 | 3 | 4 | 5 | 1 | 6 | 7 | [vazio] | LT | ET | .P. | .R.
```

Isso acontece quando o código remove o primeiro caractere do texto, por exemplo:

```python
header[1:]
```

ou qualquer transformação semelhante.

A IA **nunca** deve remover o primeiro caractere dos rótulos das colunas.

### 2. Alterar os nomes das colunas
A IA não deve trocar:

- `B1` por `1`
- `R` por vazio
- `ALT` por `LT`
- `RET` por `ET`
- `I.P.` por `.P.`
- `I.R.` por `.R.`

### 3. Quebrar o texto do cabeçalho em duas linhas
A IA não deve deixar o cabeçalho quebrado, como:

```text
Desem
penho
```

O ideal é manter `Desempenho` em uma única linha.

### 4. Aplicar largura insuficiente às colunas
Se a largura das colunas for pequena demais, o Word pode deformar visualmente a tabela. A IA deve prever largura suficiente para:

- `Desempenho`
- `ALT`
- `RET`
- `I.P.`
- `I.R.`

### 5. Desalinhar conteúdo
A IA não deve deixar:

- cabeçalho desalinhado à esquerda
- números com alinhamento inconsistente
- células sem centralização vertical

### 6. Mudar a ordem das colunas
A IA não deve reorganizar a tabela por lógica própria. A ordem deve ser sempre a mesma do modelo.

### 7. Mudar formatação decimal
A IA deve preservar vírgula decimal quando os dados estiverem em português:

- `0,88`
- `0,75`
- `0,71`
- `0,4`

Não converter automaticamente para ponto.

## Padrão visual obrigatório
A IA deve formatar a tabela com estas características:

### Cabeçalho
- Fundo verde claro ou verde suave
- Texto em negrito
- Centralizado horizontalmente e verticalmente
- Sem quebra automática de linha
- Fonte **Times New Roman**, tamanho **12**

### Primeira coluna
- Título: `Desempenho`
- Células com `Média`, `Mínimo` e `Obtido`
- Texto em negrito nas linhas de rótulo
- Pode receber preenchimento cinza muito claro para destacar os rótulos

### Corpo da tabela
- Números centralizados
- Alinhamento vertical ao centro
- Bordas finas e regulares
- Sem espaçamento extra antes ou depois do parágrafo
- Fonte **Times New Roman**, tamanho **12**

### Bordas
- Todas as bordas visíveis
- Traço fino e uniforme
- Sem bordas grossas ou irregulares

## Regra de fidelidade visual
Se houver conflito entre a interpretação da IA e o modelo visual de referência, a IA deve seguir **o modelo visual de referência**.

## Instruções específicas para geração em Python com `python-docx`
Ao gerar esta tabela em `.docx`, a IA deve seguir esta lógica:

### Cabeçalhos corretos
```python
headers = [
    "Desempenho", "A1", "A2", "A3", "A4", "A5",
    "B1", "A6", "A7", "R", "ALT", "RET", "I.P.", "I.R."
]
```

### Dados corretos
```python
data = [
    ["Média", "4", "6", "7", "8", "8", "4", "7", "7", "10", "12", "1", "1", "0,88"],
    ["Mínimo", "3", "5", "5", "6", "7", "3", "5", "6", "8", "6", "0,89", "0,75", "0,71"],
    ["Obtido", "2", "4", "5", "5", "5", "4", "2", "2", "8", "11", "1", "2", "0,4"],
]
```

### Regras técnicas obrigatórias
- Nunca usar `header[1:]`
- Nunca usar `lstrip()` nos rótulos do cabeçalho
- Nunca aplicar replace que remova a primeira letra
- Garantir que cada célula receba o texto completo
- Definir alinhamento central para todas as células, exceto quando houver necessidade clínica específica
- Zerar recuos do parágrafo dentro das células
- Remover espaçamento antes e depois do parágrafo
- Definir largura adequada da coluna `Desempenho`

## Checklist de validação antes de finalizar
A IA deve verificar, antes de concluir:

1. A tabela tem 14 colunas?
2. O cabeçalho está exatamente assim?

```text
Desempenho | A1 | A2 | A3 | A4 | A5 | B1 | A6 | A7 | R | ALT | RET | I.P. | I.R.
```

3. Nenhuma coluna perdeu a primeira letra?
4. `R` aparece visivelmente?
5. `ALT`, `RET`, `I.P.` e `I.R.` aparecem completos?
6. Os valores decimais estão com vírgula?
7. A fonte está em Times New Roman 12?
8. O cabeçalho está centralizado e em negrito?
9. A tabela está visualmente parecida com o modelo aprovado?
10. A primeira coluna está larga o suficiente para `Desempenho` sem quebra?

## Comportamento esperado da IA
Quando receber solicitação para gerar esta tabela, a IA deve:

1. Montar a tabela exatamente no padrão do modelo
2. Preservar os cabeçalhos integralmente
3. Preservar a ordem das colunas
4. Preservar a vírgula decimal
5. Ajustar largura e alinhamento para evitar deformação visual
6. Validar visualmente antes de concluir

## Prompt operacional para a IA
Use este bloco como instrução direta:

```text
Gere a tabela do RAVLT exatamente no modelo aprovado do laudo. Preserve integralmente os cabeçalhos: Desempenho, A1, A2, A3, A4, A5, B1, A6, A7, R, ALT, RET, I.P., I.R. Não remova o primeiro caractere de nenhuma coluna. Não altere a ordem. Não quebre o texto do cabeçalho. Use Times New Roman 12, cabeçalho em negrito, conteúdo centralizado, bordas finas e largura suficiente para manter a tabela limpa e legível no Word. Preserve os decimais com vírgula.
```

## Regra final
Se a saída gerada não estiver visualmente próxima do modelo aprovado, a IA deve considerar a tarefa incompleta e corrigir a tabela antes de finalizar.
