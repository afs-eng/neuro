# SKILL — Padronização do Laudo WISC-IV

## Objetivo
Padronizar a construção do capítulo **5. ANÁLISE QUALIDATIVA** e de suas subseções no laudo neuropsicológico, utilizando o **WISC-IV** como base principal.  
Nesta skill, **a estrutura textual é fixa** e **somente os valores, classificações e conteúdos variáveis do paciente devem ser substituídos**.

Baseado no modelo enviado pelo usuário. fileciteturn0file0

## Escopo atual
Esta skill trabalha **somente com o WISC-IV**, contemplando:

- 5. ANÁLISE QUALIDATIVA
- 5.1. Desempenho da paciente no WISC-IV
- 5.2. Subescalas WISC-IV
- 5.2.1. Função executiva
- 5.2.2. Linguagem
- 5.2.3. Gnosias e Praxias
- 5.2.4. Memória e Aprendizagem

## Regras gerais
1. A estrutura dos títulos e subtítulos deve ser mantida exatamente.
2. O texto-base da seção **5. ANÁLISE QUALIDATIVA** é fixo.
3. As descrições dos índices do WISC-IV são fixas.
4. A legenda do gráfico do WISC-IV é fixa.
5. O tamanho da fonte das legendas dos gráficos e das tabelas deve ser **9**.
6. O conteúdo variável deve se restringir a:
   - nome do paciente
   - sexo gramatical
   - QI Total
   - idade cognitiva estimada
   - valores dos índices
   - classificações dos índices
   - tabelas das subescalas
   - interpretações clínicas conforme os resultados obtidos
7. O texto deve manter linguagem técnica, formal e compatível com laudo neuropsicológico.
8. O nome do paciente pode ser adaptado conforme a regra vigente do caso, mas a estrutura do texto não deve ser alterada.
9. Não usar travessão longo no corpo do texto.
10. Sempre manter consistência entre:
    - índices do gráfico
    - valores descritos no texto
    - classificações
    - tabelas das subescalas
    - interpretações clínicas

---

## Entradas obrigatórias
A IA deve receber os seguintes dados estruturados:

```json
{
  "paciente": "Nome do paciente",
  "sexo_texto": "paciente",
  "qit": 61,
  "classificacao_qit": "Extremamente Baixo",
  "idade_cognitiva": "8 anos e 6 meses",
  "indices": {
    "icv": 84,
    "classificacao_icv": "Média Inferior",
    "iop": 61,
    "classificacao_iop": "Extremamente Baixo",
    "imo": 52,
    "classificacao_imo": "Extremamente Baixo",
    "ivp": 68,
    "classificacao_ivp": "Extremamente Baixo",
    "gai": 70,
    "classificacao_gai": "Limítrofe",
    "cpi": 58,
    "classificacao_cpi": "Extremamente Baixo"
  },
  "subescalas": {
    "funcao_executiva": [],
    "linguagem": [],
    "gnosias_praxias": [],
    "memoria_aprendizagem": []
  }
}
```

---

## Saída esperada
A IA deve gerar o texto final já estruturado no formato do laudo, incluindo:

- seção 5 com texto fixo + substituição dos valores
- seção 5.1 com gráfico
- legenda fixa do gráfico
- seção 5.2 com subtabelas
- legendas das tabelas
- interpretações clínicas padronizadas por domínio

# 1. Texto fixo da seção 5

## 5. ANÁLISE QUALIDATIVA
Usar exatamente este modelo:

```text
5. ANÁLISE QUALIDATIVA

Capacidade Cognitiva Global: A paciente obteve, a partir da escala WISC IV, QI Total (QIT {QIT}), ficando na classificação {CLASSIFICACAO_QIT}, quando comparado à média geral e com idade cognitiva estimada de {IDADE_COGNITIVA}. Em relação aos índices fatoriais (medidas mais apuradas da inteligência), apresentou os seguintes resultados:

- Compreensão Verbal (ICV) — {VALOR_ICV} — {CLASSIFICACAO_ICV} Avaliou o conhecimento verbal adquirido, o processo mental necessário para responder às questões formuladas, a capacidade de compreensão verbal e o raciocínio verbal.
- Organização Perceptual (IOP) — {VALOR_IOP} — {CLASSIFICACAO_IOP} Avaliou o raciocínio não verbal, a atenção para detalhes e a integração visomotora.
- Memória Operacional (IMO) — {VALOR_IMO} — {CLASSIFICACAO_IMO} Avaliou a atenção, a concentração e a memória operacional.
- Velocidade de Processamento (IVP) — {VALOR_IVP} — {CLASSIFICACAO_IVP} Avaliou a capacidade de em realizar tarefas que demandam rapidez e precisão na análise de estímulos visuais.
```

## Variáveis substituíveis
- `{QIT}`
- `{CLASSIFICACAO_QIT}`
- `{IDADE_COGNITIVA}`
- `{VALOR_ICV}`
- `{CLASSIFICACAO_ICV}`
- `{VALOR_IOP}`
- `{CLASSIFICACAO_IOP}`
- `{VALOR_IMO}`
- `{CLASSIFICACAO_IMO}`
- `{VALOR_IVP}`
- `{CLASSIFICACAO_IVP}`

---

# 2. Seção 5.1 — Gráfico do WISC-IV

## Título
```text
5.1. Desempenho da paciente no WISC-IV
```

## Elemento obrigatório
Inserir o gráfico com os seguintes índices:

- ICV
- IOP
- IMO
- IVP
- QI Total
- GAI
- CPI

## Regras visuais do gráfico
1. O gráfico deve seguir o modelo visual enviado.
2. Deve conter barras para:
   - ICV
   - IOP
   - IMO
   - IVP
   - QI Total
   - GAI
   - CPI
3. O eixo Y deve representar **Pontos Compostos**.
4. O gráfico deve apresentar as faixas visuais de classificação ao fundo, conforme o modelo.
5. O valor de cada índice deve aparecer associado à respectiva barra.
6. A legenda do gráfico deve aparecer abaixo.
7. **Fonte da legenda: tamanho 9.**

## Legenda fixa do gráfico
Usar exatamente este texto:

```text
Gráfico 1 WISC-IV - INDICES DE QIS: Índice de Compreensão Verbal (ICV): composto por provas que avaliam as habilidades verbais por meio do raciocínio, compreensão e conceituação. Índice de Organização Perceptual (IOP): constituído por atividades que examinam o grau e a qualidade do contato não verbal do indivíduo com o ambiente, assim como a capacidade de integrar estímulos perceptuais e respostas motoras pertinentes, o nível de rapidez com o qual executa uma atividade e o modo como avalia informações visuoespaciais. Índice de Memória Operacional (IMO): formado por provas que analisam atenção, concentração e memória de trabalho. Índice de Velocidade de Processamento (IVP): constitui-se de atividades que avaliam agilidade mental e processamento grafomotor. Coeficiente de Inteligência Total (QIT): avalia o nível geral do funcionamento intelectual.
```

---

# 3. Interpretação clínica da seção 5.1
Após o gráfico, inserir uma interpretação técnica integrada do WISC-IV.

## Estrutura da interpretação
A interpretação deve:
1. Introduzir o WISC-IV como instrumento de avaliação intelectual global.
2. Descrever separadamente:
   - ICV
   - IOP
   - IMO
   - IVP
   - QIT
   - GAI
   - CPI
3. Encerrar com uma síntese integrada do funcionamento cognitivo.

## Regras para a interpretação
- A redação deve ser técnica e fluida.
- Cada índice deve ser interpretado conforme:
  - valor
  - classificação
  - impacto funcional
- O texto deve ser coerente com o perfil obtido.
- Quando os índices estiverem muito rebaixados, a síntese deve mencionar impacto em aprendizagem, autonomia, organização, raciocínio e ritmo cognitivo.
- Quando houver discrepância entre raciocínio e eficiência cognitiva, isso deve ser explicitado na leitura integrada entre GAI e CPI.

---

# 4. Seção 5.2 — Subescalas WISC-IV

## Título fixo
```text
5.2. Subescalas WISC-IV
```

Abaixo deste título, devem ser criadas quatro subseções.

---

# 5.2.1. Função executiva

## Título fixo
```text
5.2.1. Função executiva
```

## Tabela
A tabela deve seguir o modelo da imagem, com as colunas:

- Testes Utilizados
- Escore Máximo
- Escore Médio
- Escore Mínimo
- Escore Obtido
- Classificação

## Subtestes usados nesta seção
- Semelhanças
- Conceitos Figurativos
- Compreensão
- Raciocínio Matricial

## Legenda da tabela
```text
Tabela 1 Resultado da Função executiva
```

**Fonte da legenda: tamanho 9.**

## Modelo de interpretação
```text
Interpretação: A avaliação das funções executivas de {PACIENTE} foi realizada por meio dos subtestes Semelhanças, Conceitos Figurativos, Compreensão e Raciocínio Matricial da Escala Wechsler de Inteligência para Crianças – Quarta Edição (WISC-IV). Esses subtestes permitem examinar habilidades de raciocínio abstrato, categorização conceitual, julgamento social e raciocínio lógico-visual, domínios diretamente relacionados ao funcionamento do córtex pré-frontal dorsolateral, orbitofrontal e regiões associadas à resolução de problemas, controle inibitório e flexibilidade cognitiva.

O desempenho em Semelhanças deve ser interpretado conforme a classificação obtida, analisando a capacidade de abstração verbal, formação de conceitos e identificação de relações semânticas entre estímulos. Em Compreensão, a interpretação deve contemplar julgamento prático, entendimento de normas sociais e resolução de situações do cotidiano.

No subteste Conceitos Figurativos, a análise deve descrever a eficiência na formação de categorias não verbais, análise de atributos visuais e organização conceitual figurativa. Em Raciocínio Matricial, a interpretação deve examinar o raciocínio lógico-abstrato não verbal, identificação de padrões, relações visoespaciais e inferência visual.

Em análise clínica, a síntese deve integrar os achados, descrevendo se o perfil executivo sugere funcionamento preservado, limitação leve, moderada ou importante em abstração, planejamento, flexibilidade cognitiva e resolução de problemas.
```

---

# 5.2.2. Linguagem

## Título fixo
```text
5.2.2. Linguagem
```

## Tabela
Colunas:
- Testes Utilizados
- Escore Máximo
- Escore Médio
- Escore Mínimo
- Escore Obtido
- Classificação

## Subtestes usados
- Semelhanças
- Vocabulário
- Compreensão
- Fala Espontânea

## Legenda da tabela
```text
Tabela 2 Resultados da Linguagem
```

**Fonte da legenda: tamanho 9.**

## Modelo de interpretação
Usar este padrão:

```text
Interpretação e Observações Clínicas: A avaliação da linguagem de {PACIENTE} foi realizada por meio dos subtestes Semelhanças, Vocabulário e Compreensão da Escala Wechsler de Inteligência para Crianças – Quarta Edição (WISC-IV), complementada pela análise clínica da fala espontânea. Esses instrumentos permitem examinar habilidades de conceituação verbal, conhecimento lexical, formulação linguística, julgamento social e compreensão de normas, funções amplamente associadas ao córtex temporal, áreas perisilvianas e regiões pré-frontais envolvidas na expressão e organização da linguagem.

No subteste Semelhanças, a interpretação deve descrever o desempenho em abstração verbal, formação de conceitos e estabelecimento de relações semânticas. Em Compreensão, a análise deve abordar entendimento de regras sociais, julgamento prático e resolução de situações do cotidiano.

No subteste Vocabulário, a interpretação deve considerar repertório lexical expressivo, precisão conceitual, definição verbal de palavras e uso espontâneo de termos mais elaborados.

A fala espontânea deve ser descrita de forma clínica e objetiva, considerando fluência, articulação, ritmo, inteligibilidade, prosódia e funcionalidade comunicativa.

Em análise clínica, a síntese deve integrar os achados formais e observacionais, explicitando se há linguagem preservada, empobrecimento lexical, lentificação, alterações articulatórias ou prejuízos funcionais na comunicação.
```

---

# 5.2.3. Gnosias e Praxias

## Título fixo
```text
5.2.3. Gnosias e Praxias
```

## Tabela
Colunas:
- Testes Utilizados
- Escore Máximo
- Escore Médio
- Escore Mínimo
- Escore Obtido
- Classificação

## Subtestes usados
- Raciocínio Matricial
- Cubos

## Legenda da tabela
```text
Tabela 3 Resultados da Gnosias e praxias
```

**Fonte da legenda: tamanho 9.**

## Modelo de interpretação
```text
Interpretação: A avaliação das habilidades visuoperceptivas e construtivas de {PACIENTE} foi realizada por meio dos subtestes Raciocínio Matricial e Cubos da Escala Wechsler de Inteligência para Crianças – Quarta Edição (WISC-IV). Esses subtestes investigam processos de percepção visual, integração visomotora, análise de padrões e organização espacial.

Em Raciocínio Matricial, a interpretação deve examinar a identificação de padrões visuais, o estabelecimento de relações abstratas e a inferência lógica a partir de estímulos não verbais. No subteste Cubos, a análise deve descrever o desempenho em praxias construtivas, organização visomotora, planejamento da ação, coordenação motora fina e integração espacial.

Em análise clínica, a síntese deve indicar se há preservação ou comprometimento das habilidades visuoconstrutivas e perceptivas, bem como o possível impacto em tarefas de cópia, construção, organização espacial e manipulação de estímulos visuais.
```

---

# 5.2.4. Memória e Aprendizagem

## Título fixo
```text
5.2.4. Memória e Aprendizagem
```

## Tabela
Colunas:
- Testes Utilizados
- Escore Máximo
- Escore Médio
- Escore Mínimo
- Escore Obtido
- Classificação

## Subtestes usados
- Seq. Núm. e Letras
- Dígitos

## Legenda da tabela
```text
Tabela 4 Resultados da Memória e aprendizagem
```

**Fonte da legenda: tamanho 9.**

## Modelo de interpretação
```text
Interpretação: A avaliação da memória e aprendizagem de {PACIENTE} foi realizada por meio dos subtestes Sequência de Números e Letras e Dígitos da Escala Wechsler de Inteligência para Crianças – Quarta Edição (WISC-IV). Esses instrumentos examinam processos de memória operacional auditiva, atenção sustentada, manipulação de informações e capacidade de atualização cognitiva.

No subteste Sequência de Números e Letras, a interpretação deve descrever a capacidade de reter, reorganizar e manipular informações auditivas em curto prazo. No subteste Dígitos, a análise deve contemplar atenção auditiva imediata, manutenção sequencial de informações verbais e sustentação atencional.

Em análise clínica, a síntese deve integrar os achados, explicitando se há prejuízo ou preservação da memória operacional, com impacto sobre aprendizagem, seguimento de instruções, organização mental e processamento sequencial.
```

---

# 5. Formato das tabelas
As tabelas devem seguir o padrão visual do modelo enviado, com:

- cabeçalho destacado
- organização horizontal
- legenda abaixo da tabela
- legenda em tamanho 9
- terminologia idêntica ao modelo
- classificação em texto explícito

## Estrutura esperada
```json
{
  "titulo_secao": "5.2.1. Função executiva",
  "tabela": {
    "colunas": [
      "Testes Utilizados",
      "Escore Máximo",
      "Escore Médio",
      "Escore Mínimo",
      "Escore Obtido",
      "Classificação"
    ],
    "linhas": []
  },
  "legenda": "Tabela 1 Resultado da Função executiva",
  "fonte_legenda": 9,
  "interpretacao": "texto gerado"
}
```

---

# 6. Regras de consistência clínica
A IA deve validar antes de gerar o texto:

1. Se o valor do índice corresponde à classificação informada.
2. Se a interpretação textual está coerente com a classificação.
3. Se o conteúdo das tabelas está coerente com a seção correspondente.
4. Se não há troca de nome do paciente.
5. Se não há troca de sexo gramatical.
6. Se não há repetição indevida de outro domínio clínico.
7. Se as legendas estão corretas e na ordem:
   - Gráfico 1
   - Tabela 1
   - Tabela 2
   - Tabela 3
   - Tabela 4

---

# 7. Classificação dos índices compostos do WISC-IV
Usar esta regra:

- ≤ 69 → Extremamente Baixo
- 70–79 → Limítrofe
- 80–89 → Média Inferior
- 90–109 → Média
- 110–119 → Média Superior
- 120–129 → Superior
- ≥ 130 → Muito Superior

---

# 8. Prompt interno recomendado para geração
```text
Gerar o capítulo 5 do laudo neuropsicológico com base exclusivamente nos dados do WISC-IV fornecidos. Manter a estrutura fixa da seção 5, da subseção 5.1 e das subseções 5.2.1 a 5.2.4. Não alterar os textos padronizados, exceto para substituir valores, classificações, nome do paciente e conteúdo variável das interpretações clínicas. As legendas do gráfico e das tabelas devem permanecer fixas. As legendas devem estar em fonte tamanho 9. O texto deve manter linguagem técnica, formal e coerência clínica integral com os resultados apresentados.
```

---

# 9. Resultado final esperado
A IA deve ser capaz de gerar automaticamente, a partir dos dados do WISC-IV:

- texto fixo da análise qualitativa
- gráfico dos índices compostos
- legenda fixa do gráfico
- quatro tabelas padronizadas
- quatro interpretações clínicas por domínio
- coerência clínica total com os resultados
