#!/usr/bin/env python3
"""
Gerador de Laudo de Avaliação Neuropsicológica
Dra. Jacqueline Oliveira Caires – CRP 09/6017
Conforme Resolução CFP 006/2019

Uso:
    python gerar_laudo.py dados.json saida.docx

O arquivo JSON pode ter qualquer subconjunto dos campos –
seções sem dados serão incluídas com placeholder "=== a preencher ===".
"""

import json
import subprocess
import sys
import os
import tempfile
from pathlib import Path

# ──────────────────────────────────────────────
# DADOS PADRÃO (placeholders)
# ──────────────────────────────────────────────
PLACEHOLDER = "=== a preencher ==="

DEFAULTS = {
    # Identificação do laudo
    "autora": "Jacqueline Oliveira Caires (CRP 09/6017)",
    "interessado": PLACEHOLDER,
    "finalidade": "Averiguação das capacidades cognitivas para auxílio diagnóstico",

    # Identificação do paciente
    "nome": PLACEHOLDER,
    "sexo": PLACEHOLDER,
    "data_nascimento": PLACEHOLDER,
    "idade": PLACEHOLDER,
    "filiacao": PLACEHOLDER,
    "escolaridade": PLACEHOLDER,
    "escola": PLACEHOLDER,

    # Procedimentos
    "num_sessoes_anamnese": "uma",
    "num_sessoes_testagem": "05",
    "responsavel_devolutiva": "sua mãe",
    "instrumentos": [
        {"sigla": "WISC-IV",    "nome": "Escala Wechsler de Inteligência para Crianças – Quarta Edição (WISC-IV)",
         "descricao": "utilizada para avaliar o funcionamento intelectual global, os índices fatoriais e fornecer indicadores sobre o perfil cognitivo."},
        {"sigla": "BPA-2",      "nome": "Bateria Psicológica para Avaliação da Atenção – Segunda Edição (BPA-2)",
         "descricao": "avalia a capacidade geral de atenção, incluindo atenção concentrada, alternada, dividida e atenção global."},
        {"sigla": "FDT",        "nome": "Teste dos Cinco Dígitos – FDT",
         "descricao": "investiga a velocidade de processamento, controle inibitório, alternância e flexibilidade cognitiva."},
        {"sigla": "RAVLT",      "nome": "Teste de Aprendizagem Auditivo-Verbal de Rey – RAVLT",
         "descricao": "avalia memória verbal episódica, aquisição, retenção, recuperação e resistência à interferência."},
        {"sigla": "E-TDAH",     "nome": "Escala para Transtorno de Déficit de Atenção e Hiperatividade (E-TDAH)",
         "descricao": "questionário para identificação de sintomas de desatenção, impulsividade, hiperatividade, regulação emocional e comportamento adaptativo."},
        {"sigla": "SCARED",     "nome": "Screen for Child Anxiety Related Emotional Disorders – SCARED",
         "descricao": "avalia sintomas ansiosos, incluindo ansiedade generalizada, de separação, fobia social e somatizações."},
        {"sigla": "SRS-2",      "nome": "Escala de Responsividade Social – Segunda Edição (SRS-2)",
         "descricao": "rastreia dificuldades em comunicação social, cognição social, padrões restritos e repetitivos e comportamentos associados ao espectro autista."},
        {"sigla": "EPQ-J",      "nome": "Inventário de Personalidade de Eysenck para Jovens – EPQ-J",
         "descricao": "aplicado para mensurar traços de personalidade relacionados a psicoticismo, extroversão, neuroticismo e sinceridade."},
    ],

    # Seções de conteúdo livre
    "motivo_encaminhamento": PLACEHOLDER,
    "historia_pessoal": PLACEHOLDER,

    # WISC-IV
    "wisc_qit": PLACEHOLDER,
    "wisc_classificacao_qit": PLACEHOLDER,
    "wisc_idade_cognitiva": PLACEHOLDER,
    "wisc_icv": PLACEHOLDER, "wisc_icv_class": PLACEHOLDER,
    "wisc_iop": PLACEHOLDER, "wisc_iop_class": PLACEHOLDER,
    "wisc_imo": PLACEHOLDER, "wisc_imo_class": PLACEHOLDER,
    "wisc_ivp": PLACEHOLDER, "wisc_ivp_class": PLACEHOLDER,
    "wisc_interpretacao": PLACEHOLDER,
    "wisc_funcao_executiva": [
        {"teste": "Semelhanças",         "max": PLACEHOLDER, "medio": PLACEHOLDER, "min": PLACEHOLDER, "obtido": PLACEHOLDER, "class": PLACEHOLDER},
        {"teste": "Conceitos Figurativos","max": PLACEHOLDER, "medio": PLACEHOLDER, "min": PLACEHOLDER, "obtido": PLACEHOLDER, "class": PLACEHOLDER},
        {"teste": "Compreensão",         "max": PLACEHOLDER, "medio": PLACEHOLDER, "min": PLACEHOLDER, "obtido": PLACEHOLDER, "class": PLACEHOLDER},
        {"teste": "Raciocínio Matricial","max": PLACEHOLDER, "medio": PLACEHOLDER, "min": PLACEHOLDER, "obtido": PLACEHOLDER, "class": PLACEHOLDER},
    ],
    "wisc_func_exec_interpretacao": PLACEHOLDER,
    "wisc_linguagem": [
        {"teste": "Semelhanças",  "max": PLACEHOLDER, "medio": PLACEHOLDER, "min": PLACEHOLDER, "obtido": PLACEHOLDER, "class": PLACEHOLDER},
        {"teste": "Vocabulário",  "max": PLACEHOLDER, "medio": PLACEHOLDER, "min": PLACEHOLDER, "obtido": PLACEHOLDER, "class": PLACEHOLDER},
        {"teste": "Compreensão",  "max": PLACEHOLDER, "medio": PLACEHOLDER, "min": PLACEHOLDER, "obtido": PLACEHOLDER, "class": PLACEHOLDER},
    ],
    "wisc_linguagem_interpretacao": PLACEHOLDER,
    "wisc_gnosias": [
        {"teste": "Raciocínio Matricial", "max": PLACEHOLDER, "medio": PLACEHOLDER, "min": PLACEHOLDER, "obtido": PLACEHOLDER, "class": PLACEHOLDER},
        {"teste": "Cubos",                "max": PLACEHOLDER, "medio": PLACEHOLDER, "min": PLACEHOLDER, "obtido": PLACEHOLDER, "class": PLACEHOLDER},
    ],
    "wisc_gnosias_interpretacao": PLACEHOLDER,
    "wisc_memoria": [
        {"teste": "Seq. Núm. e Letras", "max": PLACEHOLDER, "medio": PLACEHOLDER, "min": PLACEHOLDER, "obtido": PLACEHOLDER, "class": PLACEHOLDER},
        {"teste": "Dígitos",            "max": PLACEHOLDER, "medio": PLACEHOLDER, "min": PLACEHOLDER, "obtido": PLACEHOLDER, "class": PLACEHOLDER},
    ],
    "wisc_memoria_interpretacao": PLACEHOLDER,

    # BPA-2
    "bpa2_resultados": [
        {"escala": "Atenção Concentrada – AC", "pontos": PLACEHOLDER, "percentil": PLACEHOLDER, "class": PLACEHOLDER},
        {"escala": "Atenção Dividida – AD",    "pontos": PLACEHOLDER, "percentil": PLACEHOLDER, "class": PLACEHOLDER},
        {"escala": "Atenção Alternada – AA",   "pontos": PLACEHOLDER, "percentil": PLACEHOLDER, "class": PLACEHOLDER},
        {"escala": "Atenção Geral – AG",       "pontos": PLACEHOLDER, "percentil": PLACEHOLDER, "class": PLACEHOLDER},
    ],
    "bpa2_interpretacao": PLACEHOLDER,

    # RAVLT
    "ravlt_esperado": {"a1":"","a2":"","a3":"","a4":"","a5":"","b1":"","a6":"","a7":"","r":"","alt":"","ret":"","ip":"","ir":""},
    "ravlt_minimo":   {"a1":"","a2":"","a3":"","a4":"","a5":"","b1":"","a6":"","a7":"","r":"","alt":"","ret":"","ip":"","ir":""},
    "ravlt_obtido":   {"a1":"","a2":"","a3":"","a4":"","a5":"","b1":"","a6":"","a7":"","r":"","alt":"","ret":"","ip":"","ir":""},
    "ravlt_interpretacao": PLACEHOLDER,

    # FDT
    "fdt_resultados": [
        {"processo": "Leitura",      "tempo_medio": PLACEHOLDER, "tempo_obtido": PLACEHOLDER, "erros": PLACEHOLDER, "desempenho": PLACEHOLDER, "class": PLACEHOLDER},
        {"processo": "Contagem",     "tempo_medio": PLACEHOLDER, "tempo_obtido": PLACEHOLDER, "erros": PLACEHOLDER, "desempenho": PLACEHOLDER, "class": PLACEHOLDER},
        {"processo": "Escolha",      "tempo_medio": PLACEHOLDER, "tempo_obtido": PLACEHOLDER, "erros": PLACEHOLDER, "desempenho": PLACEHOLDER, "class": PLACEHOLDER},
        {"processo": "Alternância",  "tempo_medio": PLACEHOLDER, "tempo_obtido": PLACEHOLDER, "erros": PLACEHOLDER, "desempenho": PLACEHOLDER, "class": PLACEHOLDER},
        {"processo": "Inibição",     "tempo_medio": PLACEHOLDER, "tempo_obtido": PLACEHOLDER, "erros": PLACEHOLDER, "desempenho": PLACEHOLDER, "class": PLACEHOLDER},
        {"processo": "Flexibilidade","tempo_medio": PLACEHOLDER, "tempo_obtido": PLACEHOLDER, "erros": PLACEHOLDER, "desempenho": PLACEHOLDER, "class": PLACEHOLDER},
    ],
    "fdt_interpretacao": PLACEHOLDER,

    # E-TDAH (Pais / AD) – lista genérica de fatores
    "etdah_titulo": "E-TDAH",
    "etdah_resultados": [
        {"escala": PLACEHOLDER, "pontos": PLACEHOLDER, "media": PLACEHOLDER, "percentil": PLACEHOLDER, "class": PLACEHOLDER},
    ],
    "etdah_interpretacao": PLACEHOLDER,

    # SCARED
    "scared_autorrelato": [
        {"escala": "Pânico/Sintomas Somáticos",  "pontos": PLACEHOLDER, "media_ou_corte": PLACEHOLDER, "percentil": PLACEHOLDER, "class": PLACEHOLDER},
        {"escala": "Ansiedade Generalizada",      "pontos": PLACEHOLDER, "media_ou_corte": PLACEHOLDER, "percentil": PLACEHOLDER, "class": PLACEHOLDER},
        {"escala": "Ansiedade Separação",         "pontos": PLACEHOLDER, "media_ou_corte": PLACEHOLDER, "percentil": PLACEHOLDER, "class": PLACEHOLDER},
        {"escala": "Fobia Social",                "pontos": PLACEHOLDER, "media_ou_corte": PLACEHOLDER, "percentil": PLACEHOLDER, "class": PLACEHOLDER},
        {"escala": "Evitação Escolar",            "pontos": PLACEHOLDER, "media_ou_corte": PLACEHOLDER, "percentil": PLACEHOLDER, "class": PLACEHOLDER},
        {"escala": "Total",                       "pontos": PLACEHOLDER, "media_ou_corte": PLACEHOLDER, "percentil": PLACEHOLDER, "class": PLACEHOLDER},
    ],
    "scared_mae": [
        {"escala": "Pânico/Sintomas Somáticos",  "pontos": PLACEHOLDER, "media_ou_corte": PLACEHOLDER, "percentil": PLACEHOLDER, "class": PLACEHOLDER},
        {"escala": "Ansiedade Generalizada",      "pontos": PLACEHOLDER, "media_ou_corte": PLACEHOLDER, "percentil": PLACEHOLDER, "class": PLACEHOLDER},
        {"escala": "Ansiedade Separação",         "pontos": PLACEHOLDER, "media_ou_corte": PLACEHOLDER, "percentil": PLACEHOLDER, "class": PLACEHOLDER},
        {"escala": "Fobia Social",                "pontos": PLACEHOLDER, "media_ou_corte": PLACEHOLDER, "percentil": PLACEHOLDER, "class": PLACEHOLDER},
        {"escala": "Evitação Escolar",            "pontos": PLACEHOLDER, "media_ou_corte": PLACEHOLDER, "percentil": PLACEHOLDER, "class": PLACEHOLDER},
        {"escala": "Total",                       "pontos": PLACEHOLDER, "media_ou_corte": PLACEHOLDER, "percentil": PLACEHOLDER, "class": PLACEHOLDER},
    ],
    "scared_interpretacao": PLACEHOLDER,

    # EPQ-J
    "epqj_p_bruto": PLACEHOLDER, "epqj_p_percentil": PLACEHOLDER, "epqj_p_class": PLACEHOLDER,
    "epqj_e_bruto": PLACEHOLDER, "epqj_e_percentil": PLACEHOLDER, "epqj_e_class": PLACEHOLDER,
    "epqj_n_bruto": PLACEHOLDER, "epqj_n_percentil": PLACEHOLDER, "epqj_n_class": PLACEHOLDER,
    "epqj_s_bruto": PLACEHOLDER, "epqj_s_percentil": PLACEHOLDER, "epqj_s_class": PLACEHOLDER,
    "epqj_interpretacao": PLACEHOLDER,

    # SRS-2
    "srs2_resultados": [
        {"fator": "Percepção Social",             "brutos": PLACEHOLDER, "tscore": PLACEHOLDER, "percentil": PLACEHOLDER, "class": PLACEHOLDER},
        {"fator": "Cognição Social",              "brutos": PLACEHOLDER, "tscore": PLACEHOLDER, "percentil": PLACEHOLDER, "class": PLACEHOLDER},
        {"fator": "Comunicação Social",           "brutos": PLACEHOLDER, "tscore": PLACEHOLDER, "percentil": PLACEHOLDER, "class": PLACEHOLDER},
        {"fator": "Motivação Social",             "brutos": PLACEHOLDER, "tscore": PLACEHOLDER, "percentil": PLACEHOLDER, "class": PLACEHOLDER},
        {"fator": "Padrões Restritos e Repetitivos","brutos": PLACEHOLDER,"tscore": PLACEHOLDER,"percentil": PLACEHOLDER, "class": PLACEHOLDER},
        {"fator": "Comunicação e Interação Social","brutos": PLACEHOLDER,"tscore": PLACEHOLDER, "percentil": PLACEHOLDER, "class": PLACEHOLDER},
        {"fator": "Pontuação SRS-2 Total",        "brutos": PLACEHOLDER, "tscore": PLACEHOLDER, "percentil": PLACEHOLDER, "class": PLACEHOLDER},
    ],
    "srs2_interpretacao": PLACEHOLDER,

    # Conclusão e conduta
    "conclusao": PLACEHOLDER,
    "sugestoes_conduta": [PLACEHOLDER],

    # Assinatura
    "cidade": "Goiânia",
    "data_laudo": "=== data ===",
    "nome_profissional": "Jacqueline O. Caires",
    "crp": "CRP09/6017",
    "especialidade1": "Neuropsicóloga",
    "especialidade2": "Analista do Comportamento",
    "especialidade3": "Especialista em Saúde Mental",
    "email": "drajacquelinecaires@gmail.com",
    "telefone": "(64) 99201-2782",
}


def merge(defaults: dict, user: dict) -> dict:
    """Merge user data over defaults recursively for top-level keys."""
    result = dict(defaults)
    result.update(user)
    return result


# ──────────────────────────────────────────────
# GERADOR DE JS  (cada seção = função separada)
# ──────────────────────────────────────────────

def build_js(d: dict) -> str:
    """Retorna o código Node.js completo que gera o .docx."""

    # Serializa o objeto de dados para JS
    data_json = json.dumps(d, ensure_ascii=False, indent=2)

    margin_val = 1134

    return f"""
const {{
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  AlignmentType, HeadingLevel, LevelFormat, BorderStyle, WidthType,
  ShadingType, UnderlineType, PageNumber, Header, Footer
}} = require('docx');
const fs = require('fs');

const D = {data_json};

// ── Medidas A4 ──────────────────────────────
const PAGE_W = 11906;
const MARGIN  = {margin_val};   // ~2 cm
const CW      = PAGE_W - 2 * MARGIN;  // largura útil ≈ 9638

// ── Estilos base ────────────────────────────
const FONT = "Arial";
const SZ   = 24;   // 12 pt  (docx usa half-points)
const SZ_H1 = 28; // 14 pt

const border = {{ style: BorderStyle.SINGLE, size: 1, color: "AAAAAA" }};
const borders = {{ top: border, bottom: border, left: border, right: border }};

// ── Helpers ─────────────────────────────────

function p(children, opts={{}}) {{
  return new Paragraph({{ children, alignment: AlignmentType.JUSTIFIED, ...opts }});
}}

function t(text, opts={{}}) {{
  return new TextRun({{ text, font: FONT, size: SZ, ...opts }});
}}

function bold(text, opts={{}}) {{
  return t(text, {{ bold: true, ...opts }});
}}

function h1(text) {{
  return new Paragraph({{
    heading: HeadingLevel.HEADING_1,
    children: [new TextRun({{ text: text.toUpperCase(), font: FONT, size: SZ_H1, bold: true }})],
    spacing: {{ before: 360, after: 120 }},
  }});
}}

function h2(text) {{
  return new Paragraph({{
    heading: HeadingLevel.HEADING_2,
    children: [new TextRun({{ text, font: FONT, size: SZ, bold: true }})],
    spacing: {{ before: 240, after: 80 }},
  }});
}}

function h3(text) {{
  return new Paragraph({{
    heading: HeadingLevel.HEADING_3,
    children: [new TextRun({{ text, font: FONT, size: SZ, bold: true, underline: {{ type: UnderlineType.SINGLE }} }})],
    spacing: {{ before: 200, after: 60 }},
  }});
}}

function empty() {{
  return new Paragraph({{ children: [new TextRun("")] }});
}}

function bullet(text) {{
  return new Paragraph({{
    numbering: {{ reference: "bullets", level: 0 }},
    children: [t(text)],
  }});
}}

function labelValue(label, value) {{
  return p([bold(label + ": "), t(value)]);
}}

// ── Tabela genérica ──────────────────────────

function makeTable(headers, rows, colWidths) {{
  const total = colWidths.reduce((a,b) => a+b, 0);

  function hCell(txt, w) {{
    return new TableCell({{
      borders, width: {{ size: w, type: WidthType.DXA }},
      shading: {{ fill: "D5E8F0", type: ShadingType.CLEAR }},
      margins: {{ top: 60, bottom: 60, left: 100, right: 100 }},
      children: [new Paragraph({{ children: [new TextRun({{ text: txt, bold: true, font: FONT, size: SZ-2 }})] }})]
    }});
  }}

  function dCell(txt, w, isLast=false) {{
    return new TableCell({{
      borders, width: {{ size: w, type: WidthType.DXA }},
      margins: {{ top: 60, bottom: 60, left: 100, right: 100 }},
      shading: isLast ? {{ fill: "EEF4FB", type: ShadingType.CLEAR }} : undefined,
      children: [new Paragraph({{ children: [new TextRun({{ text: String(txt ?? ""), font: FONT, size: SZ-2, bold: isLast }})] }})]
    }});
  }}

  return new Table({{
    width: {{ size: CW, type: WidthType.DXA }},
    columnWidths: colWidths,
    rows: [
      new TableRow({{ children: headers.map((h,i) => hCell(h, colWidths[i])) }}),
      ...rows.map((row, ri) =>
        new TableRow({{ children: row.map((cell, ci) => dCell(cell, colWidths[ci], ri===rows.length-1 && ci===0)) }})
      )
    ]
  }});
}}

// ════════════════════════════════════════════
// SEÇÕES DO LAUDO
// ════════════════════════════════════════════

// ── 1. CABEÇALHO ────────────────────────────
function secCabecalho() {{
  return [
    new Paragraph({{
      alignment: AlignmentType.CENTER,
      spacing: {{ after: 80 }},
      children: [new TextRun({{
        text: "LAUDO DE AVALIAÇÃO NEUROPSICOLÓGICA",
        font: FONT, size: 32, bold: true,
        underline: {{ type: UnderlineType.SINGLE }}
      }})]
    }}),
    new Paragraph({{
      alignment: AlignmentType.CENTER,
      spacing: {{ after: 400 }},
      children: [t("De acordo com a Resolução de Elaboração de Documentos-CFP 006/2019")]
    }}),
  ];
}}

// ── 2. IDENTIFICAÇÃO ────────────────────────
function secIdentificacao() {{
  const d = D;
  return [
    h1("1. Identificação"),

    h2("1.1. Identificação do Laudo"),
    labelValue("Autora", d.autora),
    labelValue("Interessado", d.interessado),
    labelValue("Finalidade", d.finalidade),
    empty(),

    h2("1.2. Identificação do Paciente"),
    labelValue("Nome", d.nome),
    labelValue("Sexo", d.sexo),
    labelValue("Data de nascimento", d.data_nascimento),
    labelValue("Idade", d.idade),
    labelValue("Filiação", d.filiacao),
    labelValue("Escolaridade", d.escolaridade),
    ...(d.escola ? [labelValue("Escola", d.escola)] : []),
    empty(),
  ];
}}

// ── 3. DESCRIÇÃO DA DEMANDA ──────────────────
function secDemanda() {{
  return [
    h1("2. Descrição da Demanda"),
    h2("Motivo do Encaminhamento"),
    p([t(D.motivo_encaminhamento)]),
    empty(),
  ];
}}

// ── 4. PROCEDIMENTOS ────────────────────────
function secProcedimentos() {{
  const d = D;
  return [
    h1("3. Procedimentos"),
    p([t(`Para esta avaliação foram realizadas: ${{d.num_sessoes_anamnese}} sessão de anamnese, ${{d.num_sessoes_testagem}} sessões de testagem com o(a) paciente e uma sessão de devolutiva com ${{d.responsavel_devolutiva}}.`)]),
    empty(),
    bullet("Anamnese"),
    ...d.instrumentos.map(inst =>
      new Paragraph({{
        numbering: {{ reference: "bullets", level: 0 }},
        children: [
          bold(inst.nome + ": "),
          t(inst.descricao),
        ]
      }})
    ),
    empty(),
  ];
}}

// ── 5. ANÁLISE – HISTÓRIA PESSOAL ───────────
function secHistoriaPessoal() {{
  return [
    h1("4. Análise"),
    h2("História Pessoal"),
    p([t(D.historia_pessoal)]),
    empty(),
  ];
}}

// ── 6. ANÁLISE QUALITATIVA – WISC-IV ────────
function secWISC() {{
  const d = D;
  const subCols = [3200, 1300, 1300, 1000, 1100, 1738];

  return [
    h1("5. Análise Qualitativa"),
    h2("Capacidade Cognitiva Global – WISC-IV"),
    p([
      t("A paciente obteve, a partir da escala "),
      bold("WISC IV"),
      t(`, QI Total (QIT = ${{d.wisc_qit}}), ficando na classificação `),
      bold(d.wisc_classificacao_qit),
      t(`, com idade cognitiva estimada de ${{d.wisc_idade_cognitiva}}. Em relação aos índices fatoriais:`),
    ]),
    empty(),
    bullet(`Compreensão Verbal (ICV) – ${{d.wisc_icv}} – ${{d.wisc_icv_class}}`),
    bullet(`Organização Perceptual (IOP) – ${{d.wisc_iop}} – ${{d.wisc_iop_class}}`),
    bullet(`Memória Operacional (IMO) – ${{d.wisc_imo}} – ${{d.wisc_imo_class}}`),
    bullet(`Velocidade de Processamento (IVP) – ${{d.wisc_ivp}} – ${{d.wisc_ivp_class}}`),
    empty(),

    h2("Desempenho no WISC-IV"),
    p([t("[ Gráfico WISC-IV – Índices de QIs ]"), t("", {{ italics: true }})]),
    empty(),
    p([bold("Interpretação: "), t(d.wisc_interpretacao)]),
    empty(),

    // Subescalas
    h2("Subescalas WISC-IV"),

    h3("Função Executiva"),
    makeTable(
      ["Testes Utilizados","Escore Máximo","Escore Médio","Escore Mínimo","Escore Obtido","Classificação"],
      d.wisc_funcao_executiva.map(r => [r.teste, r.max, r.medio, r.min, r.obtido, r.class]),
      subCols
    ),
    empty(),
    p([bold("Interpretação: "), t(d.wisc_func_exec_interpretacao)]),
    empty(),

    h3("Linguagem"),
    makeTable(
      ["Testes Utilizados","Escore Máximo","Escore Médio","Escore Mínimo","Escore Obtido","Classificação"],
      d.wisc_linguagem.map(r => [r.teste, r.max, r.medio, r.min, r.obtido, r.class]),
      subCols
    ),
    empty(),
    p([bold("Interpretação: "), t(d.wisc_linguagem_interpretacao)]),
    empty(),

    h3("Gnosias e Praxias"),
    makeTable(
      ["Testes Utilizados","Escore Máximo","Escore Médio","Escore Mínimo","Escore Obtido","Classificação"],
      d.wisc_gnosias.map(r => [r.teste, r.max, r.medio, r.min, r.obtido, r.class]),
      subCols
    ),
    empty(),
    p([bold("Interpretação: "), t(d.wisc_gnosias_interpretacao)]),
    empty(),

    h3("Memória e Aprendizagem"),
    makeTable(
      ["Testes Utilizados","Escore Máximo","Escore Médio","Escore Mínimo","Escore Obtido","Classificação"],
      d.wisc_memoria.map(r => [r.teste, r.max, r.medio, r.min, r.obtido, r.class]),
      subCols
    ),
    empty(),
    p([bold("Interpretação: "), t(d.wisc_memoria_interpretacao)]),
    empty(),
  ];
}}

// ── 7. BPA-2 ────────────────────────────────
function secBPA2() {{
  const cols = [3800, 1500, 1600, 2738];
  return [
    h1("BPA-2 – Bateria Psicológica para Avaliação da Atenção"),
    p([t("A Bateria Psicológica para Avaliação da Atenção-2 (BPA-2) mensura a capacidade geral de atenção, avaliando individualmente: Atenção Concentrada (AC), Atenção Dividida (AD) e Atenção Alternada (AA).")]),
    empty(),
    makeTable(
      ["Atenção BPA","Pontos","Percentil","Classificação"],
      D.bpa2_resultados.map(r => [r.escala, r.pontos, r.percentil, r.class]),
      cols
    ),
    empty(),
    p([bold("Interpretação: "), t(D.bpa2_interpretacao)]),
    p([t("[ Gráfico BPA-2 – Resultados da avaliação da atenção ]")]),
    empty(),
  ];
}}

// ── 8. RAVLT ────────────────────────────────
function secRAVLT() {{
  const d = D;
  const cols = [1350,700,700,700,700,700,700,700,700,650,700,750,750];
  const headers = ["Desempenho","A1","A2","A3","A4","A5","B1","A6","A7","R","ALT","RET","I.P.","I.R."];
  const hCols   = [1350,700,700,700,700,700,700,700,700,650,700,750,750,750];

  function ravltRow(label, obj) {{
    const keys = ["a1","a2","a3","a4","a5","b1","a6","a7","r","alt","ret","ip","ir"];
    return [label, ...keys.map(k => String(obj[k] ?? ""))];
  }}

  return [
    h1("RAVLT – Rey Auditory Verbal Learning Test"),
    p([t("O RAVLT avalia a memória verbal, a capacidade de aprendizado auditivo e a retenção de informações ao longo do tempo (Lezak et al., 2004).")]),
    empty(),
    p([t("[ Gráfico RAVLT – Resultados ]")]),
    empty(),
    new Table({{
      width: {{ size: CW, type: WidthType.DXA }},
      columnWidths: hCols,
      rows: [
        new TableRow({{ children: headers.map((h,i) => new TableCell({{
          borders,
          width: {{ size: hCols[i], type: WidthType.DXA }},
          shading: {{ fill: "D5E8F0", type: ShadingType.CLEAR }},
          margins: {{ top: 60, bottom: 60, left: 80, right: 80 }},
          children: [new Paragraph({{ children: [new TextRun({{ text: h, bold: true, font: FONT, size: 18 }})] }})]
        }})) }}),
        ...[
          ravltRow("Esperado", d.ravlt_esperado),
          ravltRow("Mínimo",   d.ravlt_minimo),
          ravltRow("Obtido",   d.ravlt_obtido),
        ].map(row => new TableRow({{ children: row.map((cell,i) => new TableCell({{
          borders,
          width: {{ size: hCols[i], type: WidthType.DXA }},
          margins: {{ top: 60, bottom: 60, left: 80, right: 80 }},
          children: [new Paragraph({{ children: [new TextRun({{ text: String(cell), font: FONT, size: 18 }})] }})]
        }})) }}))
      ]
    }}),
    empty(),
    p([bold("Interpretação: "), t(d.ravlt_interpretacao)]),
    empty(),
  ];
}}

// ── 9. FDT ──────────────────────────────────
function secFDT() {{
  const cols = [2000, 1400, 1400, 900, 1200, 2738];
  return [
    h1("FDT – Teste dos Cinco Dígitos"),
    p([t("O FDT avalia processos automáticos (baixa demanda executiva) e controlados (inibição, alternância, flexibilidade cognitiva), relacionados aos circuitos pré-frontais e frontoestriatais.")]),
    empty(),
    makeTable(
      ["Processo","Tempo Médio","Tempo Obtido","Erros","Desempenho","Classificação"],
      D.fdt_resultados.map(r => [r.processo, r.tempo_medio, r.tempo_obtido, r.erros, r.desempenho, r.class]),
      cols
    ),
    empty(),
    p([bold("Interpretação: "), t(D.fdt_interpretacao)]),
    p([t("[ Gráfico FDT – Processos Automáticos ]")]),
    p([t("[ Gráfico FDT – Processos Controlados ]")]),
    empty(),
  ];
}}

// ── 10. E-TDAH ──────────────────────────────
function secETDAH() {{
  const d = D;
  const cols = [3500, 1300, 1300, 1300, 2238];
  return [
    h1(d.etdah_titulo),
    p([t("A Escala E-TDAH identifica manifestações comportamentais e emocionais associadas ao TDAH a partir da percepção dos pais ou responsáveis (Benczik, 2005).")]),
    empty(),
    makeTable(
      ["Escala","Pontos Brutos","Média","Percentil","Classificação"],
      d.etdah_resultados.map(r => [r.escala, r.pontos, r.media, r.percentil, r.class]),
      cols
    ),
    empty(),
    p([bold("Interpretação: "), t(d.etdah_interpretacao)]),
    p([t("[ Gráfico E-TDAH – Resultados ]")]),
    empty(),
  ];
}}

// ── 11. SCARED ──────────────────────────────
function secSCARED() {{
  const d = D;
  const cols = [2800, 1300, 1500, 1300, 2738];
  const headers = ["Escala","Pontos Brutos","Média / Nota de Corte","Percentil","Classificação"];

  return [
    h1("SCARED – Screen for Child Anxiety Related Emotional Disorders"),
    p([t("O SCARED rastreia sintomas ansiosos: pânico, ansiedade generalizada, ansiedade de separação, fobia social e evitação escolar (Birmaher et al., 1999).")]),
    empty(),

    h2("SCARED – Autorrelato"),
    makeTable(headers, d.scared_autorrelato.map(r => [r.escala, r.pontos, r.media_ou_corte, r.percentil, r.class]), cols),
    empty(),

    h2("SCARED – Mãe / Responsável"),
    makeTable(headers, d.scared_mae.map(r => [r.escala, r.pontos, r.media_ou_corte, r.percentil, r.class]), cols),
    empty(),

    p([bold("Interpretação: "), t(d.scared_interpretacao)]),
    p([t("[ Gráfico SCARED – Resultados ]")]),
    empty(),
  ];
}}

// ── 12. EPQ-J ───────────────────────────────
function secEPQJ() {{
  const d = D;
  const cols = [2400, 1500, 1500, 2000, 2238];
  return [
    h1("EPQ-J – Inventário de Personalidade de Eysenck para Jovens"),
    empty(),
    makeTable(
      ["Dimensão","Resultado Bruto","Percentil","Classificação",""],
      [
        ["Psicoticismo (P)", d.epqj_p_bruto, d.epqj_p_percentil, d.epqj_p_class, ""],
        ["Extroversão (E)",  d.epqj_e_bruto, d.epqj_e_percentil, d.epqj_e_class, ""],
        ["Neuroticismo (N)", d.epqj_n_bruto, d.epqj_n_percentil, d.epqj_n_class, ""],
        ["Sinceridade (S)",  d.epqj_s_bruto, d.epqj_s_percentil, d.epqj_s_class, ""],
      ],
      cols
    ),
    empty(),
    p([bold("Interpretação: "), t(d.epqj_interpretacao)]),
    p([t("[ Gráfico EPQ-J – Resultados dos percentis ]")]),
    empty(),
  ];
}}

// ── 13. SRS-2 ───────────────────────────────
function secSRS2() {{
  const cols = [3000, 1300, 1300, 1300, 2738];
  return [
    h1("SRS-2 – Escala de Responsividade Social"),
    p([t("A SRS-2 avalia aspectos da interação social e comportamentos associados ao espectro autista (Constantino & Gruber, 2012).")]),
    empty(),
    makeTable(
      ["Fator","Pontos Brutos","T-Score","Percentil","Classificação"],
      D.srs2_resultados.map(r => [r.fator, r.brutos, r.tscore, r.percentil, r.class]),
      cols
    ),
    empty(),
    p([bold("Interpretação: "), t(D.srs2_interpretacao)]),
    p([t("[ Gráfico SRS-2 – Resultados ]")]),
    empty(),
  ];
}}

// ── 14. CONCLUSÃO ───────────────────────────
function secConclusao() {{
  const d = D;
  return [
    h1("Conclusão"),
    p([t(d.conclusao)]),
    empty(),
    p([bold("Sugestões de Conduta (Encaminhamentos):")]),
    ...d.sugestoes_conduta.map(s => bullet(s)),
    empty(),
  ];
}}

// ── 15. EQUIPE MULTIDISCIPLINAR ─────────────
function secEquipe() {{
  const d = D;
  return [
    h1("A Equipe Multidisciplinar"),
    p([t("A Avaliação Neuropsicológica, quando bem fundamentada, é essencial para direcionar a reabilitação cognitiva e fornecer subsídios para outros profissionais em suas respectivas áreas de atuação. Dessa forma, a anamnese é realizada de forma detalhada, e por se tratar de um documento sigiloso, seu conteúdo só deve ser compartilhado, fotocopiado ou discutido com terceiros mediante autorização por escrito dos pais ou responsáveis.")]),
    empty(),
    p([t("É importante que o documento seja lido na íntegra, e não apenas a conclusão, para que se compreenda plenamente o raciocínio clínico utilizado ao longo de todo o processo avaliativo. Ressalta-se que o uso das informações contidas na Avaliação Neuropsicológica deve seguir princípios éticos, preservando e protegendo a integridade socioemocional da paciente, evitando qualquer exposição a situações de constrangimento ou discriminação.")]),
    empty(),
    p([t(`Com a devida autorização por escrito dos pais, coloco-me à disposição para esclarecimentos e discussões sobre o exame, podendo ser contatada pelo e-mail `), bold(d.email), t(` ou pelo telefone `), bold(d.telefone), t(".")]),
    empty(),
    p([t(`${{d.cidade}}, ${{d.data_laudo}}`)]),
    empty(),
    p([bold(d.nome_profissional)]),
    p([t(`${{d.especialidade1}} – ${{d.crp}}`)]),
    p([t(d.especialidade2)]),
    p([t(d.especialidade3)]),
    empty(),
    h2("Importante ressaltar que este documento:"),
    p([t("1. Não deve ser utilizado para fins diferentes daqueles especificados no item de identificação do documento.")]),
    p([t("2. Possui caráter sigiloso e extrajudicial, não cabendo à psicóloga a responsabilidade pelo seu uso indevido ou pela entrega do laudo sem autorização adequada.")]),
    p([t("3. A análise isolada deste laudo não possui valor diagnóstico se não for considerada em conjunto com dados clínicos, epistemológicos, exames de neuroimagem e laboratoriais adicionais referentes ao paciente.")]),
    p([t("4. Esta avaliação está em conformidade com as Resoluções CRP 09/2018 e 06/2019. Em conformidade com o Código de Ética Profissional, este exame deve ser tratado como confidencial.")]),
    empty(),
    p([t("Ressalta-se que o ser humano possui uma natureza dinâmica; não definitiva e não cristalizada. Sendo assim, os resultados aqui expostos dizem respeito ao funcionamento das funções cognitivas, como também, da personalidade, humor e afetividade do(a) paciente no momento presente, podendo haver alterações posteriores, dependendo das contingências ambientais vivenciadas e/ou do(s) acompanhamento(s) recebido(s).")]),
    empty(),
  ];
}}

// ── 16. REFERÊNCIAS ─────────────────────────
function secReferencias() {{
  const refs = [
    "CONSELHO FEDERAL DE PSICOLOGIA (CFP). Resolução nº 6, de 29 de março de 2019. Brasília: CFP, 2019.",
    "WECHSLER, D. WISC-IV – Escala de Inteligência Wechsler para Crianças – Quarta Edição. São Paulo: Pearson, 2013.",
    "RUEDA, F. J. M. Bateria Psicológica para Avaliação da Atenção – BPA-2. São Paulo: Vetor Editora, 2013.",
    "LEZAK, M. D.; HOWIESON, D. B.; BIGLER, E. D.; TRANEL, D. Neuropsychological Assessment. 5. ed. New York: Oxford University Press, 2012.",
    "STRAUSS, E.; SHERMAN, E. M. S.; SPREEN, O. A compendium of neuropsychological tests. 3. ed. New York: Oxford University Press, 2006.",
    "SALLES, J. F.; FONSECA, R. P.; PARENTE, M. A. M. P. Teste dos Cinco Dígitos (FDT). São Paulo: Casa do Psicólogo, 2011.",
    "BENCZIK, E. B. P. Escala de Transtorno de Déficit de Atenção e Hiperatividade – E-TDAH. São Paulo: Casa do Psicólogo, 2005.",
    "BIRMAHER, B. et al. Screen for Child Anxiety Related Emotional Disorders (SCARED). JAACAP, v. 36, n. 4, p. 545–553, 1997.",
    "CONSTANTINO, J. N.; GRUBER, C. P. Social Responsiveness Scale – Second Edition (SRS-2). Torrance, CA: WPS, 2012.",
    "EYSENCK, H. J.; EYSENCK, S. B. G. Inventário de Personalidade de Eysenck – Versão Jovens (EPQ-J). São Paulo: Vetor Editora, 2001.",
  ];
  return [
    h1("Referências Bibliográficas"),
    ...refs.map(ref => p([t(ref)], {{ spacing: {{ after: 100 }} }})),
  ];
}}

// ════════════════════════════════════════════
// MONTAGEM FINAL
// ════════════════════════════════════════════
const allChildren = [
  ...secCabecalho(),
  ...secIdentificacao(),
  ...secDemanda(),
  ...secProcedimentos(),
  ...secHistoriaPessoal(),
  ...secWISC(),
  ...secBPA2(),
  ...secRAVLT(),
  ...secFDT(),
  ...secETDAH(),
  ...secSCARED(),
  ...secEPQJ(),
  ...secSRS2(),
  ...secConclusao(),
  ...secEquipe(),
  ...secReferencias(),
];

const doc = new Document({{
  numbering: {{
    config: [{{
      reference: "bullets",
      levels: [{{
        level: 0,
        format: LevelFormat.BULLET,
        text: "•",
        alignment: AlignmentType.LEFT,
        style: {{ paragraph: {{ indent: {{ left: 720, hanging: 360 }} }} }}
      }}]
    }}]
  }},
  styles: {{
    default: {{
      document: {{ run: {{ font: FONT, size: SZ }} }}
    }},
    paragraphStyles: [
      {{ id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true,
         run: {{ size: SZ_H1, bold: true, font: FONT }},
         paragraph: {{ spacing: {{ before: 360, after: 120 }}, outlineLevel: 0 }} }},
      {{ id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true,
         run: {{ size: SZ, bold: true, font: FONT }},
         paragraph: {{ spacing: {{ before: 240, after: 80 }}, outlineLevel: 1 }} }},
      {{ id: "Heading3", name: "Heading 3", basedOn: "Normal", next: "Normal", quickFormat: true,
         run: {{ size: SZ, bold: true, font: FONT }},
         paragraph: {{ spacing: {{ before: 200, after: 60 }}, outlineLevel: 2 }} }},
    ]
  }},
  sections: [{{
    properties: {{
      page: {{
        size: {{ width: 11906, height: 16838 }},
        margin: {{ top: MARGIN, right: MARGIN, bottom: MARGIN, left: MARGIN }}
      }}
    }},
    children: allChildren,
  }}]
}});

const outPath = process.argv[2] || "laudo.docx";
Packer.toBuffer(doc).then(buf => {{
  fs.writeFileSync(outPath, buf);
  console.log("✅ Laudo gerado: " + outPath);
}}).catch(err => {{
  console.error("❌ Erro:", err);
  process.exit(1);
}});
""".replace("{MARGIN}", str(margin_val))


# ──────────────────────────────────────────────
# ENTRADA PRINCIPAL
# ──────────────────────────────────────────────

def main():
    # Lê JSON de dados (opcional)
    user_data = {}
    if len(sys.argv) >= 2 and sys.argv[1].endswith(".json"):
        json_path = sys.argv[1]
        with open(json_path, encoding="utf-8") as f:
            user_data = json.load(f)
        output_path = sys.argv[2] if len(sys.argv) >= 3 else "laudo.docx"
    elif len(sys.argv) >= 2 and sys.argv[1].endswith(".docx"):
        output_path = sys.argv[1]
    else:
        output_path = "laudo.docx"

    # Mescla dados
    data = merge(DEFAULTS, user_data)

    # Gera JS
    js_code = build_js(data)

    # Escreve arquivo temporário JS
    with tempfile.NamedTemporaryFile(mode="w", suffix=".js",
                                     delete=False, encoding="utf-8") as f:
        f.write(js_code)
        js_file = f.name

    try:
        result = subprocess.run(
            ["node", js_file, output_path],
            capture_output=True, text=True
        )
        if result.returncode != 0:
            print("❌ Erro no Node.js:")
            print(result.stderr)
            sys.exit(1)
        print(result.stdout.strip())
        print(f"📄 Arquivo salvo em: {os.path.abspath(output_path)}")
    finally:
        os.unlink(js_file)


if __name__ == "__main__":
    main()
