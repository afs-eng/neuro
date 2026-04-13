# SKILL — Geração de Laudo Neuropsicológico no Sistema

## Objetivo
Implementar no sistema uma skill de geração de laudo neuropsicológico que produza um documento técnico, revisável, padronizado e compatível com o modelo clínico adotado no serviço, tomando como referência estrutural o laudo do paciente Álvaro Barbosa de Araujo e a padronização visual definida para os documentos do sistema.

Esta skill deve permitir que a IA gere o laudo completo a partir dos dados estruturados da avaliação, mantendo consistência clínica, formatação profissional e aderência ao estilo do modelo utilizado.

## Referências-base do modelo
A skill deve se basear em dois pilares:

1. **Modelo de papel timbrado / identidade visual**
   - Fonte principal do documento: **Times New Roman, tamanho 12**.
   - Legendas de tabelas, gráficos e figuras: **Times New Roman, tamanho 8, em itálico, sempre abaixo do elemento correspondente**.
   - Documento em formato **A4**.
   - Uso de cabeçalho institucional e rodapé compatíveis com o padrão visual do serviço.

2. **Modelo de estrutura textual e raciocínio clínico**
   - O laudo de **Álvaro Barbosa de Araujo** deve ser utilizado como referência para:
     - ordem das seções;
     - profundidade técnica das interpretações;
     - integração entre dados quantitativos, observação clínica, anamnese e hipótese diagnóstica;
     - estilo formal, técnico e clínico;
     - seção final de conduta e encaminhamentos.

## Finalidade da skill
A skill deve gerar um **rascunho técnico do laudo** a partir dos dados já lançados no sistema, para posterior revisão do profissional responsável.

Ela não deve inventar resultados, percentis, classificações, hipóteses ou históricos. Toda redação deve derivar dos dados estruturados já registrados no sistema e das observações clínicas disponíveis.

## Posição da skill dentro do fluxo do sistema
A skill será acionada na etapa **Laudo**, depois que:

- o paciente já estiver cadastrado;
- a avaliação já estiver criada;
- os testes já tiverem sido aplicados e corrigidos;
- a anamnese já estiver registrada;
- os resultados estruturados e interpretações-base dos testes já estiverem disponíveis.

## Entrada esperada
A IA deve receber um `contexto_estruturado_do_laudo`, contendo:

```json
{
  "clinica": {
    "nome": "",
    "papel_timbrado": true,
    "cidade": "",
    "uf": ""
  },
  "profissional": {
    "nome": "",
    "crp": "",
    "titulo": ""
  },
  "paciente": {
    "nome_completo": "",
    "nome_referencia": "",
    "sexo": "",
    "data_nascimento": "",
    "idade": "",
    "escolaridade": "",
    "escola": "",
    "filiacao": ""
  },
  "identificacao_laudo": {
    "interessado": "",
    "finalidade": ""
  },
  "demanda": {
    "motivo_encaminhamento": "",
    "objetivo_avaliacao": ""
  },
  "procedimentos": {
    "anamnese_realizada": true,
    "numero_sessoes_testagem": 0,
    "houve_devolutiva": true,
    "testes_realizados": []
  },
  "anamnese": {
    "historia_pessoal": "",
    "historia_pre_natal_perinatal": "",
    "desenvolvimento_neuropsicomotor": "",
    "alimentacao_sono": "",
    "desenvolvimento_comportamental_socioemocional": "",
    "historico_escolar": "",
    "vida_social_interesses": "",
    "antecedentes_familiares": "",
    "sintese_clinica": "",
    "relatorio_escolar": ""
  },
  "observacoes_clinicas": {
    "durante_avaliacao": "",
    "comportamento_observado": "",
    "comunicacao": "",
    "engajamento": ""
  },
  "resultados_testes": {
    "wisc_iv": {},
    "wais_iii": {},
    "wasi": {},
    "bpa_2": {},
    "fdt": {},
    "ravlt": {},
    "srs_2": {},
    "etdah_pais": {},
    "etdah_ad": {},
    "scared": {},
    "bai": {},
    "bfp": {},
    "iphexa": {},
    "outros": []
  },
  "interpretacoes_testes": {
    "eficiencia_intelectual": "",
    "atencao": "",
    "funcoes_executivas": "",
    "linguagem": "",
    "gnosias_praxias": "",
    "memoria_aprendizagem": "",
    "ravlt": "",
    "fdt": "",
    "srs_2": "",
    "etdah_pais": "",
    "etdah_ad": "",
    "scared": "",
    "personalidade": ""
  },
  "graficos": {
    "wisc_iv": [],
    "bpa_2": [],
    "ravlt": [],
    "fdt": [],
    "srs_2": []
  },
  "hipotese_diagnostica": {
    "texto_base": "",
    "cid11": []
  }
}
```

## Saída esperada
A skill deve gerar um documento contendo:

- texto completo do laudo;
- estrutura técnica padronizada;
- títulos de seções;
- textos interpretativos integrados;
- hipótese diagnóstica inserida na conclusão;
- sugestões de conduta;
- fechamento técnico;
- assinatura;
- observações ético-profissionais;
- referências bibliográficas;
- marcação opcional para tabelas e gráficos.

## Estrutura obrigatória do laudo
A IA deve gerar o laudo na seguinte ordem:

1. **LAUDO DE AVALIAÇÃO NEUROPSICOLÓGICA**
2. **Referência normativa**
   - Exemplo: “De acordo com a Resolução de Elaboração de Documentos – CFP 006/2019”.
3. **IDENTIFICAÇÃO**
   - 1.1 Identificação do laudo
   - 1.2 Identificação do paciente
4. **DESCRIÇÃO DA DEMANDA**
   - Motivo do encaminhamento
5. **PROCEDIMENTOS**
   - anamnese
   - número de sessões
   - instrumentos aplicados
6. **ANÁLISE**
   - anamnese e história clínica
7. **ANÁLISE QUALITATIVA / DOMÍNIOS COGNITIVOS E COMPORTAMENTAIS**
   - Capacidade Cognitiva Global / Eficiência Intelectual
   - Funções Executivas
   - Linguagem
   - Gnosias e Praxias
   - Memória e Aprendizagem
   - Atenção
   - RAVLT
   - FDT
   - E-TDAH-PAIS / E-TDAH-AD
   - SCARED / BAI / escalas emocionais
   - Personalidade
   - SRS-2
8. **CONCLUSÃO**
   - síntese integrada
   - hipótese diagnóstica
   - CID-11, quando houver
9. **SUGESTÕES DE CONDUTA (ENCAMINHAMENTOS)**
10. **FECHAMENTO TÉCNICO / EQUIPE MULTIDISCIPLINAR**
11. **LOCAL, DATA E ASSINATURA**
12. **OBSERVAÇÕES ÉTICAS**
13. **REFERÊNCIAS BIBLIOGRÁFICAS**

## Regras de escrita clínica
A skill deve obedecer às seguintes regras:

### 1. Estilo
- Linguagem técnica, formal e clínica.
- Texto coeso, sem tom genérico de IA.
- Evitar frases excessivamente repetitivas.
- Variar a abertura dos parágrafos, evitando repetição excessiva de “No”, “Na” e “De forma geral”.
- Preferir construções clínicas como:
  - “Em análise clínica”
  - “Os achados sugerem”
  - “Observa-se”
  - “Esse padrão indica”
  - “A integração dos resultados evidencia”

### 2. Fidelidade aos dados
- Não criar informações ausentes.
- Não atribuir sintomas não descritos.
- Não afirmar diagnóstico sem sustentação nos dados.
- Quando o instrumento não sustentar sozinho uma hipótese, a IA deve integrar anamnese, observação clínica e demais testes.

### 3. Interpretação integrada
- A conclusão jamais deve ser mera soma de parágrafos soltos.
- É obrigatório integrar:
  - desempenho quantitativo;
  - achados qualitativos;
  - observação clínica;
  - dados da anamnese;
  - impacto funcional.

### 4. Hipótese diagnóstica
- A seção **Conclusão** deve conter **Hipótese Diagnóstica**.
- Sempre utilizar a expressão **“hipótese diagnóstica”**.
- Quando houver sustentação clínica, utilizar formulações como:
  - “Há hipótese diagnóstica de Transtorno do Déficit de Atenção/Hiperatividade (TDAH), apresentação combinada.”
  - “Há hipótese diagnóstica de Transtorno do Espectro Autista (TEA), nível 1 de suporte.”
- Quando solicitado, apresentar CID-11 no formato:
  - `CID-11: 6A05.0 – Transtorno do Déficit de Atenção/Hiperatividade (TDAH), apresentação predominantemente desatenta`
  - `CID-11: 6A02.0 – Transtorno do Espectro Autista (TEA), nível 1 de suporte`

### 5. Regras de nomenclatura
- Usar o nome do paciente conforme configuração do caso:
  - nome completo apenas em identificação e, quando necessário, na assinatura institucional;
  - nas análises, preferir o primeiro nome ou nome composto definido na configuração do caso.

### 6. Restrições de conteúdo
- Não incluir na anamnese temas sensíveis que o sistema tenha marcado como ocultáveis ou não publicáveis.
- Não incluir dados íntimos desnecessários.
- Respeitar o sigilo profissional.

## Regras específicas de formatação
Esta skill deve impor as seguintes regras visuais ao gerador de `.docx`:

### Página
- Tamanho: **A4**.
- Margens sugeridas:
  - superior: 3,0 cm
  - inferior: 2,5 cm
  - esquerda: 2,0 cm
  - direita: 2,0 cm

### Fonte
- Corpo do texto: **Times New Roman, 12 pt**.
- Títulos: **Times New Roman, 12 pt, negrito**.
- Legendas: **Times New Roman, 8 pt, itálico, abaixo do elemento**.

### Parágrafo
- Alinhamento justificado.
- Espaçamento entre linhas: 1,5.
- Recuo da primeira linha: 1,25 cm.
- Espaçamento entre parágrafos controlado para evitar visual fragmentado.

### Tabelas
- Devem ser usadas apenas quando o sistema estiver configurado para exibir tabelas.
- Cabeçalho em negrito.
- Conteúdo da tabela em Times New Roman 12.
- Legenda abaixo da tabela.
- Exemplo:
  - *Tabela 1. Resultados das funções executivas.*

### Gráficos
- Inserir gráfico apenas se o módulo do teste já o tiver gerado.
- Toda legenda de gráfico deve ficar abaixo.
- Exemplo:
  - *Gráfico 1. Perfil dos índices fatoriais do WISC-IV.*

### Figuras e imagens
- Legendas sempre abaixo, em itálico, tamanho 8.

## Lógica de geração por seções
A skill deve funcionar por blocos.

### Bloco 1 — Identificação
Gerar automaticamente a seção de identificação com base nos dados cadastrais.

### Bloco 2 — Descrição da Demanda
Usar o motivo do encaminhamento e o objetivo da avaliação para redigir um texto técnico, objetivo e clínico.

### Bloco 3 — Procedimentos
Listar:
- anamnese;
- número de sessões;
- devolutiva;
- instrumentos aplicados;
- objetivo resumido de cada instrumento.

### Bloco 4 — Análise Clínica Inicial
Transformar a anamnese estruturada em texto clínico contínuo, organizado por eixos:
- história pessoal;
- desenvolvimento;
- comportamento;
- escolaridade;
- vida social;
- antecedentes;
- síntese clínica.

### Bloco 5 — Interpretações por domínio
Cada domínio deve conter:
1. breve enquadre técnico do que foi avaliado;
2. síntese dos resultados principais;
3. interpretação clínica;
4. impacto funcional;
5. fechamento integrativo do domínio.

### Bloco 6 — Conclusão
A conclusão deve:
- integrar todos os achados;
- destacar funcionamento intelectual, atenção, funções executivas, linguagem, memória, aspectos emocionais e sociais;
- apontar convergências e divergências entre testes e observação clínica;
- conter a **Hipótese Diagnóstica**;
- encerrar com raciocínio clínico claro e formal.

### Bloco 7 — Sugestões de Conduta
Ordenar recomendações de forma clínica e prática.
Prioridade sugerida:
1. psiquiatra infantil / neurologista / psiquiatra / neurologista;
2. psicoterapia;
3. psicopedagogia;
4. terapia ocupacional;
5. fonoaudiologia;
6. treino de habilidades sociais;
7. orientação parental;
8. adaptações escolares.

## Comportamento esperado da IA
A IA deve operar em dois modos:

### Modo 1 — Rascunho completo
Gera o laudo inteiro a partir dos dados disponíveis.

### Modo 2 — Regeração por seção
Permite regenerar apenas uma seção, por exemplo:
- só a conclusão;
- só a anamnese;
- só a análise de atenção;
- só os encaminhamentos.

## Requisitos de implementação no backend
A skill deve ser organizada em uma arquitetura desacoplada.

### Estrutura sugerida
```text
apps/laudos/
  __init__.py
  models.py
  services/
    __init__.py
    context_builder.py
    template_loader.py
    section_generators.py
    laudo_generator.py
    docx_renderer.py
    bibliography_service.py
  prompts/
    laudo_base.md
    secoes/
      identificacao.md
      demanda.md
      procedimentos.md
      analise.md
      conclusao.md
      conduta.md
  templates/
    papel_timbrado_unimed.docx
    laudo_neuropsicologico_base.docx
```

## Responsabilidades dos serviços

### `context_builder.py`
Responsável por montar o contexto estruturado do laudo a partir de:
- paciente;
- avaliação;
- anamnese;
- testes vinculados;
- resultados corrigidos;
- interpretações já salvas.

### `template_loader.py`
Responsável por carregar:
- template `.docx` base;
- estilos de formatação;
- placeholders do documento.

### `section_generators.py`
Responsável por gerar cada seção do laudo separadamente.

### `laudo_generator.py`
Responsável por orquestrar:
- montagem do contexto;
- chamada da IA;
- composição final do conteúdo;
- revisão estrutural básica.

### `docx_renderer.py`
Responsável por:
- inserir texto no template;
- aplicar estilos;
- inserir tabelas;
- inserir gráficos;
- aplicar legendas abaixo dos elementos;
- exportar `.docx`.

### `bibliography_service.py`
Responsável por anexar referências bibliográficas padronizadas conforme os instrumentos realmente utilizados no caso.

## Prompt-base da IA
O motor de geração deve receber instruções no seguinte sentido:

- Você é responsável por redigir um laudo neuropsicológico técnico, formal, clínico e compatível com o padrão profissional brasileiro.
- Use apenas os dados fornecidos no contexto.
- Não invente informações.
- Integre resultados quantitativos, dados qualitativos, observação clínica e anamnese.
- Produza texto coeso, técnico, sem frases genéricas.
- Utilize a estrutura oficial do laudo do sistema.
- Inclua hipótese diagnóstica apenas quando houver sustentação clínica.
- Quando houver legenda de tabela, gráfico ou figura, ela deve ser curta, técnica e posicionada abaixo do elemento.

## Regras para o gerador de DOCX
O renderizador do arquivo final deve:

1. carregar o template base;
2. preservar cabeçalho e rodapé do papel timbrado;
3. inserir o conteúdo nas seções do documento;
4. aplicar Times New Roman 12 no corpo;
5. aplicar Times New Roman 8 itálico nas legendas;
6. posicionar toda legenda abaixo da tabela, gráfico ou figura;
7. evitar quebra inadequada de página em títulos isolados;
8. manter boa legibilidade e distribuição visual.

## Checklist de qualidade antes de salvar o laudo
Antes de finalizar o documento, a skill deve validar:

- se todas as seções obrigatórias foram geradas;
- se não há campos vazios aparentes;
- se não há nome de outro paciente no texto;
- se a hipótese diagnóstica está coerente com os dados;
- se as legendas estão abaixo dos elementos;
- se a fonte principal é Times New Roman 12;
- se não há travessões longos no corpo do texto;
- se o texto está em português formal e técnico;
- se as referências bibliográficas batem com os testes utilizados.

## Critérios de revisão automática
A skill deve recusar a geração final se identificar:
- mistura de nomes de pacientes;
- seções repetidas;
- CID incompatível com a conclusão;
- referências de testes não utilizados;
- texto excessivamente genérico;
- ausência da seção de hipótese diagnóstica.

## Resultado esperado
Ao final da implementação, o sistema deve ser capaz de:

- gerar laudos neuropsicológicos completos em `.docx`;
- manter padrão visual institucional;
- seguir o modelo clínico do serviço;
- produzir documentos revisáveis e escaláveis;
- reduzir retrabalho na redação dos laudos;
- padronizar tanto a forma quanto o raciocínio clínico do documento final.

## Observação final para implementação
O modelo do laudo de Álvaro deve ser utilizado como **referência de profundidade clínica, lógica argumentativa e estrutura**, e não como texto fixo a ser reaproveitado. Cada novo laudo deve ser regenerado a partir dos dados reais do paciente, preservando a individualização clínica do documento.
