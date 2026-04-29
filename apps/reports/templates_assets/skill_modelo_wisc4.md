# Skill: Correção, Interpretação e Elaboração do Resultado do WISC-IV

## 1. Objetivo da Skill

Esta skill orienta a IA e o sistema a realizar, de forma padronizada, auditável e clinicamente consistente, a correção, organização, classificação, interpretação e redação dos resultados da Escala Wechsler de Inteligência para Crianças – Quarta Edição (WISC-IV), para uso em laudos neuropsicológicos.

A skill deve ser utilizada para:

- converter escores brutos dos subtestes em escores ponderados, conforme idade cronológica da criança ou adolescente;
- calcular os índices fatoriais do WISC-IV;
- calcular o QI Total, quando aplicável;
- calcular índices complementares, quando disponíveis, como GAI e CPI;
- classificar os resultados segundo faixas psicométricas padronizadas;
- gerar interpretação clínica por índice e por domínio cognitivo;
- elaborar a seção do WISC-IV no laudo neuropsicológico em padrão técnico, objetivo e compatível com auditoria clínica.

Esta skill não substitui o manual técnico do instrumento. O sistema deve utilizar apenas tabelas normativas previamente cadastradas e validadas, respeitando os direitos autorais e a padronização do teste.

## 2. Instrumento

Nome completo: Escala Wechsler de Inteligência para Crianças – Quarta Edição

Sigla: WISC-IV

População-alvo: crianças e adolescentes, conforme faixa etária prevista no manual técnico do instrumento.

Finalidade: avaliar o funcionamento intelectual global e os principais domínios cognitivos, por meio dos índices de Compreensão Verbal, Organização Perceptual, Memória Operacional, Velocidade de Processamento e QI Total.

## 3. Estrutura Recomendada no Sistema

```text
apps/tests/
  wisc4/
    __init__.py
    config.py
    schemas.py
    validators.py
    loaders.py
    norm_utils.py
    calculators.py
    classifiers.py
    interpreters.py
    constants.py

  norms/
    wisc4/
      raw_to_scaled/
        idade_6_0_a_6_3.csv
        idade_6_4_a_6_7.csv
        idade_6_8_a_6_11.csv
        ...
      scaled_sum_to_composite/
        icv.csv
        iop.csv
        imo.csv
        ivp.csv
        qit.csv
        gai.csv
        cpi.csv
```

## 4. Arquivos do Módulo

### 4.1. `schemas.py`

Define o formato esperado dos dados de entrada.

Campos mínimos recomendados:

```python
{
    "patient_name": "string",
    "birth_date": "YYYY-MM-DD",
    "test_date": "YYYY-MM-DD",
    "chronological_age": {
        "years": int,
        "months": int
    },
    "raw_scores": {
        "cubos": int,
        "semelhancas": int,
        "digitos": int,
        "conceitos_figurativos": int,
        "codigos": int,
        "vocabulario": int,
        "sequencia_numeros_letras": int,
        "raciocinio_matricial": int,
        "compreensao": int,
        "procurar_simbolos": int,
        "completar_figuras": int,
        "cancelamento": int,
        "informacao": int,
        "aritmetica": int,
        "raciocinio_palavras": int
    }
}
```

Nem todos os subtestes suplementares precisam estar preenchidos. O sistema deve validar quais são obrigatórios para cada índice e quais podem ser utilizados como substituição, conforme regras do manual.

### 4.2. `validators.py`

Deve validar:

- idade cronológica dentro da faixa permitida pelo WISC-IV;
- data de nascimento anterior à data da avaliação;
- presença dos subtestes necessários;
- valores brutos numéricos e dentro dos limites possíveis;
- ausência de substituições inválidas;
- impossibilidade de calcular índice quando houver subteste obrigatório ausente e sem substituição permitida.

### 4.3. `loaders.py`

Responsável por carregar as tabelas normativas em CSV.

Funções recomendadas:

```python
load_raw_to_scaled_table(age_band: str) -> DataFrame
load_composite_table(index_name: str) -> DataFrame
```

### 4.4. `norm_utils.py`

Funções auxiliares:

```python
get_age_band(years: int, months: int) -> str
lookup_scaled_score(subtest: str, raw_score: int, age_band: str) -> int
lookup_composite_score(index_name: str, scaled_sum: int) -> dict
classify_composite_score(score: int) -> str
classify_scaled_score(scaled_score: int) -> str
```

### 4.5. `calculators.py`

Executa o fluxo psicométrico:

1. identificar faixa etária normativa;
2. converter escores brutos em escores ponderados;
3. somar os escores ponderados por índice;
4. converter somas em pontos compostos;
5. calcular percentis e intervalos de confiança, quando cadastrados;
6. devolver payload estruturado.

### 4.6. `classifiers.py`

Classifica os pontos compostos e os escores ponderados.

### 4.7. `interpreters.py`

Gera o texto interpretativo do WISC-IV com base nos resultados corrigidos.

Deve produzir:

- interpretação do QI Total;
- interpretação do ICV;
- interpretação do IOP;
- interpretação do IMO;
- interpretação do IVP;
- análise do GAI e CPI, quando disponíveis;
- análise de discrepâncias clinicamente relevantes;
- interpretação dos subtestes por domínio;
- síntese clínica final do WISC-IV.

### 4.8. `config.py`

Classe principal do módulo:

```python
class WISC4Module:
    instrument_key = "WISC4"
    instrument_name = "Escala Wechsler de Inteligência para Crianças – Quarta Edição"

    def validate(self, raw_payload):
        ...

    def score(self, raw_payload):
        ...

    def interpret(self, computed_payload):
        ...
```

## 5. Fluxo Geral de Correção

### Etapa 1: calcular idade cronológica

A idade cronológica deve ser calculada a partir da data de nascimento e da data da avaliação.

Exemplo:

```python
idade = data_avaliacao - data_nascimento
```

O resultado deve ser convertido em anos e meses completos.

### Etapa 2: localizar a tabela normativa correta

Após calcular a idade, o sistema deve selecionar a tabela normativa correspondente à faixa etária do paciente.

Exemplo:

```text
Paciente: 10 anos e 4 meses
Tabela normativa: idade_10_4_a_10_7.csv
```

### Etapa 3: converter escore bruto em escore ponderado

Para cada subteste aplicado, o sistema deve consultar a tabela da faixa etária e converter o escore bruto em escore ponderado.

Exemplo conceitual:

```text
Subteste: Semelhanças
Escore bruto: 23
Faixa etária: 10 anos e 4 meses a 10 anos e 7 meses
Escore ponderado: valor obtido na tabela normativa validada
```

Nunca estimar escore ponderado. Se a tabela normativa não estiver cadastrada, o sistema deve interromper a correção e retornar erro.

## 6. Subtestes do WISC-IV

### 6.1. Subtestes principais

- Cubos
- Semelhanças
- Dígitos
- Conceitos Figurativos
- Códigos
- Vocabulário
- Sequência de Números e Letras
- Raciocínio Matricial
- Compreensão
- Procurar Símbolos

### 6.2. Subtestes suplementares

- Completar Figuras
- Cancelamento
- Informação
- Aritmética
- Raciocínio com Palavras

Os subtestes suplementares devem ser utilizados apenas quando houver regra técnica válida para substituição, conforme manual do instrumento.

## 7. Cálculo dos Índices Fatoriais

### 7.1. Índice de Compreensão Verbal, ICV

Subtestes principais:

```text
ICV = Semelhanças + Vocabulário + Compreensão
```

Subtestes suplementares possíveis:

```text
Informação
Raciocínio com Palavras
```

O ICV avalia conhecimento verbal adquirido, raciocínio verbal, formação de conceitos, compreensão verbal e expressão de respostas mediadas pela linguagem.

### 7.2. Índice de Organização Perceptual, IOP

Subtestes principais:

```text
IOP = Cubos + Conceitos Figurativos + Raciocínio Matricial
```

Subteste suplementar possível:

```text
Completar Figuras
```

O IOP avalia raciocínio não verbal, organização perceptual, análise visuoespacial, integração visomotora e resolução de problemas com estímulos visuais.

### 7.3. Índice de Memória Operacional, IMO

Subtestes principais:

```text
IMO = Dígitos + Sequência de Números e Letras
```

Subteste suplementar possível:

```text
Aritmética
```

O IMO avalia atenção auditiva, memória de trabalho, manipulação mental de informações, concentração e controle mental ativo.

### 7.4. Índice de Velocidade de Processamento, IVP

Subtestes principais:

```text
IVP = Códigos + Procurar Símbolos
```

Subteste suplementar possível:

```text
Cancelamento
```

O IVP avalia rapidez perceptual, discriminação visual, coordenação visuomotora, precisão sob limite de tempo e eficiência em tarefas visuais simples.

### 7.5. QI Total, QIT

O QIT deve ser calculado a partir da soma dos escores ponderados dos subtestes principais que compõem os índices fatoriais.

Estrutura conceitual:

```text
QIT = soma dos escores ponderados dos subtestes principais do WISC-IV
```

O sistema deve utilizar a tabela normativa específica de conversão da soma dos escores ponderados para o QI Total.

Nunca calcular QIT por média aritmética dos índices. O QIT deve vir exclusivamente da tabela normativa.

## 8. Índices Complementares

### 8.1. GAI, Índice de Aptidão Geral

O GAI representa uma estimativa do raciocínio geral com menor influência de memória operacional e velocidade de processamento.

Estrutura conceitual:

```text
GAI = soma dos subtestes que compõem ICV + IOP
```

O sistema deve converter a soma em ponto composto usando tabela própria do GAI.

O GAI deve ser interpretado quando:

- houver discrepância relevante entre habilidades de raciocínio e eficiência cognitiva;
- memória operacional ou velocidade de processamento estiverem muito rebaixadas;
- for clinicamente útil diferenciar raciocínio geral de eficiência cognitiva.

### 8.2. CPI, Índice de Competência Cognitiva

O CPI representa a eficiência cognitiva relacionada à memória operacional e velocidade de processamento.

Estrutura conceitual:

```text
CPI = soma dos subtestes que compõem IMO + IVP
```

O sistema deve converter a soma em ponto composto usando tabela própria do CPI.

O CPI deve ser interpretado como indicador de eficiência mental, ritmo de trabalho, sustentação atencional e capacidade de operar cognitivamente sob demanda de tempo e manipulação de informação.

## 9. Classificação dos Pontos Compostos

Utilizar a seguinte classificação:

```text
≤ 69     = Extremamente Baixo
70–79    = Limítrofe
80–89    = Média Inferior
90–109   = Média
110–119  = Média Superior
120–129  = Superior
≥ 130    = Muito Superior
```

Essa classificação deve ser aplicada a:

- ICV;
- IOP;
- IMO;
- IVP;
- QIT;
- GAI;
- CPI.

## 10. Classificação dos Escores Ponderados dos Subtestes

Recomendação operacional:

```text
1–3      = Extremamente Baixo
4–5      = Limítrofe
6–7      = Média Inferior
8–12     = Média
13–14    = Média Superior
15–16    = Superior
17–19    = Muito Superior
```

Essa classificação deve ser usada para interpretação dos subtestes, quando o sistema estiver analisando desempenho específico por domínio.

## 11. Payload Computado Recomendado

```python
{
    "instrument": "WISC4",
    "age_band": "10_4_a_10_7",
    "scaled_scores": {
        "semelhancas": 10,
        "vocabulario": 8,
        "compreensao": 9,
        "cubos": 7,
        "conceitos_figurativos": 8,
        "raciocinio_matricial": 6,
        "digitos": 7,
        "sequencia_numeros_letras": 6,
        "codigos": 8,
        "procurar_simbolos": 7
    },
    "index_sums": {
        "ICV": 27,
        "IOP": 21,
        "IMO": 13,
        "IVP": 15,
        "QIT": 76,
        "GAI": 48,
        "CPI": 28
    },
    "composite_scores": {
        "ICV": {
            "score": 95,
            "percentile": 37,
            "classification": "Média"
        },
        "IOP": {
            "score": 82,
            "percentile": 12,
            "classification": "Média Inferior"
        },
        "IMO": {
            "score": 78,
            "percentile": 7,
            "classification": "Limítrofe"
        },
        "IVP": {
            "score": 85,
            "percentile": 16,
            "classification": "Média Inferior"
        },
        "QIT": {
            "score": 82,
            "percentile": 12,
            "classification": "Média Inferior"
        },
        "GAI": {
            "score": 88,
            "percentile": 21,
            "classification": "Média Inferior"
        },
        "CPI": {
            "score": 76,
            "percentile": 5,
            "classification": "Limítrofe"
        }
    }
}
```

Os valores acima são apenas exemplos estruturais. O sistema deve preencher os resultados reais a partir das tabelas normativas cadastradas.

## 12. Regras de Segurança Psicométrica

A IA nunca deve:

- inventar escores ponderados;
- estimar pontos compostos sem tabela normativa;
- calcular QIT por média dos índices;
- usar tabela de idade diferente da idade cronológica;
- aplicar substituição de subteste sem regra válida;
- misturar dados de outro paciente;
- manter nome de paciente de modelo anterior;
- gerar hipótese diagnóstica apenas pelo WISC-IV;
- concluir deficiência intelectual apenas pelo QIT, sem considerar funcionamento adaptativo e dados clínicos.

O sistema deve bloquear a geração quando:

- houver subteste obrigatório ausente;
- houver tabela normativa não cadastrada;
- houver idade fora da faixa permitida;
- houver inconsistência entre data de nascimento e idade informada;
- houver soma incompatível com os subtestes fornecidos.

## 13. Estrutura da Seção no Laudo

A seção do WISC-IV deve seguir esta estrutura:

```text
5. ANÁLISE QUALITATIVA

5.1. Capacidade Cognitiva Global

5.2. Desempenho no WISC-IV

5.3. Índices Fatoriais do WISC-IV

5.3.1. Compreensão Verbal
5.3.2. Organização Perceptual
5.3.3. Memória Operacional
5.3.4. Velocidade de Processamento
5.3.5. QI Total
5.3.6. GAI e CPI, quando disponíveis

5.4. Subescalas WISC-IV

5.4.1. Funções Executivas
5.4.2. Linguagem
5.4.3. Gnosias e Praxias
5.4.4. Memória e Aprendizagem
```

## 14. Modelo de Texto: Capacidade Cognitiva Global

```text
A avaliação neuropsicológica de {NOME}, por meio da Escala Wechsler de Inteligência para Crianças – Quarta Edição (WISC-IV), possibilitou a análise do funcionamento intelectual global e dos principais domínios cognitivos. {NOME} apresentou Quociente de Inteligência Total (QIT = {QIT}), classificado como {CLASSIFICACAO_QIT}, indicando {INTERPRETACAO_GLOBAL}.

Em relação aos índices fatoriais, observou-se Compreensão Verbal (ICV = {ICV}), classificada como {CLASSIFICACAO_ICV}; Organização Perceptual (IOP = {IOP}), classificada como {CLASSIFICACAO_IOP}; Memória Operacional (IMO = {IMO}), classificada como {CLASSIFICACAO_IMO}; e Velocidade de Processamento (IVP = {IVP}), classificada como {CLASSIFICACAO_IVP}. Esse conjunto de resultados evidencia {SINTESE_PERFIL}, devendo ser interpretado em integração com os achados clínicos, comportamentais, escolares e adaptativos.
```

## 15. Modelo de Texto: Interpretação dos Índices

### 15.1. ICV

```text
O Índice de Compreensão Verbal (ICV = {ICV}), classificado como {CLASSIFICACAO_ICV}, avalia conhecimento verbal adquirido, formação de conceitos, raciocínio verbal, compreensão de informações mediadas pela linguagem e capacidade de expressar respostas verbais organizadas. O desempenho de {NOME} nesse índice sugere {INTERPRETACAO_ICV}, com possíveis repercussões em tarefas que exigem compreensão de enunciados, elaboração verbal, abstração conceitual e aprendizagem mediada pela linguagem.
```

### 15.2. IOP

```text
O Índice de Organização Perceptual (IOP = {IOP}), classificado como {CLASSIFICACAO_IOP}, investiga raciocínio não verbal, análise visuoespacial, organização perceptiva, integração visomotora e resolução de problemas com estímulos visuais. O resultado indica {INTERPRETACAO_IOP}, podendo impactar atividades que exigem percepção de relações espaciais, construção visual, raciocínio lógico não verbal e planejamento visuomotor.
```

### 15.3. IMO

```text
O Índice de Memória Operacional (IMO = {IMO}), classificado como {CLASSIFICACAO_IMO}, avalia atenção auditiva, retenção temporária, manipulação mental de informações, concentração e controle mental ativo. O desempenho de {NOME} sugere {INTERPRETACAO_IMO}, com impacto potencial no acompanhamento de instruções, resolução de problemas em etapas, cálculo mental, organização sequencial e aprendizagem escolar.
```

### 15.4. IVP

```text
O Índice de Velocidade de Processamento (IVP = {IVP}), classificado como {CLASSIFICACAO_IVP}, avalia rapidez perceptual, discriminação visual, coordenação visuomotora e eficiência em tarefas simples realizadas sob limite de tempo. O resultado indica {INTERPRETACAO_IVP}, podendo repercutir no ritmo de execução de atividades escolares, cópia, leitura visual rápida, conclusão de tarefas e desempenho sob pressão temporal.
```

### 15.5. QIT

```text
O Quociente de Inteligência Total (QIT = {QIT}), classificado como {CLASSIFICACAO_QIT}, representa uma estimativa global do funcionamento intelectual. O resultado deve ser interpretado considerando a homogeneidade ou heterogeneidade entre os índices fatoriais. Quando houver discrepâncias importantes entre os domínios, o QIT pode não representar adequadamente todas as habilidades cognitivas de {NOME}, sendo necessário analisar os índices fatoriais de forma individualizada.
```

### 15.6. GAI e CPI

```text
O Índice de Aptidão Geral (GAI = {GAI}), classificado como {CLASSIFICACAO_GAI}, fornece uma estimativa das habilidades de raciocínio verbal e perceptual, com menor influência da memória operacional e da velocidade de processamento. O Índice de Competência Cognitiva (CPI = {CPI}), classificado como {CLASSIFICACAO_CPI}, reflete a eficiência cognitiva associada à memória operacional e à velocidade de processamento. A comparação entre GAI e CPI permite compreender se o desempenho global é mais influenciado por habilidades de raciocínio ou por processos de eficiência cognitiva.
```

## 16. Interpretação por Domínios Cognitivos

### 16.1. Funções Executivas

Subtestes recomendados:

- Semelhanças
- Conceitos Figurativos
- Compreensão
- Raciocínio Matricial

Modelo:

```text
A avaliação das funções executivas de {NOME} foi realizada por meio dos subtestes Semelhanças, Conceitos Figurativos, Compreensão e Raciocínio Matricial do WISC-IV. Esses subtestes permitem examinar raciocínio abstrato, categorização conceitual, julgamento social, formação de estratégias e raciocínio lógico-visual.

{ANALISE_SUBTESTES_FUNCOES_EXECUTIVAS}

Em análise clínica, o desempenho de {NOME} nesse domínio sugere {SINTESE_FUNCOES_EXECUTIVAS}, com possíveis repercussões na organização da resposta, resolução de problemas, flexibilidade cognitiva e adaptação a demandas novas.
```

### 16.2. Linguagem

Subtestes recomendados:

- Semelhanças
- Vocabulário
- Compreensão
- Fala espontânea, quando descrita clinicamente

Modelo:

```text
A avaliação da linguagem de {NOME} foi realizada por meio dos subtestes Semelhanças, Vocabulário e Compreensão do WISC-IV, complementada pela observação clínica da fala espontânea. Esses indicadores permitem examinar repertório lexical, conceituação verbal, compreensão de normas sociais, expressão verbal e organização do pensamento mediado pela linguagem.

{ANALISE_SUBTESTES_LINGUAGEM}

Em análise clínica, o perfil linguístico de {NOME} indica {SINTESE_LINGUAGEM}, devendo ser interpretado em conjunto com os dados escolares, observacionais e comportamentais.
```

### 16.3. Gnosias e Praxias

Subtestes recomendados:

- Cubos
- Raciocínio Matricial
- Completar Figuras, quando aplicado

Modelo:

```text
A avaliação das habilidades visuoperceptivas e construtivas de {NOME} foi realizada por meio dos subtestes Cubos e Raciocínio Matricial do WISC-IV. Esses subtestes investigam percepção visual, análise de padrões, organização espacial, integração visomotora e praxias construtivas.

{ANALISE_SUBTESTES_GNOSIAS_PRAXIAS}

Em análise clínica, os resultados sugerem {SINTESE_GNOSIAS_PRAXIAS}, com possível impacto em tarefas que exigem construção visual, cópia, organização espacial, planejamento visuomotor e raciocínio não verbal.
```

### 16.4. Memória e Aprendizagem

Subtestes recomendados:

- Dígitos
- Sequência de Números e Letras
- Aritmética, quando aplicada

Modelo:

```text
A avaliação da memória operacional e dos processos de aprendizagem de {NOME} foi realizada por meio dos subtestes Dígitos e Sequência de Números e Letras do WISC-IV. Esses subtestes examinam atenção auditiva, retenção imediata, manipulação de informações, organização sequencial e controle mental ativo.

{ANALISE_SUBTESTES_MEMORIA}

Em análise clínica, o desempenho indica {SINTESE_MEMORIA}, podendo repercutir no acompanhamento de instruções, aprendizagem verbal, cálculo mental, memorização sequencial e execução de tarefas com múltiplas etapas.
```

## 17. Regras para Análise de Discrepância

O sistema deve verificar discrepâncias entre os índices fatoriais.

Comparações prioritárias:

- ICV versus IOP;
- ICV versus IMO;
- ICV versus IVP;
- IOP versus IMO;
- IOP versus IVP;
- IMO versus IVP;
- GAI versus CPI.

Quando houver diferença clinicamente relevante, a interpretação deve indicar perfil heterogêneo.

Modelo:

```text
Observa-se perfil cognitivo heterogêneo, com discrepância entre {INDICE_MAIS_ALTO} e {INDICE_MAIS_BAIXO}. Esse padrão indica que o QIT deve ser interpretado com cautela, pois pode não representar de forma uniforme o funcionamento cognitivo de {NOME}. A análise dos índices fatoriais mostra-se clinicamente mais informativa para compreender suas potencialidades e vulnerabilidades.
```

Quando não houver discrepância relevante:

```text
Os índices fatoriais apresentaram distribuição relativamente homogênea, indicando que o QIT constitui uma estimativa representativa do funcionamento intelectual global de {NOME} no momento da avaliação.
```

## 18. Regras para Hipótese Diagnóstica

O WISC-IV pode contribuir para hipóteses diagnósticas, mas não deve ser usado isoladamente para fechar diagnóstico.

### 18.1. Deficiência Intelectual

Somente considerar hipótese diagnóstica de Deficiência Intelectual quando houver:

- QIT ou índices globais significativamente rebaixados;
- prejuízo em funcionamento adaptativo;
- início no período do desenvolvimento;
- integração com anamnese, observação clínica, dados escolares e instrumentos adaptativos.

Modelo:

```text
Os resultados do WISC-IV indicam funcionamento intelectual global significativamente rebaixado. Contudo, a hipótese diagnóstica de Deficiência Intelectual deve ser estabelecida apenas mediante integração com dados de funcionamento adaptativo, história do desenvolvimento, desempenho acadêmico, observações clínicas e demais instrumentos aplicados.
```

### 18.2. TDAH

O WISC-IV não diagnostica TDAH isoladamente. Pode indicar vulnerabilidades compatíveis quando há rebaixamento em memória operacional e velocidade de processamento.

Modelo:

```text
O perfil observado, especialmente quando há fragilidades em Memória Operacional e Velocidade de Processamento, pode ser compatível com dificuldades atencionais e executivas. Entretanto, a hipótese diagnóstica de TDAH deve ser sustentada apenas pela integração entre testagens atencionais específicas, escalas comportamentais, observações clínicas e dados funcionais.
```

### 18.3. Transtornos de Aprendizagem

O WISC-IV pode indicar fatores cognitivos associados a dificuldades escolares, mas não fecha diagnóstico de transtorno específico de aprendizagem isoladamente.

Modelo:

```text
As fragilidades observadas em memória operacional, velocidade de processamento, linguagem ou raciocínio visuoespacial podem contribuir para dificuldades acadêmicas. A hipótese diagnóstica de transtorno específico de aprendizagem deve ser analisada em conjunto com instrumentos pedagógicos, histórico escolar e avaliação do desempenho acadêmico formal.
```

## 19. Geração de Gráficos

O sistema deve gerar gráfico dos índices compostos do WISC-IV contendo:

- ICV;
- IOP;
- IMO;
- IVP;
- QIT;
- GAI, quando disponível;
- CPI, quando disponível.

Título recomendado:

```text
WISC-IV – Índices de QI
```

Legenda abaixo do gráfico:

```text
Gráfico {N}. WISC-IV – Índices de QI.
```

Regras de formatação:

- fonte principal: Times New Roman;
- legenda: Times New Roman, tamanho 8, itálico;
- legenda sempre abaixo do gráfico;
- largura recomendada para Word: 14 cm;
- altura recomendada para Word: 10 cm;
- evitar elementos visuais excessivos;
- preservar nitidez em exportação para DOCX e PDF.

## 20. Formatação no Laudo

Padrão recomendado:

- Fonte: Times New Roman;
- Tamanho do corpo: 12;
- Alinhamento: justificado;
- Espaçamento entre linhas: 1,5;
- Margem superior: 3 cm;
- Margem esquerda: 2 cm;
- Margem inferior: 2 cm;
- Margem direita: 2 cm;
- Tabelas centralizadas;
- Legendas abaixo de tabelas e gráficos;
- Legendas em Times New Roman, tamanho 8, itálico;
- Não utilizar linhas divisórias longas;
- Evitar excesso de tabelas quando o usuário solicitar apenas texto interpretativo.

## 21. Modelo Final de Interpretação Integrada do WISC-IV

```text
Em análise clínica, os resultados do WISC-IV indicam que {NOME} apresenta funcionamento intelectual global {DESCRICAO_GLOBAL}, com {PADRAO_HOMOGENEO_OU_HETEROGENEO}. Observa-se desempenho {DESCRICAO_ICV} em Compreensão Verbal, {DESCRICAO_IOP} em Organização Perceptual, {DESCRICAO_IMO} em Memória Operacional e {DESCRICAO_IVP} em Velocidade de Processamento.

Esse perfil sugere {SINTESE_COGNITIVA}, com repercussões potenciais em {IMPACTOS_FUNCIONAIS}. Quando comparado aos dados clínicos, escolares e comportamentais, o desempenho no WISC-IV contribui para a compreensão das potencialidades e vulnerabilidades cognitivas de {NOME}, devendo ser interpretado de forma integrada aos demais instrumentos aplicados na avaliação neuropsicológica.
```

## 22. Checklist de Auditoria Antes de Gerar o Laudo

Antes de finalizar a seção WISC-IV, verificar:

- o nome do paciente está correto;
- não há nome de outro paciente no texto;
- idade cronológica está correta;
- tabela normativa corresponde à idade;
- todos os escores brutos foram convertidos corretamente;
- somas dos escores ponderados estão corretas;
- índices compostos vieram de tabela normativa;
- classificações estão corretas;
- QIT não foi calculado por média;
- GAI e CPI só aparecem quando calculados corretamente;
- não há hipótese diagnóstica fechada apenas com base no WISC-IV;
- linguagem está técnica, clara e sem redundância;
- o texto utiliza “Em análise clínica” nos fechamentos interpretativos;
- não há resíduos de tabelas brutas após as referências bibliográficas;
- a legenda do gráfico está abaixo do gráfico;
- a seção está compatível com o restante do laudo.

## 23. Saída Final Esperada

A skill deve retornar um objeto estruturado com:

```python
{
    "computed_payload": {...},
    "tables": [...],
    "charts": [...],
    "interpretation_text": "...",
    "clinical_summary": "...",
    "audit_warnings": []
}
```

Se houver erro:

```python
{
    "status": "error",
    "message": "Não foi possível calcular o WISC-IV porque a tabela normativa da faixa etária informada não está cadastrada.",
    "missing_requirements": ["idade_10_4_a_10_7.csv"]
}
```

## 24. Referência Bibliográfica Recomendada

WECHSLER, D. Escala de Inteligência Wechsler para Crianças – Quarta Edição: WISC-IV. São Paulo: Pearson, 2013.

## 25. Observação Final

Esta skill deve ser tratada como módulo técnico de apoio à correção e interpretação. A decisão clínica final deve ser realizada por profissional habilitado, com base na integração entre testagem padronizada, observação clínica, anamnese, contexto escolar, funcionamento adaptativo e demais instrumentos aplicados.
