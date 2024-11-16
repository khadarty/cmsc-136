from django.urls import path

from . import views

urlpatterns = [
    path('handleform', views.handle_form, name='form'),
    path('', views.index, name='index'),
    path('index.html', views.index, name='index_html'),
    path("time", views.get_central, name = "get_central"),
    path("sum",views.get_sum, name = "get_sum"),
    path("createUser",views.createUser, name = "createUser"),
    path("new",views.new_user_form, name = "new_user_form"),
    path('dummypage/', views.index, name='dummypage'),
    #new ones starting from here
    path('new_course', views.new_course, name='course_create'),
    path('new_lecture', views.new_lecture, name='lecture_create'),
    path('new_qr_upload', views.new_qr_upload, name='qr_upload'),
    path('createCourse', views.create_course, name='create_course'),
    path('createLecture', views.create_lecture, name='create_lecture'),
    path('createQRCodeUpload', views.create_qr_upload, name='create_qr_upload'),
    
    #path('handleform', views.handle_form, name='form'),
]

