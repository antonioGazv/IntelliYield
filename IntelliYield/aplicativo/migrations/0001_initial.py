# Generated by Django 4.2.5 on 2023-10-19 20:00

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DetalhesKNN',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=255)),
                ('predicao', models.CharField(max_length=255)),
                ('precisao', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='DetalhesLDA',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=255)),
                ('predicao', models.CharField(max_length=255)),
                ('precisao', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='DetalhesRFC',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=255)),
                ('predicao', models.CharField(max_length=255)),
                ('precisao', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='DetalhesSVC',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=255)),
                ('predicao', models.CharField(max_length=255)),
                ('precisao', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Previsoes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('previsao', models.CharField(max_length=255)),
            ],
        ),
    ]