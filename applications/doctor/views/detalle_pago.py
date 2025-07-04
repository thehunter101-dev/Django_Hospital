"""
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.db.models import Sum # Para agregar en DeleteView
from django.http import HttpResponseRedirect

# Asumiendo que models.py y forms.py están en el mismo directorio 'doctor'
from applications.doctor.models import DetallePago, Pago 
# from applications.doctor.forms import DetallePagoForm

from decimal import Decimal

class DetallePagoListView(ListView):
    model = DetallePago
    template_name = 'clinica/detalle_pago/list.html'
    context_object_name = 'detalles_pago' 
    paginate_by = 10 # Opcional: añadir paginación

    def get_queryset(self):
        # Opcional: puedes ordenar o filtrar aquí si es necesario
        return DetallePago.objects.select_related('pago', 'servicio_adicional').order_by('-id')


class DetallePagoCreateView(CreateView):
    model = DetallePago
    form_class = DetallePagoForm
    template_name = 'clinica/detalle_pago/form.html'
    
    def get_success_url(self):
        # Redirigir a la lista o al detalle del pago padre, por ejemplo
        return reverse_lazy('doctor:detalle_pago_list') 

    def form_valid(self, form):
        # El subtotal se calcula en el save() del modelo DetallePago
        self.object = form.save()
        self.object.actualizar_total_pago() # Actualiza el Pago asociado
        return HttpResponseRedirect(self.get_success_url())

class DetallePagoUpdateView(UpdateView):
    model = DetallePago
    form_class = DetallePagoForm
    template_name = 'clinica/detalle_pago/form.html'

    def get_success_url(self):
        return reverse_lazy('doctor:detalle_pago_list')

    def form_valid(self, form):
        self.object = form.save()
        self.object.actualizar_total_pago() # Actualiza el Pago asociado
        return HttpResponseRedirect(self.get_success_url())

class DetallePagoDeleteView(DeleteView):
    model = DetallePago
    template_name = 'clinica/detalle_pago/form.html' # Usando form.html para confirmación
    
    def get_success_url(self):
        return reverse_lazy('doctor:detalle_pago_list')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        pago_asociado = self.object.pago # Guardar referencia al pago antes de eliminar
        
        # Llama al método delete() de la superclase (que elimina el objeto)
        response = super().delete(request, *args, **kwargs) 
        
        # Actualizar el monto_total del Pago asociado después de eliminar el detalle
        if pago_asociado:
            # Recalcular el total del pago sumando los subtotales de los detalles restantes
            nuevos_detalles = DetallePago.objects.filter(pago=pago_asociado)
            nuevo_total = nuevos_detalles.aggregate(total=Sum('subtotal'))['total'] or Decimal('0.00')
            pago_asociado.monto_total = round(nuevo_total, 2)
            pago_asociado.save(update_fields=['monto_total'])
            
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # 'object' ya está en el contexto por DeleteView
        # context['view'] = self # Para acceder a view.__class__.__name__ en la plantilla si es necesario
        return context
"""
