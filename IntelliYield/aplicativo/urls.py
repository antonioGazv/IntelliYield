from django.urls import path
from . import views

urlpatterns = [
    path('input/rec', views.user_input, name='user_input_rec'),
    path('input/comp', views.user_input, name='user_input_comp'),
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
]