from ninja.security import HttpBearer
from apps.accounts.models import User


class BearerAuth(HttpBearer):
    def authenticate(self, request, token):
        user = User.objects.filter(api_token=token, is_active=True).first()
        if user:
            return user
        return None


bearer_auth = BearerAuth()