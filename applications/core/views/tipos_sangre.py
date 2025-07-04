from django.contrib import messages
from django.urls import reverse_lazy
from django.db.models import Q
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from applications.security.components.mixin_crud import (CreateViewMixin,DeleteViewMixin,ListViewMixin,PermissionMixin,UpdateViewMixin)
from applications.core.models import TipoSangre
from applications.core.forms.tipos_sangre import TipoSangreForm


class TipoSangreListView(PermissionMixin, ListViewMixin, ListView):
    template_name = 'core/tipos_sangre/list.html'
    model = TipoSangre
    context_object_name = 'tipos_sangre'
    permission_required = 'view_tiposangre'

    def get_queryset(self):
        q1 = self.request.GET.get('q')
        if q1 is not None:
            self.query.add(
                Q(tipo__icontains=q1) | Q(descripcion__icontains=q1), 
                Q.OR
            )
        return self.model.objects.filter(self.query).order_by('id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('tipos_sangre_create')
        return context


class TipoSangreCreateView(PermissionMixin, CreateViewMixin, CreateView):
    model = TipoSangre
    template_name = 'core/tipos_sangre/form.html'
    form_class = TipoSangreForm
    success_url = reverse_lazy('core:tipos_sangre_list')
    permission_required = 'add_tiposangre'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Grabar Tipo de Sangre'
        context['back_url'] = self.success_url
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f"Éxito al crear el tipo de sangre: {self.object.tipo}.")
        return response


class TipoSangreUpdateView(PermissionMixin, UpdateViewMixin, UpdateView):
    model = TipoSangre
    template_name = 'core/tipos_sangre/form.html'
    form_class = TipoSangreForm
    success_url = reverse_lazy('core:tipos_sangre_list')
    permission_required = 'change_tiposangre'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Actualizar Tipo de Sangre'
        context['back_url'] = self.success_url
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f"Éxito al actualizar el tipo de sangre: {self.object.tipo}.")
        return response


class TipoSangreDeleteView(PermissionMixin, DeleteViewMixin, DeleteView):
    model = TipoSangre
    template_name = 'core/tipos_sangre/form.html'
    success_url = reverse_lazy('core:tipos_sangre_list')
    permission_required = 'delete_tiposangre'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Eliminar Tipo de Sangre'
        context['description'] = f"¿Desea eliminar el tipo de sangre: {self.object.tipo}?"
        context['back_url'] = self.success_url
        return context

    def form_valid(self, form):
        tipo_nombre = self.object.tipo
        response = super().form_valid(form)
        messages.success(self.request, f"Éxito al eliminar el tipo de sangre {tipo_nombre}.")
        return response
