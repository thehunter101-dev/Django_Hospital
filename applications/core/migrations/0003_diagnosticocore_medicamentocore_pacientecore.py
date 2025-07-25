# Generated by Django 5.2 on 2025-07-04 11:46

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0002_tipogasto_remove_doctor_duracion_cita_and_more"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="DiagnosticoCore",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "descripcion",
                    models.CharField(default="Diagnóstico Ejemplo", max_length=255),
                ),
            ],
            options={
                "verbose_name": "Diagnóstico (Core)",
                "verbose_name_plural": "Diagnósticos (Core)",
            },
        ),
        migrations.CreateModel(
            name="MedicamentoCore",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "nombre",
                    models.CharField(default="Medicamento Ejemplo", max_length=255),
                ),
            ],
            options={
                "verbose_name": "Medicamento (Core)",
                "verbose_name_plural": "Medicamentos (Core)",
            },
        ),
        migrations.CreateModel(
            name="PacienteCore",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("nombre_completo", models.CharField(max_length=100)),
                ("telefono", models.CharField(max_length=20)),
                ("email", models.EmailField(max_length=255, unique=True)),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Paciente (Core)",
                "verbose_name_plural": "Pacientes (Core)",
            },
        ),
    ]
