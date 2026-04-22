# SKILL: Interpretação do FDT para o Sistema de Laudos

## Objetivo
Esta skill orienta a IA a redigir a **interpretação clínica do Teste dos Cinco Dígitos (FDT)** no mesmo padrão técnico e descritivo utilizado nos laudos do sistema, mantendo a estrutura do modelo aprovado e incluindo, quando necessário, **parágrafos específicos sobre erros**.

A redação deve ser clínica, coesa, técnica e natural, sem tabelas, sem travessões longos e com fechamento obrigatório em **“Em análise clínica”**.

## Finalidade do texto
A IA deve gerar um texto interpretativo sobre:
- velocidade de processamento
- automatização
- controle inibitório
- alternância atencional
- flexibilidade cognitiva
- precisão da resposta
- monitoramento executivo
- presença ou ausência de erros

## Modelo-base de referência
A estrutura deve seguir este raciocínio:

1. **Apresentação do instrumento e do que ele avalia**
2. **Interpretação dos processos automáticos**
3. **Interpretação dos processos controlados**
4. **Parágrafo específico sobre erros**
5. **Síntese clínica final iniciada por “Em análise clínica”**

## Entradas esperadas pelo sistema
A skill deve considerar que o sistema fornecerá, para cada etapa do FDT:

- classificação de **Leitura**
- classificação de **Contagem**
- classificação de **Escolha**
- classificação de **Alternância**
- classificação de **Inibição**
- classificação de **Flexibilidade**
- número de erros em **Leitura**
- número de erros em **Contagem**
- número de erros em **Escolha**
- número de erros em **Alternância**

## Regra central da interpretação
A IA deve usar a classificação já calculada pelo sistema como fonte principal. A redação não deve reinventar critérios nem alterar o sentido do resultado.

## Estrutura fixa obrigatória

### Parágrafo 1: apresentação do instrumento
A IA deve iniciar explicando o que é o FDT e quais funções ele investiga.

### Modelo
```text
A avaliação das funções executivas de [NOME] incluiu a aplicação do Teste dos Cinco Dígitos (FDT), instrumento destinado à investigação da velocidade de processamento, controle inibitório, alternância atencional e flexibilidade cognitiva, contemplando processos automáticos e controlados.
```

## Parágrafo 2: processos automáticos
Este parágrafo deve integrar **Leitura** e **Contagem**.

### Quando ambos estiverem preservados
```text
Nos processos automáticos, os desempenhos em Leitura e Contagem foram classificados como sem indicativo de déficit, com execução [precisa/adequada] e [sem erros ou com baixa ocorrência de erros], sugerindo automatização preservada e velocidade de processamento adequada em tarefas de baixa demanda executiva.
```

### Quando houver prejuízo em um ou ambos
```text
Nos processos automáticos, observou-se [prejuízo/rebaixamento/dificuldade] em [Leitura, Contagem ou ambas], indicando lentificação no processamento de estímulos altamente automatizados e possível redução da eficiência em tarefas de baixa complexidade executiva. Esse padrão sugere comprometimento na rapidez de resposta e menor fluidez no processamento automático.
```

### Quando houver perfil misto
```text
Nos processos automáticos, [NOME] apresentou desempenho [preservado/adequado] em [etapa preservada], enquanto [etapa rebaixada] mostrou [indicativo de déficit/rebaixamento], sugerindo oscilação na eficiência do processamento automático. Esse perfil indica que a automatização não se encontra homogênea entre as tarefas de leitura e contagem.
```

## Parágrafo 3: processos controlados
Este parágrafo deve integrar **Escolha**, **Alternância**, **Inibição** e **Flexibilidade**.

### Quando todos estiverem preservados
```text
Nos processos controlados, [NOME] apresentou desempenho sem indicativo de déficit em Escolha, Alternância, Inibição e Flexibilidade, com [ausência de erros/boa precisão] e tempos compatíveis ou mais eficientes que a média esperada. Esse padrão indica preservação da capacidade de seleção de respostas, alternância entre regras, supressão de respostas automáticas inadequadas e adaptação cognitiva diante de mudanças de demanda.
```

### Quando houver prejuízo difuso
```text
Nos processos controlados, observaram-se dificuldades em Escolha, Alternância, Inibição e/ou Flexibilidade, sugerindo rebaixamento na capacidade de selecionar respostas relevantes, alternar critérios mentais, inibir respostas automáticas inadequadas e adaptar-se com eficiência a mudanças de regra. Esse padrão é compatível com fragilidades no controle executivo e na autorregulação cognitiva.
```

### Quando houver perfil misto
```text
Nos processos controlados, [NOME] demonstrou desempenho [preservado/adequado] em [áreas preservadas], porém apresentou [indicativo de déficit/rebaixamento] em [áreas rebaixadas]. Esse perfil sugere funcionamento executivo parcial, com preservação de alguns componentes do controle cognitivo, mas com fragilidades em [controle inibitório/alternância/flexibilidade/seleção de respostas].
```

## Parágrafo 4: parágrafo obrigatório sobre erros
Este é o ponto central desta skill. A IA deve sempre produzir um parágrafo específico comentando os erros.

### Regra
Os erros devem ser interpretados como indicadores de:
- impulsividade
- instabilidade atencional
- falhas de monitoramento
- dificuldade de controle inibitório
- baixa precisão
- desorganização na execução

A IA deve sempre ajustar a intensidade clínica do texto conforme a quantidade e a distribuição dos erros.

## Modelos para o parágrafo de erros

### 1. Ausência total de erros
Usar quando todas as etapas apresentarem zero erro.

```text
A ausência de erros em todas as etapas reforça boa precisão, controle da resposta e monitoramento executivo, sem marcadores de impulsividade, desorganização ou instabilidade cognitiva durante a execução.
```

### 2. Erros discretos e não generalizados
Usar quando houver poucos erros, isolados ou pontuais.

```text
A presença de erros discretos e pontuais não compromete de forma global o desempenho, mas sugere oscilações leves de monitoramento e controle da resposta ao longo da execução. Ainda assim, o conjunto do protocolo indica funcionamento globalmente organizado, com pequenas falhas situacionais de precisão.
```

### 3. Erros concentrados em processos automáticos
Usar quando os erros ocorrerem principalmente em Leitura e/ou Contagem.

```text
Os erros observados nos processos automáticos sugerem redução da precisão em tarefas de resposta mais imediata, podendo indicar instabilidade atencional basal, lentificação associada a perda de rastreio visual ou menor consistência na automatização de respostas simples.
```

### 4. Erros concentrados em processos controlados
Usar quando os erros ocorrerem principalmente em Escolha e/ou Alternância.

```text
Os erros observados nas etapas de maior demanda executiva sugerem dificuldade de monitoramento, controle inibitório e regulação da resposta sob condição de maior complexidade cognitiva. Esse padrão pode estar associado a impulsividade, falhas de autocontrole e menor estabilidade na condução de tarefas que exigem flexibilidade mental.
```

### 5. Erros distribuídos em diferentes etapas
Usar quando houver erros em automáticos e controlados.

```text
A ocorrência de erros em diferentes etapas do teste sugere comprometimento mais amplo da precisão, com impacto tanto em componentes automáticos quanto em processos controlados. Esse padrão pode indicar instabilidade atencional, falhas de monitoramento contínuo e menor eficiência no controle global da resposta.
```

### 6. Muitos erros
Usar quando a frequência de erros for clinicamente relevante.

```text
A frequência elevada de erros reforça a presença de prejuízos no monitoramento executivo, na precisão da resposta e na capacidade de autorregulação cognitiva, apontando para execução pouco consistente, com sinais de impulsividade e dificuldade de manutenção do controle atencional ao longo da tarefa.
```

## Parágrafo 5: síntese final obrigatória
O fechamento deve sempre começar com **“Em análise clínica”**.

### Quando o desempenho estiver preservado
```text
Em análise clínica, o desempenho de [NOME] no FDT revela funcionamento executivo preservado e eficiente, tanto nos componentes automáticos quanto nos controlados, sem evidências de prejuízo em velocidade de processamento, controle inibitório, alternância atencional ou flexibilidade cognitiva.
```

### Quando houver alterações leves ou parciais
```text
Em análise clínica, o desempenho de [NOME] no FDT sugere funcionamento executivo parcialmente preservado, com sinais de fragilidade em [domínios alterados], o que indica oscilação na eficiência do controle cognitivo e da regulação da resposta diante de demandas de maior complexidade.
```

### Quando houver prejuízo importante
```text
Em análise clínica, o desempenho de [NOME] no FDT evidencia prejuízos em componentes relevantes das funções executivas, com impacto sobre a velocidade de processamento, o controle inibitório, a alternância atencional e a flexibilidade cognitiva, sugerindo comprometimento do controle executivo global.
```

## Hipótese diagnóstica
Quando houver resultados sugestivos de alteração executiva clinicamente relevante, a skill pode acrescentar ao final:

```text
Há hipótese diagnóstica de prejuízo em funções executivas, com repercussões sobre controle inibitório, monitoramento da resposta e flexibilidade cognitiva.
```

Se o conjunto clínico do caso sustentar formulação mais específica, o sistema pode adaptar o fechamento para TDAH ou outra condição, mas apenas quando os demais dados da avaliação apontarem na mesma direção.

## Regras de redação
A IA deve seguir estas regras:

- usar apenas o primeiro nome do paciente nas análises, salvo instrução contrária do caso
- manter linguagem técnica e clínica
- não usar tabelas
- não usar travessões longos
- evitar repetição excessiva de “No” e “Na” no início das frases
- não inventar percentis se o sistema não forneceu
- não dizer que há déficit quando o resultado do sistema não indicar isso
- comentar obrigatoriamente os erros, mesmo quando ausentes
- encerrar com um parágrafo iniciado por “Em análise clínica”

## Lógica de composição para o sistema
A IA deve montar o texto assim:

1. Inserir parágrafo fixo de apresentação do FDT
2. Gerar parágrafo dos processos automáticos conforme Leitura e Contagem
3. Gerar parágrafo dos processos controlados conforme Escolha, Alternância, Inibição e Flexibilidade
4. Gerar parágrafo de erros conforme quantidade e distribuição dos erros
5. Gerar síntese final iniciada por “Em análise clínica”
6. Se houver indicativo clínico relevante, acrescentar hipótese diagnóstica

## Exemplo de saída preservada
```text
Interpretação e Observações Clínicas: A avaliação das funções executivas de Larissa incluiu a aplicação do Teste dos Cinco Dígitos (FDT), instrumento destinado à investigação da velocidade de processamento, controle inibitório, alternância atencional e flexibilidade cognitiva, contemplando processos automáticos e controlados.
Nos processos automáticos, os desempenhos em Leitura e Contagem foram classificados como sem indicativo de déficit, com execução precisa e sem erros, sugerindo automatização preservada e velocidade de processamento adequada em tarefas de baixa demanda executiva.
Nos processos controlados, Larissa apresentou desempenho sem indicativo de déficit em Escolha, Alternância, Inibição e Flexibilidade, todos com ausência de erros e tempos compatíveis ou mais eficientes que a média esperada. Esse padrão indica preservação da capacidade de seleção de respostas, alternância entre regras, supressão de respostas automáticas inadequadas e adaptação cognitiva diante de mudanças de demanda.
A ausência de erros em todas as etapas reforça boa precisão, controle da resposta e monitoramento executivo, sem marcadores de impulsividade, desorganização ou instabilidade cognitiva durante a execução.
Em análise clínica, o desempenho de Larissa no FDT revela funcionamento executivo preservado e eficiente, tanto nos componentes automáticos quanto nos controlados, sem evidências de prejuízo em velocidade de processamento, controle inibitório, alternância atencional ou flexibilidade cognitiva.
```

## Prompt operacional para a IA do sistema
```text
Gere a interpretação clínica do FDT em linguagem técnica, seguindo o modelo do laudo aprovado. Estruture o texto em cinco partes: apresentação do instrumento, processos automáticos, processos controlados, parágrafo específico sobre erros e síntese final iniciada por “Em análise clínica”. Use as classificações e os erros fornecidos pelo sistema como fonte de verdade. Não use tabelas, não use travessões longos, não invente percentis e não omita o parágrafo de erros. Quando houver alterações relevantes, descreva o impacto clínico sobre velocidade de processamento, controle inibitório, alternância atencional, flexibilidade cognitiva, precisão e monitoramento executivo. Quando couber, finalize com hipótese diagnóstica.
```

## Regra final
Se a interpretação não mencionar explicitamente os erros, a saída deve ser considerada incompleta.
