from django.urls import path
from . import views


urlpatterns = [
    path("", views.home, name="home"),
    path("login/", views.login_view, name="login"),
    path("register/", views.register, name="register"),
    path("register/patient/", views.register_patient, name="register_patient"),
    path("register/doctor/", views.register_doctor, name="register_doctor"),
    path("register/clinic/", views.register_clinic, name="register_clinic"),
    path("register/staff/", views.register_staff, name="register_staff"),
    path("logout/", views.logout_view, name="logout"),
    path("profile/", views.profile, name="profile"),

    path("dashboard/patient/", views.patient_dashboard, name="patient_dashboard"),
    path("dashboard/doctor/", views.doctor_dashboard, name="doctor_dashboard"),
    path("dashboard/clinic/", views.clinic_dashboard, name="clinic_dashboard"),
    path("dashboard/staff/", views.staff_dashboard, name="staff_dashboard"),
    path("dashboard/admin/", views.admin_dashboard, name="admin_dashboard"),

    path("verify-user/", views.verify_user, name="verify_user"),
    path("get-cities/", views.get_cities, name="get_cities"),
]
