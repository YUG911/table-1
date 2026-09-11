from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from accounts.context_processors import login_required, role_required, current_user
from .models import PatientRecord, Prescription, Report
from appointments.models import Appointment
from accounts.models import Patient
from doctors.models import Doctor


@login_required
@role_required('doctor')
def add_record(request, appointment_id):
    user = current_user(request)
    doctor = get_object_or_404(Doctor, user=user)
    appointment = get_object_or_404(Appointment, appointment_id=appointment_id, doctor=doctor)
    patient = appointment.patient

    if request.method == 'POST':
        diagnosis = request.POST.get('diagnosis', '')
        notes = request.POST.get('notes', '')
        PatientRecord.objects.create(
            patient=patient, doctor=doctor, appointment=appointment,
            diagnosis=diagnosis, notes=notes
        )
        appointment.status = 'Completed'
        appointment.save()
        Prescription.objects.create(
            appointment=appointment, uploaded_by=user, file_path=''
        ) if not Prescription.objects.filter(appointment=appointment).exists() else None
        messages.success(request, "Record added. Appointment marked as Completed.")
        return redirect('doctor_appointments')

    record_exists = PatientRecord.objects.filter(appointment=appointment).exists()
    existing_record = None
    if record_exists:
        existing_record = PatientRecord.objects.get(appointment=appointment)
    return render(request, 'records/add_record.html', {
        'doctor': doctor, 'appointment': appointment,
        'patient': patient, 'record_exists': record_exists,
        'record': existing_record,
    })


@login_required
@role_required('doctor')
def upload_prescription(request, appointment_id):
    user = current_user(request)
    doctor = get_object_or_404(Doctor, user=user)
    appointment = get_object_or_404(Appointment, appointment_id=appointment_id, doctor=doctor)

    if request.method == 'POST':
        file_path = request.FILES.get('file')
        if file_path:
            Prescription.objects.update_or_create(
                appointment=appointment, defaults={'uploaded_by': user, 'file_path': file_path.name}
            )
            if file_path:
                from django.core.files.storage import default_storage
                default_storage.save(f'prescriptions/{file_path.name}', file_path)
            messages.success(request, "Prescription uploaded.")
            return redirect('doctor_appointments')
        messages.error(request, "No file selected.")
    return render(request, 'records/upload_prescription.html', {
        'doctor': doctor, 'appointment': appointment,
    })


@login_required
@role_required('patient')
def my_records(request):
    user = current_user(request)
    patient = get_object_or_404(Patient, user=user)
    records = PatientRecord.objects.filter(patient=patient)
    return render(request, 'records/my_records.html', {'patient': patient, 'records': records})


@login_required
@role_required('patient')
def my_prescriptions(request):
    user = current_user(request)
    patient = get_object_or_404(Patient, user=user)
    prescriptions = Prescription.objects.filter(appointment__patient=patient)
    return render(request, 'records/my_prescriptions.html', {'patient': patient, 'prescriptions': prescriptions})


@login_required
@role_required('patient')
def my_reports(request):
    user = current_user(request)
    patient = get_object_or_404(Patient, user=user)
    reports = Report.objects.filter(appointment__patient=patient)
    return render(request, 'records/my_reports.html', {'patient': patient, 'reports': reports})


@login_required
@role_required('clinic staff')
def upload_report(request, appointment_id):
    user = current_user(request)
    appointment = get_object_or_404(Appointment, appointment_id=appointment_id)
    if request.method == 'POST':
        report_name = request.POST.get('report_name', '')
        file_path = request.FILES.get('file')
        if file_path:
            from django.core.files.storage import default_storage
            saved_path = default_storage.save(f'reports/{file_path.name}', file_path)
            Report.objects.create(
                appointment=appointment, uploaded_by=user,
                report_name=report_name, file_path=saved_path
            )
            messages.success(request, "Report uploaded successfully.")
            return redirect('staff_dashboard')
        messages.error(request, "No file selected.")
    return render(request, 'records/upload_report.html', {'appointment': appointment})
