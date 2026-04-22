# SKILL: Interpretação do ETDAH-AD para o Sistema de Laudos

## Objetivo
Esta skill orienta a IA a redigir a **interpretação clínica do ETDAH-AD** em padrão técnico elevado, com linguagem refinada, articulação clínica consistente e integração com os demais instrumentos do laudo.

A redação deve seguir padrão clínico de alta qualidade, com texto fluido, sem repetições mecânicas e com uso da expressão **“Em análise clínica” apenas uma vez**, preferencialmente no parágrafo final.

## Finalidade do instrumento
O **ETDAH-AD** é uma escala de autorrelato voltada à identificação breve e prática de sintomas associados ao Transtorno do Déficit de Atenção e Hiperatividade em adolescentes e adultos. A escala avalia cinco fatores:

- **Desatenção (D)**
- **Impulsividade (I)**
- **Aspectos Emocionais (AE)**
- **Autorregulação da Atenção, da Motivação e da Ação (AAMA)**
- **Hiperatividade (H)**

Esses domínios abrangem sintomas nucleares do TDAH e repercussões funcionais sobre organização do comportamento, controle da resposta, regulação motivacional e funcionamento cotidiano. citeturn218062search0turn218062search2turn218062search4

## Regra interpretativa obrigatória do sistema
Para este instrumento, a IA deve seguir exatamente esta lógica:

- **Inferior** = sem indicativo de prejuízo clínico
- **Média Inferior** = sem indicativo de prejuízo clínico
- **Média** = sem indicativo de prejuízo clínico
- **Média Superior** = indicativo de dificuldade clínica
- **Superior** = indicativo de dificuldade clínica

A IA não deve interpretar classificações **Inferior**, **Média Inferior** ou **Média** como déficit.

## Estrutura fixa obrigatória
A interpretação deve seguir esta ordem:

1. Apresentação do instrumento
2. Fator 1 – Desatenção
3. Fator 2 – Impulsividade
4. Fator 3 – Aspectos Emocionais
5. Fator 4 – Autorregulação da Atenção, da Motivação e da Ação
6. Fator 5 – Hiperatividade
7. Escore Geral
8. Análise Integrada
9. Hipótese Diagnóstica / Fechamento final

## Modelo de abertura do instrumento
A IA deve iniciar com um parágrafo técnico semelhante a este:

```text
Interpretação e Observações Clínicas: A Escala ETDAH-AD é um instrumento de autorrelato destinado à identificação de sintomas associados ao Transtorno do Déficit de Atenção e Hiperatividade em adolescentes e adultos, avaliando domínios relacionados à desatenção, impulsividade, aspectos emocionais, autorregulação da atenção, da motivação e da ação, além de hiperatividade. O instrumento permite quantificar a intensidade das manifestações referidas pelo próprio avaliado, contribuindo para a compreensão do impacto funcional desses sintomas em diferentes contextos da vida cotidiana.
```

## Regra de estilo para os fatores
Cada fator deve ser interpretado em **parágrafo próprio**, contendo:
- nome do fator
- classificação recebida do sistema
- interpretação clínica coerente
- repercussão funcional quando houver elevação

A IA deve evitar repetição mecânica de estruturas fracas, como:
- “dentro da normalidade” em todos os fatores
- “sem indicativo de prejuízo” sem variação de linguagem
- “Em análise clínica” em múltiplos trechos

## Modelos por fator

### Fator 1 – Desatenção
Este fator contempla dificuldades de atenção sustentada, seletiva, persistência do esforço, memória de trabalho, organização e manutenção do objetivo da ação. citeturn218062search4

#### Quando a classificação for Inferior, Média Inferior ou Média
```text
Fator 1 – Desatenção
O resultado foi classificado como [CLASSIFICAÇÃO], não configurando prejuízo clínico nesse domínio. Esse padrão sugere funcionamento atencional globalmente compatível com o esperado, sem evidências consistentes de distraibilidade excessiva, perda frequente do foco, falhas marcantes de organiz ação ou dificuldade relevante de sustentação atencional no autorrelato.
```

#### Quando a classificação for Média Superior ou Superior
```text
Fator 1 – Desatenção
O resultado situou-se na classificação [CLASSIFICAÇÃO], configurando indicativo de dificuldade clínica nesse domínio. Esse achado sugere presença de comportamentos associados à desatenção, como dificuldade de manter o foco, sustentar o esforço mental, organizar tarefas, acompanhar demandas sequenciais e conservar informações relevantes em mente durante a execução de atividades.
```

### Fator 2 – Impulsividade
Este fator se relaciona ao controle inibitório, autocontrole, manejo interpessoal e seguimento de regras e normas. citeturn218062search4

#### Quando a classificação for Inferior, Média Inferior ou Média
```text
Fator 2 – Impulsividade
O desempenho apresentou classificação [CLASSIFICAÇÃO], não indicando prejuízo clínico nesse domínio. Esse resultado sugere controle globalmente adequado das respostas impulsivas, sem sinais consistentes de precipitação comportamental, dificuldade significativa de inibição ou comprometimento relevante no seguimento de regras segundo o autorrelato.
```

#### Quando a classificação for Média Superior ou Superior
```text
Fator 2 – Impulsividade
O desempenho situou-se na classificação [CLASSIFICAÇÃO], configurando indicativo de dificuldade clínica relevante nesse domínio. Esse perfil sugere tendência a responder de forma precipitada, dificuldade em inibir impulsos imediatos, menor tolerância à espera e possíveis repercussões no convívio interpessoal, na tomada de decisão e na autorregulação comportamental.
```

### Fator 3 – Aspectos Emocionais
Este fator envolve humor, sensação de fracasso, relacionamento interpessoal, isolamento e inflexibilidade diante de mudanças. citeturn218062search4

#### Quando a classificação for Inferior, Média Inferior ou Média
```text
Fator 3 – Aspectos Emocionais
O escore foi classificado como [CLASSIFICAÇÃO], o que não indica prejuízo clínico relevante nesse domínio. Esse padrão sugere estabilidade emocional globalmente preservada no autorrelato, sem evidências consistentes de sofrimento afetivo acentuado, autopercepção cronicamente negativa, retraimento importante ou dificuldade emocional clinicamente significativa associada ao quadro investigado.
```

#### Quando a classificação for Média Superior ou Superior
```text
Fator 3 – Aspectos Emocionais
O escore apresentou classificação [CLASSIFICAÇÃO], indicando dificuldade clínica nesse domínio. Esse achado sugere maior presença de sofrimento subjetivo, oscilação emocional, sensação de fracasso, dificuldade no manejo de frustrações e possível repercussão afetiva secundária às dificuldades atencionais e comportamentais referidas.
```

### Fator 4 – Autorregulação da Atenção, da Motivação e da Ação
Este fator contempla estabelecimento de prioridades, planejamento, organização, regulação motivacional, persistência diante de obstáculos e uso flexível de estratégias. citeturn218062search4

#### Quando a classificação for Inferior, Média Inferior ou Média
```text
Fator 4 – Autorregulação da Atenção, da Motivação e da Ação
O resultado apresentou classificação [CLASSIFICAÇÃO], não indicando prejuízo clínico nesse domínio. Esse padrão sugere capacidade globalmente preservada de organizar metas, regular o próprio comportamento, sustentar motivação e conduzir ações de forma coerente com os objetivos propostos.
```

#### Quando a classificação for Média Superior ou Superior
```text
Fator 4 – Autorregulação da Atenção, da Motivação e da Ação
O resultado apresentou classificação [CLASSIFICAÇÃO], configurando indicativo de dificuldade clínica significativa nesse domínio. Esse achado sugere prejuízos na capacidade de estabelecer prioridades, manter motivação ao longo do tempo, organizar etapas de ação, persistir diante de obstáculos e ajustar estratégias de forma eficiente para alcançar objetivos.
```

### Fator 5 – Hiperatividade
Este fator envolve inquietação, agitação, aceleração comportamental, distração associada à instabilidade e repercussões funcionais do excesso de atividade. citeturn218062search4

#### Quando a classificação for Inferior, Média Inferior ou Média
```text
Fator 5 – Hiperatividade
O resultado foi classificado como [CLASSIFICAÇÃO], não configurando prejuízo clínico nesse domínio. Esse perfil sugere ausência de indicadores consistentes de inquietação motora excessiva, agitação persistente ou aceleração comportamental com repercussão funcional importante no cotidiano.
```

#### Quando a classificação for Média Superior ou Superior
```text
Fator 5 – Hiperatividade
O resultado foi classificado como [CLASSIFICAÇÃO], indicando dificuldade clínica nesse domínio. Esse achado sugere presença de inquietação, agitação comportamental, aceleração do ritmo de ação e instabilidade na condução das atividades, com potencial impacto sobre a qualidade do desempenho cotidiano e a manutenção da organização comportamental.
```

## Escore Geral

### Quando o escore geral for Inferior, Média Inferior ou Média
```text
Escore Geral
O escore global situou-se na classificação [CLASSIFICAÇÃO], o que não configura comprometimento clínico amplo segundo os parâmetros do instrumento. Ainda assim, a interpretação deve considerar a distribuição interna dos fatores, uma vez que elevações específicas podem coexistir com um escore global dentro dos limites esperados.
```

### Quando o escore geral for Média Superior ou Superior
```text
Escore Geral
O escore global situou-se na classificação [CLASSIFICAÇÃO], indicando comprometimento clínico global no autorrelato. Esse padrão sugere que as manifestações associadas ao TDAH se apresentam de forma mais abrangente e funcionalmente relevante, com impacto em múltiplos domínios do cotidiano.
```

## Regra de integração interna dos fatores
A IA deve observar:

- escore geral normal **não anula** elevação significativa em fatores isolados
- elevações em Desatenção e AAMA costumam apontar fragilidade executiva mais ampla
- elevações em Impulsividade e Hiperatividade sugerem componente de descontrole comportamental mais evidente
- elevação em Aspectos Emocionais deve ser articulada com ansiedade, sofrimento subjetivo, autocrítica e repercussões secundárias

### Modelo para perfil focal
```text
Embora o escore global não indique comprometimento clínico amplo, a elevação significativa em [FATOR(ES)] demonstra que as dificuldades se concentram de maneira específica nesses domínios, com repercussões funcionais mais localizadas sobre [DESCREVER IMPACTO].
```

### Modelo para perfil difuso
```text
A elevação observada no escore geral, associada ao aumento em múltiplos fatores, sugere um padrão mais disseminado de dificuldades autorreferidas, com impacto mais amplo sobre atenção, autorregulação, estabilidade emocional e organização comportamental.
```

## Análise Integrada
Esta seção deve articular o ETDAH-AD com os demais dados do laudo, especialmente:

- BPA-2
- RAVLT
- FDT
- BAI, BFP ou IPHEXA quando houver
- observação clínica
- anamnese

A IA deve construir uma análise integrada sofisticada, evitando repetir resultados crus.

## Lógica da análise integrada

### Quando houver convergência entre autorrelato, observação e testes
```text
A análise integrada demonstra convergência entre o autorrelato obtido no ETDAH-AD, os achados instrumentais e o comportamento observado durante a avaliação, reforçando a consistência clínica do quadro descrito. As elevações em [FATORES] encontram correspondência em [TESTES/OBSERVAÇÕES], sustentando a compreensão de dificuldades reais e funcionalmente relevantes nos domínios de [ATENÇÃO, IMPULSIVIDADE, AUTORREGULAÇÃO, ETC.].
```

### Quando houver dissociação entre autorrelato e testes objetivos
```text
A integração dos resultados do ETDAH-AD com os demais instrumentos revela um perfil parcialmente dissociado entre sintomas autorreferidos e desempenho psicométrico. Em [TESTES PRESERVADOS], observou-se funcionamento [preservado/adequado], ao passo que o autorrelato indicou dificuldades relevantes em [FATORES]. Esse padrão sugere que parte do sofrimento funcional pode manifestar-se de forma mais subjetiva, ecológica ou situacional, nem sempre captada integralmente por medidas estruturadas de desempenho.
```

### Parágrafo observacional sem repetir “Em análise clínica”
A IA deve preferir construções como:

```text
Durante as sessões, observaram-se comportamentos compatíveis com [DESCREVER], incluindo [EXEMPLOS], especialmente em situações que exigiam organização da resposta, manutenção do foco, controle da impulsividade ou persistência sob demanda.
```

ou

```text
Do ponto de vista observacional, o comportamento de [NOME] durante a avaliação mostrou [DESCREVER], o que confere validade ecológica às manifestações referidas no autorrelato.
```

## Fechamento final com apenas uma ocorrência de “Em análise clínica”
A expressão deve aparecer **somente no parágrafo final**.

### Modelo de fechamento refinado
```text
Em análise clínica, a integração entre o autorrelato, os achados instrumentais e o comportamento observado durante a avaliação sustenta a compreensão de que [NOME] apresenta dificuldades predominantes nos domínios de [DOMÍNIOS], com repercussão funcional sobre [ATENÇÃO, CONTROLE DA RESPOSTA, AUTORREGULAÇÃO, ORGANIZAÇÃO, ETC.].
```

## Hipótese diagnóstica
Quando houver elevação clinicamente relevante em Desatenção, Impulsividade, AAMA e/ou Hiperatividade, associada a observação clínica e demais instrumentos compatíveis, a IA pode concluir com:

```text
Há hipótese diagnóstica de Transtorno do Déficit de Atenção e Hiperatividade, considerando a presença de manifestações clinicamente significativas de [DESATENÇÃO / IMPULSIVIDADE / HIPERATIVIDADE / PREJUÍZO EXECUTIVO], com repercussão funcional em diferentes contextos da vida diária, em consonância com os critérios do DSM-5-TR™.
```

### Quando houver predomínio desatento
```text
Há hipótese diagnóstica de Transtorno do Déficit de Atenção e Hiperatividade com apresentação predominantemente desatenta, considerando a predominância de manifestações atencionais e executivas clinicamente relevantes com impacto funcional.
```

### Quando houver predomínio hiperativo/impulsivo
```text
Há hipótese diagnóstica de Transtorno do Déficit de Atenção e Hiperatividade com apresentação predominantemente hiperativa/impulsiva, considerando a predominância de manifestações de impulsividade, inquietação e descontrole comportamental com repercussão funcional.
```

### Quando houver combinação de domínios
```text
Há hipótese diagnóstica de Transtorno do Déficit de Atenção e Hiperatividade com apresentação combinada, considerando a coexistência de manifestações significativas de desatenção e hiperatividade/impulsividade com impacto funcional relevante.
```

### Regra importante
A IA não deve fechar hipótese diagnóstica de TDAH com base apenas no ETDAH-AD isoladamente. O fechamento depende da integração com observação clínica, anamnese e demais instrumentos.

## Modelo de referência refinado
```text
Interpretação e Observações Clínicas: A Escala ETDAH-AD é um instrumento de autorrelato destinado à identificação de sintomas associados ao Transtorno do Déficit de Atenção e Hiperatividade em adolescentes e adultos, avaliando domínios relacionados à desatenção, impulsividade, aspectos emocionais, autorregulação da atenção, da motivação e da ação, além de hiperatividade. O instrumento permite quantificar a intensidade das manifestações referidas pelo próprio avaliado, contribuindo para a compreensão do impacto funcional desses sintomas em diferentes contextos da vida cotidiana.

Fator 1 – Desatenção
O resultado foi classificado como [CLASSIFICAÇÃO], [INTERPRETAÇÃO CLÍNICA].

Fator 2 – Impulsividade
O resultado foi classificado como [CLASSIFICAÇÃO], [INTERPRETAÇÃO CLÍNICA].

Fator 3 – Aspectos Emocionais
O resultado foi classificado como [CLASSIFICAÇÃO], [INTERPRETAÇÃO CLÍNICA].

Fator 4 – Autorregulação da Atenção, da Motivação e da Ação
O resultado foi classificado como [CLASSIFICAÇÃO], [INTERPRETAÇÃO CLÍNICA].

Fator 5 – Hiperatividade
O resultado foi classificado como [CLASSIFICAÇÃO], [INTERPRETAÇÃO CLÍNICA].

Escore Geral
O escore global situou-se na classificação [CLASSIFICAÇÃO], [SÍNTESE DO PERFIL].

Análise Integrada
A integração dos resultados do ETDAH-AD com [DEMAIS INSTRUMENTOS] revela [CONVERGÊNCIA OU DISSOCIAÇÃO], indicando [SÍNTESE CLÍNICA]. Durante as sessões, observaram-se [COMPORTAMENTOS RELEVANTES], especialmente em contextos de [DEMANDA EXECUTIVA / ATENCIONAL / COMPORTAMENTAL].

Em análise clínica, a integração entre o autorrelato, os achados instrumentais e o comportamento observado durante a avaliação sustenta a compreensão de que [NOME] apresenta [SÍNTESE FINAL]. Há hipótese diagnóstica de [FORMULAÇÃO DIAGNÓSTICA], conforme critérios do DSM-5-TR™.
```

## Regras de redação do sistema
A IA deve seguir estas regras:

- usar linguagem técnica, fluida e natural
- evitar repetição estrutural excessiva
- usar apenas uma vez a expressão “Em análise clínica”
- não usar tabelas
- não usar travessões longos
- não contradizer a classificação do sistema
- não interpretar Inferior, Média Inferior ou Média como prejuízo
- usar apenas o primeiro nome do paciente nas análises, salvo orientação específica do caso
- incluir hipótese diagnóstica apenas quando houver sustentação clínica integrada

## Prompt operacional para a IA do sistema
```text
Gere a interpretação clínica do ETDAH-AD em padrão técnico elevado, com linguagem refinada e sem repetições desnecessárias. Estruture o texto em: apresentação do instrumento, Fator 1 – Desatenção, Fator 2 – Impulsividade, Fator 3 – Aspectos Emocionais, Fator 4 – Autorregulação da Atenção, da Motivação e da Ação, Fator 5 – Hiperatividade, Escore Geral, Análise Integrada e fechamento final. Siga a regra interpretativa do sistema: Inferior, Média Inferior e Média não indicam prejuízo clínico; Média Superior e Superior indicam dificuldade clínica. Integre o ETDAH-AD com BPA-2, RAVLT, FDT, anamnese, observação clínica e outros instrumentos quando essas informações estiverem disponíveis. Use a expressão “Em análise clínica” apenas uma vez, no parágrafo final. Se houver sustentação convergente, finalize com hipótese diagnóstica redigida em linguagem técnica e compatível com o DSM-5-TR™.
```

## Regra final
Se o texto repetir “Em análise clínica” mais de uma vez, ou interpretar classificações não clínicas como déficit, a saída deve ser considerada inadequada e precisa ser reescrita.
