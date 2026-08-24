from django.shortcuts import render, get_object_or_404
from .models import Doctor


def doctor_list(request):
    doctors = Doctor.objects.all()

    return render(
        request,
        "doctors/doctors.html",
        {
            "doctors": doctors
        }
    )


def doctor_detail(request, doctor_id):
    doctor = get_object_or_404(
        Doctor,
        doctor_id=doctor_id
    )

    return render(
        request,
        "doctors/doctor-detail.html",
        {
            "doctor": doctor
        }
    )