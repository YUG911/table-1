from django.contrib import admin
from .models import PatientRecord, Prescription, Report

admin.site.register(PatientRecord)
admin.site.register(Prescription)
admin.site.register(Report)
