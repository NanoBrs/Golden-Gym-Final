from django import forms
from .models import Cliente,Encargado,Novedad,Reporte,Plan

class ClienteForm(forms.ModelForm):
    membresia = forms.ChoiceField(
        choices=Cliente.PLANES_MEMBRESIA,
        widget=forms.RadioSelect,  # Opción para seleccionar un solo plan
        label="PLAN"
    )

    class Meta:
        model = Cliente
        fields = ['nombre', 'apellido', 'rut', 'correo', 'membresia']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'style': 'background-color: #666; color: white;'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control', 'style': 'background-color: #666; color: white;'}),
            'rut': forms.TextInput(attrs={'class': 'form-control', 'style': 'background-color: #666; color: white;'}),
            'correo': forms.EmailInput(attrs={'class': 'form-control', 'style': 'background-color: #666; color: white;'}),
        }

class EncargadoForm(forms.ModelForm):
    # Definir el formulario utilizando el modelo Encargado
    class Meta:
        model = Encargado
        fields = ['nombre', 'apellido', 'rut', 'correo', 'usuario', 'contraseña']
        
        widgets = {
            'contraseña': forms.PasswordInput(attrs={'placeholder': 'Contraseña'}),  # Campo de contraseña, muestra un placeholder
        }

    # Método adicional para realizar validaciones personalizadas si es necesario
    def clean_rut(self):
        rut = self.cleaned_data.get('rut')
        # Aquí puedes agregar validaciones para el RUT
        return rut

    def clean_correo(self):
        correo = self.cleaned_data.get('correo')
        # Aquí puedes agregar validaciones adicionales para el correo
        return correo

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