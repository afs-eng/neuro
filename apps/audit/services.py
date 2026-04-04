from django.contrib.auth import get_user_model
from django.http import HttpRequest
from typing import Optional, Any
import json

User = get_user_model()


class AuditService:
    @staticmethod
    def log(
        request: Optional[HttpRequest],
        action: str,
        resource_type: str,
        resource_id: Optional[str] = None,
        changes: Optional[dict] = None,
        metadata: Optional[dict] = None,
    ):
        from apps.audit.models import AuditLog

        user = None
        ip_address = None
        user_agent = None

        if request and request.user.is_authenticated:
            user = request.user

        if request:
            ip_address = AuditService._get_client_ip(request)
            user_agent = request.META.get("HTTP_USER_AGENT", "")[:500]

        AuditLog.objects.create(
            user=user,
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            changes=changes or {},
            ip_address=ip_address,
            user_agent=user_agent,
            metadata=metadata or {},
        )

    @staticmethod
    def _get_client_ip(request: HttpRequest) -> str:
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR", "")
        return ip

    @staticmethod
    def track_create(
        request: Optional[HttpRequest], resource_type: str, resource_id: str, data: dict
    ):
        AuditService.log(request, "create", resource_type, resource_id, {"new": data})

    @staticmethod
    def track_update(
        request: Optional[HttpRequest],
        resource_type: str,
        resource_id: str,
        old_data: dict,
        new_data: dict,
    ):
        changes = {}
        for key in set(old_data.keys()) | set(new_data.keys()):
            old_val = old_data.get(key)
            new_val = new_data.get(key)
            if old_val != new_val:
                changes[key] = {"old": old_val, "new": new_val}

        if changes:
            AuditService.log(request, "update", resource_type, resource_id, changes)

    @staticmethod
    def track_delete(
        request: Optional[HttpRequest],
        resource_type: str,
        resource_id: str,
        old_data: dict,
    ):
        AuditService.log(
            request, "delete", resource_type, resource_id, {"deleted": old_data}
        )

    @staticmethod
    def track_view(
        request: Optional[HttpRequest], resource_type: str, resource_id: str
    ):
        AuditService.log(request, "view", resource_type, resource_id)

    @staticmethod
    def track_export(request: Optional[HttpRequest], resource_type: str, count: int):
        AuditService.log(request, "export", resource_type, metadata={"count": count})

    @staticmethod
    def track_print(
        request: Optional[HttpRequest], resource_type: str, resource_id: str
    ):
        AuditService.log(request, "print", resource_type, resource_id)
