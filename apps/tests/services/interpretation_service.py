from typing import Optional

from apps.tests.models import TestApplication, TestInterpretationTemplate
from apps.tests.selectors import get_active_template_for_instrument

class TestInterpretationService:
    @staticmethod
    def get_template_for_application(application: TestApplication) -> Optional[TestInterpretationTemplate]:
        return get_active_template_for_instrument(application.instrument_id)