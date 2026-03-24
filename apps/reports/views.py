from django.shortcuts import render


def report_list_view(request):
    return render(request, "reports/list.html")
