from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.db.models import Q

from applications.security.components.mixin_crud import (PermissionMixin,ListViewMixin,CreateViewMixin,UpdateViewMixin,DeleteViewMixin)

from applications.core.models import MarcaMedicamento
from applications.core.forms.marca_medicamento import MarcaMedicamentoForm


class MarcaMedicamentoListView(PermissionMixin, ListViewMixin, ListView):
    model = MarcaMedicamento
    template_name = 'core/marca_medicamento/list.html'
    context_object_name = 'marcas'
    permission_required = 'view_marcamedicamento'

    def get_queryset(self):
        q = self.request.GET.get('q')
        if q is not None:
            self.query.add(Q(nombre__icontains=q), Q.OR)
            self.query.add(Q(descripcion__icontains=q), Q.OR)
        return self.model.objects.filter(self.query).order_by('id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('core:marca_medicamento_create')
        return context


class MarcaMedicamentoCreateView(PermissionMixin, CreateViewMixin, CreateView):
    model = MarcaMedicamento
    template_name = 'core/marca_medicamento/form.html'
    form_class = MarcaMedicamentoForm
    success_url = reverse_lazy('core:marca_medicamento_list')
    permission_required = 'add_marcamedicamento'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Grabar Marca de Medicamento'
        context['back_url'] = self.success_url
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f"Éxito al crear la marca de medicamento: {self.object.nombre}.")
        return response


class MarcaMedicamentoUpdateView(PermissionMixin, UpdateViewMixin, UpdateView):
    model = MarcaMedicamento
    template_name = 'core/marca_medicamento/form.html'
    form_class = MarcaMedicamentoForm
    success_url = reverse_lazy('core:marca_medicamento_list')
    permission_required = 'change_marcamedicamento'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Actualizar Marca de Medicamento'
        context['back_url'] = self.success_url
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f"Éxito al actualizar la marca de medicamento: {self.object.nombre}.")
        return response


class MarcaMedicamentoDeleteView(PermissionMixin, DeleteViewMixin, DeleteView):
    model = MarcaMedicamento
    template_name = 'core/marca_medicamento/form.html'
    success_url = reverse_lazy('core:marca_medicamento_list')
    permission_required = 'delete_marcamedicamento'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Eliminar Marca de Medicamento'
        context['description'] = f"¿Desea eliminar la marca de medicamento: {self.object.nombre}?"
        context['back_url'] = self.success_url
        return context

    def form_valid(self, form):
        marca_nombre = self.object.nombre
        response = super().form_valid(form)
        messages.success(self.request, f"Éxito al eliminar la marca de medicamento: {marca_nombre}.")
        return response
