from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.db.models import Q

from applications.security.components.mixin_crud import (
    PermissionMixin, ListViewMixin, CreateViewMixin, UpdateViewMixin, DeleteViewMixin
)
from applications.core.models import GastoMensual
from applications.core.forms.gasto_mensual import GastoMensualForm

class GastoMensualListView(PermissionMixin, ListViewMixin, ListView):
    template_name = 'core/gastos_mensuales/list.html'
    model = GastoMensual
    context_object_name = 'gastos'
    permission_required = 'view_gastomensual'

    def get_queryset(self):
        q = self.request.GET.get('q')
        if q:
            self.query.add(Q(observacion__icontains=q) | Q(tipo_gasto__nombre__icontains=q), Q.OR)
        return self.model.objects.filter(self.query).select_related('tipo_gasto').order_by('-fecha')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['create_url'] = reverse_lazy('core:gasto_create')
        return context


class GastoMensualCreateView(PermissionMixin, CreateViewMixin, CreateView):
    model = GastoMensual
    template_name = 'core/gastos_mensuales/form.html'
    form_class = GastoMensualForm
    success_url = reverse_lazy('core:gasto_list')
    permission_required = 'add_gastomensual'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Registrar Gasto'
        context['back_url'] = self.success_url
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f"Gasto registrado correctamente.")
        return response


class GastoMensualUpdateView(PermissionMixin, UpdateViewMixin, UpdateView):
    model = GastoMensual
    template_name = 'core/gastos_mensuales/form.html'
    form_class = GastoMensualForm
    success_url = reverse_lazy('core:gasto_list')
    permission_required = 'change_gastomensual'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Actualizar Gasto'
        context['back_url'] = self.success_url
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Gasto actualizado correctamente.")
        return response


class GastoMensualDeleteView(PermissionMixin, DeleteViewMixin, DeleteView):
    model = GastoMensual
    template_name = 'core/gastos_mensuales/delate.html'
    success_url = reverse_lazy('core:gasto_list')
    permission_required = 'delete_gastomensual'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Eliminar Gasto'
        context['description'] = f"¿Desea eliminar el gasto de {self.object.valor} en {self.object.tipo_gasto}?"
        context['back_url'] = self.success_url
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Gasto eliminado correctamente.")
        return response
