from django import forms
from applications.core.models import Diagnostico


class DiagnosticoForm(forms.ModelForm):
    class Meta:
        model = Diagnostico
        fields = [
            'codigo',
            'descripcion',
            'datos_adicionales',
            'activo',
        ]
        widgets = {
            'datos_adicionales': forms.Textarea(attrs={'rows': 3}),
        }
