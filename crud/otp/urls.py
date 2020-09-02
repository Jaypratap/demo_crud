from django.urls import path, include
from django.conf.urls import url
from . import views

urlpatterns = [
    path('generate/', views.generateotp, name='generateotp'),
    path('verify/', views.verifyotp, name='verifyotp'),
    path('register/', views.register, name='register'),

]