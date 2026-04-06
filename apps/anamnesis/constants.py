from .templates import ALL_ANAMNESIS_TEMPLATES

ANAMNESIS_DEFAULT_EXPIRATION_DAYS = 14

ANAMNESIS_MESSAGE_TEMPLATE = (
    "Olá, *{recipient_name}*! 👋\n"
    "\n"
    "Você recebeu um convite para preenchimento da *anamnese* referente "
    "à avaliação de *{patient_name}*.\n"
    "\n"
    "📋 O formulário pode ser preenchido com calma e salvo antes do envio final.\n"
    "\n"
    "Acesse pelo link abaixo:\n"
    "{public_url}"
)


def get_default_templates():
    return ALL_ANAMNESIS_TEMPLATES
