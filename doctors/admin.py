from django.contrib import admin
from .models import Doctor, DoctorAvailability, Review

admin.site.register(Doctor)
admin.site.register(DoctorAvailability)
admin.site.register(Review)
