from django import forms
from applications.doctor.models import DetallePago # Asumiendo que models.py está en el mismo directorio 'doctor'

class DetallePagoForm(forms.ModelForm):
    class Meta:
        model = DetallePago
        fields = [
            'pago',
            'servicio_adicional',
            'cantidad',
            'precio_unitario',
            'descuento_porcentaje',
            'aplica_seguro',
            'valor_seguro',
            'descripcion_seguro',
        ]
        widgets = {
            # Ejemplo de cómo podrías añadir clases para Bootstrap u otros frameworks CSS
            'pago': forms.Select(attrs={'class': 'form-control'}),
            'servicio_adicional': forms.Select(attrs={'class': 'form-control'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control'}),
            'precio_unitario': forms.NumberInput(attrs={'class': 'form-control'}),
            'descuento_porcentaje': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'aplica_seguro': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'valor_seguro': forms.NumberInput(attrs={'class': 'form-control'}),
            'descripcion_seguro': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_descuento_porcentaje(self):
        descuento = self.cleaned_data.get('descuento_porcentaje')
        if descuento is not None and (descuento < 0 or descuento > 100):
            raise forms.ValidationError("El porcentaje de descuento debe estar entre 0 y 100.")
        return descuento

    def clean(self):
        cleaned_data = super().clean()
        aplica_seguro = cleaned_data.get('aplica_seguro')
        valor_seguro = cleaned_data.get('valor_seguro')

        if aplica_seguro and valor_seguro is None:
            self.add_error('valor_seguro', "Si aplica seguro, el valor cubierto por el seguro es obligatorio.")
        
        if not aplica_seguro: # Si no aplica seguro, limpiar valor_seguro y descripcion_seguro
            cleaned_data['valor_seguro'] = None
            cleaned_data['descripcion_seguro'] = ''

        return cleaned_data
