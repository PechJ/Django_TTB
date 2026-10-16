from django.urls import path

from . import views

app_name = 'administration'

urlpatterns = [
    path('', views.administration, name='administration'),
    path('funk/', views.administration_funk, name='administration-funk'),
    path('pager/', views.administration_pager, name='administration-pager'),
    path('user/', views.administration_user, name='administration-user'),
    path('funk/<int:pk>/', views.admin_funk_detail, name='admin_funk_detail'),
    path('funk/update/<int:pk>/', views.update_device_field, name='update_device_field'),
    path('import/', views.administration_import, name='administration-import'),
]