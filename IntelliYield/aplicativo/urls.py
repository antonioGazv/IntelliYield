from django.urls import path
from . import views

urlpatterns = [
    path('input/', views.user_input, name='user_input'),
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
]