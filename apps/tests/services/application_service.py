from apps.tests.models import TestApplication


def create_test_application(**data) -> TestApplication:
    return TestApplication.objects.create(**data)


def update_test_application(application: TestApplication, **data) -> TestApplication:
    for field, value in data.items():
        setattr(application, field, value)
    application.save()
    return application