from django.shortcuts import render
from django.http import HttpResponse,Http404
from .models import Faq
# Create your views here.
def home_page(request):
    print('working home page')
    faqs = Faq.objects.order_by('date')[:3]
    print(faqs)
    try:
        return render(request,'root/index.html',{'faqs':faqs})
    except Exception as e:
        print(e)
    return render(request,'root/index.html',{'faqs':faqs})
    
def faq_page(request):
    faqs = Faq.objects.all()
    for faq in faqs:
        print(faq.question, faq.answer, faq.date)
    print(faqs)
    return render(request, 'root/faqmobile.html',{'faqs':faqs})

    
