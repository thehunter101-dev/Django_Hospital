from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.db.models import Q

from applications.security.components.mixin_crud import (
    PermissionMixin, ListViewMixin, CreateViewMixin, UpdateViewMixin, DeleteViewMixin
)
from applications.core.models import Empleado
from applications.core.forms.empleados import EmpleadoForm


class EmpleadoListView(PermissionMixin, ListViewMixin, ListView):
    template_name = 'core/empleados/list.html'
    model = Empleado
    context_object_name = 'empleados'
    permission_required = 'view_empleado'

    def get_queryset(self):
        q = self.request.GET.get('q')
        if q:
            self.query.add(
                Q(nombres__icontains=q) | Q(apellidos__icontains=q) | Q(cedula_ecuatoriana__icontains=q), Q.OR
            )
        return self.model.objects.filter(self.query).order_by('apellidos', 'nombres')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('core:empleado_create')
        return context


class EmpleadoCreateView(PermissionMixin, CreateViewMixin, CreateView):
    model = Empleado
    template_name = 'core/empleados/form.html'
    form_class = EmpleadoForm
    success_url = reverse_lazy('core:empleado_list')
    permission_required = 'add_empleado'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Guardar Empleado'
        context['back_url'] = self.success_url
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f"Empleado '{self.object.nombre_completo}' creado con éxito.")
        return response


class EmpleadoUpdateView(PermissionMixin, UpdateViewMixin, UpdateView):
    model = Empleado
    template_name = 'core/empleados/form.html'
    form_class = EmpleadoForm
    success_url = reverse_lazy('core:empleado_list')
    permission_required = 'change_empleado'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Actualizar Empleado'
        context['back_url'] = self.success_url
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f"Empleado '{self.object.nombre_completo}' actualizado correctamente.")
        return response


class EmpleadoDeleteView(PermissionMixin, DeleteViewMixin, DeleteView):
    model = Empleado
    template_name = 'core/empleados/delate.html'
    success_url = reverse_lazy('core:empleado_list')
    permission_required = 'delete_empleado'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Eliminar Empleado'
        context['description'] = f"¿Desea eliminar al empleado: {self.object.nombre_completo}?"
        context['back_url'] = self.success_url
        return context

    def form_valid(self, form):
        empleado_nombre = self.object.nombre_completo
        response = super().form_valid(form)
        messages.success(self.request, f"Empleado '{empleado_nombre}' eliminado correctamente.")
        return response
