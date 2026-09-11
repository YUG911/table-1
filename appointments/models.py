from django.db import models
from accounts.models import Patient, Clinic
from doctors.models import Doctor


class Appointment(models.Model):
    appointment_id = models.AutoField(primary_key=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, db_column='patient_id')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, db_column='doctor_id')
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE, db_column='clinic_id')
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    symptoms = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=50)
    patient_type = models.CharField(max_length=20)
    fee_charged = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    class Meta:
        db_table = 'appointments'

    def __str__(self):
        return f"Appointment #{self.appointment_id} - {self.patient.user.full_name} with {self.doctor.doctor_name}"


class Payment(models.Model):
    payment_id = models.AutoField(primary_key=True)
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE, db_column='appointment_id')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50)
    payment_status = models.CharField(max_length=20)
    paid_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'payments'

    def __str__(self):
        return f"Payment #{self.payment_id} - {self.payment_status}"
