<<<<<<< HEAD
from django.conf import settings
from django.conf.urls.static import static
=======
>>>>>>> 539c770b174407ec5b36a395ada01de547974596
from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path(
        "admin/",
        admin.site.urls
    ),

    path(
        "",
        include("accounts.urls")
    ),

    path(
        "doctors/",
        include("doctors.urls")
    ),

    path(
        "appointments/",
        include("appointments.urls")
    ),
<<<<<<< HEAD

    path(
        "records/",
        include("records.urls")
    ),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
=======
]
>>>>>>> 539c770b174407ec5b36a395ada01de547974596
