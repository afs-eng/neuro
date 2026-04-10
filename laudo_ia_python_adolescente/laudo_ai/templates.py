
from __future__ import annotations

from .schemas import EvaluationContext


def patient_display_name(context: EvaluationContext) -> str:
    if context.style_rules.use_first_name_only_in_sections:
        return context.patient.nome.split()[0]
    return context.patient.nome


def render_identificacao(context: EvaluationContext) -> str:
    return f"""1.1. Identificação do laudo:

Autora: {context.author_name} ({context.author_registry})

Interessado: {context.referral.interessado}

Finalidade: {context.referral.finalidade}

1.2. Identificação da paciente:

Nome: {context.patient.nome}

Sexo: {context.patient.sexo}

Data de nascimento: {context.patient.data_nascimento}

Idade: {context.patient.idade_texto}

Filiação: {context.patient.filiacao}

Escolaridade: {context.patient.escolaridade}

Escola: {context.patient.escola}"""


def render_demanda(context: EvaluationContext) -> str:
    return f"""Motivo do Encaminhamento

{context.referral.motivo_encaminhamento}"""


def render_procedimentos(context: EvaluationContext) -> str:
    test_list = "
".join(
        f"• {test.instrument}" for test in context.tests if test.applied
    )
    patient_word = 'paciente'
    return f"""Para esta avaliação foram realizadas: uma sessão de anamnese, {context.sessions.testing_sessions:02d} sessões de testagem com a {patient_word} e uma sessão de devolutiva com sua mãe.

Anamnese

Instrumentos aplicados:

{test_list}"""


def render_historia_pessoal(context: EvaluationContext) -> str:
    return f"""História Pessoal

{context.history.historia_pessoal}"""


def render_conduta(context: EvaluationContext) -> str:
    name = patient_display_name(context)
    return f"""• Acompanhamento neurológico contínuo, com monitoramento do quadro clínico e dos possíveis impactos cognitivos da condição neurológica.

• Acompanhamento psicológico com foco em manejo da ansiedade, regulação emocional, tolerância à frustração e fortalecimento de habilidades sociais funcionais.

• Acompanhamento psicopedagógico especializado, com adaptação de estratégias ao perfil cognitivo de {name}.

• Intervenção fonoaudiológica, quando indicada, para suporte à comunicação funcional e à compreensão verbal.

• Avaliação e acompanhamento em Terapia Ocupacional, com foco em habilidades adaptativas, autonomia funcional e organização da rotina.

• Orientação à família para estruturação do ambiente, previsibilidade de rotina e manejo das dificuldades funcionais.

• Adaptações escolares, incluindo instruções segmentadas, recursos visuais, tempo ampliado e suporte individualizado."""


def render_fechamento(context: EvaluationContext) -> str:
    return """A Avaliação Neuropsicológica, quando bem fundamentada, é essencial para direcionar a reabilitação cognitiva e fornecer subsídios para outros profissionais em suas respectivas áreas de atuação.

É importante que o documento seja lido na íntegra, e não apenas a conclusão, para que se compreenda plenamente o raciocínio clínico utilizado ao longo de todo o processo avaliativo.

Com a devida autorização por escrito dos responsáveis, coloco-me à disposição para esclarecimentos e discussões sobre o exame."""


def render_referencias(context: EvaluationContext) -> str:
    return "

".join(context.references)
