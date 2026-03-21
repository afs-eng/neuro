from django.contrib import admin

from .models import Evaluation


@admin.register(Evaluation)
class EvaluationAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "patient",
        "examiner",
        "status",
        "start_date",
        "end_date",
        "updated_at",
    )
    list_filter = ("status", "start_date", "end_date")
    search_fields = (
        "patient__full_name",
        "examiner__username",
        "examiner__full_name",
        "referral_reason",
        "evaluation_purpose",
    )
    readonly_fields = ("created_at", "updated_at")

    fieldsets = (
        (
            "Vínculos principais",
            {
                "fields": (
                    "patient",
                    "examiner",
                    "status",
                )
            },
        ),
        (
            "Dados clínicos",
            {
                "fields": (
                    "referral_reason",
                    "evaluation_purpose",
                    "general_notes",
                )
            },
        ),
        (
            "Datas",
            {
                "fields": (
                    "start_date",
                    "end_date",
                )
            },
        ),
        (
            "Controle",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )