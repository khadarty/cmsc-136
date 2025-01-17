from django.core.files.storage import default_storage
from django.shortcuts import render, redirect
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
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth import authenticate


@csrf_exempt
def index(request):

    team_bio = [
        {"Name": "Delicia", "Bio": "Delicia is a fourth-year at the University of Chicago studying Economics and Data Science. She runs on the cross country and track and field teams, enjoys trying new restaurants, and is pursuing a career in finance."},
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
        is_student = request.POST.get('is_student') in ['true', '1']

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


@csrf_exempt
def new_course(request):
    if request.method == "GET":
        return render(request, 'app/new_course.html')
    return HttpResponse(status=405)


@csrf_exempt
def new_lecture(request):
    if request.method == "GET":
        return render(request, 'app/new_lecture.html')
    return HttpResponse(status=405)


@csrf_exempt
def new_qr_upload(request):
    if request.method == "GET":
        return render(request, 'app/new_qr_upload.html')
    return HttpResponse(status=405)


@csrf_exempt
def createCourse(request):
    if request.user.is_authenticated and hasattr(request.user, 'userprofile') and not request.user.userprofile.is_student:
        if request.method == "POST":
            # Extract and validate form data
            course_name = request.POST.get("course-name")
            start_time = request.POST.get("start-time")
            end_time = request.POST.get("end-time")
            days = [day for day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"] 
                    if request.POST.get(f"day-{day[:3].lower()}") in [True, "1"]]

            # Check required fields
            if course_name and start_time and end_time and days:
                try:
                    # Save course
                    course = Course(
                        name=course_name,
                        start_time=start_time,
                        end_time=end_time,
                        days_of_week=",".join(days)
                        #instructor=request.user.username
                    )
                    course.save()
                    return JsonResponse({"success": "Course created successfully"}, status=200)
                
                except Exception as e:
                    print(f"Error in createCourse: {e}")
                    return JsonResponse({"error": "Internal server error"}, status=500)
            else:
                return JsonResponse({"error": "All fields are required."}, status=400)

    return JsonResponse({"error": "Unauthorized"}, status=401)


@csrf_exempt  # Remove if CSRF protection is enabled
def createLecture(request):
    if request.user.is_authenticated and hasattr(request.user, 'userprofile') and not request.user.userprofile.is_student:
        if request.method == "POST":
            name = request.POST.get("choice")  # Course name
            qrdata = request.POST.get("qrdata")  # Optional QR data
            
            if name:
                
                if not qrdata:
                    qrdata = ''.join(random.choices(string.ascii_letters + string.digits, k=16))

                
                try:
                    course = Course.objects.get(name=name)
                    lecture = Lecture(course=course, qrdata=qrdata)  
                    lecture.save()
                    return JsonResponse({"success": "Lecture created successfully", "qrdata": qrdata}, status=200)
                except Course.DoesNotExist:
                    return JsonResponse({"error": "Course does not exist"}, status=404)

            return JsonResponse({"error": "All fields are required."}, status=400)

       
        courses = Course.objects.all()  
        return render(request, 'app/new_lecture.html', {'courses': courses})

    return HttpResponse("Unauthorized", status=401)


@csrf_exempt  # Remove if CSRF protection is enabled
def createQRCodeUpload(request):
    if request.user.is_authenticated and hasattr(request.user, 'userprofile') and request.user.userprofile.is_student:
        if request.method == "POST" and request.FILES.get("imageUpload"):
            image = request.FILES["imageUpload"]
          
            file_path = default_storage.save(f"uploads/{image.name}", image)
            
            # Save file information to QRCodeUpload model (adjust fields as needed)
            qr_upload = QR_Code(student=request.user.username, qr_image=image)
            qr_upload.save()
            return JsonResponse({"success": "QR Code uploaded successfully"}, status=200)

        return render(request, 'app/new_qr_upload.html', {'errors': "Please select a file to upload."})

    return HttpResponse("Unauthorized", status=401)


def dumpUploads(request):

    if not request.user.is_authenticated:

        return HttpResponse("", status=401)

    # check if the user is an instructor
    if hasattr(request.user, 'userprofile') and not request.user.userprofile.is_student:
        # retrieve all uploads and create the list of dictionaries
        obj = [
            {
                "name": request.user.username,  # Adjust if your model stores the username differently
                "upload_time": upload.timestamp.strftime("%Y-%m-%d %H:%M:%S")
            }
            for upload in QR_Code.objects.all()
        ]
        
        # return the list in JSON format
        return JsonResponse(obj, safe=False)
    
    # return 401 if the user is not an instructor
    return HttpResponse("", status=401)

def getUploads(request):
    # check for 'course' parameter
    course_id = request.GET.get('course')
    if not course_id:
        return JsonResponse({'error': 'Course ID is required'}, status=400)
    
    try:
        # call the helper function to get attendance data
        uploads = getUploadsForCourse(course_id)
        
        # format data as  list of dictionaries
        response_data = [
            {'username': upload['username'], 'upload_time_as_string': str(upload['upload_time'])}
            for upload in uploads
        ]
        return JsonResponse(response_data, safe=False)
    except ObjectDoesNotExist:
        return JsonResponse({'error': 'Invalid course ID or no data found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)