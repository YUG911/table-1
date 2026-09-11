from django.urls import path
from . import views


urlpatterns = [
    path("records/", views.my_records, name="my_records"),
    path("prescriptions/", views.my_prescriptions, name="my_prescriptions"),
    path("reports/", views.my_reports, name="my_reports"),
    path("upload-report/<int:appointment_id>/", views.upload_report, name="staff_upload_report"),
    path("add-record/<int:appointment_id>/", views.add_record, name="add_record"),
    path("upload-prescription/<int:appointment_id>/", views.upload_prescription, name="upload_prescription"),
]
