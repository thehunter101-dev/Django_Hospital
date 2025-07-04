from decimal import Decimal
from django.utils import timezone
from django.db import models
from applications.doctor.utils.cita_medica import EstadoCitaChoices # Asumo que este path es correcto
from applications.doctor.utils.doctor import DiaSemanaChoices     # Asumo que este path es correcto
from applications.doctor.utils.pago import MetodoPagoChoices, EstadoPagoChoices # Asumo que este path es correcto
from django.contrib.auth.models import User
from django.conf import settings  # ← Añade esto al inicio del archivo

# Placeholder para las clases de choices si no existen en los paths asumidos
# Solo para que el linter no se queje. Debes asegurarte que los imports originales sean correctos.
if not hasattr(EstadoCitaChoices, 'choices'):
    class EstadoCitaChoices(models.TextChoices):
        PENDIENTE = 'PENDIENTE', 'Pendiente'
        CONFIRMADA = 'CONFIRMADA', 'Confirmada'
        CANCELADA = 'CANCELADA', 'Cancelada'
        REALIZADA = 'REALIZADA', 'Realizada'

if not hasattr(DiaSemanaChoices, 'choices'):
    class DiaSemanaChoices(models.TextChoices):
        LUNES = 'LUNES', 'Lunes'
        MARTES = 'MARTES', 'Martes'
        MIERCOLES = 'MIERCOLES', 'Miércoles'
        JUEVES = 'JUEVES', 'Jueves'
        VIERNES = 'VIERNES', 'Viernes'
        SABADO = 'SABADO', 'Sábado'
        DOMINGO = 'DOMINGO', 'Domingo'

if not hasattr(MetodoPagoChoices, 'choices'):
    class MetodoPagoChoices(models.TextChoices):
        EFECTIVO = 'EFECTIVO', 'Efectivo'
        TARJETA = 'TARJETA', 'Tarjeta'
        TRANSFERENCIA = 'TRANSFERENCIA', 'Transferencia'

if not hasattr(EstadoPagoChoices, 'choices'):
    class EstadoPagoChoices(models.TextChoices):
        PENDIENTE = 'PENDIENTE', 'Pendiente'
        PAGADO = 'PAGADO', 'Pagado'
        CANCELADO = 'CANCELADO', 'Cancelado'

# Mock de los modelos de la app 'core' si no existen, para validación.
# Deberías tener estos modelos definidos correctamente en tu app 'core'.
class PacienteCore(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    nombre_completo = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20)
    email = models.EmailField(max_length=255, unique=True)  # <-- Asegúrate de tener este campo si lo usas en el form

    class Meta:
        app_label = 'core'
        verbose_name = "Paciente (Core)"
        verbose_name_plural = "Pacientes (Core)"

    def __str__(self):
        return self.nombre_completo

class DiagnosticoCore(models.Model):
    descripcion = models.CharField(max_length=255, default="Diagnóstico Ejemplo")
    # Otros campos...
    class Meta:
        app_label = 'core'
        verbose_name = "Diagnóstico (Core)"
        verbose_name_plural = "Diagnósticos (Core)"
    def __str__(self):
        return self.descripcion

class MedicamentoCore(models.Model):
    nombre = models.CharField(max_length=255, default="Medicamento Ejemplo")
    # Otros campos...
    class Meta:
        app_label = 'core'
        verbose_name = "Medicamento (Core)"
        verbose_name_plural = "Medicamentos (Core)"
    def __str__(self):
        return self.nombre


class HorarioAtencion(models.Model):
    dia_semana = models.CharField(
        max_length=10,
        choices=DiaSemanaChoices.choices,
        verbose_name="Día de la Semana"
    )
    hora_inicio = models.TimeField(verbose_name="Hora de Inicio")
    hora_fin = models.TimeField(verbose_name="Hora de Fin")
    intervalo_desde = models.TimeField(verbose_name="Intervalo desde", null=True, blank=True)
    intervalo_hasta = models.TimeField(verbose_name="Intervalo hasta", null=True, blank=True)
    activo = models.BooleanField(default=True, verbose_name="Activo")

    def __str__(self):
        return f"{self.get_dia_semana_display()}" # Usar get_..._display() para choices

    class Meta:
        verbose_name = "Horario de Atención"
        verbose_name_plural = "Horarios de Atención"
        unique_together = ('dia_semana', 'hora_inicio', 'hora_fin')

class CitaMedica(models.Model):
    paciente = models.ForeignKey('core.Paciente', on_delete=models.CASCADE, verbose_name="Paciente", related_name="citas")
    fecha = models.DateField(verbose_name="Fecha de la Cita")
    hora_cita = models.TimeField(verbose_name="Hora de la Cita")
    estado = models.CharField(
        max_length=20, # Ajustado para nombres más largos como CONFIRMADA
        choices=EstadoCitaChoices.choices,
        verbose_name="Estado de la Cita"
    )
    observaciones = models.TextField(verbose_name="Observaciones", blank=True, null=True)

    def __str__(self):
        return f"{self.paciente} - {self.fecha} {self.hora_cita}" # Asume que paciente tiene __str__

    class Meta:
        ordering = ['fecha', 'hora_cita']
        indexes = [
            models.Index(fields=['fecha', 'hora_cita'], name='idx_fecha_hora_cita'), # Nombre de índice más específico
        ]
        verbose_name = "Cita Médica"
        verbose_name_plural = "Citas Médicas"
        unique_together = ('fecha', 'hora_cita')

class Atencion(models.Model):
    paciente = models.ForeignKey(
        'core.Paciente',
        on_delete=models.PROTECT,
        verbose_name="Paciente",
        related_name="atenciones",
        help_text="Paciente que recibe esta atención médica."
    )
    fecha_atencion = models.DateTimeField(
        default=timezone.now, # Cambiado de auto_now_add para permitir modificación si es necesario, o usar auto_now_add
        verbose_name="Fecha de Atención",
        help_text="Fecha y hora en que se registró la atención."
    )
    presion_arterial = models.CharField(
        max_length=20, null=True, blank=True, verbose_name="Presión Arterial", help_text="Ejemplo: 120/80 mmHg."
    )
    pulso = models.PositiveIntegerField(
        null=True, blank=True, verbose_name="Pulso (ppm)", help_text="Pulsaciones por minuto."
    )
    temperatura = models.DecimalField(
        max_digits=4, decimal_places=1, null=True, blank=True, verbose_name="Temperatura (°C)", help_text="Temperatura corporal en grados Celsius."
    )
    frecuencia_respiratoria = models.PositiveIntegerField(
        null=True, blank=True, verbose_name="Frecuencia Respiratoria (rpm)", help_text="Respiraciones por minuto."
    )
    saturacion_oxigeno = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True, verbose_name="Saturación de Oxígeno (%)", help_text="Porcentaje de oxígeno en sangre."
    )
    peso = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True, verbose_name="Peso (kg)", help_text="Peso del paciente en kilogramos."
    )
    altura = models.DecimalField(
        max_digits=4, decimal_places=2, null=True, blank=True, verbose_name="Altura (m)", help_text="Altura del paciente en metros."
    )
    motivo_consulta = models.TextField(
        verbose_name="Motivo de Consulta", help_text="Razón principal por la que el paciente acude a consulta."
    )
    sintomas = models.TextField(
        verbose_name="Síntomas", help_text="Síntomas que presenta el paciente."
    )
    tratamiento = models.TextField(
        verbose_name="Plan de Tratamiento", help_text="Indicaciones o receta entregada al paciente."
    )
    diagnostico = models.ManyToManyField(
        'core.Diagnostico', verbose_name="Diagnósticos", related_name="atenciones", help_text="Diagnósticos clínicos asociados a esta atención.", blank=True # Permitir que no haya diagnósticos
    )
    examen_fisico = models.TextField(
        null=True, blank=True, verbose_name="Examen Físico", help_text="Descripción de hallazgos del examen físico."
    )
    examenes_enviados = models.TextField(
        null=True, blank=True, verbose_name="Exámenes Solicitados", help_text="Exámenes que se han solicitado al paciente."
    )
    comentario_adicional = models.TextField(
        null=True, blank=True, verbose_name="Comentario Adicional", help_text="Observaciones adicionales del profesional de salud."
    )
    es_control = models.BooleanField(
        default=False, verbose_name="¿Es consulta de control?", help_text="Marca si esta atención es parte de un seguimiento."
    )

    class Meta:
        ordering = ['-fecha_atencion']
        verbose_name = "Atención Médica"
        verbose_name_plural = "Atenciones Médicas"

    def __str__(self):
        return f"Atención de {self.paciente} el {self.fecha_atencion.strftime('%Y-%m-%d %H:%M')}"

    @property
    def calcular_imc(self):
        if self.peso and self.altura and self.altura > 0:
            return round(Decimal(self.peso) / (Decimal(self.altura) ** 2), 2) # Usar Decimal
        return None

    @property
    def get_diagnosticos_display(self): # Renombrado para claridad
        return " - ".join([d.descripcion for d in self.diagnostico.all().order_by('descripcion')])

class DetalleAtencion(models.Model):
    atencion = models.ForeignKey(
        Atencion, on_delete=models.CASCADE, verbose_name="Atención Médica", related_name="detalles", help_text="Atención médica asociada a este detalle."
    )
    medicamento = models.ForeignKey(
        'core.Medicamento', on_delete=models.PROTECT, verbose_name="Medicamento", related_name="prescripciones", help_text="Medicamento recetado al paciente."
    )
    cantidad = models.PositiveIntegerField(
        verbose_name="Cantidad", help_text="Unidades del medicamento recetadas."
    )
    prescripcion = models.TextField(
        verbose_name="Prescripción", help_text="Instrucciones para tomar el medicamento."
    )
    duracion_tratamiento = models.PositiveIntegerField(
        verbose_name="Duración del Tratamiento (días)", null=True, blank=True, help_text="Cantidad de días de tratamiento estimado."
    )
    frecuencia_diaria = models.PositiveIntegerField(
        verbose_name="Frecuencia Diaria (veces por día)", null=True, blank=True, help_text="Cuántas veces al día debe tomar el medicamento."
    )

    class Meta:
        ordering = ['atencion']
        verbose_name = "Detalle de Atención"
        verbose_name_plural = "Detalles de Atención"

    def __str__(self):
        return f"{self.medicamento} para {self.atencion.paciente}"

class ServiciosAdicionales(models.Model):
    nombre_servicio = models.CharField(
        max_length=255, verbose_name="Nombre del Servicio", help_text="Ejemplo: Radiografía, Laboratorio clínico, Procedimiento menor."
    )
    costo_servicio = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Costo del Servicio", help_text="Costo unitario del servicio en dólares. Ejemplo: 25.00"
    )
    descripcion = models.TextField(
        null=True, blank=True, verbose_name="Descripción del Servicio", help_text="Descripción opcional del servicio. Ejemplo: Examen de sangre de rutina."
    )
    activo = models.BooleanField(
        default=True, verbose_name="Activo", help_text="Marca si el servicio adicional está disponible para agendar o prescribir."
    )

    class Meta:
        ordering = ['nombre_servicio']
        verbose_name = "Servicio Adicional"
        verbose_name_plural = "Servicios Adicionales"

    def __str__(self):
        return self.nombre_servicio

class Pago(models.Model):
    atencion = models.ForeignKey(
        Atencion, on_delete=models.PROTECT, verbose_name="Atención", related_name="pagos", null=True, blank=True
    )
    metodo_pago = models.CharField(
        max_length=20, choices=MetodoPagoChoices.choices, verbose_name="Método de Pago"
    )
    monto_total = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Monto Total", default=Decimal('0.00') # Default para que no sea None
    )
    estado = models.CharField(
        max_length=20, choices=EstadoPagoChoices.choices, default=EstadoPagoChoices.PENDIENTE, verbose_name="Estado"
    )
    fecha_pago = models.DateTimeField(verbose_name="Fecha de Pago", null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    nombre_pagador = models.CharField(
        max_length=100, verbose_name="Nombre del Pagador", blank=True, null=True
    )
    referencia_externa = models.CharField(
        max_length=100, verbose_name="Referencia Externa", blank=True, null=True, help_text="ID de transacción PayPal, etc."
    )
    evidencia_pago = models.ImageField(
        upload_to='doctor/evidencia_pagos/', verbose_name="Evidencia de Pago", blank=True, null=True, help_text="Captura de pantalla o comprobante del pago"
    )
    observaciones = models.TextField(verbose_name="Observaciones", blank=True, null=True)
    activo = models.BooleanField(default=True, verbose_name="Activo")

    def __str__(self):
        atencion_str = f"Atención ID: {self.atencion.id}" if self.atencion else "Sin atención asociada"
        return f"Pago ID: {self.id} - {atencion_str} - Monto: {self.monto_total} - Estado: {self.get_estado_display()}"

    def save(self, *args, **kwargs):
        if self.estado == EstadoPagoChoices.PAGADO and not self.fecha_pago:
            self.fecha_pago = timezone.now()
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-fecha_creacion']
        verbose_name = "Pago"
        verbose_name_plural = "Pagos"

class DetallePago(models.Model):
    pago = models.ForeignKey(
        Pago, on_delete=models.CASCADE, verbose_name="Pago", related_name="detalles", help_text="Pago al que corresponde este detalle de cobro."
    )
    servicio_adicional = models.ForeignKey(
        ServiciosAdicionales, on_delete=models.PROTECT, verbose_name="Servicio", related_name="detalles_pago", help_text="Servicio adicional cobrado."
    )
    cantidad = models.PositiveIntegerField(
        default=1, verbose_name="Cantidad", help_text="Cantidad del servicio facturado."
    )
    precio_unitario = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Precio Unitario", help_text="Precio por unidad del servicio.", null=True, blank=True
    )
    subtotal = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Subtotal", editable=False, help_text="Subtotal (cantidad * precio con descuento)."
    )
    descuento_porcentaje = models.DecimalField(
        max_digits=5, decimal_places=2, default=Decimal('0.00'), verbose_name="Descuento %", help_text="Descuento sobre precio base (0-100)."
    )
    aplica_seguro = models.BooleanField(
        default=False, verbose_name="Aplica Seguro", help_text="¿Servicio cubierto por seguro?"
    )
    valor_seguro = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Valor Cubierto por Seguro", help_text="Valor cubierto si aplica seguro."
    )
    descripcion_seguro = models.CharField(
        max_length=255, null=True, blank=True, verbose_name="Descripción del Seguro", help_text="Nombre del seguro utilizado."
    )

    def save(self, *args, **kwargs):
        current_precio_unitario = self.precio_unitario
        if current_precio_unitario is None and self.servicio_adicional:
            current_precio_unitario = self.servicio_adicional.costo_servicio

        precio_a_usar = current_precio_unitario
        if self.aplica_seguro and self.valor_seguro is not None:
            precio_a_usar = self.valor_seguro

        if precio_a_usar is None:
            precio_a_usar = Decimal('0.00')

        descuento_monto = (self.descuento_porcentaje / Decimal(100)) * precio_a_usar
        precio_final_unitario = precio_a_usar - descuento_monto
        self.subtotal = round(precio_final_unitario * self.cantidad, 2)

        super().save(*args, **kwargs)
        # La actualización del total del Pago se maneja en las vistas o signals.

    def __str__(self):
        return f"{self.cantidad} x {self.servicio_adicional} - Subtotal: {self.subtotal}"

    def actualizar_total_pago(self):
        if self.pago_id:
            total_calculado = self.pago.detalles.aggregate(
                total_sum=models.Sum('subtotal')
            )['total_sum'] or Decimal('0.00')

            self.pago.monto_total = round(total_calculado, 2)
            self.pago.save(update_fields=['monto_total'])

    class Meta:
        verbose_name = "Detalle de Pago"
        verbose_name_plural = "Detalles de Pago"

class Patient (models.Model): # Este modelo Patient parece ser de la app 'doctor'
    Primer_nombre= models.CharField(verbose_name='Nombres', max_length=150)
    apellido=models.CharField(verbose_name='Apellidos', max_length=150)
    dni = models.CharField(verbose_name='Cédula', max_length=13, unique=True)
    birth_date = models.DateField(verbose_name='Fecha de Nacimiento')
    gender = models.CharField(
        verbose_name='Género', max_length=1, choices=[('M', 'Masculino'), ('F', 'Femenino'), ('O', 'Otro')]
    )
    phone = models.CharField(verbose_name='Teléfono', max_length=15, null=True, blank=True)
    email = models.EmailField(verbose_name='Email', null=True, blank=True)
    address = models.CharField(verbose_name='Dirección', max_length=200, null=True, blank=True)
    blood_type = models.CharField(
        verbose_name='Tipo de Sangre', max_length=3,
        choices=[('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'),
                 ('AB+', 'AB+'), ('AB-', 'AB-'), ('O+', 'O+'), ('O-', 'O-')],
        null=True, blank=True
    )
    created_at = models.DateTimeField(verbose_name='Fecha de Registro', auto_now_add=True)

    def __str__(self):
        return f"{self.Primer_nombre} {self.apellido} ({self.dni})"

    class Meta:
        verbose_name = 'Paciente (Doctor App)' # Clarificando que es de esta app
        verbose_name_plural = 'Pacientes (Doctor App)'
        ordering = ['apellido', 'Primer_nombre']

class Diagnosis(models.Model): # Este modelo Diagnosis parece ser de la app 'doctor'
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, verbose_name='Paciente', related_name='diagnoses_doctor_app') # related_name cambiado
    date = models.DateTimeField(verbose_name='Fecha y Hora', auto_now_add=True)
    description = models.TextField(verbose_name='Descripción')
    icd_code = models.CharField(verbose_name='Código CIE', max_length=10, null=True, blank=True)
    notes = models.TextField(verbose_name='Notas Adicionales', null=True, blank=True)
    is_active = models.BooleanField(verbose_name='Activo', default=True)

    def __str__(self):
        return f"Diagnóstico (App) de {self.patient} - {self.date.strftime('%d/%m/%Y')}"

    class Meta:
        verbose_name = 'Diagnóstico (Doctor App)' # Clarificando
        verbose_name_plural = 'Diagnósticos (Doctor App)'
        ordering = ['-date']
