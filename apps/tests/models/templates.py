from django.db import models

from apps.tests.models.instruments import Instrument


class TestInterpretationTemplate(models.Model):
    instrument = models.ForeignKey(
        Instrument,
        on_delete=models.CASCADE,
        related_name="interpretation_templates",
        verbose_name="instrumento",
    )
    title = models.CharField("título", max_length=255)
    content = models.TextField("conteúdo")
    is_active = models.BooleanField("ativo", default=True)

    created_at = models.DateTimeField("criado em", auto_now_add=True)
    updated_at = models.DateTimeField("atualizado em", auto_now=True)

    class Meta:
        ordering = ["instrument__name", "title"]
        verbose_name = "Template de interpretação"
        verbose_name_plural = "Templates de interpretação"

    def __str__(self):
        return f"{self.instrument.code} - {self.title}"