# apps/core/forms/paciente.py
from django import forms
from applications.core.models import Paciente

class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        exclude = []
        widgets = {
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date'}),
            'direccion': forms.Textarea(attrs={'rows': 2}),
            'antecedentes_personales': forms.Textarea(attrs={'rows': 3}),
            'antecedentes_quirurgicos': forms.Textarea(attrs={'rows': 3}),
            'antecedentes_familiares': forms.Textarea(attrs={'rows': 3}),
            'alergias': forms.Textarea(attrs={'rows': 3}),
            'medicamentos_actuales': forms.Textarea(attrs={'rows': 3}),
            'vacunas': forms.Textarea(attrs={'rows': 3}),
            'antecedentes_gineco_obstetricos': forms.Textarea(attrs={'rows': 3}),
        }