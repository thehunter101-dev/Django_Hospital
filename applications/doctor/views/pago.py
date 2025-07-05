from django.forms import modelformset_factory
from applications.doctor.forms.pago import PagoForm, DetallePagoFormSet,DetalleForm
from django.views.generic import View
from django.shortcuts import render, redirect
from django.db import transaction
from applications.doctor.models import DetallePago
from django.template.loader import render_to_string
from django.http import HttpResponse

class PagoCreateWithDetallesSPAView(View):
    template_name = 'doctor/pago/pago_create_form.html'

    def get(self, request):
        pago_form = PagoForm()
        detalle_formset = DetallePagoFormSet(queryset=DetallePago.objects.none())
        return render(request, self.template_name, {
            'pago_form': pago_form,
            'detalle_formset': detalle_formset,
        })

    @transaction.atomic
    def post(self, request):
        pago_form = PagoForm(request.POST, request.FILES)
        detalle_formset = DetallePagoFormSet(request.POST)

        if pago_form.is_valid() and detalle_formset.is_valid():
            pago = pago_form.save()
            detalles = detalle_formset.save(commit=False)
            for detalle in detalles:
                detalle.pago = pago
                detalle.save()
            # eliminar detalles marcados como DELETE
            for d in detalle_formset.deleted_objects:
                d.delete()

            pago.monto_total = sum([d.subtotal for d in pago.detalles.all()])
            pago.save(update_fields=['monto_total'])

            return redirect('doctor:pago_spa')

        return render(request, self.template_name, {
            'pago_form': pago_form,
            'detalle_formset': detalle_formset,
        })

def htmx_detalle_empty_form(request):
    form = DetalleForm(prefix=f"form-{request.GET.get('form_id', 'x')}")
    html = render_to_string("doctor/pago/_detalle_form_inline.html", {"form": form})
    return HttpResponse(html)
