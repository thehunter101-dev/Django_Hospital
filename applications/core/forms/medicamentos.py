from django import forms
from applications.core.models import Medicamento


class MedicamentoForm(forms.ModelForm):
    class Meta:
        model = Medicamento
        fields = [
            'tipo',
            'marca_medicamento',
            'nombre',
            'descripcion',
            'concentracion',
            'via_administracion',
            'cantidad',
            'precio',
            'comercial',
            'foto',
        ]
        labels = {
            'tipo': 'Tipo de Medicamento',
            'marca_medicamento': 'Marca del Medicamento',
            'nombre': 'Nombre del Medicamento',
            'descripcion': 'Descripción',
            'concentracion': 'Concentración',
            'via_administracion': 'Vía de Administración',
            'cantidad': 'Stock',
            'precio': 'Precio Unitario',
            'comercial': '¿Es Comercial?',
            'foto': 'Foto del Medicamento',
        }
        widgets = {
            'tipo': forms.Select(attrs={'class': 'form-select w-full'}),
            'marca_medicamento': forms.Select(attrs={'class': 'form-select w-full'}),
            'nombre': forms.TextInput(attrs={
                'class': 'form-input w-full',
                'placeholder': 'Ejemplo: Ibuprofeno'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-textarea w-full',
                'placeholder': 'Uso, indicaciones, precauciones...',
                'rows': 3
            }),
            'concentracion': forms.TextInput(attrs={
                'class': 'form-input w-full',
                'placeholder': 'Ejemplo: 500mg'
            }),
            'via_administracion': forms.Select(attrs={'class': 'form-select w-full'}),
            'cantidad': forms.NumberInput(attrs={
                'class': 'form-input w-full',
                'placeholder': 'Cantidad en inventario'
            }),
            'precio': forms.NumberInput(attrs={
                'class': 'form-input w-full',
                'placeholder': 'Ejemplo: 5.00',
                'step': '0.01'
            }),
            'comercial': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
            'foto': forms.ClearableFileInput(attrs={'class': 'form-file w-full'}),
        }
