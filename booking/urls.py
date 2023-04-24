from django.urls import path
from . import views
from django.views.generic import TemplateView
urlpatterns = [
    path('create/form/<int:id>',views.booking_form,name='booking-form'),
    path('services',views.services_page,name='service-page'),
    path('gallery', TemplateView.as_view(template_name="booking/gallery.html"), name='Gallery')
]
