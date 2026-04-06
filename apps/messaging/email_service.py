import logging

from django.conf import settings

logger = logging.getLogger(__name__)

ANAMNESIS_EMAIL_HTML = """
<!DOCTYPE html>
<html lang="pt-BR">
<head><meta charset="UTF-8"></head>
<body style="margin:0;padding:0;background:#f4f6f8;font-family:'Segoe UI',Roboto,Arial,sans-serif;">
  <table width="100%" cellpadding="0" cellspacing="0" style="background:#f4f6f8;padding:40px 0;">
    <tr><td align="center">
      <table width="560" cellpadding="0" cellspacing="0" style="background:#ffffff;border-radius:12px;overflow:hidden;box-shadow:0 2px 12px rgba(0,0,0,0.08);">
        <tr>
          <td style="background:linear-gradient(135deg,#0f766e,#0d9488);padding:32px 40px;">
            <h1 style="margin:0;color:#ffffff;font-size:22px;font-weight:600;">NeuroAvalia</h1>
            <p style="margin:8px 0 0;color:#ccfbf1;font-size:14px;">Sistema de Avaliação Neuropsicológica</p>
          </td>
        </tr>
        <tr>
          <td style="padding:32px 40px;">
            <p style="margin:0 0 16px;color:#1e293b;font-size:16px;line-height:1.6;">
              Olá, <strong>{recipient_name}</strong>.
            </p>
            <p style="margin:0 0 24px;color:#475569;font-size:15px;line-height:1.6;">
              Você recebeu um convite para preenchimento da anamnese referente à avaliação de
              <strong>{patient_name}</strong>. O formulário pode ser preenchido com calma e salvo
              antes do envio final.
            </p>
            <table width="100%" cellpadding="0" cellspacing="0">
              <tr><td align="center" style="padding:8px 0 24px;">
                <a href="{public_url}" style="display:inline-block;background:#0f766e;color:#ffffff;text-decoration:none;padding:14px 32px;border-radius:8px;font-size:15px;font-weight:600;">
                  Preencher Anamnese
                </a>
              </td></tr>
            </table>
            <p style="margin:0;color:#94a3b8;font-size:13px;line-height:1.5;">
              Se o botão acima não funcionar, copie e cole este link no navegador:<br>
              <a href="{public_url}" style="color:#0f766e;word-break:break-all;">{public_url}</a>
            </p>
          </td>
        </tr>
        <tr>
          <td style="background:#f8fafc;padding:20px 40px;border-top:1px solid #e2e8f0;">
            <p style="margin:0;color:#94a3b8;font-size:12px;text-align:center;">
              Este é um e-mail automático do sistema NeuroAvalia. Não responda.
            </p>
          </td>
        </tr>
      </table>
    </td></tr>
  </table>
</body>
</html>
"""


def send_anamnesis_invite_email(
    *,
    recipient_email: str,
    subject: str,
    body: str,
    recipient_name: str = "",
    patient_name: str = "",
    public_url: str = "",
) -> dict:
    api_key = getattr(settings, "RESEND_API_KEY", "")

    if api_key:
        return _send_via_resend(
            api_key=api_key,
            recipient_email=recipient_email,
            subject=subject,
            recipient_name=recipient_name,
            patient_name=patient_name,
            public_url=public_url,
        )

    return _send_via_django_mail(
        recipient_email=recipient_email,
        subject=subject,
        body=body,
    )


def _send_via_resend(
    *,
    api_key: str,
    recipient_email: str,
    subject: str,
    recipient_name: str,
    patient_name: str,
    public_url: str,
) -> dict:
    import resend

    resend.api_key = api_key
    from_email = getattr(
        settings, "RESEND_FROM_EMAIL", "onboarding@resend.dev"
    )

    html = ANAMNESIS_EMAIL_HTML.format(
        recipient_name=recipient_name or "Responsável",
        patient_name=patient_name or "o paciente",
        public_url=public_url,
    )

    logger.info(
        "Sending email via Resend — to: %s, from: %s, key present: %s",
        recipient_email,
        from_email,
        bool(api_key),
    )

    try:
        result = resend.Emails.send(
            {
                "from": from_email,
                "to": recipient_email,
                "subject": subject,
                "html": html,
            }
        )
    except Exception as exc:
        logger.error("Resend API error: %s", exc)
        raise ValueError(f"Falha ao enviar e-mail via Resend: {exc}") from exc

    email_id = result.get("id", "") if isinstance(result, dict) else getattr(result, "id", "")
    logger.info("Resend email sent to %s — id: %s", recipient_email, email_id)
    return {
        "channel": "email",
        "provider": "resend",
        "recipient": recipient_email,
        "subject": subject,
        "external_id": email_id,
    }


def _send_via_django_mail(
    *, recipient_email: str, subject: str, body: str
) -> dict:
    from django.core.mail import send_mail

    send_mail(
        subject=subject,
        message=body,
        from_email=getattr(
            settings, "DEFAULT_FROM_EMAIL", "no-reply@neuroavalia.local"
        ),
        recipient_list=[recipient_email],
        fail_silently=False,
    )
    logger.info("Django SMTP email sent to %s", recipient_email)
    return {
        "channel": "email",
        "provider": "smtp",
        "recipient": recipient_email,
        "subject": subject,
        "external_id": "",
    }
