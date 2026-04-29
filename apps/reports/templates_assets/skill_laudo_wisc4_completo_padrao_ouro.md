# skill_laudo_wisc4_completo_padrao_ouro.md

## 1. Nome da Skill

**Skill Mestre para Elaboração de Laudo Neuropsicológico Infantil/Adolescente com WISC-IV – Padrão Ouro Internacional**

Esta skill orienta a IA e o sistema na construção completa de laudos neuropsicológicos que utilizam o WISC-IV como bateria cognitiva principal, integrando anamnese, observações clínicas, testes cognitivos, atencionais, executivos, mnésicos, emocionais, comportamentais e sociais.

A skill não deve gerar apenas a interpretação do WISC-IV. Ela deve produzir o laudo completo, com estrutura fixa, linguagem técnica, integração clínica entre instrumentos, hipótese diagnóstica e controle de qualidade compatível com auditoria rigorosa.

## 2. Finalidade

Padronizar a geração completa do laudo neuropsicológico infantil/adolescente, garantindo:

- organização documental compatível com avaliação psicológica;
- linguagem técnica, clara, objetiva e auditável;
- integração entre resultados de testes, anamnese e observações clínicas;
- redução de contradições diagnósticas;
- eliminação de nomes de outros pacientes;
- eliminação de resíduos de tabelas ou gráficos após as referências;
- uso consistente de hipótese diagnóstica;
- produção de texto em padrão ouro internacional.

## 3. Escopo da Skill

Esta skill deve ser usada quando o laudo envolver o WISC-IV e, conforme os instrumentos aplicados, qualquer combinação dos seguintes testes:

- WISC-IV – Escala Wechsler de Inteligência para Crianças – Quarta Edição;
- BPA-2 – Bateria Psicológica para Avaliação da Atenção;
- RAVLT – Rey Auditory Verbal Learning Test;
- FDT – Teste dos Cinco Dígitos;
- E-TDAH-PAIS;
- E-TDAH-AD;
- SCARED, versão autorrelato e/ou responsável;
- EPQ-J;
- SRS-2, versão idade escolar, pré-escolar ou heterorrelato;
- outros instrumentos complementares informados no caso.

A skill deve funcionar como um orquestrador clínico-documental do laudo inteiro.

## 4. Princípios Obrigatórios

### 4.1. Princípio de fidelidade aos dados

A IA nunca deve inventar resultados, nomes, datas, classificações, diagnósticos ou instrumentos. Quando um dado não estiver disponível, deve usar marcador técnico interno, como:

```text
[DADO NÃO INFORMADO]
```

Nunca substituir informação ausente por inferência não sustentada.

### 4.2. Princípio de consistência nominal

Antes de gerar qualquer texto, a IA deve identificar:

```json
{
  "nome_completo": "",
  "nome_de_uso": "",
  "sexo": "",
  "idade": "",
  "escolaridade": ""
}
```

Regras:

- usar nome completo apenas na identificação e na conclusão geral quando necessário;
- nas seções descritivas, usar preferencialmente o primeiro nome ou nome de uso indicado;
- nunca permitir nomes de pacientes de modelos anteriores;
- executar varredura final para detectar nomes estranhos ao caso.

### 4.3. Princípio de conclusão clínica integrada

A conclusão deve integrar:

- resultados do WISC-IV;
- funcionamento atencional;
- funções executivas;
- memória e aprendizagem;
- linguagem;
- gnosias e praxias;
- escalas emocionais e comportamentais;
- anamnese;
- observações clínicas;
- relatórios escolares ou clínicos, quando houver.

A conclusão nunca deve ser apenas uma repetição das seções anteriores. Deve sintetizar o raciocínio clínico.

### 4.4. Princípio de cautela diagnóstica

A IA deve usar a expressão:

```text
há hipótese diagnóstica de...
```

quando os dados sustentarem uma hipótese clínica, evitando formulações categóricas quando a decisão final depender de integração médica, psiquiátrica, neurológica, escolar ou longitudinal.

### 4.5. Uso obrigatório de DSM-5-TR™

Sempre que o DSM for citado, utilizar:

```text
DSM-5-TR™
```

Nunca utilizar apenas DSM-5.

### 4.6. Evitar termos obsoletos no TEA

Quando houver hipótese diagnóstica de Transtorno do Espectro Autista, utilizar níveis de suporte:

- TEA, Nível 1 de suporte;
- TEA, Nível 2 de suporte;
- TEA, Nível 3 de suporte.

Evitar TEA leve, moderado ou severo como nomenclatura diagnóstica principal.

## 5. Estrutura Obrigatória do Laudo

A skill deve organizar o laudo completo na seguinte ordem:

```text
1. IDENTIFICAÇÃO
   1.1 Identificação do laudo
   1.2 Identificação do paciente

2. DESCRIÇÃO DA DEMANDA
   2.1 Motivo do encaminhamento

3. PROCEDIMENTOS
   3.1 Sessões realizadas
   3.2 Instrumentos utilizados

4. ANÁLISE
   4.1 Anamnese
   4.2 História pessoal
   4.3 História perinatal
   4.4 Desenvolvimento motor
   4.5 Desenvolvimento linguístico
   4.6 Desenvolvimento socioemocional
   4.7 Histórico médico
   4.8 Sono e alimentação
   4.9 Escolaridade e funcionamento acadêmico
   4.10 Observações clínicas durante a avaliação

5. ANÁLISE QUALITATIVA
   5.1 WISC-IV – Capacidade Cognitiva Global
   5.2 Desempenho nos índices fatoriais
   5.3 Subescalas WISC-IV
      5.3.1 Funções Executivas
      5.3.2 Linguagem
      5.3.3 Gnosias e Praxias
      5.3.4 Memória e Aprendizagem

6. BPA-2 – Atenção

7. RAVLT – Memória Verbal e Aprendizagem

8. FDT – Processos Automáticos e Controlados

9. E-TDAH-PAIS

10. E-TDAH-AD

11. SCARED

12. EPQ-J

13. SRS-2

14. CONCLUSÃO
   14.1 Síntese clínica integrada
   14.2 Hipótese Diagnóstica

15. SUGESTÕES DE CONDUTA (ENCAMINHAMENTOS)

16. REFERÊNCIA BIBLIOGRÁFICA
```

Se algum teste não foi aplicado, remover a seção correspondente e renumerar o laudo.

## 6. Configuração Formal do Documento

Quando a skill for usada para geração de documento Word ou PDF, aplicar:

```json
{
  "fonte_principal": "Times New Roman",
  "tamanho_fonte_corpo": 12,
  "alinhamento_corpo": "justificado",
  "espacamento_linha": 1.15,
  "espacamento_antes": 0,
  "espacamento_depois": 6,
  "margem_superior_cm": 3,
  "margem_esquerda_cm": 2,
  "margem_inferior_cm": 2,
  "margem_direita_cm": 2,
  "fonte_legenda": "Times New Roman",
  "tamanho_legenda": 8,
  "estilo_legenda": "itálico",
  "posicao_legenda": "abaixo da tabela ou gráfico"
}
```

Não usar linhas divisórias longas entre seções.

## 7. Procedimentos

### 7.1. Modelo textual dos instrumentos

Usar o seguinte padrão para listar instrumentos:

```text
• Escala Wechsler de Inteligência para Crianças – Quarta Edição (WISC-IV), utilizada para avaliar o funcionamento intelectual global, os índices fatoriais de compreensão verbal, organização perceptual, memória operacional e velocidade de processamento, além de fornecer indicadores do perfil cognitivo da criança ou adolescente.
• Bateria Psicológica para Avaliação da Atenção – BPA-2, utilizada para investigar a eficiência dos sistemas atencionais, incluindo atenção concentrada, alternada, dividida e atenção geral.
• Rey Auditory Verbal Learning Test – RAVLT, utilizado para avaliar aprendizagem verbal, memória episódica auditivo-verbal, retenção, reconhecimento e resistência à interferência.
• Teste dos Cinco Dígitos – FDT, destinado à avaliação da velocidade de processamento, controle inibitório, flexibilidade cognitiva e alternância atencional.
• Escala de Transtorno de Déficit de Atenção e Hiperatividade – versão pais ou responsáveis (E-TDAH-PAIS), utilizada para identificar manifestações comportamentais associadas à atenção, hiperatividade, impulsividade, regulação emocional e comportamento adaptativo.
• Escala de Transtorno de Déficit de Atenção e Hiperatividade – Autorrelato (E-TDAH-AD), utilizada para investigar sintomas autorreferidos de desatenção, hiperatividade, impulsividade, aspectos emocionais e autorregulação da atenção, motivação e ação.
• Screen for Child Anxiety Related Emotional Disorders – SCARED, utilizado para rastrear sintomas ansiosos em crianças e adolescentes, incluindo pânico/sintomas somáticos, ansiedade generalizada, ansiedade de separação, fobia social e evitação escolar.
• Inventário de Personalidade de Eysenck para Jovens – EPQ-J, utilizado para avaliar traços de personalidade nos fatores Psicoticismo, Extroversão, Neuroticismo e Sinceridade.
• Escala de Responsividade Social – Segunda Edição (SRS-2), utilizada para rastrear dificuldades em percepção social, cognição social, comunicação social, motivação social, padrões restritos e repetitivos e funcionamento social global.
```

Remover da lista qualquer teste não aplicado.

## 8. Módulo WISC-IV

### 8.1. Dados de entrada

```json
{
  "wisc4": {
    "qit": null,
    "icv": null,
    "iop": null,
    "imo": null,
    "ivp": null,
    "gai": null,
    "cpi": null,
    "subtestes": {
      "semelhancas": {"escore_obtido": null, "classificacao": ""},
      "vocabulario": {"escore_obtido": null, "classificacao": ""},
      "compreensao": {"escore_obtido": null, "classificacao": ""},
      "cubos": {"escore_obtido": null, "classificacao": ""},
      "conceitos_figurativos": {"escore_obtido": null, "classificacao": ""},
      "raciocinio_matricial": {"escore_obtido": null, "classificacao": ""},
      "digitos": {"escore_obtido": null, "classificacao": ""},
      "sequencia_numeros_letras": {"escore_obtido": null, "classificacao": ""},
      "codigos": {"escore_obtido": null, "classificacao": ""},
      "procurar_simbolos": {"escore_obtido": null, "classificacao": ""}
    }
  }
}
```

### 8.2. Classificação dos pontos compostos

Usar a classificação:

```text
≤ 69 = Extremamente Baixo
70–79 = Limítrofe
80–89 = Média Inferior
90–109 = Média
110–119 = Média Superior
120–129 = Superior
≥ 130 = Muito Superior
```

### 8.3. Texto-base do WISC-IV

```text
A avaliação neuropsicológica de [NOME], por meio da Escala Wechsler de Inteligência para Crianças – Quarta Edição (WISC-IV), possibilitou a análise do funcionamento intelectual global e dos principais domínios cognitivos avaliados. O desempenho deve ser interpretado considerando a integração entre os índices fatoriais, os subtestes, as observações clínicas e os dados da história de desenvolvimento.
```

### 8.4. Interpretação dos índices

#### ICV – Compreensão Verbal

```text
O Índice de Compreensão Verbal (ICV = [VALOR]) situou-se na faixa [CLASSIFICAÇÃO], indicando [INTERPRETAÇÃO CLÍNICA]. Esse índice avalia conhecimento verbal adquirido, raciocínio verbal, formação de conceitos, compreensão de informações linguísticas e expressão verbal de ideias.
```

#### IOP – Organização Perceptual

```text
O Índice de Organização Perceptual (IOP = [VALOR]) situou-se na faixa [CLASSIFICAÇÃO], indicando [INTERPRETAÇÃO CLÍNICA]. Esse índice avalia raciocínio não verbal, análise visuoespacial, integração perceptiva, solução de problemas visuais e organização de estímulos complexos.
```

#### IMO – Memória Operacional

```text
O Índice de Memória Operacional (IMO = [VALOR]) situou-se na faixa [CLASSIFICAÇÃO], indicando [INTERPRETAÇÃO CLÍNICA]. Esse índice avalia atenção auditiva, retenção temporária, manipulação mental de informações, controle atencional ativo e organização sequencial.
```

#### IVP – Velocidade de Processamento

```text
O Índice de Velocidade de Processamento (IVP = [VALOR]) situou-se na faixa [CLASSIFICAÇÃO], indicando [INTERPRETAÇÃO CLÍNICA]. Esse índice avalia rapidez perceptual, discriminação visual, coordenação visuomotora, eficiência gráfica e execução sob limite de tempo.
```

#### QIT – Quociente de Inteligência Total

```text
O Quociente de Inteligência Total (QIT = [VALOR]) foi classificado como [CLASSIFICAÇÃO], refletindo [SÍNTESE DO FUNCIONAMENTO INTELECTUAL GLOBAL]. Quando houver discrepâncias clinicamente relevantes entre os índices, o QIT deve ser interpretado com cautela, considerando o perfil heterogêneo de desempenho.
```

#### GAI e CPI, quando disponíveis

```text
O Índice de Aptidão Geral (GAI = [VALOR]) foi classificado como [CLASSIFICAÇÃO], oferecendo uma estimativa das habilidades de raciocínio verbal e perceptual menos influenciada por memória operacional e velocidade de processamento.
```

```text
O Índice de Competência Cognitiva (CPI = [VALOR]) foi classificado como [CLASSIFICAÇÃO], refletindo a eficiência cognitiva associada à memória operacional e à velocidade de processamento, domínios diretamente relacionados ao rendimento acadêmico e à execução de tarefas estruturadas.
```

## 9. Subescalas WISC-IV por Domínio Clínico

### 9.1. Funções Executivas

Subtestes preferenciais:

- Semelhanças;
- Conceitos Figurativos;
- Compreensão;
- Raciocínio Matricial.

Texto-base:

```text
A avaliação das funções executivas de [NOME] foi realizada por meio de subtestes do WISC-IV que investigam raciocínio abstrato, categorização conceitual, julgamento social, raciocínio lógico-visual, flexibilidade cognitiva e resolução de problemas. Esses domínios estão associados ao funcionamento de circuitos pré-frontais e frontoparietais envolvidos no planejamento, monitoramento e adaptação do comportamento.
```

Fechamento:

```text
Em análise clínica, o desempenho de [NOME] nesse domínio sugere [SÍNTESE], com impacto potencial em tarefas que exigem planejamento, abstração, organização de estratégias, flexibilidade cognitiva e solução de problemas.
```

### 9.2. Linguagem

Subtestes preferenciais:

- Semelhanças;
- Vocabulário;
- Compreensão;
- Fala espontânea.

Texto-base:

```text
A avaliação da linguagem de [NOME] foi realizada por meio dos subtestes Semelhanças, Vocabulário e Compreensão, complementada pela observação clínica da fala espontânea. Esses indicadores permitem examinar conceituação verbal, repertório lexical, formulação linguística, compreensão de normas sociais e organização expressiva da linguagem.
```

Fechamento:

```text
Em análise clínica, o perfil linguístico de [NOME] indica [SÍNTESE], devendo ser interpretado em conjunto com o nível de atenção, memória operacional, escolaridade e condições neurológicas ou emocionais associadas.
```

### 9.3. Gnosias e Praxias

Subtestes preferenciais:

- Raciocínio Matricial;
- Cubos;
- Figuras Complexas de Rey, se aplicado.

Texto-base:

```text
A avaliação das habilidades visuoperceptivas e construtivas de [NOME] foi realizada por meio de tarefas que investigam percepção visual, integração visuomotora, análise de padrões, organização espacial e planejamento construtivo.
```

Fechamento:

```text
Em análise clínica, os resultados sugerem [SÍNTESE], com possíveis repercussões em atividades que exigem cópia, construção, organização espacial, escrita, geometria, desenho e manipulação de estímulos visuais.
```

### 9.4. Memória e Aprendizagem

Subtestes preferenciais:

- Dígitos;
- Sequência de Números e Letras;
- RAVLT, quando aplicado.

Texto-base:

```text
A avaliação da memória e aprendizagem de [NOME] incluiu medidas de memória operacional auditiva, atenção sustentada, retenção imediata, manipulação de informações e aprendizagem verbal. Esses processos são fundamentais para aquisição escolar, acompanhamento de instruções e organização sequencial do pensamento.
```

Fechamento:

```text
Em análise clínica, o desempenho indica [SÍNTESE], com impacto potencial na aprendizagem, na retenção de conteúdos, na evocação de informações e na execução de tarefas que exigem processamento sequencial.
```

## 10. Módulo BPA-2

### 10.1. Dados de entrada

```json
{
  "bpa2": {
    "atencao_concentrada": {"pontos": null, "percentil": null, "classificacao": ""},
    "atencao_dividida": {"pontos": null, "percentil": null, "classificacao": ""},
    "atencao_alternada": {"pontos": null, "percentil": null, "classificacao": ""},
    "atencao_geral": {"pontos": null, "percentil": null, "classificacao": ""}
  }
}
```

### 10.2. Texto-base

```text
A Bateria Psicológica para Avaliação da Atenção – BPA-2 tem como objetivo mensurar a capacidade geral de atenção e avaliar diferentes sistemas atencionais, incluindo atenção concentrada, atenção dividida, atenção alternada e atenção geral.
```

### 10.3. Modelo interpretativo

```text
A avaliação da atenção de [NOME] por meio da BPA-2 evidenciou desempenho [SÍNTESE GLOBAL]. A atenção concentrada, responsável pela seleção e manutenção do foco em uma fonte de informação diante de distratores, apresentou classificação [CLASSIFICAÇÃO]. A atenção dividida, relacionada ao gerenciamento simultâneo de múltiplas demandas, apresentou classificação [CLASSIFICAÇÃO]. A atenção alternada, associada à capacidade de mudar o foco entre estímulos ou regras, apresentou classificação [CLASSIFICAÇÃO]. A atenção geral, que integra os diferentes domínios avaliados, situou-se na faixa [CLASSIFICAÇÃO].

Em análise clínica, esse perfil indica [SÍNTESE FUNCIONAL], com possíveis repercussões no acompanhamento de instruções, organização das atividades, rendimento escolar, controle executivo e autorregulação cognitiva.
```

## 11. Módulo RAVLT

### 11.1. Dados de entrada

```json
{
  "ravlt": {
    "A1": null,
    "A2": null,
    "A3": null,
    "A4": null,
    "A5": null,
    "B1": null,
    "A6": null,
    "A7": null,
    "R": null,
    "ALT": null,
    "RET": null,
    "IP": null,
    "IR": null,
    "esperado": {},
    "minimo": {}
  }
}
```

### 11.2. Texto-base

```text
O Rey Auditory Verbal Learning Test – RAVLT é utilizado para avaliar memória episódica verbal, aprendizagem auditivo-verbal, curva de aquisição, retenção, evocação após interferência, reconhecimento e resistência à interferência.
```

### 11.3. Estrutura interpretativa obrigatória

A interpretação deve ser dividida em:

```text
Memória Imediata e Curva de Aprendizagem
Interferência e Retenção
Reconhecimento
Índices Derivados
Em análise clínica
```

### 11.4. Fechamento clínico

```text
Em análise clínica, o desempenho de [NOME] no RAVLT evidencia [SÍNTESE], caracterizado por [CURVA DE APRENDIZAGEM], [RETENÇÃO], [INTERFERÊNCIA] e [RECONHECIMENTO]. Esse padrão sugere [IMPACTO FUNCIONAL] em tarefas escolares e cotidianas que exigem aprendizagem verbal, memorização sequencial, evocação espontânea e recuperação de informações ao longo do tempo.
```

## 12. Módulo FDT

### 12.1. Dados de entrada

```json
{
  "fdt": {
    "leitura": {"tempo_medio": null, "tempo_obtido": null, "erros": null, "desempenho": null, "classificacao": ""},
    "contagem": {"tempo_medio": null, "tempo_obtido": null, "erros": null, "desempenho": null, "classificacao": ""},
    "escolha": {"tempo_medio": null, "tempo_obtido": null, "erros": null, "desempenho": null, "classificacao": ""},
    "alternancia": {"tempo_medio": null, "tempo_obtido": null, "erros": null, "desempenho": null, "classificacao": ""},
    "inibicao": {"tempo_medio": null, "tempo_obtido": null, "desempenho": null, "classificacao": ""},
    "flexibilidade": {"tempo_medio": null, "tempo_obtido": null, "desempenho": null, "classificacao": ""}
  }
}
```

### 12.2. Texto-base

```text
O Teste dos Cinco Dígitos – FDT permite avaliar processos automáticos e processos controlados, incluindo velocidade de processamento, controle inibitório, alternância atencional e flexibilidade cognitiva.
```

### 12.3. Estrutura interpretativa obrigatória

```text
Processos Automáticos
Processos Controlados
Análise dos Erros
Em análise clínica
```

### 12.4. Fechamento clínico

```text
Em análise clínica, o desempenho de [NOME] no FDT revela [SÍNTESE], com impacto em tarefas que exigem rapidez mental, controle inibitório, alternância de critérios, flexibilidade cognitiva, monitoramento de respostas e adaptação a mudanças.
```

## 13. Módulo E-TDAH-PAIS

### 13.1. Dados de entrada

```json
{
  "etdah_pais": {
    "fator_1_regulacao_emocional": {"percentil": null, "classificacao": ""},
    "fator_2_hiperatividade_impulsividade": {"percentil": null, "classificacao": ""},
    "fator_3_comportamento_adaptativo": {"percentil": null, "classificacao": ""},
    "fator_4_atencao": {"percentil": null, "classificacao": ""},
    "escore_geral": {"percentil": null, "classificacao": ""}
  }
}
```

### 13.2. Regra interpretativa de prejuízo

Para E-TDAH-PAIS e E-TDAH-AD:

```text
Percentil ≥ 85 → Superior → Prejuízo Grave
Percentil ≥ 65 → Média Superior → Prejuízo Moderado
Percentil ≥ 45 → Média → Sem Prejuízo
Percentil ≥ 25 → Média Inferior → Sem Prejuízo
Percentil < 25 → Inferior → Sem Prejuízo
```

Classificações inferior, média inferior e média não indicam déficit clínico nesses instrumentos.

### 13.3. Fechamento clínico

```text
Em análise clínica, os resultados do E-TDAH-PAIS indicam que [NOME] apresenta [SÍNTESE], com prejuízos clinicamente relevantes apenas nos domínios classificados como média superior ou superior. Esses achados devem ser interpretados em conjunto com os dados objetivos da avaliação neuropsicológica, observações clínicas e informações escolares.
```

## 14. Módulo E-TDAH-AD

### 14.1. Dados de entrada

```json
{
  "etdah_ad": {
    "fator_1_desatencao": {"percentil": null, "classificacao": ""},
    "fator_2_impulsividade": {"percentil": null, "classificacao": ""},
    "fator_3_aspectos_emocionais": {"percentil": null, "classificacao": ""},
    "fator_4_autorregulacao_atencao_motivacao_acao": {"percentil": null, "classificacao": ""},
    "fator_5_hiperatividade": {"percentil": null, "classificacao": ""}
  }
}
```

### 14.2. Fechamento clínico

```text
Em análise clínica, os resultados da E-TDAH-AD indicam [SÍNTESE]. Quando houver elevação clinicamente significativa em Desatenção e/ou Hiperatividade, esses dados devem ser cruzados com BPA-2, FDT, observações clínicas e prejuízo funcional antes de formular hipótese diagnóstica de TDAH.
```

### 14.3. Regra para hipótese diagnóstica de TDAH

A IA só deve sugerir hipótese diagnóstica de TDAH quando houver convergência entre múltiplas fontes, por exemplo:

```text
- prejuízo objetivo em atenção na BPA-2;
- prejuízo executivo no FDT;
- elevação clínica em E-TDAH-AD ou E-TDAH-PAIS;
- queixas funcionais consistentes na anamnese ou escola;
- observações clínicas compatíveis.
```

Modelo de frase:

```text
Diante da convergência entre os achados objetivos de atenção e funções executivas, os indicadores comportamentais e os prejuízos funcionais descritos, há hipótese diagnóstica de Transtorno do Déficit de Atenção e Hiperatividade (TDAH), [apresentação], conforme critérios do DSM-5-TR™.
```

## 15. Módulo SCARED

### 15.1. Dados de entrada

```json
{
  "scared": {
    "autorrelato": {
      "panico_sintomas_somaticos": {"percentil": null, "classificacao": ""},
      "ansiedade_generalizada": {"percentil": null, "classificacao": ""},
      "ansiedade_separacao": {"percentil": null, "classificacao": ""},
      "fobia_social": {"percentil": null, "classificacao": ""},
      "evitacao_escolar": {"percentil": null, "classificacao": ""},
      "total": {"percentil": null, "classificacao": ""}
    },
    "responsavel": {
      "panico_sintomas_somaticos": {"clinico": null},
      "ansiedade_generalizada": {"clinico": null},
      "ansiedade_separacao": {"clinico": null},
      "fobia_social": {"clinico": null},
      "evitacao_escolar": {"clinico": null},
      "total": {"clinico": null}
    }
  }
}
```

### 15.2. Estrutura interpretativa

```text
Autorrelato
Relato do responsável
Interpretação Clínica
Hipótese Diagnóstica
```

### 15.3. Fechamento clínico

```text
Em análise clínica, os resultados do SCARED indicam [SÍNTESE], com destaque para [DOMÍNIOS ELEVADOS]. A comparação entre autorrelato e relato do responsável evidencia [CONVERGÊNCIA OU DIVERGÊNCIA], sugerindo que parte do sofrimento ansioso pode se manifestar de forma internalizada, seletiva ou situacional.
```

### 15.4. Hipóteses possíveis

Usar somente quando sustentadas pelos dados:

```text
há hipótese diagnóstica de Transtorno de Ansiedade Generalizada
há hipótese diagnóstica de Transtorno de Ansiedade Social
há hipótese diagnóstica de Transtorno de Ansiedade de Separação
há hipótese diagnóstica de Evitação Escolar associada à ansiedade
```

## 16. Módulo EPQ-J

### 16.1. Dados de entrada

```json
{
  "epqj": {
    "psicoticismo_p": {"percentil": null, "classificacao": ""},
    "extroversao_e": {"percentil": null, "classificacao": ""},
    "neuroticismo_n": {"percentil": null, "classificacao": ""},
    "sinceridade_s": {"percentil": null, "classificacao": ""}
  }
}
```

### 16.2. Interpretação dos fatores

#### Psicoticismo

Interpretar como rigidez, objetividade emocional, menor flexibilidade interpessoal ou estilo comportamental mais reservado. Não associar automaticamente a psicose.

#### Extroversão

Interpretar como busca por interação, sociabilidade, energia social ou introversão, conforme classificação.

#### Neuroticismo

Interpretar como instabilidade emocional, sensibilidade ao estresse, ansiedade, reatividade emocional e vulnerabilidade afetiva.

#### Sinceridade

Interpretar como indicador de validade e estilo de resposta. Não tratar como traço moral.

### 16.3. Fechamento clínico

```text
Em análise clínica, o perfil de [NOME] no EPQ-J revela [SÍNTESE], devendo ser compreendido como indicador de estilo emocional e comportamental, e não como diagnóstico isolado. Os achados devem ser integrados aos resultados do SCARED, observações clínicas e dados da anamnese.
```

## 17. Módulo SRS-2

### 17.1. Dados de entrada

```json
{
  "srs2": {
    "versao": "idade_escolar | pre_escolar | adulto_autorrelato | heterorrelato",
    "percepcao_social": {"t_score": null, "percentil": null, "classificacao": ""},
    "cognicao_social": {"t_score": null, "percentil": null, "classificacao": ""},
    "comunicacao_social": {"t_score": null, "percentil": null, "classificacao": ""},
    "motivacao_social": {"t_score": null, "percentil": null, "classificacao": ""},
    "padroes_restritos_repetitivos": {"t_score": null, "percentil": null, "classificacao": ""},
    "comunicacao_interacao_social": {"t_score": null, "percentil": null, "classificacao": ""},
    "total": {"t_score": null, "percentil": null, "classificacao": ""}
  }
}
```

### 17.2. Classificação dos escores T

```text
T ≤ 59 = Dentro dos limites normais
T 60–65 = Nível leve
T 66–75 = Nível moderado
T ≥ 76 = Nível severo
```

### 17.3. Regra de cautela para TEA

A SRS-2 é instrumento de rastreio. Ela não fecha diagnóstico de TEA isoladamente.

Antes de sugerir hipótese diagnóstica de TEA, verificar:

```text
- prejuízo qualitativo persistente em reciprocidade socioemocional;
- prejuízo em comunicação social/pragmática;
- presença de padrões restritos e repetitivos persistentes;
- início no desenvolvimento;
- prejuízo funcional;
- exclusão de explicações mais parcimoniosas, como deficiência intelectual, ansiedade, epilepsia, privação escolar, alterações sensoriais isoladas ou dificuldades de linguagem.
```

### 17.4. Fechamento clínico quando NÃO houver TEA

```text
Em análise clínica, embora a SRS-2 indique dificuldades no funcionamento social, tais achados devem ser interpretados à luz do funcionamento cognitivo global, dos sintomas emocionais, da história clínica e das limitações adaptativas observadas. Quando as dificuldades sociais forem mais bem explicadas por rebaixamento intelectual, ansiedade, condição neurológica ou prejuízos executivos, não há elementos suficientes para sustentar hipótese diagnóstica de Transtorno do Espectro Autista.
```

### 17.5. Fechamento clínico quando houver TEA

```text
Em análise clínica, os resultados da SRS-2, integrados à anamnese, observações clínicas e histórico do desenvolvimento, indicam prejuízos qualitativos persistentes na comunicação social e na reciprocidade socioemocional, associados a padrões restritos e repetitivos de comportamento. Dessa forma, há hipótese diagnóstica de Transtorno do Espectro Autista (TEA), Nível [1/2/3] de suporte, conforme critérios do DSM-5-TR™.
```

## 18. Regras de Integração Diagnóstica

### 18.1. Deficiência Intelectual

Sugerir hipótese diagnóstica de Deficiência Intelectual quando houver convergência entre:

```text
- QIT extremamente baixo ou limítrofe com prejuízo funcional significativo;
- prejuízos adaptativos descritos na anamnese, escola ou escalas;
- dificuldades acadêmicas amplas;
- comprometimento em múltiplos domínios cognitivos;
- início no período do desenvolvimento.
```

Modelo:

```text
há hipótese diagnóstica de Deficiência Intelectual, considerando o funcionamento intelectual global significativamente rebaixado, os prejuízos cognitivos multidimensionais e as limitações adaptativas descritas no contexto familiar, escolar e clínico.
```

### 18.2. TDAH

Sugerir TDAH apenas quando houver convergência entre testes objetivos, escalas e prejuízo funcional.

Apresentações possíveis:

```text
TDAH, apresentação predominantemente desatenta
TDAH, apresentação predominantemente hiperativa/impulsiva
TDAH, apresentação combinada
```

Não concluir TDAH apenas por baixa atenção em teste cognitivo se houver explicação melhor, como Deficiência Intelectual, ansiedade grave, epilepsia, privação de sono, depressão ou uso medicamentoso.

### 18.3. Transtornos de ansiedade

Sugerir quando houver convergência entre:

```text
- SCARED elevado ou clínico;
- EPQ-J com neuroticismo elevado;
- anamnese com preocupações, evitação, sintomas somáticos ou retraimento;
- prejuízo funcional escolar, social ou familiar.
```

### 18.4. TEA

Sugerir apenas se houver evidências qualitativas claras além da SRS-2.

Não sugerir TEA quando as dificuldades sociais forem mais bem explicadas por:

```text
- Deficiência Intelectual;
- ansiedade social;
- epilepsia ou outra condição neurológica;
- dificuldades de linguagem;
- baixa velocidade de processamento;
- retraimento emocional;
- prejuízo executivo global.
```

## 19. Conclusão Geral

### 19.1. Regra de abertura

A conclusão geral deve iniciar diretamente com:

```text
[NOME] apresenta...
```

Não iniciar com:

```text
Diante da análise integrada...
```

Essa formulação pode aparecer depois, no corpo final da conclusão, com o verbo correto:

```text
Diante da integração dos resultados das testagens, das observações clínicas e dos dados da anamnese, conclui-se que...
```

Nunca usar “verifica-se que” nesse trecho.

### 19.2. Estrutura da conclusão

A conclusão deve seguir esta ordem:

```text
1. Síntese do funcionamento intelectual global.
2. Síntese dos índices do WISC-IV.
3. Atenção e funções executivas.
4. Memória e aprendizagem.
5. Linguagem, gnosias e praxias.
6. Aspectos emocionais e comportamentais.
7. Funcionamento social e SRS-2.
8. Integração clínica final.
9. Hipótese Diagnóstica.
10. Ressalva sobre natureza dinâmica do funcionamento humano.
```

### 19.3. Modelo de conclusão

```text
[NOME] apresenta funcionamento neuropsicológico caracterizado por [SÍNTESE GERAL], com [PRINCIPAIS DOMÍNIOS PRESERVADOS] e [PRINCIPAIS DOMÍNIOS PREJUDICADOS].

Na Escala Wechsler de Inteligência para Crianças – Quarta Edição (WISC-IV), apresentou Quociente de Inteligência Total classificado como [CLASSIFICAÇÃO], com perfil [homogêneo/heterogêneo], evidenciando [SÍNTESE DOS ÍNDICES]. Esse padrão sugere [IMPACTO FUNCIONAL].

No domínio atencional e executivo, os resultados indicam [SÍNTESE BPA/FDT/WISC], com repercussões em [IMPACTOS].

A avaliação da memória e aprendizagem evidenciou [SÍNTESE RAVLT/WISC], sugerindo [IMPACTO].

Nos aspectos emocionais e comportamentais, os instrumentos aplicados indicaram [SÍNTESE E-TDAH/SCARED/EPQ-J], compondo um perfil [DESCRIÇÃO].

Na avaliação do funcionamento social, os resultados da SRS-2 indicaram [SÍNTESE], devendo ser interpretados em conjunto com [FATORES EXPLICATIVOS].

Diante da integração dos resultados das testagens, das observações clínicas e dos dados da anamnese, conclui-se que [NOME COMPLETO OU NOME DE USO] apresenta [SÍNTESE DIAGNÓSTICA].

Hipótese Diagnóstica:
- há hipótese diagnóstica de [CONDIÇÃO 1], conforme critérios do DSM-5-TR™;
- há hipótese diagnóstica de [CONDIÇÃO 2], quando aplicável.

Ressalta-se que o ser humano possui natureza dinâmica, não definitiva e não cristalizada. Sendo assim, os resultados aqui expostos dizem respeito ao funcionamento cognitivo, emocional, comportamental e adaptativo no momento presente, podendo haver alterações posteriores, a depender das contingências ambientais vivenciadas e do acompanhamento recebido.
```

## 20. Sugestões de Conduta

### 20.1. Regras

As sugestões devem ser:

- técnicas;
- objetivas;
- alinhadas às hipóteses diagnósticas;
- sem excesso de repetição;
- sem prometer resultado;
- sem indicar condutas fora do escopo psicológico de forma prescritiva.

### 20.2. Modelo

```text
• Recomenda-se retorno ao neuropediatra, psiquiatra infantil ou médico assistente, para integração dos achados da avaliação neuropsicológica, definição diagnóstica e planejamento terapêutico quando necessário.
• Indica-se acompanhamento psicológico com foco em autorregulação emocional, manejo da ansiedade, tolerância à frustração, habilidades sociais e estratégias de enfrentamento adaptativo.
• Sugere-se acompanhamento psicopedagógico especializado, direcionado às dificuldades acadêmicas, com estratégias compatíveis com o perfil cognitivo, ritmo de aprendizagem e necessidades específicas de [NOME].
• Recomenda-se orientação familiar, com psicoeducação sobre o perfil neuropsicológico identificado, estruturação de rotina, previsibilidade ambiental, reforço positivo e ajuste de expectativas.
• No contexto escolar, recomenda-se a implementação de adaptações pedagógicas, incluindo instruções claras e segmentadas, tempo ampliado para atividades e avaliações, redução de estímulos distratores, uso de recursos visuais e acompanhamento pedagógico individualizado, conforme necessidade.
• Quando houver prejuízos motores, visuoconstrutivos ou adaptativos, recomenda-se avaliação em Terapia Ocupacional, com foco em autonomia funcional, planejamento motor, organização da rotina e habilidades adaptativas.
• Quando houver alterações de fala, linguagem ou comunicação funcional, recomenda-se acompanhamento fonoaudiológico ou reavaliação dos objetivos terapêuticos.
```

Remover recomendações não aplicáveis ao caso.

## 21. Referência Bibliográfica

### 21.1. Regra

As referências devem aparecer em ordem alfabética, quando possível, e o laudo deve terminar na última referência bibliográfica.

Após a última referência, não pode existir:

- tabela bruta;
- gráfico bruto;
- planilha colada;
- resto de cálculo;
- dados de percentil soltos;
- texto de teste;
- cabeçalhos residuais.

### 21.2. Referências-base

```text
BENCZIK, E. B. P. Escala de Transtorno de Déficit de Atenção e Hiperatividade – Versão Pais (E-TDAH-PAIS). São Paulo: Casa do Psicólogo, 2005.

BIRMAHER, B. et al. Screen for Child Anxiety Related Emotional Disorders (SCARED): Scale construction and psychometric characteristics. Journal of the American Academy of Child and Adolescent Psychiatry, v. 36, n. 4, p. 545–553, 1997.

CONSELHO FEDERAL DE PSICOLOGIA (CFP). Resolução do CRP nº 6, de 29 de março de 2019, e nº 31, de 2022. Institui o Manual de Elaboração de Documentos Escritos produzidos pelo psicólogo, decorrentes de avaliação psicológica; regras do registro documental elaborado pela(o) psicóloga(o), decorrentes da prestação de serviços psicológicos, diretrizes para a Avaliação Psicológica, o uso de métodos, técnicas e instrumentos reconhecidos cientificamente para uso na prática profissional, assim como o uso de procedimentos e recursos auxiliares. Brasília: CFP, 2019.

CONSTANTINO, J. N.; GRUBER, C. P. Social Responsiveness Scale – Second Edition (SRS-2). Torrance, CA: Western Psychological Services, 2012.

EYSENCK, H. J.; EYSENCK, S. B. G. Manual of the Eysenck Personality Questionnaire Junior. London: Hodder & Stoughton, 1992.

LEZAK, M. D.; HOWIESON, D. B.; BIGLER, E. D.; TRANEL, D. Neuropsychological Assessment. 5. ed. New York: Oxford University Press, 2012.

RUEDA, F. J. M. Bateria Psicológica para Avaliação da Atenção – BPA-2. São Paulo: Vetor Editora, 2013.

SALLES, J. F.; FONSECA, R. P.; PARENTE, M. A. M. P. Teste dos Cinco Dígitos (FDT). São Paulo: Casa do Psicólogo, 2011.

STRAUSS, E.; SHERMAN, E. M. S.; SPREEN, O. A compendium of neuropsychological tests: Administration, norms, and commentary. 3. ed. New York: Oxford University Press, 2006.

WECHSLER, D. Escala de Inteligência Wechsler para Crianças – Quarta Edição (WISC-IV). São Paulo: Pearson, 2013.
```

Incluir apenas referências dos testes e autores efetivamente utilizados.

## 22. Checklist de Auditoria Final

Antes de entregar o laudo, a IA deve executar esta checagem:

```text
[ ] O nome do paciente está correto em todo o laudo.
[ ] Não há nome de outro paciente.
[ ] A idade, sexo, escolaridade e filiação estão consistentes.
[ ] Todos os testes listados em Procedimentos aparecem no corpo do laudo.
[ ] Nenhum teste não aplicado aparece no laudo.
[ ] As classificações dos testes estão coerentes com os dados informados.
[ ] As interpretações não contradizem os resultados.
[ ] O texto não repete excessivamente a mesma ideia.
[ ] A conclusão integra todos os domínios avaliados.
[ ] A hipótese diagnóstica aparece dentro da conclusão.
[ ] O DSM está escrito como DSM-5-TR™.
[ ] Não há uso de “verifica-se que” no trecho “Diante da integração...”.
[ ] Não há travessões longos no corpo do laudo.
[ ] Não há linhas divisórias entre seções.
[ ] As legendas estão abaixo de tabelas e gráficos.
[ ] As legendas usam fonte 8, itálico, quando em DOCX.
[ ] O documento termina na última referência bibliográfica.
[ ] Não existem resíduos de tabelas, gráficos ou dados brutos após as referências.
```

## 23. Regras de Estilo Linguístico

### 23.1. Preferir

```text
Em análise clínica, os resultados indicam...
O desempenho sugere...
Observa-se padrão compatível com...
Esse achado deve ser compreendido em conjunto com...
Os dados sustentam hipótese diagnóstica de...
```

### 23.2. Evitar

```text
De forma geral...
Do ponto de vista funcional...
Verifica-se que...
O paciente é...
Com certeza...
Diagnóstico fechado de...
```

### 23.3. Evitar repetição no início das frases

Não iniciar frases consecutivas com:

```text
No...
Na...
O paciente...
A paciente...
```

Variar a construção textual com:

```text
Observa-se...
Esse padrão...
Tal resultado...
Em tarefas que exigem...
A análise dos dados...
```

## 24. Saída Esperada da Skill

A skill deve gerar como saída:

```json
{
  "laudo_completo_markdown": "",
  "secoes": {
    "identificacao": "",
    "descricao_demanda": "",
    "procedimentos": "",
    "analise": "",
    "wisc4": "",
    "bpa2": "",
    "ravlt": "",
    "fdt": "",
    "etdah_pais": "",
    "etdah_ad": "",
    "scared": "",
    "epqj": "",
    "srs2": "",
    "conclusao": "",
    "sugestoes": "",
    "referencias": ""
  },
  "hipoteses_diagnosticas": [],
  "alertas_auditoria": [],
  "testes_aplicados": []
}
```

## 25. Regra Final

Esta skill deve priorizar precisão clínica, coerência documental e segurança técnica. O laudo não deve parecer colagem de testes. Deve funcionar como documento integrado de avaliação neuropsicológica, com raciocínio clínico claro, linguagem profissional, fundamentação compatível com auditoria e ausência de inconsistências formais.
