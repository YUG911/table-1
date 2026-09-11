from django.contrib import admin
from .models import PatientRecord, Prescription, Report


@admin.register(PatientRecord)
class PatientRecordAdmin(admin.ModelAdmin):
    list_display = ('record_id', 'patient', 'doctor', 'appointment', 'created_date')
    list_filter = ('doctor',)
    search_fields = ('patient__user__full_name', 'doctor__doctor_name')

    def created_date(self, obj):
        if obj.appointment:
            return obj.appointment.appointment_date
        return "-"
    created_date.short_description = "Appointment Date"


@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ('prescription_id', 'appointment', 'uploaded_by', 'created_at')
    list_filter = ('created_at',)


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('report_id', 'report_name', 'appointment', 'uploaded_by', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('report_name',)
