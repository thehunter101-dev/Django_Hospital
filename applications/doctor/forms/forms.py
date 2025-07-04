from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import datetime, date, time
from applications.doctor.models import CitaMedica , PacienteCore

class CitaMedicaForm(forms.ModelForm):
    class Meta:
        model = CitaMedica
        fields = ['paciente', 'fecha', 'hora_cita', 'estado', 'observaciones']
        widgets = {
            'paciente': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': 'Seleccione un paciente'
            }),
            'fecha': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'min': date.today().strftime('%Y-%m-%d')
            }),
            'hora_cita': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time',
                'step': '300'  # 5 minutos
            }),
            'estado': forms.Select(attrs={
                'class': 'form-control'
            }),
            'observaciones': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Observaciones adicionales (opcional)'
            })
        }
        labels = {
            'paciente': 'Paciente',
            'fecha': 'Fecha de la Cita',
            'hora_cita': 'Hora de la Cita',
            'estado': 'Estado',
            'observaciones': 'Observaciones'
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Hacer que todos los campos sean obligatorios excepto observaciones
        for field_name, field in self.fields.items():
            if field_name != 'observaciones':
                field.required = True
    
    def clean_fecha(self):
        fecha = self.cleaned_data.get('fecha')
        if fecha and fecha < date.today():
            raise ValidationError('La fecha de la cita no puede ser en el pasado.')
        return fecha
    
    def clean_hora_cita(self):
        hora_cita = self.cleaned_data.get('hora_cita')
        if hora_cita:
            # Validar que la hora esté en horario de atención (8:00 AM a 6:00 PM)
            hora_inicio = time(8, 0)  # 8:00 AM
            hora_fin = time(18, 0)    # 6:00 PM
            
            if not (hora_inicio <= hora_cita <= hora_fin):
                raise ValidationError('La hora debe estar entre 8:00 AM y 6:00 PM.')
        
        return hora_cita
    
    def clean(self):
        cleaned_data = super().clean()
        fecha = cleaned_data.get('fecha')
        hora_cita = cleaned_data.get('hora_cita')
        
        if fecha and hora_cita:
            # Validar que no haya otra cita en la misma fecha y hora
            existing_cita = CitaMedica.objects.filter(
                fecha=fecha,
                hora_cita=hora_cita
            )
            
            # Si estamos editando, excluir la cita actual
            if self.instance and self.instance.pk:
                existing_cita = existing_cita.exclude(pk=self.instance.pk)
            
            if existing_cita.exists():
                raise ValidationError('Ya existe una cita programada para esta fecha y hora.')
            
            # Validar que la fecha y hora no sean en el pasado
            fecha_hora_cita = datetime.combine(fecha, hora_cita)
            if fecha_hora_cita < timezone.now():
                raise ValidationError('La fecha y hora de la cita no pueden ser en el pasado.')
        
        return cleaned_data

class CitaMedicaFilterForm(forms.Form):
    """Formulario para filtrar citas médicas"""
    search = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Buscar por paciente u observaciones...'
        })
    )
    
    estado = forms.ChoiceField(
        choices=[('', 'Todos los estados')] + CitaMedica._meta.get_field('estado').choices,
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )
    
    fecha_desde = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )
    
    fecha_hasta = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )
    
    def clean(self):
        cleaned_data = super().clean()
        fecha_desde = cleaned_data.get('fecha_desde')
        fecha_hasta = cleaned_data.get('fecha_hasta')
        
        if fecha_desde and fecha_hasta and fecha_desde > fecha_hasta:
            raise ValidationError('La fecha desde no puede ser mayor que la fecha hasta.')
        
        return cleaned_data
    




   
class CitaMedicaForm(forms.ModelForm):
    class Meta:
        model = CitaMedica
        fields = ['paciente', 'fecha', 'hora_cita', 'estado', 'observaciones']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'}),
            'hora_cita': forms.TimeInput(attrs={'type': 'time'})
        }

class PacienteRegistrationForm(forms.ModelForm):
    class Meta:
        model = PacienteCore
        fields = ['nombre_completo', 'telefono', 'email']
