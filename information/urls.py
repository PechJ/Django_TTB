from django.urls import path
from devices import views as device_views


urlpatterns = [
    path(
        "",
        device_views.dashboard,
        name="information-home",
    ),
]