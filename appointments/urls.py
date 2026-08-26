from django.urls import path
from . import views

urlpatterns = [
    path(
        "book/<int:doctor_id>/",
        views.book_appointment,
        name="book_appointment"
    ),
]