from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.db.models import Q
from applications.security.components.mixin_crud import CreateViewMixin, DeleteViewMixin, ListViewMixin, PermissionMixin, UpdateViewMixin
from applications.doctor.models import CitaMedica
from applications.doctor.forms.citas_medicas import CitaMedicaForm  # Asumo que tienes este formulario creado

class CitaMedicaListView(PermissionMixin, ListViewMixin, ListView):
    template_name = 'doctor/citas_medicas/list.html'
    model = CitaMedica
    context_object_name = 'citas'
    permission_required = 'view_citamedica'

    def get_queryset(self):
        q1 = self.request.GET.get('q')
        if q1 is not None:
            self.query.add(
                Q(paciente__nombre_completo__icontains=q1) |
                Q(estado__icontains=q1) |
                Q(observaciones__icontains=q1),
                Q.OR
            )
        return self.model.objects.filter(self.query).order_by('fecha', 'hora_cita')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('doctor:cita_create')
        return context


class CitaMedicaCreateView(PermissionMixin, CreateViewMixin, CreateView):
    model = CitaMedica
    template_name = 'doctor/citas_medicas/form.html'
    form_class = CitaMedicaForm
    success_url = reverse_lazy('doctor:cita_list')
    permission_required = 'add_citamedica'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Agendar Cita Médica'
        context['back_url'] = self.success_url
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        cita = self.object
        messages.success(self.request, f"Éxito al agendar la cita para {cita.paciente.nombre_completo} el {cita.fecha} a las {cita.hora_cita}.")
        return response


class CitaMedicaUpdateView(PermissionMixin, UpdateViewMixin, UpdateView):
    model = CitaMedica
    template_name = 'doctor/citas_medicas/form.html'
    form_class = CitaMedicaForm
    success_url = reverse_lazy('doctor:cita_list')
    permission_required = 'change_citamedica'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Actualizar Cita Médica'
        context['back_url'] = self.success_url
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        cita = self.object
        messages.success(self.request, f"Éxito al actualizar la cita para {cita.paciente.nombre_completo} el {cita.fecha} a las {cita.hora_cita}.")
        return response


class CitaMedicaDeleteView(PermissionMixin, DeleteViewMixin, DeleteView):
    model = CitaMedica
    template_name = 'core/delete.html'
    success_url = reverse_lazy('doctor:cita_list')
    permission_required = 'delete_citamedica'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Eliminar Cita Médica'
        context['description'] = f"¿Desea eliminar la cita de {self.object.paciente.nombre_completo} programada para el {self.object.fecha} a las {self.object.hora_cita}?"
        context['back_url'] = self.success_url
        return context

    def form_valid(self, form):
        cita_info = f"{self.object.paciente.nombre_completo} el {self.object.fecha} a las {self.object.hora_cita}"
        response = super().form_valid(form)
        messages.success(self.request, f"Éxito al eliminar la cita médica de {cita_info}.")
        return response
