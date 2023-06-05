
from django.shortcuts import render,redirect
from .forms import BookingForm
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .models import *
from django.http import Http404
import razorpay
from django.views.decorators.csrf import csrf_exempt
from Project.settings import RAZORPAY_KEY_ID,RAZORPAY_KEY_ID


# Create your views here.


def services_page(request):
    
    
    try:
        plans = Plans.objects.all()
        print(plans)
        return render(request,'booking/services.html',{'Plans':plans})
    except Exception as e:
        print(e)
        raise Http404



def booking_form(request,id):

    _plan = Plans.objects.get(id=id)
    form = BookingForm(request.POST,id)
    if request.method == 'POST':
        if form.is_valid(): 
            email = form.cleaned_data['email']
            first_name = form.cleaned_data['fname']
            middle_name = form.cleaned_data['mname'] or ' '
            last_name = form.cleaned_data['lname']
            contact_num = request.POST['cnum']
            date_book = form.cleaned_data['arrivedate']
            date = str(date_book)
            time_book = form.cleaned_data['time']
            time = str(time_book)
            duration = request.POST['duration']
            adult = form.cleaned_data['adults']
            child = form.cleaned_data['child']
            btn = request.POST.get('book_btn')
            return redirect(f'../../payment/{first_name}/{middle_name}/{last_name}/{email}/{contact_num}/{duration}/{date}/{time}/{adult}/{child}/{id}')
    return render(request,'booking/booking_form.html',{'form':form,'plan':_plan})


def payment(request,fname,mname,lname,email,cnum,duration,date,time,adult,child,plan_id):

    _plan = Plans.objects.get(id=plan_id)
    price = 0
    if int(duration) == _plan.Duration1:
        duration = _plan.Duration1
        price = _plan.price1*100

    elif int(duration) == _plan.Duration2:
        duration = _plan.Duration2
        price = _plan.price2 * 100

    try:
        amount = price * (int(adult)+int(child))
        client = razorpay.Client(auth=("RAZORPAY_KEY_ID", "RAZORPAY_KEY_ID"))
        pay = client.order.create({'amount': amount, 'currency': 'INR', 'payment_capture': '1'})
        booking = Booking.objects.create(
            plan=_plan, fname=fname, mname=mname or None, lname=lname or None, email=email,cnum=cnum, arrivedate=date, time=time,adults=adult,child = child, amount=amount, provider_order_id=pay["id"]
        )
        booking.save()
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
                'price': price*(int(adult)+int(child)),
                'payment': pay['id'],
                'plan_id': plan_id,
                'plan':_plan,
                'callback_url':"http://" + "127.0.0.1:8000" + f"/booking/success/{fname}/{mname}/{lname}/{email}/{cnum}/{duration}/{date}/{time}/{adult}/{child}/{plan_id}",
                "razorpay_key": RAZORPAY_KEY_ID,
                "booking":booking,
            }
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
    # payment starting
    _plan = Plans.objects.get(id=plan_id)
    
    try:
        if email and fname and lname and cnum and date and time :
            context = {'price':_plan.price1,'plan':_plan.name,'fname':fname,'mname':mname,"adults":adult,'child':child,
                       'lname':lname,'email':email,'contact':cnum,'date':date,
                       'time':time}

            html_content = render_to_string('booking/emails_template.html',context)

            # converting html content to string so that it can be used in e-mail

            text_content = strip_tags(html_content)
            e = EmailMultiAlternatives(
                                        'Taaj Backwater Cruise Booking confirmation',# subject
                                        text_content,# content
                                        settings.EMAIL_HOST_USER,# host e-mail
                                        [email],# recipient e-mail
                                    )
                                    # defining subject content host e-mail and list of resipient
            e.attach_alternative(html_content,'text/html')
            e.send()
            # context['success'] = f'email is sent to {email}'
        else:
            return render(request,f'booking/payment/{fname}/{mname}/{lname}/{email}/{cnum}/{duration}/{date}/{time}/{adult}/{child}')
    except Exception as e:
        print(e)
        
        
        
    if request=='POST':
        a = request.POST
        order_id = " "
        for key, val in a.items():
            if key == 'razorpay_order_id':
                order_id = val
                break
    return render(request,'booking/success.html')
