from django.urls import path
from . import views
from django.views.generic import TemplateView
urlpatterns = [
    # path('',views.home_page, name="Home-Page"),
    path('', TemplateView.as_view(template_name="root/index.html"), name='Home-Page'),
    path('gallery', TemplateView.as_view(template_name="root/gallery.html"), name='Gallery'),
    path('faq/learnmore', TemplateView.as_view(template_name="root/faqmobile.html"), name='Faq-learnmore'),
    
]