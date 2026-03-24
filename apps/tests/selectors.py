from typing import Optional

from django.db.models import QuerySet

from apps.tests.models import Instrument, TestApplication, TestInterpretationTemplate

def get_instruments() -> QuerySet[Instrument]:
    return Instrument.objects.filter(is_active=True).order_by("name")


def get_instrument_by_id(instrument_id: int) -> Optional[Instrument]:
    return Instrument.objects.filter(id=instrument_id).first()


def get_instrument_by_code(code: str) -> Optional[Instrument]:
    return Instrument.objects.filter(code=code).first()


def get_test_applications() -> QuerySet[TestApplication]:
    return (
        TestApplication.objects.with_details()
        .all()
        .order_by("-created_at")
    )


def get_test_application_by_id(application_id: int) -> Optional[TestApplication]:
    return (
        TestApplication.objects.with_details()
        .filter(id=application_id)
        .first()
    )


def get_test_applications_by_evaluation(evaluation_id: int) -> QuerySet[TestApplication]:
    return (
        TestApplication.objects.with_details()
        .filter(evaluation_id=evaluation_id)
        .order_by("-created_at")
    )


def get_active_template_for_instrument(instrument_id: int) -> Optional[TestInterpretationTemplate]:
    return (
        TestInterpretationTemplate.objects.filter(
            instrument_id=instrument_id,
            is_active=True,
        )
        .order_by("-updated_at")
        .first()
    )