from django.contrib import admin
from django.urls import path,include
from . import views
urlpatterns = [
    path('create/form/<int:id>',views.booking_form,name='booking-form'),
    path('verify/',views.verify_email,name='email-verify'),
    path('services',views.services_page,name='service-page'),
    path('info/page',views.info_page,name='info-page'),
]
