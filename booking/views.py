
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
import razorpay
from django.views.decorators.csrf import csrf_exempt

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



def booking_form(request,id):
    '''
This function is performing following things:
    ->  It +generates form for booking for each plans
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
            middle_name = form.cleaned_data['mname'] or ' '
            last_name = form.cleaned_data['lname']
            contact_num = form.cleaned_data['cnum']
            date_book = form.cleaned_data['arrivedate']
            date = str(date_book)
            time_book = form.cleaned_data['time']
            time = str(time_book)
            duration = request.POST['duration']
            adult = form.cleaned_data['adults']
            child = form.cleaned_data['child']
            btn = request.POST.get('book_btn')
            print(date)
            return redirect(f'../../payment/{first_name}/{middle_name}/{last_name}/{email}/{contact_num}/{duration}/{date}/{time}/{adult}/{child}/{id}')
    return render(request,'booking/booking_form.html',{'form':form,'plan':_plan})


def payment(request,fname,mname,lname,email,cnum,duration,date,time,adult,child,plan_id):
    print(fname,mname,lname,email,cnum,duration,date,time,adult,child)
    # btn = request.POST.get('pay_btn')

    _plan = Plans.objects.get(id=plan_id)
    price = 0
    if int(duration) == _plan.Duration1:
        duration = _plan.Duration1
        price = _plan.price1*100
        print(duration,price)
    elif int(duration) == _plan.Duration2:
        duration = _plan.Duration2
        price = _plan.price2 * 100
        print(duration, price)

    try:
        print('trying payment')
        print(request.method)
        print('payment started')
        amount = price * (int(adult)+int(child))
        client = razorpay.Client(auth=("rzp_test_HNRUOAkgghvxhY", "ONW9btJMjrUBLARyQrIHJSiO"))
        pay = client.order.create({'amount': amount, 'currency': 'INR', 'payment_capture': '1'})
        print(pay)
        print('Payment Done')
        context = {
                'fname': fname,
                'mname': mname,
                'lname': lname,
                'email': email,
                'cnum': cnum,
                'duration': duration,
                'date': date,
                'time': time,
                'adult': adult,
                'child': child,
                'price': price * (int(adult)+int(child)),
                'payment': pay,
                'plan_id': plan_id,
                'plan':_plan
            }
        print('payment successfully')
        return render(request,'booking/paynow.html',context)

    except Exception as e:
        print(e)

    context = {
                'fname': fname,
                'mname': mname,
                'lname': lname,
                'email': email,
                'cnum': cnum,
                'duration': duration,
                'date': date,
                'time': time,
                'adult': adult,
                'child': child,
                'price': price * (int(adult)+int(child)),
                'plan_id': plan_id,
                'plan':_plan
            }
    return render(request,'booking/paynow.html',context)




@csrf_exempt
def success(request,fname,mname,lname,email,cnum,duration,date,time,adult,child,plan_id):

    _plan = Plans.objects.get(id=plan_id)
    booking = Booking.objects.create(plan=_plan, fname=fname, mname=mname or None, lname=lname, email=email,
                                      cnum=cnum, arrivedate=date, time=time,adults=adult,child =child)
    try:
        print('emailing')
        if booking.email and booking.fname and booking.lname and booking.cnum and booking.arrivedate and booking.time :
            print('email is started')
            context = {'price':booking.plan.price1,'plan':booking.plan.name,'fname':booking.fname,'mname':booking.mname,
                       'lname':booking.lname,'email':booking.email,'contact':booking.cnum,'date':booking.arrivedate,
                       'time':booking.time}

            html_content = render_to_string('booking/emails_template.html',context)

            # converting html content to string so that it can be used in e-mail

            text_content = strip_tags(html_content)
            e = EmailMultiAlternatives(
                                        'Taaj Backwater Cruise Booking confirmation',# subject
                                        text_content,# content
                                        settings.EMAIL_HOST_USER,# host e-mail
                                        [booking.email],# recipient e-mail
                                    )
                                    # defining subject content host e-mail and list of resipient
            e.attach_alternative(html_content,'text/html')
            e.send()
            # context['success'] = f'email is sent to {email}'
        else:
            print('not sent')
            return render(request,f'booking/payment/{fname}/{mname}/{lname}/{email}/{cnum}/{duration}/{date}/{time}/{adult}/{child}')
    except Exception as e:
        print(e)
    if request=='POST':
        a = request.POST
        print(a)

    return render(request,'booking/success.html')



    
