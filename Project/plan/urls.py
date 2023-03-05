from django.contrib import admin
from django.urls import path
from .views import plan_create,plan_update,Plan_delete
urlpatterns = [
    path('create/',plan_create,name='plan-create'),
    path('<int:id>/change/',plan_update,name='plan-update'),
    path('<planid>/delete/', Plan_delete.as_view(), name= 'plan-delete')
]