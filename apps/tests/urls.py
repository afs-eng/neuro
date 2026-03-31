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
    path(
        "ebadep-ij/<int:application_id>/", views.ebaped_ij_form_view, name="ebadep_ij"
    ),
    path("ebadep-ij/", views.ebaped_ij_form_view, name="ebadep_ij_standalone"),
    path(
        "ebaped-ij/<int:application_id>/", views.ebaped_ij_form_view, name="ebaped_ij"
    ),
    path("ebaped-ij/", views.ebaped_ij_form_view, name="ebaped_ij_standalone"),
    path(
        "ebadep-ij/report/<int:application_id>/",
        views.ebaped_ij_report_view,
        name="ebadep_ij_report",
    ),
    path(
        "ebaped-ij/report/<int:application_id>/",
        views.ebaped_ij_report_view,
        name="ebaped_ij_report",
    ),
    path("ebadep-a/<int:application_id>/", views.ebadep_a_form_view, name="ebadep_a"),
    path("ebadep-a/", views.ebadep_a_form_view, name="ebadep_a_standalone"),
    path(
        "ebadep-a/report/<int:application_id>/",
        views.ebadep_a_report_view,
        name="ebadep_a_report",
    ),
    path("result/<int:application_id>/", views.test_result_view, name="result"),
    path("report/<int:application_id>/", views.bpa2_report_view, name="report"),
    path("wisc4/<int:application_id>/", views.wisc4_form_view, name="wisc4"),
    path("wisc4/", views.wisc4_form_view, name="wisc4_standalone"),
    path(
        "apply/<int:patient_id>/",
        views.apply_test_for_patient,
        name="apply_for_patient",
    ),
]
