from .templates import ALL_ANAMNESIS_TEMPLATES

ANAMNESIS_DEFAULT_EXPIRATION_DAYS = 14

ANAMNESIS_MESSAGE_TEMPLATE = (
    "Olá, {recipient_name}!\n\n"
    "Convite para preenchimento da anamnese - avaliação de {patient_name}.\n\n"
    "Acesse: {public_url}"
)


def get_default_templates():
    return ALL_ANAMNESIS_TEMPLATES
