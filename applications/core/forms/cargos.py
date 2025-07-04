# applications/core/forms/cargos.py
from django import forms
from applications.core.models import Cargo

class CargoForm(forms.ModelForm):
    class Meta:
        model = Cargo
        fields = ['nombre', 'descripcion', 'activo']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control'}),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
