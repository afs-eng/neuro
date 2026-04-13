# SKILL — Geração de Tabelas e Gráficos em Laudos `.docx`

## Objetivo
Permitir que a IA do sistema gere laudos neuropsicológicos em `.docx` com:
- tabelas profissionais e padronizadas;
- gráficos inseridos no documento;
- legendas, títulos e organização visual compatível com Microsoft Word;
- layout clínico limpo, técnico e pronto para revisão.

Essa skill deve ser usada no módulo de geração do laudo final, após a consolidação dos resultados dos testes e da redação clínica.

## Princípio geral
A IA **pode gerar o conteúdo e a estrutura** do laudo, mas a montagem visual final do `.docx` deve ser feita pelo sistema.

### Regra central
Separar a geração em 3 camadas:

1. **Camada clínica**
   - gera os textos interpretativos;
   - organiza as seções do laudo;
   - define onde entram tabelas e gráficos.

2. **Camada estrutural**
   - gera tabelas nativas do Word;
   - insere títulos, subtítulos, numeração e legendas;
   - controla alinhamento, largura de colunas, tipografia e espaçamento.

3. **Camada visual**
   - gera gráficos a partir dos resultados dos testes;
   - exporta os gráficos como imagem;
   - insere as imagens no `.docx` com tamanho e posição padronizados.

## Regra de arquitetura recomendada
A IA não deve tentar “desenhar” o `.docx` inteiro apenas com texto.
O sistema deve usar a IA para decidir **o que mostrar** e o backend para definir **como montar**.

### Fluxo ideal
1. Receber os dados do paciente e os resultados dos testes.
2. Organizar os resultados por domínio.
3. Gerar o texto do laudo.
4. Montar as tabelas em formato estruturado.
5. Gerar os gráficos em imagem.
6. Inserir tabelas e gráficos no `.docx` nas posições corretas.
7. Exportar o documento final.

## O que a IA deve ser capaz de fazer
A IA deve:
- identificar quais tabelas precisam existir;
- identificar quais gráficos fazem sentido em cada teste;
- devolver estrutura de dados organizada para o backend renderizar;
- sugerir título, legenda e posição de cada elemento;
- manter o padrão visual do laudo.

A IA não deve:
- inventar valores;
- converter texto livre em tabela sem base de dados estruturada;
- criar gráficos com escalas erradas;
- usar imagens decorativas;
- duplicar informação desnecessariamente;
- comprometer legibilidade do documento.

## Padrão visual do `.docx`
O documento deve seguir aparência profissional, clínica e compatível com Word no Windows.

### Formatação sugerida
- Fonte principal: Times New Roman ou Arial
- Corpo do texto: 11 ou 12 pt
- Títulos de seção: 12 ou 14 pt em negrito
- Espaçamento entre linhas: 1,15 ou 1,5
- Alinhamento do corpo: justificado
- Tabelas centralizadas ou alinhadas ao conteúdo
- Legendas de tabelas e gráficos com numeração sequencial
- Margens padrão A4

## Tabelas no `.docx`

### Regra principal
As tabelas devem ser **nativas do Word**, não imagens.

### Vantagens
- melhor compatibilidade com Word;
- melhor impressão;
- edição posterior facilitada;
- aparência mais profissional;
- menor risco de distorção visual.

### Padrão de tabela
Cada tabela deve conter:
- título ou legenda;
- cabeçalho bem definido;
- colunas proporcionais;
- alinhamento consistente;
- bordas discretas;
- conteúdo técnico e legível.

### Legenda
Padrão:
- `Tabela 1. Resultados do WISC-IV`
- `Tabela 2. Resultados da BPA-2`
- `Tabela 3. Resultados do RAVLT`

A legenda pode ficar acima ou abaixo da tabela, mas o sistema deve manter um padrão fixo em todo o documento.

## Tabelas recomendadas por teste

### 1. WISC-IV / WAIS-III / WASI
Criar tabelas como:

#### Tabela de índices
Colunas sugeridas:
- Índice
- Pontuação
- Classificação

#### Tabela de subtestes
Colunas sugeridas:
- Subteste
- Escore Obtido
- Classificação

### 2. BPA-2
Colunas sugeridas:
- Domínio
- Escore Bruto
- Percentil
- Classificação

Linhas sugeridas:
- Atenção Concentrada
- Atenção Dividida
- Atenção Alternada
- Atenção Geral

### 3. RAVLT
Colunas sugeridas:
- Itens
- Pontos Brutos
- Média
- Desvio Padrão
- Percentil
- Classificação

Linhas sugeridas:
- A1
- A2
- A3
- A4
- A5
- B1
- A6
- A7
- R
- ALT
- RET
- I.P.
- I.R.

### 4. FDT
#### Tabela de processos automáticos e controlados
Colunas sugeridas:
- Processo
- Tempo Médio
- Tempo Obtido
- Erros
- Percentil
- Classificação

Linhas sugeridas:
- Leitura
- Contagem
- Escolha
- Alternância
- Inibição
- Flexibilidade

### 5. ETDAH-AD / ETDAH-PAIS
Colunas sugeridas:
- Escala
- Pontos Brutos
- Média
- Percentil
- Classificação

### 6. SRS-2
Colunas sugeridas:
- Escala
- Pontuação Bruta
- Escore-T ou Norma
- Classificação

Linhas sugeridas:
- Percepção Social
- Cognição Social
- Comunicação Social
- Motivação Social
- Padrões Restritos e Repetitivos
- Comunicação e Interação Social
- Escore Total

### 7. EPQ-J / BFP / IPHEXA / BAI / EBADEP / SCARED
Gerar tabela de resultados conforme a lógica do instrumento.

## Regras de montagem das tabelas
O sistema deve:
- ajustar largura das colunas automaticamente;
- quebrar linha dentro da célula quando necessário;
- evitar colunas excessivamente estreitas;
- manter cabeçalho repetível em caso de quebra de página;
- evitar uma tabela começar em uma página e ficar ilegível na outra;
- impedir que legendas se separem do elemento correspondente.

## Gráficos no `.docx`

### Regra principal
Os gráficos devem ser gerados como **imagem** e inseridos no documento.

### Motivo
Essa estratégia é mais estável do que tentar criar gráficos editáveis diretamente no Word.

### Formato recomendado
- PNG para gráficos com texto e linhas finas;
- resolução adequada para impressão;
- fundo branco;
- alta nitidez.

## Tipos de gráficos recomendados

### 1. WISC-IV / WAIS / WASI
**Gráfico de barras** com índices principais.

Eixos sugeridos:
- eixo X: ICV, IOP, IMO, IVP, QIT
- eixo Y: pontuação composta

### 2. BPA-2
**Gráfico de barras** comparando:
- Atenção Concentrada
- Atenção Dividida
- Atenção Alternada
- Atenção Geral

### 3. RAVLT
**Gráfico de linha** mostrando a curva de aprendizagem.

Pontos sugeridos:
- A1, A2, A3, A4, A5, B1, A6, A7

Opcionalmente incluir linhas de referência para:
- desempenho esperado;
- desempenho mínimo.

### 4. FDT
Dois gráficos separados:
- Gráfico 1: Processos Automáticos
  - Leitura
  - Contagem
- Gráfico 2: Processos Controlados
  - Escolha
  - Alternância
  - Inibição
  - Flexibilidade

### 5. SRS-2
**Gráfico de barras** com os domínios e escores T.

### 6. IPHEXA / BFP
**Gráfico radar** apenas quando o teste exigir comparação entre fatores de personalidade.

## Regras para os gráficos
Os gráficos devem:
- ter título claro;
- usar rótulos legíveis;
- não ficar visualmente poluídos;
- respeitar escala coerente com o instrumento;
- manter padrão visual uniforme em todo o laudo;
- evitar excesso de cores ou elementos decorativos.

## Legendas dos gráficos
Padrão sugerido:
- `Gráfico 1. Índices do WISC-IV`
- `Gráfico 2. Perfil atencional no BPA-2`
- `Gráfico 3. Curva de aprendizagem no RAVLT`
- `Gráfico 4. FDT – Processos Automáticos`
- `Gráfico 5. FDT – Processos Controlados`

## Posição dos gráficos
Regra recomendada:
- inserir o gráfico logo após a tabela correspondente ou após o parágrafo interpretativo do teste;
- manter proximidade entre tabela, gráfico e interpretação;
- evitar jogar o gráfico para páginas muito distantes da seção.

## Estrutura de saída ideal para a IA
A IA deve devolver uma estrutura organizada para o backend, por exemplo:

```json
{
  "elementos_docx": [
    {
      "tipo": "tabela",
      "titulo": "Tabela 1. Resultados do BPA-2",
      "secao": "ATENÇÃO",
      "colunas": ["Domínio", "Escore Bruto", "Percentil", "Classificação"],
      "linhas": [
        ["Atenção Concentrada", "57", "10", "Inferior"],
        ["Atenção Dividida", "45", "25", "Média Inferior"],
        ["Atenção Alternada", "63", "30", "Média Inferior"],
        ["Atenção Geral", "165", "20", "Média Inferior"]
      ]
    },
    {
      "tipo": "grafico",
      "titulo": "Gráfico 2. Perfil atencional no BPA-2",
      "secao": "ATENÇÃO",
      "subtipo": "barras",
      "labels": ["AC", "AD", "AA", "AG"],
      "valores": [57, 45, 63, 165],
      "arquivo": "grafico_bpa2.png"
    }
  ]
}
```

## Regras de backend para montar o `.docx`
O backend deve:
- usar biblioteca apropriada para Word, como `python-docx`;
- inserir tabelas como objetos nativos;
- gerar gráficos com biblioteca como `matplotlib` ou equivalente;
- salvar gráficos temporariamente em PNG;
- inserir a imagem no documento com largura padronizada;
- aplicar estilos consistentes em todas as páginas;
- garantir compatibilidade com Word no Windows.

## Regra de compatibilidade
O arquivo final deve abrir corretamente em:
- Microsoft Word no Windows;
- LibreOffice, quando possível;
- visualizadores padrão de `.docx`.

## Regras de qualidade clínica
Tabelas e gráficos não devem ser meramente decorativos.
Cada elemento visual deve ter função clínica real, como:
- resumir resultados;
- facilitar leitura do médico ou responsável;
- destacar discrepâncias entre domínios;
- tornar a conclusão mais inteligível.

## Estratégia ideal por tipo de caso

### Casos infantis
Dar prioridade para:
- tabelas claras;
- gráficos simples de barras;
- organização limpa;
- destaque em atenção, funções executivas e aprendizagem.

### Casos adultos
Dar prioridade para:
- tabelas resumidas e elegantes;
- gráficos de índices cognitivos;
- gráficos de funções executivas;
- integração com escalas emocionais e de personalidade.

## Erros que a IA deve evitar
- gerar gráfico sem dados completos;
- usar legenda incorreta;
- misturar percentil com escore bruto no mesmo gráfico sem explicação;
- repetir a mesma informação em tabela e gráfico sem necessidade clínica;
- usar gráfico radar para qualquer teste sem justificativa;
- criar tabela muito longa sem quebra planejada;
- quebrar coerência visual entre seções.

## Regra final
A IA deve pensar o `.docx` como um documento técnico-profissional.
As tabelas devem ser nativas, legíveis e editáveis.
Os gráficos devem ser imagens limpas, precisas e clinicamente úteis.
O resultado final deve parecer um laudo produzido em padrão profissional real, e não um documento improvisado.
