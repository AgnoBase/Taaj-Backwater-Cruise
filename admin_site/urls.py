from django.urls import path
from .views import *
urlpatterns = [
    path('',admin_login, name= 'Admin-login'),
    path('logout/',admin_logout, name= 'Admin-logout'),
    path('dashboard/', admin_dashboard, name= 'Admin-dashboard'),
    path('reservation/', admin_reservations, name= 'Admin-reservation'),
    path('<int:userid>/profile/', admin_profile, name= 'Admin-profile'), 
    path('plan/create/',plan_create,name='plan-create'),  
    path('<int:userid>/plan/change/',plan_update,name='plan-update'), 
]   