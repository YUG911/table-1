from django.db import models
from accounts.models import Patient, User
from doctors.models import Doctor
from appointments.models import Appointment


class PatientRecord(models.Model):
    record_id = models.AutoField(primary_key=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, db_column='patient_id')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, db_column='doctor_id')
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE, db_column='appointment_id')
    diagnosis = models.CharField(max_length=500, null=True, blank=True)
    notes = models.CharField(max_length=500, null=True, blank=True)

    class Meta:
        db_table = 'patient_records'

    def __str__(self):
        return f"Record #{self.record_id} - {self.patient.user.full_name}"


class Prescription(models.Model):
    prescription_id = models.AutoField(primary_key=True)
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE, db_column='appointment_id')
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, db_column='uploaded_by')
    file_path = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'prescriptions'

    def __str__(self):
        return f"Prescription #{self.prescription_id}"


class Report(models.Model):
    report_id = models.AutoField(primary_key=True)
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, db_column='appointment_id')
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, db_column='uploaded_by')
    report_name = models.CharField(max_length=255)
    file_path = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'reports'

    def __str__(self):
        return self.report_name
