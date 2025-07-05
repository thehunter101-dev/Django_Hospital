from django.urls import path

from applications.doctor.views.atencion_medica import AtencionListView, AtencionCreateView, AtencionUpdateView, \
    AtencionDeleteView


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


]

