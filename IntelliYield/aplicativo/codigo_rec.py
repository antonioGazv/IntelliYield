import pandas as pd
import numpy as np
import statistics
from sklearn import preprocessing
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from .models import DetalhesRFC, DetalhesKNN, DetalhesSVC, DetalhesLDA, Previsoes
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

class Ferramenta_REC:
    def __init__(self, user=None):
        self.user = user

    def set_user(self, user):
        self.user = user

    def tratar_dados(self, N, P, K, temperature, humidity, ph, rainfall):
        csv_path = "aplicativo/dataEst.csv"
        dataset = pd.read_csv(csv_path)
        X = dataset.drop("label", axis=1)
        y = dataset["label"]
        lb = preprocessing.LabelEncoder()
        y_encoded = lb.fit_transform(y)
        user_data = [N, P, K, temperature, humidity, ph, rainfall]

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=1)

        scaler = MinMaxScaler()
        X_train_norm = scaler.fit_transform(X_train)
        X_test_norm = scaler.fit_transform(X_test)
        user_data_norm = scaler.transform([user_data])

        return X_train_norm, y_train, X_test_norm, user_data_norm, y_test

    def rfc(self, X_train_norm, y_train, X_test_norm, user_data_norm, y_test):
        # Random Forest
        rfc = RandomForestClassifier().fit(X_train_norm, y_train)
        rfcPred = rfc.predict(X_test_norm)
        rfcPredUser = rfc.predict(user_data_norm)
        rfcPrecisao = accuracy_score(y_test, rfcPred)

        return rfcPredUser, rfcPrecisao

    def knn(self, X_train_norm, y_train, X_test_norm, user_data_norm, y_test):
        # KNN
        knn = KNeighborsClassifier(n_neighbors=10)
        knn.fit(X_train_norm, y_train)
        knnPred = knn.predict(X_test_norm)
        knnPredUser = knn.predict(user_data_norm)
        knnPrecisao = accuracy_score(y_test, knnPred)

        return knnPredUser, knnPrecisao

    def svc(self, X_train_norm, y_train, X_test_norm, user_data_norm, y_test):
        # SVM
        svc = SVC(kernel='linear')
        svc.fit(X_train_norm, y_train)
        svcPred = svc.predict(X_test_norm)
        svcPredUser = svc.predict(user_data_norm)
        svcPrecisao = accuracy_score(y_test, svcPred)

        return svcPredUser, svcPrecisao

    def lda(self, X_train_norm, y_train, X_test_norm, user_data_norm, y_test):
        # LDA
        lda = LinearDiscriminantAnalysis().fit(X_train_norm, y_train)
        ldaPred = lda.predict(X_test_norm)
        ldaPredUser = lda.predict(user_data_norm)
        ldaPrecisao = accuracy_score(y_test, ldaPred)

        return ldaPredUser, ldaPrecisao

    @login_required
    def salvar_resultados(self, request, predicoes, detalhesrfc, detalhesknn, detalhessvc, detalheslda):
        current_user = self.user
        previsoes_obj = Previsoes.objects.create(user=current_user, predicaoTot=predicoes)

        for detalhe in detalhesrfc:
            DetalhesRFC.objects.create(user=current_user, predicaoRFC=detalhe['Predição'], precisaoRFC=detalhe['Precisão'], nome=detalhe['Nome'])

        for detalhe in detalhesknn:
            DetalhesKNN.objects.create(user=current_user, predicaoKNN=detalhe['Predição'], precisaoKNN=detalhe['Precisão'], nome=detalhe['Nome'])

        for detalhe in detalhessvc:
            DetalhesSVC.objects.create(user=current_user, predicaoSVC=detalhe['Predição'], precisaoSVC=detalhe['Precisão'], nome=detalhe['Nome'])

        for detalhe in detalheslda:
            DetalhesLDA.objects.create(user=current_user, predicaoLDA=detalhe['Predição'], precisaoLDA=detalhe['Precisão'], nome=detalhe['Nome'])

        return HttpResponse("Resultados salvos com sucesso")

    def resultados(self, request, rfcPredUser, knnPredUser, svcPredUser, ldaPredUser, rfcPrecisao, knnPrecisao, svcPrecisao, ldaPrecisao):
        detalhesrfc = []
        detalhesknn = []
        detalhessvc = []
        detalheslda = []

        detalhesrfc.append({
            'Nome': 'Random Forest Classifier',
            'Predição': rfcPredUser,
            'Precisão': rfcPrecisao
        })

        detalhesknn.append({
            'Nome': 'K Nearest Neighbors',
            'Predição': knnPredUser,
            'Precisão': knnPrecisao
        })

        detalhessvc.append({
            'Nome': 'Support Vector Classifier',
            'Predição': svcPredUser,
            'Precisão': svcPrecisao
        })

        detalheslda.append({
            'Nome': 'Linear Discriminant Analysis',
            'Predição': ldaPredUser,
            'Precisão': ldaPrecisao
        })

        predicoes = statistics.mode([tuple(array) for array in [rfcPredUser, knnPredUser, svcPredUser, ldaPredUser]])

        detalhes_totais = detalhesrfc + detalhesknn + detalhessvc + detalheslda
        detalhes_totais_str = "\n".join([f"{detalhe['Nome']}: {detalhe['Predição']} (Precisão: {detalhe['Precisão']})" for detalhe in detalhes_totais])

        # Historico.objects.create(usuario=request.user, predicao=predicoes, detalhes=detalhes_totais_str)

        self.salvar_resultados(request, predicoes, detalhesrfc, detalhesknn, detalhessvc, detalheslda)

        return predicoes, detalhesrfc, detalhesknn, detalhessvc, detalheslda
