from django import forms
from applications.core.models import Empleado, Cargo


class EmpleadoForm(forms.ModelForm):
    cargo = forms.ModelChoiceField(
        queryset=Cargo.objects.filter(activo=True),
        label="Cargo",
        empty_label="Seleccione un cargo",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Empleado
        fields = [
            'nombres',
            'apellidos',
            'cedula_ecuatoriana',
            'dni',
            'fecha_nacimiento',
            'cargo',
            'sueldo',
            'fecha_ingreso',
            'direccion',
            'latitud',
            'longitud',
            'foto',
            'activo',
        ]
        widgets = {
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date'}),
            'fecha_ingreso': forms.DateInput(attrs={'type': 'date'}),
            'direccion': forms.Textarea(attrs={'rows': 2}),
        }
