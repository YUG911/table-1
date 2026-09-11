from django.contrib import admin
from .models import (
    Doctor, SpecializationMaster, DoctorSpecialization,
    QualificationMaster, DoctorQualification,
    DoctorClinic, DoctorAvailability, Review
)


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('doctor_id', 'user', 'doctor_name', 'experience', 'new_patient_fee', 'old_patient_fee')
    search_fields = ('doctor_name', 'user__full_name')


@admin.register(SpecializationMaster)
class SpecializationMasterAdmin(admin.ModelAdmin):
    list_display = ('specialization_id', 'specialization_name')
    search_fields = ('specialization_name',)


@admin.register(DoctorSpecialization)
class DoctorSpecializationAdmin(admin.ModelAdmin):
    list_display = ('id', 'doctor', 'specialization')
    list_filter = ('specialization',)


@admin.register(QualificationMaster)
class QualificationMasterAdmin(admin.ModelAdmin):
    list_display = ('qualification_id', 'qualification_name')
    search_fields = ('qualification_name',)


@admin.register(DoctorQualification)
class DoctorQualificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'doctor', 'qualification')


@admin.register(DoctorClinic)
class DoctorClinicAdmin(admin.ModelAdmin):
    list_display = ('id', 'doctor', 'clinic')


@admin.register(DoctorAvailability)
class DoctorAvailabilityAdmin(admin.ModelAdmin):
    list_display = ('availability_id', 'doctor', 'clinic', 'day', 'start_time', 'end_time')
    list_filter = ('day', 'clinic')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('review_id', 'patient', 'doctor', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
