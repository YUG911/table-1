from django.db import models
from accounts.models import Clinic, User


class Doctor(models.Model):
    doctor_id = models.AutoField(primary_key=True)
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE, db_column='clinic_id')
    doctor_name = models.CharField(max_length=255)
    specialization = models.CharField(max_length=255)
    qualification = models.CharField(max_length=255)
    experience = models.IntegerField()
    consultation_fee = models.DecimalField(max_digits=10, decimal_places=2)
    about = models.CharField(max_length=500)

    class Meta:
        db_table = 'doctors'


class DoctorAvailability(models.Model):
    availability_id = models.AutoField(primary_key=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, db_column='doctor_id')
    day_of_week = models.CharField(max_length=20)
    start_time = models.TimeField()
    end_time = models.TimeField()

    class Meta:
        db_table = 'doctor_availability'


class Review(models.Model):
    review_id = models.AutoField(primary_key=True)
    patient = models.ForeignKey('accounts.Patient', on_delete=models.CASCADE, db_column='patient_id')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, db_column='doctor_id')
    appointment = models.OneToOneField('appointments.Appointment', on_delete=models.CASCADE, db_column='appointment_id')
    rating = models.DecimalField(max_digits=2, decimal_places=1)
    review_text = models.CharField(max_length=500)

    class Meta:
        db_table = 'reviews'
