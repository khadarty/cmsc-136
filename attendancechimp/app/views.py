from django.shortcuts import render
from django.http import HttpResponse
from .models import User, UserProfile
from django.contrib.auth import get_user_model
from django.contrib.auth import login
from django.db import IntegrityError
from django.views.decorators.csrf import csrf_exempt
from .models import *
from datetime import datetime
import pytz
from django.utils import timezone

@csrf_exempt
def index(request):

    team_bio = [
        {"Name": "Delicia", "Bio": "Delicia is a fourth-year at the University of Chicago studying Economics and Data Science. She runs on the cross country and track and field team, enjoys trying new restaurants, and is pursuing a career in finance."},
        {"Name": "Khadijat", "Bio": "Khadijat is a fourth-year at the University of Chicago studying Data Science. She has a fostered cat named Soup who lives with her on campus, enjoys knitting in her free time, and is planning to pursue a career in software engineering or data science."}
    ]

    current_user = request.user

    current_time = timezone.now().strftime("%Y-%m-%d %H:%M:%S")

    context = {
        "team_bio": team_bio,
        "current_user": current_user,
        "current_time": current_time
    }

    return render(request, 'app/index.html', context)

@csrf_exempt
def handle_form(request):

    cname = request.POST['cname']
    cnum =  request.POST['cnum']

    print(cname, cnum)

    new_course = Course(cname, cnum)
    new_course.save()

    return render(request, 'app/index.html', {})

def get_ct(request):
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
            sum = int(sum) if sum.is_integer() else sum
            return HttpResponse(str(sum))
        except ValueError:
            return HttpResponse(status=400)
    return HttpResponse(status=405)

def sign_up(request):
    if request.method == "GET":
        return render(request, 'app/sign_up_form.html')
    return HttpResponse(status=405)

User = get_user_model()

@csrf_exempt
def create_user(request):
    if request.method == "POST":
        email = request.POST.get('email')
        user_name = request.POST.get('user_name')
        password = request.POST.get('password')
        is_student = request.POST.get('is_student') == '1'

        if User.objects.filter(email=email).exists():
            return HttpResponse("This email is already in use", status=400)

        try:
            user = User.objects.create_user(email=email, username=user_name, password=password)
            UserProfile.objects.create(user=user, is_student=is_student)

            login(request, user)
            return HttpResponse("User created and logged in successfully")
        except IntegrityError:
            return HttpResponse("Unable to create user", status=500)
    return HttpResponse(status=405)