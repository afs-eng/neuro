from .models import Patient


def create_patient(**data):
    nullable_fields = [
        "birth_date",
        "sex",
        "schooling",
        "school_name",
        "mother_name",
        "father_name",
        "phone",
        "email",
        "city",
        "state",
        "notes",
        "responsible_name",
        "responsible_phone",
    ]
    for field in nullable_fields:
        if field not in data or data.get(field) in ("", None):
            data[field] = None
    return Patient.objects.create(**data)


def update_patient(patient: Patient, **data):
    nullable_fields = [
        "birth_date",
        "sex",
        "schooling",
        "school_name",
        "mother_name",
        "father_name",
        "phone",
        "email",
        "city",
        "state",
        "notes",
        "responsible_name",
        "responsible_phone",
        "grade_year",
    ]
    for field in nullable_fields:
        if field not in data or data.get(field) in ("", None):
            data[field] = None
    for field, value in data.items():
        setattr(patient, field, value)
    patient.save()
    return patient
