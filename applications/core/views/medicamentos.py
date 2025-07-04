from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.db.models import Q

from applications.core.models import Medicamento
from applications.core.forms.medicamentos import MedicamentoForm  # Asegúrate de tener este formulario
from applications.security.components.mixin_crud import (
    PermissionMixin, ListViewMixin, CreateViewMixin, UpdateViewMixin, DeleteViewMixin
)


class MedicamentoListView(PermissionMixin, ListViewMixin, ListView):
    model = Medicamento
    template_name = 'core/medicamentos/list.html'
    context_object_name = 'medicamentos'
    permission_required = 'view_medicamento'

    def get_queryset(self):
        q1 = self.request.GET.get('q')
        if q1:
            self.query.add(Q(nombre__icontains=q1) | Q(descripcion__icontains=q1), Q.OR)
        return self.model.objects.filter(self.query).order_by('nombre')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('core:medicamento_create')
        context['title1'] = "Listado de Medicamentos"
        context['title'] = "Medicamentos"
        return context


class MedicamentoCreateView(PermissionMixin, CreateViewMixin, CreateView):
    model = Medicamento
    form_class = MedicamentoForm
    template_name = 'core/medicamentos/form.html'
    success_url = reverse_lazy('core:medicamento_list')
    permission_required = 'add_medicamento'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Guardar Medicamento'
        context['back_url'] = self.success_url
        context['title'] = 'Nuevo Medicamento'
        context['title1'] = 'Registrar Medicamento'
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f"Medicamento '{self.object.nombre}' creado exitosamente.")
        return response


class MedicamentoUpdateView(PermissionMixin, UpdateViewMixin, UpdateView):
    model = Medicamento
    form_class = MedicamentoForm
    template_name = 'core/medicamentos/form.html'
    success_url = reverse_lazy('core:medicamento_list')
    permission_required = 'change_medicamento'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Actualizar Medicamento'
        context['back_url'] = self.success_url
        context['title'] = 'Editar Medicamento'
        context['title1'] = 'Actualizar Medicamento'
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f"Medicamento '{self.object.nombre}' actualizado exitosamente.")
        return response


class MedicamentoDeleteView(PermissionMixin, DeleteViewMixin, DeleteView):
    model = Medicamento
    template_name = 'core/medicamentos/form.html'
    success_url = reverse_lazy('core:medicamento_list')
    permission_required = 'delete_medicamento'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Eliminar Medicamento'
        context['description'] = f"¿Desea eliminar el medicamento: {self.object.nombre}?"
        context['back_url'] = self.success_url
        return context

    def form_valid(self, form):
        nombre = self.object.nombre
        response = super().form_valid(form)
        messages.success(self.request, f"Medicamento '{nombre}' eliminado correctamente.")
        return response
