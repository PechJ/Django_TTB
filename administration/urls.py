from django.urls import path

from . import views

app_name = 'administration'

urlpatterns = [
    path('', views.administration, name='administration'),
    path('funk/', views.administration_funk, name='administration-funk'),
    path('pager/', views.administration_pager, name='administration-pager'),
]