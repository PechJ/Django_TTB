from django.urls import path

from . import views

urlpatterns = [

    path("", views.home, name="alarmierung-home"),
    path("sirenen/", views.sirenen, name="alarmierung-sirenen"),

]