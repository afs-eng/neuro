from django.http import JsonResponse


# Create your views here. API-only responses are returned as JSON.
def account_index(request):
    return JsonResponse({"ok": True})
