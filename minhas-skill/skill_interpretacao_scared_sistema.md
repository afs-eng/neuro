# SKILL: Interpretação do SCARED para o Sistema de Laudos

## Objetivo
Esta skill orienta a IA a redigir a **interpretação clínica do SCARED** em linguagem técnica, clara e consistente com o padrão dos laudos do sistema, contemplando tanto a **versão respondida pelos pais ou responsáveis** quanto a **versão de autorrelato**, quando disponível.

A redação deve ser fluida, sem repetições mecânicas, sem tabelas e com uso da expressão **“Em análise clínica” apenas uma vez**, preferencialmente no parágrafo final.

## Finalidade do instrumento
O **SCARED** é um instrumento destinado à investigação de sintomas ansiosos em crianças e adolescentes, podendo ser respondido pelos pais ou responsáveis e, em determinadas faixas etárias, também pelo próprio avaliado. O instrumento abrange diferentes manifestações de ansiedade, incluindo:

- Pânico / Sintomas Somáticos
- Ansiedade Generalizada
- Ansiedade de Separação
- Fobia Social
- Evitação Escolar
- Escore Total

Seu objetivo é rastrear a presença, a distribuição e a intensidade de sintomas ansiosos em diferentes domínios do funcionamento emocional.

## Estrutura fixa obrigatória
A interpretação deve seguir esta ordem:

1. Apresentação do instrumento
2. Escore Total
3. Pânico / Sintomas Somáticos
4. Ansiedade Generalizada
5. Ansiedade de Separação
6. Fobia Social
7. Evitação Escolar
8. Síntese clínica final
9. Hipótese diagnóstica, quando cabível

## Regra central da interpretação
A IA deve usar como fonte de verdade:
- o **status clínico ou não clínico** de cada domínio
- o **resultado do escore total**
- a **versão aplicada**: pais/responsáveis, autorrelato ou ambas

A IA não deve reinventar pontos de corte nem contradizer a classificação fornecida pelo sistema.

## Regra de linguagem
A IA deve evitar o termo **“informante”**. Em vez disso, usar:
- “segundo a percepção dos responsáveis”
- “na percepção materna”
- “no relato dos cuidadores”
- “no autorrelato”
- “na autoavaliação do paciente”

## Modelo de abertura – versão pais/responsáveis
```text
Interpretação e Observações Clínicas: O SCARED é um instrumento destinado à investigação de sintomas ansiosos em crianças e adolescentes, a partir da percepção dos pais ou responsáveis, abrangendo diferentes manifestações de ansiedade, como ansiedade de separação, ansiedade generalizada, sintomas de pânico/somáticos, fobia social e evitação escolar.
```

## Modelo de abertura – autorrelato
```text
Interpretação e Observações Clínicas: O SCARED é um instrumento destinado à investigação de sintomas ansiosos em crianças e adolescentes, a partir do autorrelato, abrangendo diferentes manifestações de ansiedade, como ansiedade de separação, ansiedade generalizada, sintomas de pânico/somáticos, fobia social e evitação escolar.
```

## Modelo de abertura – quando houver ambas as versões
```text
Interpretação e Observações Clínicas: O SCARED é um instrumento destinado à investigação de sintomas ansiosos em crianças e adolescentes, podendo ser respondido tanto pelos pais ou responsáveis quanto pelo próprio avaliado. O instrumento rastreia diferentes manifestações de ansiedade, incluindo sintomas de pânico/somáticos, ansiedade generalizada, ansiedade de separação, fobia social e evitação escolar, permitindo comparar a percepção familiar com a vivência subjetiva da criança ou do adolescente.
```

## Modelos por domínio
Cada domínio deve ser descrito conforme o resultado clínico ou não clínico.

### Escore Total não clínico
```text
Os resultados indicaram ausência de quadro ansioso global, conforme evidenciado pelo escore total abaixo do ponto de corte, sugerindo funcionamento emocional geral dentro dos limites esperados [segundo a percepção dos responsáveis / no autorrelato / em ambas as versões].
```

### Escore Total clínico
```text
Os resultados indicaram presença de sintomas ansiosos em nível global, conforme evidenciado pelo escore total em faixa clínica, sugerindo comprometimento emocional mais abrangente [segundo a percepção dos responsáveis / no autorrelato / em ambas as versões].
```

### Pânico / Sintomas Somáticos não clínico
```text
No domínio de Pânico/Sintomas Somáticos, a pontuação situou-se na faixa não clínica, não indicando presença relevante de sintomas físicos associados à ansiedade, crises de pânico ou desconfortos somáticos recorrentes relacionados ao estado emocional.
```

### Pânico / Sintomas Somáticos clínico
```text
No domínio de Pânico/Sintomas Somáticos, observou-se classificação clínica, sugerindo presença de manifestações físicas associadas à ansiedade, como desconfortos somáticos recorrentes, sensação de tensão corporal, medo intenso ou sintomas compatíveis com episódios de pânico.
```

### Ansiedade Generalizada não clínico
```text
Em Ansiedade Generalizada, o resultado foi classificado como não clínico, não indicando preocupações excessivas, estado persistente de apreensão ou antecipação ansiosa significativa diante de múltiplas situações do cotidiano.
```

### Ansiedade Generalizada clínico
```text
Em Ansiedade Generalizada, observou-se classificação clínica, sugerindo presença de preocupações excessivas, tendência à apreensão constante, dificuldade de relaxamento e antecipação ansiosa diante de diferentes demandas do cotidiano.
```

### Ansiedade de Separação não clínico
```text
No domínio de Ansiedade de Separação, a pontuação foi classificada como não clínica, afastando indicativos de insegurança emocional relevante diante do afastamento das figuras de apego.
```

### Ansiedade de Separação clínico
```text
No domínio de Ansiedade de Separação, observou-se classificação clínica, sugerindo presença de insegurança emocional em situações de afastamento das figuras de apego, com possível necessidade aumentada de proximidade, previsibilidade e suporte emocional em contextos de separação. Esse resultado pode estar relacionado a maior desconforto diante de afastamentos, preocupação com a ausência dos cuidadores ou necessidade intensificada de segurança emocional para lidar com situações de autonomia.
```

### Fobia Social não clínico
```text
Em Fobia Social, o resultado foi classificado como não clínico, afastando indicativos de inibição social importante, medo acentuado de exposição ou desconforto significativo em interações sociais.
```

### Fobia Social clínico
```text
Em Fobia Social, observou-se classificação clínica, indicando presença de desconforto relevante em situações de exposição, interação social ou avaliação por outras pessoas, com possível tendência à inibição, evitação ou sofrimento em contextos interpessoais.
```

### Evitação Escolar não clínico
```text
O domínio de Evitação Escolar apresentou pontuação não clínica, não sugerindo recusa escolar ou ansiedade relevante associada ao ambiente escolar.
```

### Evitação Escolar clínico
```text
O domínio de Evitação Escolar apresentou classificação clínica, sugerindo desconforto emocional relevante diante do contexto escolar, com possível tendência à recusa, resistência ou sofrimento associado à frequência e permanência na escola.
```

## Síntese clínica final
A expressão **“Em análise clínica”** deve aparecer apenas no último parágrafo.

### Modelo para alteração circunscrita em um domínio
```text
Em análise clínica, o perfil emocional de [NOME] revela sintomas ansiosos específicos e circunscritos ao domínio de [DOMÍNIO], sem evidências de comprometimento ansioso amplo nos demais eixos avaliados. Esse padrão sugere manifestação ansiosa mais focal, relacionada a situações específicas do funcionamento emocional.
```

### Modelo para múltiplos domínios alterados
```text
Em análise clínica, o perfil emocional de [NOME] revela sintomatologia ansiosa distribuída em múltiplos domínios, indicando sofrimento emocional mais abrangente e com potencial repercussão sobre o funcionamento adaptativo, relacional e acadêmico.
```

### Modelo para ausência de alterações clínicas
```text
Em análise clínica, o perfil emocional de [NOME] não revela indicadores consistentes de quadro ansioso clinicamente significativo, mantendo-se dentro dos limites esperados no conjunto dos domínios investigados.
```

## Hipótese diagnóstica
A hipótese diagnóstica deve ser escrita apenas quando houver sustentação clínica e sempre de forma prudente.

### Ansiedade de separação circunscrita
```text
Há hipótese diagnóstica de sintomatologia ansiosa relacionada à ansiedade de separação, em nível circunscrito, devendo esse achado ser interpretado de forma integrada aos demais dados clínicos e contextuais da avaliação.
```

### Ansiedade social
```text
Há hipótese diagnóstica de sintomatologia ansiosa relacionada à fobia social, devendo esse achado ser interpretado em conjunto com os dados observacionais, escolares e clínicos da avaliação.
```

### Ansiedade generalizada
```text
Há hipótese diagnóstica de sintomatologia ansiosa com predomínio de ansiedade generalizada, considerando a presença de preocupações excessivas e apreensão persistente com repercussão funcional.
```

### Quadro ansioso mais amplo
```text
Há hipótese diagnóstica de sintomatologia ansiosa clinicamente relevante, com manifestações em múltiplos domínios, devendo o quadro ser interpretado de forma integrada à anamnese, à observação clínica e aos demais instrumentos aplicados.
```

### Regra importante
A IA não deve fechar diagnóstico formal de transtorno ansioso apenas com base no SCARED isoladamente. O texto deve falar em **hipótese diagnóstica**, rastreio ou sintomatologia compatível, integrando sempre com os demais dados da avaliação.

## Regras para quando houver autorrelato e heterorrelato
Quando o sistema fornecer as duas versões, a IA deve comparar os resultados.

### Quando houver convergência
```text
Observou-se convergência entre a percepção dos responsáveis e o autorrelato, o que reforça a consistência do achado ansioso no domínio de [DOMÍNIO].
```

### Quando houver divergência
```text
Observou-se divergência entre a percepção dos responsáveis e o autorrelato, sugerindo diferença entre a expressão subjetiva dos sintomas e sua percepção no ambiente familiar. Esse padrão deve ser interpretado com cautela e articulado aos dados observacionais e contextuais da avaliação.
```

### Quando apenas uma versão estiver alterada
```text
A elevação observada apenas em [VERSÃO] sugere que os sintomas podem estar sendo percebidos de forma mais intensa [pelo próprio paciente / pelos responsáveis], o que reforça a importância de interpretação integrada com o contexto clínico e comportamental.
```

## Regras de redação do sistema
A IA deve seguir estas regras:

- usar linguagem técnica, fluida e natural
- usar apenas uma vez a expressão “Em análise clínica”
- não usar tabelas
- não usar travessões longos
- não usar o termo “informante”
- não contradizer o status clínico fornecido pelo sistema
- usar apenas o primeiro nome do paciente nas análises, salvo instrução específica do caso
- incluir hipótese diagnóstica apenas quando houver achado clínico relevante
- quando houver duas versões, comparar convergência e divergência

## Modelo refinado baseado no exemplo fornecido
```text
Interpretação e Observações Clínicas: O SCARED é um instrumento destinado à investigação de sintomas ansiosos em crianças e adolescentes, a partir da percepção dos pais ou responsáveis, abrangendo diferentes manifestações de ansiedade, como ansiedade de separação, ansiedade generalizada, sintomas de pânico/somáticos, fobia social e evitação escolar.

Os resultados de João Pedro indicaram ausência de quadro ansioso global, conforme evidenciado pelo escore total abaixo do ponto de corte, sugerindo funcionamento emocional geral dentro dos limites esperados segundo a percepção materna.

No domínio de Pânico/Sintomas Somáticos, a pontuação situou-se na faixa não clínica, não indicando presença relevante de sintomas físicos associados à ansiedade, crises de pânico ou desconfortos somáticos recorrentes relacionados ao estado emocional. Em Ansiedade Generalizada, o resultado também foi classificado como não clínico, afastando preocupações excessivas, estado persistente de apreensão ou antecipação ansiosa significativa diante de múltiplas situações do cotidiano.

No domínio de Ansiedade de Separação, observou-se classificação clínica, sugerindo presença de insegurança emocional em situações de afastamento das figuras de apego, com possível necessidade aumentada de proximidade, previsibilidade e suporte emocional em contextos de separação. Esse resultado pode estar relacionado a maior desconforto diante de afastamentos, preocupação com a ausência dos cuidadores ou necessidade intensificada de segurança emocional para lidar com situações de autonomia.

Em Fobia Social, o resultado foi classificado como não clínico, afastando indicativos de inibição social importante, medo acentuado de exposição ou desconforto significativo em interações sociais. O domínio de Evitação Escolar também apresentou pontuação não clínica, não sugerindo recusa escolar ou ansiedade relevante associada ao ambiente escolar.

Em análise clínica, o perfil emocional de João Pedro revela sintomas ansiosos específicos e circunscritos ao domínio da ansiedade de separação, sem evidências de ansiedade generalizada, pânico, fobia social ou comprometimento ansioso global. Esse padrão sugere manifestação ansiosa mais situacional, centrada na necessidade de vínculo e segurança emocional diante do afastamento das figuras de referência. Há hipótese diagnóstica de sintomatologia ansiosa relacionada à ansiedade de separação, em nível circunscrito, devendo esse achado ser interpretado de forma integrada aos demais dados clínicos e contextuais da avaliação.
```

## Prompt operacional para a IA do sistema
```text
Gere a interpretação clínica do SCARED em linguagem técnica e fluida, sem repetições desnecessárias. Estruture o texto em: apresentação do instrumento, escore total, Pânico/Sintomas Somáticos, Ansiedade Generalizada, Ansiedade de Separação, Fobia Social, Evitação Escolar e síntese final. Use a expressão “Em análise clínica” apenas uma vez, no parágrafo final. Não use o termo “informante”. Quando houver autorrelato e heterorrelato, compare convergência e divergência entre as versões. Não feche diagnóstico formal apenas com base no SCARED; utilize a formulação “há hipótese diagnóstica de...” quando houver achados clínicos relevantes.
```

## Regra final
Se a saída não deixar claro se a interpretação foi baseada em pais/responsáveis, autorrelato ou ambas as versões, ela deve ser considerada incompleta e precisa ser reescrita.
