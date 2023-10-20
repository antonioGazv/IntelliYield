from django.db import models

# Create your models here.

class DetalhesRFC(models.Model):
    nome = models.CharField(max_length=255)
    predicaoRFC = models.CharField(max_length=255)
    precisaoRFC = models.FloatField()

class DetalhesKNN(models.Model):
    nome = models.CharField(max_length=255)
    predicaoKNN = models.CharField(max_length=255)
    precisaoKNN = models.FloatField()

class DetalhesSVC(models.Model):
    nome = models.CharField(max_length=255)
    predicaoSVC = models.CharField(max_length=255)
    precisaoSVC = models.FloatField()

class DetalhesLDA(models.Model):
    nome = models.CharField(max_length=255)
    predicaoLDA = models.CharField(max_length=255)
    precisaoLDA = models.FloatField()

class Previsoes(models.Model):
    predicaoTot = models.CharField(max_length=255)
