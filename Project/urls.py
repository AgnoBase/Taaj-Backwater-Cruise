from django.contrib import admin
from django.urls import path,include
urlpatterns = [
    path('admin/', admin.site.urls),
    path('booking/',include('booking.urls')),
    path('',include('root.urls')),
    path('admin_area/',include('admin_site.urls')),
    path('plan/',include('plan.urls')) 
]
