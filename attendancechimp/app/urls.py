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
    #path('handleform', views.handle_form, name='form'),
]

