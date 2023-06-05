from django.urls import path
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    path('create/form/<int:id>',views.booking_form,name='booking-form'),
    path('services',views.services_page,name='service-page'),
    path('gallery', TemplateView.as_view(template_name="booking/gallery.html"), name='Gallery'),
    path('payment/<fname>/<mname>/<lname>/<email>/<cnum>/<duration>/<date>/<time>/<adult>/<child>/<plan_id>',views.payment,name='Payment'),
    path('success/<fname>/<mname>/<lname>/<email>/<cnum>/<duration>/<date>/<time>/<adult>/<child>/<plan_id>',views.success,name = 'success')
]
