from django.http import JsonResponse


def report_list_view(request):
    return JsonResponse({"ok": True})
