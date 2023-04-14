from django.shortcuts import render,redirect
from .forms import BookingForm,Emailform
from django.conf import settings
import re,random,uuid
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .models import *
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
    global is_verified
    is_verified = False
    number = 0
    email=''
    print(request.POST)
    try:
        # _plan holds information for plan selected from services page 
        _plan = Plans.objects.get(id=id)
        try:
            email_form = Emailform(request.POST)
            form = BookingForm(request.POST,id)
            if email_form.is_valid():
                # getting data from email form about email
                email = request.POST['email']
                
            if request.method == 'POST' and form.is_valid():
                #getting data from forms 
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
                # printing data from form
                print(f'{first_name}\n{middle_name}\n{last_name}\n{contact_num}\n{time}\n{adult}\n{child}')
                # validating phone from above given function 
                if phone_validate(contact_num):
                    # checking whether email is given or not
                    if email != '':
                        print(email)
                        html_content = render_to_string('booking/emails_template.html',{'code':number})
                        # converting html content to string so that it can be used in e-mail
                        text_content = strip_tags(html_content)
                        e = EmailMultiAlternatives(
                            'testing',# subject
                            text_content,# content
                            settings.EMAIL_HOST_USER,# host e-mail
                            [email],# resipient e-mail
                        )
                        # defining subject content host e-mail and list of resipient 
                        e.attach_alternative(html_content,'text/html')
                        e.send()
                        # sending the e-mail with data from e 
                        is_verified = True
                        # defining booking as verified 
                        request.session['fname'] = first_name
                        request.session['mname'] = middle_name
                        request.session['lname'] = last_name
                        request.session['email'] = email
                        request.session['cnum'] = contact_num
                        request.session['date'] = date 
                        request.session['time'] = time
                        request.session['adult'] = adult
                        request.session['child'] = child
                        # Above are sessions generated to send data from one view to other views 
                else:
                    return HttpResponse('bhai email to daal de!!!!!!')
                # redirecting to info page which will tell user to get the link from e-mail for further steps 
                return redirect('/booking/info/page')
        except Exception as e :
            print(e)
            raise HttpResponse('chalak bro')
    except Exception as e:
        print(e)
        raise Http404 
    print(number)
    return render(request,'booking/booking_form.html',{'form':form,'plan':_plan,'emailform':email_form,'code':number})



def verify_email(request):
    '''
This function is performing following :
->  It accepts GET request when data is required to display
->  It also accepts POST request when submit button is clicked
->  POST request deletes the session
'''
    print(request.POST)
    try:
        if not request.method == 'POST':
            # getting data from sessions that were created in booking view
            first_name = request.session.get('fname') 
            middle_name = request.session.get('mname')
            last_name = request.session.get('lname')
            email = request.session.get('email')
            contact_num = request.session.get('cnum')
            time = request.session.get('time')
            adult = request.session.get('adult')
            child = request.session.get('child')
            context = {
                'first_name':first_name, 
                'middle_name':middle_name,
                'last_name':last_name,
                'email':email,
                'contact_number':contact_num,
                'time':time,
                'adult':adult,
                'child':child
                }
            print(f'{first_name}\n{middle_name}\n{last_name}')
            return render(request,'booking/verify.html',context)
        else:
            # getting submit button value 
            sub = request.POST['sub']
            # checking whether sub is more than 0 and if it is then delete all the sessions 
            if sub :
                del request.session['fname']
                del request.session['mname']
                del request.session['lname']
                return HttpResponse('bro data to delete ho gaya')
    except Exception as e:
        print(e)
        raise Http404 


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
    except:
        raise Http404 
    

def info_page(request):
    '''
This function performs following :
->  It gives info that now user should follow link from e-mail
'''
    first_name = request.session['fname'] 
    middle_name = request.session.get('mname')
    last_name = request.session.get('lname')
    return render(request,'booking/info_page.html',{'first_name':first_name,'middle_name':middle_name,'last_name':last_name})