from django import forms
from applications.core.models import Doctor  # Ajusta la ruta según tu proyecto

class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = '__all__'
        widgets = {
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date'}),
            'especialidad': forms.CheckboxSelectMultiple(),
            'horario_atencion': forms.Textarea(attrs={'rows': 3}),
        }
