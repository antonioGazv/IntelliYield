from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path("", views.index, name='index'),
    path('input/rec/', views.user_input, name='user_input_rec'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('logout/', views.user_logout, name='user_logout'),
    path('historico/', views.historico, name='historico'),
    path('editarConta/', views.editarConta, name='editarConta'),
    path('password/', auth_views.PasswordChangeView.as_view(template_name='alterarSenha.html', success_url=""), name='password'),
    path('excluirConta/', views.excluirConta, name='excluirConta'),
    path('perfil/', views.perfil, name='perfil'),
]