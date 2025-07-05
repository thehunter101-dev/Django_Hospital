from django.urls import path

from applications.doctor.views.atencion_medica import AtencionListView, AtencionCreateView, AtencionUpdateView, \
    AtencionDeleteView
from applications.doctor.views.calendario import calendario_dashboard


# from applications.doctor.views.detalle_pago import DetallePagoCreateView, DetallePagoDeleteView, DetallePagoListView, DetallePagoUpdateView

from applications.doctor.views.cita_medica import (
    cita_medica_list,
    cita_medica_create,
    cita_medica_detail,
    cita_medica_update,
    cita_medica_delete,
    cita_medica_change_estado,
    citas_hoy,
    citas_por_fecha
)
from applications.doctor.views.servicios_adicionales import (
    ServiciosAdicionalesListView,
    ServiciosAdicionalesCreateView,
    ServiciosAdicionalesUpdateView,
    ServiciosAdicionalesDeleteView,
)
from applications.doctor.views.citas_medicas import (
    CitaMedicaListView,
    CitaMedicaCreateView,
    CitaMedicaUpdateView,
    CitaMedicaDeleteView,
)



from applications.doctor.views.pago import *
from applications.doctor.views.pago import (
    PagoCreateWithDetallesSPAView,
    htmx_detalle_empty_form,
)
app_name='doctor' # define un espacio de nombre para la aplicacion
urlpatterns = [
    # Rutas  para vistas relacionadas con Doctor
    path('atencion_list/', AtencionListView.as_view(), name="atencion_list"),
    path('atencion_create/', AtencionCreateView.as_view(), name="atencion_create"),
    path('atencion_update/<int:pk>/', AtencionUpdateView.as_view(), name="atencion_update"),
    path('atencion_delete/<int:pk>/', AtencionDeleteView.as_view(), name="atencion_delete"),
    path("pago/nuevo/", PagoCreateWithDetallesSPAView.as_view(), name="pago_nuevo"),
    path("htmx/detalle/empty-form/", htmx_detalle_empty_form, name="htmx_detalle_empty_form"),
        path(
        'servicios-adicionales/',
        ServiciosAdicionalesListView.as_view(),
        name='servicios_adicionales_list'
    ),
    path(
        'servicios-adicionales/crear/',
        ServiciosAdicionalesCreateView.as_view(),
        name='servicios_adicionales_create'
    ),
    path(
        'servicios-adicionales/editar/<int:pk>/',
        ServiciosAdicionalesUpdateView.as_view(),
        name='servicios_adicionales_update'
    ),
    path(
        'servicios-adicionales/eliminar/<int:pk>/',
        ServiciosAdicionalesDeleteView.as_view(),
        name='servicios_adicionales_delete'
    ),
    path('citas/', CitaMedicaListView.as_view(), name='cita_list'),
    path('citas/nueva/', CitaMedicaCreateView.as_view(), name='cita_create'),
    path('citas/<int:pk>/editar/', CitaMedicaUpdateView.as_view(), name='cita_update'),
    path('citas/<int:pk>/eliminar/', CitaMedicaDeleteView.as_view(), name='cita_delete'),

    # path('detalle_pago/', DetallePagoListView.as_view(), name='detalle_pago_list'),
    # path('detalle_pago/create/', DetallePagoCreateView.as_view(), name='detalle_pago_create'),
    # path('detalle_pago/<int:pk>/edit/', DetallePagoUpdateView.as_view(), name='detalle_pago_update'),
    # path('detalle_pago/<int:pk>/delete/', DetallePagoDeleteView.as_view(), name='detalle_pago_delete'),

      # Rutas para citas médicas
    path('citas/', cita_medica_list, name='cita_medica_list'),
    path('citas/crear/', cita_medica_create, name='cita_medica_create'),
    path('citas/<int:pk>/', cita_medica_detail, name='cita_medica_detail'),
    path('citas/<int:pk>/editar/', cita_medica_update, name='cita_medica_update'),
    path('citas/<int:pk>/eliminar/', cita_medica_delete, name='cita_medica_delete'),
    
    # URLs adicionales para citas
    path('citas/<int:pk>/cambiar-estado/', cita_medica_change_estado, name='cita_medica_change_estado'),
    path('citas/hoy/', citas_hoy, name='citas_hoy'),
    path('citas/fecha/<str:fecha>/', citas_por_fecha, name='citas_por_fecha'),
    path('calendario',calendario_dashboard,name = 'calendario'),

]
