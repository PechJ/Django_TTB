from django.contrib import admin
from django.urls import include, path
from devices import views as device_views


urlpatterns = [
    path("", include("core.urls")),
    
    path(
        "alarmierung/",
        device_views.alarmierung_home,
        name="alarmierung_home",
    ),

    path("devices/", include("devices.urls")),
    path("funk/", include("funk.urls")),
    path("alarmierung/", include("devices.urls")),
    path("information/", include("information.urls")),

    path("admin/", admin.site.urls),
]