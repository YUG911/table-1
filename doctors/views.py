from datetime import date
from django.db.models import Q
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from accounts.context_processors import login_required, role_required, current_user
from .models import Doctor, DoctorAvailability, Review
from accounts.models import Patient, Clinic, DayMaster
from appointments.models import Appointment


def doctor_list(request):
    search = request.GET.get('search', '')
    specialization = request.GET.get('specialization', '')
    location = request.GET.get('location', '')

    doctors = Doctor.objects.all()
    if search:
        doctors = doctors.filter(
            Q(doctor_name__icontains=search) |
            Q(doctor_specialization__specialization__specialization_name__icontains=search)
        ).distinct()
    if specialization:
        doctors = doctors.filter(
            doctor_specialization__specialization__specialization_name__icontains=specialization
        ).distinct()
    if location:
        doctors = doctors.filter(
            doctor_clinic__clinic__city__city_name__icontains=location
        ).distinct()

    from doctors.models import SpecializationMaster
    specializations = SpecializationMaster.objects.all()
    cities = Clinic.objects.values_list('city__city_name', flat=True).distinct()

    return render(request, 'doctors/doctor_list.html', {
        'doctors': doctors,
        'specializations': specializations,
        'cities': cities,
    })


def doctor_detail(request, doctor_id):
    doctor = get_object_or_404(Doctor, doctor_id=doctor_id)
    specializations = doctor.doctor_specialization.all().select_related('specialization')
    qualifications = doctor.doctor_qualification.all().select_related('qualification')
    clinic_links = doctor.doctor_clinic.all().select_related('clinic')
    clinics = [cl.clinic for cl in clinic_links]
    availabilities = DoctorAvailability.objects.filter(doctor=doctor).select_related('day', 'clinic')

    reviews = Review.objects.filter(doctor=doctor).order_by('-created_at')[:5]
    avg_rating = 0
    if reviews:
        avg_rating = sum(float(r.rating) for r in reviews) / len(reviews)

    return render(request, 'doctors/doctor_detail.html', {
        'doctor': doctor,
        'specializations': specializations,
        'qualifications': qualifications,
        'clinics': clinics,
        'availabilities': availabilities,
        'reviews': reviews,
        'avg_rating': round(avg_rating, 1),
    })


@login_required
@role_required('doctor')
def doctor_profile(request):
    user = current_user(request)
    doctor = get_object_or_404(Doctor, user=user)
    from doctors.models import DoctorSpecialization, DoctorQualification, DoctorClinic
    specializations = DoctorSpecialization.objects.filter(doctor=doctor).select_related('specialization')
    qualifications = DoctorQualification.objects.filter(doctor=doctor).select_related('qualification')
    clinics = DoctorClinic.objects.filter(doctor=doctor).select_related('clinic')
    return render(request, 'doctors/doctor_profile.html', {
        'doctor': doctor,
        'specializations': specializations,
        'qualifications': qualifications,
        'clinics': clinics,
    })


@login_required
@role_required('doctor')
def doctor_availability(request):
    user = current_user(request)
    doctor = get_object_or_404(Doctor, user=user)
    days = DayMaster.objects.all().order_by('day_id')
    clinics = Clinic.objects.filter(doctor_clinic__doctor=doctor)

    if request.method == 'POST':
        DoctorAvailability.objects.filter(doctor=doctor).delete()
        for day in days:
            day_id = day.day_id
            start = request.POST.get(f'start_{day_id}')
            end = request.POST.get(f'end_{day_id}')
            clinic_ids = request.POST.getlist(f'clinics_{day_id}')
            if start and end and clinic_ids:
                for clinic_id in clinic_ids:
                    clinic = get_object_or_404(Clinic, clinic_id=clinic_id)
                    DoctorAvailability.objects.create(
                        doctor=doctor, clinic=clinic, day=day,
                        start_time=start, end_time=end
                    )
        messages.success(request, "Availability updated successfully.")
        return redirect('doctor_availability')

    existing = DoctorAvailability.objects.filter(doctor=doctor).select_related('day', 'clinic')
    return render(request, 'doctors/doctor_availability.html', {
        'doctor': doctor,
        'days': days,
        'clinics': clinics,
        'existing_availability': existing,
    })


@login_required
@role_required('doctor')
def doctor_appointments(request):
    user = current_user(request)
    doctor = get_object_or_404(Doctor, user=user)
    status_filter = request.GET.get('status', '')
    appointments = Appointment.objects.filter(doctor=doctor).order_by('-appointment_date')
    if status_filter:
        appointments = appointments.filter(status=status_filter)
    return render(request, 'doctors/doctor_appointments.html', {
        'doctor': doctor,
        'appointments': appointments,
    })


@login_required
@role_required('doctor')
def doctor_patients(request):
    user = current_user(request)
    doctor = get_object_or_404(Doctor, user=user)
    patients = Patient.objects.filter(
        appointment__doctor=doctor
    ).distinct()
    return render(request, 'doctors/doctor_patients.html', {
        'doctor': doctor,
        'patients': patients,
    })
