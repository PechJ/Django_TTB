from django.contrib import admin
from django.urls import include, path
from devices import views as device_views
from administration import views as administration_views
from django.contrib.auth import views as auth_views
from core import views
from django.views.generic import RedirectView


urlpatterns = [
    
    path("admin/", admin.site.urls),
    
    path('', views.home, name='home'),
    
    # 1. Die Login-Seite (nutzt Djangos fertige View, wir übergeben nur unser Template)
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    
    # 2. Die Logout-Funktion
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    # 3. Die automatische Weiterleitung nach dem Login basierend auf der Rolle
    path('login-redirect/', views.login_redirect_view, name='login_redirect'),
    
    path("", include("core.urls")),
    
    path('register/', views.register_view, name='register'),
    
    path(
        "alarmierung/",
        device_views.alarmierung_home,
        name="alarmierung_home",
    ),
    
    
    path('administration/', include('administration.urls', namespace='administration')),    
    path("devices/", include("devices.urls")),
    path("funk/", include("funk.urls")),
    path("alarmierung/", include("alarmierung.urls")),
    path("information/", include("information.urls")),
]
