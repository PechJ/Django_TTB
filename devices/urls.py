from django.urls import path

from . import views


app_name = "devices"


urlpatterns = [
    path(
        "",
        views.device_list,
        name="device_list",
    ),

    path(
        "import/radio/",
        views.manufacturer_radio_import,
        name="manufacturer_radio_import",
    ),
    
    path(
        "import/",
        views.import_view,
        name="import",
    ),
]