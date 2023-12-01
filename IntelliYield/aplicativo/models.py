from django.db import models
from django.contrib.auth.models import User

# class DetalhesRFC(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     nome = models.CharField(max_length=255)
#     predicaoRFC = models.CharField(max_length=255)
#     precisaoRFC = models.FloatField()

# class DetalhesKNN(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     nome = models.CharField(max_length=255)
#     predicaoKNN = models.CharField(max_length=255)
#     precisaoKNN = models.FloatField()

# class DetalhesSVC(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     nome = models.CharField(max_length=255)
#     predicaoSVC = models.CharField(max_length=255)
#     precisaoSVC = models.FloatField()

# class DetalhesLDA(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     nome = models.CharField(max_length=255)
#     predicaoLDA = models.CharField(max_length=255)
#     precisaoLDA = models.FloatField()

class Previsoes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    predicaoTot = models.CharField(max_length=255)
    predicaoLDA = models.CharField(max_length=255)
    precisaoLDA = models.FloatField()
    predicaoSVC = models.CharField(max_length=255)
    precisaoSVC = models.FloatField()
    predicaoKNN = models.CharField(max_length=255)
    precisaoKNN = models.FloatField()
    predicaoRFC = models.CharField(max_length=255)
    precisaoRFC = models.FloatField()
    
# class Historico(models.Model):
#     usuario = models.ForeignKey(User, on_delete=models.CASCADE)
#     predicao = models.CharField(max_length=255)
#     detalhes = models.TextField()