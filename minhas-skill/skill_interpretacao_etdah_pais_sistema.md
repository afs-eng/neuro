# SKILL: Interpretação do E-TDAH-PAIS para o Sistema de Laudos

## Objetivo
Esta skill orienta a IA a redigir a **interpretação clínica do E-TDAH-PAIS** em padrão técnico elevado, com linguagem refinada, coerência interna, integração com outros instrumentos e formulação diagnóstica compatível com o restante do laudo.

A redação deve seguir padrão clínico de alta qualidade, evitando repetições desnecessárias, especialmente da expressão **“Em análise clínica”**, que deve aparecer **uma única vez**, preferencialmente no parágrafo conclusivo final.

## Finalidade do instrumento
O texto deve partir da compreensão de que o **E-TDAH-PAIS** investiga manifestações comportamentais e emocionais associadas ao Transtorno do Déficit de Atenção e Hiperatividade a partir da percepção dos responsáveis, contemplando os domínios de:

- regulação emocional
- hiperatividade/impulsividade
- comportamento adaptativo
- atenção
- escore geral

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
2. Fator 1 – Regulação Emocional
3. Fator 2 – Hiperatividade / Impulsividade
4. Fator 3 – Comportamento Adaptativo
5. Fator 4 – Atenção
6. Escore Geral
7. Análise Integrada
8. Hipótese Diagnóstica / Fechamento final

## Modelo de abertura do instrumento
A IA deve iniciar com um parágrafo técnico semelhante a este:

```text
Interpretação e Observações Clínicas: A Escala E-TDAH-PAIS tem como objetivo identificar manifestações comportamentais e emocionais associadas ao Transtorno do Déficit de Atenção e Hiperatividade (TDAH) a partir da percepção dos responsáveis, avaliando domínios relacionados à regulação emocional, hiperatividade/impulsividade, comportamento adaptativo e atenção. O instrumento fornece indicadores quantitativos sobre a intensidade e o impacto funcional desses comportamentos no cotidiano da criança, contribuindo para a compreensão clínica do quadro comportamental em diferentes contextos de desenvolvimento (Benczik, 2005).
```

## Regra de estilo para os fatores
Cada fator deve ser interpretado em **parágrafo próprio**, com:
- nome do fator
- classificação recebida do sistema
- interpretação clínica coerente
- impacto funcional quando houver elevação

A IA não deve repetir fórmulas pobres como:
- “em análise clínica” em vários parágrafos
- “dentro da normalidade” em excesso
- “sem indicativo de prejuízo” em sequência mecânica sem variar a linguagem

## Modelos por fator

### Fator 1 – Regulação Emocional

#### Quando a classificação for Inferior, Média Inferior ou Média
```text
Fator 1 – Regulação Emocional
O resultado foi classificado como [CLASSIFICAÇÃO], o que, conforme os critérios interpretativos do instrumento, não indica prejuízo clínico nesse domínio. Esse padrão sugere estabilidade emocional globalmente compatível com a faixa etária, sem evidências consistentes de labilidade afetiva acentuada, irritabilidade persistente ou dificuldade significativa de modulação emocional na percepção dos responsáveis.
```

#### Quando a classificação for Média Superior ou Superior
```text
Fator 1 – Regulação Emocional
O resultado situou-se na classificação [CLASSIFICAÇÃO], configurando indicativo de dificuldade clínica nesse domínio. Esse achado sugere maior frequência de manifestações como irritabilidade, oscilação afetiva, reatividade emocional aumentada e dificuldade de autorregulação, com possível repercussão no convívio familiar e na adaptação às frustrações cotidianas.
```

### Fator 2 – Hiperatividade / Impulsividade

#### Quando a classificação for Inferior, Média Inferior ou Média
```text
Fator 2 – Hiperatividade / Impulsividade
O desempenho apresentou classificação [CLASSIFICAÇÃO], não configurando prejuízo clínico nesse domínio. Esse resultado sugere ausência de indicadores consistentes de agitação motora excessiva, impulsividade comportamental ou dificuldade relevante de inibição de respostas na percepção parental.
```

#### Quando a classificação for Média Superior ou Superior
```text
Fator 2 – Hiperatividade / Impulsividade
O desempenho situou-se na classificação [CLASSIFICAÇÃO], configurando indicativo de dificuldade clínica relevante nesse domínio. Esse achado aponta para comportamentos frequentes de inquietação, agitação psicomotora, impulsividade e dificuldade em postergar respostas imediatas, com impacto funcional percebido no ambiente familiar e potencial repercussão em outros contextos de exigência comportamental.
```

### Fator 3 – Comportamento Adaptativo

#### Quando a classificação for Inferior, Média Inferior ou Média
```text
Fator 3 – Comportamento Adaptativo
O escore foi classificado como [CLASSIFICAÇÃO], sendo interpretado como sem indicativo de prejuízo clínico. Esse padrão sugere repertório funcional adequado para responder a rotinas, regras e demandas cotidianas compatíveis com a etapa do desenvolvimento.
```

#### Quando a classificação for Média Superior ou Superior
```text
Fator 3 – Comportamento Adaptativo
O escore apresentou classificação [CLASSIFICAÇÃO], indicando dificuldade clínica nesse domínio. Esse resultado sugere prejuízos na organização do comportamento frente às exigências do cotidiano, com possíveis dificuldades para seguir rotinas, adaptar-se a regras, sustentar comportamentos adequados ao contexto e responder de forma funcional às demandas ambientais.
```

### Fator 4 – Atenção

#### Quando a classificação for Inferior, Média Inferior ou Média
```text
Fator 4 – Atenção
O resultado apresentou classificação [CLASSIFICAÇÃO], não indicando prejuízo clínico nesse domínio segundo a percepção dos responsáveis. Esse perfil sugere funcionamento atencional globalmente compatível com a faixa etária, sem sinais consistentes de distraibilidade excessiva, dificuldade de sustentação do foco ou comprometimento importante na conclusão de tarefas.
```

#### Quando a classificação for Média Superior ou Superior
```text
Fator 4 – Atenção
O resultado apresentou classificação [CLASSIFICAÇÃO], indicando dificuldade clínica significativa nesse domínio. Esse achado sugere presença de comportamentos associados à desatenção, como dificuldade em manter o foco, concluir tarefas, acompanhar instruções e sustentar a atenção em atividades estruturadas.
```

### Escore Geral

#### Quando o escore geral for Inferior, Média Inferior ou Média
```text
Escore Geral
O escore global situou-se na classificação [CLASSIFICAÇÃO], o que não configura comprometimento clínico amplo segundo os parâmetros do instrumento. Ainda assim, a interpretação deve considerar a distribuição interna dos fatores, uma vez que alterações específicas podem coexistir com um escore global dentro dos limites esperados.
```

#### Quando o escore geral for Média Superior ou Superior
```text
Escore Geral
O escore global situou-se na classificação [CLASSIFICAÇÃO], indicando comprometimento clínico global na percepção dos responsáveis. Esse resultado sugere que as manifestações comportamentais relacionadas ao TDAH se apresentam de forma mais abrangente e funcionalmente relevante no cotidiano da criança.
```

## Regra de integração interna dos fatores
A IA deve observar:

- Escore geral normal **não anula** elevação específica em fatores isolados
- Fatores elevados devem ser destacados mesmo quando o escore global estiver na média
- O texto deve explicar se as dificuldades são **focais** ou **difusas**

### Modelo para perfil focal
```text
Embora o escore global não indique comprometimento clínico amplo, a presença de elevação significativa em [FATOR(ES)] demonstra que as dificuldades se concentram de maneira específica nesses domínios, com repercussões funcionais mais localizadas.
```

### Modelo para perfil difuso
```text
A elevação observada no escore geral, associada ao aumento em múltiplos fatores, sugere um padrão mais disseminado de dificuldades comportamentais, com impacto mais amplo sobre o funcionamento cotidiano.
```

## Análise Integrada
Esta seção deve articular o E-TDAH-PAIS com os demais dados do laudo, especialmente:

- BPA-2
- RAVLT
- FDT
- observação clínica
- dados da anamnese

A IA deve construir uma análise integrada sofisticada, evitando mera repetição dos resultados brutos.

## Lógica da análise integrada

### Quando houver dissociação entre percepção parental e testes objetivos
```text
A integração dos resultados do E-TDAH-PAIS com os demais instrumentos revela um perfil parcialmente dissociado entre desempenho psicométrico e percepção comportamental. Em [TESTES PRESERVADOS], observou-se funcionamento [preservado/adequado/eficiente]. Entretanto, [TESTE ALTERADO ou OBSERVAÇÃO CLÍNICA] evidenciou [DESCREVER ALTERAÇÃO], sugerindo que as dificuldades se manifestam de forma mais expressiva no plano comportamental, autorregulatório ou situacional do que necessariamente em medidas estruturadas de desempenho.
```

### Quando houver convergência entre escalas, testes e observação
```text
A análise integrada demonstra convergência entre a percepção dos responsáveis, os achados dos instrumentos objetivos e a observação clínica, reforçando a consistência do quadro comportamental descrito. A elevação em [FATORES] no E-TDAH-PAIS encontra correspondência em [TESTES/OBSERVAÇÕES], sustentando a compreensão de dificuldades reais e funcionalmente relevantes nos domínios de [ATENÇÃO, IMPULSIVIDADE, AUTORREGULAÇÃO, ETC.].
```

### Parágrafo observacional sem repetir “Em análise clínica”
Em vez de repetir “Em análise clínica” no meio do texto, a IA deve usar construções como:

```text
Durante as sessões, foram observados comportamentos compatíveis com [DESCREVER], incluindo [EXEMPLOS], especialmente em situações de maior exigência de controle da resposta, manutenção do foco ou tolerância ao tempo de execução.
```

ou

```text
Do ponto de vista observacional, o comportamento de [NOME] durante a avaliação mostrou [DESCREVER], o que acrescenta validade ecológica aos achados descritos pelos responsáveis.
```

## Fechamento final com apenas uma ocorrência de “Em análise clínica”
A expressão deve aparecer **somente no parágrafo final**, preferencialmente junto da hipótese diagnóstica.

### Modelo de fechamento refinado
```text
Em análise clínica, a integração entre a percepção parental, os achados instrumentais e o comportamento observado durante a avaliação sustenta a compreensão de que [NOME] apresenta dificuldades predominantes nos domínios de [DOMÍNIOS], com repercussão funcional sobre [AUTORREGULAÇÃO, CONTROLE INIBITÓRIO, ATENÇÃO, ETC.].
```

## Hipótese diagnóstica
Quando houver elevação clinicamente relevante nos fatores de Hiperatividade/Impulsividade e Atenção, associada a observação clínica e outros instrumentos compatíveis, a IA pode concluir com:

```text
Há hipótese diagnóstica de Transtorno do Déficit de Atenção e Hiperatividade com apresentação combinada, considerando a presença de manifestações significativas de desatenção e hiperatividade/impulsividade com impacto funcional nos contextos de vida diária, em consonância com os critérios do DSM-5-TR™.
```

### Quando houver predomínio atencional
```text
Há hipótese diagnóstica de Transtorno do Déficit de Atenção e Hiperatividade com apresentação predominantemente desatenta, considerando a predominância de manifestações atencionais clinicamente relevantes com repercussão funcional.
```

### Quando houver predomínio hiperativo/impulsivo
```text
Há hipótese diagnóstica de Transtorno do Déficit de Atenção e Hiperatividade com apresentação predominantemente hiperativa/impulsiva, considerando a predominância de manifestações de inquietação motora, impulsividade e dificuldade de inibição comportamental com impacto funcional.
```

### Regra importante
A IA não deve fechar hipótese diagnóstica de TDAH apenas com base no E-TDAH-PAIS isoladamente. O fechamento deve depender da integração com:
- observação clínica
- anamnese
- demais instrumentos

## Versão refinada do modelo fornecido
Abaixo está a versão reescrita em padrão mais elevado, sem repetição de “Em análise clínica” no corpo do texto:

```text
Interpretação e Observações Clínicas: A Escala E-TDAH-PAIS tem como objetivo identificar manifestações comportamentais e emocionais associadas ao Transtorno do Déficit de Atenção e Hiperatividade (TDAH) a partir da percepção dos responsáveis, avaliando domínios relacionados à regulação emocional, hiperatividade/impulsividade, comportamento adaptativo e atenção. O instrumento fornece indicadores quantitativos sobre a intensidade e o impacto funcional desses comportamentos no cotidiano da criança, contribuindo para a caracterização clínica do perfil comportamental observado (Benczik, 2005).

Fator 1 – Regulação Emocional
O resultado foi classificado como Inferior, o que, conforme os critérios interpretativos do instrumento, não indica prejuízo clínico nesse domínio. Esse padrão sugere estabilidade emocional compatível com o esperado para a idade, sem sinais consistentes de labilidade afetiva importante, explosividade recorrente ou desregulação emocional persistente na percepção parental.

Fator 2 – Hiperatividade / Impulsividade
O desempenho situou-se na classificação Superior, configurando indicativo de dificuldade clínica relevante nesse domínio. Esse achado aponta para comportamentos frequentes de inquietação, agitação psicomotora, impulsividade e dificuldade em inibir respostas imediatas, com impacto funcional percebido no ambiente familiar.

Fator 3 – Comportamento Adaptativo
O escore foi classificado como Inferior, sendo interpretado como sem indicativo de prejuízo clínico. Esse padrão sugere repertório funcional adequado para seguir rotinas, responder a regras básicas e adaptar-se às demandas cotidianas compatíveis com a faixa etária.

Fator 4 – Atenção
O resultado apresentou classificação Superior, indicando dificuldade clínica significativa nesse domínio segundo a percepção dos responsáveis. Esse achado sugere presença de comportamentos associados à desatenção, como dificuldade em manter o foco, concluir tarefas, acompanhar instruções e sustentar atenção em atividades estruturadas.

Escore Geral
O escore global situou-se na classificação Média, o que não configura comprometimento clínico amplo segundo os parâmetros do instrumento. Ainda assim, a elevação significativa nos fatores de Hiperatividade/Impulsividade e Atenção demonstra que as dificuldades se concentram de modo específico nesses domínios.

Análise Integrada
A integração dos resultados do E-TDAH-PAIS com os achados da BPA-2, do RAVLT e do FDT revela um perfil parcialmente dissociado entre desempenho psicométrico e percepção comportamental. Na BPA-2, Débora apresentou funcionamento atencional preservado e, em alguns domínios, acima da média. No RAVLT, observou-se memória verbal eficiente, com curva de aprendizagem progressiva e boa retenção. Por outro lado, o FDT evidenciou lentificação significativa em processos automáticos e controlados, com indicativos de prejuízo na velocidade de processamento e no controle executivo sob demanda temporal.

Durante as sessões, foram observados comportamentos compatíveis com inquietação psicomotora, necessidade de redirecionamento frequente e dificuldade em manter engajamento contínuo em tarefas estruturadas, sobretudo em situações que exigiam controle da resposta e sustentação do foco sob limite temporal.

Esse conjunto de achados sugere que, embora os instrumentos objetivos de atenção sustentada tenham indicado funcionamento globalmente preservado, as dificuldades se manifestam de forma mais expressiva no plano comportamental e autorregulatório, com impacto relevante na organização da conduta e no manejo das exigências cotidianas.

Em análise clínica, a integração entre a percepção parental, os achados instrumentais e o comportamento observado durante a avaliação sustenta a compreensão de que Débora apresenta dificuldades significativas nos domínios de desatenção e hiperatividade/impulsividade, com repercussão funcional sobre autorregulação, controle da resposta e manejo comportamental. Há hipótese diagnóstica de Transtorno do Déficit de Atenção e Hiperatividade com apresentação combinada, de gravidade atual moderada, conforme critérios do DSM-5-TR™.
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
Gere a interpretação clínica do E-TDAH-PAIS em padrão técnico elevado, com linguagem refinada e sem repetições desnecessárias. Estruture o texto em: apresentação do instrumento, Fator 1, Fator 2, Fator 3, Fator 4, Escore Geral, Análise Integrada e fechamento final. Siga a regra interpretativa do sistema: Inferior, Média Inferior e Média não indicam prejuízo clínico; Média Superior e Superior indicam dificuldade clínica. Integre o E-TDAH-PAIS com BPA-2, RAVLT, FDT, observação clínica e anamnese quando essas informações estiverem disponíveis. Use a expressão “Em análise clínica” apenas uma vez, no parágrafo final. Se houver sustentação convergente, finalize com hipótese diagnóstica redigida em linguagem técnica e compatível com o DSM-5-TR™.
```

## Regra final
Se o texto repetir “Em análise clínica” mais de uma vez, a saída deve ser considerada inadequada e precisa ser reescrita.
