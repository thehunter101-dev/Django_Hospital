from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.db.models import Q
from django.contrib import messages
from django.urls import reverse_lazy

from applications.security.components.mixin_crud import (
    PermissionMixin, ListViewMixin, CreateViewMixin, UpdateViewMixin, DeleteViewMixin
)

from applications.core.models import TipoGasto
from applications.core.forms.tipos_gasto import TipoGastoForm


class TipoGastoListView(PermissionMixin, ListViewMixin, ListView):
    template_name = 'core/tipos_gasto/list.html'
    model = TipoGasto
    context_object_name = 'tipos'
    permission_required = 'view_tipogasto'

    def get_queryset(self):
        q1 = self.request.GET.get('q')
        if q1:
            self.query.add(Q(nombre__icontains=q1), Q.OR)
        return self.model.objects.filter(self.query).order_by('nombre')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('core:tipo_gasto_create')
        context['title'] = 'Listado de Tipos de Gastos'
        context['title1'] = 'Tipos de Gastos'
        return context


class TipoGastoCreateView(PermissionMixin, CreateViewMixin, CreateView):
    model = TipoGasto
    template_name = 'core/tipos_gasto/form.html'
    form_class = TipoGastoForm
    success_url = reverse_lazy('core:tipo_gasto_list')
    permission_required = 'add_tipogasto'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Grabar Tipo de Gasto'
        context['back_url'] = self.success_url
        context['title'] = 'Crear Tipo de Gasto'
        context['title1'] = 'Nuevo Tipo de Gasto'
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f"Tipo de gasto '{self.object.nombre}' creado correctamente.")
        return response


class TipoGastoUpdateView(PermissionMixin, UpdateViewMixin, UpdateView):
    model = TipoGasto
    template_name = 'core/tipos_gasto/form.html'
    form_class = TipoGastoForm
    success_url = reverse_lazy('core:tipo_gasto_list')
    permission_required = 'change_tipogasto'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Actualizar Tipo de Gasto'
        context['back_url'] = self.success_url
        context['title'] = 'Editar Tipo de Gasto'
        context['title1'] = 'Editar Tipo de Gasto'
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f"Tipo de gasto '{self.object.nombre}' actualizado correctamente.")
        return response


class TipoGastoDeleteView(PermissionMixin, DeleteViewMixin, DeleteView):
    model = TipoGasto
    template_name = 'core/tipos_gasto/form.html'
    success_url = reverse_lazy('core:tipo_gasto_list')
    permission_required = 'delete_tipogasto'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Eliminar Tipo de Gasto'
        context['description'] = f"¿Desea eliminar el tipo de gasto: {self.object.nombre}?"
        context['back_url'] = self.success_url
        return context

    def form_valid(self, form):
        nombre = self.object.nombre
        response = super().form_valid(form)
        messages.success(self.request, f"Tipo de gasto '{nombre}' eliminado correctamente.")
        return response
