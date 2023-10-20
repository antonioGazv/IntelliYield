from django import forms

class MLForm(forms.Form):
    N = forms.DecimalField(label='Nitrogênio')
    P = forms.DecimalField(label='Fósforo')
    K = forms.DecimalField(label='Potássio')
    temperature = forms.DecimalField(label='Temperatura (°C)')
    humidity = forms.DecimalField(label='Umidade (%)')
    ph = forms.DecimalField(label='pH')
    rainfall = forms.DecimalField(label='Precipitação (mm)')

