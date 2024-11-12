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

# @csrf_exempt
# def index(request):
#     return render(request, 'app/index.html', {})

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
    if request.method == 'POST':
        email = request.POST.get('email')
        user_name = request.POST.get('user_name')
        password = request.POST.get('password')
        is_student = request.POST.get('is_student') == '1'

       
        if User.objects.filter(email=email).exists():
            return JsonResponse({'error': 'A user with this email already exists.'}, status=400)

        
        user = User.objects.create_user(username=user_name, email=email, password=password)
        user.save()

        
        return JsonResponse({'success': 'User created successfully.'}, status=200)
    
    return JsonResponse({'error': 'Invalid request method.'}, status=405)

# @login_required
def index(request):
  
    chicago_time = timezone.now().astimezone(pytz.timezone("America/Chicago"))
    current_time = chicago_time.strftime("%H:%M") 
 
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
    
@csrf_exempt
def create_course(request):
    if not request.user.is_authenticated or not request.user.is_instructor:
        return HttpResponse(status=401)
    if request.method == "POST":
        course_name = request.POST.get("course-name")
        start_time = request.POST.get("start-time")
        end_time = request.POST.get("end-time")
        days = [day for day in ["mon", "tue", "wed", "thu", "fri"] if request.POST.get(f"day-{day}")]
        
        Course.objects.create(name=course_name, start_time=start_time, end_time=end_time, days=days)
        return JsonResponse({"status": "Course created"}, status=201)
    return HttpResponse(status=405)

@csrf_exempt
def create_lecture(request):
    if not request.user.is_authenticated or not request.user.is_instructor:
        return HttpResponse(status=401)
    if request.method == "POST":
        course_id = request.POST.get("choice")
        course = Course.objects.get(id=course_id)
        Lecture.objects.create(course=course)
        return JsonResponse({"status": "Lecture created"}, status=201)
    return HttpResponse(status=405)

@csrf_exempt
def create_qr_upload(request):
    if not request.user.is_authenticated or not request.user.is_student:
        return HttpResponse(status=401)
    if request.method == "POST":
        image = request.FILES.get("imageUpload")
        QRCodeUpload.objects.create(user=request.user, image=image)
        return JsonResponse({"status": "Upload created"}, status=201)
    return HttpResponse(status=405)