from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import *
from datetime import datetime
import pytz

@csrf_exempt
def index(request):
    return render(request, 'app/index.html', {})

@csrf_exempt
def handle_form(request):

    new_course = Course(cname, cnum)
    new_course.save()

    return render(request, 'app/index.html', {})

def get_central(request):
    if request.method == "GET":
        ct = datetime.now(pytz.timezone("America/Chicago"))
        hr = ct.hour
        min = ct.minute
        five_string = f"{hr:02}:{min:02}"
        return HttpResponse(five_string)
    return HttpResponse(status=405)
    
def get_sum(request):
    if request.method == "GET":
        n1 = request.GET.get("n1")
        n2 = request.GET.get("n2")
        try:
            n1_float = float(n1)
            n2_float = float(n2)
            sum = n1_float + n2_float
            return HttpResponse(str(sum))
        except ValueError:
            return HttpResponse(status=400)
    return HttpResponse(status=405)   
    
    
