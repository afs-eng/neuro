from ninja import Router

from apps.ai.services.ai_healthcheck_service import AIHealthcheckService
from apps.api.auth import bearer_auth

from .schemas import AIHealthErrorOut, AIHealthOut


router = Router(tags=["ai"])


@router.get(
    "/health",
    response={200: AIHealthOut, 503: AIHealthErrorOut},
    auth=bearer_auth,
)
def ai_health(request):
    try:
        return 200, AIHealthcheckService.ensure_available(timeout=20)
    except ValueError as exc:
        return 503, {"message": str(exc)}
