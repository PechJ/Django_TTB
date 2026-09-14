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
        "pager/", 
        views.pager_list, 
        name="pager_list"
    ),

    path(
        "pager/<int:device_id>/",
        views.pager_detail,
        name="pager_detail",
    ),
    
    path(
        "pager/<int:device_id>/reparatur/",
        views.pager_reparatur_start,
        name="pager_reparatur_start",
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
    
    path(
        "pager/reparatur/<int:reparatur_id>/rueckkehr/",
        views.pager_reparatur_rueckkehr,
        name="pager_reparatur_rueckkehr",
    ),
    
    path(
        "pager/reparatur/[int:reparatur_id](int:reparatur_id)/rueckkehr/",
        views.pager_reparatur_rueckkehr,
        name="pager_reparatur_rueckkehr",
    ),

    path(
        "pager/<int:device_id>/historie/",
        views.pager_historie,
        name="pager_historie",
    ),
]