#!/usr/bin/env python3

from django import forms
from django.contrib.auth.models import Group

# Formulario para el modelo Group de Django
class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={
                "placeholder": "Ingrese nombre del grupo",
                "id": "id_name",
                "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
            }),
        }
        labels = {
            "name": "Nombre del Grupo",
        }
        error_messages = {
            "name": {
                "unique": "Ya existe un grupo con este nombre.",
            },
        }

    def clean_name(self):
        name = self.cleaned_data.get("name")
        return name.upper()
