from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User

class MLForm(forms.Form):
    N = forms.DecimalField(label='Nitrogênio')
    P = forms.DecimalField(label='Fósforo')
    K = forms.DecimalField(label='Potássio')
    temperature = forms.DecimalField(label='Temperatura (°C)')
    humidity = forms.DecimalField(label='Umidade (%)')
    ph = forms.DecimalField(label='pH')
    rainfall = forms.DecimalField(label='Precipitação (mm)')

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = (
            'username',
            'email',
        )