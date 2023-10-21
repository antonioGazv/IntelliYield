from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .codigo_rec import tratarDados, resultados, rfc, knn, svc, lda
from .codigo_comp import escolher_plantio
from .forms import MLForm

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def user_input(request):
    if request.method == 'POST':
        form = MLForm(request.POST)
        if form.is_valid():
            N = form.cleaned_data['N']
            P = form.cleaned_data['P']
            K = form.cleaned_data['K']
            temperature = form.cleaned_data['temperature']
            humidity = form.cleaned_data['humidity']
            ph = form.cleaned_data['ph']
            rainfall = form.cleaned_data['rainfall']

            X_train_norm, y_train, X_test, user_data_norm, y_test = tratarDados(N, P, K, temperature, humidity, ph, rainfall)

            rfcPredUser, rfcPrecisao = rfc(X_train_norm, y_train, X_test, user_data_norm, y_test)
            knnPredUser, knnPrecisao = knn(X_train_norm, y_train, X_test, user_data_norm, y_test)
            svcPredUser, svcPrecisao = svc(X_train_norm, y_train, X_test, user_data_norm, y_test)
            ldaPredUser, ldaPrecisao = lda(X_train_norm, y_train, X_test, user_data_norm, y_test)
            
            predicoes, detalhesrfc, detalhesknn, detalhessvc, detalheslda = resultados(rfcPredUser, knnPredUser, svcPredUser, ldaPredUser, rfcPrecisao, knnPrecisao, svcPrecisao, ldaPrecisao)

            return render(request, 'result_rec.html', {'predicoes': predicoes, 'detalhesrfc': detalhesrfc, 'detalhesknn': detalhesknn, 'detalhessvc': detalhessvc, 'detalheslda': detalheslda})
    else:
        form = MLForm()

    return render(request, 'user_input_rec.html', {'form': form})

def index(request):
    return render(request, 'index.html')

def calcular_compatibilidade(request):
    if request.method == 'POST':
        form = MLForm(request.POST)
        if form.is_valid():
            N = form.cleaned_data['N']
            P = form.cleaned_data['P']
            K = form.cleaned_data['K']
            temperature = form.cleaned_data['temperature']
            humidity = form.cleaned_data['humidity']
            ph = form.cleaned_data['ph']
            rainfall = form.cleaned_data['rainfall']

        plantio_escolhido = request.POST['plantio']
        if plantio_escolhido in requisitos_plantios:
            usuario_data = [N, P, K, temperature, humidity, ph, rainfall]
            requisitos = requisitos_plantios[plantio_escolhido]
            compatibilidade = calcular_compatibilidade_solo(usuario_data, requisitos)
            return render(request, 'result_comp.html', {'compatibilidade': compatibilidade})

