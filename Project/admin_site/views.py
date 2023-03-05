from django.shortcuts import render,redirect
from django.conf import settings
import random
from django.urls import reverse
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib.auth.forms import AuthenticationForm,PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login
from booking.models import Booking,Plans
from .forms import AdminProfile
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy

def otp():
    return str(random.randint(1000,9999))

global number
number = otp()
# Create your views here.

def admin_login(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(request=request,data = request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            print(username,password)
            match = User.objects.get(username=username)
            if match is not None:
                if match.is_superuser==True:
                    print('admin',match)
                    user = authenticate(username=username, password=password)
                    print(user)
                    if user:
                        login(request, user)
                        return redirect("/")
            else:
                print('invalid credentials')
    return render(request,'admin_area/login.html',{'form':form})


def admin_dashboard(request):
    no_of_bookings = []
    total_plans = Plans.objects.all()
    print(total_plans)
    total_ = list(total_plans)
    print(total_)
    for i in total_ :
        no_of_booked_plans = Booking.objects.filter(plan_id = i.id).count()
        no_of_bookings.append(no_of_booked_plans)
        print('\n \n \n \n')
        print(i, no_of_booked_plans)

    print(no_of_bookings)

    return render(request, 'admin_area/admin_dashboard.html', 
                  {'title':'Admin|Dashboard', 
                   'plans': total_plans , 
                   'no_of_bookings': no_of_bookings})

def admin_reservations (request):
    reservations = Booking.objects.all()
    return render(request, 'admin_area/admin_reservation.html', 
                  {'reservations' : reservations}) 

def admin_profile(request,userid):
    form = AdminProfile(instance=request.user)
    user = User.objects.get(id=userid)
    if request.method == 'POST':
        new_email = request.POST.get('nemail')
        request.session['new_email'] = new_email
        print(new_email)
        user_email = user.email
        if user_email != new_email:
            # user.email = new_email
            html_content = render_to_string('admin_area/emails_template.html',{'code':number})
            # converting html content to string so that it can be used in e-mail
            text_content = strip_tags(html_content)
            e = EmailMultiAlternatives(
                            'Admin Email Verification',# subject
                            text_content,# content
                            settings.EMAIL_HOST_USER,# host e-mail
                            [new_email],# resipient e-mail
                    )
            # defining subject content host e-mail and list of resipient 
            e.attach_alternative(html_content,'text/html')
            e.send()
            return HttpResponseRedirect(reverse('pet_detail',args=[str(userid)]))
    return render(request, 'admin_area/admin_profile.html', {'form' : form})

def admin_verify(request,userid):
    new_email = request.session['new_email']
    print('email by user' ,new_email)
    user = User.objects.get(id=userid)
    user_email = user.email
    if request.POST :
        code = request.POST.get('vcode')
        if code == number:
            if user_email != new_email:
                user.email=new_email
                user.save()
            return redirect('/admin-area/dashboard')
    return render(request,'admin_area/admin_verify.html')

class PasswordChange(PasswordChangeView):
    form_class = PasswordChangeForm
    template_name = 'admin_area/admin_new_password.html'
    success_url = reverse_lazy('Admin-Password-verify')

def admin_password_verify(request):
    return render(request,'admin_area/admin_password_verify.html')