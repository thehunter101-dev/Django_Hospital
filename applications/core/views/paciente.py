from django.http import JsonResponse
from django.db.models import Q
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from applications.core.models import Paciente
from applications.core.forms.paciente import PacienteForm
from applications.security.components.mixin_crud import (
    PermissionMixin, ListViewMixin, CreateViewMixin,
    UpdateViewMixin, DeleteViewMixin
)

""" Vista para buscar pacientes mediante AJAX. Por nombres, apellidos, cédula o teléfono. """
@login_required
@require_http_methods(["GET"])
def paciente_find(request):
    try:
        query = request.GET.get('q', '').strip()

        if len(query) < 3:
            return JsonResponse({
                'success': False,
                'message': 'Debe proporcionar al menos 3 caracteres para la búsqueda',
                'pacientes': []
            })

        pacientes_query = Paciente.objects.filter(
            Q(activo=True) & (
                Q(nombres__icontains=query) |
                Q(apellidos__icontains=query) |
                Q(cedula_ecuatoriana__icontains=query) |
                Q(dni__icontains=query) |
                Q(telefono__icontains=query)
            )
        ).select_related('tipo_sangre').prefetch_related(
            'atenciones__diagnostico',
            'atenciones__detalles__medicamento'
        ).order_by('apellidos', 'nombres')[:20]

        pacientes_data = []
        for paciente in pacientes_query:
            edad = paciente.edad
            atenciones = []
            for atencion in paciente.atenciones.all()[:10]:
                detalles = [
                    {
                        'medicamento': d.medicamento.nombre if d.medicamento else None,
                        'cantidad': d.cantidad,
                        'prescripcion': d.prescripcion,
                        'duracion_tratamiento': d.duracion_tratamiento,
                        'frecuencia_diaria': d.frecuencia_diaria,
                    } for d in atencion.detalles.all()
                ]
                diagnosticos = [d.descripcion for d in atencion.diagnostico.all()]
                tipo_consulta = "Chequeo"
                if atencion.es_control:
                    tipo_consulta = "Control"
                elif "urgencia" in atencion.motivo_consulta.lower() or "dolor" in atencion.motivo_consulta.lower():
                    tipo_consulta = "Urgencia"

                atenciones.append({
                    'id': atencion.id,
                    'fecha_atencion': atencion.fecha_atencion.isoformat(),
                    'tipo_consulta': tipo_consulta,
                    'presion_arterial': atencion.presion_arterial,
                    'pulso': atencion.pulso,
                    'temperatura': float(atencion.temperatura) if atencion.temperatura else None,
                    'frecuencia_respiratoria': atencion.frecuencia_respiratoria,
                    'saturacion_oxigeno': float(atencion.saturacion_oxigeno) if atencion.saturacion_oxigeno else None,
                    'peso': float(atencion.peso) if atencion.peso else None,
                    'altura': float(atencion.altura) if atencion.altura else None,
                    'imc': atencion.calcular_imc,
                    'motivo_consulta': atencion.motivo_consulta,
                    'sintomas': atencion.sintomas,
                    'tratamiento': atencion.tratamiento,
                    'diagnosticos': diagnosticos,
                    'examen_fisico': atencion.examen_fisico,
                    'examenes_enviados': atencion.examenes_enviados,
                    'comentario_adicional': atencion.comentario_adicional,
                    'es_control': atencion.es_control,
                    'prescripciones': detalles
                })

            pacientes_data.append({
                'id': paciente.id,
                'nombres': paciente.nombres,
                'apellidos': paciente.apellidos,
                'cedula_ecuatoriana': paciente.cedula_ecuatoriana,
                'dni': paciente.dni,
                'fecha_nacimiento': paciente.fecha_nacimiento.isoformat() if paciente.fecha_nacimiento else None,
                'edad': edad,
                'telefono': paciente.telefono,
                'email': paciente.email,
                'sexo': paciente.sexo,
                'estado_civil': paciente.estado_civil,
                'direccion': paciente.direccion,
                'latitud': float(paciente.latitud) if paciente.latitud else None,
                'longitud': float(paciente.longitud) if paciente.longitud else None,
                'tipo_sangre': paciente.tipo_sangre.tipo if paciente.tipo_sangre else None,
                'foto_url': paciente.get_image,
                'antecedentes_personales': paciente.antecedentes_personales,
                'antecedentes_quirurgicos': paciente.antecedentes_quirurgicos,
                'antecedentes_familiares': paciente.antecedentes_familiares,
                'alergias': paciente.alergias,
                'medicamentos_actuales': paciente.medicamentos_actuales,
                'habitos_toxicos': paciente.habitos_toxicos,
                'vacunas': paciente.vacunas,
                'antecedentes_gineco_obstetricos': paciente.antecedentes_gineco_obstetricos,
                'atenciones': atenciones,
                'total_atenciones': paciente.atenciones.count()
            })

        return JsonResponse({
            'success': True,
            'pacientes': pacientes_data,
            'total': len(pacientes_data),
            'query': query
        })

    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Error en la búsqueda: {str(e)}',
            'pacientes': []
        }, status=500)


# CRUD Paciente

class PacienteListView(PermissionMixin, ListViewMixin, ListView):
    model = Paciente
    template_name = 'core/pacientes/list.html'
    context_object_name = 'pacientes'
    permission_required = 'view_paciente'

    def get_queryset(self):
        q = self.request.GET.get('q')
        if q:
            self.query.add(Q(nombres__icontains=q) | Q(apellidos__icontains=q), Q.OR)
        return self.model.objects.filter(self.query).order_by('apellidos')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['create_url'] = reverse_lazy('core:paciente_create')
        return context


class PacienteCreateView(PermissionMixin, CreateViewMixin, CreateView):
    model = Paciente
    template_name = 'core/pacientes/form.html'
    form_class = PacienteForm
    success_url = reverse_lazy('core:paciente_list')
    permission_required = 'add_paciente'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Registrar Paciente'
        context['back_url'] = self.success_url
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f"Paciente '{self.object.nombre_completo}' registrado con éxito.")
        return response


class PacienteUpdateView(PermissionMixin, UpdateViewMixin, UpdateView):
    model = Paciente
    template_name = 'core/pacientes/form.html'
    form_class = PacienteForm
    success_url = reverse_lazy('core:paciente_list')
    permission_required = 'change_paciente'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Actualizar Paciente'
        context['back_url'] = self.success_url
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f"Paciente '{self.object.nombre_completo}' actualizado correctamente.")
        return response


class PacienteDeleteView(PermissionMixin, DeleteViewMixin, DeleteView):
    model = Paciente
    template_name = 'core/pacientes/delate.html'
    success_url = reverse_lazy('core:paciente_list')
    permission_required = 'delete_paciente'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Eliminar Paciente'
        context['description'] = f"¿Desea eliminar al paciente: {self.object.nombre_completo}?"
        context['back_url'] = self.success_url
        return context

    def form_valid(self, form):
        paciente = self.object.nombre_completo
        response = super().form_valid(form)
        messages.success(self.request, f"Paciente '{paciente}' eliminado correctamente.")
        return response
