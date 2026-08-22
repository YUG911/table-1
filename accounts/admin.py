from django.contrib import admin
from .models import User, Clinic, ClinicStaff, Patient

admin.site.register(User)
admin.site.register(Clinic)
admin.site.register(ClinicStaff)
admin.site.register(Patient)
