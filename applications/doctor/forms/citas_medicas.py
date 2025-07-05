from django import forms
from applications.doctor.models import CitaMedica

class CitaMedicaForm(forms.ModelForm):
    class Meta:
        model = CitaMedica
        fields = ['paciente', 'fecha', 'hora_cita', 'estado', 'observaciones']
        widgets = {
            'paciente': forms.Select(attrs={
                'class': 'form-control',
            }),
            'fecha': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control',
            }),
            'hora_cita': forms.TimeInput(attrs={
                'type': 'time',
                'class': 'form-control',
            }),
            'estado': forms.Select(attrs={
                'class': 'form-control',
            }),
            'observaciones': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Opcional: detalles adicionales o notas de la cita'
            }),
        }
        labels = {
            'paciente': 'Paciente',
            'fecha': 'Fecha de la Cita',
            'hora_cita': 'Hora de la Cita',
            'estado': 'Estado de la Cita',
            'observaciones': 'Observaciones',
        }
        help_texts = {
            'paciente': 'Seleccione el paciente para la cita',
            'fecha': 'Seleccione la fecha para la cita',
            'hora_cita': 'Seleccione la hora para la cita',
            'estado': 'Seleccione el estado actual de la cita',
            'observaciones': 'Notas adicionales sobre la cita (opcional)',
        }
