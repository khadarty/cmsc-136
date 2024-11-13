from django.urls import path

from . import views

urlpatterns = [
    path('handleform', views.handle_form, name='form'),
    path('', views.index, name='index'),
    path("time", views.get_ct, name="get_ct"),
    path("sum", views.get_sum, name="get_sum"),
    path("new", views.sign_up, name="sign_up"),
    path("createUser", views.create_user, name="create_user"),
    path('new_course', views.new_course, name='course_create'), # course_create: localhost:8000/app/new_course
    path('new_lecture', views.new_lecture, name='qr_create'), # qr_create: localhost:8000/app/new_lecture
    path('new_qr_upload', views.new_qr_upload, name='qr_upload'), # qr_upload: localhost:8000/new_qr_upload
    path('createCourse/', views.createCourse, name='create_course'),
    path('createLecture/', views.createLecture, name='create_qr'),
    path('createQRCodeUpload/', views.createQRCodeUpload, name='upload_qr'),
    path('dumpUploads', views.dumpUploads, name='dump_uploads')
]
