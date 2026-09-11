from django.urls import path
from . import views

<<<<<<< HEAD

urlpatterns = [
    path("book/<int:doctor_id>/", views.book_appointment, name="book_appointment"),
    path("my-appointments/", views.my_appointments, name="my_appointments"),
    path("reschedule/<int:appointment_id>/", views.reschedule_appointment, name="reschedule_appointment"),
    path("review/<int:appointment_id>/", views.submit_review, name="submit_review"),
]
=======
urlpatterns = [
    path(
        "book/<int:doctor_id>/",
        views.book_appointment,
        name="book_appointment"
    ),
]
>>>>>>> 539c770b174407ec5b36a395ada01de547974596
