from django.db import models
from accounts.models import Patient, User
from doctors.models import Doctor
from appointments.models import Appointment


class PatientRecord(models.Model):
    record_id = models.AutoField(primary_key=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, db_column='patient_id')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, db_column='doctor_id')
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE, db_column='appointment_id')
    diagnosis = models.CharField(max_length=500)
    notes = models.CharField(max_length=500)

    class Meta:
        db_table = 'patient_records'


class Prescription(models.Model):
    prescription_id = models.AutoField(primary_key=True)
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE, db_column='appointment_id')
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, db_column='uploaded_by')
    file_path = models.CharField(max_length=500)

    class Meta:
        db_table = 'prescriptions'


class Report(models.Model):
    report_id = models.AutoField(primary_key=True)
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, db_column='appointment_id')
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, db_column='uploaded_by')
    file_path = models.CharField(max_length=500)
    report_name = models.CharField(max_length=255)

    class Meta:
        db_table = 'reports'
