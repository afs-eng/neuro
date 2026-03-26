from django.apps import AppConfig


class TestsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.tests"
    verbose_name = "Testes"

    def ready(self):
        from apps.tests.bpa2 import BPA2Module  # noqa
        from apps.tests.wisc4 import WISC4Module  # noqa
        from apps.tests.ebaped_ij import EBADEPIJModule  # noqa
        from apps.tests.ebadep_a import EBADEPAModule  # noqa
