from django import forms
from applications.core.models import MarcaMedicamento

class MarcaMedicamentoForm(forms.ModelForm):
    class Meta:
        model = MarcaMedicamento
        fields = ['nombre', 'descripcion', 'activo']
        labels = {
            'nombre': 'Nombre de la Marca',
            'descripcion': 'Descripción',
            'activo': 'Activo',
        }
        help_texts = {
            'nombre': 'Nombre comercial de la marca (ejemplo: Pfizer, Bayer, Novartis)',
            'descripcion': 'Observaciones o detalles de esta marca.',
            'activo': 'Marca como activa o inactiva para uso en el sistema.',
        }
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
