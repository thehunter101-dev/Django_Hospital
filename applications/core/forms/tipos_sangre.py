from django import forms
from applications.core.models import TipoSangre

class TipoSangreForm(forms.ModelForm):
    class Meta:
        model = TipoSangre
        fields = ['tipo', 'descripcion']
        widgets = {
            'tipo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. O+', 'maxlength': '10'}),
            'descripcion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Descripción del tipo', 'maxlength': '100'}),
        }
