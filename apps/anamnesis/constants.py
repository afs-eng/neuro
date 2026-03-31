from .templates import ALL_ANAMNESIS_TEMPLATES

ANAMNESIS_DEFAULT_EXPIRATION_DAYS = 14

ANAMNESIS_MESSAGE_TEMPLATE = (
    "Ola, {recipient_name}. Segue o link para preenchimento da anamnese referente "
    "a avaliacao de {patient_name}. O formulario pode ser preenchido com calma e salvo "
    "antes do envio final. Link: {public_url}"
)


def get_default_templates():
    return ALL_ANAMNESIS_TEMPLATES
