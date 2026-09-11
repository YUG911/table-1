<<<<<<< HEAD
from datetime import datetime, timedelta, time
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from accounts.context_processors import login_required, role_required, current_user
from .models import Appointment, Payment
from accounts.models import Patient, Clinic, User, Role
from doctors.models import Doctor, DoctorAvailability
from records.models import PatientRecord, Prescription, Report
from doctors.models import Review
from django.http import JsonResponse


@login_required
@role_required('patient')
def book_appointment(request, doctor_id):
    user = current_user(request)
    patient = get_object_or_404(Patient, user=user)
    doctor = get_object_or_404(Doctor, doctor_id=doctor_id)
    clinics = doctor.doctor_clinic_set.all().select_related('clinic')

    if request.method == 'POST':
        clinic_id = request.POST.get('clinic_id')
        appointment_date = request.POST.get('appointment_date')
        appointment_time = request.POST.get('appointment_time')
        symptoms = request.POST.get('symptoms', '')
        patient_type = request.POST.get('patient_type', 'New')

        clinic = get_object_or_404(Clinic, clinic_id=clinic_id) if clinic_id else clinics[0].clinic

        # Double-booking check
        if Appointment.objects.filter(
            doctor=doctor, appointment_date=appointment_date,
            appointment_time=appointment_time
        ).exists():
            messages.error(request, "This time slot is already booked. Please select another.")
            return redirect('book_appointment', doctor_id=doctor_id)

        fee = doctor.new_patient_fee if patient_type == 'New' else doctor.old_patient_fee

        appointment = Appointment.objects.create(
            patient=patient,
            doctor=doctor,
            clinic=clinic,
            appointment_date=appointment_date,
            appointment_time=appointment_time,
            symptoms=symptoms,
            status='Pending',
            patient_type=patient_type,
            fee_charged=fee
        )
        messages.success(request, f"Appointment #{appointment.appointment_id} booked successfully!")
        return redirect('my_appointments')

    # Get available slots
    today = datetime.now().date()
    next_14_days = [today + timedelta(days=i) for i in range(14)]
    availabilities = DoctorAvailability.objects.filter(doctor=doctor).select_related('day', 'clinic')

    # Build available dates/slots
    available_slots = {}
    for avail in availabilities:
        day_name = avail.day.day_name.lower()
        for d in next_14_days:
            if d.strftime('%A').lower() == day_name:
                date_str = d.strftime('%Y-%m-%d')
                if date_str not in available_slots:
                    available_slots[date_str] = {'date': d, 'slots': [], 'clinic': avail.clinic}

    # Remove already booked slots
    booked = Appointment.objects.filter(
        doctor=doctor, appointment_date__in=[s['date'] for s in available_slots.values()],
        status__in=['Pending', 'Confirmed']
    ).values_list('appointment_date', 'appointment_time')

    for date_str, data in available_slots.items():
        d = data['date']
        # Get availability for this date
        day_qs = availabilities.filter(day__day_name__iexact=d.strftime('%A'))
        if day_qs:
            avail_obj = day_qs.first()
            start_time = datetime.strptime(str(avail_obj.start_time), '%H:%M:%S').time()
            end_time = datetime.strptime(str(avail_obj.end_time), '%H:%M:%S').time()

            current = datetime.combine(d, start_time)
            end_dt = datetime.combine(d, end_time)
            interval = timedelta(minutes=30)
            while current < end_dt:
                slot_time = current.time().strftime('%H:%M')
                already_booked = any(
                    b[0] == d and b[1] == current.time().strftime('%H:%M:%S')[:5]
                    for b in booked
                )
                if not already_booked:
                    data['slots'].append(slot_time)
                current += interval

    # Filter out dates with no slots
    available_slots = {k: v for k, v in available_slots.items() if v['slots']}

    return render(request, 'appointments/book_appointment.html', {
        'doctor': doctor,
        'patient': patient,
        'clinics': clinics,
        'available_slots': available_slots,
    })


@login_required
@role_required('patient')
def my_appointments(request):
    user = current_user(request)
    patient = get_object_or_404(Patient, user=user)
    appointments = Appointment.objects.filter(patient=patient).order_by('-appointment_date')
    return render(request, 'appointments/my_appointments.html', {
        'patient': patient,
        'appointments': appointments,
    })


@login_required
@role_required('patient')
def reschedule_appointment(request, appointment_id):
    user = current_user(request)
    patient = get_object_or_404(Patient, user=user)
    appointment = get_object_or_404(
        Appointment, appointment_id=appointment_id, patient=patient,
        status__in=['Pending', 'Confirmed']
    )
    doctor = appointment.doctor

    if request.method == 'POST':
        new_date = request.POST.get('appointment_date')
        new_time = request.POST.get('appointment_time')

        if Appointment.objects.filter(
            doctor=doctor, appointment_date=new_date,
            appointment_time=new_time
        ).exclude(appointment_id=appointment_id).exists():
            messages.error(request, "This time slot is already booked.")
            return redirect('reschedule_appointment', appointment_id=appointment_id)

        appointment.appointment_date = new_date
        appointment.appointment_time = new_time
        appointment.save()
        messages.success(request, "Appointment rescheduled successfully.")
        return redirect('my_appointments')

    today = datetime.now().date()
    availabilities = DoctorAvailability.objects.filter(doctor=doctor).select_related('day', 'clinic')

    available_slots = {}
    for d_idx in range(14):
        d = today + timedelta(days=d_idx)
        day_name = d.strftime('%A').lower()
        day_qs = availabilities.filter(day__day_name__iexact=day_name)
        if day_qs:
            avail_obj = day_qs.first()
            date_str = d.strftime('%Y-%m-%d')
            start_time = datetime.strptime(str(avail_obj.start_time), '%H:%M:%S').time()
            end_time = datetime.strptime(str(avail_obj.end_time), '%H:%M:%S').time()

            current = datetime.combine(d, start_time)
            end_dt = datetime.combine(d, end_time)
            interval = timedelta(minutes=30)
            slots = []
            while current < end_dt:
                slot_time = current.time().strftime('%H:%M')
                already_booked = Appointment.objects.filter(
                    doctor=doctor, appointment_date=d,
                    appointment_time=current.time().strftime('%H:%M:%S')[:5]
                ).exclude(appointment_id=appointment_id).exists()
                if not already_booked:
                    slots.append(slot_time)
                current += interval
            if slots:
                available_slots[date_str] = {'date': d, 'slots': slots}

    return render(request, 'appointments/reschedule_appointment.html', {
        'appointment': appointment,
        'doctor': doctor,
        'available_slots': available_slots,
    })


@login_required
@role_required('patient')
def submit_review(request, appointment_id):
    user = current_user(request)
    patient = get_object_or_404(Patient, user=user)
    appointment = get_object_or_404(
        Appointment, appointment_id=appointment_id, patient=patient, status='Completed'
    )
    if Review.objects.filter(appointment=appointment).exists():
        messages.info(request, "You have already reviewed this appointment.")
        return redirect('my_appointments')

    if request.method == 'POST':
        rating = request.POST.get('rating')
        review_text = request.POST.get('review_text', '')
        Review.objects.create(
            patient=patient, doctor=appointment.doctor,
            appointment=appointment, rating=rating, review_text=review_text
        )
        messages.success(request, "Your review has been submitted.")
        return redirect('my_appointments')
    return render(request, 'appointments/submit_review.html', {
        'appointment': appointment, 'doctor': appointment.doctor,
    })
=======
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
>>>>>>> 539c770b174407ec5b36a395ada01de547974596
