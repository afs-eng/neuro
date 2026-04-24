from ninja import Schema


class AIHealthOut(Schema):
    ok: bool
    provider: str
    model: str | None = None
    finish_reason: str | None = None


class AIHealthErrorOut(Schema):
    message: str
