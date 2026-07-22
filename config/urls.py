from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("", include("core.urls")),

    path("devices/", include("devices.urls")),
    path("funk/", include("funk.urls")),
    path("information/", include("information.urls")),

    path("admin/", admin.site.urls),
]