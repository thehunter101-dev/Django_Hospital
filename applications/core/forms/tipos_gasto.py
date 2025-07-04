from django import forms
from applications.core.models import TipoGasto

class TipoGastoForm(forms.ModelForm):
    class Meta:
        model = TipoGasto
        fields = '__all__'
