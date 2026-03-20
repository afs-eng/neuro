from .models import Patient


def create_patient(**data):
    return Patient.objects.create(**data)


def update_patient(patient: Patient, **data):
    for field, value in data.items():
        setattr(patient, field, value)
    patient.save()
    return patient