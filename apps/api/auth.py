from ninja.security import HttpBearer
from django.db.models import Q

from apps.accounts.models import User
from apps.accounts.models import hash_api_token


class BearerAuth(HttpBearer):
    def authenticate(self, request, token):
        token_hash = hash_api_token(token)
        token_filters = Q(api_token_hash=token_hash)
        if not token.startswith("tok_"):
            token_filters |= Q(api_token=token)

        user = User.objects.filter(is_active=True).filter(token_filters).first()
        if user:
            return user
        return None


bearer_auth = BearerAuth()
