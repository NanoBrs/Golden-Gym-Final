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