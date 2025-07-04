from django.urls import path
from applications.core.views.tipos_sangre import (
    TipoSangreListView, TipoSangreCreateView, TipoSangreUpdateView, TipoSangreDeleteView
)
from applications.core.views.medicamentos import (
    MedicamentoListView, MedicamentoCreateView, MedicamentoUpdateView, MedicamentoDeleteView,
)
from applications.core.views.tipos_medicamento import (
    TipoMedicamentoListView, TipoMedicamentoCreateView, TipoMedicamentoUpdateView, TipoMedicamentoDeleteView
)
from applications.core.views.marca_medicamento import (
    MarcaMedicamentoListView, MarcaMedicamentoCreateView, MarcaMedicamentoUpdateView, MarcaMedicamentoDeleteView
)
from applications.core.views.cargos import (
    CargoListView, CargoCreateView, CargoUpdateView, CargoDeleteView
)
from applications.core.views.tipos_gasto import (
    TipoGastoListView, TipoGastoCreateView, TipoGastoUpdateView, TipoGastoDeleteView
)
from applications.core.views.paciente import paciente_find

app_name = 'core'

urlpatterns = [
    
    path('paciente_find/', paciente_find, name="paciente_find"),

    # Tipos de sangre
    path('tipos_sangre', TipoSangreListView.as_view(), name='tipos_sangre_list'),
    path('tipos_sangre_crear/', TipoSangreCreateView.as_view(), name='tipos_sangre_create'),
    path('tipos_sangre_editar/<int:pk>/', TipoSangreUpdateView.as_view(), name='tipos_sangre_update'),
    path('tipos_sangre_eliminar/<int:pk>/', TipoSangreDeleteView.as_view(), name='tipos_sangre_delete'),

    # Medicamentos
    path('medicamentos', MedicamentoListView.as_view(), name='medicamento_list'),
    path('medicamentos/crear/', MedicamentoCreateView.as_view(), name='medicamento_create'),
    path('medicamentos/editar/<int:pk>/', MedicamentoUpdateView.as_view(), name='medicamento_update'),
    path('medicamentos/eliminar/<int:pk>/', MedicamentoDeleteView.as_view(), name='medicamento_delete'),

    # Tipos de medicamentos
    path('tipos_medicamento', TipoMedicamentoListView.as_view(), name='tipo_medicamento_list'),
    path('tipos_medicamento/crear/', TipoMedicamentoCreateView.as_view(), name='tipo_medicamento_create'),
    path('tipos_medicamento/editar/<int:pk>/', TipoMedicamentoUpdateView.as_view(), name='tipo_medicamento_update'),
    path('tipos_medicamento/eliminar/<int:pk>/', TipoMedicamentoDeleteView.as_view(), name='tipo_medicamento_delete'),
    
    #MArcas Medicamentos
    path('marca/', MarcaMedicamentoListView.as_view(), name='marca_medicamento_list'),
    path('marca/create/', MarcaMedicamentoCreateView.as_view(), name='marca_medicamento_create'),
    path('marca/<int:pk>/update/', MarcaMedicamentoUpdateView.as_view(), name='marca_medicamento_update'),
    path('marca/<int:pk>/delete/', MarcaMedicamentoDeleteView.as_view(), name='marca_medicamento_delete'),
    
    #cargos
    path('cargos/', CargoListView.as_view(), name='cargo_list'),
    path('cargos/create/', CargoCreateView.as_view(), name='cargo_create'),
    path('cargos/<int:pk>/update/', CargoUpdateView.as_view(), name='cargo_update'),
    path('cargos/<int:pk>/delete/', CargoDeleteView.as_view(), name='cargo_delete'),
    
    #tipos de gasto
    path('tipos_gasto/', TipoGastoListView.as_view(), name='tipo_gasto_list'),
    path('tipos_gasto/create/', TipoGastoCreateView.as_view(), name='tipo_gasto_create'),
    path('tipos_gasto/<int:pk>/update/', TipoGastoUpdateView.as_view(), name='tipo_gasto_update'),
    path('tipos_gasto/<int:pk>/delete/', TipoGastoDeleteView.as_view(), name='tipo_gasto_delete'),

]


