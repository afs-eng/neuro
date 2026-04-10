from django.contrib import admin
from .models import EvaluationDocument


@admin.register(EvaluationDocument)
class EvaluationDocumentAdmin(admin.ModelAdmin):
    list_display = ["title", "evaluation", "patient", "document_type", "created_at"]
    list_filter = ["document_type"]
    search_fields = ["title", "evaluation__code", "patient__full_name"]
