from django.db import models
from accounts.models import Clinic, User, DayMaster


class Doctor(models.Model):
    doctor_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, db_column='user_id')
    doctor_name = models.CharField(max_length=255)
    experience = models.IntegerField(null=True, blank=True)
    new_patient_fee = models.DecimalField(max_digits=10, decimal_places=2)
    old_patient_fee = models.DecimalField(max_digits=10, decimal_places=2)
    about = models.CharField(max_length=500, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'doctors'

    def __str__(self):
        return self.doctor_name


class SpecializationMaster(models.Model):
    specialization_id = models.AutoField(primary_key=True)
    specialization_name = models.CharField(max_length=255)

    class Meta:
        db_table = 'specialization_master'

    def __str__(self):
        return self.specialization_name


class DoctorSpecialization(models.Model):
    id = models.AutoField(primary_key=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, db_column='doctor_id', related_name='doctor_specialization')
    specialization = models.ForeignKey(SpecializationMaster, on_delete=models.CASCADE, db_column='specialization_id')

    class Meta:
        db_table = 'doctor_specialization'

    def __str__(self):
        return f"{self.doctor.doctor_name} - {self.specialization.specialization_name}"


class QualificationMaster(models.Model):
    qualification_id = models.AutoField(primary_key=True)
    qualification_name = models.CharField(max_length=255)

    class Meta:
        db_table = 'qualification_master'

    def __str__(self):
        return self.qualification_name


class DoctorQualification(models.Model):
    id = models.AutoField(primary_key=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, db_column='doctor_id', related_name='doctor_qualification')
    qualification = models.ForeignKey(QualificationMaster, on_delete=models.CASCADE, db_column='qualification_id')

    class Meta:
        db_table = 'doctor_qualification'

    def __str__(self):
        return f"{self.doctor.doctor_name} - {self.qualification.qualification_name}"


class DoctorClinic(models.Model):
    id = models.AutoField(primary_key=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, db_column='doctor_id', related_name='doctor_clinic')
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE, db_column='clinic_id')

    class Meta:
        db_table = 'doctor_clinic'

    def __str__(self):
        return f"{self.doctor.doctor_name} - {self.clinic.clinic_name}"


class DoctorAvailability(models.Model):
    availability_id = models.AutoField(primary_key=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, db_column='doctor_id')
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE, db_column='clinic_id')
    day = models.ForeignKey(DayMaster, on_delete=models.CASCADE, db_column='day_id')
    start_time = models.TimeField()
    end_time = models.TimeField()

    class Meta:
        db_table = 'doctor_availability'

    def __str__(self):
        return f"{self.doctor.doctor_name} - {self.day.day_name}"


class Review(models.Model):
    review_id = models.AutoField(primary_key=True)
    patient = models.ForeignKey('accounts.Patient', on_delete=models.CASCADE, db_column='patient_id')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, db_column='doctor_id')
    appointment = models.OneToOneField('appointments.Appointment', on_delete=models.CASCADE, db_column='appointment_id')
    rating = models.DecimalField(max_digits=2, decimal_places=1)
    review_text = models.CharField(max_length=500, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'reviews'

    def __str__(self):
        return f"Review by {self.patient.user.full_name} for {self.doctor.doctor_name}"
