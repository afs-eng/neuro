from django.contrib import admin

from .models import Patient


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "full_name",
        "birth_date",
        "sex",
        "schooling",
        "city",
        "state",
        "updated_at",
    )
    list_filter = ("sex", "state", "schooling")
    search_fields = (
        "full_name",
        "mother_name",
        "father_name",
        "email",
        "phone",
        "city",
    )
    readonly_fields = ("created_at", "updated_at")

    fieldsets = (
        (
            "Dados principais",
            {
                "fields": (
                    "full_name",
                    "birth_date",
                    "sex",
                    "schooling",
                    "grade_year",
                    "school_name",
                )
            },
        ),
        (
            "Filiação e contato",
            {
                "fields": (
                    "mother_name",
                    "father_name",
                    "phone",
                    "email",
                    "city",
                    "state",
                )
            },
        ),
        (
            "Responsável",
            {
                "fields": (
                    "responsible_name",
                    "responsible_phone",
                )
            },
        ),
        (
            "Observações",
            {"fields": ("notes",)},
        ),
        (
            "Controle",
            {"fields": ("created_at", "updated_at")},
        ),
    )
