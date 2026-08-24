from django.urls import path
from . import views


urlpatterns = [

    path(
        "",
        views.doctor_list,
        name="doctor_list"
    ),

    path(
        "<int:doctor_id>/",
        views.doctor_detail,
        name="doctor_detail"
    ),

]