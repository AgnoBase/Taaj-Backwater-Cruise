from django.shortcuts import render 
from django.views.generic import DeleteView
from booking.models import Plans

# Create your views here.


# @staff_member_require
class Plan_delete(DeleteView):
    model = Plans
    # template_name = 'admin-area/admin_plan_delete.html'
    success_url = '/'