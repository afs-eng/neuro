from django.urls import path
from . import views

app_name = "tests"

urlpatterns = [
    path("", views.test_list_view, name="list"),
    path(
        "add/<int:evaluation_id>/<str:instrument_code>/",
        views.add_test_to_evaluation,
        name="add",
    ),
    path(
        "apply/<int:evaluation_id>/<str:instrument_code>/",
        views.add_test_to_evaluation,
        name="apply",
    ),
    path("bpa2/<int:application_id>/", views.bpa2_form_view, name="bpa2"),
    path("bpa2/", views.bpa2_form_view, name="bpa2_standalone"),
    path("result/<int:application_id>/", views.test_result_view, name="result"),
    path("report/<int:application_id>/", views.bpa2_report_view, name="report"),
    path("wisc4/", views.wisc4_form_view, name="wisc4"),
]
