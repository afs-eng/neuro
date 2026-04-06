import logging
from urllib.parse import quote

from django.conf import settings

logger = logging.getLogger(__name__)


def send_whatsapp_message(*, recipient_phone: str, body: str) -> dict:
    """Send WhatsApp message via Evolution API if configured, otherwise return wa.me link."""
    api_url = getattr(settings, "EVOLUTION_API_URL", "")
    api_key = getattr(settings, "EVOLUTION_API_KEY", "")
    instance = getattr(settings, "EVOLUTION_INSTANCE", "")

    if api_url and api_key and instance:
        return _send_via_evolution(
            api_url=api_url,
            api_key=api_key,
            instance=instance,
            recipient_phone=recipient_phone,
            body=body,
        )

    return _build_whatsapp_link(recipient_phone=recipient_phone, body=body)


def _send_via_evolution(
    *,
    api_url: str,
    api_key: str,
    instance: str,
    recipient_phone: str,
    body: str,
) -> dict:
    import requests

    phone = _normalize_phone(recipient_phone)
    url = f"{api_url.rstrip('/')}/message/sendText/{instance}"

    try:
        response = requests.post(
            url,
            headers={"apikey": api_key, "Content-Type": "application/json"},
            json={"number": phone, "text": body},
            timeout=15,
        )
        response.raise_for_status()
        data = response.json()
        external_id = data.get("key", {}).get("id", "")
        logger.info("Evolution API WhatsApp sent to %s — id: %s", phone, external_id)
        return {
            "channel": "whatsapp",
            "provider": "evolution",
            "recipient": phone,
            "external_id": external_id,
            "message": body,
            "auto_sent": True,
        }
    except requests.RequestException as exc:
        logger.warning(
            "Evolution API failed for %s: %s — falling back to wa.me link",
            phone,
            str(exc),
        )
        result = _build_whatsapp_link(recipient_phone=phone, body=body)
        result["fallback_reason"] = str(exc)
        return result


def _build_whatsapp_link(*, recipient_phone: str, body: str) -> dict:
    phone = _normalize_phone(recipient_phone)
    whatsapp_link = f"https://wa.me/{phone}?text={quote(body)}"
    return {
        "channel": "whatsapp",
        "provider": "wa_me_link",
        "recipient": phone,
        "whatsapp_link": whatsapp_link,
        "message": body,
        "auto_sent": False,
    }


def _normalize_phone(phone: str) -> str:
    digits = "".join(char for char in phone if char.isdigit())
    if digits and not digits.startswith("55") and len(digits) <= 11:
        digits = f"55{digits}"
    return digits
