from .email_service import send_anamnesis_invite_email
from .whatsapp_service import build_whatsapp_link


def send_anamnesis_invite_via_email(*, invite, public_url: str, message: str) -> dict:
    subject = f"Anamnese - {invite.patient.full_name}"
    return send_anamnesis_invite_email(
        recipient_email=invite.recipient_email,
        subject=subject,
        body=message,
    )


def send_anamnesis_invite_via_whatsapp(
    *, invite, public_url: str, message: str
) -> dict:
    whatsapp_link = build_whatsapp_link(
        recipient_phone=invite.recipient_phone, body=message
    )
    return {
        "channel": "whatsapp",
        "recipient": invite.recipient_phone,
        "whatsapp_link": whatsapp_link,
        "message": message,
    }
