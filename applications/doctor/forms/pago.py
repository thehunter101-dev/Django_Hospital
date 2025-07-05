from django import forms
from django.forms import modelformset_factory
from applications.doctor.models import Pago, DetallePago
from django.forms import modelform_factory


class PagoForm(forms.ModelForm):
    class Meta:
        model = Pago
        fields = [
            'atencion', 'metodo_pago', 'nombre_pagador', 'referencia_externa',
            'evidencia_pago', 'observaciones'
        ]
        widgets = {
            'observaciones': forms.Textarea(attrs={'rows': 3}),
        }


class DetallePagoForm(forms.ModelForm):
    class Meta:
        model = DetallePago
        fields = [
            'servicio_adicional', 'cantidad', 'precio_unitario',
            'descuento_porcentaje', 'aplica_seguro', 'valor_seguro',
            'descripcion_seguro'
        ]
        widgets = {
            'descripcion_seguro': forms.TextInput(attrs={'placeholder': 'Ej: Seguro Médico XYZ'}),
        }


DetallePagoFormSet = modelformset_factory(
    DetallePago,
    form=DetallePagoForm,  # Usa tu form personalizado
    extra=1,                # Puedes cambiar a 0 si prefieres que no aparezca ninguno al inicio
    can_delete=True         # Permite eliminar detalles
)


DetalleForm = modelform_factory(
    DetallePago,
    fields=[
        'servicio_adicional', 'cantidad', 'precio_unitario',
        'descuento_porcentaje', 'aplica_seguro', 'valor_seguro', 'descripcion_seguro'
    ]
)
