from django.contrib import admin
from django.urls import path
from .views import Plan_delete
urlpatterns = [
    
    path('<planid>/delete/', Plan_delete.as_view(), name= 'plan-delete')
]