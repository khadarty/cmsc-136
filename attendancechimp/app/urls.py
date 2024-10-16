from django.urls import path

from . import views

urlpatterns = [
    path('handleform', views.handle_form, name='form'),
    path('', views.index, name='index'),
    path("time", views.get_central, name = "get_central"),
    path("sum",views.get_sum, name = "get_sum"),
    #path('handleform', views.handle_form, name='form'),
]
