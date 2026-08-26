from django.shortcuts import render, get_object_or_404, redirect
from .models import Appointment
from doctors.models import Doctor
from accounts.models import Patient


def book_appointment(request, doctor_id):

    doctor = get_object_or_404(Doctor, doctor_id=doctor_id)

    if request.method == "POST":

        appointment_date = request.POST.get("appointment_date")
        appointment_time = request.POST.get("appointment_time")
        symptoms = request.POST.get("symptoms")

        # Temporary: use Patient with ID 1
        patient = get_object_or_404(Patient, patient_id=1)

        Appointment.objects.create(
            patient=patient,
            doctor=doctor,
            appointment_date=appointment_date,
            appointment_time=appointment_time,
            symptoms=symptoms,
            status="Pending"
        )

        return redirect("/")

    return render(
        request,
        "appointments/book_appointment.html",
        {
            "doctor": doctor
        }
    )