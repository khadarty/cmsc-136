from django.urls import path

from . import views

urlpatterns = [
    path('handleform', views.handle_form, name='form'),
    path('', views.index, name='index'),
    #path('handleform', views.handle_form, name='form'),
    path("time", views.get_ct, name="get_ct"),
    path("sum", views.get_sum, name="get_sum")
]
