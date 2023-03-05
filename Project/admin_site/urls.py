from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_view
from .views import admin_login, admin_dashboard, admin_reservations,admin_profile,admin_verify,PasswordChange,admin_password_verify
urlpatterns = [
    path('login/',admin_login, name= 'Admin-login'),
    path('dashboard/', admin_dashboard, name= 'Admin-dashboard'),
    path('reservation/', admin_reservations, name= 'Admin-reservation'),
    path('<int:userid>/profile/', admin_profile, name= 'Admin-profile'),
    path('<int:userid>/verify/',admin_verify,name='Admin-verify'),
    path('<int:userid>/new/pass',PasswordChange.as_view(),name='Admin-verify'),
    path('verify/',admin_password_verify,name='Admin-Password-verify')
    
]