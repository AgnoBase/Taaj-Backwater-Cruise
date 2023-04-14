from django.shortcuts import render
from django.http import HttpResponse,Http404
# Create your views here.
def home_page(request):
    try:
        if request.method == 'GET':
            return render(request,'root/index.html')
    except Exception as e:
        print(e)
        return Http404
        
        