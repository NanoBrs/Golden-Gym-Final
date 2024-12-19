from django import forms
from .models import Cliente,Encargado,Novedad,Reporte,Plan,Inscripcion

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre', 'apellido', 'rut', 'correo', 'suscripcion_activa']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Deshabilitar el campo encargado si es necesario, pero no lo incluyas en 'fields'
        if self.instance.pk:  # Si estamos editando un cliente existente
            # No deberías estar accediendo al campo 'encargado' aquí, ya que no está en 'fields'
            # Si lo quieres deshabilitar en el formulario, puedes hacerlo manualmente si fuera necesario
            pass


class EncargadoForm(forms.ModelForm):
    class Meta:
        model = Encargado
        fields = ['username', 'first_name', 'last_name', 'rut', 'email', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }

    def save(self, commit=True):
        encargado = super().save(commit=False)
        if self.cleaned_data['password']:
            encargado.set_password(self.cleaned_data['password'])  # Se asegura de que la contraseña sea almacenada de forma segura
        if commit:
            encargado.save()
        return encargado

class NovedadForm(forms.ModelForm):
    class Meta:
        model = Novedad
        fields = ['titulo', 'contenido', 'imagen' ,'ruta_video']  # Incluye ambos campos

class ReporteForm(forms.ModelForm):
    class Meta:
        model = Reporte
        fields = ['fecha', 'peso_actual', 'altura', 'press_banca', 'sentadilla', 'peso_muerto']
        widgets = {
            'fecha': forms.SelectDateWidget(years=range(2024, 2025)),
        }

class PlanForm(forms.ModelForm):
    class Meta:
        model = Plan
        fields = ['nombre', 'precio', 'duracion_dias']


class InscripcionForm(forms.ModelForm):
    class Meta:
        model = Inscripcion
        fields = ['cliente', 'plan', 'monto_pagado', 'metodo_pago']  # Sin 'encargado' porque lo asignamos automáticamente
        widgets = {
            'cliente': forms.Select(attrs={'class': 'form-control'}),
            'plan': forms.Select(attrs={'class': 'form-control'}),
            'monto_pagado': forms.NumberInput(attrs={'class': 'form-control'}),
            'metodo_pago': forms.Select(choices=Inscripcion.METODOS_PAGO, attrs={'class': 'form-control'}),
        }
