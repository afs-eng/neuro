from django.db import models


class Instrument(models.Model):
    code = models.CharField("código", max_length=50, unique=True)
    name = models.CharField("nome", max_length=255)
    category = models.CharField("categoria", max_length=100, blank=True)
    version = models.CharField("versão", max_length=50, blank=True)
    is_active = models.BooleanField("ativo", default=True)
    created_at = models.DateTimeField("criado em", auto_now_add=True)
    updated_at = models.DateTimeField("atualizado em", auto_now=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Instrumento"
        verbose_name_plural = "Instrumentos"

    def __str__(self):
        return f"{self.name} ({self.code})"