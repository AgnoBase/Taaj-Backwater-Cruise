from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login
from booking.models import Booking,Plans
from .forms import AdminProfile
from django.contrib.auth import logout
from django.contrib.auth.decorators import user_passes_test
# Create your views here.


def admin_login(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(request=request,data = request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            match = User.objects.get(username=username)
            if match is not None:
                if match.is_superuser==True:
                    print('admin',match)
                    user = authenticate(username=username, password=password)
                    print(user)
                    if user:
                        login(request, user)
                        return redirect('../../admin_area/dashboard')
            else:
                print('invalid credentials')
    return render(request,'admin_area/login.html',{'form':form})




@user_passes_test(lambda u: u.is_superuser,
                  login_url='../../admin_area/login')
def admin_logout(request):
    logout(request)
    return redirect('../../admin_area/login')



@user_passes_test(lambda u: u.is_superuser,
                  login_url='../../admin_area/login')
def admin_dashboard(request):
    no_of_bookings = []
    name = []
    total_plans = Plans.objects.all()
    total = list(total_plans)
    
    for i in total:
        print(i.name)
        name.append(i.name)
    for i in total :
        no_of_booked_plans = Booking.objects.filter(plan_id = i.id).count()
        no_of_bookings.append(no_of_booked_plans)
        
    print(name)
    return render(request, 'admin_area/admin_dashboard.html', 
                  {'title':'Admin|Dashboard', 
                   'plans': total_plans , 
                   'no_of_bookings': no_of_bookings,
                   'name':name})



@user_passes_test(lambda u: u.is_superuser,
                  login_url='../../admin_area/login')
def admin_reservations (request):
    reservations = Booking.objects.all()
    return render(request, 'admin_area/admin_reservation.html', 
                  {'reservations' : reservations, 'title' : 'Admin|Reservations'}) 



@user_passes_test(lambda u: u.is_superuser,
                  login_url='../../../admin_area/')
def admin_profile(request,userid):
    form = AdminProfile(instance=request.user)
    user = User.objects.get(id=userid)
    if request.method == 'POST':
        new_email = request.POST.get('nemail')
        request.session['new_email'] = new_email
        user_email = user.email
        if user_email != new_email:
            user.email = new_email
            user.save()
            return render(request, 'admin_area/admin_profile.html', {'form' : form , 'success_message' : 'Done !!! Your email is changed have a good day :)'})
    return render(request, 'admin_area/admin_profile.html', {'form' : form})


@user_passes_test(lambda u: u.is_superuser,
                  login_url='../../admin_area/')
def admin_password_verify(request):
    return render(request,'admin_area/admin_password_verify.html')


@user_passes_test(lambda u: u.is_superuser,
                  login_url='../../admin_area/')
def plan_create (request):
    if request.method == 'POST':
        name        =   request.POST.get('pname')
        description =   request.POST.get('description')
        Duration    =   request.POST.get('duration')
        price       =   request.POST.get('price')
        new_plan    =   Plans.objects.create(    name=name,  
                                                 description=description, 
                                                 Duration=Duration, 
                                                 price=price)
        return redirect('../../../admin_area/dashboard')
    return render(request,'admin_area/admin_plan_create.html')


@user_passes_test(lambda u: u.is_superuser,
                  login_url='../../../admin_area/')
def plan_update(request,userid):
    plan = get_object_or_404(Plans,id=userid)
    if request.method == 'POST':
        plan.name        =   request.POST.get('pname')
        plan.description =   request.POST.get('description')
        plan.Duration    =   request.POST.get('duration')
        plan.price       =   request.POST.get('price')
        plan.save()
        return redirect('../../../../admin_area/dashboard')
    elif request.method == 'GET':
        return render(request,'admin_area/plan_update.html',{'plan':plan})
