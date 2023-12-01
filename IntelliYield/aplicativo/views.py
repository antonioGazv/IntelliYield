from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, logout, update_session_auth_hash
from django.contrib.auth import login as auth_login
from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .codigo_rec import Ferramenta_REC
# from .models import Historico
from .forms import MLForm, CustomUserChangeForm

ferramenta_rec = Ferramenta_REC()

def register(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            auth_login(request, user)
            return redirect('index')
        else:
            messages.error(request, "Dados inválidos.")
    context = {'form': form}
    return render(request, 'register.html', context)

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('index')
        else:
            messages.error(request, "Dados inválidos.")
            return redirect('login.html')

    return render(request, 'login.html')

def user_logout(request):
    logout(request)
    return redirect('index')

@login_required
def editarConta(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = CustomUserChangeForm(instance=request.user)
    return render(request, 'editarConta.html', {'form': form})

@login_required
def alterarSenha(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Sua senha foi alterada com sucesso!')
            return redirect('index')
        else:
            messages.error(request, 'Por favor, corrija os erros abaixo.')
    else:
        form = PasswordChangeForm(request.user)

    return render(request, 'alterarSenha.html', {'form': form})

@login_required
def excluirConta(request):
    if request.method == 'POST':
        request.user.delete()
        return redirect('index')
    return render(request, 'excluirConta.html')

# @login_required
# def historico(request):
#     resultados = Historico.objects.filter(usuario=request.user)
#     return render(request, 'historico.html', {'resultados': resultados})

@login_required
def perfil(request):
    return render(request, 'perfil.html')

@login_required
def user_input(request):
    if request.method == 'POST':
        ferramenta_rec.set_user(request.user)
        form = MLForm(request.POST)
        if form.is_valid():
            N = form.cleaned_data['N']
            P = form.cleaned_data['P']
            K = form.cleaned_data['K']
            temperature = form.cleaned_data['temperature']
            humidity = form.cleaned_data['humidity']
            ph = form.cleaned_data['ph']
            rainfall = form.cleaned_data['rainfall']

            X_train_norm, y_train, X_test, user_data_norm, y_test = ferramenta_rec.tratar_dados(N, P, K, temperature, humidity, ph, rainfall)

            rfcPredUser, rfcPrecisao = ferramenta_rec.rfc(X_train_norm, y_train, X_test, user_data_norm, y_test)
            knnPredUser, knnPrecisao = ferramenta_rec.knn(X_train_norm, y_train, X_test, user_data_norm, y_test)
            svcPredUser, svcPrecisao = ferramenta_rec.svc(X_train_norm, y_train, X_test, user_data_norm, y_test)
            ldaPredUser, ldaPrecisao = ferramenta_rec.lda(X_train_norm, y_train, X_test, user_data_norm, y_test)

            predicoes, detalhesrfc, detalhesknn, detalhessvc, detalheslda = ferramenta_rec.resultados(request, rfcPredUser, knnPredUser, svcPredUser, ldaPredUser, rfcPrecisao, knnPrecisao, svcPrecisao, ldaPrecisao)

            return render(request, 'result_rec.html', {'predicoes': predicoes, 'detalhesrfc': detalhesrfc, 'detalhesknn': detalhesknn, 'detalhessvc': detalhessvc, 'detalheslda': detalheslda})

            ferramenta_rec.salvar_resultados(request, predicoes, detalhesrfc, detalhesknn, detalhessvc, detalheslda)
    else:
        form = MLForm()

    return render(request, 'user_input_rec.html', {'form': form})


def index(request):
    return render(request, 'index.html')
