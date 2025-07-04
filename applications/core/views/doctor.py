from django.contrib import messages
from django.urls import reverse_lazy
from applications.security.components.mixin_crud import CreateViewMixin, DeleteViewMixin, ListViewMixin, PermissionMixin, UpdateViewMixin
from applications.core.forms.doctor import DoctorForm
from applications.core.models import Doctor
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.db.models import Q


class DoctorListView(PermissionMixin, ListViewMixin, ListView):
    template_name = 'core/doctor/list.html'
    model = Doctor
    context_object_name = 'doctores'
    permission_required = 'view_doctor'

    def get_queryset(self):
        q = self.request.GET.get('q')
        if q:
            self.query.add(
                Q(nombres__icontains=q) | Q(apellidos__icontains=q) | Q(ruc__icontains=q) | Q(codigo_unico_doctor__icontains=q),
                Q.OR
            )
        return self.model.objects.filter(self.query).order_by('apellidos', 'nombres')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('core:doctor_create')
        return context


class DoctorCreateView(PermissionMixin, CreateViewMixin, CreateView):
    model = Doctor
    template_name = 'core/doctor/form.html'
    form_class = DoctorForm
    success_url = reverse_lazy('core:doctor_list')
    permission_required = 'add_doctor'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['grabar'] = 'Grabar Doctor'
        context['back_url'] = self.success_url
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        doctor = self.object
        messages.success(self.request, f"Éxito al crear el doctor {doctor.nombre_completo}.")
        return response


class DoctorUpdateView(PermissionMixin, UpdateViewMixin, UpdateView):
    model = Doctor
    template_name = 'templates/core/doctor/form.html'
    form_class = DoctorForm
    success_url = reverse_lazy('core:doctor_list')
    permission_required = 'change_doctor'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['grabar'] = 'Actualizar Doctor'
        context['back_url'] = self.success_url
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        doctor = self.object
        messages.success(self.request, f"Éxito al actualizar el doctor {doctor.nombre_completo}.")
        return response


class DoctorDeleteView(PermissionMixin, DeleteViewMixin, DeleteView):
    model = Doctor
    template_name = 'core/doctor/confirm_delete.html'
    success_url = reverse_lazy('core:doctor_list')
    permission_required = 'delete_doctor'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['grabar'] = 'Eliminar Doctor'
        context['description'] = f"¿Desea eliminar el doctor: {self.object.nombre_completo}?"
        context['back_url'] = self.success_url
        return context

    def form_valid(self, form):
        doctor_name = self.object.nombre_completo
        response = super().form_valid(form)
        messages.success(self.request, f"Éxito al eliminar lógicamente el doctor {doctor_name}.")
        return response
