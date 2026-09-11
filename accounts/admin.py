from django.contrib import admin
from .models import (
    Role, User, StateMaster, CityMaster,
    Clinic, DayMaster, ClinicHours, Patient,
    ClinicStaff, Admin as AdminModel, VerificationLog
)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'full_name', 'email', 'phone', 'role', 'is_verified', 'account_status')
    list_filter = ('role', 'is_verified', 'account_status')
    search_fields = ('full_name', 'email', 'phone')


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('role_id', 'role_name')


@admin.register(StateMaster)
class StateMasterAdmin(admin.ModelAdmin):
    list_display = ('state_id', 'state_name')
    search_fields = ('state_name',)


@admin.register(CityMaster)
class CityMasterAdmin(admin.ModelAdmin):
    list_display = ('city_id', 'city_name', 'state')
    list_filter = ('state',)
    search_fields = ('city_name',)


@admin.register(Clinic)
class ClinicAdmin(admin.ModelAdmin):
    list_display = ('clinic_id', 'clinic_name', 'user', 'city', 'contact_number')
    search_fields = ('clinic_name', 'contact_number')


@admin.register(DayMaster)
class DayMasterAdmin(admin.ModelAdmin):
    list_display = ('day_id', 'day_name')


@admin.register(ClinicHours)
class ClinicHoursAdmin(admin.ModelAdmin):
    list_display = ('hours_id', 'clinic', 'day', 'open_time', 'close_time')


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('patient_id', 'user', 'date_of_birth', 'gender', 'blood_group')
    search_fields = ('user__full_name', 'user__email')


@admin.register(ClinicStaff)
class ClinicStaffAdmin(admin.ModelAdmin):
    list_display = ('staff_id', 'user', 'clinic')


@admin.register(AdminModel)
class AdminModelAdmin(admin.ModelAdmin):
    list_display = ('admin_id', 'user', 'access_level')


@admin.register(VerificationLog)
class VerificationLogAdmin(admin.ModelAdmin):
    list_display = ('verification_id', 'user', 'admin', 'status', 'verified_at')
    list_filter = ('status', 'verified_at')
