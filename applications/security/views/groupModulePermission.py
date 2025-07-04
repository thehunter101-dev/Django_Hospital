from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import Group
from applications.security.models import GroupModulePermission, Module
from applications.security.components.mixin_crud import (
    CreateViewMixin, DeleteViewMixin, ListViewMixin, PermissionMixin, UpdateViewMixin
)
from applications.security.forms.groupModulePermision import GroupModulePermissionForm

# --- SPA/HTMX Main Page ---
class GroupModulePermissionSPAView(PermissionMixin, View):
    permission_required = 'view_groupmodulepermission'
    template_name = 'security/groupsModulePermission/spa.html'

    def get(self, request):
        groups = Group.objects.all().order_by("name")
        context = {
            "groups": groups,
            "title": "Gestión Permisos Grupo-Módulo",
            "title1": "Gestión de Permisos por Grupo y Módulo",
        }
        return render(request, self.template_name, context)

# --- HTMX Partial: Lista de grupos ---
def htmx_group_list(request):
    groups = Group.objects.all().order_by("name")
    return render(request, "security/groupsModulePermission/_group_list.html", {"groups": groups})

# --- HTMX Partial: Lista de módulos por grupo ---
def htmx_module_list(request, group_id):
    group = get_object_or_404(Group, pk=group_id)
    modules = Module.objects.filter(group_permissions__group=group).distinct().order_by("name")
    exist_modules = modules.exists()
    print(str(exist_modules))
    return render(request, "security/groupsModulePermission/_module_list.html", {
        "modules": modules,
        "group": group,
        "exist_modules":exist_modules
    })

# --- HTMX Partial: Permisos por grupo y módulo ---
def htmx_permission_list(request, group_id, module_id):
    group = get_object_or_404(Group, pk=group_id)
    module = get_object_or_404(Module, pk=module_id)
    try:
        gmp = GroupModulePermission.objects.get(group=group, module=module)
        permissions = gmp.permissions.all().order_by("name")
    except GroupModulePermission.DoesNotExist:
        permissions = []
    return render(request, "security/groupsModulePermission/_permission_list.html", {
        "permissions": permissions,
        "group": group,
        "module": module,
    })


# --- CRUD CLASSES SIGUEN IGUAL ---
class GroupModulePermissionListView(PermissionMixin, ListViewMixin, ListView):
    template_name = 'security/groupsModulePermission/list.html'
    model = GroupModulePermission
    context_object_name = 'group_module_permissions'
    permission_required = 'view_groupmodulepermission'

    def get_queryset(self):
        q1 = self.request.GET.get('q')
        if q1:
            self.query.add(Q(group__name__icontains=q1), Q.OR)
            self.query.add(Q(module__name__icontains=q1), Q.OR)
        return self.model.objects.filter(self.query).select_related('group', 'module').order_by('group', 'module')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('security:group_module_permission_create')
        return context

class GroupModulePermissionCreateView(PermissionMixin, CreateViewMixin, CreateView):
    model = GroupModulePermission
    template_name = 'security/groupsModulePermission/form.html'
    form_class = GroupModulePermissionForm
    success_url = reverse_lazy('security:group_module_permission_list')
    permission_required = 'add_groupmodulepermission'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Grabar Permiso'
        context['back_url'] = self.success_url
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        obj = self.object
        messages.success(self.request, f"Permiso para el grupo {obj.group.name} y módulo {obj.module.name} creado correctamente.")
        return response

class GroupModulePermissionUpdateView(PermissionMixin, UpdateViewMixin, UpdateView):
    model = GroupModulePermission
    template_name = 'security/groupsModulePermission/form.html'
    form_class = GroupModulePermissionForm
    success_url = reverse_lazy('security:group_module_permission_list')
    permission_required = 'change_groupmodulepermission'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Actualizar Permiso'
        context['back_url'] = self.success_url
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        obj = self.object
        messages.success(self.request, f"Permiso para el grupo {obj.group.name} y módulo {obj.module.name} actualizado correctamente.")
        return response

class GroupModulePermissionDeleteView(PermissionMixin, DeleteViewMixin, DeleteView):
    model = GroupModulePermission
    template_name = 'core/delete.html'
    success_url = reverse_lazy('security:group_module_permission_list')
    permission_required = 'delete_groupmodulepermission'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Eliminar Permiso'
        context['description'] = f"¿Desea eliminar los permisos del grupo: {self.object.group.name} sobre el módulo: {self.object.module.name}?"
        context['back_url'] = self.success_url
        return context

    def form_valid(self, form):
        obj = self.object
        response = super().form_valid(form)
        messages.success(self.request, f"Permiso del grupo {obj.group.name} para el módulo {obj.module.name} eliminado correctamente.")
        return response


# Peticiones json
