# SKILL: Gerar gráfico BPA-2 para laudo neuropsicológico

## Objetivo
Implementar, no sistema de laudos, a geração automática do gráfico do BPA-2 em formato de imagem PNG, com estilo visual semelhante ao modelo fornecido pelo usuário, para posterior inserção no laudo DOCX.

## Contexto
O sistema possui testes estruturados, com cálculo e classificação separados da renderização visual. O gráfico do BPA-2 deve usar os dados já processados do teste, sem recalcular normas, percentis ou classificações.

A renderização do gráfico deve ficar desacoplada da lógica do teste.

## Regra principal
O gráfico deve:
- receber os dados já calculados do BPA-2
- gerar uma imagem PNG em alta resolução
- manter estilo padronizado
- ser reutilizável em laudos
- não depender do frontend para exportação final

## Stack obrigatória
- Python
- Matplotlib
- Integração com Django
- Saída final em PNG
- Inserção posterior em DOCX com `python-docx`

## Estrutura recomendada
```text
apps/
  reports/
    charts/
      __init__.py
      base.py
      styles.py
      bpa2_chart.py
```

## Arquivo principal
Criar o arquivo:

`apps/reports/charts/bpa2_chart.py`

## Função principal esperada
Criar uma função pública com esta assinatura ou equivalente:

```python
def gerar_grafico_bpa(
    output_path,
    atencao_concentrada,
    atencao_dividida,
    atencao_alternada,
    atencao_geral,
    titulo="BPA - BATERIA PSICOLÓGICA PARA AVALIAÇÃO DA ATENÇÃO",
    dpi=300,
) -> str:
    ...
```

## Formato esperado dos dados de entrada
Cada domínio deve receber um dicionário com esta estrutura:

```python
{
    "maximo": 119,
    "medio": 78,
    "minimo": 43,
    "bruto": 58,
    "percentil": 25,
}
```

## Séries obrigatórias
O gráfico deve conter exatamente estas quatro séries:
- ATENÇÃO CONCENTRADA
- ATENÇÃO DIVIDIDA
- ATENÇÃO ALTERNADA
- ATENÇÃO GERAL

## Categorias obrigatórias no eixo X
O gráfico deve conter exatamente estas cinco categorias:
- Escore Máximo
- Escore Médio
- Escore Mínimo
- Escore Bruto
- Percentil Obtido

## Estilo visual obrigatório
A implementação deve seguir este padrão visual:

### Fundo
- fundo geral em cinza claro
- fundo da área do gráfico também em cinza claro

### Título
- texto em verde
- centralizado
- em negrito
- estilo serifado
- semelhante ao modelo enviado pelo usuário

### Barras
- gráfico de barras agrupadas
- 4 barras por grupo
- sem contorno visível
- com as seguintes cores aproximadas:
  - atenção concentrada: laranja
  - atenção dividida: amarelo
  - atenção alternada: verde
  - atenção geral: marrom/laranja escuro

### Rótulos numéricos
- exibir valor acima de cada barra
- centralizado
- cor escura
- tamanho legível

### Eixo Y
- mostrar grade horizontal
- sem bordas externas
- escala automática com arredondamento visual bonito

### Legenda
- posicionada abaixo do gráfico
- centralizada
- quatro itens em linha
- sem caixa ao redor

## Restrições técnicas
A IA não deve:
- recalcular percentis
- recalcular classificação
- puxar dados diretamente do banco dentro da função de renderização
- depender de JavaScript para gerar a imagem final do laudo
- misturar interpretação textual com geração de gráfico

## Regras de arquitetura
A função de renderização:
- recebe apenas dados prontos
- gera apenas imagem
- retorna o caminho do arquivo salvo

A função não deve conter:
- regras normativas do BPA-2
- lookup de CSV
- interpretação clínica
- regras de negócio do teste

## Regras de qualidade
A implementação deve:
- criar automaticamente a pasta de saída, se não existir
- usar `bbox_inches="tight"`
- usar `facecolor` do gráfico ao salvar
- fechar a figura com `plt.close(fig)`
- permitir reutilização em outros relatórios

## Saída esperada
A função deve retornar uma string com o caminho final do PNG gerado.

Exemplo:
```python
"/tmp/grafico_bpa.png"
```

## Exemplo de uso esperado
```python
gerar_grafico_bpa(
    output_path="/tmp/grafico_bpa.png",
    atencao_concentrada={
        "maximo": 119,
        "medio": 78,
        "minimo": 43,
        "bruto": 58,
        "percentil": 25,
    },
    atencao_dividida={
        "maximo": 116,
        "medio": 71,
        "minimo": 38,
        "bruto": 77,
        "percentil": 50,
    },
    atencao_alternada={
        "maximo": 119,
        "medio": 89,
        "minimo": 54,
        "bruto": 94,
        "percentil": 60,
    },
    atencao_geral={
        "maximo": 353,
        "medio": 238,
        "minimo": 152,
        "bruto": 229,
        "percentil": 40,
    },
)
```

## Integração com o laudo
Depois de gerar o gráfico, ele deve ser inserido no DOCX via `python-docx`, usando `add_picture()`.

A legenda do gráfico, no laudo final, deve seguir o padrão do sistema:
- fonte Times New Roman
- tamanho 8
- itálico
- posicionada abaixo do gráfico

## Critérios de aceite
A tarefa será considerada concluída quando:
1. o arquivo `bpa2_chart.py` existir
2. a função gerar o PNG corretamente
3. o gráfico tiver o mesmo tipo visual do modelo do usuário
4. a função não depender do frontend
5. a imagem puder ser inserida no laudo DOCX sem ajustes manuais

## Entrega esperada da IA
A IA deve entregar:
- o código completo do arquivo `apps/reports/charts/bpa2_chart.py`
- imports corretos
- função pronta para uso
- exemplo de chamada
- código limpo e reutilizável
