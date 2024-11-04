from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from .models import *
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
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

@require_http_methods(["GET"])
def new_user_form(request):
    return render(request, 'app/new_user_form.html')

@require_http_methods(["POST"])
@csrf_exempt
def createUser(request):
    email = request.POST.get('email')
    user_name = request.POST.get('user_name')
    password = request.POST.get('password')
    is_student = request.POST.get('is_student') == 1
    if User.objects.filter(email=email).exists():
        return JsonResponse({'error': 'A user with this email already exists.'}, status=200) 
    
    user = User.objects.create_user(username=user_name, email=email, password=password)
    user.profile.is_student = is_student  
    user.save()
    
    
    login(request, user)
    return JsonResponse({'success': 'User created and signed in successfully.'})

@login_required
def index(request):
  
    current_time = timezone.now().strftime("%Y-%m-%d %H:%M:%S")
 
    current_user = request.user.username if request.user.is_authenticated else "Guest"
 
    bio = "Khadijat Durojaiye!"

    context = {
        'current_time': current_time,
        'current_user': current_user,
        'bio': bio,
    }
    
    return render(request, 'app/index.html', context)

# def bio(request):
#     bio_text = 'Khadijat Durojaiye. Bing bong.'
#     return render(request, 'index.html', {'bio_text': bio_text})
# def time_now(request):
#     current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#     context = {
#         'bio_text': "This is my bio text.",  
#         'current_time': current_time,
#     }
    
#     return render(request, 'index.html', context)
    
