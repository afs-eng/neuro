from datetime import date
from django.db import models


class Patient(models.Model):
    full_name = models.CharField("nome completo", max_length=255)
    birth_date = models.DateField("data de nascimento", null=True, blank=True)
    sex = models.CharField("sexo", max_length=20, blank=True)
    schooling = models.CharField("escolaridade", max_length=120, blank=True)
    school_name = models.CharField("escola", max_length=255, blank=True)
    occupation = models.CharField("ocupação", max_length=120, blank=True)
    mother_name = models.CharField("nome da mãe", max_length=255, blank=True)
    father_name = models.CharField("nome do pai", max_length=255, blank=True)
    phone = models.CharField("telefone", max_length=30, blank=True)
    email = models.EmailField("e-mail", blank=True)
    city = models.CharField("cidade", max_length=120, blank=True)
    state = models.CharField("estado", max_length=80, blank=True)
    notes = models.TextField("observações", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["full_name"]
        verbose_name = "Paciente"
        verbose_name_plural = "Pacientes"

    def __str__(self):
        return self.full_name

    @property
    def age(self):
        if not self.birth_date:
            return None
        today = date.today()
        age = today.year - self.birth_date.year
        if (today.month, today.day) < (self.birth_date.month, self.birth_date.day):
            age -= 1
        return age
