from django.shortcuts import render,redirect,get_object_or_404
from django.views.generic import DeleteView
from .forms import PlanForm
from booking.models import Plans
from django.contrib.admin.views.decorators import staff_member_required
# Create your views here.

@staff_member_required
def plan_create (request):
    print(request.POST)
    form = PlanForm()
    print(form)
    if request.method == 'POST':
        form = PlanForm(request.POST)
        if form.is_valid():
            name        =   form.cleaned_data.get('name')
            boat_name   =   form.cleaned_data.get('boat_name')
            description =   form.cleaned_data.get('description')
            Duration    =   form.cleaned_data.get('Duration')
            price       =   form.cleaned_data.get('price')
            new_plan    =   Plans.objects.create(name=name, 
                                                 boat_name=boat_name, 
                                                 description=description, 
                                                 Duration=Duration, 
                                                 price=price)
            return redirect('../../admin-area/dashboard')
    return render(request,'plan/admin_plan_create.html',{'form':form})


@staff_member_required
def plan_update(request,id):
    plan = get_object_or_404(Plans,id=id)
    form = PlanForm(instance=plan)
    if request.method == 'POST':
        form = PlanForm(request.POST, instance = plan)
        if form.is_valid():            
            form.save()
            return redirect('../../../admin-area/dashboard')
    return render(request,'plan/plan_update.html',{'form':form})

# @staff_member_require
class Plan_delete(DeleteView):
    model = Plans
    # template_name = 'admin-area/admin_plan_delete.html'
    success_url = '/'