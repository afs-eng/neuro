from django.contrib import admin

from apps.tests.models import Instrument, TestApplication, TestInterpretationTemplate


@admin.register(Instrument)
class InstrumentAdmin(admin.ModelAdmin):
    list_display = ("id", "code", "name", "category", "version", "is_active")
    list_filter = ("category", "is_active")
    search_fields = ("code", "name")


@admin.register(TestApplication)
class TestApplicationAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "evaluation",
        "instrument",
        "applied_on",
        "is_validated",
        "updated_at",
    )
    list_filter = ("instrument", "is_validated", "applied_on")
    search_fields = (
        "evaluation__patient__full_name",
        "instrument__code",
        "instrument__name",
    )
    readonly_fields = ("created_at", "updated_at")


@admin.register(TestInterpretationTemplate)
class TestInterpretationTemplateAdmin(admin.ModelAdmin):
    list_display = ("id", "instrument", "title", "is_active", "updated_at")
    list_filter = ("instrument", "is_active")
    search_fields = ("title", "instrument__code", "instrument__name")