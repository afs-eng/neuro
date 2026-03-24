from django.contrib import admin
from django.urls import path, include

from apps.api.router import api
from apps.patients import views as patient_views
from apps.evaluations import views as eval_views
from apps.tests import views as test_views
from apps.reports import views as report_views


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", api.urls),
    # Dashboard
    path("", patient_views.dashboard_view, name="dashboard"),
    # Pacientes
    path("pacientes/", include("apps.patients.urls")),
    # Avaliações
    path("avaliacoes/", include("apps.evaluations.urls")),
    # Testes
    path("testes/", include("apps.tests.urls")),
    # Relatórios
    path("relatorios/", include("apps.reports.urls")),
]
