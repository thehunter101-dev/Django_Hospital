from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.db.models import Q

from applications.security.components.mixin_crud import (
    PermissionMixin, ListViewMixin, CreateViewMixin, UpdateViewMixin, DeleteViewMixin
)
from applications.core.models import Especialidad
from applications.core.forms.especialidades import EspecialidadForm


class EspecialidadListView(PermissionMixin, ListViewMixin, ListView):
    template_name = 'core/especialidades/list.html'
    model = Especialidad
    context_object_name = 'especialidades'
    permission_required = 'view_especialidad'

    def get_queryset(self):
        q = self.request.GET.get('q')
        if q:
            self.query.add(Q(nombre__icontains=q), Q.OR)
        return self.model.objects.filter(self.query).order_by('nombre')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('core:especialidad_create')
        return context


class EspecialidadCreateView(PermissionMixin, CreateViewMixin, CreateView):
    model = Especialidad
    template_name = 'core/especialidades/form.html'
    form_class = EspecialidadForm
    success_url = reverse_lazy('core:especialidad_list')
    permission_required = 'add_especialidad'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Guardar Especialidad'
        context['back_url'] = self.success_url
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f"Especialidad '{self.object.nombre}' creada con éxito.")
        return response


class EspecialidadUpdateView(PermissionMixin, UpdateViewMixin, UpdateView):
    model = Especialidad
    template_name = 'core/especialidades/form.html'
    form_class = EspecialidadForm
    success_url = reverse_lazy('core:especialidad_list')
    permission_required = 'change_especialidad'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Actualizar Especialidad'
        context['back_url'] = self.success_url
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f"Especialidad '{self.object.nombre}' actualizada correctamente.")
        return response


class EspecialidadDeleteView(PermissionMixin, DeleteViewMixin, DeleteView):
    model = Especialidad
    template_name = 'core/especialidades/delate.html'
    success_url = reverse_lazy('core:especialidad_list')
    permission_required = 'delete_especialidad'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Eliminar Especialidad'
        context['description'] = f"¿Desea eliminar la especialidad: {self.object.nombre}?"
        context['back_url'] = self.success_url
        return context

    def form_valid(self, form):
        especialidad_nombre = self.object.nombre
        response = super().form_valid(form)
        messages.success(self.request, f"Especialidad '{especialidad_nombre}' eliminada correctamente.")
        return response
