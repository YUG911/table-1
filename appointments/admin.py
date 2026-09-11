from django.contrib import admin
from .models import Appointment, Payment


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('appointment_id', 'patient', 'doctor', 'clinic', 'appointment_date', 'appointment_time', 'status', 'patient_type', 'fee_charged')
    list_filter = ('status', 'appointment_date', 'clinic')
    search_fields = ('patient__user__full_name', 'doctor__doctor_name')


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('payment_id', 'appointment', 'amount', 'payment_method', 'payment_status', 'paid_at')
    list_filter = ('payment_status', 'payment_method')
