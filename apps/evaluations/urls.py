from django.urls import path
from . import views

app_name = "evaluations"

urlpatterns = [
    path("", views.evaluation_list_view, name="list"),
    path("nova/", views.evaluation_create_view, name="create"),
    path("<int:pk>/", views.evaluation_detail_view, name="detail"),
]
