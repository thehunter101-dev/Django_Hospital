from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.db.models import Q

from applications.security.components.mixin_crud import (
    PermissionMixin, ListViewMixin, CreateViewMixin, UpdateViewMixin, DeleteViewMixin
)
from applications.core.models import Diagnostico
from applications.core.forms.diagnostico import DiagnosticoForm


class DiagnosticoListView(PermissionMixin, ListViewMixin, ListView):
    template_name = 'core/diagnostico/list.html'
    model = Diagnostico
    context_object_name = 'diagnosticos'
    permission_required = 'view_diagnostico'

    def get_queryset(self):
        q = self.request.GET.get('q')
        if q:
            self.query.add(Q(codigo__icontains=q) | Q(descripcion__icontains=q), Q.OR)
        return self.model.objects.filter(self.query).order_by('codigo')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['create_url'] = reverse_lazy('core:diagnostico_create')
        return context


class DiagnosticoCreateView(PermissionMixin, CreateViewMixin, CreateView):
    model = Diagnostico
    template_name = 'core/diagnostico/form.html'
    form_class = DiagnosticoForm
    success_url = reverse_lazy('core:diagnostico_list')
    permission_required = 'add_diagnostico'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Guardar Diagnóstico'
        context['back_url'] = self.success_url
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f"Diagnóstico '{self.object.codigo}' creado correctamente.")
        return response


class DiagnosticoUpdateView(PermissionMixin, UpdateViewMixin, UpdateView):
    model = Diagnostico
    template_name = 'core/diagnostico/form.html'
    form_class = DiagnosticoForm
    success_url = reverse_lazy('core:diagnostico_list')
    permission_required = 'change_diagnostico'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Actualizar Diagnóstico'
        context['back_url'] = self.success_url
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f"Diagnóstico '{self.object.codigo}' actualizado correctamente.")
        return response


class DiagnosticoDeleteView(PermissionMixin, DeleteViewMixin, DeleteView):
    model = Diagnostico
    template_name = 'core/diagnostico/delate.html'
    success_url = reverse_lazy('core:diagnostico_list')
    permission_required = 'delete_diagnostico'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Eliminar Diagnóstico'
        context['description'] = f"¿Desea eliminar el diagnóstico: {self.object.codigo} - {self.object.descripcion}?"
        context['back_url'] = self.success_url
        return context

    def form_valid(self, form):
        diagnostico = f"{self.object.codigo} - {self.object.descripcion}"
        response = super().form_valid(form)
        messages.success(self.request, f"Diagnóstico '{diagnostico}' eliminado correctamente.")
        return response
