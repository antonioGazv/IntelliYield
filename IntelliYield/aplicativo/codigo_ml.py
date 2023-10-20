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


def tratarDados(N, P, K, temperature, humidity, ph, rainfall):
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

def rfc(X_train_norm, y_train, X_test_norm, user_data_norm, y_test):
    #Random Forest
    rfc = RandomForestClassifier().fit(X_train_norm, y_train)
    rfcPred = rfc.predict(X_test_norm)
    rfcPredUser = rfc.predict(user_data_norm)
    rfcPrecisao = accuracy_score(y_test, rfcPred)
    
    return rfcPredUser, rfcPrecisao

def knn(X_train_norm, y_train, X_test_norm, user_data_norm, y_test):
    #KNN
    knn = KNeighborsClassifier(n_neighbors=10)
    knn.fit(X_train_norm, y_train)
    knnPred = knn.predict(X_test_norm)
    knnPredUser = knn.predict(user_data_norm)
    knnPrecisao = accuracy_score(y_test, knnPred)

    return knnPredUser, knnPrecisao

def svc(X_train_norm, y_train, X_test_norm, user_data_norm, y_test):
    #SVM
    svc = SVC(kernel='linear')
    svc.fit(X_train_norm, y_train)
    svcPred = svc.predict(X_test_norm)
    svcPredUser = svc.predict(user_data_norm)
    svcPrecisao = accuracy_score(y_test, svcPred)

    return svcPredUser, svcPrecisao

def lda(X_train_norm, y_train, X_test_norm, user_data_norm, y_test):
    #LDA
    lda = LinearDiscriminantAnalysis().fit(X_train_norm, y_train)
    ldaPred = lda.predict(X_test_norm)
    ldaPredUser = lda.predict(user_data_norm)    
    ldaPrecisao = accuracy_score(y_test, ldaPred)

    return ldaPredUser, ldaPrecisao

def salvar_resultados(predicoes, detalhesrfc, detalhesknn, detalhessvc, detalheslda):
    Previsoes.objects.create(predicaoTot = predicoes)

    for detalhe in detalhesrfc:
        DetalhesRFC.objects.create(nome=detalhe['Nome'], predicaoRFC=detalhe['Predição'], precisaoRFC=detalhe['Precisão'])

    for detalhe in detalhesknn:
        DetalhesKNN.objects.create(nome=detalhe['Nome'], predicaoKNN=detalhe['Predição'], precisaoKNN=detalhe['Precisão'])

    for detalhe in detalhessvc:
        DetalhesSVC.objects.create(nome=detalhe['Nome'], predicaoSVC=detalhe['Predição'], precisaoSVC=detalhe['Precisão'])

    for detalhe in detalheslda:
        DetalhesLDA.objects.create(nome=detalhe['Nome'], predicaoLDA=detalhe['Predição'], precisaoLDA=detalhe['Precisão'])

def resultados(rfcPredUser, knnPredUser, svcPredUser, ldaPredUser, rfcPrecisao, knnPrecisao, svcPrecisao, ldaPrecisao):

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

    salvar_resultados(predicoes, detalhesrfc, detalhesknn, detalhessvc, detalheslda)

    return predicoes, detalhesrfc, detalhesknn, detalhessvc, detalheslda
