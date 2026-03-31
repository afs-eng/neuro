from .models import Patient


def create_patient(**data):
    nullable_fields = ["birth_date", "notes", "responsible_name", "responsible_phone"]
    blank_string_fields = [
        "sex",
        "schooling",
        "school_name",
        "grade_year",
        "mother_name",
        "father_name",
        "phone",
        "email",
        "city",
        "state",
    ]

    for field in nullable_fields:
        if field not in data or data.get(field) in ("", None):
            data[field] = None

    for field in blank_string_fields:
        if field not in data or data.get(field) is None:
            data[field] = ""

    return Patient.objects.create(**data)


def update_patient(patient: Patient, **data):
    nullable_fields = ["birth_date", "notes", "responsible_name", "responsible_phone"]
    blank_string_fields = [
        "sex",
        "schooling",
        "school_name",
        "grade_year",
        "mother_name",
        "father_name",
        "phone",
        "email",
        "city",
        "state",
    ]

    for field in nullable_fields:
        if field in data and data.get(field) in ("", None):
            data[field] = None

    for field in blank_string_fields:
        if field in data and data.get(field) is None:
            data[field] = ""

    for field, value in data.items():
        setattr(patient, field, value)
    patient.save()
    return patient
