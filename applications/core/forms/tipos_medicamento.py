from django import forms
from applications.core.models import TipoMedicamento


class TipoMedicamentoForm(forms.ModelForm):
    class Meta:
        model = TipoMedicamento
        fields = ['nombre', 'descripcion', 'activo']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'w-full rounded-lg border-gray-300 shadow-sm dark:bg-principal dark:border-gray-600 dark:text-white',
                'placeholder': 'Ejemplo: Antibiótico, Analgésico...',
                'autocomplete': 'off'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'w-full rounded-lg border-gray-300 shadow-sm dark:bg-principal dark:border-gray-600 dark:text-white',
                'rows': 3,
                'placeholder': 'Descripción opcional del tipo de medicamento'
            }),
            'activo': forms.CheckboxInput(attrs={
                'class': 'h-5 w-5 text-blue-600 border-gray-300 rounded dark:bg-principal dark:border-gray-600'
            }),
        }
        labels = {
            'nombre': 'Nombre',
            'descripcion': 'Descripción',
            'activo': '¿Está activo?',
        }
