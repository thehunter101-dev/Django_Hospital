from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.db.models import Q
from django.contrib import messages
from django.urls import reverse_lazy

from applications.security.components.mixin_crud import (
    PermissionMixin, ListViewMixin, CreateViewMixin, UpdateViewMixin, DeleteViewMixin
)

from applications.core.models import TipoMedicamento
from applications.core.forms.tipos_medicamento import TipoMedicamentoForm  # Asegúrate que exista este form

class TipoMedicamentoListView(PermissionMixin, ListViewMixin, ListView):
    template_name = 'core/tipos_medicamento/list.html'
    model = TipoMedicamento
    context_object_name = 'tipos'
    permission_required = 'view_tipomedicamento'

    def get_queryset(self):
        q1 = self.request.GET.get('q')
        if q1:
            self.query.add(Q(nombre__icontains=q1), Q.OR)
        return self.model.objects.filter(self.query).order_by('nombre')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('core:tipo_medicamento_create')
        context['title'] = 'Listado de Tipos de Medicamentos'
        context['title1'] = 'Tipos de Medicamentos'
        return context


class TipoMedicamentoCreateView(PermissionMixin, CreateViewMixin, CreateView):
    model = TipoMedicamento
    template_name = 'core/tipos_medicamento/form.html'
    form_class = TipoMedicamentoForm
    success_url = reverse_lazy('core:tipo_medicamento_list')
    permission_required = 'add_tipomedicamento'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Grabar Tipo Medicamento'
        context['back_url'] = self.success_url
        context['title'] = 'Crear Tipo de Medicamento'
        context['title1'] = 'Nuevo Tipo de Medicamento'
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f"Tipo de medicamento '{self.object.nombre}' creado correctamente.")
        return response


class TipoMedicamentoUpdateView(PermissionMixin, UpdateViewMixin, UpdateView):
    model = TipoMedicamento
    template_name = 'core/tipos_medicamento/form.html'
    form_class = TipoMedicamentoForm
    success_url = reverse_lazy('core:tipo_medicamento_list')
    permission_required = 'change_tipomedicamento'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Actualizar Tipo Medicamento'
        context['back_url'] = self.success_url
        context['title'] = 'Editar Tipo de Medicamento'
        context['title1'] = 'Editar Tipo de Medicamento'
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f"Tipo de medicamento '{self.object.nombre}' actualizado correctamente.")
        return response


class TipoMedicamentoDeleteView(PermissionMixin, DeleteViewMixin, DeleteView):
    model = TipoMedicamento
    template_name = 'core/tipos_medicamento/form.html'
    success_url = reverse_lazy('core:tipo_medicamento_list')
    permission_required = 'delete_tipomedicamento'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Eliminar Tipo Medicamento'
        context['description'] = f"¿Desea eliminar el tipo de medicamento: {self.object.nombre}?"
        context['back_url'] = self.success_url
        return context

    def form_valid(self, form):
        nombre = self.object.nombre
        response = super().form_valid(form)
        messages.success(self.request, f"Tipo de medicamento '{nombre}' eliminado correctamente.")
        return response
