from .email_service import send_anamnesis_invite_email
from .whatsapp_service import send_whatsapp_message


def send_anamnesis_invite_via_email(
    *, invite, public_url: str, message: str
) -> dict:
    subject = f"Anamnese - {invite.patient.full_name}"
    return send_anamnesis_invite_email(
        recipient_email=invite.recipient_email,
        subject=subject,
        body=message,
        recipient_name=invite.recipient_name,
        patient_name=invite.patient.full_name,
        public_url=public_url,
    )


def send_anamnesis_invite_via_whatsapp(
    *, invite, public_url: str, message: str
) -> dict:
    return send_whatsapp_message(
        recipient_phone=invite.recipient_phone,
        body=message,
    )
