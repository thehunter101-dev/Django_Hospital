from django.urls import path
from applications.core.views.paciente import paciente_find
from applications.core.views.doctor import DoctorListView, DoctorCreateView, DoctorUpdateView, DoctorDeleteView
from applications.core.views.especialidades import EspecialidadListView, EspecialidadCreateView, EspecialidadUpdateView, EspecialidadDeleteView
from applications.core.views.empleados import EmpleadoListView, EmpleadoCreateView, EmpleadoUpdateView, EmpleadoDeleteView
from applications.core.views.diagnostico import DiagnosticoListView, DiagnosticoDeleteView, DiagnosticoUpdateView, DiagnosticoCreateView



app_name='core' # define un espacio de nombre para la aplicacion
urlpatterns = [
    # Rutas  para vistas relacionadas con Pacientes
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

]