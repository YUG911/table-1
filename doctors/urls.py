from django.urls import path
from . import views


urlpatterns = [
    path("", views.doctor_list, name="doctor_list"),
    path("<int:doctor_id>/", views.doctor_detail, name="doctor_detail"),
    path("profile/", views.doctor_profile, name="doctor_profile"),
    path("availability/", views.doctor_availability, name="doctor_availability"),
    path("appointments/", views.doctor_appointments, name="doctor_appointments"),
    path("patients/", views.doctor_patients, name="doctor_patients"),
]
