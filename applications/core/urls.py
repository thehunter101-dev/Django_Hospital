from django.urls import path
from applications.core.views.tipos_sangre import (
    TipoSangreListView,TipoSangreCreateView,TipoSangreUpdateView,TipoSangreDeleteView)
from applications.core.views.medicamentos import (
    MedicamentoListView,MedicamentoCreateView,MedicamentoUpdateView,MedicamentoDeleteView,)
from applications.core.views.paciente import paciente_find

app_name='core' # define un espacio de nombre para la aplicacion

urlpatterns = [
    
    path('paciente_find/', paciente_find, name="paciente_find"),
    path('tipos_sangre', TipoSangreListView.as_view(), name='tipos_sangre_list'),
    path('tipos_sangre_crear/', TipoSangreCreateView.as_view(), name='tipos_sangre_create'),
    path('tipos_sangre_editar/<int:pk>/', TipoSangreUpdateView.as_view(), name='tipos_sangre_update'),
    path('tipos_sangre_eliminar/<int:pk>/', TipoSangreDeleteView.as_view(), name='tipos_sangre_delete'),
    
    path('medicamentos', MedicamentoListView.as_view(), name='medicamento_list'),
    path('medicamentos/crear/', MedicamentoCreateView.as_view(), name='medicamento_create'),
    path('medicamentos/editar/<int:pk>/', MedicamentoUpdateView.as_view(), name='medicamento_update'),
    path('medicamentos/eliminar/<int:pk>/', MedicamentoDeleteView.as_view(), name='medicamento_delete'),
]

