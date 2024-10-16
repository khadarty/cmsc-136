from django.http import HttpResponse

def dummypage(request):
     if request.method == "GET": 
         return HttpResponse("No content here, sorry!")


