from django.http import JsonResponse


# API helper root
def api_root(request):
    return JsonResponse({"ok": True})
