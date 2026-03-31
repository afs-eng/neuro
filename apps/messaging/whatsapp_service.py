from urllib.parse import quote


def build_whatsapp_link(*, recipient_phone: str, body: str) -> str:
    phone = "".join(char for char in recipient_phone if char.isdigit())
    return f"https://wa.me/{phone}?text={quote(body)}"
