
from django.shortcuts import render,redirect
from .forms import BookingForm
from django.conf import settings
import re,random,uuid
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .models import *
from plan.models import *
from django.http import HttpResponse,Http404

'''utilities for views'''

def phone_validate(num):
    '''
This function is:
    ->  returning True if number is verified 
    ->  if number is not corrrect then it will return false
'''
    try:
        # getting number from booking view and coverting it to string and matching it with Pattern
        get_num = str(num)
        Pattern = re.compile("[6-9][0-9]{9}")
        if (Pattern.match(get_num)):   
            return True
        return False
    except:
        return False

# Create your views here.

def booking_form(request,id):
    '''
This function is performing following things:
    ->  It generates form for booking for each plans
    ->  Getting data from forms(Emailform,Bookingform)
    ->  checking for there validity
    ->  cheking phone validation using function phone_validate
    ->  checking E-mail for validation using uuid
    ->  creating sessions for data retrieved from forms
    ->  it returns booking_form.html template
'''
    print(request.POST)
    # _plan holds information for plan selected from services page 
    _plan = Plans.objects.get(id=id)
    form = BookingForm(request.POST,id)
    if request.method == 'POST':
        print('method-post')
        if form.is_valid():
            #getting data from forms 
            email = form.cleaned_data['email']
            first_name = form.cleaned_data['fname']
            middle_name =form.cleaned_data['mname']
            last_name = form.cleaned_data['lname']
            contact_num = form.cleaned_data['cnum']
            date_book = form.cleaned_data['arrivedate']
            date = str(date_book)
            time_book = form.cleaned_data['time']
            time = str(time_book)
            adult = form.cleaned_data['adults']
            child =form.cleaned_data['child']
            btn = request.POST.get('book_btn')
                # printing data from form
            # print(f'{first_name}\n{middle_name}\n{last_name}\n{contact_num}\n{time}\n{adult}\n{child}\n{email}')
                # validating phone from above given function 
                
            try:
                if btn:
                    new_book = Booking.objects.create(plan = _plan,fname = first_name,mname = middle_name,lname=last_name,email = email,cnum = contact_num,arrivedate= date,time =time)
                    
                    html_content = render_to_string('booking/emails_template.html',{'price':new_book.plan.price1,'plan':new_book.plan.name,'fname':new_book.fname,'mname':new_book.mname,'lname':new_book.lname,'email':new_book.email,'contact':new_book.cnum,'date':date,'time':time})
                                                    
                    # converting html content to string so that it can be used in e-mail
                    text_content = strip_tags(html_content)
                    e = EmailMultiAlternatives(
                                    'Taaj Backwater Cruise Booking confirmation',# subject
                                    text_content,# content
                                    settings.EMAIL_HOST_USER,# host e-mail
                                    [email],# resipient e-mail
                                )
                                # defining subject content host e-mail and list of resipient 
                    e.attach_alternative(html_content,'text/html')
                    e.send()
                    return render(request,'booking/booking_form.html',{'form':form,'plan':_plan,'success_message':'email is sent to you with the pass please check !!!!'})
            except Exception as e:
                print(e)
            
    return render(request,'booking/booking_form.html',{'form':form,'plan':_plan})





def services_page(request):
    '''
This function performs following :
->  all the plans in the database 
->  so that user can select a plan 
'''
    try:
        plans = Plans.objects.all()
        print(plans)
        return render(request,'booking/services.html',{'Plans':plans})
    except Exception as e:
        print(e)
        raise Http404 
    
