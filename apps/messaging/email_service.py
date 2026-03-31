from django.conf import settings
from django.core.mail import send_mail


def send_anamnesis_invite_email(
    *, recipient_email: str, subject: str, body: str
) -> dict:
    send_mail(
        subject=subject,
        message=body,
        from_email=getattr(
            settings, "DEFAULT_FROM_EMAIL", "no-reply@neuroavalia.local"
        ),
        recipient_list=[recipient_email],
        fail_silently=False,
    )
    return {"channel": "email", "recipient": recipient_email, "subject": subject}
