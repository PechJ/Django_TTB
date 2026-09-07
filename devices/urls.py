from django.urls import path

from . import views


app_name = "devices"


urlpatterns = [
    path("", views.funk_home, name="funk_home"),

    path(
        "list/",
        views.device_list,
        name="device_list",
    ),

    path(
        "import/",
        views.import_view,
        name="import",
    ),

    path(
        "manufacturer/",
        views.manufacturer_import_view,
        name="manufacturer_import",
    ),
    
    path(
        "pager-import/",
        views.pager_import_view,
        name="pager_import",
    ),
    
    path(
        "programming/",
        views.programming_list,
        name="programming_list",
        ),
    
    path(
        "programming/<int:device_id>/complete/",
        views.programming_complete,
        name="programming_complete",
    ),
]