
from django.urls import path

from applications.security.views.auth import signin, signout
from applications.security.views.menu import MenuCreateView, MenuDeleteView, MenuListView, MenuUpdateView
from applications.security.views.module import ModuleCreateView, ModuleDeleteView, ModuleListView, ModuleUpdateView
from applications.security.views.group import GroupListView, GroupCreateView, GroupUpdateView, GroupDeleteView
from applications.security.views.groupModulePermission import GroupModulePermissionHTMXCreateView, GroupModulePermissionHTMXDeleteView, GroupModulePermissionHTMXEditView, htmx_group_list, GroupModulePermissionSPAView, GroupModulePermissionCreateView,GroupModulePermissionListView, GroupModulePermissionUpdateView, GroupModulePermissionDeleteView, htmx_module_list, htmx_permission_list
app_name='security' # define un espacio de nombre para la aplicacion
urlpatterns = [

  # rutas de modulos
  path('module_list/',ModuleListView.as_view() ,name="module_list"),
  path('module_create/', ModuleCreateView.as_view(),name="module_create"),
  path('module_update/<int:pk>/', ModuleUpdateView.as_view(),name='module_update'),
  path('module_delete/<int:pk>/', ModuleDeleteView.as_view(),name='module_delete'),

# rutas de menus
  path('menu_list/',MenuListView.as_view() ,name="menu_list"),
  path('menu_create/', MenuCreateView.as_view(),name="menu_create"),
  path('menu_update/<int:pk>/', MenuUpdateView.as_view(),name='menu_update'),
  path('menu_delete/<int:pk>/', MenuDeleteView.as_view(),name='menu_delete'),

  path('group_list/', GroupListView.as_view(), name="group_list"),
  path('group_create/', GroupCreateView.as_view(), name="group_create"),
  path('group_update/<int:pk>/', GroupUpdateView.as_view(), name="group_update"),
  path('group_delete/<int:pk>/', GroupDeleteView.as_view(), name="group_delete"),

  path('group_module_permission_list/', GroupModulePermissionSPAView.as_view(), name="group_module_permission_list"),

  path('htmx/gmp/edit/<int:pk>/', GroupModulePermissionHTMXEditView.as_view(), name='gmp_edit'),
  path('htmx/gmp/delete/<int:pk>/', GroupModulePermissionHTMXDeleteView.as_view(), name='gmp_delete'),

  path('gmp_module_list/<int:group_id>',htmx_module_list, name="gmp_modules_list"),
  path('gmp_permission_list/<int:group_id>/<int:module_id>/permission',htmx_permission_list, name="gmp_permission_list"),
  path('group_module_permission_create/', GroupModulePermissionCreateView.as_view(), name="group_module_permission_create"),
  path('group_module_permission_update/<int:pk>/', GroupModulePermissionUpdateView.as_view(), name="group_module_permission_update"),
  path('group_module_permission_delete/<int:pk>/', GroupModulePermissionDeleteView.as_view(), name="group_module_permission_delete"),
  path('htmx/gmp/create/<int:group_id>/<int:module_id>/', GroupModulePermissionHTMXCreateView.as_view(), name='gmp_create_htmx'),

  # rutas de autenticacion
  path('logout/', signout, name='signout'),
  path('signin/', signin, name='signin'),
  #path('signup/', signup, name='signup'),

]
