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
from applications.core.views.doctor import DoctorListView, DoctorCreateView, DoctorUpdateView, DoctorDeleteView
from applications.core.views.especialidades import EspecialidadListView, EspecialidadCreateView, EspecialidadUpdateView, EspecialidadDeleteView
from applications.core.views.empleados import EmpleadoListView, EmpleadoCreateView, EmpleadoUpdateView, EmpleadoDeleteView
from applications.core.views.diagnostico import DiagnosticoListView, DiagnosticoDeleteView, DiagnosticoUpdateView, DiagnosticoCreateView
from applications.core.views.gasto_mensual import GastoMensualListView,GastoMensualCreateView,GastoMensualUpdateView,GastoMensualDeleteView
from applications.core.views.paciente import PacienteListView, PacienteCreateView, PacienteUpdateView, PacienteDeleteView



app_name = 'core'

urlpatterns = [
    
    path('paciente_find/', paciente_find, name="paciente_find"),
    path('doctores/', DoctorListView.as_view(), name='doctor_list'),
    path('doctores/nuevo/', DoctorCreateView.as_view(), name='doctor_create'),
    path('doctores/editar/<int:pk>/', DoctorUpdateView.as_view(), name='doctor_update'),
    path('doctores/eliminar/<int:pk>/', DoctorDeleteView.as_view(), name='doctor_delete'),
    path('especialidades/', EspecialidadListView.as_view(), name='especialidad_list'),
    path('especialidades/nueva/', EspecialidadCreateView.as_view(), name='especialidad_create'),
    path('especialidades/editar/<int:pk>/', EspecialidadUpdateView.as_view(), name='especialidad_update'),
    path('especialidades/eliminar/<int:pk>/', EspecialidadDeleteView.as_view(), name='especialidad_delete'),
    path('empleados/', EmpleadoListView.as_view(), name='empleado_list'),
    path('empleados/nuevo/', EmpleadoCreateView.as_view(), name='empleado_create'),
    path('empleados/editar/<int:pk>/', EmpleadoUpdateView.as_view(), name='empleado_update'),
    path('empleados/eliminar/<int:pk>/', EmpleadoDeleteView.as_view(), name='empleado_delete'),
    path('diagnosticos/', DiagnosticoListView.as_view(), name='diagnostico_list'),
    path('diagnosticos/nuevo/', DiagnosticoCreateView.as_view(), name='diagnostico_create'),
    path('diagnosticos/editar/<int:pk>/', DiagnosticoUpdateView.as_view(), name='diagnostico_update'),
    path('diagnosticos/eliminar/<int:pk>/', DiagnosticoDeleteView.as_view(), name='diagnostico_delete'),
    path('gastos/', GastoMensualListView.as_view(), name='gasto_list'),
    path('gastos/crear/', GastoMensualCreateView.as_view(), name='gasto_create'),
    path('gastos/<int:pk>/editar/', GastoMensualUpdateView.as_view(), name='gasto_update'),
    path('gastos/<int:pk>/eliminar/', GastoMensualDeleteView.as_view(), name='gasto_delete'),
    path('pacientes/', PacienteListView.as_view(), name='paciente_list'),
    path('pacientes/crear/', PacienteCreateView.as_view(), name='paciente_create'),
    path('pacientes/<int:pk>/editar/', PacienteUpdateView.as_view(), name='paciente_update'),
    path('pacientes/<int:pk>/eliminar/', PacienteDeleteView.as_view(), name='paciente_delete'),

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


